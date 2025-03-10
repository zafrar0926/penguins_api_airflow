from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import pymysql

# Configuración de conexión a MySQL
MYSQL_HOST = "mysql_container"
MYSQL_USER = "airflow"
MYSQL_PASSWORD = "airflow"
MYSQL_DATABASE = "penguins_db"

# Ruta del archivo CSV en el sistema
CSV_PATH = "/opt/airflow/Archivos_Profesor/penguins_size.csv"


def load_csv_to_mysql():
    """Carga datos desde un archivo CSV a MySQL con manejo de NaN."""
    import numpy as np

    # Leer el CSV
    df = pd.read_csv(CSV_PATH)

    # Reemplazar NaN por valores adecuados (ejemplo: NULL en SQL o un valor por defecto)
    df = df.fillna(value=np.nan)  # Opcionalmente, puedes usar df.fillna("NULL") si quieres insertar NULL en SQL
    df = df.replace({np.nan: None})  # Reemplazar NaN con None para que MySQL lo acepte como NULL

    # Conectar a MySQL
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    cursor = connection.cursor()

    # Insertar datos en la tabla
    for _, row in df.iterrows():
        insert_query = """
        INSERT INTO penguins (species, island, bill_length_mm, bill_depth_mm, 
                              flipper_length_mm, body_mass_g, sex)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, tuple(row))

    connection.commit()
    cursor.close()
    connection.close()
    print("Datos cargados correctamente en MySQL.")


# Configuración del DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 9),
}

with DAG(
    dag_id="load_penguins_data",
    default_args=default_args,
    schedule_interval="@once",
    catchup=False,
) as dag:
    
    load_data_task = PythonOperator(
        task_id="load_csv_to_mysql",
        python_callable=load_csv_to_mysql
    )

    load_data_task
