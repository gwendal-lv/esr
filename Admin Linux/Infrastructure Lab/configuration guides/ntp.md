# NTP Clock synchonization (Ubuntu 20.04)

## Introduction
NTP (Network Time Protocol) allows computers to synchronize their system clock over the network. It's intended to synchronize all participating computers clock to within a few milliseconds of the UTC time.

NTP uses a hierarchical system to organize time sources. Each level is called *stratum*.
- Stratum 0 : High precision clocks (atomic clocks, ...)
- Stratum 1 : Computers synchronized with their stratum 0 devices.
- Stratum 2 : computers suncgonized with several stratum 1 compures, they can also synchronize whith each other.
- etc.

NTP protocol use the Epoch Time as reference (1st Jan 1970 UTC).

## Manual time manipulation

### Display system time & date
```
$ date
Wed Aug 25 09:24:03 CEST 2021
```

### Display actual date and time system settings
```
$ timedatectl status
               Local time: Wed 2021-08-25 09:24:56 CEST
           Universal time: Wed 2021-08-25 07:24:56 UTC
                 RTC time: Wed 2021-08-25 07:24:56
                Time zone: Europe/Brussels (CEST, +0200)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

### Manually adjust system clock
```
$ sudo timedatectl set-time 'HH:mm:ss'
$ sudo timedatectl set-time 'A-M-J'
```
or
```
$ sudo timedatectl set-time 'A-M-J HH:mm:ss'
```

### Set system TimeZone
List available timezones
```
$ timedatectl list-timezones
```
Set system timezone
```
$ sudo timedatectl set-timezone Europe/Brussels
```

## Use NTP to synchronize system clock (client side) using *systemd*

### Configure NTP sources
NTP sources are defined in */etc/systemd/timesyncd.conf*
```ini
[Time]
# Primary NTP sources (space separated values)
NTP=be.pool.ntp.org time.google.com
# Fallback NTP sources
FallbackNTP=europe.pool.ntp.org ntp.ripe.net
```

### Enable/disable NTP synchronization
```
$ sudo timedatectl set-ntp true|false
```

### Stop/Start/Restart/status systemd *timesyncd* service
```
$ sudo service systemd-timesyncd stop|start|restart|status
```

## Configure Chrony as NTP client/server
chrony comes with two tools:
- chronyc: the NTP client (will replace base NTP client included with Ubuntu 20.04)
- chronyd: the NTP server daemon

### Install Chrony
Install required packages.
```
$ sudo apt install chrony
```

Verify chrony installation.
```
$ chronyc activity
```

### Configure Chrony
Chrony configuration file is */etc/chrony/chrony.conf*
```bash
# NTP sources
server 192.168.0.1                                  # Single NTP server 
pool be.pool.ntp.org        iburst maxsources 2     # Pool of NTP servers
pool europe.pool.ntp.org    iburst maxsources 1

# Key file for NTP authentication
keyfile /etc/chrony/chrony.keys

# File where chronyd will store drift informations
driftfile /var/lib/chrony/chrony.drift

# Turn on logging
log tracking measurements statistics

# Log files location
logdir /var/log/chrony

# Stop bad estimates upsetting machine clock
maxupdateskew 100.0

# Enable system real timeclock sync
rtcsync

# Steps the clock if diff > 1s only the forst 3 updates
# Stepping = change immediately >< Slewing = gradual change
makestep 1 3

# Defines which client can synch with the server
allow 192.168.0.0/24
allow 192.168.1.0/24
```

### Manage Chrony service
(Re)start/stop/reload/status Chrony
```
$ sudo service chrony start|restart|stop|reload|status
```

## Sources
- [NTP: The Network Time Protocol Official page](http://ntp.org)
- [ Network time Protocol - Wikipedia (en)](https://en.wikipedia.org/wiki/Network_Time_Protocol)
- [RFC5905 NTPv4 (ietf.org)](https://datatracker.ietf.org/doc/html/rfc5905)