# DHCP server & relay configuration

## Installing DHCP server on Ubuntu 20.04

### Instalation procedure
Install *isc-dhcp-server* package.
```
$ sudo apt install isc-dhcp-server
```

### Configure DHCP server
The main configuration file is */etc/dhcp/dhcpd.conf*  

The configuration must at least contain the following elements:
- default parameters (lease time, ...)
- DHCP server subnet (even if not used for address assignment)
- One subnet section for each network to manage

#### Minimal configuration file sample
```bash
# Default parameters
default-lease-time 86400;                       # default lease time in seconds
max-lease-time 172800;                          # maximum lease time in seconds
lease-file-name "/var/lib/dhcp/dhcpd.leases";   # where leases are stored
#authoritative;                                 # must be uncommented if DHCP server network must be managed.
ddns-update-style none;                         # don't update DNS entries

# Default options (not required)
option domain-name "linux.lab";                 # Default domain suffix for clients
option domain-name-servers 8.8.8.8, 1.1.1.1;             # Default dns-server for clients

# DHCP Server subnet
subnet 192.168.0.0 netmask 255.255.255.0 {
}
```
For each managed network an additionnal *subnet* declaration must added.
```bash
subnet 192.168.1.0 netmask 255.255.255.0 {
        default-lease-time          600;                        # Lease duration in seconds
        max-lease-time              7200;                       # Maximum lease duration
        option routers              192.168.1.1;                # Default gateway(s)
        option subnet-mask          255.255.255.0;              # Subnet mask
        option broadcast-address    192.168.1.255;              # subnet broadcast
        option domain-name-servers  8.8.8.8;                    # DNS server(s)
        option ntp-servers          192.168.1.1;                # NTP server(s)
        range                       192.168.1.10 192.168.1.50;  # Range of addresses to use
}
```

#### Define static address reservation
```
host client1 {
    hardware ethernet 00:01:01:ab:cd:01;
    fixed-address 192.168.1.87;
}
```

### Manage DHCP server

#### Start, stop, reload DHCP server
```
$ sudo service isc-dhcp-server start|restart|stop|reload
```

#### Display DHCP leases
```
$ dhcp-lease-list
```
All informations about leases are stored in the file defined by the *lease-file-name* parameter in */etc/dhcp/dhcpd.conf*.  

Each lease is defined by a *lease* block in the *dhcpd.leases* file:
```bash
lease 192.168.1.40 {
    starts 3 2021/08/18 08:25:11;                       # Lease start time
    ends 3 2021/08/18 08:35:11;                         # Lease end time
    binding state active;                               # Actual lease status
    next binding state expired;                         # Next lease status
    hardware ethernet 08:00:27:2d:ac:68;                # Client mac address
    uid "\001\010\000'-\254i";                          # Client unique ID
    set vendor-class-identifier = "udhcp 1.33.1";       # Client vendor id
    client-hostname "client-vm";                        # client hostname
}
```
To manually remove a lease:
1) Stop dhcpd service
2) Remove the whole lease block
3) Restart dhcpd service

---

## Configure DHCP failover with *isc-dhcp-server* on Ubuntu 20.04

DHCP failover allows two servers to work together through a communication channel, to assign addresses to clients.  
The main benefit is that the DHCP service will be assured as long as at least one server is running.

### Failover requirements with *isc-dhcp-server*
- Servers must be able to reach each other.
- Both servers should share the same subnet definitions.

### DHCP failover configuration

A failover section must be added to *dhcpd.conf* for each dhcp server.  
Subnets definition must include a *pool* definition where the failover peer is defined.

