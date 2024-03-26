from kafka import KafkaProducer
from confluent_kafka import Producer
import pandas as pd
import asyncio
from binance.client import AsyncClient
from binance import BinanceSocketManager
from binance.enums import *
import json

kafka_conf = {'bootstrap.servers': 'localhost:9092'}

#Création de notre producer
producer = Producer(kafka_conf)

async def main():
    #api_key = 'mVJMDUgghiBBlgQTW73iB5PQJMtU32qny0eFWRnEAfh5VSsa4lgDXWSZhujuQXZ6'
    #api_secret = 'rHMU91gAKVQvD34HMKFm1HxKUbWjnhwWI7qKtPTqH5JmkgcrNaNgyVUVt1N9HLok'
    api_secret = '<api_secret>'
    api_key = '<api_key>'


    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    
    # Création du socket d'écoute sur les klines du BTCUSDT
    ks = bm.kline_socket('BTCUSDT', interval=KLINE_INTERVAL_5MINUTE)
    
    # Réception permanente du message
    async with ks as tscm:
        while True:
            res = await tscm.recv()
            
            # S'assure que la donnée reçu correspond bien à celle de la fermeture de la k_line afin de respecter les 5MIN d'interval
            if res['k']['x']:
                # Envoi des données au topic Kafka
                producer.produce('BTCUSDT_topic', json.dumps(res))
                producer.poll(0)  # Appel poll pour s'assurer que le message est envoyé
                
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
        producer.flush()  # Attendre que tous les messages soient envoyés
        producer.close()  # Fermer le producer