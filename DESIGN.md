# PyTorch + MLflow Docker Image Design

## 概述
创建一个包含 PyTorch 和 MLflow 的 Docker 镜像，支持通过 Jupyter Notebook web 界面访问 MLflow 跟踪服务器。

## 技术栈
- **基础镜像**: `pytorch/pytorch` (官方 PyTorch 镜像)
- **MLflow**: 最新稳定版本
- **Jupyter Notebook**: 用于交互式开发
- **Web 接口**: MLflow UI (端口 5000) + Jupyter (端口 8888)

## 功能特性
1. PyTorch 深度学习框架
2. MLflow 实验跟踪和模型管理
3. Jupyter Notebook 开发环境
4. MLflow 服务器自动启动
5. 数据持久化支持

## 目录结构
```
mlflow-pytorch-docker/
├── Dockerfile
├── start.sh
├── requirements.txt
└── README.md
```

## 端口配置
- **5000**: MLflow 跟踪服务器 UI
- **8888**: Jupyter Notebook 界面
- **6006**: TensorBoard (可选)

## 数据持久化
- `/mlflow`: MLflow 实验数据存储
- `/notebooks`: Jupyter notebook 工作目录
- `/models`: 训练好的模型存储

## 启动流程
1. 启动 MLflow 跟踪服务器
2. 启动 Jupyter Notebook
3. 暴露 web 接口端口