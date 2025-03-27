# Systemd login services

This is a continuation exercise to highlight advanced possibilities of `systemd`.
Imagine we want to give each user a personal website folder in their `~/` directory but *only* active when they are logged into the machine.
The site would be accessed by going to `http://localhost/$USERNAME` so for me it would be `http://192.168.0.38/waldek`.
This website could give them stats, or just a hello message.
In order to to this we'll need a basic Debian machine with a webserver installed.
I would go for `nginx` but you can do `apache2` if you prefer.


## The webserver

```
➜  ~ sudo apt install nginx
Reading package lists... Done
Building dependency tree       
Reading state information... Done
nginx is already the newest version (1.14.2-2+deb10u4).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
➜  ~ 
```

This webserver only needs to offer these personal websites so we can go ahead and deactivate the default site.

```
➜  ~ ls /etc/nginx/sites-enabled/ -l
total 0
lrwxrwxrwx 1 root root 34 Aug 29 21:38 default -> /etc/nginx/sites-available/default
➜  ~ sudo rm /etc/nginx/sites-enabled/default 
➜  ~ ls /etc/nginx/sites-enabled/ -l         
total 0
➜  ~ 
```

We'll create a configuration file from scratch to host our user websites.
In `/etc/nginx/sites-available` you should create a `user-site.conf` file and put the following content in there.
It's a *super* basic configuration but it works!

```
server {
        listen 80 default_server;

        location ~ ^/(.+?)(/.*)?$ {
                alias /home/$1/site$2;
                index index.html index.htm;
                autoindex on;
        }
}
```

Now we symlink that file to the `/etc/nginx/sites-enabled` directory and we reload our webserver.
The advantage of reloading instead of restarting is that the webserver won't have any downtime.
On serious production servers this can be a handy feature.

```
➜  ~ sudo ln -s /etc/nginx/sites-available/user_site.conf /etc/nginx/sites-enabled
➜  ~ ls /etc/nginx/sites-enabled/ -l
total 0
lrwxrwxrwx 1 root root 41 Aug 29 21:43 user_site.conf -> /etc/nginx/sites-available/user_site.conf
➜  ~ sudo systemctl reload nginx.service 
```

We can test our website by using `wget` and showing the output on `STDOUT` with the following command.

```
➜  ~ wget -O - localhost/waldek
--2021-08-29 21:46:45--  http://localhost/waldek
Resolving localhost (localhost)... ::1, 127.0.0.1
Connecting to localhost (localhost)|::1|:80... connected.
HTTP request sent, awaiting response... 404 Not Found
2021-08-29 21:46:45 ERROR 404: Not Found.

➜  ~ 
```

The 404 error is because we don't *have* a personal website in our home folder so let's quickly create one and test again with `wget`.
This time around I'll add the `-q` argument to reduce the verbosity.

```
➜  ~ mkdir ~/site && echo "hello world" > ~/site/index.html
➜  ~ wget -q -O - localhost/waldek                         
hello world
➜  ~ 
```

## More users

Let's add a second user to our machine to test out our system.
We'll also need to add the site directory and test it all out.

```
➜  ~ sudo adduser alice                                                                     
➜  ~ sudo su alice                                                                     
alice@squid:/home/waldek$ cd && mkdir site && echo "this is Alice her website" > site/index.html
alice@squid:~$ cat site/index.html 
this is Alice her website
alice@squid:~$ exit
exit
➜  ~ wget -q -O - localhost/alice                                                      
this is Alice her website
➜  ~ 
```

It's working nicely as expected but all these users will have their website running permanently and we want them only available when they are logged in.
How would we go about that?
Let's have a dive into our running services.

