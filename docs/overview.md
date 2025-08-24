# AI 文章阅读器项目概览

AI 文章阅读器是一个全栈 Web 应用，允许用户输入文章链接，自动抓取、解析并美化文章内容，并可基于内容进行智能问答。

## 功能特性
- 文章抓取与解析
- AI 内容美化
- 智能问答
- 持久化存储 (SQLite)
- 现代化前端界面
- 前后端分离架构

## 技术架构
### 后端
- Python 与 Flask
- Newspaper3k 用于网页解析
- OpenAI API 提供大模型能力
- SQLite 数据库存储文章数据
- 使用 `uv` 管理 Python 依赖

### 前端
- React 与 Vite
- React Router
- 自定义 CSS 样式

## 目录结构
```
.
├── back/   # Flask 后端服务
└── front/  # React 前端应用
```

## 开发与运行
### 后端
```bash
cd back
uv venv
source .venv/bin/activate
uv sync
uv run
```
服务默认运行在 `http://127.0.0.1:4000`。

### 前端
```bash
cd front
npm install
npm run dev
```
前端开发服务器默认运行在 `http://127.0.0.1:5173`。

## Docker 部署
在项目根目录执行：
```bash
docker-compose up --build
```
启动后可通过 `http://localhost:8080` 访问前端应用。
