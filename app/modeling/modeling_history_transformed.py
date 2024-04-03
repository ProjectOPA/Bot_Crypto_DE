# 4. step4_modeling : Machine Learning (Apprentissage automatique)
#     - construction du modèle (séparation de la variable cible des variables explicatives,
#       séparation du jeu d'entraînement et du jeu de test)
#     - entrainement du modèle
#     - évaluation du modèle
#     - test du modèle sur les données de streaming
import pandas as pd
import warnings
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# authentification à MongoDB
mongo_user = "admin"
mongo_password = "pass"
mongo_host = "localhost"
mongo_port = 27017

# connexion à la base de données et à la collection
client = MongoClient(
    f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
)

db_transformed = client["transform_data_binance"]
collection_history_transformed = db_transformed["historical_data_transformed"]


# définition d'une fonction pour entraîner un modèle de régression linéaire
def train_linear_regression_model():
    warnings.filterwarnings("ignore")
    """
    - Entraîne un modèle de régression linéaire pour prédire le prix de clôture suivant à partir des données stockées dans MongoDB.

        - utilisation de méthode de régression linéaire de l'apprentissage supervisé

        - utilisation de la variable 'next_close' comme valeur cible(étiquette) dans les données d'apprentissage supervisé

    - Définition des valeurs explicatives (caractéristiques)

        - Prix d'ouverture (open)

        - Prix le plus haut (high)

        - Prix le plus bas (low)

        - Prix auquel la paire de trading a été échangée à la fin de cette bougie (close )

        - Volume de transactions (volume)

    - Définition de la valeur cible (étiquette)

        - La valeur cible sera la variable 'next_close' indiquant le prix de fermeture de la bougie suivantes.

    Returns:
    - regressor (LinearRegression): Le modèle de régression linéaire entraîné.

    Cette fonction se connecte à une base de données MongoDB,
    récupère les données historiques transformées,
    entraîne un modèle de régression linéaire,
    évalue sa performance sur les ensembles d'entraînement et de test.

    """
    # récupération des données dans un DataFrame
    df = pd.DataFrame(list(collection_history_transformed.find()))

    # il est nécessaire de supprimer la colonne "_id" qui est un objet de type ObjectId de MongoDB
    # pour éviter une erreur lors de l'entraînement du modèle. Nous supprimons également la variable taux de variation, issue d'un calcul sur les données existantes et donc génératrive de biais
    df = df.drop(["_id", "taux_variation"], axis=1)

    # Création de la variable cible next_close qui correspond à la valeure suivante de la crypto
    df["next_close"] = df["close"].shift(-1)

    # Suppression des lignes avec valeurs manquantes (1 seule valeur manquante dans notre cas d'espèces)
    df = df.dropna()
    # séparation du jeu d'entraînement et du jeu de test

    # Separation des variable feats et de la variable cible à prédire
    feats = df.drop("next_close", axis=1)
    target = df["next_close"]

    X_train, X_test, y_train, y_test = train_test_split(
        feats, target, test_size=0.20, random_state=42
    )

    # initialisation du modèle de régression linéaire
    regressor = LinearRegression()

    # entrainement du modèle de régression linéaire
    regressor.fit(X_train, y_train)

    # évaluation de la performance du modèle
    print("score sur test:", regressor.score(X_test, y_test))

    print("score sur train:", regressor.score(X_train, y_train))

    return regressor


# si le script est exécuté directement en ligne de commande (et non importé en tant que module)
if __name__ == "__main__":
    # appel de la fonction pour entraîner le modèle de régression linéaire
    model = train_linear_regression_model()
