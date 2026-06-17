# 汉化魔改计划：将 BookSage-AI 改造成中文智能图书推荐项目

## 背景

当前仓库 `ZeroPointSix/BookSage-AI` 是一个完整的图书推荐系统，技术栈包括：

- 后端：FastAPI
- 前端：React 19 + Vite + Tailwind CSS + DaisyUI
- 推荐算法：协同过滤、基于内容推荐、Hybrid 混合推荐
- 数据：Book-Crossing 数据集及已训练/序列化模型
- 部署：Docker / docker-compose / Render 配置

从 README 和主要代码看，目前项目整体仍是英文展示，品牌名为 `BookSage-AI`，前端核心文案包括：

- `AI-Powered Recommendations`
- `Discover your next favorite book...`
- `How It Works`
- `Trending Books`
- `Collaborative Filtering / Content-Based / Hybrid Model`
- `No Recommendations Found`

本文件用于记录第二套项目方案：基于现有 BookSage-AI 做中文化、展示层魔改和提交材料包装，把它改造成可以用于课程/项目提交的中文智能图书推荐系统。

> 说明：仓库当前关闭了 GitHub Issues，因此本文件先作为 issue-style 计划文档保存。后续打开 Issues 后，可将本文内容原样迁移为 GitHub issue。

## 改造目标

把原项目从英文开源 demo 改造成一个更适合中文项目提交的版本：

- 前端界面完整汉化。
- README 和项目说明改成中文提交版。
- 保留原有推荐算法能力，但重新包装成“智能图书推荐系统”。
- 增加项目展示感、验收说明、运行方式和功能说明。
- 尽量不大改底层算法，优先在 UI、文案、说明、接口展示和 demo 体验上魔改。

## 建议项目中文定位

可选中文名称：

- 书灵 BookSage：智能图书推荐系统
- 智阅推荐：混合式图书推荐平台
- 智能图书推荐系统：基于协同过滤与内容相似度的混合推荐

建议最终提交标题：

> 智能图书推荐系统：基于协同过滤与内容相似度的混合推荐平台

## 改造范围

### 1. 前端汉化

需要汉化的主要区域：

- 首页 Hero 区文案
- 搜索框 placeholder
- 推荐方式按钮
- 推荐方法说明区
- 热门图书区标题
- 结果页返回按钮
- 已选择图书区域
- 推荐结果区域
- 空状态、加载状态、错误提示
- 图书卡片按钮和 tooltip

建议中文映射：

| 英文 | 中文 |
| --- | --- |
| `AI-Powered Recommendations` | `AI 智能图书推荐` |
| `Search for a book you love...` | `搜索一本你喜欢的书...` |
| `Hybrid` | `混合推荐` |
| `Collaborative / Collab` | `协同过滤` |
| `Content-Based / Content` | `内容相似` |
| `How It Works` | `推荐方式` |
| `Trending Books` | `热门图书` |
| `Back to Home` | `返回首页` |
| `Your Selected Book` | `你选择的图书` |
| `No Recommendations Found` | `暂无推荐结果` |
| `Try a different book or method.` | `可以尝试换一本书或切换推荐方式。` |

### 2. 品牌与视觉魔改

目标不是大重构，而是让项目看起来不是原样搬运：

- 将页面主标题从 `BookSage-AI` 调整为中文项目名。
- 增加中文副标题，强调“协同过滤 + 内容相似度 + 混合推荐”。
- 调整首页文案，让它更像课程/实训项目展示。
- 保留现有 React/Tailwind 结构，避免过度重写。
- 重新整理推荐方法卡片，使解释更适合中文答辩/提交。
- 检查移动端和桌面端布局，避免中文文本溢出。

### 3. 推荐结果展示增强

在不大改算法的前提下，增强结果可解释性：

- 在结果页展示当前使用的推荐方式。
- 对每种推荐方式给出一句中文解释。
- 推荐卡片中保留匹配分数或推荐强度。
- 如果后端已经返回 `type` / `score`，前端以中文方式展示。
- 空结果时给出明确下一步操作。

### 4. README 改造成中文提交版

README 需要从英文项目介绍改为中文项目提交说明，建议结构：

- 项目名称
- 项目简介
- 功能特点
- 技术栈
- 系统架构
- 推荐算法说明
- 页面功能说明
- API 接口说明
- 本地运行方式
- Docker 运行方式
- 测试与验证
- 项目目录结构
- 后续可扩展方向

需要特别处理：

- 原 README 中的英文 demo、原作者 clone 地址、英文营销描述要改写。
- 保留必要技术事实，避免夸大。
- 说明本项目是基于混合推荐思想实现的图书推荐平台。

### 5. 提交材料化

为了更适合项目提交，可以补充：

- `PROJECT_REPORT.md` 或中文项目报告。
- `WORKSPACE.md` 或开发记录。
- 截图说明：首页、搜索、推荐结果、空状态。
- 验收清单：功能、接口、构建、测试、运行。

如果后续需要正式交付，可进一步生成：

- 中文项目报告 PDF / DOCX
- 演示 PPT
- 运行截图
- 答辩讲稿

### 6. 后端轻量改造

后端尽量少动，优先保留已有接口：

- `GET /api/popular`
- `POST /api/recommend`
- `GET /api/search_books`
- `GET /api/health`

可考虑的小改动：

- FastAPI 标题和描述中文化。
- 健康检查返回中文友好字段可选。
- 推荐方法参数保持兼容：`hybrid` / `collaborative` / `content`。
- 不改训练流程，除非验证发现模型或数据无法加载。

## 验收标准

- 首页主要文案完成中文化。
- 搜索、推荐方式、结果页、空状态均为中文体验。
- 项目标题和 README 已改为中文提交版。
- 原有推荐流程保持可用：搜索图书 -> 选择推荐方式 -> 查看推荐结果。
- 前端生产构建通过：`npm run build`。
- 后端基础接口可访问：`/api/health`、`/api/popular`、`/api/search_books`、`/api/recommend`。
- 如果环境允许，Docker Compose 能正常启动前后端。
- 页面在桌面端和移动端没有明显文本溢出或布局错乱。

## 不纳入本轮

- 不重写推荐算法。
- 不换技术栈。
- 不引入登录、注册、权限系统。
- 不接入真实用户数据库。
- 不做复杂后台管理。
- 不大规模改训练数据和模型文件。
- 不做生产级部署安全加固。

## 建议实施顺序

1. 先跑通项目，确认前后端和模型是否可用。
2. 汉化前端所有用户可见文案。
3. 调整品牌名称、首页文案和推荐方式说明。
4. 优化推荐结果页的中文可解释性。
5. 改写 README 为中文提交版。
6. 补充项目报告/验收说明。
7. 执行构建、接口和页面验证。
8. 最后根据验证结果决定是否开 PR 合并。

## 相关文件初步关注点

- `README.md`
- `frontend/src/App.js`
- `frontend/src/views/HomeView.js`
- `frontend/src/views/ResultsView.js`
- `frontend/src/components/BookCard.js`
- `frontend/src/components/Hero.js`
- `frontend/src/components/Footer.js`
- `frontend/src/App.css`
- `frontend/src/index.css`
- `backend/app/main.py`
- `docker-compose.yml`

## 当前判断

这个仓库比之前的最小 MVP 更完整，适合作为“第二套/加强版项目提交”。改造重点应该放在：

- 中文化
- 项目身份重塑
- 前端展示 polish
- README/报告提交化
- 保持推荐算法和接口稳定

这样可以最大化利用已有工程基础，同时让最终结果看起来像我们自己的中文智能图书推荐项目。
