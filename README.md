# MLflow On-Premise Deployment using Docker Compose
Easily deploy an MLflow tracking server with 1 command.

MinIO S3 is used as the artifact store and MySQL server is used as the backend store.

## Development notes

### Listening ports - `103xx`

Services will listening on `103xx` ports

| Services            | Ports       |
| ------------------- | ----------- |
| web(mlflow_service) | 10380       |
| database(MySQL)     | 10336       |
| Minio(S3/OSS)       | 10390,10391 |

### Others

- This repository is using PyPI mirror in Dockerfile. The region of mirror is the mainland of China.

## How to run

1. Clone (download) this repository

    ```bash
    git clone https://github.com/sachua/mlflow-docker-compose.git
    ```

2. `cd` into the `mlflow-docker-compose` directory

3. Build and run the containers with `docker-compose`

    ```bash
    docker-compose up -d --build
    ```

4. Access MLflow UI with http://localhost:10380

5. Access MinIO UI with http://localhost:10390

## Containerization

The MLflow tracking server is composed of 4 docker containers:

* MLflow server
* MinIO object storage server
* MySQL database server

## Example

1. Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

2. Install MLflow with extra dependencies, including scikit-learn

    ```bash
    pip install mlflow[extras]
    ```

3. Set environmental variables

    ```bash
    export MLFLOW_TRACKING_URI=http://localhost:10380
    export MLFLOW_S3_ENDPOINT_URL=http://localhost:10390
    ```
4. Set MinIO credentials

    ```bash
    cat <<EOF > ~/.aws/credentials
    [default]
    aws_access_key_id=minio
    aws_secret_access_key=minio123
    EOF
    ```

5. Train a sample MLflow model

    ```bash
    mlflow run https://github.com/mlflow/mlflow-example.git -P alpha=0.42
    ```

    * Note: To fix ModuleNotFoundError: No module named 'boto3'

        ```bash
        #Switch to the conda env
        conda env list
        conda activate mlflow-3eee9bd7a0713cf80a17bc0a4d659bc9c549efac #replace with your own generated mlflow-environment
        pip install boto3
        ```

 6. Serve the model (replace with your model's actual path)
    ```bash
    mlflow models serve -m S3://mlflow/0/98bdf6ec158145908af39f86156c347f/artifacts/model -p 1234
    ```

 7. You can check the input with this command
    ```bash
    curl -X POST \
      -H "Content-Type:application/json; format=pandas-split" \
      --data '{"columns":["alcohol", "chlorides", "citric acid", "density", "fixed acidity", "free sulfur dioxide", "pH", "residual sugar", "sulphates", "total sulfur dioxide", "volatile acidity"],"data":[[12.8, 0.029, 0.48, 0.98, 6.2, 29, 3.33, 1.2, 0.39, 75, 0.66]]}' \
      http://127.0.0.1:1234/invocations
    ```

## Credits

This project is updated base on [mlflow-docker-compose@sachua](https://github.com/sachua/mlflow-docker-compose)

## FQA

**MySQL client(GUI) fail to connect to MySQL Server(docker-compose service)**

```shell
### enter into shell of mysql server
$ docker-compose exec db bash
### use mysql client
bash-4.4# mysql -u root -p
Enter password: mysql
...
### fix problem:
mysql> CREATE USER 'mlflow_user'@'127.0.0.1' IDENTIFIED BY 'mlflow';
Query OK, 0 rows affected (0.30 sec)

mysql> GRANT ALL PRIVILEGES ON *.* TO 'mlflow_user'@'127.0.0.1' WITH GRANT OPTION;
Query OK, 0 rows affected (0.05 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.04 sec)

mysql> \q
Bye
bash-4.4# exit
exit
$ 
```
