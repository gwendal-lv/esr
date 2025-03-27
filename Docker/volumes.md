


# Volumes

## Persistence des données

![](img/image_readonly.png)

## Volume Docker

Pour permettre la persistence des données, mais aussi pour donner accès des données situées à l'extérieur du conteneur, on peut utiliser des Docker Volumes.

![](img/types-of-mounts.png)

Exemple : base de données (sur la machine hôte) séparée du serveur de base de données (dans le container)

![](img/volume_mount.png)



# Exercices

## Serveur web nginx : site web personnalisé

1. Télécharger un canevas de site web statique depuis https://html5up.net
2. Renommer le dossier en tant que ```mon_super_site_web```, puis le placer dans votre dossier utilisateur (```/home/NOM_UTILISATEUR```).
3. Depuis Docker Desktop: lancer une image nginx dans un conteneur (port local 8090), puis aller explorer le contenu du dossier ```/usr/share/nginx/html``` du conteneur. Vérifier le bon fonctionnement de l'image dans votre navigateur (on doit avoir le message "Welcome to nginx!").

4. Créer un nouveau conteneur à base de l'image nginx (port local 8091), mais en créant un volume Docker qui relie le dossier local ```/home/NOM_UTILISATEUR/mon_super_site_web``` au dossier du conteneur ```/usr/share/nginx/html/mon_super_site_web```.

5. Expliquer alors pourquoi le site web est accessible depuis http://localhost:8091/mon_super_site_web/. On pourra explorer l'onglet "Files" de ce second conteneur.

Remarque : on pourrait aussi créer des images docker qui contiennent tout le code source de l'application web.

6. Supprimer le conteneur, puis le re-créer à l'aide de la ligne de commande uniquement. Pour monter le volume, utiliser l'option suivante : ```-v /chemin/original/machine/physique:/chemin/dans/le/conteneur``` (option de la commande ```docker run```).

# Références

https://docs.docker.com/storage/volumes/