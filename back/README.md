# AI Reader Backend

AI Reader 后端API服务，提供文章抓取、美化和AI问答功能。

## 技术栈

- **Python 3.10+**
- **Flask** - Web框架
- **uv** - 包管理器
- **OpenAI API** - AI功能
- **newspaper3k** - 文章抓取
- **flask-cors** - 跨域支持

## 功能特性

- 文章URL抓取和内容提取
- 文章内容AI美化和润色
- 基于文章内容的AI问答
- RESTful API接口
- CORS支持，便于前端调用

## 环境要求

- Python 3.10+
- uv包管理器

## 安装和使用

### 1. 克隆项目

```bash
git clone <repository-url>
cd AI-Reader/back
```

### 2. 创建环境变量文件

创建 `.env` 文件：

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.deepseek.com
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. 安装依赖

```bash
uv sync
```

### 4. 启动服务

```bash
# 方式1: 使用启动脚本
./start.sh

# 方式2: 直接运行
uv run python main.py
```

服务将启动在 `http://localhost:5000`

## API 接口

### 获取所有文章
- **GET** `/api/articles`
- **响应**: 
```json
{
  "articles": [...],
  "total": 5
}
```

### 获取单篇文章
- **GET** `/api/articles/{index}`
- **响应**:
```json
{
  "article": {...},
  "index": 0
}
```

### 添加文章
- **POST** `/api/articles`
- **请求体**:
```json
{
  "url": "https://example.com/article"
}
```

### AI问答
- **POST** `/api/ask`
- **请求体**:
```json
{
  "question": "这篇文章讲了什么？",
  "index": 0
}
```

### 健康检查
- **GET** `/api/health`

## 项目结构

```
back/
├── main.py          # Flask应用主文件
├── model.py         # 核心业务逻辑
├── pyproject.toml   # uv项目配置
├── .env             # 环境变量（需要创建）
├── .gitignore       # Git忽略文件
├── start.sh         # 启动脚本
├── articles.json    # 文章数据存储
└── README.md        # 项目文档
```

## 开发说明

- 使用 `uv` 管理Python依赖
- 使用 `.env` 文件管理配置
- 支持热重载开发模式
- 包含CORS支持，便于前端开发

## 部署

生产环境部署时：

1. 设置 `FLASK_ENV=production`
2. 设置 `FLASK_DEBUG=False`
3. 使用适当的WSGI服务器（如Gunicorn）
4. 配置反向代理（如Nginx）目是一个基于 Flask 和 DeepSeek API 构建的智能文章阅读和问答应用。用户可以输入文章链接，应用会自动抓取、解析和美化文章内容，并提供一个清爽的阅读界面。在阅读的同时，用户可以随时就文章内容向 AI 提问，实现沉浸式的智能阅读体验。

## ✨ 功能特性

- **现代化前端界面**：采用极简设计风格，美观、专业且易于使用。
- **文章抓取与美化**：输入 URL 即可自动抓取网页正文，并进行排版优化，提供最佳阅读效果。
- **两栏式阅读视图**：左侧为文章内容，右侧为问答区域，结构清晰，方便对照阅读和提问。
- **智能问答**：集成 DeepSeek 大模型，可以针对文章内容进行实时提问和回答。
- **异步非阻塞操作**：添加文章、提问等操作均为异步执行，并配有加载动画，提升用户体验。
- **聊天记录**：问答历史会以气泡形式清晰地展示在问答区。
- **响应式设计**：完美适配桌面和移动端浏览器。
- **极简主页**：主页设计简洁，聚焦于核心功能——“输入链接，开始阅读”。

## 🛠️ 技术栈

- **后端**：Python, Flask
- **前端**：HTML, CSS, JavaScript (Fetch API)
- **AI 模型**：DeepSeek API
- **Python 库**：`requests`, `beautifulsoup4`, `flask` 等

## 🚀 安装与运行

1.  **解压项目**
    ```bash
    cd Deepseek-Reader
    ```

2.  **创建并激活虚拟环境**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

4.  **配置 API Key**
    - 打开 `config.py` 文件。
    - 将 `DEEPSEEK_API_KEY` 的值替换为你自己的 DeepSeek API 密钥。
    - （可选）根据需要修改 `DEEPSEEK_API_BASE`。

5.  **运行应用**
    ```bash
    python main.py
    ```

6.  在浏览器中打开 `http://127.0.0.1:5000` 即可访问。

## 📖 使用指南

1.  **添加文章**：在主页的输入框中粘贴文章的 URL，点击“添加文章”按钮。应用会自动处理并在下方卡片中显示新添加的文章。
2.  **开始阅读和问答**：点击主页上的文章卡片，进入文章详情页。
3.  **提问**：在右侧的问答区输入框中输入你的问题，点击发送按钮或按回车键。AI 的回答将显示在下方。

## 📁 文件结构

```
.
├── templates/
│   ├── article.html      # 文章阅读和问答页面
│   └── home.html         # 应用主页
├── articles.json         # 存储已添加文章信息的数据库文件
├── config.py             # 配置文件（API Key 等）
├── main.py               # Flask 应用主逻辑（路由、视图函数）
├── model.py              # 核心业务逻辑（文章抓取、AI 调用）
├── requirements.txt      # Python 依赖列表
└── README.md             # 项目说明文档
```
