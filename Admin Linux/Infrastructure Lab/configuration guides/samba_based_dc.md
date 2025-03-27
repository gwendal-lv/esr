# Using Samba 4 as Active Directory Domain Controller (Ubuntu 20.04 LTS)

Samba4 by default provides a way to create Active Directory domains, including DNS zone management.

Some basic assumptions:
- You start from a fresh Ubuntu 20.04 LTS server installation
- The hostname is *addc*
- The domain name will be *linux.lab*
- The server use static IP address 192.168.0.100/24

## Preparing the machine
### Disable systemd-resolved stub listener 
*systemd-resolved* can prevents samba dns service to work properly.  

*/etc/systemd/resolv.conf*
```
[Resolve]
DNSStubListener=no
```


### Configure DNS forwarder manualy
*/etc/resolv.conf*
```
nameserver 1.1.1.1
options edns0 trust-ad
search linux.lab
```





### Edit */etc/hosts*
- 127.0.0.0.1 must resolve to localhost
- 127.0.1.1 entry must be removed
- lan ip address must resolve to both hostname and fqdn
```
127.0.0.1 localhost
#127.0.1.1 addc
192.168.0.100      addc.linux.lab  addc

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```


## Installing required packages

```
$ sudo apt install acl attr samba samba-dsdb-modules samba-vfs-modules winbind libpam-winbind libnss-winbind libpam-krb5 krb5-config krb5-user dnsutils
```

## Prepare Provisionning the Samba Active Directory

### Stoping and disabling unneeded services
```
$ sudo systemctl stop nmbd smbd winbind
$ sudo systemctl disable smbd nmbd
```

### Removing base config files
```
$ sudo rm /etc/krb5.conf
$ sudo rm /etc/samba/smb.conf
```

### Removing old database files
Samba by default use *tdb* and *ldb* files to store informations in several locations.
- Get database files locations:
```
$ smbd -b | egrep "LOCKDIR|STATEDIR|CACHEDIR|PRIVATE_DIR"
LOCKDIR: /run/samba
STATEDIR: /var/lib/samba
CACHEDIR: /var/cache/samba
PRIVATE_DIR: /var/lib/samba/private
```
- Remove all *.tdb and *.ldb files from each folder

## Provision the Samba AD

### Create the domain structure
```
$ sudo samba-tool domain provision --server-role=dc --use-rfc2307 --dns-backend=SAMBA_INTERNAL --realm=LINUX.LAB --domain=LINUX --adminpass=Azerty1
```
Where...
- realm : domain name, must be CAPITALIZED
- domain : Netbios name of the domain, must be CAPITALIZED
- adminpass : Password of the Administrator user (default domain Administrator)

### Create a reverse DNS zone
```
$ sudo samba-tool dns zonecreate -U Administrator 192.168.0.100 168.192.in-addr.arpa
```

### Configure Kerberos
Samba-tool should have create *krb5.conf* in */var/lib/samba/private/*. The file must be copied in */etc*. Simlinking won't work because of file permissions.
```
$ sudo copy /var/lib/samba/private/krb5.conf /etc
```
The file shoud like this...
```
[libdefaults]
        default_realm = LINUX.LAB
        dns_lookup_realm = false
        dns_lookup_kdc = true
```

## Starting Samba Domain Controller
### Enable samba-ad-dc service
```
$ sudo systemctl unmask samba-ad-dc.service
$ sudo systemctl enable samba-ad-dc.service
```

## If local DNS lookup fails ...
*systemd.resolved* can still prevents DNS lookup for the local domain.  
To correct the problem:
- disable *systemd-resolved.service*
- edit manually */etc/resolv.conf*

### Start, stop, status
```
$ sudo service samba-ad-dc.service start|stop|status|restart
```

## Testing the AD DC installation

### DNS verifications
#### Verify the DC resolution
```
$ dig -t SRV @localhost _ldap._tcp.linux.lab

; <<>> DiG 9.16.1-Ubuntu <<>> -t SRV @localhost _ldap._tcp.linux.lab
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 6171
;; flags: qr aa rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 0

;; QUESTION SECTION:
;_ldap._tcp.linux.lab.          IN      SRV

;; ANSWER SECTION:
_ldap._tcp.linux.lab.   900     IN      SRV     0 100 389 addc.linux.lab.

;; AUTHORITY SECTION:
linux.lab.              3600    IN      SOA     addc.linux.lab. hostmaster.linux.lab. 1 900 600 86400 3600

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: ven. sept. 17 12:24:02 CEST 2021
;; MSG SIZE  rcvd: 110
```

### Test AD Authentication
```
$ kinit -V Administrator
$ klist
```




# Samba File Server in ADS Mode

## Prerequisites
- The server must be able to resolve the domain DNS zone.

## Installing required packages
```
$ sudo apt install samba winbind krb5-user libpam-winbind libnss-windind
```

## Configuring Samba */etc/samba/smb.conf*
```
[global]
        workgroup = LINUX
        security = ADS
        realm = LINUX.LAB

        winbind refresh tickets = Yes
        vfs objects = acl_xattr
        map acl inherit = Yes
        store dos attributes = Yes

        dedicated keytab file = /etc/krb5.keytab
        kerberos method = secrets and keytab

        winbind use default domain = yes
        winbind nss info = template
        winbind enum users = yes
        winbind enum groups = yes

        username map = /user/local/samba/etc/user.map

        idmap config * : backend = tdb
        idmap config * : range = 3000-7999

        idmap config LINUX:backend = rid
        idmap config LINUX:schema_mode = rfc2307
        idmap config LINUX:range = 10000-999999
```

## Configuring Kerberos */etc/krb5.conf*
```
[libdefaults]
        default_realm = LINUX.LAB
        dns_lookup_realm = false
        dns_lookup_kdc = true
```

## Configuring NSSSWITCH */etc/nssswitch.conf*
```
passwd:         files winbind systemd
group:          files winbind systemd
shadow:         files
gshadow:        files

hosts:          files dns
networks:       files

protocols:      db files
services:       db files
ethers:         db files
rpc:            db files

netgroup:       nis
```

## Restarting services
```
$ sudo service smbd restart
$ sudo service nmbd restart
$ sudo service winbind restart
```

## Joining and testing the domain membership

### Joining the domain
```
$ sudo net ads join -U Administrator
```

### Testing domain membership
Check if you can obtain a ticket from the controller
```
$ kinit -V Administrator
$ klist
```

Check connectivity with the domain-controller
```
$ wbinfo --ping-dc
```

Check if domain users are added to local database
```
$ getent passwd
```
there should be at least two new users:
```
administrator:*:10500:10513::/home/LINUX/administrator:/bin/false
krbtgt:*:10502:10513::/home/LINUX/krbtgt:/bin/false
```

## Using domain users/groups for files permissions
You can now use domain users/groups for file ownership with the regular *chown* command.  
Example:
```
$ sudo chown -Rf "LINUX\\Administrator":"LINUX\Domain Users" /srv/files
```
This will set *administrator@linux.lab* as owner and *"Domain Users"* as the owner group.


## Create a shared folder on the member server
When using AD permissions, never user *user* or *group* directives in the share definition (like *valid users* or *force user*).  
Example (*/etc/samba/smbd.conf*):
```
[files]
        comment = Shared folder
        path = /srv/samba/files
        browsable = yes
        guest ok = no
        read only = no
        create mask = 0755
        directory mask = 0755
```