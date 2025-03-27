# dbus

From our system administrator's point of view, dbus is a bit like systemd.
Most of the time we're unaware of it's existence but it's an essential part of most modern Linux distributions.
But what *is* it and what does it do?

The plain truth is that dbus is an inter process communication bus or [IPC](https://en.wikipedia.org/wiki/Inter-process_communication).
Each program of server we launch is an independent *process* that is managed by our operating system.
It will claim the necessary memory it needs to run, to store data and variables, but this chunk of memory is exclusive to the process.
No other processes *should* be able to access this memory and data.
But how can programs talk to each other if they need to?
This is where dbus comes on the scene.

![dbus](./assets/dbus_01.png)

Dbus allows for programs to expose variables and method, functions the program can execute, to the other program connected to dbus.
The program exposing has full control over what it will **do** when methods are called or variables accessed.
Dbus is in charge of connecting and delivering what it's client demand of each other. 
While this sounds simple, it does this with grate care and precision.
The dbus [specification](https://dbus.freedesktop.org/doc/dbus-specification.html) states that:

> D-Bus is a system for low-overhead, easy to use interprocess communication (IPC). In more detail:

> * D-Bus is low-overhead because it uses a binary protocol, and does not have to convert to and from a text format such as XML. Because D-Bus is intended for potentially high-resolution same-machine IPC, not primarily for Internet IPC, this is an interesting optimization. D-Bus is also designed to avoid round trips and allow asynchronous operation, much like the X protocol.

> * D-Bus is easy to use because it works in terms of messages rather than byte streams, and automatically handles a lot of the hard IPC issues. Also, the D-Bus library is designed to be wrapped in a way that lets developers use their framework's existing object/type system, rather than learning a new one specifically for IPC.

## Two different busses

On most machines you'll encounter two different, and independent, busses.

* a system bus used by the system to communicate
* a session bus (per logged in user) for programs run by the user

This separation is needed from both practical and security stand point.
Practically speaking I want to control *my* VLC player and not some other one.
From a security point of view unprivileged users should not be allowed to circumvent permissions by hopping on the system bus and triggering all sorts of things they are not allowed to!

Let's have a look at what's running on my home computer.
We clearly see two independent busses running.

```bash
➜  ~ git:(master) ✗ ps aux | grep dbus         
message+     548  0.0  0.0   8864  5192 ?        Ss   Aug28   0:06 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
waldek      1780  0.0  0.0   8628  5136 ?        Ss   Aug28   0:01 /usr/bin/dbus-daemon --session --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
waldek    799748  0.0  0.0   6316   656 pts/2    S+   20:42   0:00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn --exclude-dir=.idea --exclude-dir=.tox dbus
➜  ~ git:(master) ✗ 
```

Now on a server.
Where we only see **one** bus which is the system bus.
This server is headless, so no graphical login is possible.

```bash
➜  ~ ps aux | grep dbus
message+   596  0.0  0.1   8956  3744 ?        Ss   Mar22  29:09 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
waldek    2982  0.0  0.0   6144   824 pts/0    S+   18:44   0:00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn --exclude-dir=.idea --exclude-dir=.tox dbus
➜  ~ 
```

Both `PID`'s are in the same *ballpark* number wise and on the lower end of the spectrum.
This probably means the dbus system bus process is started at boot.
Let's find out a bit more about it.
As it's a program running at boot, it's probably started by `systemd`.

```bash
➜  ~ sudo systemctl list-dependencies dbus.service --reverse
dbus.service
● └─multi-user.target
●   └─graphical.target
➜  ~ 
```

Here we can see that dbus is started when the computer reaches the `multi-user.target` runlevel.
If we would reboot in single user mode, or `rescue.target`, dbus would not be launched!
What about the user bus?
We don't see any specific service files for that one?
Let's have a look at the `systemctl --user` output.

```bash
➜  ~ git:(master) ✗ systemctl --user --type=service | grep dbus
  dbus.service                        loaded active running D-Bus User Message Bus
➜  ~ git:(master) ✗ 
```

```bash
➜  ~ git:(master) ✗ systemctl --user list-dependencies dbus.service 
dbus.service
● ├─app.slice
● ├─dbus.socket
● └─basic.target
●   ├─paths.target
●   ├─sockets.target
●   │ ├─dbus.socket
●   │ ├─dirmngr.socket
●   │ ├─gpg-agent-browser.socket
●   │ ├─gpg-agent-extra.socket
●   │ ├─gpg-agent-ssh.socket
●   │ ├─gpg-agent.socket
●   │ ├─pipewire.socket
●   │ ├─pk-debconf-helper.socket
●   │ └─pulseaudio.socket
●   └─timers.target
➜  ~ git:(master) ✗ 
```

```bash
➜  ~ git:(master) ✗ systemctl --user list-dependencies dbus.service --reverse      
dbus.service
➜  ~ git:(master) ✗ 
```

## Inspecting the bus

### Graphical

When you're in a graphical environment the *easiest* tool to understand what is exposed on the bus is `d-feet`.
To see what is going on on the bus you're better off with `bustle`.
Let's install both and open up d-feet first.
We can do all of this in the command line as well, but first we'll have a look at the graphical applications.
For an easy demonstration I would like you to install `vlc` as well.

```bash
➜  ~ git:(master) ✗ sudo apt install d-feet bustle vlc
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
bustle is already the newest version (0.8.0-1).
d-feet is already the newest version (0.3.15-3).
vlc is already the newest version (3.0.16-1).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
➜  ~ git:(master) ✗ 
```

Open up `d-feet` and `vlc` and search for vlc on the session bus.
You should see something very similar to the screenshot below.
Open a video or audio file in vlc and try to pause it from d-feet.
Have a look at some properties and some methods.
What would the *signals* be?

![d-feet](./assets/dbus_02.png)

Now keep both vlc and d-feet open and we'll add bustle to the mix.
Bustle can record events on either the system or your session bus.
As we're using vlc for the demonstration go ahead and record the session bus.
Try to pause and play your video and try to spit the flow of operations.

![bustle](./assets/dbus_03.png)

### From the command line

Dbus comes with it's own command line tools to interact with programs exposed on the bus.
Let's have a look at them.
First up is `dbus-monitor` and let's see it's arguments.

```bash
➜  ~ git:(master) ✗ dbus-monitor --help  
Usage: dbus-monitor [--system | --session | --address ADDRESS] [--monitor | --profile | --pcap | --binary ] [watch expressions]
➜  ~ git:(master) ✗ 
```

The most general way to invoke it is with either `--system` or `--session`.
We've already looked at the session bus so let's now look at the system bus.
Let's one op one terminal, run `sudo dbus-monitor --system` and keep it running.
In a second terminal stop one of your running services, such as ssh.
You'll see a bunch of messages appearing in the monitor terminal.
Start the service back up.
Do you understand what is happening here?
Try and visualize both terminals at the same time as in the screenshot below.
Try some tabcomplete and see what is happening.

![tab complete](./assets/dbus_04.png)

## Sending messages

We can send things over dbus ourselves with the `dbus-send` program but first we'll use a special program that's very handy to send messages to the notification program of our desktop environment.
It's called `notify-send` and you can install it by installing the `libnotify-bin` package ins Debian.
Once it's installed try it out as follows.

```
➜  ~ git:(master) ✗ notify-send "hello"
➜  ~ git:(master) ✗ 
```

It immediately return but a notification should have popped up on your screen.
You can use this from within bash scripts to signal the user about updates or errors.
But let's dig a little deeper to see what's happening on the inside.
For this we need to inspect the session bus and post a message again.
Look for your message and observe the method that was called.
It should look similar to the one below.

```bash
method call time=1630874537.889652 sender=:1.544 -> destination=:1.52 serial=7 path=/org/freedesktop/Notifications; interface=org.freedesktop.Notifications; member=Notify
   string "notify-send"
   uint32 0
   string "dialog-information"
   string "Hello world!"
   string "I am a notification..."
   array [
   ]
   array [
      dict entry(
         string "urgency"
         variant             byte 1
      )
   ]
   int32 -1
```

With this information we can construct a raw dbus-send command ourselves (but we'll run into a problem!).
Let's try and map the usage to what we observed above.
Luckily `dbus-send` does autocomplete!
But we can take d-feet on the side to better understand the structure.

```bash
➜  ~ git:(master) ✗ dbus-send --help
Usage: dbus-send [--help] [--system | --session | --bus=ADDRESS | --peer=ADDRESS] [--dest=NAME] [--type=TYPE] [--print-reply[=literal]] [--reply-timeout=MSEC] <destination object path> <message name> [contents ...]
➜  ~ git:(master) ✗ dbus-send --session --print-reply --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.Notify
```

We need to send a message to:

* `--session` bus
* we want to see the reply, or error, if any `--print-reply`
* our destination is `--dest` the notifications
* at this destination we only have one object `/org/freedesktop/Notifications`
* on this object we can call the `org.freedesktop.Notifications.Notify` method

But we run in to an error! (that's why we want the `--print-reply` argument)

```bash
Error org.freedesktop.DBus.Error.InvalidArgs: Type of message, “()”, does not match expected type “(susssasa{sv}i)”
```

The `Notify` method needs arguments and quite a lot of them!
In `d-feet` or our `dbus-monitor` output above we can visualize what these arguments are.
The *type* in the error message looks abstract but when we put it side by side with our dbus-monitor output it starts to make sense.

```bash
string "notify-send"
uint32 0
string "dialog-information"
string "Hello world!"
string "I am a notification..."
array [
]
array [
   dict entry(
      string "urgency"
      variant             byte 1
   )
]
int32 -1
```

Dbus can send only specific types over the wire and they are described in the specification online.
We could try to get get to work on the command line but sadly it won't!
`dbus-send` and not send the *variant* type in an array so we're out of luck (I might be wrong here!).
An alternative program that can complete this challenge is `gdbus`.
Try to get that one to display a notification!

Let's try to interact with vlc via dbus-send instead.
Below are some examples that you'll have to tweak to suit your needs.

```bash
dbus-send --session --print-reply=literal --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause 
dbus-send --session --print-reply=literal --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play
dbus-send --session --print-reply=literal --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.SetPosition objpath:/org/videolan/vlc/playlist/3 int64:100000000
dbus-send --session --print-reply=literal --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.OpenUri string:"file:///home/waldek/Coralis_MASTER+VO-V5.mp4"
```

