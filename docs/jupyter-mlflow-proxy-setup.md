# 通过 Jupyter Notebook 端口访问 MLflow 的技术方案

## 概述

本文档详细介绍了如何通过 Jupyter Notebook 的端口（8888）访问运行在内部端口（5001）的 MLflow 服务。这种配置允许用户在同一个浏览器标签页中管理 Jupyter Notebook 和 MLflow，简化了工作流程。

## 当前状态分析

### 现有配置
- **Jupyter Notebook**: 运行在端口 8888
- **MLflow**: 运行在端口 5001  
- **问题**: 无法通过 `http://localhost:8888/proxy/5001` 访问 MLflow（返回 404）

### 根本原因
当前的 Jupyter Notebook 配置没有启用服务器代理功能，无法将请求转发到其他端口的服务。

## 技术方案对比

### 方案一：jupyter-server-proxy（推荐）

**优点**：
- 官方支持的解决方案
- 配置简单，只需修改配置文件
- 支持自动生成启动器图标
- 支持路径重写和认证

**缺点**：
- 需要额外安装依赖包
- 需要 JupyterLab 环境支持

**实现复杂度**：低

### 方案二：Nginx 反向代理

**优点**：
- 性能优秀，适合生产环境
- 配置灵活，支持负载均衡
- 与 Jupyter 解耦，互不影响

**缺点**：
- 需要额外的 Nginx 服务
- 配置复杂
- 在 Docker 环境中部署复杂

**实现复杂度**：高

### 方案三：自定义 Notebook 扩展

**优点**：
- 完全自定义集成
- 可以深度集成 MLflow 功能
- 用户体验最好

**缺点**：
- 开发成本高
- 需要前端开发技能
- 维护成本高

**实现复杂度**：很高

## 推荐方案：jupyter-server-proxy

### 核心原理

jupyter-server-proxy 是一个 Jupyter 服务器扩展，允许 Jupyter Notebook 代理到其他 HTTP 服务。它通过以下方式工作：

1. 拦截特定路径的请求（如 `/mlflow` 或 `/proxy/5001`）
2. 将请求转发到配置的后端服务
3. 处理响应并返回给客户端

### 实现步骤

#### 1. 安装依赖

在 `requirements.txt` 中添加：

```python
jupyter-server-proxy>=4.0.0
```

#### 2. 更新 Jupyter 配置

在 `jupyter_notebook_config.py` 中添加：

```python
# 配置服务器代理
c.ServerProxy.servers = {
    'mlflow': {
        'port': 5001,
        'absolute_url': True,
        'launcher_entry': {
            'title': 'MLflow UI',
            'icon_path': '/usr/share/icons/hicolor/48x48/apps/jupyter.png'
        }
    },
    'mlflow-external': {
        'command': ['mlflow', 'server', '--host', '0.0.0.0', '--port', '{port}', '--backend-store-uri', '/mlflow', '--default-artifact-root', '/mlflow'],
        'environment': {},
        'timeout': 30,
        'absolute_url': True,
        'launcher_entry': {
            'title': 'MLflow UI (Internal)',
            'icon_path': '/usr/share/icons/hicolor/48x48/apps/jupyter.png'
        }
    }
}

# 启用代理功能
c.Application.log_level = 'DEBUG'
c.ServerProxy.host_whitelist = ['localhost', '127.0.0.1', '0.0.0.0']
```

#### 3. 更新 Dockerfile

```dockerfile
# 在现有 Dockerfile 基础上添加
RUN pip install jupyter-server-proxy

# 或者使用 conda
RUN conda install -c conda-forge jupyter-server-proxy
```

#### 4. 修改启动脚本

更新 `start.sh` 脚本：

```bash
#!/bin/bash

# 启动 MLflow 跟踪服务器（后台运行）
echo "Starting MLflow server..."
mlflow server \
    --host 0.0.0.0 \
    --port 5001 \
    --backend-store-uri /mlflow \
    --default-artifact-root /mlflow \
    &> /dev/null &

# 等待 MLflow 服务器启动
sleep 3

# 启动 Jupyter Notebook
echo "Starting Jupyter Notebook..."
jupyter notebook \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --allow-root \
    --config=/etc/jupyter/jupyter_notebook_config.py
```

### 访问方式

配置完成后，可以通过以下方式访问 MLflow：

1. **直接代理**: `http://localhost:8888/proxy/5001`
2. **命名代理**: `http://localhost:8888/mlflow`
3. **Jupyter 启动器**: 在 Jupyter 主页点击 "MLflow UI" 图标