```
➜  ~ sudo systemctl --type=service --no-pager
UNIT                               LOAD   ACTIVE SUB     DESCRIPTION                                                            
apparmor.service                   loaded active exited  Load AppArmor profiles                                                 
console-setup.service              loaded active exited  Set console font and keymap                                            
cron.service                       loaded active running Regular background program processing daemon                           
dbus.service                       loaded active running D-Bus System Message Bus                                               
getty@tty1.service                 loaded active running Getty on tty1                                                          
ifup@enp1s0.service                loaded active exited  ifup for enp1s0                                                        
ifupdown-pre.service               loaded active exited  Helper to synchronize boot up for ifupdown                             
keyboard-setup.service             loaded active exited  Set the console keyboard layout                                        
kmod-static-nodes.service          loaded active exited  Create list of required static device nodes for the current kernel     
networking.service                 loaded active exited  Raise network interfaces                                               
nginx.service                      loaded active running A high performance web server and a reverse proxy server               
ntopng.service                     loaded active running ntopng - High-Speed Web-based Traffic Analysis and Flow Collection Tool
redis-server.service               loaded active running Advanced key-value store                                               
rsyslog.service                    loaded active running System Logging Service                                                 
serial-getty@ttyS0.service         loaded active running Serial Getty on ttyS0                                                  
ssh.service                        loaded active running OpenBSD Secure Shell server                                            
systemd-journal-flush.service      loaded active exited  Flush Journal to Persistent Storage                                    
systemd-journald.service           loaded active running Journal Service                                                        
systemd-logind.service             loaded active running Login Service                                                          
systemd-modules-load.service       loaded active exited  Load Kernel Modules                                                    
systemd-random-seed.service        loaded active exited  Load/Save Random Seed                                                  
systemd-remount-fs.service         loaded active exited  Remount Root and Kernel File Systems                                   
systemd-sysctl.service             loaded active exited  Apply Kernel Variables                                                 
systemd-sysusers.service           loaded active exited  Create System Users                                                    
systemd-timesyncd.service          loaded active running Network Time Synchronization                                           
systemd-tmpfiles-setup-dev.service loaded active exited  Create Static Device Nodes in /dev                                     
systemd-tmpfiles-setup.service     loaded active exited  Create Volatile Files and Directories                                  
systemd-udev-trigger.service       loaded active exited  udev Coldplug all Devices                                              
systemd-udevd.service              loaded active running udev Kernel Device Manager                                             
systemd-update-utmp.service        loaded active exited  Update UTMP about System Boot/Shutdown                                 
systemd-user-sessions.service      loaded active exited  Permit User Sessions                                                   
user-runtime-dir@1000.service      loaded active exited  User Runtime Directory /run/user/1000                                  
user@1000.service                  loaded active running User Manager for UID 1000                                              

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.

33 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.
➜  ~ 
```

We're currently the only user logged in on this system.
This is verifiable with a few commands.
`waldek` is the only one logged in but over a few different connections, some running tmux, some not.

```
➜  ~ who
waldek   pts/0        2021-08-29 19:54 (192.168.0.33)
waldek   pts/1        2021-08-29 21:40 (tmux(1554).%4)
waldek   pts/2        2021-08-29 20:37 (tmux(1554).%0)
waldek   pts/3        2021-08-29 20:38 (tmux(1554).%1)
waldek   pts/4        2021-08-29 20:50 (tmux(1554).%2)
waldek   pts/5        2021-08-29 20:51 (tmux(1554).%3)
waldek   pts/6        2021-08-29 22:01 (192.168.0.33)
➜  ~ 
```

The first user account created on most Linux machine is the UID 1000.
We can use the `id` command to find out which UID is assigned to a specific user or vice a versa.

```
➜  ~ id -u -n 1000  
waldek
➜  ~ id -u alice  
1002
```

Now going back to the list of running service for our UID or just 'user' we get the following.

```
➜  ~ sudo systemctl --type=service --no-pager | grep 1000
user-runtime-dir@1000.service      loaded active exited  User Runtime Directory /run/user/1000                                  
user@1000.service                  loaded active running User Manager for UID 1000                                              
➜  ~ sudo systemctl --type=service --no-pager | grep user
systemd-sysusers.service           loaded active exited  Create System Users                                                    
systemd-user-sessions.service      loaded active exited  Permit User Sessions                                                   
user-runtime-dir@1000.service      loaded active exited  User Runtime Directory /run/user/1000                                  
user@1000.service                  loaded active running User Manager for UID 1000                                              
➜  ~ 
```

