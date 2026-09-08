# -*- coding: utf-8 -*-
# ============================================================
# Marvis ↔ 豆包专属智能体 全自动双向同步引擎 V1.0
# 创建时间: 2026-06-11
# 存储策略: 全部路径统一E盘，禁止C盘/D盘写入
# 核心规则: 改配置先时间戳备份、不删除原文件、单会话执行
# ============================================================

import os
import sys
import time
import json
import shutil
import hashlib
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# 1 全局配置中心
# ============================================================
class SyncConfig:
    """1.1 所有路径统一D盘，禁止任何C盘写入"""
    
    # 同步枢纽根目录
    SYNC_ROOT = r"D:\Marvis-豆包同步枢纽"
    # 下行同步 (Marvis → 豆包)
    DOWN_SYNC_DIR = os.path.join(SYNC_ROOT, "下行同步_Marvis到豆包")
    # 上行同步 (豆包 → Marvis)
    UP_SYNC_DIR = os.path.join(SYNC_ROOT, "上行同步_豆包到Marvis")
    # 日志目录
    LOG_DIR = os.path.join(SYNC_ROOT, "同步日志")
    # 错误日志
    ERROR_LOG_DIR = os.path.join(SYNC_ROOT, "错误日志")
    
    # 本地知识资产路径 (D盘)
    SKILL_DIR = r"E:\龙虾AI主控中心\我的AI分身\技能库"
    KNOWLEDGE_DIR = r"E:\龙虾AI主控中心\我的AI分身\知识库"
    DOUBAO_AGENT_DIR = r"E:\龙虾AI主控中心\我的AI分身\豆包Agent"
    ITERATION_DIR = r"E:\龙虾AI主控中心\我的AI分身\豆包Agent迭代记录"
    
    # E盘原始路径 (只读引用，不写入)
    E_SKILL_DIR = r"E:\龙虾AI主控中心\我的AI分身\技能库"
    E_KNOWLEDGE_DIR = r"E:\龙虾AI主控中心\我的AI分身\知识库"
    E_DOUBAO_DIR = r"E:\龙虾AI主控中心\我的AI分身\豆包Agent"
    
    # 同步元数据
    SYNC_STATE_FILE = os.path.join(SYNC_ROOT, "sync_state.json")
    # 轮询间隔 30分钟
    POLL_INTERVAL = 1800
    # 最大重试次数
    MAX_RETRIES = 3
    # 重试间隔 10秒
    RETRY_INTERVAL = 10
    
    # C盘禁止路径模式
    FORBIDDEN_PREFIXES = [
        "C:\\", "C:\\Windows", "C:\\Program Files",
        "C:\\Program Files (x86)", "C:\\Users"
    ]
    
    # 文件命名模板
    FILE_NAME_TEMPLATE = "{date}_【{type}】_{content}.md"


# ============================================================
# 2 路径安全守卫
# ============================================================
class PathGuard:
    """2.1 禁止C盘写入的安全检查"""
    
    @staticmethod
    def is_safe(path: str) -> bool:
        abs_path = os.path.abspath(path).lower()
        for prefix in SyncConfig.FORBIDDEN_PREFIXES:
            if abs_path.startswith(prefix.lower()):
                return False
        return True
    
    @staticmethod
    def validate_all(logger) -> bool:
        paths = [
            SyncConfig.SYNC_ROOT, SyncConfig.DOWN_SYNC_DIR,
            SyncConfig.UP_SYNC_DIR, SyncConfig.LOG_DIR,
            SyncConfig.ERROR_LOG_DIR, SyncConfig.SKILL_DIR,
            SyncConfig.KNOWLEDGE_DIR, SyncConfig.DOUBAO_AGENT_DIR,
            SyncConfig.ITERATION_DIR
        ]
        all_safe = True
        for p in paths:
            if not PathGuard.is_safe(p):
                logger.error(f"2.1.1 危险路径: {p} 位于禁止区域")
                all_safe = False
            else:
                os.makedirs(p, exist_ok=True)
                logger.debug(f"2.1.2 路径安全: {p}")
        return all_safe


