# Systemd

## What is systemd?

Systemd is a collection of programs that aim to unify the service configuration and behavior on *most* modern Linux distributions.
All of the distributions we've used up until now come with systemd and we've been manipulating most of our servers and services via `systemctl` which is the standard command line interface to systemd.
It's worth pointing out that systemd is not just an additional piece of software that is added to your computer.
You should see it as a sort of *glue* that ties the system together as it's responsible for launching and monitoring all services you run on your server.

### Some history

As with most things Linux there are multiple alternatives to systemd and believe it or not, the introduction (around 2015) of systemd to Debian was a controversial moment.
A lot of online debates were had to discuss the pro's and cons and Debian was even [forked](https://www.devuan.org/) to remove systemd all together.

> Devuan GNU+Linux is a fork of Debian without systemd that allows users to reclaim control over their system by avoiding unnecessary entanglements and ensuring Init Freedom.

You can be for or against systemd but the current reality is that it *is* the most widely used `init` system around today.
This can, and probably will, change in the future but for now the world is run by systemd.

## The basics

During the numerous hours you've spent using `htop` you have probably noticed the first process is often `/lib/systemd/systemd --system` on Debian machines.
On Raspberry Pi's that first process is most likely `/sbin/init` but a closer look at this program shows the following.

```
pi@camone:~ $ pgrep -a systemd
1 /sbin/init
122 /lib/systemd/systemd-journald
150 /lib/systemd/systemd-udevd
295 /lib/systemd/systemd-timesyncd
378 /lib/systemd/systemd-logind
16414 /lib/systemd/systemd --user
pi@camone:~ $ which /sbin/init
/sbin/init
pi@camone:~ $ ls -l /sbin/init
lrwxrwxrwx 1 root root 20 Apr  1 14:57 /sbin/init -> /lib/systemd/systemd
pi@camone:~ $ 
```

