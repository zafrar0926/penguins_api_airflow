FROM python:3.9

WORKDIR /app

COPY app/models /app/models
COPY requirements.uv requirements.uv

# Instalar dependencias directamente con pip
RUN pip install --upgrade pip && \
    pip install -r requirements.uv

COPY . .

CMD ["uvicorn", "app.fastapi_penguins:app", "--host", "0.0.0.0", "--port", "8989"]
