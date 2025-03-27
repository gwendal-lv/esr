# Alpine Linux Installation (Virtual Box)

## Alpine Linux Image
From the download page ([https://www.alpinelinux.org/downloads/](https://www.alpinelinux.org/downloads/)) choose the standard image x86_64.

## Virtual Machine Settings
- **System**: Linux / Other Linux 64bits
- **RAM**: 512Mo
- **CPU**: 1 or 2

## Installing Alpine Linux
### Notes
- Out of the box Alpine Linux runs from RAM and won't install automatically.
- Default user is "root" without password.

### Installation procedure
- Log in as "root"
- Launch setup procedure
```
# setup-alpine
```
The command asks for several options (keyboard layout, install type, network config, ...).
For traditionnal installation, choose "sys" mode disk usage.

* Reboot the VM.
```
# reboot
```

### Desktop environment instalaltion (optionnal)
* Launch X-Server setup
```
# setup-xorg-base
```
* Uncomment community sources repository in */etc/apk/repositories*
* Update packages list
```
# apk update
```
* Install XFCE required package
```
# apk add xfce4 xfce4-terminal xfce4-screensaver lightdm-gtp-greeter
```
* Start and enable *desktop-bus* at startup
```
# rc-service dbus start
# rc-update add dbus
```
* Enable graphical login (requies *lightdm-gtk-greeter*)
```
# rc-service lightdm start
# rc-update add lightdm
```
* Reboot

### Launch desktop GUI from command line
```
# startx
```