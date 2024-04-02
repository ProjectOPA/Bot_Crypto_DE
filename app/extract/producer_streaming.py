# 1. step1_extract : Extraction des données
# - Cette étape consiste à extraire les données brutes à partir l'API Binance
#     - extraction des données de streamings

from confluent_kafka import Producer
import sys
import os
import pandas as pd
import asyncio
from binance.client import AsyncClient
from binance import BinanceSocketManager
from binance.enums import *
import json

# Ajout du dossier app/ pour que python puisse lire les paquets
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(script_dir, ".."))

# Import du modèle
from modeling.modeling_history_transformed import train_linear_regression_model

# Instanciation du modèle de regression entraînée
regressor = train_linear_regression_model()

kafka_conf = {"bootstrap.servers": "localhost:9092"}

# Création de notre producer
producer = Producer(kafka_conf)


async def main():

    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)

    # Création du socket d'écoute sur les klines du BTCUSDT
    ks = bm.kline_socket("BTCUSDT", interval=KLINE_INTERVAL_5MINUTE)

    # Réception permanente du message
    async with ks as tscm:
        while True:
            res = await tscm.recv()

            # S'assure que la donnée reçu correspond bien à celle de la fermeture de la k_line afin de respecter les 5MIN d'interval
            if res["k"]["x"]:

                # Envoi des données au topic Kafka
                producer.produce("BTCUSDT_topic", json.dumps(res))
                producer.poll(0)  # Appel poll pour s'assurer que le message est envoyé

                # utilisation du modèle de regression pour prédire le prix de clôture
                # et affichage des données
                res["k"]["x"] = False
                res["k"]["c"] = regressor.predict(pd.DataFrame([res["k"]]))[0]

                # Affichage des données pour vérification
                print(res)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()  # Attendre que les messages soient envoyés
        producer.close()
