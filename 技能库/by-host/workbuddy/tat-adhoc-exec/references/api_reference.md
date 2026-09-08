# 腾讯云 TAT API 速查

## 接口说明

- 服务：`tat.tencentcloudapi.com`
- 版本：`2020-10-28`
- 签名：TC3-HMAC-SHA256

## 常用接口

### CreateCommand
创建命令，返回 `CommandId`。

```json
{
  "Content": "base64(shell_script)",
  "CommandName": "name",
  "CommandType": "SHELL",
  "WorkingDirectory": "/root",
  "Timeout": 300,
  "Username": "root"
}
```

### InvokeCommand
调用命令到实例，返回 `InvocationId` 和 `TaskIdSet`。

```json
{
  "CommandId": "cmd-xxx",
  "InstanceIds": ["lhins-xxx"]
}
```

### DescribeInvocationTasks
查询任务状态。正确参数：

```json
{
  "Filters": [{"Name": "invocation-id", "Values": ["inv-xxx"]}],
  "Limit": 100
}
```

注意：不可使用 `TaskIds` 参数，会报 `UnknownParameter`。

## 输出解码

`TaskResult.Output` 是 base64 字符串，需解码：

```python
base64.b64decode(output_b64).decode("utf-8", errors="replace")
```
