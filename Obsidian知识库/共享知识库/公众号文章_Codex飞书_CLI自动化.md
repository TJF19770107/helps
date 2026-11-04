# 如何通过 Codex 对话接入飞书完整版来了！

> 来源: https://mp.weixin.qq.com/s/lp1fV7O1flKzV1AgeMBQ3A

大家好，我是姚路行，一个爱搞AI的大厂程序员，也是一个90后奶爸

关注下
方

_[图片 1: 无可识别文本]_

公众
号
，回复【claude】免费领取Claude Code学习资料

最近 Codex 真的太火了！

总有同学问我怎么能让 Codex 可以接入飞书的能力！

因为接入飞书，Codex 就
可以创建和更新文档，可以读写 Base，可以查日历、发消息、管任务，甚至还能碰邮箱、知识库、会议纪要这些东西。

确实牛逼！

那我今天就给大家来一个保姆级的教程，
只和 Codex 对话即可
！

保姆级实操：4 步把
飞书
接进
Codex

好，咱们直接干整！

第 1 步：安装飞书 CLI

直接让 Codex 帮你安装飞书 CLI：

```
帮 我 安 装 飞 书 CLI: https://open.feishu.cn/document/no_class/mcp-archive/feishu-cli-installation-guide.md

# 讥 权 限 v codex 5.5 高 、 (+)
```

整个过程可能会持续4～5分钟。

```
已 处 理 4m 15s

安 装 好 了 。

验 证 结 果 :

* lark-cli 路 径 : /Users/ /.nvmyversions/node/v20.19.1/biny lark-cti
* 版 本 : lark-ctt version 1.0.44

。 飞 书 /Lark Al Skills 也 已 安 装 , 共 26 个 , 位 置 在 */.agents/skiLts/ lark-#

过 程 中 官 方 一 键 安 装 向 导 通 到 过 一 次 npm 权 限 问 题 : 全 局 包 目 录 里 已 有 一 个 root 拥 有 的 Glarksuite/cLi 目 录 。 但
当 前 CLI 本 身 已 经 安 装 可 用 , npm list -g @larksuite/cli 也 显 示 是 1.0.44 。

下 一 步 需 要 你 做 授 权 配 置 时 运 行 :

bash

lark-cli config init --new
lark-cli auth login -~-recommend

Pa)
```

第 2 步：配置飞书应用

接下来初始化配置，直接让 Codex 输出浏览器可以访问的链接：

```
输 出 浏 览 器 的 访 问 链 接

已 处 理 5s

请 在 浏 览 器 打 开 这 个 链 接 完 成 配 置 :
国 https://open:feishucnypagejcli?user_code=V3N4-USGX&lpv=1.0.44&ocv=1.0.44&from=cli

我 这 边 的 命 令 还 在 等 待 配 置 结 果 。
```

运行后，它会吐给你一个配置链接。

你把这个链接丢到浏览器里打开，按页面提示创建应用，或者绑定已有应用。

```
头 像 *

创 建 飞 书 CLI 应 用

坪 贵 面 目 面 国 网 。

名 称 *

| Codex 的 飞 书 CLI |

创 建 后 ,

动 完 成 所 有 配 置 >

选 择 已 有 应 用
```

这接着将这个创建好的飞书应用的 App ID 和 App Secret 交给 Codex。

```
Codextt"# CLI a
a

E 0 aweate

wee
日 xaszate s
& otra

‘App Secret ©
en 0 @ C

E
E
E

E

口 em
口 zfses 蹇
O zsen

日 ssseua 2

3

mR
```

```
App ID:
App Secret:

text

OK: 应 用 配 置 成 功

App ID:
brand: feishu

密 钥 已 由 CLI 保 存 平 在 输 出 里 脱 敏 。 下 一 步 可 以 登 录 授 权 :

bash

lark-cli auth login --recommend
```

第 3 步：登录授权

应用配好之后，再做一次用户授权，同理可以让他输出
浏览器可以访问的链接
：

```
辐 出 浏 览 器 的 访 问 链 接

已 处 理 15s

请 打 开 这 个 链 接 完 成 授 权 :
```

