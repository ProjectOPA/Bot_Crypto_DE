# Bot_Crypto_DE
Crypto bot pour projet de Data Engineer

- git clone https://github.com/ProjectOPA/Bot_Crypto_DE.git

- cd app

- python3 -m venv .venv

- source .venv/bin/activate python3.10.12

- pip install -r requirements.txt

## Approche d'une programmation fonctionnelle
### Architecture logiciel ETL
1. step1_extract : Extraction des données
- Cette étape consiste à extraire les données brutes à partir  l'API Binance 
    - extraction des données historiques
    - extraction des données de streamings
    - stockage des données historiques dans le dossier .data
    - stockage des données de streamings dans le dossier 

2. step2_transform : Transformation (pré-processing)
- Une fois les données extraites, cette étape consiste à transformer les données extraites (gestion des valeurs manquantes, création de nouvelles colonnes, normalisation..)pour l'analyse et le traitement par le modèle de Machine Learning. 
    - transformation des données historiques stockées
    - transformation des données de streamings 

3. step3_dataviz : Visualisation des données
    - visualisation des données pour mieux comprendre la structure des données, les relations entre les variables, etc. 

4. step4_modeling : Machine Learning (Apprentissage automatique) 
    - construction du modèle (séparation de la variable cible des variables explicatives, séparation du jeu d'entraînement et du jeu de test)
    - entrainement du modèle
    - évaluation du modèle
    - test du modèle sur les données de streaming

5. step5_load : Load (Chargement des résultats du modèle dans une bd)
    - sauvegarde des prédictions

#### s'assurez-vous que le service Docker est en cours d'exécution sur votre système. Vous pouvez démarrer le service Docker en utilisant la commande suivante :
pip install --upgrade docker-compose

#### si problème d'installation de docker-compose.  Cette commande force l'installation de la dernière version disponible de docker-compose, même si une version antérieure est déjà installée
sudo service docker start

## ouvrir un terminal et exécuter le docker-compose
sudo docker-compose up -d

<!-- ## accès au terminal ubuntu
docker exec -it ubuntu-project-api-binance bash


## éteindre docker-compose
sudo docker-compose down

