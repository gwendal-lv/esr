# Docker networks

## Types de réseaux Docker

Docker permet de placer les conteneurs dans différents types de réseaux :

- ```bridge``` : **type de réseau par défaut**, réseau virtuel qui  permet aux conteneurs sur le même hôte de communiquer entre eux

![](img/network_bridge.png)

- ```host``` : permet à un conteneur de partager l'espace réseau de la machine physique

![](img/network_host.png)

- ```overlay``` : permet la communication entre des conteneurs sur différentes machines physiques au sein d'un cluster Docker Swarm

![](img/network_overlay.png)


- autres: ```ipvlan```, ```macvlan```


## Gestion des réseaux

Il existe plusieurs [sous-commandes pour docker network](https://docs.docker.com/reference/cli/docker/network/), notamment :
- ```docker network create``` et ```docker network rm```
- ```docker network connect``` et ```docker network disconnect```
- ```docker network ls```

Pour l'instant, on va travailler uniquement avec les réseaux créés automatiquement lorsque l'on utilise ```docker compose```.


# Networking et docker compose

Les réseaux créés automatiquement au démarrage de Docker sont les suivants :

```
gwendal@sshgw:~/network_demo $ sudo docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
ad59c66c982b   bridge    bridge    local
2dc0aa0d0db0   host      host      local
e08d8c51efdc   none      null      local
```

Maintenant, on va utiliser le fichier ```docker-compose.yml``` (dans le dossier courant) avec la commande ```docker compose up``` pour créer plusieurs conteneurs. Un réseau de type ```bridge```, nommé comme le dossier parent, est créé automatiquement par Docker.

```
gwendal@sshgw:~/network_demo $ sudo docker network ls
NETWORK ID     NAME                   DRIVER    SCOPE
ad59c66c982b   bridge                 bridge    local
2dc0aa0d0db0   host                   host      local
97e103b13568   network_demo_default   bridge    local
e08d8c51efdc   none                   null      local
```


# Exercice : NGinx reverse proxy et routage d'URLs

## Docker compose avec 3 conteneurs

1. Télécharger le dossier ```./network_demo``` et s'y déplacer dans le terminal.
2. Analyser le fichier docker compose (```cat docker-compose.yml```) : quel service est disponible sur quel port ?
3. Lancer les conteneurs (```docker compose up -d```), puis lister tous les conteneurs actifs (```docker ps```).
4. Vérifier dans le navigateur le fonctionnement des 3 conteneurs.
5. Ouvrir un terminal à l'intérieur du conteneur "network_demo-web_hello-1" (commande ```docker exec```).
6. Depuis l'intérieur du conteneur, utiliser la commande ```ping``` avec le nom des conteneurs pour vérifier qu'ils soient bien joignables (on ne connaît pas encore leur adresse IP). Noter alors les adresses IP de chaque conteneur.
7. Depuis Ubuntu, confirmer la cohérence des résultats à l'aide des commandes ```docker network ls```et ```docker network inspect <network-name>```.

## Analyse et modification du réseau docker

1. Depuis l'intérieur du conteneur "network_demo-web_hello-1", essayer de ```ping``` les noms d'hôtes définis dans le docker-compose.yml au lieu des noms de conteneurs.
2. Analyser le fichier ```nginx.conf```. Comment accéder aux serveurs web via URL, sur le port 8080 ? (Et pas 8081 ni 8082)
3. Dans ```docker-compose.yml```, supprimer l'accès direct aux serveurs web via un port local (accès seulement via reverse-proxy NGinx).
4. Modifier ```docker-compose.yml``` pour que Nginx soit accessible sur le port 80. Constater que toutes les URLs sont également accessibles depuis les autres machines physiques du réseau local.


# Références
- https://docs.docker.com/network/
- https://docs.docker.com/compose/networking/

