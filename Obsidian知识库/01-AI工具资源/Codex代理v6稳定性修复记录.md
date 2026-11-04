# Codex 代理 v6 稳定性修复记录

**日期**: 2026-08-01  
**状态**: ✅ 已修复  
**影响范围**: Codex++ 桌面程序与 Orca 项目同时使用

## 问题现象

1. Codex++ 桌面程序连接 `http://127.0.0.1:15730/v1/responses` 时频繁断开
2. 错误信息: `stream disconnected before completion`
3. 代理不稳定，一会儿好一会儿坏

## 根因分析（物理层/信息层/逻辑层）

### 物理层
- Python 环境错误：使用了 `E:\VNPY\` 的 Python，缺少 `ssl` 模块
- 修复：使用正确的 Python 路径 `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`

### 信息层
- 代理日志不详细，难以排查问题
- 修复：添加详细日志记录

### 逻辑层
1. **模型名未转换**: Codex++ 发送 `gpt-5.4-mini`，MiMo 不支持
2. **text.format 未过滤**: Codex++ 发送 `json_schema` 格式，MiMo 只支持 `text` 和 `json_object`
3. **编码处理不健壮**: UTF-8 解码失败时直接跳过转换
4. **异常处理不完善**: `ConnectionAbortedError` 导致代理崩溃

## 修复方案

### 1. 模型名转换
```python
# 自动将不支持的模型名转换为 mimo-v2.5-pro
original_model = data.get("model", "")
if not original_model or "mimo" not in original_model.lower():
    data["model"] = "mimo-v2.5-pro"
```

### 2. text.format 过滤
```python
# 过滤 MiMo 不支持的 text.format 类型
if "text" in data and isinstance(data["text"], dict):
    text_config = data["text"]
    if "format" in text_config and isinstance(text_config["format"], dict):
        format_type = text_config["format"].get("type", "")
        if format_type not in ("text", "json_object"):
            del text_config["format"]
```

### 3. 多编码支持
```python
# 尝试多种编码解码请求体
for encoding in ['utf-8', 'gbk', 'latin-1']:
    try:
        data = json.loads(body.decode(encoding))
        break
    except (UnicodeDecodeError, json.JSONDecodeError):
        continue
```

### 4. 异常处理加固
```python
try:
    # 发送错误响应
except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
    # 客户端已断开连接，忽略发送错误
    self.log_message(f"⚠ 客户端已断开，跳过错误响应")
```

## 测试验证

| 测试项 | 结果 |
|--------|------|
| 模型名转换 | ✅ `gpt-5.4-mini → mimo-v2.5-pro` |
| text.format 过滤 | ✅ `json_schema` 被过滤 |
| 流式请求 | ✅ 正常返回 SSE 格式 |
| 非流式请求 | ✅ 正常返回响应 |
| 异常处理 | ✅ 不再崩溃 |

## 端口隔离

- 代理只监听 `127.0.0.1:15730`
- 不干扰 Marvis/CCGUI 的运行
- Codex 桌面程序与 Orca 项目可以同时使用

## 稳定性保障

- 代理响应正常（3秒内返回）
- 流式/非流式请求都支持
- 自动处理各种编码和格式
- 客户端断开时不会崩溃

## 相关文件

- 代理脚本: `E:\龙虾AI主控中心\MCP服务\codex_tool_proxy.py`
- 配置文件: `~/.codex/config.toml`
- 模型目录: `~/.codex/cc-switch-model-catalog.json`

## 后续建议

1. 定期检查代理进程状态
2. 监控代理日志，及时发现异常
3. 保持 Python 环境正确配置

## 2026-08-01 更新：ConnectionAbortedError 修复

### 问题
代理在处理请求时崩溃，错误：`ConnectionAbortedError: [WinError 10053] 你的主机中的软件中止了一个已建立的连接。`

### 根因
- 客户端在代理发送响应之前断开连接
- 代理在 `end_headers()` 和 `wfile.write()` 时抛出异常
- 异常未被捕获，导致代理进程崩溃

### 修复方案
在整个响应路径中添加连接错误异常处理：

```python
try:
    # 发送响应
    self.send_response(resp.status)
    self.end_headers()
    # ... 流式/非流式响应 ...
except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError) as conn_err:
    self.log_message(f"⚠ 客户端连接断开: {conn_err}")
    return
except Exception as err:
    # 其他异常处理
    try:
        # 发送错误响应
    except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
        # 客户端已断开，忽略
```

### 测试验证
- ✅ 代理不再因客户端断开而崩溃
- ✅ 流式请求正常工作
- ✅ 异常时优雅降级

## 2026-08-01 更新：handle_one_request() 修复

### 问题
代理在读取请求行时崩溃，错误：`ConnectionAbortedError: [WinError 10053]` 发生在 `self.rfile.readline(65537)`

### 根因
- 客户端在代理读取请求行之前就断开连接
- `handle_one_request()` 方法未捕获早期连接断开异常
- 异常传播到 `socketserver` 框架，导致代理进程崩溃

### 修复方案
重写 `handle_one_request()` 方法，捕获早期连接断开：

```python
def handle_one_request(self):
    """重写以捕获早期连接断开"""
    try:
        super().handle_one_request()
    except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
        # 客户端在读取请求前就断开连接，忽略
        pass
    except Exception as e:
        # 其他异常记录日志
        self.log_message(f"⚠ 请求处理异常: {e}")
```

### 测试验证
- ✅ 代理不再因客户端断开而崩溃
- ✅ 流式请求正常工作
- ✅ 异常时优雅降级，不影响其他请求

## 最终修复方案

### 问题总结
代理在处理客户端连接时频繁崩溃，错误包括：
1. `ConnectionAbortedError: [WinError 10053]` - 响应路径
2. `ConnectionResetError: [WinError 10054]` - 请求路径

### 根因
- 客户端在代理处理请求的各个阶段断开连接
- 异常未被捕获，导致代理进程崩溃

### 最终修复方案
在三个层面添加异常处理：

#### 1. 请求读取层面（handle_one_request）
```python
def handle_one_request(self):
    """重写以捕获早期连接断开"""
    try:
        super().handle_one_request()
    except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
        # 客户端在读取请求前就断开连接，忽略
        pass
    except Exception as e:
        # 其他异常记录日志
        self.log_message(f"⚠ 请求处理异常: {e}")
```

#### 2. 响应发送层面（_proxy方法）
```python
try:
    # 发送响应
    self.send_response(resp.status)
    self.end_headers()
    # ... 流式/非流式响应 ...
except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError) as conn_err:
    self.log_message(f"⚠ 客户端连接断开: {conn_err}")
    return
```

#### 3. 错误响应层面（异常处理块）
```python
try:
    # 发送错误响应
except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
    # 客户端已断开，忽略
    self.log_message(f"⚠ 客户端已断开，跳过错误响应")
```

### 测试验证
- ✅ 代理不再因客户端断开而崩溃
- ✅ 流式请求正常工作
- ✅ 异常时优雅降级，不影响其他请求
- ✅ 代理稳定运行，不会频繁重启
