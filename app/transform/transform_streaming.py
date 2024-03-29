from pymongo import MongoClient
from sklearn.impute import SimpleImputer
from app.transform.transform_history import train_linear_regression_model

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
collection = db["producer_data"]


# utilisation du modèle entraîné pour prédire le valeur cible 'close' sur des données de streaming
def predict_close(streaming_data, model):
    """
    Prédit les prix de clôture à partir des données de streaming en utilisant
    le modèle de régression linéaire entraîné.

    Args:
    - streaming_data (DataFrame): Les données de streaming à utiliser pour la prédiction.
    - model (LinearRegression): Le modèle de régression linéaire entraîné.

    Returns:
    - predictions (array): Les prédictions des prix de clôture.
    """
    # prétrai des données de streaming
    feats_streaming = streaming_data.drop(["timestamp", "_id", "symbol"], axis=1)

    num_imputer = SimpleImputer(missing_values=np.nan, strategy="median")

    feats_streaming_clean = pd.DataFrame(
        num_imputer.fit_transform(feats_streaming), columns=feats_streaming.columns
    )

    # prédiction des prix de clôture
    predictions = model.predict(feats_streaming_clean)

    # retourne les prédictions
    return predictions


# utilisation du modèle entraîné pour prédire les valeurs sur des données de streaming

# instanciation du modèle entraîné sur les données historiques
trained_model = train_linear_regression_model()

# instanciation des données de streaming
streaming_data = pd.DataFrame(list(collection.find()))

# utilisation du modèle entraîné pour prédire les prix de clôture
predictions = predict_close(streaming_data, trained_model)
