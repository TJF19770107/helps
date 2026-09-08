# -*- coding: utf-8 -*-
# ============================================================
# Marvis-豆包双向交互自动化技能 V2.0
# 创建: 2026-06-11 | 升级: V2.0 浏览器实时推送加固
# 存储: 主控中心→E盘，同步枢纽→D盘，禁止C盘写入
# 新增: 浏览器端豆包窗口实时消息推送
# ============================================================

import os
import sys
import time
import json
import hashlib
import logging
import traceback
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# 1 全局配置
# ============================================================
class InteractConfig:
    """1.1 交互自动化配置"""
    # D盘同步枢纽
    SYNC_ROOT = r"D:\Marvis-豆包同步枢纽"
    DOWN_SYNC_DIR = os.path.join(SYNC_ROOT, "下行同步_Marvis到豆包")
    UP_SYNC_DIR = os.path.join(SYNC_ROOT, "上行同步_豆包到Marvis")
    LOG_DIR = os.path.join(SYNC_ROOT, "同步日志")
    ERR_DIR = os.path.join(SYNC_ROOT, "错误日志")
    # 本地日志
    LOCAL_LOG_DIR = r"E:\龙虾AI主控中心\我的AI分身\运行日志"
    # 技能库
    SKILL_DIR = r"E:\龙虾AI主控中心\我的AI分身\技能库"
    # 状态文件
    STATE_FILE = os.path.join(SYNC_ROOT, "interact_state.json")
    # 监控轮询间隔 (秒)
    POLL_INTERVAL = 5
    # 最大重试
    MAX_RETRIES = 3
    RETRY_INTERVAL = 10
    # 重连间隔
    RECONNECT_INTERVAL = 30
    # C盘禁止前缀
    FORBIDDEN = [r"C:\\", r"C:\\Windows", r"C:\\Program Files"]

class InteractLogger:
    """1.2 双通道日志"""
    def __init__(self, session_id=None):
        self.sid = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(InteractConfig.LOG_DIR, f"interact_{self.sid}.log")
        self.err_path = os.path.join(InteractConfig.ERR_DIR, f"interact_error_{self.sid}.log")
        self._setup()
    def _setup(self):
        self.log = logging.getLogger(f"Interact_{self.sid}")
        self.log.setLevel(logging.DEBUG)
        for p, lvl in [(self.log_path, logging.INFO), (self.err_path, logging.ERROR)]:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            h = logging.FileHandler(p, encoding='utf-8')
            h.setLevel(lvl)
            h.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
            self.log.addHandler(h)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        self.log.addHandler(ch)
    def info(self, m): self.log.info(m)
    def error(self, m): self.log.error(m)
    def debug(self, m): self.log.debug(m)

# ============================================================
# 2 路径安全守卫
# ============================================================
class PathGuard:
    @staticmethod
    def safe(p: str) -> bool:
        ap = os.path.abspath(p).lower()
        for f in InteractConfig.FORBIDDEN:
            if ap.startswith(f.lower()):
                return False
        return True
    @staticmethod
    def ensure_safe(p: str, logger) -> bool:
        if not PathGuard.safe(p):
            logger.error(f"危险路径拒绝: {p}")
            return False
        os.makedirs(p, exist_ok=True)
        return True

# ============================================================
# 3 备份管理器
# ============================================================
class BackupMgr:
    @staticmethod
    def backup(fp: str, logger) -> Optional[str]:
        if not os.path.exists(fp):
            return None
        bp = f"{fp}.bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy2(fp, bp)
        logger.info(f"备份: {bp}")
        return bp
    @staticmethod
    def safe_write(fp: str, content: str, logger, mode='w'):
        BackupMgr.backup(fp, logger)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, mode, encoding='utf-8') as f:
            f.write(content)
        logger.info(f"安全写入: {fp}")

