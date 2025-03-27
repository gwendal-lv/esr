# GRUB2

### Introduction

GRUB2 is a multiboot *boot loader*. It replaces GRUB which is now named as GRUB Legacy.

A boot loader is the first software that runs when the computer starts. Its main task is to load the operating system kernel and transfer of the computre to it. The kernel itsself inityalizes the rest of the system.

There are other boot loaders available with their own features which can sometime be prefered if you don't need GRUB features. (i.e. for minimal system):

- LILO: The old traditionnal linux bootloader (generaly replaced by GRUB)

- ELILO: the EFI variant of LILO

- Systemd-boot: Systemd integrated bootloader (doesn't support multiboot)

- Syslinux

- etc.

## Grub main features

- Full multiboot support

- Providides a user interface

- Flexible command line iterface

- Supports most filesystems types

- Supports network boot

- Allows chainloading other boot loaders

- Customizable menu content and appearance

## Installing grub

Installing *GRUB* can be a bit confusing. As it is needed to boot our system it should be installed while we install our system for the first time and thus must be included in the installation image we are using. But sometimes it could be necessary to reinstall it or simply installed because we were using another boot loader. Therefore if it's not already present the first thing to do is to install the `grub2` package. As usual the package name could be different on non-debian based systems.

```
sudo apt install grub2
```

Having the `grub2` package doesn't mean GRUB is ready to work. In fact we need to install its *code* into the filesystem and make sure it has a configuration file.

### Installing GRUB on a BIOS based systems

On BIOS based system, the boot loader must be installed on the Master Boot Record of the primary disk. Thus if our system has a primary disk named `sda` we would need to install grub using the following command:

```
grub-install /dev/sda
```

This command install GRUB code to the MBR and its files in the `/boot` directory.

### Installing GRUB on a EFI based  system

On EFI based systems GRUB mus be installed on a dedicated partition which should by default be mounted in `/boot/efi/`. This partition, the '*EFI System Partition (ESP)* must be independent from the system partition and have enough space to store the files needed at boot time (the kernel and other files). You should have at least 300Mo available but 500Mo to 1Go would be wise if you have enough space.

It's also recommended to use a GPT parition table. The UEFI/MBR is not always supported by operatin system installers.

To install GRUB on the given partition we would simply need to call `grub-install` with specific *efi* options.

```
grub-install --efi-directory=/boot/efi
```

### Generating GRUB configuration

GRUB needs a configuration file which by default would be `/boot/grub/grub.cfg`. This file should never be edited manually. Instead we must use `grub-mkconfig` to create or update it.

```
grub-mkconfig -o /boot/grub/grub.cfg
```

When generating the configuration file, `grub-mkconfig` uses scripts found in `/etc/grub.d` to create its `grub.cfg` file.

```
sdejongh@debian-base:~$ ls -al /etc/grub.d/
total 96
drwxr-xr-x   2 root root  4096 Sep  8 09:02 .
drwxr-xr-x 126 root root 12288 Oct 18 09:59 ..
-rwxr-xr-x   1 root root 10046 Jul 11  2021 00_header
-rwxr-xr-x   1 root root  6260 Jul 11  2021 05_debian_theme
-rwxr-xr-x   1 root root 13664 Jul 11  2021 10_linux
-rwxr-xr-x   1 root root 13726 Jul 11  2021 20_linux_xen
-rwxr-xr-x   1 root root 12059 Jul 11  2021 30_os-prober
-rwxr-xr-x   1 root root  1416 Jul 11  2021 30_uefi-firmware
-rwxr-xr-x   1 root root   214 Jul 11  2021 40_custom
-rwxr-xr-x   1 root root   216 Jul 11  2021 41_custom
-rw-r--r--   1 root root   483 Jul 11  2021 README
sdejongh@debian-base:~$
```

`mk-grubcfg` simply executes all executable files in this directory following the alphanumeric order. That's the reason why by default filenames include a numeric value.

Generaly you should never modify thos files except those named *custom*. This is where you should eventually add customizations.

If you want to disable one of those script, you can simply remove the executable attribute of the file using `chmod -x`.

## Using GRUB

Depending on its configuration GRUB could display a menu at boot time or not. In any case holding the `shift` key while booting should force GRUB to display it.

![](./assets/grub_01.png)

There you can use the arrow keys to navigate the menu and press `Enter` to choose a boot entry. You can also press `e` to edit the menu entries (modification are temporary) or `c` to access the GRUB shell.

## Customizing GRUB behaviour

The general GRUB behavious is defined in `/etc/default/grub`. In this file you can define settings like the menu timeout, the screen definition, ...

Each time you modify this file you should regenerate the `grub.cfg` file using the following command...

```
sudo update-grub
```

Let's have a lot at the `/etc/default/grub` file...

```bash
# If you change this file, run 'update-grub' afterwards to update
# /boot/grub/grub.cfg.
# For full documentation of the options in this file, see:
#   info -f grub -n 'Simple configuration'

GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet"
GRUB_CMDLINE_LINUX=""

# Uncomment to enable BadRAM filtering, modify to suit your needs
# This works with Linux (no patch required) and with any kernel that obtains
# the memory map information from GRUB (GNU Mach, kernel of FreeBSD ...)
#GRUB_BADRAM="0x01234567,0xfefefefe,0x89abcdef,0xefefefef"

# Uncomment to disable graphical terminal (grub-pc only)
#GRUB_TERMINAL=console

# The resolution used on graphical terminal
# note that you can use only modes which your graphic card supports via VBE
# you can see them in real GRUB with the command `vbeinfo'
#GRUB_GFXMODE=640x480

# Uncomment if you don't want GRUB to pass "root=UUID=xxx" parameter to Linux
#GRUB_DISABLE_LINUX_UUID=true

# Uncomment to disable generation of recovery mode menu entries
#GRUB_DISABLE_RECOVERY="true"

# Uncomment to get a beep at grub start
#GRUB_INIT_TUNE="480 440 1"
```

As you can see this file contains setting variables which are used to generate the `grub.cfg`file.

Here are some of the most used options and their usage:

| Setting                    | Description                                                                                                                                                                                                      | Values                                                                                          |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| GRUB_DEFAULT               | The default entry GRUB will use to boot                                                                                                                                                                          | a number (nth entry) or the entry title or `saved`                                              |
| GRUB_SAVEDEFAULT           | Save the choosent entry and use it as default for next boots. GRUB_DEFAULT should be set to `saved`                                                                                                              | `true` `false`                                                                                  |
| GRUB_TIMEOUT               | How long will the menu be displayed.                                                                                                                                                                             | 0 to boot immediatly, -1 to wait indefinitely, or any number to wait for a given time (seconds) |
| GRUB_TIMEOUT_STYLE         | Defines wether or not the menu should be displayed during the timeout. If `hidden` then user  should press `ESC` to end the timeout and display the menu. If `menu` the menu is shown before the timeout starts. | `menu` or `hidden`                                                                              |
| GRUB_CMDLINE_LINUX         | Command-line arguments to add to menu entries for the linux kernel.                                                                                                                                              | String of space separated arguments.                                                            |
| GRUB_CMDLINE_LINUX_DEFAULT | command-line arguments to add only to the default (recovery) menu entry, after those listed in 'GRUB_CMDLINE_LINUX'                                                                                              | String of space separated arguments.                                                            |
| GRUB_DISABLE_RECOVERY      | Disable the auto generation of recovery entries in the grub menu                                                                                                                                                 | `true` or `false`                                                                               |

## Kernel command line arguments

Wether you add them to the menu entries using the `/etc/default/grub` file, or by editing the menu entries while in the grub menu or by editing the files in `/etc/grub.d/`, the kernel command line arguments are used to change the kernel behaviour at boot time.

You can find the full list of kernel arguments here:  [The kernel’s command-line parameters &mdash; The Linux Kernel documentation](https://www.kernel.org/doc/html/v4.14/admin-guide/kernel-parameters.html)

Some of them can be very useful:

| Argument       | Description                                                                                                             | Values                    |
| -------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `quiet`        | Disable log messages while booting                                                                                      | -                         |
| `init`         | Run a specific binary in stead of /sbin/init                                                                            | /path/to/binary           |
| `single`       | Boot into single user mode. `root` account should not be locked.                                                        | -                         |
| `splash`       | Display splash screen while booting. `quiet` should also be enable to prevent log message to disrupt the splash screen. | -                         |
| `systemd.unit` | Boot to the given systemd target                                                                                        | systemd target unit name. |

## Accessing GRUB shell

GRUB shell is command line interface allowing you to operate your system manually (loading kernell, etc.). You can access it by pressing `c` while the boot menu is displayed.

![](./assets/grub_02.png)

## Resources

- [GNU GRUB Manual 2.06: Top](https://www.gnu.org/software/grub/manual/grub/html_node/index.html)

- [GRUB 2 bootloader - Full tutorial](https://www.dedoimedo.com/computers/grub-2.html)

- How Linux Works (3rd edition) by Brian Ward - Chapter 5 (p117-135)
