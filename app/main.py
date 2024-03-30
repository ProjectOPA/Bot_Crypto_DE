from fastapi import FastAPI
from extract.extract_history import collect_historical_data
from transform.transform_history import transform_historical_data
from modeling.modeling_history_transformed import (
    train_linear_regression_model as train_lr_model,
)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/collect_historical_data")
def collect_data():
    collect_historical_data()
    return {"message": "Data collected"}


@app.get("/transform_historical_data")
def transform_data():
    transform_historical_data()
    return {"message": "Data transformed"}


@app.get("/train_linear_regression_model")
def train_model():
    train_lr_model()
    return {"message": "Model trained"}


# exécution de l'API FastAPI
# lorsque le script est exécuté en tant que programme principal
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


# exécution de l'API Fastapi dans le terminal
# uvicorn main:app --reload ou python3 main.py
