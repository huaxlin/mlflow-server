import os
import mlflow

# os.environ['MLFLOW_TRACKING_URI'] = 'mysql+pymysql://mlflow_user:mlflow@127.0.0.1:10336/mlflow_database'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://127.0.0.1:10390"
os.environ['AWS_ACCESS_KEY_ID'] = 'minio'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minio123'

os.environ['MLFLOW_TRACKING_URI'] = 'http://127.0.0.1:10380'
experiment_name = "experiment_insurance"
try:
    mlflow.create_experiment(experiment_name, artifact_location="s3://insurance/mlflow/artifacts")
except mlflow.MlflowException as e:
    print('-' * 10, 'SKIP EXIST', '-' * 10, '\n', e, '\n', '-' * 30)
mlflow.set_experiment(experiment_name)

mlflow.start_run()
# Log a parameter (key-value pair)
mlflow.log_param("param1", 5)

# Log a metric; metrics can be updated throughout the run
mlflow.log_metric("foo", 1)
mlflow.log_metric("foo", 2)
mlflow.log_metric("foo", 3)

# Log an artifact (output file)
with open("output.txt", "w") as f:
    f.write("Hello world!")
mlflow.log_artifact("output.txt")
mlflow.end_run()
