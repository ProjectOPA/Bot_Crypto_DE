import pandas as pd
import numpy as np
import warnings
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
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
db = client["extract_data_binance"]
collection = db["historical_data"]


# définition d'une fonction pour entraîner un modèle de régression linéaire
def train_linear_regression_model():
    warnings.filterwarnings("ignore")
    """
    - Entraîne un modèle de régression linéaire pour prédire le prix de clôture à partir des données stockées dans MongoDB.

    - Étude des variations journalière des données historiques entre le prix le plus haut et le prix le plus bas
    pour chaque jour afin de mesurer la volatilité du marché dans le but de prédire le prix à la fermeture de chaque bougie.

        - utilisation de méthode de régression linéaire de l'apprentissage supervisé

        - calcule de la variation entre le prix le plus haut et le plus bas pour chaque période de temps (chaque bougie dans notre cas)

        - utilisation de la variable 'close' comme valeur cible(étiquette) dans les données d'apprentissage supervisé

    - Définition des valeurs explicatives (caractéristiques)

        - Prix d'ouverture (open)

        - Prix le plus haut (high)

        - Prix le plus bas (low)

        - Prix auquel la paire de trading a été échangée à la fin de cette bougie (close )

        - Volume de transactions (volume)

    - Définition de la valeur cible (étiquette)

        - La valeur cible sera la variable 'close' indiquant le prix de fermeture

    Returns:
    - regressor (LinearRegression): Le modèle de régression linéaire entraîné.
    - train_r2 (float): Le coefficient de détermination R2 du modèle sur l'ensemble d'entraînement.
    - test_r2 (float): Le coefficient de détermination R2 du modèle sur l'ensemble de test.

    Cette fonction se connecte à une base de données MongoDB,
    récupère les données historiques de prix,
    calcule le taux de variation journalier,
    effectue le nettoyage des données,
    divise le jeu de données en ensembles d'entraînement et de test,
    remplit les valeurs manquantes,
    entraîne un modèle de régression linéaire,
    évalue sa performance sur les ensembles d'entraînement et de test,
    et affiche un nuage de points pour visualiser les prédictions du modèle.

    """
    # récupération des données dans un DataFrame
    df = pd.DataFrame(list(collection.find()))

    # calcul du taux de variation journalier entre le prix le plus haut et le prix le plus bas
    df["taux_variation"] = (df["high"] - df["low"]) / df["low"] * 100

    # suppression des colonnes non nécessaires au machine learning
    df = df.drop(["timestamp", "_id", "symbol"], axis=1)

    # séparation de la variable cible des variables explicatives
    feats = df.drop("close", axis=1)
    target = df["close"]

    # séparation du jeu d'entraînement et du jeu de test
    X_train, X_test, y_train, y_test = train_test_split(
        feats, target, test_size=0.20, random_state=42
    )

    # remplissage des valeurs manquantes dans les variables numériques
    num_imputer = SimpleImputer(missing_values=np.nan, strategy="median")
    X_train_imputed = pd.DataFrame(
        num_imputer.fit_transform(X_train), columns=X_train.columns
    )
    X_test_imputed = pd.DataFrame(num_imputer.transform(X_test), columns=X_test.columns)

    # initialisation du modèle de régression linéaire
    regressor = LinearRegression()

    # entraînement du modèle de régression linéaire
    regressor.fit(X_train_imputed, y_train)

    # évaluation de la performance du modèle
    train_r2 = regressor.score(X_train_imputed, y_train)
    test_r2 = regressor.score(X_test_imputed, y_test)

    # # affichage du coefficient de détermination R2 sur le jeu d'entraînement
    # print("Coefficient de détermination du modèle sur train:", train_r2)

    # # affichage du coefficient de détermination R2 sur le jeu de test
    # print("Coefficient de détermination du modèle sur test:", test_r2)

    # visualisation des prédictions
    fig = plt.figure(figsize=(10, 10))
    pred_test = regressor.predict(X_test_imputed)
    plt.scatter(pred_test, y_test, c="green")
    plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color="red")
    plt.xlabel("prediction")
    plt.ylabel("vraie valeur")
    plt.title("régression linéaire pour la prédiction du prix de clôture")
    plt.show()

    # retourne le modèle entraîné et ses performances
    return regressor, train_r2, test_r2


# exemple d'utilisation de la fonction
trained_model, train_r2, test_r2 = train_linear_regression_model()
