# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a PyTorch + MLflow Docker project that provides a complete machine learning development environment with experiment tracking capabilities. The container includes Jupyter Notebook for interactive development and MLflow for experiment management.

## Architecture

The project consists of:
- **Docker container** built from `pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime`
- **MLflow tracking server** running on port 5000 for experiment tracking
- **Jupyter Notebook** running on port 8888 for interactive development
- **Data persistence** through mounted volumes at `/mlflow`, `/notebooks`, and `/models`

## Common Commands

### Development
```bash
# Build the Docker image
docker build -t mlflow-pytorch .

# Run the container
docker run -p 8888:8888 -p 5000:5000 -v $(pwd)/notebooks:/notebooks -v $(pwd)/mlruns:/mlflow mlflow-pytorch

# Run with minimal dependencies
docker build -f Dockerfile.minimal -t mlflow-pytorch-minimal .
```

### Testing
```bash
# Test MLflow connection
python test_connection.py

# Run the main application
python main.py
```

## Key Components

- `start.sh`: Main startup script that launches MLflow server and Jupyter Notebook
- `Dockerfile`: Multi-stage build with PyTorch, CUDA, and all ML dependencies
- `Dockerfile.minimal`: Lightweight version with minimal dependencies
- `requirements.txt`: Python dependencies including MLflow, PyTorch, and data science libraries
- `jupyter_notebook_config.py`: Jupyter configuration for the container environment

## Port Configuration
- **5000**: MLflow tracking server UI
- **8888**: Jupyter Notebook interface

## Data Persistence
The container expects volumes to be mounted at:
- `/mlflow`: MLflow experiment data storage
- `/notebooks`: Jupyter notebook working directory  
- `/models`: Trained model storage

## Dependencies

Core ML/data science stack:
- MLflow (experiment tracking)
- PyTorch/Torchvision (deep learning)
- Jupyter/Notebook (development environment)
- Pandas/NumPy (data manipulation)
- Matplotlib/Seaborn (visualization)
- Scikit-learn (machine learning utilities)