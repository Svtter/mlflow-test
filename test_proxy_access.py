#!/usr/bin/env python3
"""
测试脚本：验证是否可以通过 notebook 端口访问 MLflow
"""

import requests
import json
from urllib.parse import urljoin

def test_mlflow_access():
    """测试 MLflow 访问"""
    
    # 测试直接访问 MLflow
    mlflow_url = "http://localhost:5001"
    print(f"测试直接访问 MLflow: {mlflow_url}")
    
    try:
        response = requests.get(mlflow_url)
        print(f"✓ 直接访问 MLflow 成功: {response.status_code}")
    except Exception as e:
        print(f"✗ 直接访问 MLflow 失败: {e}")
        return False
    
    # 测试通过 Jupyter 代理访问 MLflow
    # Jupyter Notebook 的代理通常使用 /proxy/<port>/ 路径
    jupyter_url = "http://localhost:8888"
    proxy_url = f"{jupyter_url}/proxy/5001"
    
    print(f"\n测试通过 Jupyter 代理访问 MLflow: {proxy_url}")
    
    try:
        response = requests.get(proxy_url)
        print(f"✓ 通过 Jupyter 代理访问 MLflow 成功: {response.status_code}")
        
        # 检查响应内容是否包含 MLflow 相关内容
        if "MLflow" in response.text:
            print("✓ 响应内容包含 MLflow")
            return True
        else:
            print("✗ 响应内容不包含 MLflow")
            return False
            
    except Exception as e:
        print(f"✗ 通过 Jupyter 代理访问 MLflow 失败: {e}")
        return False

def test_jupyter_access():
    """测试 Jupyter Notebook 访问"""
    
    jupyter_url = "http://localhost:8888"
    print(f"\n测试 Jupyter Notebook 访问: {jupyter_url}")
    
    try:
        response = requests.get(jupyter_url)
        print(f"✓ Jupyter Notebook 访问成功: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Jupyter Notebook 访问失败: {e}")
        return False

if __name__ == "__main__":
    print("=== 测试 MLflow 访问 ===")
    
    # 测试 Jupyter Notebook 访问
    jupyter_ok = test_jupyter_access()
    
    # 测试 MLflow 访问
    mlflow_ok = test_mlflow_access()
    
    print(f"\n=== 测试结果 ===")
    print(f"Jupyter Notebook: {'✓' if jupyter_ok else '✗'}")
    print(f"MLflow 直接访问: {'✓' if mlflow_ok else '✗'}")
    
    if jupyter_ok and mlflow_ok:
        print("\n✓ 基本功能正常，但需要配置代理以实现通过 notebook 端口访问 MLflow")
    else:
        print("\n✗ 存在配置问题，需要检查")