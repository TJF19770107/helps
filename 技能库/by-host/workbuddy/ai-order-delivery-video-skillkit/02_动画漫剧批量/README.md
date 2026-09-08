# 02 · 动画漫剧批量（接入槽位）

## 一句话
分镜 → 角色 → 镜头 → 后期——用 6 视频融合流水线（Seedance2/HyperFrames/Remotion/剪映/Video-Use/ImageGen）批量出漫剧片段。

## 接入路径
1. 调 ai-video-production-pipeline 技能确认 6 技能路由
2. 写一个批处理入口 `make_comic_batch.py` —— 传 JSON 角色/分镜→自动出片
3. 落 3 条漫剧样片

## 关键依赖
- Seedance2（分镜提示词入口）
- HyperFrames（多镜头批量）
- Remotion（动态排版）
- ImageGen（封面）

## 占位资源
- 待落：JSON 分镜模板
- 待落：批量出片脚本
