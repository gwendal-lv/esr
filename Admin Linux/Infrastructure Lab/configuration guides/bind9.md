# BIND9 configuration on Ubuntu Server 20.04

## Tools for querying DNS servers

The package *bind9-dnsutils* provides a collection of tools for querying DNS servers and finding out informations about hosts and also some tools for system administration.

Installing *bind9-dnsutils* (installed by default on Ubuntu Server 20.04)

```
$ sudo apt install bind9-dnsutils
```

### Manual DNS query with *nslookup*

```
$ nslookup [-q=<type>] <domain-name> [dns-server]
```

Simple DNS query example:

```
$ nslookup google.be 1.1.1.1
Server:         1.1.1.1
Address:        1.1.1.1#53

Non-authoritative answer:
Name:   google.be
Address: 142.250.179.195
Name:   google.be
Address: 2a00:1450:400e:803::2003
```

Querying for a specific entry (ie: MX, mail exchange server entry)

```
$ nslookup -q=MX gmail.com 1.1.1.1
Server:         1.1.1.1
Address:        1.1.1.1#53

Non-authoritative answer:
gmail.com       mail exchanger = 40 alt4.gmail-smtp-in.l.google.com.
gmail.com       mail exchanger = 10 alt1.gmail-smtp-in.l.google.com.
gmail.com       mail exchanger = 30 alt3.gmail-smtp-in.l.google.com.
gmail.com       mail exchanger = 20 alt2.gmail-smtp-in.l.google.com.
gmail.com       mail exchanger = 5 gmail-smtp-in.l.google.com.
```

### Detailed DNS lookup with *dig*

```
$ dig [@dns-server] <domain-name> [type]
```

Simple DNS lookup

```
$ dig @1.1.1.1 gmail.com

; <<>> DiG 9.16.1-Ubuntu <<>> @1.1.1.1 gmail.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 1790
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;gmail.com.                     IN      A

;; ANSWER SECTION:
gmail.com.              76      IN      A       142.250.179.165

;; Query time: 19 msec
;; SERVER: 1.1.1.1#53(1.1.1.1)
;; WHEN: Wed Aug 25 08:55:28 CEST 2021
;; MSG SIZE  rcvd: 54
```

DNS lookup for a specific entry type

```
$ dig @1.1.1.1 gmail.com MX

; <<>> DiG 9.16.1-Ubuntu <<>> @1.1.1.1 gmail.com MX
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 36804
;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;gmail.com.                     IN      MX

;; ANSWER SECTION:
gmail.com.              3566    IN      MX      40 alt4.gmail-smtp-in.l.google.com.
gmail.com.              3566    IN      MX      20 alt2.gmail-smtp-in.l.google.com.
gmail.com.              3566    IN      MX      5 gmail-smtp-in.l.google.com.
gmail.com.              3566    IN      MX      10 alt1.gmail-smtp-in.l.google.com.
gmail.com.              3566    IN      MX      30 alt3.gmail-smtp-in.l.google.com.

;; Query time: 23 msec
;; SERVER: 1.1.1.1#53(1.1.1.1)
;; WHEN: Wed Aug 25 08:57:20 CEST 2021
;; MSG SIZE  rcvd: 161
```

## BIND9 Installation

```bash
$ sudo apt install bind9
```

## Configuration files and default settings

By default Bind9 comes with several configuration files.

- Daemon related configuration: */etc/default/named* file
- Service related configuration: */etc/bind/* folder

Main configuration file is */etc/bind/named.conf*.  
It's possible to put the whole configuration in this file, but a better approach is to use separarted files for each "topic" (zones definitions, general parameters, ...) and then include them in *named.conf*.  

Bind9 general options (default forwarder, ipv4/ipv6 listening interfaces, ...) are located in */etc/bind/named.conf.options*.  

Configuration about local names (DNS roots, localhost, ...) can be found in */etc/bind/named.conf.default-zones*.  

Finally, */etc/bind/named.conf.local* should contain all custom configurations.

## Verify configuration files

```
$ sudo named-checkconf /etc/bind/named.conf
```

## Start, stop, reload ... Bind9

```bash
$ sudo service named start|restart|stop|reload|force-reload|status
```

## Bind9 Configuration

### Terminology

- Forwarder: server to which resuqests will be forwarded
- Recursive search: the local server will resolve the queried domain name starting from the root servers and then cache the result.
- Iterative search: the dns client resolve a domain name using result received from multiple dns servers. 

### Base configuration

Base configuration in */etc/bind/named.conf.options*

