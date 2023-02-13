# https://medium.com/@amir_masoud/setup-collaborative-mlflow-with-postgresql-as-tracking-server-and-minio-as-artifact-store-using-45c76a9d9814
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

import os
import mlflow
import mlflow.sklearn

os.environ['MLFLOW_TRACKING_URI'] = 'mysql+pymysql://mlflow_user:mlflow@127.0.0.1:10336/mlflow_database'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://127.0.0.1:10390"
os.environ['AWS_ACCESS_KEY_ID'] = 'minio'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minio123'

experiment_name = "smoke_experiment"

try:
    mlflow.create_experiment(experiment_name, artifact_location="s3://mlflow")
except mlflow.MlflowException as e:
    print(e)
mlflow.set_experiment(experiment_name)
