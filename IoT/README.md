# Internet des objets

IoT (*Internet of Things*) : [supports de cours en PDF](./5-eln-info%20IoT%20-%20G.%20Le%20Vaillant.pdf).

# Communication MQTT

## Introduction

- MQTT = *Message Queuing Telemetry Transport*
- Protocole de transmission de messages, basé sur TCP/IP
- Devenu un standard pour l'IoT et l'IIoT (*Industrial IoT*)

## Protocole *publish/subscribe*

![](https://www.hivemq.com/sb-assets/f/243938/1920x1080/d2bbcc60d9/mqtt-overview.webp)

Caractéristiques :
- léger
- sécurisé
- *scalable*

### Exemple : mesure de température

![](https://mqtt.org/assets/img/mqtt-publish-subscribe.png)



## Exercices

### Transmission de messages via broker externe

On va ici tester l'envoi et la réception de messages à travers un [broker public](https://www.hivemq.com/mqtt/public-mqtt-broker/).

- Depuis Docker Desktop, ou bien depuis un terminal, récupérer l'image Docker ```eclipse-mosquitto```. Elle pourra servir de broker aussi bien que de client MQTT.
- Dans un terminal, créer un conteneur appelé ```mqtt-client-1``` via la commande :  ```docker run -it --name mqtt-client-1 eclipse-mosquitto sh```. Cela permet d'exécuter immédiatement des commandes à l'intérieur du conteneur.
- Exécuter la commande ```mosquitto_sub -t brufor_PRENOM -h broker.hivemq.com -p 1883```, en remplaçant PRENOM par votre prénom (sans espace ni caractère spécial). Que signifient la commande ```sub``` et les arguments ```-t```, ```-h``` et ```-p``` ?
- Constater qu'il ne passe rien dans la console (c'est normal). Pourquoi ?
- Dans un terminal, créer un 2ème conteneur appelé ```mqtt-client-2```.
- Depuis ce conteneur, exécuter la commande ```mosquitto_pub -t brufor_PRENOM -h broker.hivemq.com -p 1883 -m 'Coucou !'```. Que signifient la commande ```pub```et l'argument ```-m``` ?
- Vérifier dans l'autre terminal ```mqtt-client-1``` la bonne réception du message.
- Créer un 3ème et un 4ème conteneur à partir de l'image ```eclipse-mosquitto```. Tester la publication (conteneur 3) et la souscription (conteneur 4) à votre topic. Vérifier la réception des messages dans tous les conteneurs actifs.


### Transmission de messages via broker externe - topic partagé

- Créer 2 conteneurs ```eclipse-mosquitto```. Dans le premier, souscrire au topic ```brufor_essentiel_reseau```. Dans le second, publier des messages sur ce même topic.
- Vérifier que les messages sont reçus par tous les stagiaires.

<!-- 
### Utilisation d'un broker local

TODO besoin de l'IP host dans Docker
- Depuis Docker Desktop, récupérer l'image du broker ```eclipse-mosquitto```. Lancer alors cette dans un conteneur avec le nom 'mqtt-broker' et en assignant le port 1883 de la machine au port 1883 du conteneur.
- À partir de 2 autres conteneurs basés sur ```emqx/mqttx-cli```, tester ce broker local. Son adresse sera ```TODO```.
-->

### Broker MQTT IoT : The Things Network

On va maintenant récupérer des informations via MQTT, depuis le broker ```eu1.cloud.thethings.network``` chez The Things Network (TTN). Une application IoT avec des noeuds LoRaWAN a déjà été créée. L'accès aux données est toutefois sécurisé :
- utilisateur : ```stm32-end-node-basic@ttn```
- mot de passe (mars 2024) : ```NNSXS.JZP7KEYXIXNSU7JANLTZ6UWZVMLNT3WRNMYGQBY.6HJXAMYSABCMK3DBT5GGXUKPLDJ46DLQGAVTMYPIXKG2VHGATRAQ```

Exercice : 
- Dans un conteneur mosquitto, souscrire à tous les topics grâce à l'argument ```-t '#'```. Si besoin, un exemple de commande mosquitto est disponible dans [la doc de TTN](https://www.thethingsindustries.com/docs/integrations/mqtt/#mqtt-clients).
- Analyser le contenu des *payloads* reçus.
- Refaire la souscription, en ajoutant l'option ```-d```. Quels sont les différents topics ? Quels sont les autres échanges entre le client et le broker ? 
- Tester ensuite la souscription à un seul noeud IoT en particulier (par exemple ```eui-0080e115000a930c```).

# Références

- IoT : références dans les slides
- MQTT : 
    - https://mqtt.org
    - https://www.hivemq.com/mqtt/