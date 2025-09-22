FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 创建数据目录
RUN mkdir -p /mlflow /notebooks /models

# 复制启动脚本和配置文件
COPY start.sh .
COPY jupyter_notebook_config.py /etc/jupyter/
RUN chmod +x start.sh

# 暴露端口
EXPOSE 8888
EXPOSE 5000

# 设置默认命令
CMD ["./start.sh"]