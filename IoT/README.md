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

On va ici tester l'envoi et la réception de messages à travers un [broker public](https://www.hivemq.com/mqtt/public-mqtt-broker/) : `broker.hivemq.com`.
Si ce broker est surchargé (indisponible ou lent à répondre), utiliser le broker interne IRISIB sur `172.30.2.204`.

- Ouvrir un nouveau terminal. À l'aide de la commande ```mosquitto_sub```, faire la souscription au topic `brufor_PRENOM` en remplaçant PRENOM par votre prénom (sans espace ni caractère spécial). 
- Constater qu'il ne passe rien dans la console (c'est normal). Pourquoi ?
- Dans un second terminal, utiliser la commande `mosquitto_pub` pour envoyer le message `Coucou !` au premier terminal. Vérifier la bonne réception du message.
- Créer un 3ème et un 4ème terminal à partir de l'image ```eclipse-mosquitto```. Tester la publication (terminal 3) et la souscription (terminal 4) à votre topic. Vérifier la réception des messages dans tous les conteneurs actifs.


### Transmission de messages via broker externe - topic partagé

- Ouvrir deux onglets de terminal. Dans le premier, souscrire au topic ```brufor_essentiel_reseau```. Dans le second, publier des messages sur ce même topic.
- Vérifier que les messages sont reçus par tous les stagiaires.

### Broker MQTT IoT : The Things Network

On va maintenant récupérer des informations via MQTT, depuis le broker ```eu1.cloud.thethings.network``` chez The Things Network (TTN). Une application IoT avec des noeuds LoRaWAN a déjà été créée. L'accès aux données est toutefois sécurisé :
- utilisateur : ```stm32-end-node-basic@ttn```
- mot de passe (avril 2025) : ```NNSXS.JZP7KEYXIXNSU7JANLTZ6UWZVMLNT3WRNMYGQBY.6HJXAMYSABCMK3DBT5GGXUKPLDJ46DLQGAVTMYPIXKG2VHGATRAQ```

Exercice : 

- Dans un conteneur mosquitto, souscrire à tous les topics grâce à l'argument ```-t '#'```. Si besoin, un exemple de commande mosquitto est disponible dans [la doc de TTN](https://www.thethingsindustries.com/docs/integrations/mqtt/#mqtt-clients).
- Analyser le contenu des *payloads* reçus.
- Refaire la souscription, en ajoutant l'option ```-d```. Quels sont les différents topics ? Quels sont les autres échanges entre le client et le broker ? 
- Tester ensuite la souscription à un seul noeud IoT en particulier (par exemple ```eui-0080e115000a930c```).
- On va maintenant utiliser l'utilitaire ```jq``` pour afficher proprement du JSON puis extraire seulement certaines informations des messages reçus. 
    - Ajouter la commande ```| jq '.'``` à la fin de la ligne exécutant la commande ```mosquitto_sub```, et rappeler à quoi sert le *pipe* (```|```). Constater que le formatage JSON est bien meilleur.
    - Pour extraire des champs correspondants aux clés CLE1 puis CLE2 d'une chaîne JSON, la syntaxe de base est ```| jq '.CLE1.CLE2'```. Utiliser ```jq``` pour d'extraire uniquement *decoded_payload*, ou bien uniquement la température, etc. 
- À quoi sert l'option ```-c``` de ```jq``` ? 

# Références

- IoT : références dans les slides
- MQTT : 
    - https://mqtt.org
    - https://www.hivemq.com/mqtt/
- [JSON: JavaScript Object Notation](https://fr.wikipedia.org/wiki/JavaScript_Object_Notation)
- https://jqlang.org/

