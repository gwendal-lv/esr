# Docker - introduction

---

# Conteneurs d'applications

## Machine virtuelle vs. Conteneur

![](img/VM_vs_container.png)


Avantages des conteneurs par rapport aux VMs:
- très légers (stockage, RAM et CPU)
- rapides à créer / modifier / déployer
- possibilité de mise à l'échelle (exemple : application en double/triple pour répartir la charge de calcul)

Avantages des VMs par rapport aux conteneurs:
- offrent un OS complet
- modifiable après création 

## Exemple : micro-services

| Architecture monolithique | Architecture basée sur micro-services |
| - | - |
| ![](img/arch_monolithic.png) | ![](img/arch_microservice.png) |


# Conteneur vs. image

## Création d'une image

- Image = format standardisé d'une application, déployable facilement
- La commande ```docker build``` permet de construire une image d'application, à l'aide du Dockerfile
    - Exemples d'applications :
        - serveur web statique Nginx
        - application web Node.JS
        - base de données MySQL
        - réseau de neurones avec Python/PyTorch
        - etc.
- La commande ```docker run``` permet d'exécuter une image dans un conteneur

![](img/dockerfile_image_container.png)

## Création de conteneurs à partir d'une image

![](img/single_image_multi_container.png)

---

# Références

https://aws.amazon.com/fr/compare/the-difference-between-containers-and-virtual-machines

https://docs.docker.com/build/

https://cto.ai/blog/docker-image-vs-container-vs-dockerfile/