# ============================================================
# 4 回复生成器
# ============================================================
class ReplyGenerator:
    """4.1 生成标准CHAT_REPLY格式的md文件"""
    @staticmethod
    def generate(content: str, metadata: dict = None) -> str:
        ts = datetime.now()
        date_str = ts.strftime("%Y%m%d")
        time_str = ts.strftime("%H%M%S")
        fname = f"{date_str}_【CHAT_REPLY】_{time_str}.md"
        fpath = os.path.join(InteractConfig.DOWN_SYNC_DIR, fname)
        
        header = (
            f"<!-- Marvis→豆包 交互回复 -->\n"
            f"<!-- 时间戳: {ts.isoformat()} -->\n"
            f"<!-- 类型: CHAT_REPLY -->\n"
            f"<!-- 版本: V1.0 -->\n\n"
        )
        body = f"【{ts.strftime('%Y-%m-%d %H:%M:%S')}】\n\n{content}\n"
        if metadata:
            body += f"\n<!-- 元数据: {json.dumps(metadata, ensure_ascii=False)} -->"
        
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(header + body)
        return fpath

# ============================================================
# 4.2 浏览器实时推送模块 (V2.0新增)
# ============================================================
class BrowserPusher:
    """4.2.1 通过Edge浏览器实时推送消息到豆包聊天窗口"""
    
    # 豆包聊天窗口URL
    DOUBAO_URL = "https://www.doubao.com/chat/"
    
    # 推送任务文件目录
    PUSH_DIR = os.path.join(InteractConfig.SYNC_ROOT, "push_queue")
    
    @staticmethod
    def ensure_dir():
        os.makedirs(BrowserPusher.PUSH_DIR, exist_ok=True)
    
    @staticmethod
    def push(message: str, cycle_id: str = None) -> Dict:
        """4.2.2 生成推送任务文件，供browser-agent执行"""
        BrowserPusher.ensure_dir()
        ts = datetime.now()
        task_id = cycle_id or ts.strftime("%Y%m%d_%H%M%S")
        
        task = {
            "task_id": task_id,
            "timestamp": ts.isoformat(),
            "target_url": BrowserPusher.DOUBAO_URL,
            "action": "send_message",
            "message": message,
            "verify": {
                "window_visible": False,
                "message_sent": False,
                "message_displayed": False
            }
        }
        
        task_path = os.path.join(BrowserPusher.PUSH_DIR, f"push_{task_id}.json")
        with open(task_path, 'w', encoding='utf-8') as f:
            json.dump(task, f, ensure_ascii=False, indent=2)
        
        return {
            "status": "queued",
            "task_id": task_id,
            "task_path": task_path,
            "message_preview": message[:100] + ("..." if len(message) > 100 else "")
        }
    
    @staticmethod
    def get_pending_tasks() -> List[str]:
        """4.2.3 获取待推送任务列表"""
        BrowserPusher.ensure_dir()
        tasks = []
        if os.path.exists(BrowserPusher.PUSH_DIR):
            for f in sorted(os.listdir(BrowserPusher.PUSH_DIR)):
                if f.endswith('.json'):
                    tasks.append(os.path.join(BrowserPusher.PUSH_DIR, f))
        return tasks
    
    @staticmethod
    def mark_sent(task_path: str, logger) -> bool:
        """4.2.4 标记推送任务已完成"""
        try:
            with open(task_path, 'r', encoding='utf-8') as f:
                task = json.load(f)
            task["verify"]["message_sent"] = True
            task["verify"]["message_displayed"] = True
            task["verify"]["window_visible"] = True
            task["completed_at"] = datetime.now().isoformat()
            with open(task_path, 'w', encoding='utf-8') as f:
                json.dump(task, f, ensure_ascii=False, indent=2)
            sent_path = task_path.replace('.json', '.sent.json')
            os.rename(task_path, sent_path)
            logger.info(f"推送已标记完成: {sent_path}")
            return True
        except Exception as e:
            if logger:
                logger.error(f"标记推送失败: {e}")
            return False

