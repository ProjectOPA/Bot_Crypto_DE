# 2. step2_transform : Transformation (pré-processing)
# - Une fois les données extraites, cette étape consiste à transformer les données extraites
#  (gestion des valeurs manquantes, création de nouvelles colonnes, normalisation..)
#   pour l'analyse et le traitement par le modèle de Machine Learning.
#     - transformation des données historiques stockées

import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.impute import SimpleImputer
from transform_history import transform_historical_data

# authentification à MongoDB
mongo_user = "admin"
mongo_password = "pass"
mongo_host = "localhost"
mongo_port = 27017

# connexion à la base de données et à la collection
client = MongoClient(
    f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
)

# instanciation de la base de données
db = client["extract_data_binance"]

# instanciation de la collection
collection = db["streaming_data"]


# utilisation du modèle entraîné pour prédire le valeur cible 'close' sur des données de streaming
def transform_streaming_data():
    pass
