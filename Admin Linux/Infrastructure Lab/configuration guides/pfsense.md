# pfSense Firewall

## Download PFsense Image

Official site: [https://www.pfsense.org/download/](https://www.pfsense.org/download/)

## Virtual Box Installation

### Virtual Machine settings:
- vCPU: 1 or 2 (1 is enough, 2 is smoother)
- RAM: 1024 Mb
- System type: FreeBSD 64bits
- Virtual Hard Drive: 16Go
- Network interfaces:
    - Wan interface (bridged on physical network for the topology)
    - LAN interface (common intnet with router-vm)
    - Management interface (host-only optionnal but easier for webconfiguration)

### Installation procedure:
Load the image file as a virtual disk, start the VM and follow the installation assistant instructions.

After installation and reboot, use the CLI menu to configure basic settings (network interfaces, ...):
- Define bridged interface as WAN interface
- Define host-only interface (if used) as LAN interface
- Define intnet interface as OPT1 interface (if hostonly used, else configrue as LAN)

By default pfSense will define NAT between WAN and LAN/OPT interfaces.

Configure IP addresses:
- WAN : dhcp
- LAN : host-only address (ie: 192.168.56.5/24)
- OPT1 : can be done later or configure wanted ip address.

Once network interfaces are configured, use the WebConfigurator and use the configuration assitant for initial configuration.

Important notes:
- pfSense can only be managed from its LAN interface by default
- webconfigurator is available at: **http://pfsense-lan-address**
- default login is: **admin**
- default password is: **pfsense**


## Configuration Guide lines

### Configure static routing
1) Configure a new gateway (next-hop of the desired static route) if not already done under *System/Routing/Wateways*.
2) Create the static route under *System/Routing/Static routes*