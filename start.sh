#!/bin/bash

# 启动 MLflow 跟踪服务器（后台运行）
mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri /mlflow \
    --default-artifact-root /mlflow \
    &> /dev/null &

# 等待 MLflow 服务器启动
sleep 3

# 启动 Jupyter Notebook
jupyter notebook \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --allow-root \
    --config=/etc/jupyter/jupyter_notebook_config.py