We've already made an `@.service` ourselves so we *know* it's a template that is instantiated multiple times.
Let's log in as `alice` and see what we get.

```
➜  ~ who                                                 
waldek   pts/0        2021-08-29 19:54 (192.168.0.33)
waldek   pts/1        2021-08-29 21:40 (tmux(1554).%4)
waldek   pts/2        2021-08-29 20:37 (tmux(1554).%0)
waldek   pts/3        2021-08-29 20:38 (tmux(1554).%1)
waldek   pts/4        2021-08-29 20:50 (tmux(1554).%2)
waldek   pts/5        2021-08-29 20:51 (tmux(1554).%3)
waldek   pts/6        2021-08-29 22:01 (192.168.0.33)
alice    pts/7        2021-08-29 22:12 (192.168.0.33)
➜  ~ sudo systemctl --type=service --no-pager | grep user
systemd-sysusers.service           loaded active exited  Create System Users                                                    
systemd-user-sessions.service      loaded active exited  Permit User Sessions                                                   
user-runtime-dir@1000.service      loaded active exited  User Runtime Directory /run/user/1000                                  
user-runtime-dir@1002.service      loaded active exited  User Runtime Directory /run/user/1002                                  
user@1000.service                  loaded active running User Manager for UID 1000                                              
user@1002.service                  loaded active running User Manager for UID 1002                                              
➜  ~ 
```

`who` tells us alice is definitely logged in and the list of running services shows a new **instance** of the `user@.service` running.
We can peak at the configuration file to learn more about this service.

```
➜  ~ sudo systemctl cat user@.service
# /usr/lib/systemd/system/user@.service
#  SPDX-License-Identifier: LGPL-2.1+
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

[Unit]
Description=User Manager for UID %i
Documentation=man:user@.service(5)
After=systemd-user-sessions.service user-runtime-dir@%i.service dbus.service
Requires=user-runtime-dir@%i.service
IgnoreOnIsolate=yes

[Service]
User=%i
PAMName=systemd-user
Type=notify
ExecStart=-/lib/systemd/systemd --user
Slice=user-%i.slice
KillMode=mixed
Delegate=pids memory
TasksMax=infinity
TimeoutStopSec=120s
➜  ~ 
```

This service is run whenever a user logs in and remains running until they log out.
If they log in multiple times, the service is not disturbed so it's a good point to attach our *actions* to.
But what will we do?
We'll need to write a custom service that starts and stops each individual website.
A script is probably the way to go but I can think of a different way as well.
We can try that afterwards.

## The script

The script needs to do two things.

* start the website
* stop the website

But it also needs to be modular because we'll want to reuse it for all users on the machine.
We know that we can pass information from the service to the script, like we did for the USB stick.
Starting and stopping is a bit out of place here, because we won't stop `nginx` itself.
We just need to remove the website or put a 'user is offline...' message in the `index.html` file.
One script that does multiple things screams **functions** and **case**!
Try to have a go a creating one from scratch!

<details>
  <summary>Spoiler warning</summary>

```
➜  ~ cat site-manager.sh 
#!/bin/bash

function start(){
	mkdir -p /home/$1/site && echo "created online site dir for $1"
	chown $1:$1 /home/$1/site/* && echo "chowned all site files to $1:$1"
	echo "$1 logged in..." > /home/$1/site/index.html && echo "online site installed for $1"
}

function stop(){
	mkdir -p /home/$1/.offline-site && echo "created offline site dir for $1"
	chown $1:$1 /home/$1/site/* && echo "chowned all site files to $1:$1"
	mv /home/$1/site/* /home/$1/.offline-site/ && echo "moved online site to offline site for $1"
	echo "$1 not logged in..." > /home/$1/site/index.html && echo "offline site installed for $1"
}

USER="$(id -u -n $2)"

case $1 in
	start)
		start $USER
		;;
	stop)
		stop $USER
		;;
	*)
		echo -n "NOP"
		;;
esac
➜  ~ 
```

</details>


If we try out this script, as `sudo` because we need to modify files owned by other users, we get the following.
It's a proof of concept but more than enough to continue with the service files.

