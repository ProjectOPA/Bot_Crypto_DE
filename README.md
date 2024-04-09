# Bot_Crypto_DE
Crypto bot pour projet de Data Engineer

## Introduction
Ce Bot de cryptomonnaie permet d'obtenir certaines informations ainsi que des conseils d'investissement sur les paires de cryptomonnaie. Dans sa version actuelle, l'ensemble de ces fonctionnalités s'articulent principalement autour de la paire Bitcoin - US Dollar (BTCUSDT). Il se base sur les données extraites de l'API de Binance (https://www.binance.com/fr/binance-api) et intègre un modèle de machine learning afin de réaliser des prédictions sur la baise ou la hausse de la valeur de ladite paire. D'autres fonctionnalités sont également disponible depuis l'API mise à disposition pour interagir avec notre Bot.

## Pré-requis
Ce bot utilise Docker pour le déploiement de ces services. Afin d'assurer son bon fonctionnement, il est indispensable de s'assurer de l'installation au préalable de Docker et de Docker compose.

Consultez la documentation de Docker (https://docs.docker.com/get-docker/) pour installer Docker et Docker-compose si besoin.

Afin de s'assurer qu'ils sont bien installés, exécutez les commandes suivantes:
- docker --version
- docker-compose --version

Sur certains systèmes, l'installation de Docker requiert celle de Docker Desktop (https://docs.docker.com/engine/install/).

## Installation et lancement
Pour lancer le Bot de crypto, effectuer chronologiquement les actions suivantes:

- git clone https://github.com/ProjectOPA/Bot_Crypto_DE.git

- cd app

- ./conf.sh

Suite à ce lancement, des containers se lancent:

- **Container mongo-project-api-binance** : Base de données Mongo permettant le stockage des données utilisées par le bot
- **Container mongo-express-api-binance** : Interface graphique permettant d'interagir avec notre base de données
- **Container app-kafka-1** : Permettant de traiter les données de streaming
- **Container kafkaui** : Interface graphique de Kafka permettant d'interagir avec kafka
- **Container zookeeper** : Service essentiel pour le bon fonctionnement de Kafka
- **Container historic_handler** : Service permettant la création, le stockage et la transformation des données historiques
- **Container stream_producer** : Service permettant de récupérer les données de streaming, d'appliquer le modèle de prédiction et de stocker les données dans un topic kafka
- **Container stream_loader** : Service permettant l'acheminement des données de kafka vers MongoDB
- **Container opa_api** : API permettant d'interagir avec notre Bot

## Utilisation
Une fois les services lancés, vous pouvez accéder sur votre navigateur au service suivant:

- MongoDB : http://localhost:8081
- Kafka : http://localhost:8080
- API documentation : http://localhost:8000/docs

Veuillez noter que pour des raisons évidentes de collection de données suffisantes pour entraîner le modèle, toutes les fonctionnalités de notre application de sont disponibles qu'au bout de 15 min après son lancement. Vous pourrez toutefois voir les services et y accéder pendant cette phase d'initialisation.

## Exemples
En guise d'exemple, nous allons montrer quelques requêtes effectuables sur notre API

### Récupérer des données historiques sur la paire BTCUSDT

curl -X 'GET' \
  'http://localhost:8000/historical?start_date=2023-11-08&end_date=2023-11-09' \
  -H 'accept: application/json'

### Récupérer des données de streaming sur la paire BTCUSDT

curl -X 'GET' \
  'http://localhost:8000/predict?start_date=2024-04-06&end_date=2024-04-12' \
  -H 'accept: application/json'

### Avoir un conseil d'investissement sur la paire BTCUSDT en temps réel

curl -X 'GET' \
  'http://localhost:8000/invest' \
  -H 'accept: application/json'

Il s'agit d'exemples. Pour voir l'ensemble des fonctionnalités déployées, consultez la documentations de notre API.

## Arrêt de l'app
Dans le repertoire où le conf.sh à été exécuté, lancer :
- docker-compose down

## Auteurs
- Elvis AKOTEGNON
- Khaty GUYET
- Tristan KALI

