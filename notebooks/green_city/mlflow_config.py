import os
from pathlib import Path
from contextlib import contextmanager

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

class MlflowRunInfoDummy():
    def __init__(self):
        self.run_uuid = "NO_UUID_BC_DUMMY"
        self.run_id = "NO_ID_BC_DUMMY"

class MlflowRunDummy():
    def __init__(self):
        self.info = MlflowRunInfoDummy()
    #def __enter__(self):
    #    return self
    #def __exit__(self):
    #    pass

class MlflowDummy():
    def __init__(self):
        pass
    def set_tracking_uri(self, *args, **kwargs):
        pass
    def set_experiment(self, *args, **kwargs):
        pass

    @contextmanager
    def start_run(self, *args, **kwargs):
        try:
            yield MlflowRunDummy()
        finally:
            pass

    def log_param(self, *args, **kwargs):
        pass
    def log_params(self, *args, **kwargs):
        pass
    def log_metric(self, *args, **kwargs):
        pass
    def log_metrics(self, *args, **kwargs):
        pass