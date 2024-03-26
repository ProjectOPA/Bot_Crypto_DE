from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import json

#Configuration de Kafka
kafka_conf = {
    'bootstrap.servers': 'localhost:9092',  # Adresse du broker Kafka
    'group.id': 'consumer',
    'auto.offset.reset': 'earliest'  # Commencer à lire les messages depuis le début du topic
}

#Configuration MongoDB
mongo_conf = {
    'host': 'localhost',  # Adresse de l'hôte MongoDB
    'port': 27017,  # Port MongoDB
    'database': 'OPA',  # Nom de la base de données MongoDB
    'collection': 'BTCUSDT'  # Nom de la collection MongoDB
}

# Création du consommateur Kafka
consumer = Consumer(kafka_conf)

# Connexion à la base de données MongoDB
client = MongoClient(mongo_conf['host'], mongo_conf['port'])
db = client[mongo_conf['database']]
collection = db[mongo_conf['collection']]

# Abonnement au topic BTCUSDT_topic
consumer.subscribe(['BTCUSDT_topic'])

# Boucle de consommation des messages
try:
    while True:
        msg = consumer.poll(timeout=30.0)  # Récupération du message du topic Kafka chaque 30 secondes
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
            data = json.loads(msg.value().decode('utf-8')) 
            collection.insert_one(data)
            print("Message inséré dans MongoDB:", data)

finally:
    consumer.close()