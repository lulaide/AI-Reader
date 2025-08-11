# 使用 astral/uv 官方镜像作为基础镜像，它已预装 uv
FROM astral/uv:python3.12-bookworm-slim

# 设置工作目录
WORKDIR /app

# 复制依赖管理文件
# 单独复制这些文件可以利用 Docker 的层缓存机制
# 只有当这些文件改变时，才会重新执行 uv sync
COPY pyproject.toml uv.lock ./

# 使用 uv 安装项目依赖
# --system 表示安装到系统级的 Python 环境中
# --no-cache 避免缓存不必要的包
RUN uv sync --system --no-cache

# 复制后端所有源代码到工作目录
COPY . .

# 暴露 Flask 应用运行的端口
EXPOSE 4000

# 定义容器启动时运行的命令
# 使用 uv run 来启动应用，并监听所有网络接口
CMD ["uv", "run", "--host=0.0.0.0", "--port=4000"]
