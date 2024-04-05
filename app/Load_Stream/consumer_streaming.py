# step5_load : Load (Chargement des résultats du modèle dans une bd)
#     - sauvegarde des prédictions

from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import json
import time
from datetime import datetime


# Configuration de Kafka
kafka_conf = {
    "bootstrap.servers": "app-kafka-1:9092",  # Adresse du broker Kafka
    "group.id": "consumer",
    "auto.offset.reset": "earliest",  # Commencer à lire les messages depuis le début du topic
}

# Configuration MongoDB
mongo_conf = {
    "user": "admin",
    "password": "pass",
    "host": "mongo-project-api-binance",  # Adresse de l'hôte MongoDB
    "port": 27017,  # Port MongoDB
    "database": "streaming_data",  # Nom de la base de données MongoDB
    "collection": "streaming_data_predict",  # Nom de la collection MongoDB
}

# Attendre un moment pour que les données soient disponible dans le topic kafka
time.sleep(60*18)

# Création du consommateur Kafka
consumer = Consumer(kafka_conf)

# URI de connection à Mongo DB
uri = f"mongodb://{mongo_conf['user']}:{mongo_conf['password']}@{mongo_conf['host']}:{mongo_conf['port']}/"

# Connexion à la base de données MongoDB
client = MongoClient(uri)
db = client[mongo_conf["database"]]
collection = db[mongo_conf["collection"]]

# création de l'index TTL de 24 heures (en secondes), nous indiquons à MongoDB de
# supprimer automatiquement les documents de la collection
# après 24 heures à compter de la valeur du champ timestamp.
collection.create_index("timestamp", expireAfterSeconds=86400)

# Abonnement au topic BTCUSDT_topic
consumer.subscribe(["BTCUSDT_topic"])

# Boucle de consommation des messages
try:
    while True:
        msg = consumer.poll(
            timeout=30.0
        )  # Récupération du message du topic Kafka chaque 30 secondes
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Fin de la partition, aucun message supplémentaire à lire
                continue
            else:
                # Erreur inattendue
                print(msg.error())
                break
        else:
            # Insertion du message dans la base de données MongoDB
            data = json.loads(msg.value().decode("utf-8"))
            timestamp_str = data["timestamp"]
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            data["timestamp"] = timestamp
            collection.insert_one(data)

            print("Message inséré dans MongoDB:", data)

finally:
    consumer.close()
