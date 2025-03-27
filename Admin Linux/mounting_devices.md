# Mounting file systems

In Linux/Unix systems all files are arranged in one big tree, the file hierarchy. As we already know, the root of this hierarchy is `/`.

Files can be spread over several devices which must be attached to the file hierarchy at some point,  that's what we call *mounting* a file system.

Mounting and unmounting file systems can be done using the `mount` and `umount` utilities.  Obviously it's also possible to automaticaly mount them when the system is initialized using the *File System TABle* also know as `fstab`.

## Listing mounted file systems

As said earlier, file systems can be mounted manualy using the `mount` command or automatically using `fstab`.  All mounted file systems can be listed using the `mount` command without any argument.

```
sdejongh@debian:~$ mount
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
dev on /dev type devtmpfs (rw,nosuid,relatime,size=4044160k,nr_inodes=1011040,mode=755)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
tmpfs on /run type tmpfs (rw,nosuid,nodev,noexec,relatime,size=813500k,mode=755)
/dev/sda2 on / type ext4 (rw,relatime,errors=remount-ro)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
tmpfs on /run/lock type tmpfs (rw,nosuid,nodev,noexec,relatime,size=5120k)
cgroup2 on /sys/fs/cgroup type cgroup2 (rw,nosuid,nodev,noexec,relatime,nsdelegate,memory_recursiveprot)
pstore on /sys/fs/pstore type pstore (rw,nosuid,nodev,noexec,relatime)
efivarfs on /sys/firmware/efi/efivars type efivarfs (rw,nosuid,nodev,noexec,relatime)
none on /sys/fs/bpf type bpf (rw,nosuid,nodev,noexec,relatime,mode=700)
systemd-1 on /proc/sys/fs/binfmt_misc type autofs (rw,relatime,fd=29,pgrp=1,timeout=0,minproto=5,maxproto=5,direct,pipe_ino=13594)
mqueue on /dev/mqueue type mqueue (rw,nosuid,nodev,noexec,relatime)
hugetlbfs on /dev/hugepages type hugetlbfs (rw,relatime,pagesize=2M)
debugfs on /sys/kernel/debug type debugfs (rw,nosuid,nodev,noexec,relatime)
tracefs on /sys/kernel/tracing type tracefs (rw,nosuid,nodev,noexec,relatime)
fusectl on /sys/fs/fuse/connections type fusectl (rw,nosuid,nodev,noexec,relatime)
configfs on /sys/kernel/config type configfs (rw,nosuid,nodev,noexec,relatime)
/dev/sda3 on /var type ext4 (rw,relatime)
/dev/sda5 on /tmp type ext4 (rw,relatime)
/dev/sda6 on /home type ext4 (rw,relatime)
/dev/sda1 on /boot/efi type vfat (rw,relatime,fmask=0077,dmask=0077,codepage=437,iocharset=ascii,shortname=mixed,utf8,errors=remount-ro)
tmpfs on /run/user/1000 type tmpfs (rw,nosuid,nodev,relatime,size=813496k,nr_inodes=203374,mode=700,uid=1000,gid=1000)
gvfsd-fuse on /run/user/1000/gvfs type fuse.gvfsd-fuse (rw,nosuid,nodev,relatime,user_id=1000,group_id=1000)
sdejongh@debian:~$
```

As you can see, event on a freshly installed machine there are a lot of mount points.

> You will find the same informations inside the `/etc/mtab` file.

For each mount point, you see the file system, the actual mount point, the file system type and the options.

## (un)Mounting file systems using the GUI

Most graphical environments have utilities to manage how new file systems (mostly on removable devices) will be handled by the system like USB drives, optial drives, etc.

Generaly the removable devices file systems are automaticaly shown in the file manager (like Nautilus if you are using a Gnome interface) and mounted as soon as you want to browse them.