Every running Linux computer must have a **first** process.
But where does this first process come from?
Below you can see a nice graph of the **boot sequence** of a standard Linux machine (taken from the [Debian system administrator handbook](https://debian-handbook.info/browse/stable/unix-services.html#sect.system-boot)).

![startup sequence](./assets/systemd_sequence.png)

By default the Linux kernel will run the `init` program but this can be overridden by passing an argument to the kernel upon boot.
For those who have played around with the [broken machines](./exercise_broken_machines.md) this is probably no real news.
At the last stage of the boot sequence, systemd takes over and launches all services that are `enabled` for the requested `runlevel`.
The runlevel might be new to you but we'll come back to that in a minute.

### Interfacing with systemd

Your main tool to *talk* to systemd is `systemctl`.
It's sort of a **client** to the systemd **server**.
The most used commands, that you probably know by hearth, are:

```
sudo systemctl start sshd.service
sudo systemctl stop sshd.service
sudo systemctl restart sshd.service
sudo systemctl status sshd.service
sudo systemctl enable sshd.service
sudo systemctl disable sshd.service
```

Just knowing these will get you a long way but there are a few more handy commands to push it all a bit further.

## Beyond the basics

### A deeper look into what's available

If you invoke just `sudo systemctl` it lists all the units that are active.
It's actually a shortcut to `sudo systemctl list-units`.
You'll be confronted with an interface, `less`, that you know pretty well so have a look around and maybe search for some keywords.

At the bottom of the pager you'll see a few hints that point you to other commands that show even more output.
When we disable a server such as `sshd` it's configuration files are not changed at all as the server never tries to start itself.
Systemd is responsible for that so if we want to see all servers available on our system we type `sudo systemctl list-unit-files` which gives a clear table, also via `less`, that outlines the current state and vendor state.

We can add more command line arguments to `systemctl` to narrow down the output a bit.
A handy one is `--type service` to only see services.
I advise you to have a read of the `man systemctl` to grasp the full scope of it's capabilities.

### Inspecting a running service

To inspect a running service we can run `sudo systemctl status sshd.service`.
This gives us the following output:

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2021-07-26 12:14:35 CEST; 2 weeks 6 days ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 576 (sshd)
      Tasks: 1 (limit: 23851)
     Memory: 2.8M
        CPU: 112ms
     CGroup: /system.slice/ssh.service
             └─576 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups

Jul 26 12:14:35 deathstar systemd[1]: Starting OpenBSD Secure Shell server...
Jul 26 12:14:35 deathstar sshd[576]: Server listening on 0.0.0.0 port 22.
Jul 26 12:14:35 deathstar sshd[576]: Server listening on :: port 22.
Jul 26 12:14:35 deathstar systemd[1]: Started OpenBSD Secure Shell server.
Jul 28 20:13:38 deathstar sshd[175321]: Connection closed by authenticating user waldek 192.168.0.222 port 51542 [preauth]
Aug 14 09:05:36 deathstar sshd[1001518]: Connection closed by authenticating user waldek 192.168.0.33 port 35448 [preauth]
Aug 14 09:05:56 deathstar sshd[1001567]: Connection closed by authenticating user waldek 192.168.0.33 port 35636 [preauth]
Aug 14 09:06:20 deathstar sshd[1001648]: Connection closed by authenticating user waldek 192.168.0.236 port 53346 [preauth]
```

There is quite a bit of interesting information here.
There are two **blocks** of information.
At the top we see some details and links to the help about the service in question and at the bottom we see the last eight lines of the server logs.
To see *how* systemd has the sshd service configured we need to have a look at the second line, the one that sais `Loaded:`.
The path that follows is the service file that systemd uses to know **how**, **when** and **where** to run the service.
As with most things Linux this is a simple text file we can open up with `less`, `vim` or even `nano` but there is a sweet shortcut supplied by systemd itself!

```
➜  ~ git:(master) ✗ sudo systemctl cat sshd.service
# /lib/systemd/system/ssh.service
[Unit]
Description=OpenBSD Secure Shell server
Documentation=man:sshd(8) man:sshd_config(5)
After=network.target auditd.service
ConditionPathExists=!/etc/ssh/sshd_not_to_be_run

[Service]
EnvironmentFile=-/etc/default/ssh
ExecStartPre=/usr/sbin/sshd -t
ExecStart=/usr/sbin/sshd -D $SSHD_OPTS
ExecReload=/usr/sbin/sshd -t
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartPreventExitStatus=255
Type=notify
RuntimeDirectory=sshd
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target
Alias=sshd.service
➜  ~ git:(master) ✗ 
```

### Modifying a service

What can we do with these unit files you might ask?
Well, we can have a look at the command line arguments for sshd with `man sshd`.
This gives us an overview of all options available to us.
One that peaks my interest is the `-p` argument which allows us to override the port and ignore all ports specified in the configuration file.
Let's try it out!

To edit the unit file we need a text editor.
There are *two* ways to do it but we'll go for the most straightforward one first.
I'll be using vim to edit the file via `sudo vim /lib/systemd/system/ssh.service`.
Notice the syntax highlighting, nice no?
I modified the tenth line so that it reads:

```
ExecStart=/usr/sbin/sshd -D $SSHD_OPTS -p 2222

```

Now, how do we take this change into account?
Let's restart the service.

```
  ~ git:(master) ✗ sudo systemctl restart sshd.service 
Warning: The unit file, source configuration file or drop-ins of sshd.service changed on disk. Run 'systemctl daemon-reload' to reload units.
➜  ~ git:(master) ✗ 
```

We can see a warning but did the service restart?
Let's have a look at the status.

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2021-08-15 20:00:49 CEST; 38s ago
       Docs: man:sshd(8)
             man:sshd_config(5)
    Process: 1108166 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
   Main PID: 1108167 (sshd)
      Tasks: 1 (limit: 23851)
     Memory: 1.1M
        CPU: 15ms
     CGroup: /system.slice/ssh.service
             └─1108167 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups

Aug 15 20:00:49 deathstar systemd[1]: Starting OpenBSD Secure Shell server...
Aug 15 20:00:49 deathstar sshd[1108167]: Server listening on 0.0.0.0 port 22.
Aug 15 20:00:49 deathstar sshd[1108167]: Server listening on :: port 22.
Aug 15 20:00:49 deathstar systemd[1]: Started OpenBSD Secure Shell server.
```

Yes it did, but the service is still running on port 22.
This is what systemd means by `loaded`.
A configuration file is loaded into memory and used from there.
To take changes to unit files into account we need to reload the files that have changed, sort of like we restart `sshd` when we make changes to it's configuration file but we can't restart `systemd` as that would freeze our computer.
Luckily there is a command to do this and it's written in the warning notice.

```
➜  ~ git:(master) ✗ sudo systemctl daemon-reload      
➜  ~ git:(master) ✗ sudo systemctl restart sshd.service
➜  ~ git:(master) ✗ sudo systemctl status sshd.service 
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2021-08-15 20:05:53 CEST; 2s ago
       Docs: man:sshd(8)
             man:sshd_config(5)
    Process: 1108694 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
   Main PID: 1108695 (sshd)
      Tasks: 1 (limit: 23851)
     Memory: 1.1M
        CPU: 15ms
     CGroup: /system.slice/ssh.service
             └─1108695 sshd: /usr/sbin/sshd -D -p 2222 [listener] 0 of 10-100 startups

Aug 15 20:05:53 deathstar systemd[1]: Starting OpenBSD Secure Shell server...
Aug 15 20:05:53 deathstar sshd[1108695]: Server listening on 0.0.0.0 port 2222.
Aug 15 20:05:53 deathstar sshd[1108695]: Server listening on :: port 2222.
Aug 15 20:05:53 deathstar systemd[1]: Started OpenBSD Secure Shell server.
➜  ~ git:(master) ✗
```

Nice!
Now, let's first undo our changes and explore the alternative way to modify unit files.
Next we do the same changes but in the alternative way.
Just as we have a handy shortcut to `cat` unit files we have one to `edit` them!
I'll run the `sudo -E systemctl edit --full sshd.service` command, notice the `-E`, why would I do that?
This opens up my editor of choice and I can go ahead an make my changes to line 10 which I add `-p 2200` to this time.

```
➜  ~ git:(master) ✗ sudo -E systemctl edit sshd.service --full
➜  ~ git:(master) ✗ sudo systemctl daemon-reload          
➜  ~ git:(master) ✗ sudo systemctl restart sshd.service    
➜  ~ git:(master) ✗ sudo systemctl status sshd.service     
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/etc/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2021-08-15 20:24:47 CEST; 4s ago
       Docs: man:sshd(8)
             man:sshd_config(5)
    Process: 1111232 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
   Main PID: 1111233 (sshd)
      Tasks: 1 (limit: 23851)
     Memory: 1.1M
        CPU: 15ms
     CGroup: /system.slice/ssh.service
             └─1111233 sshd: /usr/sbin/sshd -D -p 2200 [listener] 0 of 10-100 startups

Aug 15 20:24:47 deathstar systemd[1]: Starting OpenBSD Secure Shell server...
Aug 15 20:24:47 deathstar sshd[1111233]: Server listening on 0.0.0.0 port 2200.
Aug 15 20:24:47 deathstar sshd[1111233]: Server listening on :: port 2200.
Aug 15 20:24:47 deathstar systemd[1]: Started OpenBSD Secure Shell server.
➜  ~ git:(master) ✗ 
```

Notice something different here?
The location of the unit file is no longer `/lib/systemd/system/ssh.service` but `/etc/systemd/system/ssh.service`.
This is the actual *preferred* way of modifying unit files supplied by your distribution because if at some point in the future your distro changes it's configuration file and you update, you'll overwrite your custom changes! (see [this](https://serverfault.com/questions/840996/modify-systemd-unit-file-without-altering-upstream-unit-file) post on serverfault)
Think of the similar situation we encountered with `/etc/dnsmask.d/` when installing a pihole.
What if you want to `revert` back to file supplied by Debian?
A quick `sudo systemctl revert sshd.service` should do the trick!
Don't forget to `daemon-reload` when you want to restart the service.

## Writing your own service files

Imagine we want to run a custom server each time the machine boots.
Here systemd comes to the rescue, plus we can run them as *ourselves* and don't need to interfere with the standard system services.
Let's give this a go!

A simple example to a server would be a small python3 webserver.
Let's create a directory in our home called website.
We can do this with `mkdir ~/website`.
In this folder we'll make an `index.html` file where we add the content of our *website* to.
You can write anything you want, in html or plaintext.
To spin up a quick webserver we can use the `http.server` class from the standard library.
I **must** note that it's not a production proof server and should **only** be used for small testing purposes (and for our example).

```
➜  website git:(master) ✗ python3 -m http.server 8080
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
127.0.0.1 - - [15/Aug/2021 20:45:30] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [15/Aug/2021 20:45:30] code 404, message File not found
127.0.0.1 - - [15/Aug/2021 20:45:30] "GET /favicon.ico HTTP/1.1" 404 -
```

The website is now up and running and we can see all requests logged to the command line.
Go to `http://localhost:8080` to see your website, or to the IP address	of one of the other students to see the logs grow.

Right, we're happy with our service and we would like to offer it permanently.
In order to do so we need to create our own unit file and we can do this in **two locations**.
The first one is `/etc/systemd/system/` which houses most of our system services but **users** can have their own services!
In order to create your own service, without root privileges, you can add unit files to `~/.local/share/systemd/user`.
You will probably have to create this directory.
In this directory you can add as many `.service` files as you want.
For now we'll just make one called `website.service` where we need to define some things in.

```
[Unit]
Description=Our own webserver

[Service]
WorkingDirectory=/home/waldek/website
ExecStart=/usr/bin/python3 -m http.server 8080

[Install]
WantedBy=default.target
```

Next we need to `enable` and `start` our service.
Notice that I'm not using `sudo` and that I added the `--user` argument.

```
systemctl --user enable website.service
systemctl --user start website.service
```

And we can inspect the logs via the trusted `status` argument as such.

```
➜  ~ git:(master) ✗ systemctl --user status website.service
● website.service - Our own webserver
     Loaded: loaded (/home/waldek/.local/share/systemd/user/website.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2021-08-15 20:58:15 CEST; 5min ago
   Main PID: 1114451 (python3)
      Tasks: 1 (limit: 23851)
     Memory: 8.8M
        CPU: 92ms
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/website.service
             └─1114451 /usr/bin/python3 -m http.server 8080

Aug 15 20:58:15 deathstar systemd[585]: Started Our own webserver.
Aug 15 20:58:23 deathstar python3[1114451]: 127.0.0.1 - - [15/Aug/2021 20:58:23] "GET / HTTP/1.1" 304 -
Aug 15 20:58:24 deathstar python3[1114451]: 127.0.0.1 - - [15/Aug/2021 20:58:24] "GET / HTTP/1.1" 304 -
Aug 15 20:58:24 deathstar python3[1114451]: 127.0.0.1 - - [15/Aug/2021 20:58:24] "GET / HTTP/1.1" 304 -
Aug 15 20:58:25 deathstar python3[1114451]: 127.0.0.1 - - [15/Aug/2021 20:58:25] "GET / HTTP/1.1" 304 -
➜  ~ git:(master) ✗ 
```

For those that want to dive deeper into the syntax of the configuration file you should have a look at the output of `systemctl --user show website.service` which list all of the *hidden* settings that are predefined for a service.
To see what you can change them to, have a look [here](https://www.freedesktop.org/software/systemd/man/systemd.service.html).

### Deep dive into the logs

All logs made you systemd go into the `/var/log/daemon.log` file by default.
You can override this but I would highly advise you not to do it as there are special **tools** that come with systemd to inspect the logs, plus all logs in one place is quite handy for grepping.
Have a look at the file and you should see a similar output.

```
Aug 15 20:24:44 deathstar systemd[1]: Reloading.
Aug 15 20:24:47 deathstar systemd[1]: Stopping OpenBSD Secure Shell server...
Aug 15 20:24:47 deathstar systemd[1]: ssh.service: Succeeded.
Aug 15 20:24:47 deathstar systemd[1]: Stopped OpenBSD Secure Shell server.
Aug 15 20:24:47 deathstar systemd[1]: Starting OpenBSD Secure Shell server...
Aug 15 20:24:47 deathstar systemd[1]: Started OpenBSD Secure Shell server.
Aug 15 20:57:38 deathstar systemd[585]: Started VTE child process 1114299 launched by gnome-terminal-server process 1027574.
Aug 15 20:58:02 deathstar systemd[585]: Reloading.
Aug 15 20:58:15 deathstar systemd[585]: Started Our own webserver.
Aug 15 20:58:23 deathstar python3[1114451]: 127.0.0.1 - - [15/Aug/2021 20:58:23] "GET / HTTP/1.1" 304 -
Aug 15 20:58:24 deathstar python3[1114451]: 127.0.0.1 - - [15/Aug/2021 20:58:24] "GET / HTTP/1.1" 304 -
Aug 15 20:58:24 deathstar python3[1114451]: 127.0.0.1 - - [15/Aug/2021 20:58:24] "GET / HTTP/1.1" 304 -
Aug 15 20:58:25 deathstar python3[1114451]: 127.0.0.1 - - [15/Aug/2021 20:58:25] "GET / HTTP/1.1" 304 -
```

Systemd comes with a specialized program to sift through it's logs called `journalctl`.
Just invoking `journalctl` will give you the output of the log file in less.
A **very handy** argument you'll probably always use is `-e` which scrolls to the end of the logs.
As an alternative you can add `--no-pager` which will not pipe to `less` but just print to STDOUT.
To only view a specific service we can add the `--unit` argument, followed by the service name.
For example:

```
➜  ~ git:(master) ✗ sudo journalctl --unit ssh.service --no-pager --since "1 h 25 min ago"
-- Journal begins at Wed 2021-07-14 22:35:36 CEST, ends at Sun 2021-08-15 21:46:42 CEST. --
Aug 15 20:22:14 deathstar sshd[1110635]: Received signal 15; terminating.
Aug 15 20:22:14 deathstar systemd[1]: Stopping OpenBSD Secure Shell server...
Aug 15 20:22:14 deathstar systemd[1]: ssh.service: Succeeded.
Aug 15 20:22:14 deathstar systemd[1]: Stopped OpenBSD Secure Shell server.
Aug 15 20:22:14 deathstar systemd[1]: Starting OpenBSD Secure Shell server...
Aug 15 20:22:14 deathstar sshd[1110849]: Server listening on 0.0.0.0 port 2222.
Aug 15 20:22:14 deathstar sshd[1110849]: Server listening on :: port 2222.
Aug 15 20:22:14 deathstar systemd[1]: Started OpenBSD Secure Shell server.
Aug 15 20:24:47 deathstar systemd[1]: Stopping OpenBSD Secure Shell server...
Aug 15 20:24:47 deathstar sshd[1110849]: Received signal 15; terminating.
Aug 15 20:24:47 deathstar systemd[1]: ssh.service: Succeeded.
Aug 15 20:24:47 deathstar systemd[1]: Stopped OpenBSD Secure Shell server.
Aug 15 20:24:47 deathstar systemd[1]: Starting OpenBSD Secure Shell server...
Aug 15 20:24:47 deathstar sshd[1111233]: Server listening on 0.0.0.0 port 2200.
Aug 15 20:24:47 deathstar sshd[1111233]: Server listening on :: port 2200.
Aug 15 20:24:47 deathstar systemd[1]: Started OpenBSD Secure Shell server.
➜  ~ git:(master) ✗ 
```

To understand the `--since` argument I advise you to read the `man systemd.time` pages.
An argument you'll often see suggested online is `-x`.
It adds more verbose output to debug issues.
The manpage documentation is below for reference purpose for reference purposes.

```
-x, --catalog
    Augment log lines with explanation texts from the message catalog. This will add explanatory help texts to log messages
    in the output where this is available. These short help texts will explain the context of an error or log event,
    possible solutions, as well as pointers to support forums, developer documentation, and any other relevant manuals. Note
    that help texts are not available for all messages, but only for selected ones. For more information on the message
    catalog, please refer to the Message Catalog Developer Documentation[5].

    Note: when attaching journalctl output to bug reports, please do not use -x.
```

Last but not least, the `-f` argument does a *live* stream of the log so you can debug on the fly.
This can be very handy in a `tmux` session.
For more information I highly advise the man pages with `man journalctl`!

## A sidetrack into cron

But what if we want to run a quick script or command every day at midnight?
Like an email report of the system status, or a `apt update`?
This can also be done with systemd but the *classic* way of doing this is via `cron`.
As always, have a look at `man cron` and when you're finished you'll know you want to read the `man crontab` as well.

In short, every user can have a crontab which is a list of command to execute at certain intervals.
To inspect your own crontab, just execute `crontab -e` which will open your editor of choice.
Read through the comments, it's quite self explanatory no?
Only the timestamp syntax is quite annoying in my opinion but there is a handy [website](https://crontab.guru/every-1-minute) to help you understand it a bit better.
To have a command executed every minute you add the following.

```
* * * * * echo "helloword" >> /tmp/coucou
```

The `root` user has his own crontab you can edit with `sudo crontab -e`
To do an `apt update` every day at midnight you would add the following.

```
0 0 * * * apt update
```

I must note that this is not really the best way to accomplish automatic update and upgrades.
Have a look [here](https://help.ubuntu.com/community/AutoWeeklyUpdateHowTo) for better alternatives.

## Systemd timers

As you can probably see, `cron` is a very basic but powerful way of scheduling actions.
So people really like the simplicity bit for others a bit more control is desired, hence `man systemd.timer`.
We can list all current timers with the following command.

```
➜  ~ git:(master) ✗ systemctl list-timers --no-pager
NEXT                       LEFT          LAST                       PASSED       UNIT                       ACTIVATES
Mon 2021-08-16 00:00:00 C… 1h 40min left Sun 2021-08-15 00:00:13 C… 22h ago      logrotate.timer            logrotate.service
Mon 2021-08-16 00:00:00 C… 1h 40min left Sun 2021-08-15 00:00:13 C… 22h ago      man-db.timer               man-db.service
Mon 2021-08-16 06:52:37 C… 8h left       Sun 2021-08-15 06:34:23 C… 15h ago      apt-daily-upgrade.timer    apt-daily-upgrade.service
Mon 2021-08-16 12:45:13 C… 14h left      Sun 2021-08-15 12:45:13 C… 9h ago       systemd-tmpfiles-clean.ti… systemd-tmpfiles-clean.ser…
Mon 2021-08-16 12:46:51 C… 14h left      Sun 2021-08-15 19:56:29 C… 2h 23min ago apt-daily.timer            apt-daily.service
Sun 2021-08-22 03:10:26 C… 6 days left   Sun 2021-08-15 03:10:52 C… 19h ago      e2scrub_all.timer          e2scrub_all.service

6 timers listed.
Pass --all to see loaded but inactive timers, too.
➜  ~ git:(master) ✗ 
```

To list your own timers you add the `--user` argument.

```
➜  ~ git:(master) ✗ systemctl --user list-timers --no-pager
NEXT LEFT LAST PASSED UNIT ACTIVATES

0 timers listed.
Pass --all to see loaded but inactive timers, too.
➜  ~ git:(master) ✗ 
```

Let's add one!
In order to create a timer, we need a service that we can run so let's do that first.
In the same folder as before I'll create a `monitor.service` file and will add the following to it.

```
➜  user git:(master) ✗ systemctl --user cat monitor.service
# /home/waldek/.local/share/systemd/user/monitor.service
[Unit]
Description=Doing some monitoring
Wants=monitor.timer

[Service]
Type=oneshot
ExecStart=/usr/bin/ps u

[Install]
WantedBy=multi-user.target
➜  user git:(master) ✗ 
```

Now, let's test the service.

```
➜  user git:(master) ✗ systemctl --user start monitor.service 
➜  user git:(master) ✗ systemctl --user status monitor.service
● monitor.service - Doing some monitoring
     Loaded: loaded (/home/waldek/.local/share/systemd/user/monitor.service; disabled; vendor preset: enabled)
     Active: inactive (dead)

Aug 15 22:29:08 deathstar ps[1122931]: waldek   1099261  0.0  0.0  16300  9880 pts/2    Ss   17:54   0:00 zsh
Aug 15 22:29:08 deathstar ps[1122931]: waldek   1101477  0.0  0.0  17468 11496 pts/3    Ss   18:31   0:06 zsh
Aug 15 22:29:08 deathstar ps[1122931]: waldek   1117521  0.0  0.0  16744 10068 pts/4    Ss   21:38   0:01 zsh
Aug 15 22:29:08 deathstar ps[1122931]: waldek   1118424  0.0  0.0  17120 10052 pts/5    Ss+  21:44   0:00 zsh
Aug 15 22:29:08 deathstar ps[1122931]: waldek   1119048  0.0  0.0  40788  7956 pts/4    S+   21:50   0:00 journalctl -f
Aug 15 22:29:08 deathstar ps[1122931]: waldek   1121204  1.9  0.1  45280 31108 pts/2    S+   22:11   0:20 vim learning_systemd.md
Aug 15 22:29:08 deathstar ps[1122931]: waldek   1122718  0.2  0.0  12848  8716 pts/6    Ss+  22:27   0:00 zsh
Aug 15 22:29:08 deathstar ps[1122931]: waldek   1122930  0.0  0.0  10072  1168 pts/3    S+   22:29   0:00 systemctl --user start monit>
Aug 15 22:29:08 deathstar systemd[585]: monitor.service: Succeeded.
Aug 15 22:29:08 deathstar systemd[585]: Finished Doing some monitoring.
```

OK, that seems to work well, so now we want to create the timer that will run this service every minute.
In order to do this we create a `monitor.timer` file with the following content.
The `onCalendar=*-*-* *:*:00` make it run every minute.
You can read more about the syntax in the `man systemd.time` pages.

```
➜  user git:(master) ✗ systemctl --user cat monitor.timer  
# /home/waldek/.local/share/systemd/user/monitor.timer
[Unit]
Description=Doing some timely monitoring
Requires=monitor.service

[Timer]
Unit=monitor.service
OnCalendar=*-*-* *:*:00

[Install]
WantedBy=timers.target
➜  user git:(master) ✗ 
```

Once the timer is in place you should `start` the service with `systemctl --user start monitor.service`.
There is no need to start or enable the `monitor.timer` file as the link between them is in the `monitor.service` file via the `Wants=monitor.timer` configuration line.
If you now watch your log in real time with `journalctl -f --user-unit monitor.service` you should see your service executing every minute!

### Pro's and cons

The following advice was taken from the arch [wiki](https://wiki.archlinux.org/title/Systemd/Timers).

#### As a cron replacement

Although cron is arguably the most well-known job scheduler, systemd timers can be an alternative.

##### Benefits

The main benefits of using timers come from each job having its own systemd service. Some of these benefits are:

* Jobs can be easily started independently of their timers. This simplifies debugging.
* Each job can be configured to run in a specific environment (see systemd.exec(5)).
* Jobs can be attached to cgroups.
* Jobs can be set up to depend on other systemd units.
* Jobs are logged in the systemd journal for easy debugging.

##### Caveats

Some things that are easy to do with cron are difficult to do with timer units alone:

* Creation: to set up a timed job with systemd you need to create two files and run systemctl commands, compared to adding a single line to a crontab.
* Emails: there is no built-in equivalent to cron's MAILTO for sending emails on job failure. See the next section for an example of setting up a similar functionality using OnFailure=.

Also note that user timer units will only run during an active user login session by default. However, lingering can enable services to run at boot even when the user has no active login session.

## A sidetrack into runlevels

The world of Linux has a concept called *runlevels* which determines a target state the machine is in, or to which you want the manche to go to.
It's a complicated way of saying fully operational with graphical interface, a root only rescue mode, a reboot, halted etc.
The official specification of the runlevels defines them as such.

* Runlevel 0 or Halt is used to shift the computer from one state to another. It shut down the system.
* Runlevel 1, s, S or Single-User Mode is used for administrative and recovery functions. It has only enough daemons to allow one user (the root user) to log in and perform system maintenance tasks. All local file systems are mounted. Some essential services are started, but networking remains disabled.
* Runlevel 2 or Multi-user Mode is used for most daemons running and allows multiple users the ability to log in and use system services but without networking. On Debian and its derivatives, a full multi-user mode with X running and a graphical login. Most other distributions leave this runlevel undefined.
* Runlevel 3 or Extended Multi-user Mode is used for a full multi-user mode with a console (without GUI) login screen with network services available
* Runlevel 4 is not normally used and undefined so it can be used for a personal customization
* Runlevel 5 or Graphical Mode is same as Runlevel 3 with graphical login _(such as GDN)_.
* Runlevel 6 or Reboot is a transitional runlevel to reboot the system.

You can inspect the runlevel your system is currenty at by ececuting the following command.

```
➜  ~ git:(master) ✗ sudo runlevel
N 5
➜  ~ git:(master) ✗ 
```

You can change your runlevel with the `sudo telinit`, followed by the level number, command.
You'll probably won't see that much difference between levels but try to change it to level `6` and see what happens.
If you change the runlevel to `1` your machine will probably freeze.
This has to do with the fact we haven't set a `root` password on most of our machines so the single user mode can't be accessed.
Try setting a root password and reset the level to one and see what happens.

## Systemd targets

Systemd take the concept of runlevels a bit further and they are renamed to **targets**.
The mapping of runlevels to targets is as follows.

* poweroff.target (runlevel 0): shutdown and power off the system
* rescue.target (runlevel 1): launch the rescue shell session
* multi-user.target (runlevel 2,3,4): set the system in non graphical (console) multi-user system
* graphical.target (runlevel 5): use a graphical multi-user system with network services
* reboot.target (runlevel 6): shutdown and reboot the system

But, there are a *lot* more targets available on a machine running systemd.
Luckily `systemctl` offers a nice way to inspect them.

```
➜  ~ git:(master) ✗ sudo systemctl list-units --type target
  UNIT                 LOAD   ACTIVE SUB    DESCRIPTION
  basic.target         loaded active active Basic System
  cryptsetup.target    loaded active active Local Encrypted Volumes
  getty.target         loaded active active Login Prompts
  local-fs-pre.target  loaded active active Local File Systems (Pre)
  local-fs.target      loaded active active Local File Systems
  multi-user.target    loaded active active Multi-User System
  network.target       loaded active active Network
  nfs-client.target    loaded active active NFS client services
  paths.target         loaded active active Paths
  remote-fs-pre.target loaded active active Remote File Systems (Pre)
  remote-fs.target     loaded active active Remote File Systems
  rpcbind.target       loaded active active RPC Port Mapper
  slices.target        loaded active active Slices
  sockets.target       loaded active active Sockets
  swap.target          loaded active active Swap
  sysinit.target       loaded active active System Initialization
  time-set.target      loaded active active System Time Set
  time-sync.target     loaded active active System Time Synchronized
  timers.target        loaded active active Timers

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.
19 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.
```

Notice how some of the mappings, such as rescue.target, are missing?
We can show the inactive ones as well if we add the `--all` argument.

```
➜  ~ git:(master) ✗ sudo systemctl list-units --type target --all --no-pager
  UNIT                                                   LOAD   ACTIVE   SUB    DESCRIPTION
  basic.target                                           loaded active   active Basic System
  blockdev@dev-disk-by\x2duuid-4a77d180\x2dfc64\x2d4057… loaded inactive dead   Block Device Preparation for /dev/disk/by-uuid/4a77d18…
  blockdev@dev-dm\x2d1.target                            loaded inactive dead   Block Device Preparation for /dev/dm-1
  blockdev@dev-mapper-deathstar\x2d\x2dvg\x2droot.target loaded inactive dead   Block Device Preparation for /dev/mapper/deathstar--vg…
  blockdev@dev-mapper-deathstar\x2d\x2dvg\x2dswap_1.tar… loaded inactive dead   Block Device Preparation for /dev/mapper/deathstar--vg…
  blockdev@dev-sda1.target                               loaded inactive dead   Block Device Preparation for /dev/sda1
  bluetooth.target                                       loaded inactive dead   Bluetooth
  cryptsetup.target                                      loaded active   active Local Encrypted Volumes
  emergency.target                                       loaded inactive dead   Emergency Mode
  first-boot-complete.target                             loaded inactive dead   First Boot Complete
  getty-pre.target                                       loaded inactive dead   Login Prompts (Pre)
  getty.target                                           loaded active   active Login Prompts
  graphical.target                                       loaded inactive dead   Graphical Interface
  local-fs-pre.target                                    loaded active   active Local File Systems (Pre)
  local-fs.target                                        loaded active   active Local File Systems
  multi-user.target                                      loaded active   active Multi-User System
  network-online.target                                  loaded inactive dead   Network is Online
  network-pre.target                                     loaded inactive dead   Network (Pre)
  network.target                                         loaded active   active Network
  nfs-client.target                                      loaded active   active NFS client services
  nss-user-lookup.target                                 loaded inactive dead   User and Group Name Lookups
  paths.target                                           loaded active   active Paths
  remote-fs-pre.target                                   loaded active   active Remote File Systems (Pre)
  remote-fs.target                                       loaded active   active Remote File Systems
  rescue.target                                          loaded inactive dead   Rescue Mode
  rpcbind.target                                         loaded active   active RPC Port Mapper
  shutdown.target                                        loaded inactive dead   Shutdown
  slices.target                                          loaded active   active Slices
  sockets.target                                         loaded active   active Sockets
  sound.target                                           loaded inactive dead   Sound Card
  swap.target                                            loaded active   active Swap
  sysinit.target                                         loaded active   active System Initialization
  time-set.target                                        loaded active   active System Time Set
  time-sync.target                                       loaded active   active System Time Synchronized
  timers.target                                          loaded active   active Timers
  umount.target                                          loaded inactive dead   Unmount All Filesystems

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.
36 loaded units listed.
To show all installed unit files use 'systemctl list-unit-files'.
➜  ~ git:(master) ✗
```

That's better but still, some other ones such as poweroff.target seem to be missing.
Those are both not active and not loaded, but still available.
We can list all unit files known to our system with a different command.

```
➜  ~ git:(master) ✗ sudo systemctl list-unit-files --type target --all --no-pager 
UNIT FILE                     STATE    VENDOR PRESET
basic.target                  static   -            
blockdev@.target              static   -            
bluetooth.target              static   -            
boot-complete.target          static   -            
cryptsetup-pre.target         static   -            
cryptsetup.target             static   -            
ctrl-alt-del.target           alias    -            
default.target                alias    -            
emergency.target              static   -            
exit.target                   disabled disabled     
final.target                  static   -            
first-boot-complete.target    static   -            
getty-pre.target              static   -            
getty.target                  static   -            
graphical.target              static   -            
halt.target                   disabled disabled     
hibernate.target              static   -            
hybrid-sleep.target           static   -            
initrd-fs.target              static   -            
initrd-root-device.target     static   -            
initrd-root-fs.target         static   -            
initrd-switch-root.target     static   -            
initrd.target                 static   -            
kexec.target                  disabled disabled     
local-fs-pre.target           static   -            
local-fs.target               static   -            
multi-user.target             static   -            
network-online.target         static   -            
network-pre.target            static   -            
network.target                static   -            
nfs-client.target             enabled  enabled      
nss-lookup.target             static   -            
nss-user-lookup.target        static   -            
paths.target                  static   -            
poweroff.target               disabled disabled     
printer.target                static   -            
reboot.target                 disabled enabled      
remote-cryptsetup.target      disabled enabled      
remote-fs-pre.target          static   -            
remote-fs.target              enabled  enabled      
rescue-ssh.target             static   -            
rescue.target                 static   -            
rpcbind.target                static   -            
runlevel0.target              alias    -            
runlevel1.target              alias    -            
runlevel2.target              alias    -            
runlevel3.target              alias    -            
runlevel4.target              alias    -            
runlevel5.target              alias    -            
runlevel6.target              alias    -            
shutdown.target               static   -            
sigpwr.target                 static   -            
sleep.target                  static   -            
slices.target                 static   -            
smartcard.target              static   -            
sockets.target                static   -            
sound.target                  static   -            
suspend-then-hibernate.target static   -            
suspend.target                static   -            
swap.target                   static   -            
sysinit.target                static   -            
system-update-pre.target      static   -            
system-update.target          static   -            
time-set.target               static   -            
time-sync.target              static   -            
timers.target                 static   -            
umount.target                 static   -            
usb-gadget.target             static   -            

68 unit files listed.
➜  ~ git:(master) ✗
```

That seems to be complete.
Now, how do we switch form one target to an other in a modern systemd-like fashion?
For this we use the `isolate` argument to `systemctl`.
A quick test of a this can be done as such, `sudo systemctl isolate reboot.target`.
On a Linux system where root has a password set you could try the `rescue.target` as well.
You can get and set the default runlevel of you system with the following commands.

```
➜  ~ git:(master) ✗ sudo systemctl get-default 
graphical.target
➜  ~ git:(master) ✗ sudo systemctl set-default multi-user.target 
Created symlink /etc/systemd/system/default.target → /lib/systemd/system/multi-user.target.
➜  ~ git:(master) ✗ sudo systemctl get-default                  
multi-user.target
➜  ~ git:(master) ✗ 
```

## A deeper look into targets

What is included in all of these targets?
We can inspect their dependencies by invoking the `list-dependencies` argument to `systemctl`.
Let's start with the most basic one, the `rescue.target`.

```
➜  ~ git:(master) ✗ sudo systemctl list-dependencies rescue.target --no-pager
rescue.target
● ├─rescue.service
● ├─systemd-update-utmp-runlevel.service
● └─sysinit.target
●   ├─apparmor.service
●   ├─blk-availability.service
●   ├─dev-hugepages.mount
●   ├─dev-mqueue.mount
●   ├─keyboard-setup.service
●   ├─kmod-static-nodes.service
●   ├─lvm2-lvmpolld.socket
●   ├─lvm2-monitor.service
●   ├─proc-sys-fs-binfmt_misc.automount
●   ├─sys-fs-fuse-connections.mount
●   ├─sys-kernel-config.mount
●   ├─sys-kernel-debug.mount
●   ├─sys-kernel-tracing.mount
●   ├─systemd-ask-password-console.path
●   ├─systemd-binfmt.service
●   ├─systemd-boot-system-token.service
●   ├─systemd-hwdb-update.service
●   ├─systemd-journal-flush.service
●   ├─systemd-journald.service
●   ├─systemd-machine-id-commit.service
●   ├─systemd-modules-load.service
●   ├─systemd-pstore.service
●   ├─systemd-random-seed.service
●   ├─systemd-sysctl.service
●   ├─systemd-sysusers.service
●   ├─systemd-timesyncd.service
●   ├─systemd-tmpfiles-setup-dev.service
●   ├─systemd-tmpfiles-setup.service
●   ├─systemd-udev-trigger.service
●   ├─systemd-udevd.service
●   ├─systemd-update-utmp.service
●   ├─cryptsetup.target
●   ├─local-fs.target
●   │ ├─-.mount
●   │ ├─boot.mount
●   │ ├─systemd-fsck-root.service
●   │ └─systemd-remount-fs.service
●   └─swap.target
●     └─dev-mapper-deathstar\x2d\x2dvg\x2dswap_1.swap
➜  ~ git:(master) ✗ 
```

As you can see, it's quite basic.
All of these services and additional targets will try to be loaded and started when we enter rescue mode.
Now, let's compare it to the most elaborate runlevel, `5`.

```
➜  ~ git:(master) ✗ sudo systemctl list-dependencies graphical.target --no-pager 
graphical.target
● ├─display-manager.service
● ├─systemd-update-utmp-runlevel.service
● ├─udisks2.service
● └─multi-user.target
●   ├─avahi-daemon.service
●   ├─binfmt-support.service
●   ├─blueman-mechanism.service
●   ├─chrony.service
●   ├─console-setup.service
●   ├─cron.service
●   ├─cups-browsed.service
●   ├─cups.path
●   ├─dbus.service
●   ├─e2scrub_reap.service
●   ├─ModemManager.service
●   ├─networking.service
●   ├─rpcbind.service
●   ├─rsyslog.service
●   ├─ssh.service
●   ├─systemd-ask-password-wall.path
●   ├─systemd-logind.service
●   ├─systemd-update-utmp-runlevel.service
●   ├─systemd-user-sessions.service
●   ├─wpa_supplicant.service
●   ├─basic.target
●   │ ├─-.mount
●   │ ├─tmp.mount
●   │ ├─paths.target
●   │ ├─slices.target
●   │ │ ├─-.slice
●   │ │ └─system.slice
●   │ ├─sockets.target
●   │ │ ├─avahi-daemon.socket
●   │ │ ├─cups.socket
●   │ │ ├─dbus.socket
●   │ │ ├─dm-event.socket
●   │ │ ├─pcscd.socket
●   │ │ ├─rpcbind.socket
●   │ │ ├─systemd-initctl.socket
●   │ │ ├─systemd-journald-audit.socket
●   │ │ ├─systemd-journald-dev-log.socket
●   │ │ ├─systemd-journald.socket
●   │ │ ├─systemd-udevd-control.socket
●   │ │ └─systemd-udevd-kernel.socket
●   │ ├─sysinit.target
●   │ │ ├─apparmor.service
●   │ │ ├─blk-availability.service
●   │ │ ├─dev-hugepages.mount
●   │ │ ├─dev-mqueue.mount
●   │ │ ├─keyboard-setup.service
●   │ │ ├─kmod-static-nodes.service
●   │ │ ├─lvm2-lvmpolld.socket
●   │ │ ├─lvm2-monitor.service
●   │ │ ├─proc-sys-fs-binfmt_misc.automount
●   │ │ ├─sys-fs-fuse-connections.mount
●   │ │ ├─sys-kernel-config.mount
●   │ │ ├─sys-kernel-debug.mount
●   │ │ ├─sys-kernel-tracing.mount
●   │ │ ├─systemd-ask-password-console.path
●   │ │ ├─systemd-binfmt.service
●   │ │ ├─systemd-boot-system-token.service
●   │ │ ├─systemd-hwdb-update.service
●   │ │ ├─systemd-journal-flush.service
●   │ │ ├─systemd-journald.service
●   │ │ ├─systemd-machine-id-commit.service
●   │ │ ├─systemd-modules-load.service
●   │ │ ├─systemd-pstore.service
●   │ │ ├─systemd-random-seed.service
●   │ │ ├─systemd-sysctl.service
●   │ │ ├─systemd-sysusers.service
●   │ │ ├─systemd-timesyncd.service
●   │ │ ├─systemd-tmpfiles-setup-dev.service
●   │ │ ├─systemd-tmpfiles-setup.service
●   │ │ ├─systemd-udev-trigger.service
●   │ │ ├─systemd-udevd.service
●   │ │ ├─systemd-update-utmp.service
●   │ │ ├─cryptsetup.target
●   │ │ ├─local-fs.target
●   │ │ │ ├─-.mount
●   │ │ │ ├─boot.mount
●   │ │ │ ├─systemd-fsck-root.service
●   │ │ │ └─systemd-remount-fs.service
●   │ │ └─swap.target
●   │ │   └─dev-mapper-deathstar\x2d\x2dvg\x2dswap_1.swap
●   │ └─timers.target
●   │   ├─apt-daily-upgrade.timer
●   │   ├─apt-daily.timer
●   │   ├─e2scrub_all.timer
●   │   ├─logrotate.timer
●   │   ├─man-db.timer
●   │   └─systemd-tmpfiles-clean.timer
●   ├─getty.target
●   │ ├─getty-static.service
●   │ └─getty@tty1.service
●   ├─nfs-client.target
●   │ ├─auth-rpcgss-module.service
●   │ ├─nfs-blkmap.service
●   │ └─remote-fs-pre.target
●   └─remote-fs.target
●     └─nfs-client.target
●       ├─auth-rpcgss-module.service
●       ├─nfs-blkmap.service
●       └─remote-fs-pre.target
➜  ~ git:(master) ✗
```

You immediately see, and probably recognise a lot of very useful services that get launched when we enter the graphical target.
Mind you that the output above is from a pretty lean system running a minimal i3 graphical environment.

We can also use the `list-dependencies` to inspect services such as `sshd.service`.
The list below is everything sshd depends on to succesfully run as a systemd service.

```
sshd.service
● ├─-.mount
● ├─system.slice
● └─sysinit.target
●   ├─apparmor.service
●   ├─blk-availability.service
●   ├─dev-hugepages.mount
●   ├─dev-mqueue.mount
●   ├─keyboard-setup.service
●   ├─kmod-static-nodes.service
●   ├─lvm2-lvmpolld.socket
●   ├─lvm2-monitor.service
●   ├─proc-sys-fs-binfmt_misc.automount
●   ├─sys-fs-fuse-connections.mount
●   ├─sys-kernel-config.mount
●   ├─sys-kernel-debug.mount
●   ├─sys-kernel-tracing.mount
●   ├─systemd-ask-password-console.path
●   ├─systemd-binfmt.service
●   ├─systemd-boot-system-token.service
●   ├─systemd-hwdb-update.service
●   ├─systemd-journal-flush.service
●   ├─systemd-journald.service
●   ├─systemd-machine-id-commit.service
●   ├─systemd-modules-load.service
●   ├─systemd-pstore.service
●   ├─systemd-random-seed.service
●   ├─systemd-sysctl.service
●   ├─systemd-sysusers.service
●   ├─systemd-timesyncd.service
●   ├─systemd-tmpfiles-setup-dev.service
●   ├─systemd-tmpfiles-setup.service
●   ├─systemd-udev-trigger.service
●   ├─systemd-udevd.service
●   ├─systemd-update-utmp.service
●   ├─cryptsetup.target
●   ├─local-fs.target
●   │ ├─-.mount
●   │ ├─boot.mount
●   │ ├─systemd-fsck-root.service
●   │ └─systemd-remount-fs.service
●   └─swap.target
●     └─dev-mapper-deathstar\x2d\x2dvg\x2dswap_1.swap
➜  ~ git:(master) ✗ 
```

A very clever *reverse dependency* list can be show by adding the `--reverse` argument.
The output below show the dependencies of the networking.service first.
You can see it *needs* the ifupdown-pre.service, system.slice and the network.target.
The second command shows the reverse, which services or targets *depend* on the networking.service to be up and running.

```
➜  ~ git:(master) ✗ sudo systemctl list-dependencies networking.service --no-pager             
networking.service
● ├─ifupdown-pre.service
● ├─system.slice
● └─network.target
➜  ~ git:(master) ✗ sudo systemctl list-dependencies networking.service --no-pager --reverse
networking.service
● ├─multi-user.target
● │ └─graphical.target
● └─network-online.target
➜  ~ git:(master) ✗ 
```

The combination of both can give you a solid understanding of how all services and targets are interconnected.
Just as with services we can inspect *what* a target is doing by looking at it's unit file.

```
➜  ~ git:(master) ✗ sudo systemctl cat network-online.target   
# /lib/systemd/system/network-online.target
#  SPDX-License-Identifier: LGPL-2.1-or-later
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

[Unit]
Description=Network is Online
Documentation=man:systemd.special(7)
Documentation=https://www.freedesktop.org/wiki/Software/systemd/NetworkTarget
After=network.target
➜  ~ git:(master) ✗ 
```

This might not tell you all that much on first sight, but I urge you to take the time out to really read the `man systemd.special`.
It will explain you all the intricacies of the different standard targets and how you can use them to your benefit.

