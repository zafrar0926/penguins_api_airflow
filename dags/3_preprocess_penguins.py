from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine

def preprocess_penguins():
    # Crear conexión a MySQL usando SQLAlchemy
    engine = create_engine("mysql+pymysql://airflow:airflow@mysql_container/penguins_db")
    
    # Leer los datos de la tabla 'penguins'
    try:
        df = pd.read_sql("SELECT * FROM penguins", con=engine)
    except Exception as e:
        print("Error al leer datos de MySQL:", e)
        raise

    print("Datos originales:")
    print(df.head())
    
    # Aplicar imputación de valores nulos usando la estrategia 'most_frequent'
    imputer = SimpleImputer(strategy='most_frequent')
    df[:] = imputer.fit_transform(df)
    
    # Detectar y codificar columnas categóricas (si existen)
    categorical_cols = []
    for col in ['island', 'sex', 'species']:
        if col in df.columns:
            categorical_cols.append(col)
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    print("Datos preprocesados:")
    print(df.head())
    
    # Guardar los datos preprocesados en una nueva tabla en MySQL
    df.to_sql("penguins_preprocessed", con=engine, if_exists="replace", index=False)
    print("Datos preprocesados guardados en la tabla 'penguins_preprocessed'.")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 9),
}

with DAG(
    dag_id="preprocess_penguins_data",
    default_args=default_args,
    schedule_interval="@once",
    catchup=False,
    description="Lee datos de la tabla 'penguins', los preprocesa y los guarda en 'penguins_preprocessed'."
) as dag:
    
    preprocess_task = PythonOperator(
        task_id="preprocess_penguins",
        python_callable=preprocess_penguins
    )

    preprocess_task
