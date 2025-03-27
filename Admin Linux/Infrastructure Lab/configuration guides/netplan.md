# Configuring Network Interfaces using **netplan**

**netplan** is the default network configuration interface for ubuntu 20.04 Server.  
Network configuration is made through YAML configutatyion files located in */etc/netplan*.  
Configurations can be stored in a signle file or in several files.


## Configuration file examples
### Single interface using IPv4 DHCP
```yaml
network:
    version: 2
    ethernets:
        enp0s3:
            dhcp4: true
```

### Single interface using static IPv4 address
```yaml
network:
    version: 2
    ethernets:
        enp0s3:
            addresses: [192.168.0.10/24]
            gateway4: 192.168.0.1
            nameservers: 
                addresses: [8.8.8.8, 8.8.4.4]
                search: ["domain.com"]
```

### Multiple interfaces
```yaml
network:
    version: 2
    ethernets:
        enp0s3:
            addresses: [192.168.0.10/24]
            gateway4: 192.168.0.1
            nameservers: 
                addresses: [8.8.8.8, 8.8.4.4]
                search: ["domain.com"]
        
        enp0s8:
            dhcp4: true
```

## Testing and applying
### Testing configuration
```
$ sudo netplan try
```

### Apply configuration
```
$ sudo netplan apply
```