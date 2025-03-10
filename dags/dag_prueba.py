from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def list_archivos():
    path = "/opt/airflow/dags/Archivos_Profesor"
    archivos = os.listdir(path)
    print("Archivos en {}: {}".format(path, archivos))
    return archivos

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 9),
}

with DAG(
    dag_id="debug_list_archivos",
    default_args=default_args,
    schedule_interval="@once",
    catchup=False,
) as dag:
    
    list_task = PythonOperator(
        task_id="list_files",
        python_callable=list_archivos
    )

    list_task
