FROM node:14.17.3-alpine3.14

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
COPY .npmrc .
COPY .yarnrc.yml .
RUN npm ci
COPY ./server.js ./

# Lancement direct de node : .npmrc contient ignore-scripts=true, qui (npm 6)
# désactive aussi "npm start" -> le conteneur sortirait immédiatement (code 0)
CMD ["node","server.js"]
