#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""腾讯云 TAT 任意命令执行器（复用 tat_deploy.py 的签名逻辑）
用法: python tat_exec.py <shell_script_path> [--name <command_name>]
"""
import os, sys, json, time, hmac, hashlib, base64, argparse
from urllib import request, error
from datetime import datetime, timezone

CRED_FILE = r"C:\Users\Administrator\WorkBuddy\2026-07-18-14-16-19\secrets\tencent.env"
PUBLIC_IP = "43.161.202.206"
REGION = "ap-hongkong"


def load_env(path):
    creds = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip()
    return creds


def tc3_sign(secret_id, secret_key, service, payload_json, action, version):
    timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")
    host = f"{service}.tencentcloudapi.com"
    ct = "application/json"
    canonical_request = (
        "POST\n/\n\n"
        f"content-type:{ct}\nhost:{host}\n\n"
        "content-type;host\n"
        f"{hashlib.sha256(payload_json.encode('utf-8')).hexdigest()}"
    )
    credential_scope = f"{date}/{service}/tc3_request"
    string_to_sign = (
        "TC3-HMAC-SHA256\n"
        f"{timestamp}\n"
        f"{credential_scope}\n"
        f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    )
    secret_date = hmac.new(f"TC3{secret_key}".encode("utf-8"), date.encode("utf-8"), hashlib.sha256).digest()
    secret_service = hmac.new(secret_date, service.encode("utf-8"), hashlib.sha256).digest()
    secret_signing = hmac.new(secret_service, b"tc3_request", hashlib.sha256).digest()
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    auth = (
        "TC3-HMAC-SHA256 "
        f"Credential={secret_id}/{credential_scope}, "
        "SignedHeaders=content-type;host, "
        f"Signature={signature}"
    )
    return {
        "Content-Type": ct,
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Version": version,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Region": REGION,
        "Authorization": auth,
    }


def call_api(secret_id, secret_key, service, payload, action, version):
    payload_json = json.dumps(payload)
    headers = tc3_sign(secret_id, secret_key, service, payload_json, action, version)
    req = request.Request(f"https://{service}.tencentcloudapi.com/", data=payload_json.encode("utf-8"), headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code}: {body}") from e


def find_instance_id(cred):
    resp = call_api(
        cred["SecretId"], cred["SecretKey"], "lighthouse",
        {"Limit": 100, "Offset": 0},
        "DescribeInstances", "2020-03-24",
    )
    if resp.get("Response", {}).get("Error"):
        raise RuntimeError(f"Lighthouse API 错误: {resp['Response']['Error']}")
    for ins in resp["Response"].get("InstanceSet", []):
        for addr in ins.get("PublicAddresses", []):
            if addr == PUBLIC_IP:
                return ins["InstanceId"]
        if PUBLIC_IP in ins.get("PublicIpAddresses", []) or ins.get("PublicIpAddress") == PUBLIC_IP:
            return ins["InstanceId"]
    raise RuntimeError(f"未找到公网IP为 {PUBLIC_IP} 的实例")


def create_command(cred, script_path, name, timeout=300):
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    payload = {
        "Content": encoded,
        "CommandName": name,
        "CommandType": "SHELL",
        "WorkingDirectory": "/root",
        "Timeout": timeout,
        "Username": "root",
        "Description": f"TAT exec {name}",
    }
    resp = call_api(cred["SecretId"], cred["SecretKey"], "tat", payload, "CreateCommand", "2020-10-28")
    if resp.get("Response", {}).get("Error"):
        raise RuntimeError(f"CreateCommand 错误: {resp['Response']['Error']}")
    return resp["Response"]["CommandId"]


def invoke_command(cred, command_id, instance_id):
    resp = call_api(
        cred["SecretId"], cred["SecretKey"], "tat",
        {"CommandId": command_id, "InstanceIds": [instance_id]},
        "InvokeCommand", "2020-10-28",
    )
    if resp.get("Response", {}).get("Error"):
        raise RuntimeError(f"InvokeCommand 错误: {resp['Response']['Error']}")
    return resp["Response"].get("InvocationId", "")


def poll_task(cred, invocation_id, max_seconds=300):
    start = time.time()
    while time.time() - start < max_seconds:
        r = call_api(
            cred["SecretId"], cred["SecretKey"], "tat",
            {
                "Filters": [{"Name": "invocation-id", "Values": [invocation_id]}],
                "Limit": 100,
            },
            "DescribeInvocationTasks", "2020-10-28",
        )
        if r.get("Response", {}).get("Error"):
            print(f"[WARN] 查询出错: {r['Response']['Error']}; 10秒后重试...")
            time.sleep(10)
            continue
        tasks = r["Response"].get("InvocationTaskSet", [])
        if not tasks:
            print("[INFO] 任务尚未就绪，10秒后重试...")
            time.sleep(10)
            continue
        task = tasks[0]
        status = task.get("TaskStatus", "PENDING")
        print(f"[INFO] 任务状态: {status} (已耗时 {int(time.time()-start)}s)")
        if status in ("SUCCESS", "FAILED", "TIMEOUT", "TERMINATED"):
            return task
        time.sleep(15)
    raise RuntimeError("轮询超时")


def decode_output(task):
    out = task.get("TaskResult", {}).get("Output", "")
    if not out:
        return "(无输出)"
    try:
        return base64.b64decode(out).decode("utf-8", errors="replace")
    except Exception as e:
        return f"[解码失败: {e}]"


def main():
    parser = argparse.ArgumentParser(description="TAT 任意命令执行器")
    parser.add_argument("script", help="要执行的本地 shell 脚本路径")
    parser.add_argument("--name", default="adhoc_command", help="TAT 命令名称")
    parser.add_argument("--timeout", type=int, default=300, help="TAT 命令超时(秒)")
    args = parser.parse_args()

    if not os.path.isfile(args.script):
        print(f"[ERROR] 脚本不存在: {args.script}")
        return 1

    cred = load_env(CRED_FILE)
    print(f"[{datetime.now().isoformat()}] TAT 执行启动: {args.name}")
    print(f"[INFO] 已加载凭证: SecretId={cred.get('SecretId','')[:6]}...")

    instance_id = find_instance_id(cred)
    command_id = create_command(cred, args.script, args.name, args.timeout)
    invocation_id = invoke_command(cred, command_id, instance_id)
    print(f"[INFO] InvocationId={invocation_id}")

    task = poll_task(cred, invocation_id, max_seconds=args.timeout)
    output = decode_output(task)
    task_result = task.get("TaskResult", {})

    print("\n==================== 执行结果 ====================")
    print(f"状态: {task.get('TaskStatus')}")
    print(f"退出码: {task_result.get('ExitCode', 'N/A')}")
    print("\n--- 输出 ---")
    print(output[:4000])
    if len(output) > 4000:
        print(f"\n... 输出共 {len(output)} 字符，已截断 ...")

    return 0 if task.get("TaskStatus") == "SUCCESS" and task_result.get("ExitCode") == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
