#!/usr/bin/env python3
"""TradingAgents - 多智能体交易决策服务"""

import json
from fastapi import FastAPI

app = FastAPI(title="TradingAgents Service", version="1.0")

@app.get("/health")
async def health():
    return {"ok": True, "service": "TradingAgents", "version": "1.0"}

@app.get("/")
async def root():
    return {"message": "TradingAgents Multi-Agent Trading System"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
