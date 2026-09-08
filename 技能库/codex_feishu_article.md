# 如何通过 Codex 对话接入飞书完整版来了！

**作者**: 我姚学AI  
**来源**: 微信公众号  
**原始链接**: [https://mp.weixin.qq.com/s/lp1fV7O1flKzV1AgeMBQ3A](https://mp.weixin.qq.com/s/lp1fV7O1flKzV1AgeMBQ3A)  
**提取时间**: 2026-06-16

---

大家好，我是姚路行，一个爱搞AI的大厂程序员，也是一个90后奶爸

关注下方公众号，回复【claude】免费领取Claude Code学习资料

---

最近 Codex 真的太火了！

总有同学问我怎么能让 Codex 可以接入飞书的能力！

因为接入飞书，Codex 就可以创建和更新文档，可以读写 Base，可以查日历、发消息、管任务，甚至还能碰邮箱、知识库、会议纪要这些东西。

确实牛逼！

那我今天就给大家来一个保姆级的教程，只和 Codex 对话即可！

---

## 保姆级实操：4 步把飞书接进 Codex

好，咱们直接干整！

### 第 1 步：安装飞书 CLI

直接让 Codex 帮你安装飞书 CLI：

> **提示**：以下 CLI 命令以截图形式嵌入原文，此处保留图片引用。  
> ![Step 1 截图](https://mmbiz.qpic.cn/mmbiz_png/nnCcYpy3mJEJPl0MRK6VRyJ8QeFNFztAC7tyTSkImq8BvmDibiaZl2lfDw8diaAS88WgkfT556C3ibiaeZH6PJ0hdlj6KIRnILjIg7ZThbDNbq4Y/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=1)

![Step 1 截图 2](https://mmbiz.qpic.cn/sz_mmbiz_png/nnCcYpy3mJFHWpe4y9qhR53QOicibDarMRkoFmwn1JISmCiaNeo5Wh2NJG8z9jAzOCyZoWDlK6scsdTXQd6sLreOKDORWHNE507PRegaJ7EWxI/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=2)

整个过程可能会持续4～5分钟。

### 第 2 步：配置飞书应用

接下来初始化配置，直接让 Codex 输出浏览器可以访问的链接：

> **提示**：以下 CLI 命令以截图形式嵌入原文，此处保留图片引用。  
> ![Step 2 截图](https://mmbiz.qpic.cn/sz_mmbiz_png/nnCcYpy3mJHia81UECsiazPOwVlGUQib4iaNpMtOS52tWvaTdlDwZJzCWdgvfFuoINiasVSkUsXvNvCTnd6EZ5lp5RvxUgY8LGI81pDg1urTnRzI/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=3)

运行后，它会吐给你一个配置链接。

你把这个链接丢到浏览器里打开，按页面提示创建应用，或者绑定已有应用。

这接着将这个创建好的飞书应用的 App ID 和 App Secret 交给 Codex。

> **提示**：以下 CLI 命令以截图形式嵌入原文，此处保留图片引用。  
> ![Step 2 截图 2](https://mmbiz.qpic.cn/sz_mmbiz_png/nnCcYpy3mJEBDdkjee24TM7vhqjez3pBiaB3Zdb6fqRqnkvYwhzxNJbRBosOQO2V8w91gajnGEoVeBM06rRjyza2NID8kggX28oscRQFqeQo/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=4)

### 第 3 步：登录授权

应用配好之后，再做一次用户授权，同理可以让他输出浏览器可以访问的链接：

> **提示**：以下 CLI 命令以截图形式嵌入原文，此处保留图片引用。  
> ![Step 3 截图](https://mmbiz.qpic.cn/mmbiz_png/nnCcYpy3mJE6AHujP6LR0DhOY6GoicUPGa6dBUbEh44Px3Sn88PAdzUDYXhnZgSibl2mQwVxoEYGuywFlFWwNXquS17yqjyicvibic2Qg6JPAGBg/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=5)

它同样会给你一个链接，浏览器打开，确认授权。

> **提示**：以下 CLI 命令以截图形式嵌入原文，此处保留图片引用。  
> ![Step 3 截图 2](https://mmbiz.qpic.cn/mmbiz_png/nnCcYpy3mJH0bg3uYlibCWcIH8cQHiavTq8Y31PavUAz5icxice8RYfDHd9mdT3emppZEkn5epEfbQzCYPJI7fevsdb29RsPz77W260DPyhrevE/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=6)

### 第 4 步：验证接入是否成功

最简单的验证方式，就是跑一个低风险命令。

比如创建一个下周一8点的飞书日历：

> **提示**：以下 CLI 命令以截图形式嵌入原文，此处保留图片引用。  
> ![Step 4 截图](https://mmbiz.qpic.cn/mmbiz_png/nnCcYpy3mJEFz88MshHgruEaibwnOrKZWrgPUKJWLIMfAx1XZzzcEyHrUGSjJJUxLqnD5Ok6j9AgHt84VABTGOiaEyrXkbCreqfLMTdcV7tws/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=7)

如果能正常看到日历内容，说明权限和链路基本通了。

只要这一步通了，后面就不是"能不能接"的问题，而是"你想让它做什么"的问题了。

---

## 总结一下

Codex 很火，这没问题。

但我觉得，真正值得写的，不是"Codex 又多强了"，而是 Codex 终于开始接上真实工作流了。

飞书 CLI 的价值，不是多了几个命令。而是让 AI 从"会写代码"，走到"能处理工作"。

所以如果你最近正好在折腾 Codex，我很建议你试试飞书 CLI。

AI 不只是回答你，它开始替你完成任务。

---

## 往期优质文章

*   这些Skills让OpenClaw把搜索做到极致！
*   【别错过】35+ OpenClaw实战案例，每个都能直接抄作业！
*   血泪总结！我用 OpenClaw 1个月，总结了这6个让你从"玩具"变"生产力"的配置原则
*   我给OpenClaw招了两个"下属"，7×24待命！
*   会主动找你的 OpenClaw 才叫"AI 助手"！
*   我花1天教会了OpenClaw完美复刻我的写作风格！
*   安装了72个Skills后，我的OpenClaw无所不能！
*   20分钟搭建性价比最高的 OpenClaw 组合！
*   一起学习

---

## 文章图片清单（CLI命令截图）

| 序号 | 位置 | 图片URL |
|:---:|------|---------|
| 1 | 第1步 - 安装CLI命令 | `https://mmbiz.qpic.cn/mmbiz_png/nnCcYpy3mJEJPl0MRK6VRyJ8QeFNFztAC7tyTSkImq8BvmDibiaZl2lfDw8diaAS88WgkfT556C3ibiaeZH6PJ0hdlj6KIRnILjIg7ZThbDNbq4Y/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=1` |
| 2 | 第1步 - 安装过程 | `https://mmbiz.qpic.cn/sz_mmbiz_png/nnCcYpy3mJFHWpe4y9qhR53QOicibDarMRkoFmwn1JISmCiaNeo5Wh2NJG8z9jAzOCyZoWDlK6scsdTXQd6sLreOKDORWHNE507PRegaJ7EWxI/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=2` |
| 3 | 第2步 - 配置命令 | `https://mmbiz.qpic.cn/sz_mmbiz_png/nnCcYpy3mJHia81UECsiazPOwVlGUQib4iaNpMtOS52tWvaTdlDwZJzCWdgvfFuoINiasVSkUsXvNvCTnd6EZ5lp5RvxUgY8LGI81pDg1urTnRzI/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=3` |
| 4 | 第2步 - 应用配置 | `https://mmbiz.qpic.cn/sz_mmbiz_png/nnCcYpy3mJEBDdkjee24TM7vhqjez3pBiaB3Zdb6fqRqnkvYwhzxNJbRBosOQO2V8w91gajnGEoVeBM06rRjyza2NID8kggX28oscRQFqeQo/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=4` |
| 5 | 第3步 - 授权命令 | `https://mmbiz.qpic.cn/mmbiz_png/nnCcYpy3mJE6AHujP6LR0DhOY6GoicUPGa6dBUbEh44Px3Sn88PAdzUDYXhnZgSibl2mQwVxoEYGuywFlFWwNXquS17yqjyicvibic2Qg6JPAGBg/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=5` |
| 6 | 第3步 - 授权确认 | `https://mmbiz.qpic.cn/mmbiz_png/nnCcYpy3mJH0bg3uYlibCWcIH8cQHiavTq8Y31PavUAz5icxice8RYfDHd9mdT3emppZEkn5epEfbQzCYPJI7fevsdb29RsPz77W260DPyhrevE/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=6` |
| 7 | 第4步 - 验证命令 | `https://mmbiz.qpic.cn/mmbiz_png/nnCcYpy3mJEFz88MshHgruEaibwnOrKZWrgPUKJWLIMfAx1XZzzcEyHrUGSjJJUxLqnD5Ok6j9AgHt84VABTGOiaEyrXkbCreqfLMTdcV7tws/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=7` |
| 8 | 验证结果 | `https://mmbiz.qpic.cn/mmbiz_png/nnCcYpy3mJGJX3IoanD8cNb82NQHM3sAQxap86icca6ibH1V3Zb8CDS7EUtiawibEA6oS2riabD8ib4MuQSqEP4bRo59uQBVno1WLrZKbkBhrPMUI/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=8` |
| 9 | 补充截图 | `https://mmbiz.qpic.cn/sz_mmbiz_png/nnCcYpy3mJEZnTXmnauGic3bhhyXOsewpRom0s8ibS7rLEDylD4nXpVzFw6AAy8JpIPgjbTStzngicbW8sUNicWBLqv4Wq2olkFz4bkCt7wgOR0/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=9` |
| 10 | 补充截图 | `https://mmbiz.qpic.cn/mmbiz_png/nnCcYpy3mJFsria99uSibwsr7Tqudicy9fRX0LKUerhib4m1A3j5hfdQIjcIyUKScibV37h3kWGEODtiapyy6kSMWLmibS96EYlnIicum6H8UzwXIYc/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=10` |
| 11 | 补充截图 | `https://mmbiz.qpic.cn/sz_mmbiz_png/nnCcYpy3mJGse2cA1uQtIAoh1HEzgbEaHsWHDXq4Yy4ib1nUpibHkw1m2pL0N6lzrqiaIun4LQKcibnicyTYE1E0pO77bLRFBA9awNDLg9iaQGyZk/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=11` |

> **注意**：原文中的 CLI 命令（`feishu` 相关安装、配置、授权、验证命令）均以 PNG 截图方式嵌入，无法通过 DOM 文本直接提取。上表列出了所有图片的 CDN 地址，建议后续通过 OCR 或 AI 视觉分析提取图片中的命令文本。图片 0 为 GIF 引导关注动画，非内容截图。

---

*本文内容提取自微信公众号「我姚学AI」，原文链接：https://mp.weixin.qq.com/s/lp1fV7O1flKzV1AgeMBQ3A*