它同样会给你一个链接，浏览器打开，确认授权。

```
添 加 、 五
。 删 除 云 文 档
获 取 云 文 档
修 改 云 文 档
复 、 修 改 、 删 除 云 文 档 q

銮

Codex 的 飞 书 CLI

确 定 开 通 并 授 权 以 下 权 限 吗 ?

回

创

查 看 云 空 间

复 云 文 档 中 的 评 论

建 新 版 文 档
查 看 新 版 文 档
编 辑 新 版 文 档

查 看 群 信 息

更 新 群 信 息

查 看 Pin 消 息
添 加 、 取 消 Pin 消 息

F 的 评 论
F 的 评 论
F 的 评 论

文 件 元 数 据

o

查 看 消 息 表 情

F 的 评 论

该 应

将 可 持 续 访 问

已 授 权 的 数 据 @
```

第 4 步：验证接入是否成功

最简单的验证方式，就是跑一个低风险命令。

比如创建一个下周一8点的飞书日历：

```
帮 我 创 建 一 个 下 周 一 早 上 8 点 的 飞 书 日 历

已 处 理 25s

已 创 建 成 功 。

日 程 信 息 :

* 标 题 ; AR

* 时 间 ; 2026-06-01 08:00-09:00 (Asia/Shanghail

* 日 程 ID: 055c6d89-94de-4e73-8920-98f4cf7111d1_0
* Sf): user
```

如果能正常看到日历内容，说明权限和链路基本通了。

```
bet 日 历 “ 会 议 室 “ 预 约 活 动

~ im

> 2026 年 5 月 《 > 民 量
Q 搜 索 (#+KJ 今 天 《 > “2026 年 5 月 31 日 - oF
日 国 二 = 四 五 六
s 周 日 周 一
白 消 息 @ 26 27 2 2 30 1 2
ore 5 月 31 日 6 月 1 日
回 日 历 3 4 5 6 7 8 9
民 云 文 档 10 M “12 13 14 “15 16
回 多 维 表 格 17 “18 19 20 21 22 23 日 莲
园 视 频 会 议 24 25 26 27 28 29 30 [0-200

3 工 作 台 @) 1 2 3 4 8 G
```

只要这一步通了，后面就不是“能不能接”的问题，而是“你想让它做什么”的问题了。

总结一下

Codex 很火，这没问题。

但我觉得，真正值得写的，不是“Codex 又多强了”，而是
Codex 终于开始接上真实工作流了
。

飞书 CLI 的价值，不是多了几个命令。
而是让 AI 从“会写代码”，走到“能处理工作”。

所以如果你最近正好在折腾 Codex，我很建议你试试飞书 CLI。

AI 不只是回答你，它开始替你完成任务。

往期优质文章

这些Skills让OpenClaw把搜索做到极致！

【别错过】35+ OpenClaw实战案例，每个都能直接抄作业！

血泪总结！我用 OpenClaw 1个月，总结了这6个让你从"玩具"变"生产力"的配置原则

我给OpenClaw招了两个“下属”，7×24待命！

会主动找你的 OpenClaw 才叫“AI 助手”！

我花1天教会了OpenClaw完美复刻我的写作风格！

安装了72个Skills后，我的OpenClaw无所不能！

20分钟搭建性价比最高的 OpenClaw 组合！

一起学习

```
姚 路 行 的 蒸 汽 朋 克 AI 编 程 世 界

探 索 AL 与 前 端 技 术 的 无 限 可 能

国 # 孕
AT WISIN,
28
DeepSeekbifii AT 5 NLD (ogi Hee
华 OpenClaw 驿 睿 师

扫 码 加 我 微 信

@ I0A.Al 红 程 阳 作 诊
拉 你 迹 OpenClaw 交 流 酮
绍 周 A 技 术 精 选 与 前 浙 工 具 推 荫 微 信 号

ylx2ail

技 术 难 题 答 疑 与 实 战 经 验 分 宣 人 注 ; BREAN)

定 期 专 题 直 播 与 学 习 资 源 更 新
```