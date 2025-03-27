# Infrastructure Lab - Phase 1

## Description
The purpose of this first phase is to deploy main network services for the topology to work properly:
- Routing & NAT (NAT will be relocated on a firewall later)
- DHCP server with failpver
- Primary and secondary DNS servers
- NTP Server

Some devices and services will be added in further phases:
- PFsense Firewall betwwen router and external network
- File server
- etc.

## Virtual Machines specifications

### Router VM
- Operating system: Ubuntu 20.04 LTS Server
- RAM: 1 Go
- CPU: 1 or 2 (1 is enough, 2 is for usage smoothness)
- Network Interfaces: 5 Ethernet (see related doc too add 5th interface)

### Primary & Secondary DNS VMs
- Operating system: Ubuntu 20.04 LTS Server
- RAM: 1 Go
- CPU: 1 or 2 (1 is enough, 2 is for usage smoothness)
- Network Interfaces: 1 Ethernet

### Primary & Secondary DHCP VMs
- Operating system: Ubuntu 20.04 LTS Server
- RAM: 1 Go
- CPU: 1 or 2 (1 is enough, 2 is for usage smoothness)
- Network Interfaces: 1 Ethernet

### Employee & Techos VM
- Operating system: Alpine Linux (see related doc for installation)
- RAM: 512 Mo
- CPU: 1 or 2 (1 is enough, 2 is for usage smoothness)
- Network Interfaces: 1 Ethernet

### pfSense
- Operating system: pfSense (see related doc for installation)
- RAM: 1024 Mo
- CPU: 1 or 2 (1 is enough, 2 is for usage smoothness)
- Network Interfaces: 3 Ethernet ( 1 bridged, 1 Intnet and 1 hostonly)

### Samba file server
- Operating system: Ubuntu 20.04 LTS Server
- RAM: 1 Go
- CPU: 1 or 2 (1 is enough, 2 is for usage smoothness)
- Network Interfaces: 1 Ethernet