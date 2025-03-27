# Deploying a fileserver using Samba (Ubuntu 20.04)

## Introduction

Samba is a free and open-source implementation of the SMB protocol. It provides ressources (files and printers) sharing service across the network for Windows clients but run on most Unix-like systems.

Samba can run standalone or integrated in centrally managed systems like Active Directory and even act as domain controller.

## Samba server types

### Standalone server
Clients must firs log-on with valid username and password stored locally.  
This is the default server mode.

### Member server
This mode is intended to integrate the server in a Windows domain. Active Directory users are mapped to local users.

### Active Directory domain controller
Runs the server as a Windows Domain Controller providing domain logon services to Windows and Samba clients.

## Samba security modes

### Users mode
Client must log-on with a valid username and password stored locally.

### ADS mode
Samba will act as a member of Active Directory realm and authenticate users using the domain controller services. (Require kerberos installed and configured).

## Samba installation & configuration

### Installing samba
```
$ sudo apt install samba
```

### Configuring Samba as standalone server

By default the main configuration file is */etc/samba/smb.conf*.  
Settings are grouped in sections starting with *[section name]*.

#### General settings

```ini
# General settings
[global]
    ### AUTHENTICATION ###
    # Define the server as standalone
    server role = standalone server

    # Use locally stored username/passwords
    security = user

    # Apply PAM rules/restrictions
    obey pam restrictions = yes

    # Synchronize system user password with samba password
    unix password sync = yes

    # Tool to configure system passwords
    passwd program = /usr/bin/passwd %u
    passwd chat = *Enter\snew\s*\spassword:* %n\n *retype\snew\s*password:* %n\n *password\supdated\ssuccessfully* .

    # Use PAM to modify passwords
    pam password change = yes

    # Map failed authentication to anonymouse connections.
    map to guest = bad user


    ### GENERAL SETTINGS ###
    # Domain/Workgroup name
    workgroup = WORKGROUP

    # Server description
    # %h will be replaced with the server hostname
    server string = %h Samba server

    # Which interfaces to use
    interfaces = 127.0.0.0/8 enp0s3

    # Enable specifi interface usage
    bind interfaces only = yes

    # Restrict access to clients in specific networks
    # allows all client with ip addresses starting with 192.168. or 127.
    hosts allow = 192.168. 127.

    # Define password storage backend
    # tbmsam (Trivial database) stores users in database files.
    # for large implmentation ( >250 users ) ldapsam should be prefered but requires an ldap server.
    passdb backend = tdbsam

    # Separates log files for each machine
    log file = /var/log/samba/log.%m

    # Maximum log size (KiB)
    max log size = 1000

    # Logging system to use
    # logs alla messages to files and important syslog message to syslog service
    logging = file syslog@1
```

#### Defining a user home directory share
Samba uses a specific [homes] section to define a dedicated home directory for each user. By default it will share the system user home directory (ie: /home/username).
```ini
[homes]
    # Share description
    comment = Users home directories
    # shown in shares list (or not)
    browseable = no
    # Can user write or not
    read only = no
    # Permissions applied to new files
    create mask = 0755
    # Permissions applied to new directories
    directory mask = 0755
    # Who can access the share ( %S matches the shared folder/username )
    valid users = %S
```
This will create a share smb://samba_server/username and only allow the user to browse/access the content.

#### Defining a shared folder
```ini
# Share name
[files]
    # Share description
    comment = Shared folder
    # Share files location
    path = /srv/samba/files
    # Shown in shares list
    browsable = yes
    # Allow anonymous connection (or not)
    guest ok = no
    # Can user write or not
    read only = no
    # New file permissions
    create mask = 0755
    # New directory permissions
    directory mask = 0755
    # Force file/directory owner
    force user = root
    # Force file/directory group
    force group = employees
    # Who can access the share (can be usernames or @groupname)
    valid users = @employees
```

### Test configuration files
```
$ testparm
```
This will report errors or dump the configuration if everything is OK.


### Start/Stop/Restart samba services
```
$ sudo service smbd start|stop|restart|status
$ sudo service nmbd start|stop|restart|status
```

### User management

#### Add user
Users must exists in both system and samba database. Samba will use user-id to set permisisons etc.  
1) Create the system user
```
$ sudo adduser <username> --disabled-login
```
note: *--disabled-login* prevents the user to log in the server as user.  

2) Define user Samba password
```
$ sudo pdbedit -a <userbname>
```

#### Remove user
```
$ sudo pdbedit -x <username>
```
Note: This won't remove system user.


### Reset account (unlock)
```
$ sudo pdbedit -z <username>
```

### Change user password
```
$ sudo smbpasswd <username>
```

#### List users
```
$ sudo pdbedit -L
```

#### Display user informations
```
$ sudo pdbedit -v <username>
```
