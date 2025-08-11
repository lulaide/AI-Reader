# --- 构建阶段 ---
# 使用官方 Node.js 镜像作为构建环境
FROM node:20-alpine AS build

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json (或 yarn.lock, pnpm-lock.yaml)
# 单独复制这些文件可以利用 Docker 的层缓存机制
COPY package.json package-lock.json* ./

# 安装项目依赖
RUN npm install

# 复制所有前端源代码
COPY . .

# 构建生产版本的应用
# 这会生成一个 `dist` 目录，包含所有静态文件
RUN npm run build

# --- 生产阶段 ---
# 使用轻量级的 Nginx 镜像来提供静态文件服务
FROM nginx:1.27-alpine

# 从构建阶段复制编译好的静态文件到 Nginx 的默认 Web 根目录
COPY --from=build /app/dist /usr/share/nginx/html

# 复制自定义的 Nginx 配置文件
# 这会覆盖掉 Nginx 镜像中默认的配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露 Nginx 默认的 HTTP 端口
EXPOSE 80

# 定义容器启动时运行的命令
# Nginx 会自动启动并提供 /usr/share/nginx/html 目录下的文件
CMD ["nginx", "-g", "daemon off;"]
