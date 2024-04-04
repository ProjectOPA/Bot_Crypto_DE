# 2. step2_transform : Transformation (pré-processing)
# - Une fois les données extraites, cette étape consiste à transformer les données extraites
#   (gestion des valeurs manquantes, création de nouvelles colonnes, normalisation..)
#   pour l'analyse et le traitement par le modèle de Machine Learning.
#     - transformation des données de streamings
import pandas as pd
from pymongo import MongoClient

# authentification à MongoDB
mongo_user = "admin"
mongo_password = "pass"
mongo_host = "localhost"
mongo_port = 27017

# connexion à la base de données et à la collection
client = MongoClient(
    f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
)
db = client["extract_data_binance"]
collection = db["historical_data"]

db_transformed = client["transform_data_binance"]
collection_history_transformed = db_transformed["historical_data_transformed"]


# définition d'une fonction pour transformer les données historiques
def transform_historical_data():
    """
    Description:
    - Calcul des variations journalières des données historiques entre le prix le plus haut et le prix le plus bas
    pour chaque jour afin de mesurer la volatilité du marché dans le but de prédire le prix à la fermeture de chaque bougie.

    Arguments:
    - aucun argument n'est requis

    Returns:
    - stock le résultat dans une nouvelle collection nommée "historical_data_transformed"

    Cette fonction se connecte à une base de données MongoDB,
    récupère les données historiques de prix,
    calcule le taux de variation journalier,
    effectue le nettoyage des données,
    et stocke le résultat dans une nouvelle collection

    """
    # suppression de tous les documents existants dans la collection
    # pour éviter les doublons de données
    collection_history_transformed.delete_many({})

    # récupération des données dans un DataFrame
    df = pd.DataFrame(list(collection.find()))

    # calcul du taux de variation journalier entre le prix le plus haut et le prix le plus bas
    df["taux_variation"] = (df["high"] - df["low"]) / df["low"] * 100

    # suppression des colonnes non nécessaires au machine learning
    # il est nécessaire de supprimer la colonne "_id" qui est un objet de type ObjectId de MongoDB
    # pour éviter une erreur lors de l'entraînement du modèle
    df = df.drop(["timestamp", "_id", "symbol"], axis=1)

    print(df.head())

    # stockage des données transformées dans une nouvelle collection
    collection_history_transformed.insert_many(
        df.to_dict(orient="records"), ordered=False
    )


# si le script est exécuté directement en ligne de commande (et non importé en tant que module)
if __name__ == "__main__":
    # appel de la fonction pour transformer les données historiques
    transform_historical_data()