#### **Primary DHCP server configuration sample**
Failover peer configuration and OMAPI channel setup.
```bash
failover peer "dhcp-failover" {
    primary;
    address 192.168.0.100;              # Address of this server
    port 847;                           # Port this server will listen on
    peer address 192.168.0.101;         # Remote DHCP server address
    peer port 647;                      # Port remote DHCP server will listen on
    max-response-delay 60;              # Max wait time for a response from remote server
    max-unacked-updates 10;             # Max message unacked by remote server
    mclt 3600;                          # Time one server can extends a lease allocated by the other server (Mandatory, only on primary)
    split 128;                          # Each server will manage 50% of the address space (Mandatory, only on primary)
    load balance max seconds 5;                 # Serve other server's client requests if DHCP header "SECS" value is greater than 5.
}

omapi-port 7911;
omapi-key dhcp_key;

key dhcp_key {
    algorithm hmac-md5;                         # Hash algorithm used to generate the key
    secret 787f85c5247874b68c4a3307dd850cf3;    # Hashed key value (use hmac-md5 generator to create one), must be the same on both servers
}

```
*split* parameter defines how both servers with share the address range. 
- split is a value between 0 and 256
- split defines how many leading bits must be in the mac address to be managed by the primary server
- 128 means 50%-50% shares
- 256 means primary withh manage all addres space, secondary will only work if primary is down

OMAPI protocol is used by *isc-dhcp-server* to exchange objects informations securely between servers (dhcp leases, ...).

  
#### **Secondary DHCP server configuration sample**
```bash
failover peer "dhcp-failover" {
    secondary;
    address 192.168.0.101;              # Address of this server
    port 647;                           # Port this server will listen on
    peer address 192.168.0.100;         # Remote DHCP server address
    peer port 847;                      # Port remote DHCP server will listen on
    max-response-delay 60;              # Max wait time for a response from remote server
    max-unacked-updates 10;             # Max message unacked by remote server
    load balance max seconds 5;                 # Serve other server's client requests if DHCP header "SECS" value is greater than 5.
}

omapi-port 7911;
omapi-key dhcp_key;

key dhcp_key {
    algorithm hmac-md5;                         # Hash algorithm used to generate the key
    secret 787f85c5247874b68c4a3307dd850cf3;    # Hashed key value
}
```

#### **Subnet definitions modifications to support failover**
```bash
subnet 192.168.1.0 netmask 255.255.255.0 {
        default-lease-time          600;                        # Lease duration in seconds
        max-lease-time              7200;                       # Maximum lease duration
        option routers              192.168.1.1;                # Default gateway(s)
        option subnet-mask          255.255.255.0;              # Subnet mask
        option broadcast-address    192.168.1.255;              # subnet broadcast
        option domain-name-servers  8.8.8.8;                    # DNS server(s)
        option ntp-servers          192.168.1.1;                # NTP server(s)
        pool {
            failover peer "dhcp-failover";                      # Which failover peer to use
            range 192.168.0.10 192.168.0.100;                   # Address range managed by the failover service
        }
}
```
Changes to subnet definition must be done on both servers.  

Once configuration changes are made, both dhcp services must be restarted
```
$ sudo service isc-dhcp-server restart
```

#### **Verifying failover activity**
Failover communication is reported by default in */var/log/syslog*
```
$ tail -f /var/log/syslog
```

---

## Installing DHCP relay on Ubuntu 20.04

### What does DHCP relay do ?
DHCP packets sent by the client use broadcast destination address. This means the packet cannot be routed and can only be treated by hosts in the same broadcast domain.  
  

When the DHCP server is not in the same broadcast domain as the client, DHCP relay must be configured on the gateway of the network.  
  

DHCP relay extracts the client message and encapsulate it in a unicast packet to the DHCP server allowing routers to route the packet to the remote server.

### Installation procedure
Install *isc-dhcp-relay* package
```bash
$ sudo apt install isc-dhcp-relay
```
The setup script asks for several informations:
- Address of the DHCP server(s)
- Interface used for relaying DHCP packets
- Optionnals args

Use either the IP addresse(s) or hostname(s) of the "real" DHCP server(s).  
Interfaces list used for relaying DHCP packets must include all interfaces facing both clients and server(s).  

After setup is complete, modifications can be done editing */etc/default/isc-dhcp-relay*

### Configuration sample file
```ini
SERVERS="10.0.2.130"
INTERFACES="enp0s3 enp0s8"
OPTIONS=""
```

### (Re)Starting, stoppping DHCP relay
```bash
$ sudo service isc-dhcp-relay start|restart|stop|status
```
