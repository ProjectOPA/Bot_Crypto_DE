from pymongo import MongoClient
from pydantic import BaseModel
from fastapi import HTTPException
from typing import Optional

# connexion à MongoDB avec authentification
mongo_user = "admin"
mongo_password = "pass"
mongo_host = "mongo-project-api-binance"
mongo_port = 27017
client = MongoClient(
    f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
)

# connexion à la base de données "extract_data_binance" pour les données historiques
db_historical = client["extract_data_binance"]
collection_historical = db_historical["historical_data"]

# connexion à la base de donnnées "transform_data_binance" pour les données historiques transformées
db_transformed = client["transform_data_binance"]
collection_history_transformed = db_transformed["historical_data_transformed"]

# connexion à la base de données "streaming_data" pour les données de prédiction
db_streaming = client["streaming_data"]
collection_streaming = db_streaming["streaming_data_predict"]


# définition du modèle de corps de réponse pour les données historiques
class HistoricalData(BaseModel):
    _id: str
    symbol: str
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float

# définition du modèle de corps de réponse pour les données historiques transformées
class TransformedData(BaseModel):
    _id: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    taux_variation: float

# définition du modèle de corps de réponse pour les données de prédiction
class PredictionData(BaseModel):
    _id: str
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    next_close: float


# définition de la fonction pour récupérer des données historiques de MongoDB
# qui prend un filtre en paramètre pour filtrer les données
# la fonction renvoie une liste de données historiques si aucune erreur n'est levée
    
def get_historical_data(filter=None):
    # projection est utilisé pour filtrer les champs à renvoyer
    # 1 signifie que le champ est inclus, 0 signifie qu'il est exclu
    # par défaut, tous les champs sont inclus
    try:
        projection = {
            "_id": 1,
            "symbol": 1,
            "timestamp": 1,
            "open": 1,
            "high": 1,
            "low": 1,
            "close": 1,
            "volume": 1,
        }
        # si un filtre est fourni, les données sont filtrées en fonction du filtre
        if filter:
            # définition de data pour stocker les données filtrées
            # la méthode find() de PyMongo est utilisée pour récupérer les données de la collection
            # la méthode find() prend en argument le filtre et la projection
            data = list(collection_historical.find(filter, projection=projection))
        else:
            # si aucun filtre n'est fourni, toutes les données sont récupérées
            # la méthode find() est appelée sans filtre
            # la méthode find() prend en argument la projection
            data = list(collection_historical.find({}, projection=projection))
        # définition d'une boucle pour formater les données
        # la boucle convertit l'objet ObjectId en chaîne pour l'ID
        # et convertit l'objet datetime en chaîne pour la date

        for item in data:
            item["_id"] = str(item["_id"])
            # le fomat de la date est de type ISODate sur MongoDB,
            # .isoformat() est une méthode de l'objet datetime en Python,
            # qui convertit un objet datetime en une chaîne de caractères représentant la date et l'heure au format ISO 8601.
            item["timestamp"] = item["timestamp"].isoformat()
        # retourne les données formatées
        return data
    # lève une exception si une erreur est rencontrée
    except Exception as e:
        return {"error": str(e)}



# définition de la fonction pour récupérer des données historiques transformées de MongoDB
# qui prend un nombre d'éléments en paramètre pour limiter les données
# la fonction renvoie une liste de données historiques transformées si aucune erreur n'est levée
def get_transformed_data(number_of_items: Optional[int] = None):
    try:
        # définition d'une variable pour stocker le nombre d'éléments
        # si le nombre d'éléments est fourni, le nombre d'éléments est défini
        # sinon, le nombre d'éléments est défini à 0
        limit = number_of_items if number_of_items else 0

        # définition  d'une variable pour stocker les données transformées
        # création d'une liste de données transformées en utilisant la méthode find() de PyMongo
        # appel de la méthode find() sur la collection_history_transformed pour récupérer les données
        # appel de la méthode limit() pour limiter le nombre d'éléments
        # la méthode limit() prend en argument le nombre d'éléments
        transformed_data = list(collection_history_transformed.find().limit(limit))

        # définition d'une boucle pour formater les données
        # la boucle convertit l'objet ObjectId en chaîne pour l'ID
        for item in transformed_data:
            item["_id"] = str(item["_id"])

        # retourne les données formatées
        return transformed_data
    except Exception as e:
        return {"error": str(e)}

# définition de la fonction pour récupérer des données de prédiction de MongoDB
def get_prediction_data(filter=None):
    # projection est utilisé pour filtrer les champs à renvoyer
    # 1 signifie que le champ est inclus, 0 signifie qu'il est exclu
    # par défaut, tous les champs sont inclus
    try:
        projection = { 
            "_id": 1,
            "timestamp": 1,
            "open": 1,
            "high": 1,
            "low": 1,
            "close": 1,
            "volume": 1,
            "next_close": 1
        }
        # si un filtre est fourni, les données sont filtrées en fonction du filtre
        if filter:
            # définition de data pour stocker les données filtrées
            # la méthode find() de PyMongo est utilisée pour récupérer les données de la collection
            # la méthode find() prend en argument le filtre et la projection
            prediction_data = list(
                collection_streaming.find(filter, projection=projection)
            )
        else:
            # si aucun filtre n'est fourni, toutes les données sont récupérées
            # la méthode find() est appelée sans filtre
            # la méthode find() prend en argument la projection

            prediction_data = list(collection_streaming.find({}, projection=projection))
            
        # définition d'une boucle pour formater les données
        # la boucle convertit l'objet ObjectId en chaîne pour l'ID
        # et convertit l'objet datetime en chaîne pour la date
        for item in prediction_data:
            item["_id"] = str(item["_id"])
            # le fomat de la date est de type ISODate sur MongoDB,
            # .isoformat() est une méthode de l'objet datetime en Python,
            # qui convertit un objet datetime en une chaîne de caractères représentant la date et l'heure au format ISO 8601.
            item["timestamp"] = item["timestamp"].isoformat()
        # retourne les données formatées
        return prediction_data
    # lève une exception si une erreur est rencontrée
    except Exception as e:
        return {"error": str(e)}


#Fonction pour Consieller sur un investissement
def advice():
    latest = collection_streaming.find_one(sort=[("timestamp", -1)])

    if latest:
        result = {"next_price":str(latest.get("next_close"))+" USD",
                  "actual_price": str(latest.get("close"))+" USD" }
        if latest.get("next_close") >= latest.get("close"):
            result['advice'] = "En vue de l'augmentation prochaine de la valeur nous vous conseillons d'acheter"
        else:
            result['advice'] = "En vue de la diminution prochaine de la valeur nous vous conseillons de vendre"
        return result
    else:
        raise HTTPException(status_code=404, detail="Aucun document dans la collection des prédictions")