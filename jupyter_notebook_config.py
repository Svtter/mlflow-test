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

# Jupyter Server Proxy 配置
c.ServerProxy.servers = {
    'mlflow': {
        'port': 5000,
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