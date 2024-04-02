from pymongo import MongoClient

# import de BaseModel du module pydantic pour définir des modèles de données
from pydantic import BaseModel

# import de List pour définir une liste de données
# import de Optional pour définir des types de données
from typing import Optional, List


# authentification à MongoDB
# définition des informations d'identification nécessaires
# pour s'authentifier auprès de MongoDB en local
mongo_user = "admin"
mongo_password = "pass"
mongo_host = "localhost"
mongo_port = 27017

# connexion à MongoDB avec authentification
# création du client MongoDB
# pour établir une connexion à la base de données MongoDB
# Le client est connecté à l'instance MongoDB
# en cours d'exécution sur "localhost" sur le port 27017
client = MongoClient(
    f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
)

# connexion à la database "extract_data_binance" MongoDB
db = client["extract_data_binance"]
collection = db["historical_data"]


# définition d'un corps de requete pour la route /historical
# cette requete doit être de type GET pour récupérer les données historiques
# en fonction de la date de début et de la date de fin de la période
# les données historiques sont stockées dans une base de données mongoDB
# définition de la classe HistoricalRequest qui hérite de BaseModel
class HistoricalRequest(BaseModel):
    start_date: str
    end_date: str


# définition d'un corps de reponse pour la route /historical
# cette réponse doit être de type JSON
# les données historiques sont stockées dans une base de données mongoDB
# la réponse doit être un tableau de données historiques
# définition de la classe HistoricalResponse qui hérite de BaseModel
class HistoricalResponse(BaseModel):
    data: list


# définition d'un corps de requete pour la route /predict
# cette requete doit être de type GET pour récupérer les prédictions
# en fonction de la date de début et de la date de fin de la période
# définition de la classe PredictRequest qui hérite de BaseModel
class PredictRequest(BaseModel):
    start_date: str
    end_date: str


# définition d'un corps de reponse pour la route /predict
# cette réponse doit être de type JSON
# les prédictions sont stockées dans une base de données mongoDB
# la réponse doit être un tableau de prédictions
# définition de la classe PredictResponse qui hérite de BaseModel
class PredictResponse(BaseModel):
    data: list
