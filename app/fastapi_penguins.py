from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import joblib
import pandas as pd
from pydantic import BaseModel
import os

# Definir rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = "/app/models"
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Cargar modelos con manejo de errores
try:
    clf = joblib.load(os.path.join(MODEL_DIR, "decision_tree_model.pkl"))
    xgb_model = joblib.load(os.path.join(MODEL_DIR, "xgboost_model.pkl"))
   # svm_model = joblib.load(os.path.join(MODEL_DIR, "svm_model.pkl"))
    label_encoders = joblib.load(os.path.join(MODEL_DIR, "label_encoders.pkl"))
except FileNotFoundError as e:
    raise RuntimeError(f"Error: No se encontró el archivo del modelo: {e}")
except Exception as e:
    raise RuntimeError(f"Error al cargar los modelos: {e}")

# Crear la app
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Servir la página de inicio
@app.get("/", response_class=HTMLResponse)
async def read_root():
    file_path = os.path.join(STATIC_DIR, "index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Definir el esquema de entrada
class PenguinInput(BaseModel):
    island: str
    culmen_length_mm: float
    culmen_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float
    sex: str
    model: str

# Endpoint de predicción
@app.post("/predict")
def predict_species(data: PenguinInput):
    try:
        input_data = pd.DataFrame([data.dict()])

        # Transformar variables categóricas
        for col in ["island", "sex"]:
            if col in input_data:
                input_data[col] = label_encoders[col].transform(input_data[col])

        # Seleccionar el modelo
        if data.model == "decision_tree":
            model = clf
        elif data.model == "xgboost":
            model = xgb_model
        else:
            raise HTTPException(status_code=400, detail="Modelo no válido. Usa 'decision_tree', 'xgboost'")

        # Hacer la predicción
        prediction = model.predict(input_data.drop(columns=["model"]))[0]
        species = label_encoders["species"].inverse_transform([prediction])[0]

        return {"species_predicted": species}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

  