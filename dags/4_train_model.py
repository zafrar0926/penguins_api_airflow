from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from xgboost import XGBClassifier
import os

def train_models():
    # Crear el directorio si no existe
    models_dir = "/opt/airflow/models/"
    os.makedirs(models_dir, exist_ok=True)
    # Conexión a la base de datos MySQL
    engine = create_engine("mysql+pymysql://airflow:airflow@mysql_container/penguins_db")
    
    # Leer datos preprocesados de la tabla 'penguins_preprocessed'
    df = pd.read_sql("SELECT * FROM penguins_preprocessed", con=engine)
    print("Datos preprocesados:")
    print(df.head())
    
    # Suponemos que la columna objetivo es 'species'
    X = df.drop('species', axis=1)
    y = df['species']
    
    # Dividir en conjunto de entrenamiento y prueba (80%/20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entrenar modelo de Árbol de Decisión
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    y_pred_dt = dt_model.predict(X_test)
    
    acc_dt = accuracy_score(y_test, y_pred_dt)
    rec_dt = recall_score(y_test, y_pred_dt, average='weighted')
    prec_dt = precision_score(y_test, y_pred_dt, average='weighted')
    f1_dt = f1_score(y_test, y_pred_dt, average='weighted')
    
    print("Métricas del Árbol de Decisión:")
    print(f"Accuracy: {acc_dt}")
    print(f"Recall: {rec_dt}")
    print(f"Precision: {prec_dt}")
    print(f"F1 Score: {f1_dt}")
    
    # Entrenar modelo XGBoost
    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=42)
    xgb_model.fit(X_train, y_train)
    y_pred_xgb = xgb_model.predict(X_test)
    
    acc_xgb = accuracy_score(y_test, y_pred_xgb)
    print("Métricas de XGBoost:")
    print(f"Accuracy: {acc_xgb}")
    
    # Guardar los modelos en la carpeta montada para modelos
    joblib.dump(dt_model, "/opt/airflow/models/decision_tree_model.pkl")
    joblib.dump(xgb_model, "/opt/airflow/models/xgboost_model.pkl")
    print("Modelos guardados correctamente.")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 9),
}

with DAG(
    dag_id="train_penguins_model",
    default_args=default_args,
    schedule_interval="@once",
    catchup=False,
    description="Entrena modelos usando datos preprocesados de la tabla 'penguins_preprocessed'"
) as dag:
    
    train_task = PythonOperator(
        task_id="train_models",
        python_callable=train_models
    )
    
    train_task