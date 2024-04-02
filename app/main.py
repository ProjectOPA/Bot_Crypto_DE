from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_home():
    return {"msg": "Hello World"}


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
