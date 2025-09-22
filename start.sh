#!/bin/bash

# 启动 MLflow 服务器在后台
echo "Starting MLflow server on port 5000..."
mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri /mlflow \
    --default-artifact-root /mlflow &

# 等待 MLflow 服务器启动
echo "Waiting for MLflow server to start..."
sleep 5

# 启动 Jupyter Notebook
echo "Starting Jupyter Notebook..."
jupyter notebook \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --allow-root \
    --config=/etc/jupyter/jupyter_notebook_config.py