### 完整的配置文件

#### 更新后的 jupyter_notebook_config.py

```python
c.NotebookApp.allow_origin = '*'
c.NotebookApp.allow_remote_access = True
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token = ''
c.NotebookApp.password = ''

# 配置 MLflow 代理
c.NotebookApp.allow_origin_pat = '.*'
c.NotebookApp.disable_check_xsrf = True

# 设置工作目录
c.NotebookApp.notebook_dir = '/notebooks'

# 服务器代理配置
c.ServerProxy.servers = {
    'mlflow': {
        'port': 5001,
        'absolute_url': True,
        'launcher_entry': {
            'title': 'MLflow UI',
            'icon_path': '/usr/share/icons/hicolor/48x48/apps/jupyter.png'
        }
    }
}

# 启用代理功能
c.Application.log_level = 'INFO'
c.ServerProxy.host_whitelist = ['localhost', '127.0.0.1', '0.0.0.0']
```

#### 更新后的 requirements.txt

```
mlflow==2.14.0
torch==2.0.1
torchvision==0.15.2
jupyter==1.0.0
notebook==6.5.6
pandas==2.1.4
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
scikit-learn==1.3.2
jupyter-server-proxy>=4.0.0
```

## 部署和测试

### 1. 构建镜像

```bash
docker build -t mlflow-pytorch-proxy .
```

### 2. 运行容器

```bash
docker run -d \
  --name mlflow-test-proxy \
  -p 8888:8888 \
  -p 5001:5001 \
  -v $(pwd)/notebooks:/notebooks \
  -v $(pwd)/mlruns:/mlflow \
  -v $(pwd)/models:/models \
  mlflow-pytorch-proxy
```

### 3. 测试访问

```bash
# 测试 Jupyter Notebook
curl http://localhost:8888

# 测试 MLflow 代理
curl http://localhost:8888/proxy/5001

# 测试命名代理
curl http://localhost:8888/mlflow
```

### 4. 验证功能

1. 打开浏览器访问 `http://localhost:8888`
2. 应该能看到 "MLflow UI" 启动器图标
3. 点击图标或在浏览器中访问 `http://localhost:8888/mlflow`
4. 确认 MLflow 界面正常加载

## 故障排除

### 常见问题

#### 1. 代理无法访问

**症状**：访问 `http://localhost:8888/proxy/5001` 返回 404

**解决方案**：
- 检查 `jupyter-server-proxy` 是否正确安装
- 验证 Jupyter 配置文件语法
- 查看 Jupyter 日志：`docker logs <container-id>`

#### 2. 启动器图标不显示

**症状**：Jupyter 主页没有显示 MLflow 启动器

**解决方案**：
- 检查 `launcher_entry` 配置
- 确保 JupyterLab 已安装
- 重启 Jupyter 服务器

#### 3. 权限问题

**症状**：访问被拒绝或认证失败

**解决方案**：
- 检查 `host_whitelist` 配置
- 确认认证设置
- 验证防火墙规则

### 调试命令

```bash
# 查看容器日志
docker logs mlflow-test-proxy

# 检查代理配置
docker exec mlflow-test-proxy jupyter serverproxy list

# 测试内部连接
docker exec mlflow-test-proxy curl http://localhost:5001

# 检查进程状态
docker exec mlflow-test-proxy ps aux
```

## 高级配置

### 安全增强

```python
# 添加认证令牌
c.ServerProxy.auth_token = 'your-secret-token'

# 限制允许的主机
c.ServerProxy.host_whitelist = ['localhost', '127.0.0.1']

# 启用 HTTPS
c.NotebookApp.certfile = '/path/to/cert.pem'
c.NotebookApp.keyfile = '/path/to/key.pem'
```

### 性能优化

```python
# 增加超时时间
c.ServerProxy.timeout = 60

# 启用压缩
c.ServerProxy.compress_responses = True

# 配置缓存
c.ServerProxy.cache_max_age = 300
```

## 总结

通过使用 `jupyter-server-proxy` 扩展，我们可以轻松实现通过 Jupyter Notebook 端口访问 MLflow 的需求。这个方案具有以下优势：

1. **简单易用**：只需修改配置文件，无需复杂设置
2. **官方支持**：Jupyter 官方维护的解决方案
3. **功能完整**：支持多种代理模式和认证
4. **易于维护**：与现有 Jupyter 环境无缝集成

推荐在生产环境中使用此方案来提供统一的访问入口和更好的用户体验。