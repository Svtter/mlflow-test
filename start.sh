#!/bin/bash

# 等待 MLflow 服务器启动（如果外部运行在端口 5001）
echo "Waiting for external MLflow server on port 5001..."
sleep 5

# 启动 Jupyter Notebook
jupyter notebook \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --allow-root \
    --config=/etc/jupyter/jupyter_notebook_config.py