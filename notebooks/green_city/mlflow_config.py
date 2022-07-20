import os
from pathlib import Path

def get_mlflow_config(base_dir = ".."):
    base_dir = Path(base_dir)

    try:
        TRACKING_URI = open(base_dir / ".mlflow_uri").read().strip()
    except:
        TRACKING_URI = os.getenv("MLFLOW_URI")
    
    EXPERIMENT_NAME = "green_city_experiments"
    
    return {
        "TRACKING_URI": TRACKING_URI,
        "EXPERIMENT_NAME": EXPERIMENT_NAME,
    }