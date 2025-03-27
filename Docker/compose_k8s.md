# Docker Compose

## Présentation

Moteur de lancement d'un ensemble de conteneurs dépendant les uns des autres (application multi-conteneurs). Par exemple, application web (Python) via un serveur web (Nginx, Gunicorn, ...), avec serveur de bases de données (MySQL, ...) :

![](img/compose.jpeg)

## Exercice

1. Télécharger tout le code du repository https://github.com/docker/awesome-compose/ (Code -> Download ZIP)
2. Extraire le code. Ouvrir un terminal, puis se déplacer (commande ```cd```) vers le dossier extrait.
3. Dans le terminal, se déplacer vers le sous-dossier ```nginx-nodejs-redis```, puis afficher le contenu de ce dossier.
4. Taper la commande ```docker compose up```.
5. Ouvrir http://localhost dans le navigateur, et la rafraîchir plusieurs fois. Constater que la réponse vient parfois du serveur ```web1```, et parfois du serveur ```web2```, même si ces 2 serveurs partagent la même base de données Redis.
6. À l'aide de la commande ```docker ps```, analyser les conteneurs créés par Docker Compose. Comment obtenir une page web servie par ```web1``` ou ```web2``` spécifiquement ?
7. Ouvrir le fichier ```compose.yaml``` et essayer d'en comprendre le contenu.

## Docker Engine + Docker Compose : limitations

Avantages :
- (très) facile à utiliser

Inconvénients : 
- 1 seule machine physique (pas de mise à l'échelle)



# Orchestration via Kubernetes


## Présentation générale

![](img/Kubernetes-vs-Docker.jpg)

Solution similaire : Docker Swarm (plus simple, moins configurable)


## Orchestration en Cluster

### Master et Nodes (Workers)

![](img/K8s_arch.png)

- Master = machine physique qui gère les Nodes
    - redondance possible du master
- Worker = Node = machine physique dans le réseau
- Cluster = ensemble des Masters et Nodes

### Pods

![](img/K8s_node.png)

- Pod = ensemble de conteneurs
    - les conteneurs d'un Pod partagent des ressources (volumes, ports localhost)
    - chaque Pod a sa propre adresse IP, accessible aux autres Pods du cluster

### Applications en pratique 

- déploiement automatique de conteneurs Docker sur plusieurs machines
- *auto-scaling* (*load balancing*)
- difficile à prendre en main

# Références

https://www.atlassian.com/microservices/microservices-architecture/kubernetes-vs-docker

https://kubernetes.io/docs/concepts/architecture/

https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/