```c
options {
    # Working directory
    directory "/var/cache/bind";

    # Defining listening interfaces
    # any               : all interfaces
    # none              : no interface
    # ipv4/ipv6 address : use defined interfaces only

    # Listen on all local IPv4 interfaces for queries
    listen-on { any; };

    # Don't listen on any IPv6 interfaces for queries
    listen-on-v6 { none; };

    # Enable or disable recusion
    recursion yes;

    # Will send authoritative answers or not for unknown domains
    auth-nxdomain no; # conform to RFC1035

    # Allowed clients queries, can be "any" or list of specific networks/addresses
    allow-query { 192.168.0.0/24; };

    # Allowed clients to query local cache, can be "any" or list of specific networks/addresses
    allow-query-cache { 192.168.0.0/24; };

    # Allowed clients to use recrusion
    allow-recursion { 192.168.0.0/24; }; 

    # List of servers to forward requests
    # If none set, Bind will use recusive search if enabled.
    forwarders {
        # Google Public DNS
        8.8.8.8;
        8.8.4.4;

        # Cloudflare Public DNS
        1.1.1.1;
    };

};
```

Without any other configuration, this will make Bind work as a caching DNS server.

- Bind will listen on all IPv4 interfaces.
- Bind won't listen on any IPv6 interface.
- Bind will use recusion when needed to resolve domain names.
- Only queries from clients of the 192.168.0.0/24 network will be treated.
- Queries for domains not defined on this server will be forwared to public.

### Using ACLs to define addreses ranges

ACLs can be used in Bind configuration files to identify addresses ranges / networks. They can be written in any file but must be defined before any usage.  

Note: Acls are ordered list of rules. the first rule matching tha address is applied.

#### Simple ACL example

```c
acl trusted_clients {
    192.168.0.0/24;
    192.168.1.0/24;
};
```

#### Exclusion ACL example

```c
acl anything_but_this {
    !172.16.0.0/12;
    !10.0.0.0/8;
    any;
}
```

#### Nest ACL example

```c
acl some_hosts {
    172.16.0.0/24;
};

acl some_more_hosts {
    "some_hosts";
    172.16.0.1/24;
}
```

#### A nice way to integrate ACLs in Bind9

- Create a file where all ACLs will be defined (ie: */etc/bind/named.conf.acl*)
- Include that fil in */etc/named.conf* before any other include statement

*named.conf.acl* example

```c
acl network_clients {
    192.168.0.0/24;
    !192.168.1.50/32;
    192.168.1.0/24;
};
```

*named.conf.options* example

```c
options {
    directory "/var/cache/bind";
    listen-on { any; };
    listen-on-v6 { none; };
    recursion yes;
    auth-nxdomain no;

    allow-query { network_clients; };
    allow-query-cache { network_clients; };
    allow-recursion { network_clients; }; 

    forwarders {
        8.8.8.8;
        8.8.4.4;
        1.1.1.1;
    };

};
```

*named.conf* example

```c
include "/etc/bind/named.conf.acl";
include "/etc/bind/named.conf.options";
include "/etc/bind/named.conf.local";
include "/etc/bind/named.conf.default-zones";
```

### Configuring a DNS zone

There are several DNS zone types, the three main ones are:

- master / primary: the master copy of the zone informations.
- slave / secondary: the whole zone information inherited from a master zone.
- forward: forwards requests to recursive dns servers.

To define a zone (a domain name), there must be a zone declaration in *named.conf.local* or in any file included and a zone definition (DNS entries etc.)

#### Master/Primary zone declaration examples

##### A master direct dns zone without slave server nor dynamic dns update.

```c
zone "linux.lab" {
    type master;
    file "/etc/bind/zones/db.linux.lab";
    allow-query { trusted-clients; };
    allow-transfer { none; };
    notify no;
    allow-update { none; };
};
```

##### A master reverse dns zone without slave server nor dynamic dns update.

```c
zone "0.168.192.in-addr.arpa." {
    type master;
    file "/etc/bind/zones/db.linux.lab.rev";
    allow-query { trusted-clients; };
    allow-transfer { none; };
    notify no;
    allow-update { none; };    
};
```

##### DNS zone definition file *db.linux.lab*