```
➜  ~ sudo ./site-manager.sh start 1002
created online site dir for alice
chowned all site files to alice:alice
online site installed for alice
➜  ~ wget -q -O - localhost/alice     
alice logged in...
➜  ~ sudo ./site-manager.sh stop 1002 
created offline site dir for alice
chowned all site files to alice:alice
moved online site to offline site for alice
offline site installed for alice
➜  ~ wget -q -O - localhost/alice    
alice not logged in...
➜  ~ 
```

## The service

Now that we have a functional script, we can write a service file for it.
As we'll be using it for more than one user, we'll do a template.
You can name it whatever you want but I went for the following.

```
➜  ~ sudo systemctl cat user-website@.service
# /etc/systemd/system/user-website@.service
[Unit]
Description=User %i website service
PartOf=user@%i.service
After=systemd-user-sessions.service dbus.service

[Service]
Type=oneshot
RemainAfterExit=true
ExecStart=/home/waldek/site-manager.sh start %i
ExecStop=/home/waldek/site-manager.sh stop %i
➜  ~ 
```

There are a couple of new thing in this service file so let's break them down.
This time we specify the `Type` of service.
We can read the `man systemd.service` for more information but the gist of it is this.

```
•   Behavior of oneshot is similar to simple; however, the service manager will consider the unit started after the main
    process exits. It will then start follow-up units.  RemainAfterExit= is particularly useful for this type of
    service.  Type=oneshot is the implied default if neither Type= nor ExecStart= are specified.
```

The combination of `Type=oneshot` and `RemainAfterExit=true` make it so that the service is started and remains active even after the script has finished.
In order for the service to *stop* when the user logs out, we need the `PartOf` line.

```
PartOf=
    Configures dependencies similar to Requires=, but limited to stopping and restarting of units. When systemd stops or
    restarts the units listed here, the action is propagated to this unit. Note that this is a one-way dependency — changes
    to this unit do not affect the listed units.

    When PartOf=b.service is used on a.service, this dependency will show as ConsistsOf=a.service in property listing of
    b.service.  ConsistsOf= dependency cannot be specified directly.
```

We can test out this service, for our alice user, as follows.

```
➜  ~ sudo systemctl start user-website@1002.service
➜  ~ sudo journalctl --unit user-website@1002.service
-- Logs begin at Sun 2021-08-29 22:58:12 CEST, end at Sun 2021-08-29 23:00:53 CEST. --
Aug 29 23:00:25 squid systemd[1]: Starting User 1002 website service...
Aug 29 23:00:25 squid site-manager.sh[507]: created online site dir for alice
Aug 29 23:00:25 squid site-manager.sh[507]: chowned all site files to alice:alice
Aug 29 23:00:25 squid site-manager.sh[507]: online site installed for alice
Aug 29 23:00:25 squid systemd[1]: Started User 1002 website service.
➜  ~ sudo systemctl stop user-website@1002.service
➜  ~ sudo journalctl --unit user-website@1002.service
-- Logs begin at Sun 2021-08-29 22:58:12 CEST, end at Sun 2021-08-29 23:01:09 CEST. --
Aug 29 23:00:25 squid systemd[1]: Starting User 1002 website service...
Aug 29 23:00:25 squid site-manager.sh[507]: created online site dir for alice
Aug 29 23:00:25 squid site-manager.sh[507]: chowned all site files to alice:alice
Aug 29 23:00:25 squid site-manager.sh[507]: online site installed for alice
Aug 29 23:00:25 squid systemd[1]: Started User 1002 website service.
Aug 29 23:01:06 squid systemd[1]: Stopping User 1002 website service...
Aug 29 23:01:06 squid site-manager.sh[529]: created offline site dir for alice
Aug 29 23:01:06 squid site-manager.sh[529]: chowned all site files to alice:alice
Aug 29 23:01:06 squid site-manager.sh[529]: moved online site to offline site for alice
Aug 29 23:01:06 squid site-manager.sh[529]: offline site installed for alice
Aug 29 23:01:06 squid systemd[1]: user-website@1002.service: Succeeded.
Aug 29 23:01:06 squid systemd[1]: Stopped User 1002 website service.
➜  ~ 
```