Here is the Nautilus window before I insert a new USB drive on my machine (it's a laptop with Ubuntu 22.04 Desktop installed) ...

![](./assets/2022-08-13-10-57-14-image.png)

Now i inserted the USB drive, Nautilus automatically mounted it.

![](./assets/2022-08-13-10-59-10-image.png)

You can seee the `Debian 11.3.0...` at the bottom of the left panel. To unmount it, i simply need to click on the arrow at the right of the drive. Note that it's really important to unmount a drive before removing it physically. It will ensure that all data will be safe and that the drive has stopped working.

With Ubuntu as with Debian, removable drives are mounted in the file system under the `/media` directory.

We can use the `mount`command to get some informations about the mount point.

```
sdejongh@jarvis:~$ mount | grep media
/dev/sda1 on /media/sdejongh/Debian 11.3.0 amd64 n type iso9660 (ro,nosuid,nodev,relatime,nojoliet,check=s,map=n,blocksize=2048,uid=1000,gid=1000,dmode=500,fmode=400,iocharset=utf8,uhelper=udisks2)
sdejongh@jarvis:~$
```

We see here that the USB drive is known by the system as `/dev/sda1` and it has been mounted under `/media/sdejongh/Debian 11.3.0 amd64 n` , it's type is ISO9660 (which is the file system used on optical drives) and it has some properties like `ro` which means it's mounted as read-only, we can also find the `uid` and `gid` of the owner of the mount which are my uid and gid:

```
sdejongh@jarvis:~$ id
uid=1000(sdejongh) gid=1000(sdejongh) groupes=1000(sdejongh),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),122(lpadmin),134(lxd),135(sambashare),139(libvirt),141(vboxusers),142(wireshark),143(ubridge)
sdejongh@jarvis:~$
```

That's something important to understand when we want to manually mount file systems, we need to think about who's gonna need to access the drive and correctly set the owner uid and gid. That also define for example who will be able to unmount the drive without the need of root permissions.

As i'm the owner of the mount i can simply unmount it manually using the command line without calling `sudo` or also use the graphical interface method described earlier`.

```
sdejongh@jarvis:~$ umount /media/sdejongh/Debian\ 11.3.0\ amd64\ n 
sdejongh@jarvis:~$ mount | grep media
sdejongh@jarvis:~$
```

## (un)Mounting file systems using the command line

### Mounting a file system using the `mount` command.

Here is the general structure of the `mount` command:

```
mount [OPTION...] DEVICE_NAME DIRECTORY
```

Note that the command requires `root` priviledges to mount a filesystem.

Most important options are:

- `-t <type>` which allows to specify the file system type (ext4, vfat, ...) when `mount` doesn't automatically recognize the file system. Generaly it won't be necessary for file systems like ext3, ext4, vfat, ...

- `-r` which prevents writing to the mount point and is équivamlent to `-o ro`.

- `-w` which makes the mount point readable and writable and equivalent to `-o rw`.

- `-U <UUID>` mounts the file system identified by its UUID.

- `-L <label>` mounts the file system identified by its label.

#### Identifying the file system

First of all we need to identify the file system we want to mount. This can be done with commands like `fdisk -l`, `lsblk` ...

Let's say we recently added a new hard drive to our machine. The hard drive has been partionned and formated.

```
sdejongh@debian:~$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   50G  0 disk 
├─sda1   8:1    0  512M  0 part /boot/efi
├─sda2   8:2    0 48.5G  0 part /
└─sda3   8:3    0  976M  0 part [SWAP]
sdb      8:16   0    8G  0 disk 
└─sdb1   8:17   0    8G  0 part 
sr0     11:0    1 1024M  0 rom  
sdejongh@debian:~$
```

Here we see that the `/dev/sdb1` partition has not been mounted into the system.

We can also retrieve its UUID using the `blkid` command.

```
sdejongh@debian:~$ sudo blkid
/dev/sda1: UUID="F163-7444" BLOCK_SIZE="512" TYPE="vfat" PARTUUID="1974fa9e-e835-4408-a78c-c3d701230dec"
/dev/sda2: UUID="47bee845-488b-4478-9164-100f86c0d3ed" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="8bfa308d-7634-4ab7-b019-a44e30ffdc7c"
/dev/sda3: UUID="cd67c4f9-13cf-42b8-a1b9-fb9f8dee3804" TYPE="swap" PARTUUID="3f8d0585-33f5-43bd-9519-4e25d964e29f"
/dev/sdb1: UUID="1c4df02c-de3e-4721-a305-0d8ea28590bb" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="dafbccb1-01"
sdejongh@debian:~$
```

The UUID of the `/dev/sdb1` partition is `1c4df02c-de3e-4721-a305-0d8ea28590bb`, that's what we need to specify if we use the `-U` option.

Note that file systems are found under the `/dev` directory like `/deb/sdb1` but they can also be found under `/dev` by their UUID...

```
sdejongh@debian:~$ ls -al /dev/disk/by-uuid/
total 0
drwxr-xr-x 2 root root 120 Sep  4 12:16 .
drwxr-xr-x 6 root root 120 Sep  4 12:10 ..
lrwxrwxrwx 1 root root  10 Sep  4 12:16 1c4df02c-de3e-4721-a305-0d8ea28590bb -> ../../sdb1
lrwxrwxrwx 1 root root  10 Sep  4 12:10 47bee845-488b-4478-9164-100f86c0d3ed -> ../../sda2
lrwxrwxrwx 1 root root  10 Sep  4 12:10 cd67c4f9-13cf-42b8-a1b9-fb9f8dee3804 -> ../../sda3
lrwxrwxrwx 1 root root  10 Sep  4 12:10 F163-7444 -> ../../sda1
sdejongh@debian:~$
```

Pay attention when using UUIDs. You need to remember that its generated when the partition is formated and will change every time the parition is formated.

```
sdejongh@debian:~$ sudo mkfs.ext4 /dev/sdb1
mke2fs 1.46.2 (28-Feb-2021)
/dev/sdb1 contains a ext4 file system
    created on Sun Sep  4 12:16:59 2022
Proceed anyway? (y,N) y

Creating filesystem with 2096896 4k blocks and 524288 inodes
Filesystem UUID: fb0b255a-53be-4959-b250-c6bd834d64ca
Superblock backups stored on blocks: 
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done 

sdejongh@debian:~$
```

```
sdejongh@debian:~$ sudo blkid
/dev/sda1: UUID="F163-7444" BLOCK_SIZE="512" TYPE="vfat" PARTUUID="1974fa9e-e835-4408-a78c-c3d701230dec"
/dev/sda2: UUID="47bee845-488b-4478-9164-100f86c0d3ed" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="8bfa308d-7634-4ab7-b019-a44e30ffdc7c"
/dev/sda3: UUID="cd67c4f9-13cf-42b8-a1b9-fb9f8dee3804" TYPE="swap" PARTUUID="3f8d0585-33f5-43bd-9519-4e25d964e29f"
/dev/sdb1: UUID="fb0b255a-53be-4959-b250-c6bd834d64ca" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="dafbccb1-01"
sdejongh@debian:~$
```

As you can see the UUID of `/dev/sdb1` has changed.

#### Defining the target directory

The second required parameter is the target directory (where the file system will be mounted). There are two main conditions:

- The target directory must exist

- The target directory must be empty

Let's say we whant to mount out `/dev/sdb1` parition in a new directory `/data`. The directory doens't exist yet, so we need to create it:

```
sdejongh@debian:~$ sudo mkdir /data
```

#### Mounting the file system

Now that we identified the file system and that we created the target directory, we are ready to create the mount point.

The most basic mount would just need to define the file system and the target directory...

```
sdejongh@debian:~$ sudo mount /dev/sdb1 /data
```

Note that if you didn't format the parititon the mount will simply fail.

We can now see how the mount point has been created

```
sdejongh@debian:~$ mount | grep sdb1
/dev/sdb1 on /data type ext4 (rw,relatime)
sdejongh@debian:~$
```

Without any option, `mount` will try to figure out the file system type (here its `ext4`), will set the mount point as readable and writable and will set root as the owner.

### Unmouting a file system using the `umount` command.

Unmounting a file system is straightforward, you simply need to call `umount` and specify which mount point you want to unmount

```
sdejongh@debian:~$ sudo umount /data
```

You could also specify the mount point itself...

```
sdejongh@debian:~$ sudo umount /data
```

### Going further with `mount`

#### Mounting the file system as read-only

```
sdejongh@debian:~$ sudo mount -o ro /dev/sdb1 /data
sdejongh@debian:~$ sudo touch /data/test
touch: cannot touch '/data/test': Read-only file system
sdejongh@debian:~$
```

#### Mounting an ISO file

ISO files are optical drive images. They can be mounted into the file system but requires some specific options.

Let's say we have a Debian ISO file we want to mount under `/media/iso` , first, let's create the directory.

```
sdejongh@debian:~$ sudo mkdir -p /media/iso
```

Now let's mount the iso file...

```
sdejongh@debian:~$ sudo mount ~/Downloads/debian-11.4.0-amd64-netinst.iso /media/iso -o loop,ro
```

The important thing here is the `-o loop,ro` option. The `loop` option maps the file to a loop device which allows the file to be used as any storage device.

The `ro` option simply makes it only readable (who wants to write to an optical drive ?)

The ISO file works now like any optical device...

```
sdejongh@debian:~$ ls -al /media/iso
total 692
dr-xr-xr-x 1 root root   4096 Jul  9 11:34 .
drwxr-xr-x 4 root root   4096 Sep  4 12:58 ..
-r--r--r-- 1 root root    146 Jul  9 11:33 autorun.inf
dr-xr-xr-x 1 root root   2048 Jul  9 11:33 boot
dr-xr-xr-x 1 root root   2048 Jul  9 11:33 css
lr-xr-xr-x 1 root root      1 Jul  9 11:33 debian -> .
dr-xr-xr-x 1 root root   2048 Jul  9 11:34 .disk
dr-xr-xr-x 1 root root   2048 Jul  9 11:33 dists
dr-xr-xr-x 1 root root   2048 Jul  9 11:33 doc
dr-xr-xr-x 1 root root   2048 Jul  9 11:33 EFI
dr-xr-xr-x 1 root root   2048 Jul  9 11:33 firmware
-r--r--r-- 1 root root 184032 Jul  5 16:57 g2ldr
-r--r--r-- 1 root root   8192 Jul  5 16:57 g2ldr.mbr
dr-xr-xr-x 1 root root   2048 Jul  9 11:33 install
dr-xr-xr-x 1 root root   2048 Jul  9 11:33 install.amd
dr-xr-xr-x 1 root root   6144 Jul  9 11:33 isolinux
-r--r--r-- 1 root root  91977 Jul  9 11:34 md5sum.txt
dr-xr-xr-x 1 root root   4096 Jul  9 11:33 pics
dr-xr-xr-x 1 root root   2048 Jul  9 11:33 pool
-r--r--r-- 1 root root   8509 Jul  9 11:34 README.html
-r--r--r-- 1 root root    291 Mar  4  2017 README.mirrors.html
-r--r--r-- 1 root root     86 Mar  4  2017 README.mirrors.txt
-r--r--r-- 1 root root    543 Jul  9 11:33 README.source
-r--r--r-- 1 root root   5192 Jul  9 11:34 README.txt
-r--r--r-- 1 root root 364571 Jul  5 16:57 setup.exe
dr-xr-xr-x 1 root root   2048 Jul  9 11:33 tools
-r--r--r-- 1 root root    233 Jul  9 11:33 win32-loader.ini
sdejongh@debian:~$
```

## Mounting file systems using `fstab`

The `mount` command allows you to mount file systems on demand, be you will often want those mount points to be created automatically either by calling `mount -a` or either at system boot.

`fstab` configuration can be found in `/etc/fstab`. Each line defines a mount point.

```bash
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# systemd generates mount units based on this file, see systemd.mount(5).
# Please run 'systemctl daemon-reload' after making changes here.
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
# / was on /dev/sda2 during installation
UUID=47bee845-488b-4478-9164-100f86c0d3ed /               ext4    errors=remount-ro 0       1
# /boot/efi was on /dev/sda1 during installation
UUID=F163-7444  /boot/efi       vfat    umask=0077      0       1
# swap was on /dev/sda3 during installation
UUID=cd67c4f9-13cf-42b8-a1b9-fb9f8dee3804 none            swap    sw              0       0
/dev/sr0        /media/cdrom0   udf,iso9660 user,noauto     0       0
```

The structure of a definition looks like this

```
<file system>    <mount point>    <type>    <options>    <dump>    <pass>
```

- `file system`: the file system we want to mount

- `mount point`: where we wat to mount the file system

- `type`: the file system type (ext4, vfat, ...)

- `options`: the options we would pass using the `-o` parameter like `ro` or `loop` 

- `dump`: définit si l'utilitaire `dump` sauvegardera le système si il est utilisé, généralement laissé à `0`

- `pass`: définit la priorité de passage lors de l'utilisation de `fsck`.
  
     - `0`: le système est ignoré
  
     - `1`: haute priorité
  
     - `2`: basse priorité

By default on linux systems, paritions are named following their type and their order. That means the name of a device can change over the time. That's the reason why is always a good idea, especially for non-removable drives, to identify their partitions by their UUID.

### Adding our `/dev/sdb1` to the `fstab` rules

First let's find the UUID of `/dev/sdb1`...

```
sdejongh@debian:~$ sudo blkid | grep sdb1
/dev/sdb1: UUID="fb0b255a-53be-4959-b250-c6bd834d64ca" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="dafbccb1-01"
sdejongh@debian:~$
```

Assuming our target directory `/data` already exists we can now add a new rule in the `/etc/fstab` file.

```bash
# /dev/sdb1 mounted on /data
UUID=fb0b255a-53be-4959-b250-c6bd834d64ca    /data    ext4    errors=remount-ro    0    0
```

We can now try to automatically mount our file system using `mount -afv` this will attempt to mount all paritions automatically. The `-f` tells mount to fake the mount and the `-v` makes mount report some informations.

```
sdejongh@debian:~$ sudo mount -afv
/                        : ignored
/boot/efi                : already mounted
none                     : ignored
/media/cdrom0            : ignored
/data                    : successfully mounted
sdejongh@debian:~$
```

If the command does not report any error, we can now really run it.

```
sdejongh@debian:~$ sudo mount -a
```

The `lsblk` command should now show where `/dev/sdb1` has been mounted.

```
sdejongh@debian:~$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   50G  0 disk 
├─sda1   8:1    0  512M  0 part /boot/efi
├─sda2   8:2    0 48.5G  0 part /
└─sda3   8:3    0  976M  0 part [SWAP]
sdb      8:16   0    8G  0 disk 
└─sdb1   8:17   0    8G  0 part /data
sr0     11:0    1 1024M  0 rom  
sdejongh@debian:~$
```

### Adding the ISO file to the `fstab` rules

Any file system you mount using the `mount` command can be added to the `fstab` rules.

Let's say we want to make our iso file available on demande (not automatically)...

```bash
# Mounting debian iso on /media/iso on deman only
/home/sdejongh/Downloads/debian-11.4.0-amd64-netinst.iso    /media/iso    auto    noauto,ro,loop    0    0
```

The file system type is set to `auto` meaning `mount` will try to discover the type itself. The `noauto` option makes the mount available on demand, the `loop` and `ro` options  are the same we used in the manual `mount` command.

Let's verify if everything is working...

```
sdejongh@debian:~$ sudo mount -afv
/                        : ignored
/boot/efi                : already mounted
none                     : ignored
/media/cdrom0            : ignored
/data                    : already mounted
/media/iso               : ignored
sdejongh@debian:~$
```

Now that the ISO file has been added to the fstab rules, we can mount it easily...

```
sdejongh@debian:~$ sudo mount /media/iso
```

As you can see, we don't need to sepcify any information except the mount point, everything else is determined by the fstab rule.

And as usual, when we don't need it anymore, we can unmount it too

```
sdejongh@debian:~$ sudo umount /media/iso
```

## Some useful ressources

- [How To Mount and Unmount Drives on Linux &ndash; devconnected](https://devconnected.com/how-to-mount-and-unmount-drives-on-linux/)

- [mount(8) - Linux manual page](https://man7.org/linux/man-pages/man8/mount.8.html)

- [fstab(5) - Linux manual page](https://man7.org/linux/man-pages/man5/fstab.5.html)
