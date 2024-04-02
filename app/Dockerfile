# commande pour construire l'image Docker
# une que le fichier Dockerfile est créé, 
# on peut construire l'image Docker à partir de ce fichier en utilisant la commande suivante :
# sudo docker image build . -t image_api_binance_opa:1.0.0

# commandes de base pour la création d'une image Docker
FROM ubuntu:20.04

# définition de l'environnement non interactif 
# afin d'avoir les installations sans interaction de l'utilisateur 
# et les variables d'environnement par défaut pour les paquets apt 
ENV DEBIAN_FRONTEND=noninteractive

# mise à jour du cache des paquets apt et installation des packages nécessaires
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    mongodb \
    nodejs \
    npm \
    default-jdk \
    wget \
    tar \
    curl

# installation de Mongo Express version 1.0.0 
# pour accéder à la base de données MongoDB à partir d'une interface web
# version spécifiée de Mongo Express dans le registre npm (Node Package Manager)
# nous devons spécifier implicitement la version de Mongo Express à installer sinon cela génère une erreur
RUN npm install -g mongo-express@1.0.0

# téléchargement de Kafka version 3.7.0
RUN wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz

# utilisation de la commande tar pour extraire le contenu de l'archive Kafka
# utilisation de l'option -xzf pour extraire le contenu de l'archive Kafka
# dans le répertoire /opt pour l'installation et l'exécution de Kafka
# utilisation de l'option -C pour spécifier le répertoire de destination
RUN tar -xzf kafka_2.13-3.7.0.tgz -C /opt && \
    # utilisation de la commande mv pour renommer le répertoire kafka_2.13-3.7.0 en kafka
    # pour simplifier l'accès à Kafka
    # utilisation de la commande mv pour déplacer le répertoire kafka dans le répertoire /opt
    # pour l'installation et l'exécution de Kafka 
    mv /opt/kafka_* /opt/kafka

# installation de zookeeper
RUN apt-get install -y zookeeperd

# exposition du port 27017 pour intéragir avec Mongodb
EXPOSE 27017

# exposition du port 8081 pour accéder à Mongo Express 
# en utilisant un navigateur web en utilisant l'URL http://localhost:8081
EXPOSE 8081

# exposition du port 27017 pour de Kafka
EXPOSE 9092

# exposition du port 8080 pour accéder à Kafka UI
# en utilisant un navigateur web en utilisant l'URL http://localhost:8080
EXPOSE 8080

# exposition du port 2181 pour accéder à Zookeeper
EXPOSE 2181


# copie des fichiers de l'application dans le conteneur Docker 
COPY . /app

# changement du répertoire de travail à partir duquel les commandes CMD, RUN, et ENTRYPOINT sont exécutées 
WORKDIR /app

# installation des dépendances python à partir du fichier requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# commande par défaut pour démarrer Kafka
CMD ["/opt/kafka/bin/kafka-server-start.sh", "/opt/kafka/config/server.properties"]

# changement du répertoire de travail
WORKDIR /app/extract

# commande par défaut à exécuter lorsque le conteneur démarre
CMD [ "python3", "extract_history.py" ]
