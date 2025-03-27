# Configuration IPv6 (Debian)

## Remarques régénrales

- La configuration d'une interface dans */etc/network/interfaces* empêche sa prise en charge par le *NetworkManager* utilisé par GNOME.
- L'utilisation de l'autoconfiguration IPv6 requiert qu'un routeur émette des ICMPv6 RA (cf. installation et configuration du package *radvd*)

---

## Configuration IPv6 statique d'une interface

Dans le fichier */etc/network/interfaces*
```
auto <iface>
iface <iface> inet6 static
    address <prefix>/<length>
    gateway <address>
```

iface
: nom de l'interface  
prefix
: préfixe IPv6, ex: 2a02:c8a:12:1008::  
length
: longueur de préfixe, ex: 64 (pour /64)  

---
## Configuration IPv6 d'une interface en autoconfiguration 
Dans le fichier */etc/network/interfaces*
```
auto <iface>
iface <iface> inet6 auto
```
iface
: nom de l'interface  

---
## Activation du routage IPv6
### Activation temporaire
```
$ sudo sysctl -w net.ipv6.conf.all.forwarding=1
```
### Activation permanente
Dans le fichier */etc/sysctl.conf* décommenter la ligne suivante
```
net.ipv6.conf.all.forwarding=1
```
Ensuite rehcrager la configuration:
```
$ sudo sysctl -p /etc/sysctl.conf
```
---
## Activation des ICMPv6 RA avec le package *radvd*
### Installation du package *radvd*
```
$ sudo apt install radvd
```
*radvd* se configure via le fichier */etc/radvd.conf* qui n'est pas créé lors de l'installation du package.

### Configuration de *radvd*
Modifier ou créer le fichier */etc/radvd.conf*
```
interface <iface> {
    AdvSendAdvert on;
    prefix <prefix>/<length>
    {
        AdvOnLink on;
        AdvAutonomous on;
        AdvRouterAddr on;
    };
};
```
iface
: nom de l'interface  
prefix
: préfixe IPv6, ex: 2a02:c8a:12:1008::  
length
: longueur de préfixe, ex: 64 (pour /64)  

### Redémarrage du service
```
$ sudo systemctl restart radvd
```

---
## Création d'un tunnel 6to4
Un tunnel 6to4 permet d'encapsuler des paquest IPv6 dns des paquets IPv4 afin de permettre à deux réseaux IPv6 de communiquer au travers d'une zone IPv4.

```
                                              |                +----------+
                                              |                |          |
                                              | 192.168.0.20/24| Routeur  |     Réseau IPv6
                                              +----------------+          +-----------------
                                              |                |    B     |
                                              |                |          |
                                              |                +----------+
                  +----------+                |
                  |          |                |
 Réseau IPv6      | Routeur  |                |
------------------+          +----------------+
                  |    A     |192.168.0.10/24 |
                  |          |                |
                  +----------+                |
                                              |
                                              |                +----------+
                                              |                |          |
                                              | 192.168.0.30/24| Routeur  |    Réseau IPv6
                                              +----------------+          +----------------
                                              |                |    C     |
                                              |                |          |
                                              |                 +----------+
```
Les réseaux IPv6 situés derrière le routeur qui sert de point d'entrée/sortie du tunnel doivent être adressés en fonction de l'adresse IPv4 du routeur selon le schéma suivant:  2002:XXXX:XXXX::/48 où XXXX:XXXX  correspond à l'expression au format hexadécimal de l'adresse IPv4.

**Exemple:**
Pour le routeur A: 
192.168.0.10 s'écrit en hexadécimal C0 A8 00 0A  
Les réseaux derrière le routeur A doivent donc être adressés dans la plage suivante: 2002:C0A8:A::/48

### Configuration de l'interface 6to4
Dans le fichier */etc/network/interfaces*
```
auto <iface>
iface <iface> inet6 6to4
    source <ipv4 address>
    address <prefix>/<length>    # optionnel
``` 
iface
: nom de l'interface (à définir soi même)  
prefix
: préfixe IPv6, ex: 2a02:c8a:12:1008::  
length
: longueur de préfixe, ex: 64 (pour /64)  

### Redémarrage du servuice réseau
```
$ sudo systemctl restart networking
```
---
## Commandes relatives à IPv6
### Afficher les informations des interfaces IPv6
```
$ ip -6 addr
```
### Afficher les résolutions d'adresses ICMPv6 ND
```
$ ip -6 neigh
```
### Afficher ta table de routage IPv6
```
$ ip -6 route
```