# importation des librairies nécessaires
# requests de python pour effectuer des requêtes HTTP
import requests


# URL de l'API Binance pour les données historiques klines (candles)
api_url = "https://api.binance.com/api/v3/klines"

# choix des crypto-monnaies
# création d'une liste pour lesquels on récupére les données historiques
# des transactions (trades) pour la paire "BTCUSDT"
symbols = ["BTCUSDT"]
# choix de l'intervalle (1m, 1h, 1d, etc.)
interval = "2h"


# définition d'une fonction
# pour obtenir des données historiques depuis l'API Binance
def get_binance_data(symbol, interval, start_date, end_date):
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_date,
        "endTime": end_date,
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    return data


# Dans le contexte du trading financier,
# une bougie (candlestick ou candle en anglais)
# est une représentation graphique d'une unité de temps spécifique
# (comme une minute, une heure, un jour, etc.)
# des mouvements de prix d'un actif financier,
# tel qu'une paire de devises,
# une action ou une crypto-monnaie.


# point d'entrée du script
if __name__ == "__main__":
    # Appel à la fonction pour collecter les données historiques
    get_binance_data()


# faire CTRL+C pour arreter la boucle
# ou dans un autre terminal sudo docker-compose down

# je vais mettre en place un cronjob pour lancer le script en arrière-plan
# pour récupérer les données de la journée précédente
# et les stocker dans MongoDB
# pour les symboles et l'intervalle spécifiés.
# configuration du cronjob dans le fichier crontab
# crontab - e
# ajout de la ligne suivante pour exécuter le script toutes les secondes
# execution de la commande toutes les secondes
# python3 Application/extract_history.py
