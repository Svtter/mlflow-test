import requests
import time

def test_jupyter():
    try:
        response = requests.get('http://localhost:8889', timeout=5)
        print(f"Jupyter Server: OK (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"Jupyter Server: ERROR - {e}")
        return False

def test_mlflow():
    try:
        response = requests.get('http://localhost:5002', timeout=5)
        print(f"MLflow Server: OK (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"MLflow Server: ERROR - {e}")
        return False

if __name__ == "__main__":
    print("Testing connections to Docker services...")
    
    # Wait a moment for services to be fully ready
    time.sleep(2)
    
    jupyter_ok = test_jupyter()
    mlflow_ok = test_mlflow()
    
    if jupyter_ok and mlflow_ok:
        print("\n✅ All services are running successfully!")
        print("Jupyter Notebook: http://localhost:8889")
        print("MLflow UI: http://localhost:5002")
    else:
        print("\n❌ Some services failed to start")