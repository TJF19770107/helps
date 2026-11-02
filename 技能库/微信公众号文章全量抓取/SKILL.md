---
name: 微信公众号文章全量抓取
description: >
  在无微信客户端、无 API 权限的条件下，把指定公众号的文章正文批量抓下来并做溯源归档。
  当任务涉及：学习某个公众号/博主的所有文章、公众号内容采集、微信文章正文抓不到、
  「参数错误」「环境异常」「请在微信客户端打开链接」、搜狗微信 antispider、
  要给某个博主建档并蒸馏技能 时使用。
agent_created: true
version: 1.0.0
created: 2026-11-03
source: 实战打通（俊哥AI落地 7 篇 / 27,673 字），踩坑 6 次换 4 条路线
---

# 微信公众号文章全量抓取

## 一、先讲结论（省你两小时）

**唯一稳定的通道是：带完整 `sn` + `chksm` 的文章直链 + curl + 移动端 UA。**
其他四条路（无头浏览器 / 搜狗跳转 / 公众号主页 / 无 chksm 直链）**全部死路**，别再试。

```
https://mp.weixin.qq.com/s?__biz={BIZ}&mid={MID}&idx={IDX}&sn={SN}&chksm={CK}
```

四条缺一不可。**`chksm` 是总开关。**

---

## 二、关键事实表（这是本技能的核心价值）

| 现象 | 真实原因 | 是否可解 |
|---|---|---|
| 页面 ~3.5MB 但抓不到 `js_content`，正文 0 字 | **缺 `chksm`**，返回空壳页 | ✅ 补 chksm 即得全文 |
| 页面只有 2KB，标题「未知错误」/「失效的验证页面」 | `sn` 与 `chksm` **不是同一签发对**（自己拼的） | ❌ 必须用原文页的配对 |
| 「参数错误」 | `sn` 缺失或是假值（如 `sn=0`） | ❌ 不可枚举 |
| 「环境异常 去验证」→ 跳 `mp/wappoc_appmsgcaptcha` | 触发风控 | 换 IP/间隔重试 |
| 「请在微信客户端打开链接」 | 访问的是公众号主页 `mp/profile_ext?action=home` | ❌ 纯 curl/无头浏览器一律无解 |
| 搜狗列表页能拿，`/link?url=` 一跳就 `antispider` | 搜狗反爬（要求 cookie 会话 + 图形验证码） | ❌ 已验证 4 次，放弃 |
| HTTP 200 但只有 2000 多字节 | 200 不代表有内容，**必须校验 `js_content` 存在** | ⚠️ 这是最容易误判成功的坑 |

> ⚠️ **`http_code == 200` 是一个假信号。** 微信的错误页也返 200。
> 判据必须是：`'id="js_content"' in html and 正文长度 > 500`。

---

## 三、标准流程

### Step 1 · 建链接清单（`links.py`）

```python
BIZ_A = "MzA4OTM0NDc1Mg=="   # 主体 A（base64，注意末尾 == 必须保留）
ARTICLES = [
    dict(acct="号名", issue="第38期", mid="2651509076", idx="1",
         sn="49f85e3f...", ck="8a7c14b9...", title="..."),
]
```
- `__biz` 是 base64，`==` 别丢
- 同一号名可能对应**多个 biz 主体**（迁移/矩阵号），必须建 dict 映射，不能 if/else

### Step 2 · curl 直取（移动端 UA 更稳）

```python
UA_M = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
subprocess.run(["curl","-s","-L","-m","40","-o",out,"-w","%{http_code}",
                url,"-H",f"User-Agent: {UA_M}",
                "-H","Accept-Language: zh-CN,zh;q=0.9","--compressed"])
```
- **PC UA 会失败，移动端 UA 成功率高得多**
- `--compressed` 必须带
- 每次间隔 0.8–1.5 秒

### Step 3 · 正文提取（三个易错点）