See [https://bind9.readthedocs.io/en/latest/reference.html#zone-file](https://bind9.readthedocs.io/en/latest/reference.html#zone-file) for the complete zone definition informations.

```bind
$ORIGIN .   ; following names are relative to dns root
$TTL 300    ; 5 minutes

linux.lab       IN  SOA ns1.linux.lab. hostmaster.linux.lab. (
                        2021082401  ; serial number
                        14400       ; refresh time (4h)
                        900         ; retry timer (15m)
                        28800       ; expire after (8h)
                        240         ; minimum (4m)
                        )

                NS      ns1.linux.lab.
                NS      ns2.linux.lab.

$ORIGIN linux.lab.
ns1             A       192.168.0.10
ns2             A       192.168.0.11
dhcp1           CNAME   ns1
dhcp2           CNAME   ns2
gateway         A       192.168.0.1
```

##### Reverse DNS zone definition file *db.linux.lav.rev*

```bind
$ORIGIN .
$TTL 300

0.168.192.in-addr.arpa  IN  SOA ns1.linux.lab. hostmaster.linux.lab. (
                        2021082401  ; serial number
                        14400       ; refresh (4h)
                        900         ; retry timer (15m)
                        28800       ; expire after (8h)
                        240         ; minimum (4m)
                        )

                NS      ns1.linux.lab.
                NS      ns2.linux.lab.

$ORIGIN 0.168.192.in-addr.arpa.
1               PTR     gateway.linux.lab.
10              PTR     ns1.linux.lab.
11              PTR     ns2.linux.lab.
```

#### Configuring DNS redundancy with master and slave zone

In this example, primary DNS server is 192.168.0.10 and secondary is 192.168.0.11.

On primary DNS server

```c
zone "linux.lab" {
    type master;
    file "/etc/bind/zones/db.linux.lab";
    allow-query { trusted-clients; };
    allow-transfer { 192.168.0.11; };
    notify yes;
    allow-update { none; };
};
```

On secondary DNS server

```c
zone "linux.lab" {
    type slave;
    file "/var/lib/bind/db.linux.lab";
    allow-query { trusted-clients; };
    masters { 192.168.0.10; };
};
```

Notes:

- The secondary server doesn't need the definition file. It will synchronize with the master server and populate the file itself.
- Same configuration principe applies for direct and reverse dns zones.

### Configuring dynamic zone updates from *isc-dhcp-server*

Dynamic DNS updates are usefull to allow hosts (workstations, laptops, ...) using their DNS name.  
The goal is to make the DHCP server update de DNS zone definition when a client gets its configuration.  
The dynamic update configuration is only needed on the primary server.

#### Prerequisites

- *bind9* and *isc-dhcp-server* running. If they are running on separate hosts, they must be able to communicate.
- Zones that must be updated dynamicaly must be configured (direct and/or reverse zones).

#### Generating RNDC encryption key

Bind9 comes with a tool, *rndc*, to interact with the Bind9 service. When the DHCP server wants to update the zone definition, il witll use *rndc* to communicate with *Bind9*.

An encryption key must be shared between the DHCP server and the DNS server.

By default Bind9 will generates an encryption key stored in */etc/bind/rndc.key*. You can either use that one or generate a new one.

```bash
$ tsig-keygen [-a algorithm] <key_name> > <destination_filepath>
```

Both DNS server and DHCP server must have the same key definition.  
It's also possible to add the key definition directly in the *dhcpd.conf* and the *named.conf* (or any include file), but it's generally a better idea to keep the key in a separate file to prevent anyone to be able to read the file.

#### Configuring DDNS in Bind9

In */etc/named.conf* add the following line before any other include statement.

```c
include "/etc/bind/rndc.key";
```

Update the zones declarations to allow dynamic updates.

```c
zone "linux.lab" {
    type master;
    file "/etc/bind/zones/db.linux.lab";
    allow-query { trusted-clients; };
    allow transfer { 192.168.0.11; };
    notify yes;
    allow-update { key rndc-key; };
    journal "/var/cache/bind/linux.lab.jnl";
}

zone "0.10.in-addr.arpa." {
    type master;
    file "/etc/bind/zones/db.linux.lab.rev.db";
    allow-query { trusted-clients; };
    allow transfer { 192.168.0.11; };
    notify yes;
    allow-update { key rndc-key; };
    journal "/var/cache/bind/0.10.in-addr.arpa.jnl";
}
```

By default, Bind9 will create a journal file with the same name as the zone definition and in the same folder. (ie: */etc/bind/zones/db.linux/lab.jnl*).
The *bind* user must have write permission on the folder containing the zone definition.  

It's generally a bad idea to let a service write in `/etc`, that's why we use the `journal` instruction which tells bind where to write the dynamix updates.

#### Configuring DDNS updates in *isc-dhcp-server*

Dynamic dns configuration in */etc/dhcp/dhcpd.conf*

```c
include "/etc/dhcp/rndc.key";

ddns-updates on;
ddns-update-style standard;

zone linux.lab. {
    primary 192.168.0.10;
    key rndc-key;
};

zone 0.168.190.in-addr.arpa. {
    primary 192.168.0.10;
    key rndc-key;
};
```

Notes:

- domain-name option in subnet definition must match the zone to update.
- *primary* defines the address or hostname of the primary dns server of the zone
- *key* defines which signature key to use (name of the key ibn the key file).

#### Restart both services

Bind9 and isc-dhcp-server must be restarted for changes to take effect.

#### Verifying DDNS operations

On the primary DNS server:

```
$ sudo systemctl -u named -f
```

DNS updates created by the DHCP server will appear in the log.  
Most common errors are:

- rdnc key mismatch
- key file permissions
- bind cannot write in the zones folder 

### Modifying a dynamic DNS zone

Modifying and reloading without freezing a dynamix zone will generally ends with a "out of sync" journal file which prevents the zone to be loaded.

To safely modify a dynamic zone, follow the next steps:

1) Freeze the dns zone  
   
   ```
   $ sudo rndc freeze <zonename>
   ```
2) Edit the zone definition file
3) Thaw the frozen zone
   
   ```
   $ sudo rndc thow <zonename>
   ```
   
   bind will automatically reload the zone.