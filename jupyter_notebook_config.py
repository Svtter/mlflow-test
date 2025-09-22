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