from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pymysql

# Configuración de conexión a MySQL
MYSQL_HOST = "mysql_container"
MYSQL_USER = "airflow"
MYSQL_PASSWORD = "airflow"
MYSQL_DATABASE = "penguins_db"

def reset_database():
    """Conecta a MySQL y borra los datos de la tabla 'penguins'."""
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    cursor = connection.cursor()

    # Crear la tabla si no existe
    create_table_query = """
    CREATE TABLE IF NOT EXISTS penguins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        species VARCHAR(50),
        island VARCHAR(50),
        bill_length_mm FLOAT,
        bill_depth_mm FLOAT,
        flipper_length_mm FLOAT,
        body_mass_g FLOAT,
        sex VARCHAR(10)
    );
    """
    cursor.execute(create_table_query)

    # Borrar datos de la tabla
    delete_query = "DELETE FROM penguins;"
    cursor.execute(delete_query)

    connection.commit()
    cursor.close()
    connection.close()
    print("Base de datos reseteada correctamente.")

# Configuración del DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 9),
}

with DAG(
    dag_id="reset_penguins_db",
    default_args=default_args,
    schedule_interval="@once",
    catchup=False,
) as dag:
    
    reset_db_task = PythonOperator(
        task_id="reset_database",
        python_callable=reset_database
    )

    reset_db_task
