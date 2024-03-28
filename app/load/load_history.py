# import de la fonction d'extract_history.py
from app.extract.extract_history import get_binance_data

# importation des symboles et de l'intervalle
from app.extract.extract_history import symbols, interval

# MongoClient pour interagir avec MongoDB
from pymongo import MongoClient

# datetime pour manipuler des objets datetime
from datetime import datetime, timedelta

# importation de la librairie time pour mettre en pause le script
# pendant un court instant pour ne pas saturer le serveur de l'API Binance
import time


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

        candle_data = {
            # symbol: c'est le symbole de la paire de trading pour laquelle les données sont collectées
            # "BTCUSDT" indique que les données sont pour la paire de trading Bitcoin (BTC)
            # par rapport à l'US Dollar Tether (USDT)
            "symbol": symbol,
            # timestamp: c'est le moment précis de la bougie (candle) représentée par cette ligne
            # il est donné en heure universelle coordonnée (UTC) sous forme de chaîne de caractères formatée
            "timestamp": timestamp,
            # open:c'est le prix d'ouverture de la bougie,
            # c'est-à-dire le prix auquel la paire de trading a commencé à être échangée à ce moment précis
            "open": open_price,
            # high: c'est le prix le plus élevé atteint pendant cette bougie
            "high": high_price,
            # low: c'est le prix le plus bas atteint pendant cette bougie
            "low": low_price,
            # close: c'est le prix de clôture de la bougie,
            # c'est-à-dire le prix auquel la paire de trading a été échangée à la fin de cette bougie
            "close": close_price,
            # volume: c'est le volume de trading qui indique la quantité totale d'actifs échangés pendant cette bougie.
            "volume": volume,
        }
        collection.insert_one(candle_data)


# définition de la fonction pour récupérer les données historiques
def collect_historical_data():
    # détermination de la date d'aujourd'hui
    end_date = datetime.now()

    # calcul de la date il y a 4 ans
    start_date = end_date - timedelta(days=365 * 4)

    # utilisation d'une boucle pour récupérer les données pour chaque jour sur une période de 4 ans
    while start_date <= end_date:
        for symbol in symbols:
            # appel de la fonction get_binance_data pour obtenir les données historiques pour chaque jour
            historical_data = get_binance_data(
                symbol,
                interval,
                int(start_date.timestamp() * 1000),
                int((start_date + timedelta(days=1)).timestamp() * 1000),
            )
            # stockage des données dans MongoDB
            store_in_mongodb(historical_data, symbol)

        # incrémentation pour passage au jour suivant
        start_date += timedelta(days=1)

        # attente d'une seconde entre chaque jour pour éviter de surcharger l'API Binance
        # nous évitons de faire trop de requêtes à l'API en même temps pour ne pas être bloqué
        # et avoir une erreur au niveau du serveur de l'API
        # mise en pause de 1 seconde entre chaque jour
        time.sleep(1)


# point d'entrée du script
if __name__ == "__main__":
    # Appel à la fonction pour collecter les données historiques
    collect_historical_data()