```python
# ① 标题：三种写法都要兼容
title = re.search(r"var msg_title = '(.*?)'", s) \
        or re.search(r'property="og:title" content="(.*?)"', s)

# ② 作者：★★ 两种写法 —— 第二种曾经让 author 全空
#    var nickname = "俊哥聊AI"
#    var nickname = htmlDecode("俊哥AI落地")     ← 必须兼容
author = re.search(r'var nickname\s*=\s*htmlDecode\(\s*["\'](.*?)["\']\s*\)', s) \
         or re.search(r'var nickname\s*=\s*["\'](.*?)["\']', s)

# ③ 正文：id="js_content" 到 </div><script
body = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*<script', s, re.S)

# ④ 日期
date = re.search(r'var ct\s*=\s*"(\d+)"', s)   # unix 时间戳
```

清洗顺序：`<br>`→`\n` → 块级闭标签→`\n` → 去所有标签 → `html.unescape` → 压空行。

### Step 4 · 溯源归档

每篇写一个 txt，头部固定四行：
```
# {标题}
公众号: {author}
发布日期: {date}
期号: {issue}
原文: {url}
```

---

## 四、拿不到完整链接时怎么办（现实答案）

**拿不到就是拿不到，编不出来。** 四条可行路径按优先级：

| 优先级 | 方法 | 成功率 |
|---|---|---|
| 1 | **已有文章页里的内链**（正文「往期推荐/相关阅读」） | 能拿到 `mid+sn`，但**通常不带 chksm** → 仅能拿到线索，不能直接抓 |
| 2 | **WebSearch 按精确标题搜** `"标题" mp.weixin.qq.com` | 中（第7篇就是这样拿到的） |
| 3 | 搜狗列表页 | 能拿标题+日期，`/link` 被 antispider 挡 |
| 4 | 无头浏览器 / 公众号主页 | ❌ 全部失败 |

> **能覆盖方法论主干的长文，优先于数量。** 实测：7 篇里 4 篇成体系长文（含 1 篇 11,000 字论文）
> 已足够蒸馏出完整技能；剩余同模板短文边际增量很小。
> **不要为了凑数去伪造 URL 或编造内容。**

---

## 五、明确的能力边界（必须如实告知用户）

以下**公开通道做不到**，不要说"我试试"然后绕圈：

- ❌ **视频号内容**：无公开 Web 入口，必须在微信客户端内浏览
- ❌ **公众号全量历史列表**：`mp/profile_ext?action=home&__biz=...` 需微信客户端环境
- ❌ **文章内嵌图片批量下载**：`data-src` 可提取，但图片服务器有防盗链，需 Referer + 时效 token
- ❌ **同名干扰过滤**：搜狗/搜索会混入大量同名号（如「俊哥聊球」「俊哥聊车」「小俊哥聊购物」），必须人工核对

---

## 六、环境适配（本机 Windows）

| 坑 | 解法 |
|---|---|
| `urllib` 访问 127.0.0.1 报 502 | 系统代理在拦 → `build_opener(ProxyHandler({}))` |
| 外网要代理 | `HTTP_PROXY=http://127.0.0.1:60216`，curl 加 `--proxy` |
| Chrome 进程跨 Bash 调用被杀 | 必须**同一 Python 进程内** `Popen` → 用 → `terminate` |
| PIL 在系统 python 缺失 | 用 venv `~/.workbuddy/binaries/python/envs/default/Scripts/python.exe` |
| 微信文章 HTML 有 3.5MB | 别直接 print，写文件再用 grep |

---

## 七、自检清单（交付前必须过）

```
☐ 每篇 http_code == 200  且  'id="js_content"' 存在  且  正文 > 500 字
☐ author 字段非空（验证 htmlDecode 分支已被覆盖）
☐ date 字段是 YYYY-MM-DD
☐ 总字数与篇数打印出来（本次基准：7 篇 / 27,673 字）
☐ 每篇头部有原文 URL，可独立复核
☐ 未抓到的篇目在文档里如实标注为「未拿到完整 URL」，不编造
```

---

## 附：可复用脚本

`scripts/s4_curl.py` 的完整实现见实战产物：
`E:\博主学习库\_tmp_shot\s4_curl.py`（+ `links.py`）

用法：
```bash
python s4_curl.py        # 读 links.py，产出 raw_cl/*.txt + articles.json
```
