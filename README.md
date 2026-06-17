# 书灵 BookSage：智能图书推荐系统

书灵 BookSage 是一个中文化的智能图书推荐系统展示项目。项目基于 Book-Crossing 图书数据集和已训练模型，提供热门图书浏览、图书搜索、协同过滤推荐、内容相似推荐和混合推荐能力，适合作为课程设计、实训项目或推荐系统方向的工程展示。

## 项目简介

本项目在原有 BookSage-AI 工程基础上完成中文化和提交材料化改造，保留 FastAPI 后端、React 前端、Docker 编排和既有推荐模型，不重写底层算法，重点优化中文使用体验、项目说明和验收可读性。

核心流程：搜索一本图书 -> 选择推荐方式 -> 查看推荐结果和推荐强度。

## 功能特点

- 图书搜索：根据关键词搜索图书标题，并展示作者和封面。
- 热门图书：展示样本数据中较热门的图书。
- 协同过滤：根据相似读者的评分行为推荐图书。
- 内容相似：根据图书内容、作者、出版信息等特征推荐相近作品。
- 混合推荐：结合协同过滤和内容相似度，输出更稳妥的推荐结果。
- 中文界面：首页、按钮、结果页、空状态、加载状态和页脚均已中文化。
- 可解释展示：结果页展示当前推荐方式、方式说明和推荐强度。

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 前端 | React 19、Vite、Tailwind CSS、DaisyUI、Lucide React |
| 后端 | FastAPI、Uvicorn、Pydantic |
| 推荐模型 | 协同过滤、TF-IDF 内容相似、混合加权推荐 |
| 数据处理 | Pandas、NumPy、SciPy、scikit-learn |
| 部署 | Docker、Docker Compose、Nginx |
| 测试 | Vitest、Testing Library、Pytest |

## 系统架构

```text
用户浏览器
  |
  v
React + Vite 前端
  |
  v
FastAPI JSON API
  |
  v
推荐引擎：协同过滤 / 内容相似 / 混合推荐
  |
  v
Book-Crossing 数据与序列化模型
```

## 推荐算法说明

### 协同过滤

协同过滤通过读者历史评分行为构建相似关系，从“相似读者喜欢什么”出发，为当前图书生成推荐。

### 内容相似

内容相似推荐通过 TF-IDF 和余弦相似度等方式分析图书文本与元数据特征，从“这本书和哪些书更像”出发生成推荐。

### 混合推荐

混合推荐将协同过滤和内容相似推荐结果进行加权融合，兼顾用户群体偏好和图书内容相似性，是默认推荐方式。

## API 接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/popular` | 获取热门图书 |
| GET | `/api/search_books?query=关键词` | 搜索图书 |
| POST | `/api/recommend` | 根据 `book_title` 和 `method` 获取推荐 |
| GET | `/api/health` | 健康检查 |

`method` 支持：

- `hybrid`：混合推荐
- `collaborative`：协同过滤
- `content`：内容相似

## 本地运行

### 使用 Docker Compose

```bash
git clone https://github.com/ZeroPointSix/BookSage-AI.git
cd BookSage-AI
docker compose up -d --build
```

启动后访问：

- 前端：`http://127.0.0.1:3000`
- 后端：`http://127.0.0.1:8000`
- 健康检查：`http://127.0.0.1:8000/api/health`

### 前端单独运行

```bash
cd frontend
npm install
npm run dev
```

### 后端单独运行

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 测试与验证

```bash
cd frontend
npm install
npm run build
npm test -- --run
```

```bash
cd backend
pip install -r requirements.txt
pytest
```

部署验收建议检查：

- 首页中文标题、搜索框、推荐方式和热门图书正常显示。
- 搜索图书后可以切换混合推荐、协同过滤和内容相似。
- 结果页能展示推荐方式说明、推荐数量和推荐强度。
- `/api/health` 返回 `healthy` 且 `models_loaded` 为可用状态。

## 项目目录

```text
BookSage-AI/
├── backend/                 # FastAPI 后端与推荐模型
├── frontend/                # React 前端界面
├── docs/                    # 改造计划与项目文档
├── docker-compose.yml       # 前后端 Docker 编排
├── PROJECT_REPORT.md        # 中文项目报告
└── README.md                # 中文提交版说明
```

## 后续扩展方向

- 增加用户登录和个人收藏。
- 引入真实用户行为数据进行在线更新。
- 增加推荐解释字段，例如相似作者、相似主题或评分贡献。
- 增加后台管理页，用于查看模型状态和数据统计。
- 补充项目截图、演示 PPT 和答辩讲稿。
