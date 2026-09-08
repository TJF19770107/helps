---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_3c4759cc733e11f1897e5254002afed2
    ReservedCode1: Detm9rdmFXRWD7WaZq8tcIfaf6Tv0MrBpueIeET/3Inp8e5FnsGL3Nsv4T3iUs5k4oVsP7C+yjj+wFaVlRHOHzFE0pT7HXNApv1XOqSXc3l/zSjYdnK0siMBxjr1ThodcImc8EXHK711bny8xpJZu7E2bjRirDoOWdT9c/l0zm3ce4i+kSU9dt+LUY4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_3c4759cc733e11f1897e5254002afed2
    ReservedCode2: Detm9rdmFXRWD7WaZq8tcIfaf6Tv0MrBpueIeET/3Inp8e5FnsGL3Nsv4T3iUs5k4oVsP7C+yjj+wFaVlRHOHzFE0pT7HXNApv1XOqSXc3l/zSjYdnK0siMBxjr1ThodcImc8EXHK711bny8xpJZu7E2bjRirDoOWdT9c/l0zm3ce4i+kSU9dt+LUY4=
---


---
技能名称：直连网络一键恢复+回滚
技能标识：direct_network_recovery_rollback_v1.0
版本：v1.0
日期：2026-06-29
执行环境：Windows PowerShell（管理员权限）
适用场景：代理故障/网络不通/浏览器无法上网/豆包服务异常
关联：龙虾标准五步法 v2.1
---

## 功能目标
纯本地执行，清除所有代理残留，恢复系统干净直连网络，保证浏览器、豆包、系统各服务正常联网。

## 执行步骤

### Step 1：结束代理进程
结束所有代理/翻墙相关进程（Clash、v2rayN、mihomo、sing-box、trojan、shadowsocks等）

### Step 2：重置系统代理
netsh winhttp reset proxy

### Step 3：重置 Winsock 和 IP 栈
netsh winsock reset
netsh int ip reset

### Step 4：释放并刷新 DNS
ipconfig /release
ipconfig /flushdns
ipconfig /renew

### Step 5：自动获取 DNS
恢复网卡为自动获取 DNS，不写死 114、223 等

### Step 6：验证连通性
ping www.baidu.com，能通则网络正常

### Step 7：结果提示
网络已恢复直连，Chrome/豆包可正常打开

## 回滚机制
执行前自动备份当前网络状态到同目录 backup\ 子目录：
- 当前代理配置（注册表导出）
- 当前 DNS 配置
- 当前 IP 配置
- 回滚说明 ROLLBACK.md

## 使用方式
Marvis 调用此技能时，按 Step 1→7 顺序执行，不许跳步。
*（内容由AI生成，仅供参考）*