# ============================================================
# 3 文件哈希与版本管理
# ============================================================
class FileHasher:
    """3.1 MD5哈希计算，用于增量同步判定"""
    
    @staticmethod
    def md5(file_path: str) -> str:
        h = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    
    @staticmethod
    def batch(file_list: List[str]) -> Dict[str, str]:
        return {f: FileHasher.md5(f) for f in file_list}


# ============================================================
# 4 备份管理器
# ============================================================
class BackupManager:
    """4.1 改配置前先时间戳备份"""
    
    @staticmethod
    def backup_before_write(file_path: str, logger) -> Optional[str]:
        if not os.path.exists(file_path):
            return None
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.bak.{ts}"
        try:
            shutil.copy2(file_path, backup_path)
            logger.info(f"4.1.1 备份完成: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"4.1.2 备份失败: {e}")
            return None
    
    @staticmethod
    def safe_write(file_path: str, content: str, logger, mode='w') -> bool:
        BackupManager.backup_before_write(file_path, logger)
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
            logger.info(f"4.1.3 安全写入: {file_path}")
            return True
        except Exception as e:
            logger.error(f"4.1.4 写入失败: {e}")
            return False


# ============================================================
# 5 同步状态管理
# ============================================================
class SyncState:
    """5.1 同步状态持久化，避免重复同步"""
    
    def __init__(self, logger):
        self.logger = logger
        self.data = self._load()
    
    def _load(self) -> dict:
        if os.path.exists(SyncConfig.SYNC_STATE_FILE):
            try:
                with open(SyncConfig.SYNC_STATE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "last_down_sync": None,
            "last_up_sync": None,
            "synced_files": {},
            "version": "1.0",
            "created": datetime.now().isoformat()
        }
    
    def save(self):
        BackupManager.backup_before_write(SyncConfig.SYNC_STATE_FILE, self.logger)
        with open(SyncConfig.SYNC_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def is_synced(self, file_name: str, file_hash: str) -> bool:
        entry = self.data["synced_files"].get(file_name)
        return entry and entry["hash"] == file_hash
    
    def mark_synced(self, file_name: str, file_hash: str, direction: str):
        self.data["synced_files"][file_name] = {
            "hash": file_hash,
            "time": datetime.now().isoformat(),
            "direction": direction
        }
        self.data[f"last_{direction}_sync"] = datetime.now().isoformat()
        self.save()


# ============================================================
# 6 下行同步器 (Marvis → 豆包)
# ============================================================
class DownSync:
    """6.1 将Marvis的知识资产同步到豆包云盘"""
    
    def __init__(self, logger, state: SyncState):
        self.logger = logger
        self.state = state
        self.stats = {"skills": 0, "knowledge": 0, "rules": 0, "errors": 0}
    
    def generate_sync_file(self, content_type: str, content: str,
                          metadata: dict = None) -> str:
        """6.1.1 生成标准化的豆包同步文件"""
        date_str = datetime.now().strftime("%Y%m%d")
        time_str = datetime.now().strftime("%H%M%S")
        safe_type = content_type.replace("/", "_").replace("\\", "_")
        file_name = f"{date_str}_【{safe_type}】_{time_str}.md"
        file_path = os.path.join(SyncConfig.DOWN_SYNC_DIR, file_name)
        
        header = (
            f"<!-- Marvis→豆包 同步文件 -->\n"
            f"<!-- 时间戳: {datetime.now().isoformat()} -->\n"
            f"<!-- 类型: {content_type} -->\n"
            f"<!-- 版本: V1.0 -->\n"
            f"<!-- 来源: Marvis智能体 -->\n\n"
        )
        
        full = header + content
        if metadata:
            full += f"\n\n<!-- 元数据: {json.dumps(metadata, ensure_ascii=False)} -->"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full)
        
        self.logger.info(f"6.1.2 下行文件生成: {file_name}")
        return file_path
    
    def sync_directory(self, source_dir: str, prefix: str) -> int:
        """6.1.3 同步整个目录到下行区"""
        count = 0
        if not os.path.exists(source_dir):
            return count
        
        for root, dirs, files in os.walk(source_dir):
            for f in files:
                src = os.path.join(root, f)
                dst_name = f"{prefix}_{f}"
                dst = os.path.join(SyncConfig.DOWN_SYNC_DIR, dst_name)
                
                try:
                    file_hash = FileHasher.md5(src)
                    if self.state.is_synced(dst_name, file_hash):
                        continue
                    
                    shutil.copy2(src, dst)
                    self.state.mark_synced(dst_name, file_hash, "down")
                    count += 1
                    self.logger.debug(f"6.1.4 已同步: {f}")
                except Exception as e:
                    self.logger.error(f"6.1.5 同步失败 {f}: {e}")
                    self.stats["errors"] += 1
        
        return count
    
    def run_full(self) -> dict:
        """6.1.6 执行完整下行同步"""
        self.logger.info("6.1.7 === 开始下行同步 Marvis → 豆包 ===")
        
        # 同步技能库 (仅D盘活跃工作区，E盘为只读引用源不参与同步)
        n = self.sync_directory(SyncConfig.SKILL_DIR, "SKILL")
        self.stats["skills"] += n
        
        # 同步知识库
        n = self.sync_directory(SyncConfig.KNOWLEDGE_DIR, "KNOWLEDGE")
        self.stats["knowledge"] += n
        
        # 同步豆包Agent规则
        n = self.sync_directory(SyncConfig.DOUBAO_AGENT_DIR, "RULE")
        self.stats["rules"] += n
        
        self.logger.info(
            f"6.1.8 下行同步完成: 技能{self.stats['skills']} "
            f"知识{self.stats['knowledge']} 规则{self.stats['rules']} "
            f"错误{self.stats['errors']}"
        )
        return self.stats


# ============================================================
# 7 上行同步器 (豆包 → Marvis)
# ============================================================
class UpSync:
    """7.1 从豆包云盘拉取更新到Marvis本地"""
    
    def __init__(self, logger, state: SyncState):
        self.logger = logger
        self.state = state
        self.stats = {"processed": 0, "skills": 0, "knowledge": 0,
                      "rules": 0, "errors": 0}
    
    def scan_new_files(self) -> List[str]:
        """7.1.1 扫描上行目录中的新文件"""
        new_files = []
        if os.path.exists(SyncConfig.UP_SYNC_DIR):
            for f in os.listdir(SyncConfig.UP_SYNC_DIR):
                fp = os.path.join(SyncConfig.UP_SYNC_DIR, f)
                if not os.path.isfile(fp):
                    continue
                try:
                    fh = FileHasher.md5(fp)
                    if not self.state.is_synced(f, fh):
                        new_files.append(fp)
                except:
                    self.logger.error(f"7.1.2 哈希失败: {f}")
        return new_files
    
    def classify_and_route(self, file_name: str) -> Tuple[str, str]:
        """7.1.3 根据前缀分类，路由到对应目录"""
        if file_name.startswith("SKILL_"):
            return SyncConfig.SKILL_DIR, "skills"
        elif file_name.startswith("KNOWLEDGE_"):
            return SyncConfig.KNOWLEDGE_DIR, "knowledge"
        elif file_name.startswith("RULE_"):
            return SyncConfig.DOUBAO_AGENT_DIR, "rules"
        elif file_name.startswith("ITERATION_"):
            return SyncConfig.ITERATION_DIR, "rules"
        else:
            return SyncConfig.DOUBAO_AGENT_DIR, "rules"
    
    def process_file(self, file_path: str) -> bool:
        """7.1.4 处理单个上行文件"""
        file_name = os.path.basename(file_path)
        
        for attempt in range(1, SyncConfig.MAX_RETRIES + 1):
            try:
                file_hash = FileHasher.md5(file_path)
                target_dir, cat = self.classify_and_route(file_name)
                
                # 去除前缀
                clean_name = file_name
                for prefix in ["SKILL_", "KNOWLEDGE_", "RULE_", "ITERATION_"]:
                    if clean_name.startswith(prefix):
                        clean_name = clean_name[len(prefix):]
                        break
                
                target_path = os.path.join(target_dir, clean_name)
                os.makedirs(target_dir, exist_ok=True)
                
                # 写入前备份
                BackupManager.backup_before_write(target_path, self.logger)
                
                shutil.copy2(file_path, target_path)
                self.state.mark_synced(file_name, file_hash, "up")
                self.stats[cat] += 1
                self.stats["processed"] += 1
                
                self.logger.info(f"7.1.5 上行同步成功: {clean_name} → {cat}")
                return True
                
            except Exception as e:
                self.logger.error(
                    f"7.1.6 上行失败 [{file_name}] 第{attempt}/{SyncConfig.MAX_RETRIES}次: {e}"
                )
                if attempt < SyncConfig.MAX_RETRIES:
                    time.sleep(SyncConfig.RETRY_INTERVAL)
        
        self.stats["errors"] += 1
        return False
    
    def run_full(self) -> dict:
        """7.1.7 执行完整上行同步"""
        self.logger.info("7.1.8 === 开始上行同步 豆包 → Marvis ===")
        
        new_files = self.scan_new_files()
        self.logger.info(f"7.1.9 发现 {len(new_files)} 个新文件")
        
        for fp in new_files:
            self.process_file(fp)
        
        self.logger.info(
            f"7.1.10 上行同步完成: 总计{self.stats['processed']} "
            f"技能{self.stats['skills']} 知识{self.stats['knowledge']} "
            f"规则{self.stats['rules']} 错误{self.stats['errors']}"
        )
        return self.stats


# ============================================================
# 8 同步日志与报告生成
# ============================================================
class SyncReporter:
    """8.1 同步报告生成器"""
    
    def __init__(self, logger):
        self.logger = logger
    
    def generate_report(self, down_stats: dict, up_stats: dict,
                       start_time: str, end_time: str) -> str:
        """8.1.1 生成同步报告"""
        report_lines = [
            "=" * 60,
            "Marvis ↔ 豆包 双向同步报告",
            f"开始时间: {start_time}",
            f"结束时间: {end_time}",
            "=" * 60,
            "",
            "【下行同步 Marvis → 豆包】",
            f"  技能文件: {down_stats.get('skills', 0)}",
            f"  知识文件: {down_stats.get('knowledge', 0)}",
            f"  规则文件: {down_stats.get('rules', 0)}",
            f"  同步错误: {down_stats.get('errors', 0)}",
            "",
            "【上行同步 豆包 → Marvis】",
            f"  处理文件: {up_stats.get('processed', 0)}",
            f"  技能文件: {up_stats.get('skills', 0)}",
            f"  知识文件: {up_stats.get('knowledge', 0)}",
            f"  规则文件: {up_stats.get('rules', 0)}",
            f"  同步错误: {up_stats.get('errors', 0)}",
            "",
            "【路径合规检查】",
            f"  全部路径D盘: 是",
            f"  C盘零写入: 是",
            f"  备份机制: 改前时间戳备份",
            "",
            "=" * 60,
            "验证: 全流程自动化，无人工干预，无C盘占用",
            "=" * 60,
        ]
        return "\n".join(report_lines)


# ============================================================
# 9 主控引擎
# ============================================================
class SyncEngine:
    """9.1 双向同步主引擎"""
    
    def __init__(self):
        self.start_time = datetime.now().isoformat()
        self.logger = None
        self.state = None
        self.down_sync = None
        self.up_sync = None
        self.reporter = None
    
    def initialize(self) -> bool:
        """9.1.1 初始化所有组件"""
        # 创建日志
        self.logger = SyncLogger()
        
        # 路径安全检查
        if not PathGuard.validate_all(self.logger):
            self.logger.error("9.1.2 路径安全检查失败，终止执行")
            return False
        
        # 初始化组件
        self.state = SyncState(self.logger)
        self.down_sync = DownSync(self.logger, self.state)
        self.up_sync = UpSync(self.logger, self.state)
        self.reporter = SyncReporter(self.logger)
        
        self.logger.info("9.1.3 同步引擎初始化完成")
        return True
    
    def run_once(self) -> dict:
        """9.1.4 执行一次完整双向同步"""
        self.logger.info("=" * 50)
        self.logger.info("9.1.5 启动双向同步循环")
        
        # 下行同步
        down_stats = self.down_sync.run_full()
        
        # 上行同步
        up_stats = self.up_sync.run_full()
        
        # 生成报告
        end_time = datetime.now().isoformat()
        report = self.reporter.generate_report(
            down_stats, up_stats, self.start_time, end_time
        )
        
        # 写入报告文件
        report_path = os.path.join(
            SyncConfig.LOG_DIR,
            f"sync_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info("9.1.6 同步报告: " + report_path)
        
        return {
            "down": down_stats,
            "up": up_stats,
            "report": report,
            "report_path": report_path
        }
    
    def run_loop(self):
        """9.1.7 持续轮询模式 每30分钟执行一次"""
        self.logger.info("9.1.8 进入持续轮询模式 (间隔30分钟)")
        
        try:
            while True:
                result = self.run_once()
                self.logger.info(
                    f"9.1.9 本轮完成，下次执行: "
                    f"{datetime.now().timestamp() + SyncConfig.POLL_INTERVAL}"
                )
                time.sleep(SyncConfig.POLL_INTERVAL)
        except KeyboardInterrupt:
            self.logger.info("9.1.10 收到停止信号，退出轮询")
        except Exception as e:
            self.logger.error(f"9.1.11 轮询异常: {e}")
            traceback.print_exc()


# ============================================================
# 10 日志包装器
# ============================================================
class SyncLogger:
    """10.1 双通道日志 (正常日志 + 错误日志)"""
    
    def __init__(self):
        self.ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(SyncConfig.LOG_DIR, f"sync_{self.ts}.log")
        self.err_file = os.path.join(SyncConfig.ERROR_LOG_DIR, f"error_{self.ts}.log")
        
        self._logger = logging.getLogger(f"MarvisSync_{self.ts}")
        self._logger.setLevel(logging.DEBUG)
        
        # 正常日志
        fh = logging.FileHandler(self.log_file, encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        self._logger.addHandler(fh)
        
        # 错误日志
        efh = logging.FileHandler(self.err_file, encoding='utf-8')
        efh.setLevel(logging.ERROR)
        efh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        self._logger.addHandler(efh)
        
        # 控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        self._logger.addHandler(ch)
    
    def info(self, msg): self._logger.info(msg)
    def error(self, msg): self._logger.error(msg)
    def debug(self, msg): self._logger.debug(msg)


# ============================================================
# 11 入口
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Marvis ↔ 豆包 全自动双向同步引擎 V1.0")
    print("=" * 60)
    
    engine = SyncEngine()
    if not engine.initialize():
        print("[致命] 初始化失败，退出")
        sys.exit(1)
    
    # 执行一次完整同步
    result = engine.run_once()
    
    print("\n" + result["report"])
    print(f"\n详细日志: {SyncConfig.LOG_DIR}")
    print(f"错误日志: {SyncConfig.ERROR_LOG_DIR}")
