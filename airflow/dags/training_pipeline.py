from asyncio import tasks
import json
from textwrap import dedent
import pendulum
import os
from airflow import DAG
from airflow.operators.python import PythonOperator

# DAG is directed acyclic graph in airflow. we need to define pipling in airflow
with DAG(
    'sensor_training',
    default_args={'retries': 2}, #default augument
    # [END default_args]
    description='Sensor Fault Detection',
    schedule_interval="@weekly",
    start_date=pendulum.datetime(2022, 2, 2, tz="UTC"),
    catchup=False,
    tags=['example'],
) as dag:

    # defing a funtion which i want to call
    def training(**kwargs):
        from sensor.pipeline.training_pipeline import start_training_pipeline #we are importing the file training pipline
        start_training_pipeline()
    
    def sync_artifact_to_s3_bucket(**kwargs):
        bucket_name = os.getenv("BUCKET_NAME")
        os.system(f"aws s3 sync /app/artifact s3://{bucket_name}/artifacts") #save artifect folder
        os.system(f"aws s3 sync /app/saved_models s3://{bucket_name}/saved_models") #save saved_models folder

    # we are going to creat operators in airflow and we give task id to operator and colablr fun name 
    training_pipeline  = PythonOperator(
            task_id="train_pipeline",
            python_callable=training

    )
    
    sync_data_to_s3 = PythonOperator(
            task_id="sync_data_to_s3",
            python_callable=sync_artifact_to_s3_bucket

    )
    #  we want to run our training pipeline 
    training_pipeline >> sync_data_to_s3