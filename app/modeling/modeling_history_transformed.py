# 4. step4_modeling : Machine Learning (Apprentissage automatique)
#     - construction du modèle (séparation de la variable cible des variables explicatives, séparation du jeu d'entraînement et du jeu de test)
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
    récupère les données historiques transformées,
    entraîne un modèle de régression linéaire,
    évalue sa performance sur les ensembles d'entraînement et de test,
    et affiche un nuage de points pour visualiser les prédictions du modèle.

    """
    # récupération des données dans un DataFrame
    df = pd.DataFrame(list(collection_history_transformed.find()))

    # affichage des 5 premières lignes du DataFrame
    print(df.head())

    # séparation de la variable cible des variables explicatives
    # il est nécessaire de supprimer la colonne "_id" qui est un objet de type ObjectId de MongoDB
    # pour éviter une erreur lors de l'entraînement du modèle
    feats = df.drop(["close", "_id"], axis=1)
    target = df["close"]

    # séparation du jeu d'entraînement et du jeu de test
    X_train, X_test, y_train, y_test = train_test_split(
        feats, target, test_size=0.20, random_state=42
    )

    # initialisation du modèle de régression linéaire
    regressor = LinearRegression()

    # entrainement du modèle de régression linéaire
    regressor.fit(X_train, y_train)

    # évaluation de la performance du modèle
    train_r2 = regressor.score(X_train, y_train)
    test_r2 = regressor.score(X_test, y_test)

    # affichage du coefficient de détermination R2 sur le jeu d'entraînement
    print("Coefficient de détermination du modèle sur train:", train_r2)

    # affichage du coefficient de détermination R2 sur le jeu de test
    print("Coefficient de détermination du modèle sur test:", test_r2)

    # création d'une figure pour afficher le nuage de points
    fig = plt.figure(figsize=(10, 10))

    # instanciation de l'objet LinearRegression, apprentissage et prédiction
    pred_test = regressor.predict(X_test)

    # création d'un nuage de points pour afficher les prédictions
    plt.scatter(pred_test, y_test, c="green")

    # affichage de la droite d'équation y = x par dessus le nuage de points
    plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color="red")

    # ajout de titre et de labels
    plt.xlabel("prediction")
    plt.ylabel("vraie valeur")
    plt.title("régression linéaire pour la prédiction du prix de clôture")

    # affichage du graphique
    plt.show()

    # retourne le modèle entraîné
    return regressor


train_linear_regression_model()
