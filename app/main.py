from fastapi import FastAPI
from mongo_query import HistoricalRequest, HistoricalResponse, PredictRequest, PredictResponse

# définition de l'application FastAPI
# en utilisant la classe FastAPI de FastAPI
# pour créer une application.
app = FastAPI(
    title="API Questions",
    description=""" 
                          
    """,
    version="1.0.1",
    openapi_tags=[
        {"name": "home", "description": "page d'accueil de l'API"},
        {"name": "historical", "description": "page requete sur les données historiques"},
        {"name": "predict", "description": "page requete sur les prédictions"},
    ],
)

@app.get("/")
def get_home():
    return {"msg": "Hello World"}

@app.get("/historical"):
    pass
    """
    
    """


@app.get("/predict")
def get_predict():
    pass


# exécution de l'API FastAPI
# lorsque le script est exécuté en tant que programme principal
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


# exécution de l'API Fastapi dans le terminal
# uvicorn main:app --reload ou python3 main.py
