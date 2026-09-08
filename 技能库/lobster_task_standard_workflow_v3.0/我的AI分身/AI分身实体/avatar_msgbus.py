# avatar_msgbus.py · P1 多Agent编排（读信号文件）
# 监听 signal_exchange/doing/*.json，读一条 → 打回显 → 移到 done/
import json, os, glob, shutil, datetime, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DOING = os.path.join(HERE, "signal_exchange", "doing")
DONE  = os.path.join(HERE, "signal_exchange", "done")
os.makedirs(DOING, exist_ok=True); os.makedirs(DONE, exist_ok=True)

def respond_one(f):
    try:
        with open(f, "r", encoding="utf-8") as fh:
            sig = json.load(fh)
        task = sig.get("task") or sig.get("content") or sig.get("cmd") or ""
        print(f"[{datetime.datetime.now():%H:%M:%S}] 读到信号: {sig.get('id','?')} -> {task[:60]}")
        print(f"  回应: 汤小龙收到并已响应: {task[:80]}")
        sig["response"] = f"汤小龙已响应: {task[:80]}"
        sig["status"] = "done"
        sig["handled_at"] = datetime.datetime.now().isoformat()
        dest = os.path.join(DONE, os.path.basename(f))
        with open(dest, "w", encoding="utf-8") as fh:
            json.dump(sig, fh, ensure_ascii=False, indent=2)
        os.remove(f)
        return True
    except Exception as e:
        print("处理失败:", e)
        return False

def main():
    once = "--once" in sys.argv
    while True:
        files = sorted(glob.glob(os.path.join(DOING, "*.json")))
        n = 0
        for f in files:
            if respond_one(f): n += 1
        if once or n == 0:
            if once: print("once 完成，共处理", n, "条"); break
        import time; time.sleep(3)

if __name__ == "__main__":
    main()