
# Docker desktop

## Présentation

- Docker Desktop : à installer sur votre machine
    - Les conteneurs fonctionneront dans une VM linux, créée automatiquement sur votre machine locale lorsque Docker Desktop démarre
    - Gestion graphique des conteneurs et images
    - Gestion également possible par CLI (*Command Line Interface*)
- Docker Hub https://hub.docker.com : bibliothèques d'images prêtes à l'emploi
    - Accessible depuis Docker Desktop lui-même

![](img/desktop_hub.png)

## Installation sur Ubuntu 

Instructions disponibles sur : https://docs.docker.com/desktop/install/ubuntu/



# Exercices

## Multiples serveurs et apps web (via Docker Desktop)

1. Chercher l'image nginx officielle, puis la récupérer localement (*Pull*).

![](img/nginx_pull.png)

2. Créer un conteneur appelé ```nginx_web_server_1```, basé sur l'image nginx, et qui assigne le port local 8080 au port 80 à l'intérieur du conteneur. Quelle est la différence entre l'image (de Docker Hub) et le conteneur que l'on vient de créer ?

![](img/desktop_image_run.png)

3. Vérifier le résultat dans votre navigateur à l'adresse http://localhost:8080. 

4. Lorsque l'on accède à http://localhost:8080, nginx sert automatiquement un fichier ```index.html``` situé dans le dossier ```/usr/share/nginx/html``` du conteneur. Retrouver ce dossier en explorant le conteneur depuis Docker Desktop.

5. Créer un second conteneur nommé ```nginx_web_server_2```, accessible cette fois depuis le port local 8081. Constater qu'on a bien deux conteneurs basés sur la même image.

![](img/nginx_two_containers.png)

6. Arrêter un des deux conteneurs, puis vérifier dans votre navigateur que le port correspondant ne répond plus (soit ```localhost:8080```, soit ```localhost:8081```). Ensuite, redémarrer ce conteneur.

7. Récupérer l'image ```docker/welcome-to-docker```, puis la lancer dans un conteneur nommé ```welcome_web_server```. Le port local 8082 sera assigné au port 80 du conteneur. Tester ce 3ème conteneur dans votre navigateur.

8. Récupérer l'image ```gwendallv/python-flask-demo```, puis la lancer dans un conteneur nommé ```python_flask_web_demo```. Le port local 8083 sera assigné au port 5000 du conteneur. Tester ce 4ème conteneur dans votre navigateur.


## Multiples serveurs et apps web (via ligne de commande)

Refaire l'exercice précédent, mais en utilisant uniquement la ligne de commande. Quelques remarques :
- avec Ubuntu, les conteneurs créés par Docker Desktop (dans une VM) sont isolés des conteneurs Docker Engine créés via CLI
- utiliser le préfixe ```sudo``` pour gérer les conteneurs par CLI




# Références

https://docs.docker.com/guides/walkthroughs/run-hub-images/