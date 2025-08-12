FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt ./

# 安装依赖，并使用清华镜像源加速
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 修复 newspaper3k 的 nltk 数据依赖
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader punkt_tab
# 复制所有源代码到工作目录
COPY . .

# 暴露 Flask 应用运行的端口
EXPOSE 4000

# 定义容器启动时运行的命令
CMD ["python", "main.py"]

