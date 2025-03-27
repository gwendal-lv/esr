# Routing related configuration (Ubuntu 20.04)

## Enabling IPv4 routing permanently
In */etc/sysctl.conf* uncomment the following line:
```
net.ipv4.ip_forward=1
```
Apply changes
```
$ sudo sysctl -p
```

## Adding static routes using **netplan**
With **netplan** static routes must be added under the interface confuiguration block in the YAML file.

### Static route to a defined network example
```yaml
network:
    version: 2
    ethernets:
        enp0s3:
            addresses: [192.168.0.10/24]
            routes:
                - to: 10.0.0.0/8
                  via: 192.168.0.1
```

### Default route example
```yaml
network:
    version: 2
    ethernets:
        enp0s3:
            addresses: [192.168.0.10/24]
            routes:
                - to: 0.0.0.0/0
                  via: 192.168.0.1
```

### Multiple static routes example
```yaml
network:
    version: 2
    ethernets:
        enp0s3:
            addresses: [192.168.0.10/24]
            routes:
                - to: 10.0.0.0/8
                  via: 192.168.0.1
                - to: 172.16.0.0/24
                  via: 192.168.0.2
                - to: 172.16.1.0/24
                  via: 192.168.0.3
```

### Testing, applying and verifying configuration
Test netplan configuration
```
$ sudo netplan try
```
Apply netplan configuration
```
$ sudo netplan apply
```
Verify routing table
```
$ ip route
```