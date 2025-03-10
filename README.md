# 🐧 Penguin Species Prediction API con Airflow y FastAPI
Este proyecto es una API construida con FastAPI y Docker Compose, que permite predecir la especie de un pingüino en base a sus características morfológicas.

Además, integra Apache Airflow para la gestión de tareas como la carga, preprocesamiento y entrenamiento de modelos de Machine Learning en un flujo de trabajo automatizado.

## 🚀 Tecnologías Utilizadas
- FastAPI (para construir la API)
- Uvicorn (servidor ASGI)
- Scikit-learn (para modelos de ML)
- XGBoost (modelo de boosting)
- Joblib (para serializar los modelos)
- Apache Airflow (para la orquestación del flujo de datos)
- MySQL (base de datos relacional para almacenar los datos de entrenamiento)
- Redis (broker para la ejecución distribuida en Airflow)
- Docker & Docker Compose (para contenerización y orquestación de servicios)
- JupyterLab (para la exploración y análisis de datos)

## 📚 Estructura del Proyecto

📦 penguin_project
│-- 📂 app/                    # Código de la API en FastAPI
│   │-- 📄 fastapi_penguins.py  # API FastAPI con modelos ML
│-- 📂 dags/                   # DAGs de Airflow para procesamiento de datos
│   │-- 📄 1_mysql.py           # Reseteo de la base de datos
│   │-- 📄 2_load_data.py       # Carga de datos en MySQL
│   │-- 📄 3_preprocess.py      # Preprocesamiento de datos
│   │-- 📄 4_train_model.py     # Entrenamiento de modelos
│-- 📂 models/                 # Modelos entrenados (.pkl)
│-- 📂 static/                 # Archivos estáticos (HTML, CSS, JS)
│-- 📂 Archivos_Profesor/      # Dataset original (CSV)
│-- 📄 Dockerfile              # Configuración de la imagen Docker
│-- 📄 docker-compose.yml      # Orquestación de servicios con Docker Compose
│-- 📄 requirements.txt        # Dependencias de Python
│-- 📄 requirements.uv         # Dependencias con UV
│-- 📄 README.md               # Documentación del proyecto

## 🛠️ Instalación y Ejecución Local

### 1️⃣ Clonar el Repositorio

git clone https://github.com/zafrar0926/penguins_api_airflow.git
cd penguins_api_airflow

### 2️⃣ Construir y levantar los contenedores con Docker Compose

docker-compose up --build -d

Esto levantará:

- Apache Airflow en el puerto 8080
- FastAPI en el puerto 8989
- JupyterLab en el puerto 8888
- Base de datos MySQL en el puerto 3306

## 📊 Flujo de Datos con Airflow

- 1️⃣ reset_penguins_db (DAG 1): Reinicia la base de datos y estructura la tabla penguins.
- 2️⃣ load_penguins_data (DAG 2): Carga los datos desde el CSV a la base de datos MySQL.
- 3️⃣ preprocess_penguins_data (DAG 3): Preprocesa los datos para eliminar valores nulos y codificar variables categóricas.
- 4️⃣ train_penguins_model (DAG 4): Entrena modelos de Machine Learning (Árbol de Decisión y XGBoost) y los guarda en /models/.

## 📌 Uso de la API

**🔹 Ejemplo de Petición POST a /predict**

curl -X POST "http://localhost:8989/predict" -H "Content-Type: application/json" -d '{
  "island": "Torgersen",
  "culmen_length_mm": 50.0,
  "culmen_depth_mm": 15.0,
  "flipper_length_mm": 200.0,
  "body_mass_g": 4000.0,
  "sex": "MALE",
  "model": "decision_tree"
}'

**🔹 Respuesta Esperada:**

{
  "species_predicted": "Chinstrap"
}

- 📌 Modelos disponibles:

"model": "decision_tree"
"model": "xgboost"

## 🎯 Ejecutar DAGs en Airflow
- 1️⃣ Accede a Airflow 👉 http://localhost:8080
- 2️⃣ Habilita los DAGs en la interfaz
- 3️⃣ Ejecuta los DAGs en orden:

✅ reset_penguins_db
✅ load_penguins_data
✅ preprocess_penguins_data
✅ train_penguins_model
🚀 Después de ejecutar estos DAGs, los modelos estarán listos para su uso en la API.

## 👥 Desarrollado por
🔹 Santiago Zafra Rodríguez 🚀
🔹 Edwin A. Caro 🚀
🔹 Andrés F. Matallana 🚀