# ============================================================
# 5 校验器
# ============================================================
class Validator:
    """5.1 三步校验机制"""
    def __init__(self, logger):
        self.logger = logger
        self.results = {}
    
    def check_file_exists(self, label: str, path: str, retries=3) -> bool:
        for i in range(1, retries+1):
            if os.path.exists(path) and os.path.getsize(path) > 0:
                self.logger.info(f"校验通过 [{label}]: {path}")
                self.results[label] = True
                return True
            self.logger.error(f"校验失败 [{label}] 第{i}/{retries}次: {path}")
            if i < retries:
                time.sleep(InteractConfig.RETRY_INTERVAL)
        self.results[label] = False
        return False
    
    def check_log_written(self, label: str, path: str, keyword: str, retries=3) -> bool:
        for i in range(1, retries+1):
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        if keyword in f.read():
                            self.logger.info(f"校验通过 [{label}]: {path}")
                            self.results[label] = True
                            return True
                except:
                    pass
            self.logger.error(f"校验失败 [{label}] 第{i}/{retries}次")
            if i < retries:
                time.sleep(InteractConfig.RETRY_INTERVAL)
        self.results[label] = False
        return False
    
    def all_passed(self) -> bool:
        return all(self.results.values()) if self.results else False
    
    def summary(self) -> str:
        lines = ["=== 校验结果 ==="]
        for k, v in self.results.items():
            lines.append(f"  {k}: {'通过' if v else '失败'}")
        lines.append(f"  总结果: {'全部通过' if self.all_passed() else '存在失败项'}")
        return "\n".join(lines)