Now the service works as expected but does it actually trigger when users log in?
Let's investigate!
When alice is logged in over SSH we get the following active services.

```
➜  ~ sudo systemctl --type=service --no-pager | grep user
systemd-sysusers.service           loaded active exited  Create System Users                                               
systemd-user-sessions.service      loaded active exited  Permit User Sessions                                              
user-runtime-dir@1000.service      loaded active exited  User Runtime Directory /run/user/1000                             
user-runtime-dir@1002.service      loaded active exited  User Runtime Directory /run/user/1002                             
user@1000.service                  loaded active running User Manager for UID 1000                                         
user@1002.service                  loaded active running User Manager for UID 1002                                         
➜  ~ 
```

It does not seem to works, let's try starting the service to see if it *actually* lists itself.
 
```
➜  ~ sudo systemctl --type=service --no-pager | grep user
systemd-sysusers.service           loaded active exited  Create System Users                                               
systemd-user-sessions.service      loaded active exited  Permit User Sessions                                              
user-runtime-dir@1000.service      loaded active exited  User Runtime Directory /run/user/1000                             
user-runtime-dir@1002.service      loaded active exited  User Runtime Directory /run/user/1002                             
user-website@1002.service          loaded active exited  User 1002 website service                                         
user@1000.service                  loaded active running User Manager for UID 1000                                         
user@1002.service                  loaded active running User Manager for UID 1002                                         
➜  ~ 
```

It does list itself as active, thanks to the `RemainAfterExit` setting but how do we link our template service to the `user@.service` template?

## Overriding service files

Our `PartOf` setting links the shutdown of our service.
We can try this by logging alice back out.
The `user-website@1002.service` will stop but if we log back in it won't be started again!

```
➜  ~ sudo systemctl --type=service --no-pager | grep user
systemd-sysusers.service           loaded active exited  Create System Users                                               
systemd-user-sessions.service      loaded active exited  Permit User Sessions                                              
user-runtime-dir@1000.service      loaded active exited  User Runtime Directory /run/user/1000                             
user@1000.service                  loaded active running User Manager for UID 1000                                         
➜  ~ 
```

In order to have the service start we need to attach it to the `user@.service file`.
Up until now we made our changes into the actual file but we can be smarter that that!
The service files supplied by Debian are very good and if they would make changes to them it would destroy *our* changes after an update.
To mitigate this we've been user `service.d/` directories and systemd has the same on an individual service level.
You can create the structure by hand but the *easiest* way is to use the built in `edit` subcommand to `systemctl`.
By invoking `sudo systemctl edit user@.service` your favorite text editor will open up with a blank file.
Here we'll add our additions to.

```
[Unit]
Requires=user-website@%i.service
```

We simply state that `user@.service` requires `user-website@.service` to start as well.
If we now inspect the service file of `user@.service` we see it sources it's configuration form **two** places.
One is the default `/usr/lib/systemd/system/user@.service`, which can be modified by upstream changes, the other one is in our classic `/etc/systemd/system/user@.service.d/override.conf` path.

```
➜  ~ sudo systemctl cat user@.service
# /usr/lib/systemd/system/user@.service
#  SPDX-License-Identifier: LGPL-2.1+
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

[Unit]
Description=User Manager for UID %i
Documentation=man:user@.service(5)
After=systemd-user-sessions.service user-runtime-dir@%i.service dbus.service
Requires=user-runtime-dir@%i.service
IgnoreOnIsolate=yes

[Service]
User=%i
PAMName=systemd-user
Type=notify
ExecStart=-/lib/systemd/systemd --user
Slice=user-%i.slice
KillMode=mixed
Delegate=pids memory
TasksMax=infinity
TimeoutStopSec=120s

# /etc/systemd/system/user@.service.d/override.conf
[Unit]
Requires=user-website@%i.service
➜  ~ 
```

## An alternative approach

You can achieve similar results in multiple ways.
Without much scripting you can try to chain the following concepts together.

* `nginx` sites-available
* symbolic links to `nginx` sites-enabled
* `nginx` location, include and wildcards
* `systemctl reload`
