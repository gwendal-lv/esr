# À la base, on part d'une image de Python 3.10 (peu importe s'il existe de nouvelles versions de Python)
#     avec Python contenu dans un "tout petit linux" appelé "alpine" (minimum 5Mo)
# Si on avait utilisé une image python basée sur ubuntu, le conteneur ferait minimum 150Mo
FROM python:3.10-alpine

# Port du serveur Flask (5000 par défaut)
EXPOSE 5000

# RUN exécute des commandes dans un terminal à l'intérieur du conteneur
# D'abord on crée un dossier dans lequel on va mettre (copier) notre code source
RUN mkdir /app
COPY . /app

# Installation des dépendances python (par exemple : version spécifique de Flask)
RUN pip install -r /app/requirements.txt


# Finalement, on peut enfin lancer le serveur Flask (qui reste "tourner" dans le conteneur)
CMD python3 /app/app.py