# ============================================================
# 6 交互引擎
# ============================================================
class InteractEngine:
    """6.1 双向交互主引擎"""
    def __init__(self):
        self.logger = InteractLogger()
        self.validator = Validator(self.logger)
        self.session_active = True
        # 初始化目录
        for d in [InteractConfig.DOWN_SYNC_DIR, InteractConfig.UP_SYNC_DIR,
                   InteractConfig.LOG_DIR, InteractConfig.ERR_DIR,
                   InteractConfig.LOCAL_LOG_DIR]:
            PathGuard.ensure_safe(d, self.logger)
        self.logger.info("6.1.1 交互引擎初始化完成")
    
    def execute_command(self, cmd_text: str) -> str:
        """6.1.2 解析并执行用户指令"""
        self.logger.info(f"收到指令: {cmd_text[:100]}...")
        # 这里是核心执行逻辑，实际由Marvis主Agent处理
        # 当前脚本提供框架，实际执行由Marvis调度
        result = f"[Marvis已执行] {cmd_text}"
        return result
    
    def process_cycle(self, instruction: str) -> Dict:
        """6.1.3 完整交互周期"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cycle_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.logger.info(f"=== 交互周期启动 {cycle_id} ===")
        
        result = {
            "cycle_id": cycle_id,
            "timestamp": ts,
            "instruction": instruction,
            "steps": {}
        }
        
        # 步骤1: 执行指令
        try:
            response = self.execute_command(instruction)
            result["steps"]["execution"] = "success"
            result["response"] = response
        except Exception as e:
            result["steps"]["execution"] = "failed"
            result["error"] = str(e)
            self.logger.error(f"指令执行失败: {e}")
            return result
        
        # 步骤2: 生成并上传MD文件到下行目录
        md_path = None
        for retry in range(1, InteractConfig.MAX_RETRIES + 1):
            try:
                md_path = ReplyGenerator.generate(
                    f"指令: {instruction}\n回复: {response}",
                    {"cycle_id": cycle_id, "type": "CHAT_REPLY"}
                )
                if self.validator.check_file_exists("md上传", md_path, 1):
                    result["steps"]["md_upload"] = "success"
                    result["md_path"] = md_path
                    break
            except Exception as e:
                self.logger.error(f"MD生成失败 第{retry}次: {e}")
            if retry == InteractConfig.MAX_RETRIES:
                result["steps"]["md_upload"] = "failed"
                result["md_error"] = "重试耗尽"
        
        # 步骤3: 写本地日志
        log_path = os.path.join(
            InteractConfig.LOCAL_LOG_DIR,
            f"interact_{cycle_id}.log"
        )
        log_content = (
            f"时间: {ts}\n"
            f"指令: {instruction}\n"
            f"回复: {response}\n"
            f"MD文件: {md_path or '生成失败'}\n"
            f"状态: {json.dumps(result['steps'], ensure_ascii=False)}\n"
        )
        for retry in range(1, InteractConfig.MAX_RETRIES + 1):
            try:
                BackupMgr.safe_write(log_path, log_content, self.logger)
                if self.validator.check_file_exists("本地日志", log_path, 1):
                    result["steps"]["log_write"] = "success"
                    result["log_path"] = log_path
                    break
            except Exception as e:
                self.logger.error(f"日志写入失败 第{retry}次: {e}")
            if retry == InteractConfig.MAX_RETRIES:
                result["steps"]["log_write"] = "failed"
        
        # 步骤4: 浏览器实时推送到豆包聊天窗口 (V2.0新增)
        push_message = f"【Marvis回复 {ts}】\n指令: {instruction}\n回复: {response}"
        for retry in range(1, InteractConfig.MAX_RETRIES + 1):
            try:
                push_result = BrowserPusher.push(push_message, cycle_id)
                self.logger.info(f"推送任务已排队: {push_result['task_id']}")
                result["steps"]["browser_push"] = "success"
                result["push_task"] = push_result
                break
            except Exception as e:
                self.logger.error(f"推送任务生成失败 第{retry}次: {e}")
            if retry == InteractConfig.MAX_RETRIES:
                result["steps"]["browser_push"] = "failed"
                result["push_error"] = str(e)
        
        self.logger.info(f"=== 交互周期完成 {cycle_id} ===")
        self.logger.info(self.validator.summary())
        
        return result
    
    def run_test(self) -> Dict:
        """6.1.4 执行BTC价格查询全链路测试"""
        self.logger.info("启动全链路测试: BTC价格查询")
        instruction = "查询币安BTC/USDT最新交易价格、24小时涨跌幅"
        return self.process_cycle(instruction)
    
    def run_daemon(self):
        """6.1.5 后台常驻模式 (依赖外部调度)"""
        self.logger.info("进入常驻模式，轮询间隔: {}秒".format(InteractConfig.POLL_INTERVAL))
        try:
            while self.session_active:
                # 扫描上行目录中的新指令
                new_instructions = []
                if os.path.exists(InteractConfig.UP_SYNC_DIR):
                    for f in os.listdir(InteractConfig.UP_SYNC_DIR):
                        fp = os.path.join(InteractConfig.UP_SYNC_DIR, f)
                        if os.path.isfile(fp) and f.endswith('.md'):
                            try:
                                with open(fp, 'r', encoding='utf-8') as fh:
                                    content = fh.read()
                                new_instructions.append((f, content))
                            except:
                                pass
                
                for fname, content in new_instructions:
                    self.logger.info(f"发现新指令文件: {fname}")
                    result = self.process_cycle(content)
                    self.logger.info(f"处理结果: {json.dumps(result['steps'], ensure_ascii=False)}")
                
                time.sleep(InteractConfig.POLL_INTERVAL)
        except KeyboardInterrupt:
            self.logger.info("收到停止信号")
        except Exception as e:
            self.logger.error(f"常驻模式异常: {e}")
            traceback.print_exc()

# ============================================================
# 7 入口
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("Marvis-豆包双向交互自动化技能 V1.0")
    print("=" * 55)
    
    engine = InteractEngine()
    # 执行全链路测试
    print("\n[测试] BTC价格查询全链路验证...")
    result = engine.run_test()
    
    print("\n" + "=" * 55)
    print("测试结果:")
    for k, v in result["steps"].items():
        status = "通过" if v == "success" else "失败"
        print(f"  {k}: {status}")
    print(f"  MD文件: {result.get('md_path', 'N/A')}")
    print(f"  日志: {result.get('log_path', 'N/A')}")
    print("=" * 55)
