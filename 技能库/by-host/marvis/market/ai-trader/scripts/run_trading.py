#!/usr/bin/env python3
"""
AI-Trader runner script.
Executes trading experiments with proper error handling and logging.
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path

def get_project_root():
    """Return absolute path to AI-Trader project root."""
    # This script is in skills/ai-trader/scripts/
    # Project is at workspace/AI-Trader/AI-Trader-main/
    script_dir = Path(__file__).parent.parent.parent.parent.parent
    project_dir = script_dir / "AI-Trader" / "AI-Trader-main"
    if not project_dir.exists():
        raise FileNotFoundError(f"AI-Trader project not found at {project_dir}")
    return project_dir

def run_command(cmd, cwd=None, env=None):
    """Run shell command with real-time output."""
    print(f"▶️  Running: {cmd}")
    process = subprocess.Popen(
        cmd,
        shell=True,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    for line in process.stdout:
        print(line.rstrip())
    
    process.wait()
    return process.returncode

def check_env():
    """Check if .env file exists and has required keys."""
    project_root = get_project_root()
    env_file = project_root / ".env"
    
    if not env_file.exists():
        print("❌ .env file not found. Please create it with:")
        print("   cp .env.example .env")
        print("Then edit .env with your API keys.")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    required = ["OPENAI_API_KEY", "ALPHAADVANTAGE_API_KEY"]
    missing = [key for key in required if key not in content]
    
    if missing:
        print(f"❌ .env missing keys: {missing}")
        return False
    
    print("✅ .env file looks good")
    return True

def install_deps():
    """Install Python dependencies."""
    project_root = get_project_root()
    req_file = project_root / "requirements.txt"
    
    if not req_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("📦 Installing dependencies...")
    return run_command("pip install -r requirements.txt", cwd=project_root) == 0

def prepare_data(market="us"):
    """Run data preparation scripts."""
    project_root = get_project_root()
    data_dir = project_root / "data"
    
    if market == "us":
        print("📊 Preparing NASDAQ 100 data...")
        os.chdir(data_dir)
        run_command("python get_daily_price.py")
        run_command("python merge_jsonl.py")
        return True
    elif market == "cn":
        print("📊 Preparing A-share data...")
        astock_dir = data_dir / "A_stock"
        os.chdir(astock_dir)
        run_command("python get_daily_price_tushare.py")
        run_command("python merge_jsonl_tushare.py")
        return True
    elif market == "crypto":
        print("📊 Preparing cryptocurrency data...")
        crypto_dir = data_dir / "crypto"
        os.chdir(crypto_dir)
        run_command("python get_daily_price_crypto.py")
        run_command("python merge_crypto_jsonl.py")
        return True
    else:
        print(f"❌ Unknown market: {market}")
        return False

def start_mcp_services():
    """Start MCP services."""
    project_root = get_project_root()
    agent_tools = project_root / "agent_tools"
    
    print("🛠️  Starting MCP services...")
    # Run in background
    import subprocess
    process = subprocess.Popen(
        ["python", "start_mcp_services.py"],
        cwd=agent_tools,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Give it a moment to start
    import time
    time.sleep(3)
    
    # Check if still running
    if process.poll() is not None:
        print("❌ MCP services failed to start")
        return False
    
    print("✅ MCP services started (PID: {})".format(process.pid))
    return process

def run_trading(config_path):
    """Run main trading script."""
    project_root = get_project_root()
    config_file = project_root / "configs" / config_path
    
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        return False
    
    print(f"🤖 Starting trading with config: {config_path}")
    return run_command(f"python main.py {config_file}", cwd=project_root) == 0

def main():
    parser = argparse.ArgumentParser(description="AI-Trader runner")
    parser.add_argument("--config", default="default_config.json", help="Config file name (in configs/)")
    parser.add_argument("--market", choices=["us", "cn", "crypto"], help="Market type (auto-detected from config)")
    parser.add_argument("--prepare-data", action="store_true", help="Run data preparation")
    parser.add_argument("--start-mcp", action="store_true", help="Start MCP services")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--check-env", action="store_true", help="Check .env file")
    parser.add_argument("--all", action="store_true", help="Run full setup and trading")
    
    args = parser.parse_args()
    
    project_root = get_project_root()
    print(f"📁 Project: {project_root}")
    
    # Full setup mode
    if args.all:
        if not check_env():
            return 1
        if not install_deps():
            return 1
        
        # Detect market from config
        config_file = project_root / "configs" / args.config
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            market = config.get("market", "us")
        else:
            market = "us"
        
        if not prepare_data(market):
            return 1
        
        mcp_process = start_mcp_services()
        if not mcp_process:
            return 1
        
        try:
            run_trading(args.config)
        finally:
            mcp_process.terminate()
        return 0
    
    # Individual steps
    if args.check_env:
        return 0 if check_env() else 1
    
    if args.install:
        return 0 if install_deps() else 1
    
    if args.prepare_data:
        market = args.market or "us"
        return 0 if prepare_data(market) else 1
    
    if args.start_mcp:
        process = start_mcp_services()
        if process:
            try:
                print("Press Ctrl+C to stop MCP services...")
                process.wait()
            except KeyboardInterrupt:
                process.terminate()
        return 0 if process else 1
    
    # Default: just run trading
    return 0 if run_trading(args.config) else 1

if __name__ == "__main__":
    sys.exit(main())