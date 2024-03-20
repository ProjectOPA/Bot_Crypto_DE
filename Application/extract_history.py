# importation des librairies nécessaires
# requests de python pour effectuer des requêtes HTTP
import requests

# MongoClient pour interagir avec MongoDB
from pymongo import MongoClient

# datetime pour manipuler des objets datetime
from datetime import datetime


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

# # clés d'API Binance(les secrets sont créées sur GitHub, il faudra les mettre dans le fichier YAML du workflow)
# api_key = "<api_key>"
# api_secret = "<api_secret>"

# URL de l'API Binance pour les données historiques klines (candles)
api_url = "https://api.binance.com/api/v3/klines"

# Dans le contexte du trading financier,
# une bougie (candlestick ou candle en anglais)
# est une représentation graphique d'une unité de temps spécifique
# (comme une minute, une heure, un jour, etc.)
# des mouvements de prix d'un actif financier,
# tel qu'une paire de devises,
# une action ou une crypto-monnaie.


# définition d'une fonction
# pour obtenir des données historiques depuis l'API Binance
def get_binance_data(symbol, interval):
    params = {"symbol": symbol, "interval": interval}

    response = requests.get(api_url, params=params)
    data = response.json()

    return data


# définition d'une fonction
# pour stocker les données dans MongoDB
def store_in_mongodb(data, symbol):
    # création d'une boucle pour parcourir chaque bougie (candle)
    # dans les données récupérées de l'API Binance
    for candle in data:
        # convertion du timestamp de la bougie en objet datetime UTC
        # et convertion du timestamp de la bougie de millisecondes en secondes "candle[0] / 1000.0"
        # UTC est un standard de temps universel, et cela évite les confusions liées aux différents fuseaux horaires.
        timestamp = datetime.utcfromtimestamp(candle[0] / 1000.0)
        # extraction et convertion des string en float pour le traitement des données de prix et de volume de la bougie
        open_price = float(candle[1])
        high_price = float(candle[2])
        low_price = float(candle[3])
        close_price = float(candle[4])
        volume = float(candle[5])

        # création d'un dictionnaire 'candle_data'
        # dans la database représentant les données de la bougie
        candle_data = {
            "symbol": symbol,  # symbole associé à la bougie
            "timestamp": timestamp,  # moment de la bougie
            "open": open_price,  # prix d'ouverture de la bougie
            "high": high_price,  # prix le plus haut de la bougie
            "low": low_price,  # prix le plus bas de la bougie
            "close": close_price,  # prix de clôture de la bougie
            "volume": volume,  # volume de la bougie
        }

        # insertion des données de la bougie dans la collection MongoDB spécifiée
        collection.insert_one(candle_data)


# point d'entrée du script 'if __name__ == "__main__"': :
# cette ligne vérifie si le script est exécuté directement
# (pas importé comme module dans un autre script).
# Cela permet d'assurer que le bloc de code ci-dessous
# est exécuté uniquement lorsque le script est exécuté en tant que programme principal.
if __name__ == "__main__":
    # choix des crypto-monnaies
    # création d'une liste pour lesquels on récupére les données historiques
    # des transactions (trades) pour la paire "BTCUSDT"
    symbols = ["BTCUSDT"]
    # choix de l'intervalle (1m, 1h, 1d, etc.)
    interval = "1s"

    while True:
        for symbol in symbols:
            # appel de la fonction get_binance_data
            # pour obtenir les données historiques pour le symbole et l'intervalle spécifiés.
            historical_data = get_binance_data(symbol, interval)
            # appel la fonction store_in_mongodb
            # pour stocker les données historiques dans MongoDB pour le symbole actuel.
            store_in_mongodb(historical_data, symbol)

# faire CTRL+C pour arreter la boucle
