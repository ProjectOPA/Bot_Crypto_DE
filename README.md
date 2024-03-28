# Bot_Crypto_DE
Crypto bot pour projet de Data Engineer

- git clone https://github.com/ProjectOPA/Bot_Crypto_DE.git

- cd app

- python3 -m venv .venv

- source .venv/bin/activate

- pip install -r requirements.txt

## Approche d'une programmation fonctionnelle
### Architecture logiciel ETL
1. Extract
    - extraction des données historiques
    - extraction des données de streamings
    - stockage des données historiques dans le dossier data
    - stockage des données de streamings dans le dossier data

2. Transform (pré-processing)
    - transformation des données historiques stockées
    - transformation des données de streamings stockées

3. Load
    - chargement des données historiques transformées
    - chargement des données de streamings transformées

4. Model 
    - entrainement et prédiction sur les données historiques transformées
    - entrainement et prédiction sur les données de streamings transformées

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

