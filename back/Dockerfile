# 使用 astral/uv 官方镜像作为基础镜像，它已预装 uv
FROM astral/uv:python3.12-bookworm-slim

# 设置工作目录
WORKDIR /app

# 复制后端所有源代码到工作目录
COPY . .

# 使用 uv 安装项目依赖
RUN uv sync

# 修复 newspaper 依赖
RUN python -m nltk.downloader punkt_tab

# 暴露 Flask 应用运行的端口
EXPOSE 4000

# 定义容器启动时运行的命令
# 使用 uv run 来启动应用，并监听所有网络接口
CMD ["uv", "run", "main.py"]
