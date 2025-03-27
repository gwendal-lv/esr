# Disk Management

## Introduction

Every computer needs to store data (files) somewhat permanently, therefore there must me some kind of physical device attached to it like hard disk drives (aka HDDs), solid state drives (aka SSDs), etc.

If you want to use the storage device, you need a structure/scheme defining how and where data are stored on the drive. Such structures/schemes are named *file systems*.

To keep it simple, think of *file systems* as some kind of directory which allows you to access data stored on the drive.

There are a lot of different file sytems, each one having its own properties and limits like maximum file size, maximum volume size, etc. For example, today the most common file system found on Linux machines is `ext4` which allows files up to 16Tio and volumes up to 1Eio. On Windows based machines you'll mainly find `NTFS` volumes, ...

Now, imagine that you buy a new computer equiped with a 2To SSD and you want to keep your system files separate from your personnal data. You'd need to divide your drive space into two parts, this is where *disk partitions* come into play.
Disk partitions allow you to create several logical volumes on the same physical drive, each having its own file system.

So, if we stick to the classical model, when you want to use a storage drive, you will first create partitions and then format each one with the wanted file system.

## Identifying available storage devices

### Listing available drives and partitions

First of all we need to identify storage devices attached to our computer. This can easily be done thanks to the `lsblk` command.

```
steve@linux-box:~$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   20G  0 disk 
├─sda1   8:1    0   19G  0 part /
├─sda2   8:2    0    1K  0 part 
└─sda5   8:5    0  975M  0 part [SWAP]
sr0     11:0    1 58.3M  0 rom  
steve@linux-box:~$ 
```

- NAME : Drive or partition name

- MAJ:MIN : Major or Minor peripheral number

- RM : 0 is for fixed device, 1 is for removable devices

- SIZE : the volume size

- RO : 0 is for normal devices, 1 is for read-only devices

- TYPE : type of device (disk ,partition, lvm, loop, ...)

- MOUNTPOINT : where the device is mounted in the system

There you can see we have two drives `sda`, the hard drive and `sr0`, the optical drive. The default view shows a tree view of disk partitions. So for example, here you can see that there are three partitions on the  `sda` drive: `sda1`, `sda2` and `sda5`.

You can also use the `lsblk` command to display a simple list view.

```
steve@linux-box:~$ lsblk -l
NAME MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda    8:0    0   20G  0 disk 
sda1   8:1    0   19G  0 part /
sda2   8:2    0    1K  0 part 
sda5   8:5    0  975M  0 part [SWAP]
sr0   11:0    1 58.3M  0 rom  
steve@linux-box:~$
```

This seems to be less intuitive but can be usefull if you need to use the output in some scripts.

### Device naming

You could ask yourself why your drive is named `sda`, the reason is simple, there is some king of naming convention based on drive type.

- fd : for floppy drives

- hd : for old IDE drives

- sd : for SCSI and SATA drives

- sr : for SCSI or SATA optical drives

- nvme : for PCIe NVMe solid state drives

The third letter of the drive name is for the device order `sda` being the first drive, `sdb` would be the second drive and so on.

### Device path

When we'll need to partition a disk, format a partition etc, we'll need to know the path to the device. Fortunately is quite straight forward. All devices attached to the computer are listed in `/dev`.

```
steve@linux-box:~$ ls /dev --width=60
autofs           nvram     tty16  tty45      vboxuser
block            port      tty17  tty46      vcs
bsg              ppp       tty18  tty47      vcs1
btrfs-control    psaux     tty19  tty48      vcs2
bus              ptmx      tty2   tty49      vcs3
cdrom            pts       tty20  tty5       vcs4
char             random    tty21  tty50      vcs5
console          rfkill    tty22  tty51      vcs6
core             rtc       tty23  tty52      vcsa
cpu              rtc0      tty24  tty53      vcsa1
cpu_dma_latency  sda       tty25  tty54      vcsa2
cuse             sda1      tty26  tty55      vcsa3
disk             sda2      tty27  tty56      vcsa4
dri              sda5      tty28  tty57      vcsa5
dvd              sg0       tty29  tty58      vcsa6
fb0              sg1       tty3   tty59      vcsu
fd               shm       tty30  tty6       vcsu1
full             snapshot  tty31  tty60      vcsu2
fuse             snd       tty32  tty61      vcsu3
hidraw0          sr0       tty33  tty62      vcsu4
hpet             stderr    tty34  tty63      vcsu5
hugepages        stdin     tty35  tty7       vcsu6
initctl          stdout    tty36  tty8       vfio
input            tty       tty37  tty9       vga_arbiter
kmsg             tty0      tty38  ttyS0      vhci
log              tty1      tty39  ttyS1      vhost-net
loop-control     tty10     tty4   ttyS2      vhost-vsock
mapper           tty11     tty40  ttyS3      zero
mem              tty12     tty41  uhid
mqueue           tty13     tty42  uinput
net              tty14     tty43  urandom
null             tty15     tty44  vboxguest
steve@linux-box:~$
```

Now, we know that the full path to our `sda`drive is `/dev/sda`.

## Analyzing drives space usage

Now that we know how to find available devices and partitions, it can be usefull to know a bit more about their usage. For example we need to know how much free space is left on each of them. Let's use the `df` utility to retreive some informations:

```
steve@linux-box:~$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
udev             8172752       0   8172752   0% /dev
tmpfs            1639216    1180   1638036   1% /run
/dev/sda1       19480400 4953084  13512432  27% /
tmpfs            8196076       0   8196076   0% /dev/shm
tmpfs               5120       4      5116   1% /run/lock
tmpfs            1639212     112   1639100   1% /run/user/1000
steve@linux-box:~$ 
```

By default `df` uses block size informations which is not really human friendly. Let's get some more readable numbers:

```
steve@linux-box:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            7.8G     0  7.8G   0% /dev
tmpfs           1.6G  1.2M  1.6G   1% /run
/dev/sda1        19G  4.8G   13G  27% /
tmpfs           7.9G     0  7.9G   0% /dev/shm
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           1.6G  112K  1.6G   1% /run/user/1000
steve@linux-box:~$ 
```

Now we see volume size in Go.

- Filesystem: name of the file system.

- Size: size of the file system in Go

- Used: space used on file system in Go

- Avail: available space on file system in Go

- Use%: percentage of used space on file system

- Mounted on: the mount point in the system

You can also get detailed informations about a specific drive or volume:

```
steve@linux-box:~$ df /dev/sda -h
Filesystem      Size  Used Avail Use% Mounted on
udev            7.8G     0  7.8G   0% /dev
steve@linux-box:~$
```

This can be handy if you need to retreive those informations in a script.

## Analyzing drives partitions

### The fdisk quest

We found our drives and partitions, we now see their space usage, but what about file systems and advanced properties of each partition ? We now need to use `fdisk`, a tool designed to manipulate disks partition table.

```
steve@linux-box:~$ fdisk --help
bash: fdisk: command not found
steve@linux-box:~$
```

Woops! `fdisk` is a standard tool to manage partitions but it doens seem to be available. Let's dig a bit deeper and have a look at `man fdisk`

```
FDISK(8)                                                          System Administration                                                          FDISK(8)

NAME
       fdisk - manipulate disk partition table

SYNOPSIS
       fdisk [options] device
       fdisk -l [device...]
... 
```

Ok, if there is a *man page* we can assume that `fdisk` is available ... somewhere.

```
steve@linux-box:~$ find / -executable -name fdisk 2> /dev/null
/usr/share/doc/fdisk
/usr/sbin/fdisk
steve@linux-box:~$ 
```

Here we searched for executable files named `fdisk` from the root and redirected errors on STDERR to `/dev/null` to get a clean output.

`/usr/sbin/fdisk` is the one we are looking for. If we can't call it without specifying a full path, this means `/usr/sbin` is not included in `PATH`, let's verify:

```
steve@linux-box:~$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
steve@linux-box:~$ 
```

> This behaviour is specific to Debian (and perhaps some other distributions). On Ubuntu, for example, `/usr/sbin` is included in `PATH` by default.

Now, let's try to get a list of our partitions...

```
steve@linux-box:~$ /usr/sbin/fdisk -l
fdisk: cannot open /dev/sda: Permission denied
steve@linux-box:~$ 
```

Manipulating partitions is not trivial. That's why we need to get elevated priviledges to use `fdisk`

```
steve@linux-box:~$ sudo /usr/sbin/fdisk -l

Disk /dev/sda: 20 GiB, 21474836480 bytes, 41943040 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xec67cdb9

Device     Boot    Start      End  Sectors  Size Id Type
/dev/sda1  *        2048 39942143 39940096   19G 83 Linux
/dev/sda2       39944190 41940991  1996802  975M  5 Extended
/dev/sda5       39944192 41940991  1996800  975M 82 Linux swap / Solaris
steve@linux-box:~$ 
```

As you can see we now have all informations about the drive, its size, model, and the detail of each partition on the drive:

- Device : path of the partition

- Boot : is the partition flagged as bootable or not

- Start : first block of the partition

- End : last block of the partition

- Secotrs : number of sectors of the drive

- Size : partition size

- Id : the partition type ID

- Type : Type of the partition

```
00 Empty            24 NEC DOS          81 Minix / old Lin  bf Solaris        
01 FAT12            27 Hidden NTFS Win  82 Linux swap / So  c1 DRDOS/sec (FAT-
02 XENIX root       39 Plan 9           83 Linux            c4 DRDOS/sec (FAT-
03 XENIX usr        3c PartitionMagic   84 OS/2 hidden or   c6 DRDOS/sec (FAT-
04 FAT16 <32M       40 Venix 80286      85 Linux extended   c7 Syrinx         
05 Extended         41 PPC PReP Boot    86 NTFS volume set  da Non-FS data    
06 FAT16            42 SFS              87 NTFS volume set  db CP/M / CTOS / .
07 HPFS/NTFS/exFAT  4d QNX4.x           88 Linux plaintext  de Dell Utility   
08 AIX              4e QNX4.x 2nd part  8e Linux LVM        df BootIt         
09 AIX bootable     4f QNX4.x 3rd part  93 Amoeba           e1 DOS access     
0a OS/2 Boot Manag  50 OnTrack DM       94 Amoeba BBT       e3 DOS R/O        
0b W95 FAT32        51 OnTrack DM6 Aux  9f BSD/OS           e4 SpeedStor      
0c W95 FAT32 (LBA)  52 CP/M             a0 IBM Thinkpad hi  ea Linux extended 
0e W95 FAT16 (LBA)  53 OnTrack DM6 Aux  a5 FreeBSD          eb BeOS fs        
0f W95 Ext'd (LBA)  54 OnTrackDM6       a6 OpenBSD          ee GPT            
10 OPUS             55 EZ-Drive         a7 NeXTSTEP         ef EFI (FAT-12/16/
11 Hidden FAT12     56 Golden Bow       a8 Darwin UFS       f0 Linux/PA-RISC b
12 Compaq diagnost  5c Priam Edisk      a9 NetBSD           f1 SpeedStor      
14 Hidden FAT16 <3  61 SpeedStor        ab Darwin boot      f4 SpeedStor      
16 Hidden FAT16     63 GNU HURD or Sys  af HFS / HFS+       f2 DOS secondary  
17 Hidden HPFS/NTF  64 Novell Netware   b7 BSDI fs          fb VMware VMFS    
18 AST SmartSleep   65 Novell Netware   b8 BSDI swap        fc VMware VMKCORE 
1b Hidden W95 FAT3  70 DiskSecure Mult  bb Boot Wizard hid  fd Linux raid auto
1c Hidden W95 FAT3  75 PC/IX            bc Acronis FAT32 L  fe LANstep        
1e Hidden W95 FAT1  80 Old Minix        be Solaris boot     ff BBT          
```

### About partitions

#### MBR vs GPT

MBR, GPT are two different way to manage drives and partitions.

MBR (Master Boot Record) is the old traditionnal way which only allows four main partitions and a maximum disk size of 2To. MBR also contains a boot loader written in the forst blocks of the drive.

GPT (GUID Partition Table) can have up to 128 partition entries and doesn't contain a boot loader. GPT is only supported by recent BIOS called UEFI. Instead of loading the boot loader from the MBR, UEFI Bios uses EFI images from EFI System Partition to boot.

> The debian installer with automatically choose between MBR and GPT scheme depending on the hardware.

#### Primary and Extended partitions (MBR)

Traditionnaly there are two main partition types: primary and extended. The original partionning scheme for PCs drives only allow four primary partitions, this means that there are only four entires in the partition table.

To create more than four partitions you can use one of the four available to create a extended partition which works like a container for smaller logical partitions.

#### The swap partition

> Swap space under Debian and other GNU/Linux based operating systems is a form of virtual memory. Simply put this means that if the system runs out of physical memory (RAM), then it will transfer some of the lesser used data in RAM to this space. Swap space is also fundamental to the processes of the "[Suspend](https://wiki.debian.org/Suspend)" and "Hibernate" features of Linux. Swap is primarily setup as a separate dedicated partition(s) (recommended) or as a specially created file(s) residing on an existing file system.

from [Swap - Debian Wiki](https://wiki.debian.org/Swap)

## Drive partitionning

Now that wa know how to gather drives informations, it's time to learn how to manage a new drive. For the xample I attached a new virtual hard drive to my virtual machine.

First of all we need to find the new drive.

```
steve@linux-box:~$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   20G  0 disk
├─sda1   8:1    0   19G  0 part /
├─sda2   8:2    0    1K  0 part
└─sda5   8:5    0  975M  0 part [SWAP]
sdb      8:16   0   40G  0 disk
sr0     11:0    1 1024M  0 rom
steve@linux-box:~$
```

As you can see, a new drive named `sdb` appeared. The new drive has no partition and cannot be used in its current state. Let's see what `fdisk` knows about the new drive...

```
steve@linux-box:~$ sudo /usr/sbin/fdisk -l

Disk /dev/sdb: 40 GiB, 42949672960 bytes, 83886080 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

Disk /dev/sda: 20 GiB, 21474836480 bytes, 41943040 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xec67cdb9

Device     Boot    Start      End  Sectors  Size Id Type
/dev/sda1  *        2048 39942143 39940096   19G 83 Linux
/dev/sda2       39944190 41940991  1996802  975M  5 Extended
/dev/sda5       39944192 41940991  1996800  975M 82 Linux swap / Solaris
steve@linux-box:~$
```

Here we see that the drive exists, but has no partition or even any partition table.

### `fidisk`in interactive mode

`fdisk` works in an interactive mode when used to alter a drive partition table. 

```
steve@linux-box:~$ sudo /usr/sbin/fdisk /dev/sdb

Welcome to fdisk (util-linux 2.36.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help):
```

`fdisk` has a small built-in help. 

```
Command (m for help): m

Help:

  GPT
   M   enter protective/hybrid MBR

  Generic
   d   delete a partition
   F   list free unpartitioned space
   l   list known partition types
   n   add a new partition
   p   print the partition table
   t   change a partition type
   v   verify the partition table
   i   print information about a partition

  Misc
   m   print this menu
   x   extra functionality (experts only)

  Script
   I   load disk layout from sfdisk script file
   O   dump disk layout to sfdisk script file

  Save & Exit
   w   write table to disk and exit
   q   quit without saving changes

  Create a new label
   g   create a new empty GPT partition table
   G   create a new empty SGI (IRIX) partition table
   o   create a new empty DOS partition table
   s   create a new empty Sun partition table


Command (m for help):
```

#### Creating the partition table

First of all we need to create the partition table. Depending on our needs we will choose between *DOS (aka MBR)* or *GPT* scheme.

Let's create a simple *DOS* partition table.

```
Command (m for help): o
Created a new DOS disklabel with disk identifier 0x408d7dba.

Command (m for help):
```

The partition table has been created. Note that changes will only be applied when we will ask `fdisk` to write the table to the disk.

Let's create our first 5 Go primary patition...

```
Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-83886079, default 2048):

Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-83886079, default 83886079): +5G

Created a new partition 1 of type 'Linux' and of size 5 GiB.

Command (m for help):
```

### Checking the parition table

Let's see our parition table

```
Command (m for help): p

Disk /dev/sdb: 40 GiB, 42949672960 bytes, 83886080 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x408d7dba

Device     Boot Start      End  Sectors Size Id Type
/dev/sdb1        2048 10487807 10485760   5G 83 Linux

Command (m for help):
```

### Finding out unpartitioned space

We wan also find out how much space is still available on the drive...

```
Command (m for help): F
Unpartitioned space /dev/sdb: 35 GiB, 37579915264 bytes, 73398272 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes

   Start      End  Sectors Size
10487808 83886079 73398272  35G

Command (m for help):
```

### Applying changes

Let's write the changes to the disk and verify the result...

```
Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.

steve@linux-box:~$
```

```
steve@linux-box:~$ sudo /usr/sbin/fdisk -l

Disk /dev/sdb: 40 GiB, 42949672960 bytes, 83886080 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x408d7dba

Device     Boot Start      End  Sectors Size Id Type
/dev/sdb1        2048 10487807 10485760   5G 83 Linux


Disk /dev/sda: 20 GiB, 21474836480 bytes, 41943040 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xec67cdb9

Device     Boot    Start      End  Sectors  Size Id Type
/dev/sda1  *        2048 39942143 39940096   19G 83 Linux
/dev/sda2       39944190 41940991  1996802  975M  5 Extended
/dev/sda5       39944192 41940991  1996800  975M 82 Linux swap / Solaris
steve@linux-box:~$
```

We now have a usable parition named `sdb1` but we cannot write files to it yet because there is no file system defined, we still need to format the partition.

## Formatting volumes

Before writing anything the the disk we need to define a file system four our new parition.

### Choosing the right file system

Each file system has its own properties and limits. some are supported everywhere like `FAT` others are proprietary like `NTFS`, chossing the right file system is not trivial.

Here is a list of the most common file systems and their main characteristics:

| File system | OS Compatibility | Max File Size | Max Volume Size |
| ----------- | ---------------- | ------------- | --------------- |
| FAT16       | Any              | 32MB          | 32MB            |
| FAT32       | Any              | 4GB           | 16TB            |
| exFAT       | Any recent OS    | 16EB          | 64ZB            |
| NTFS        | Windows OS       | 16TB          | 16TB            |
| ext3        | Unix/Linux/MacOS | 16GB          | 32TB            |
| ext4        | Unix/Linux/MacOS | 16TB          | 1EB             |

Most linux system actually use `ext4` as the main file system. But if for any reason you need your drive to be readable by other systems (external drives, usb drives, ...) you should go for `FAT32` or `exFAT``.

You can find more about file systems here: [Comparison of file systems - Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_file_systems)

### Formatting

As we are working on linux let's stick with `ext4` as file system for our new partition.

the main tool for creating a file system is `mkfs` which is located in the same directory as `fdisk` so only accessible using full path by default.

```
steve@linux-box:~$ /usr/sbin/mkfs --help

Usage:
 mkfs [options] [-t <type>] [fs-options] <device> [<size>]

Make a Linux filesystem.

Options:
 -t, --type=<type>  filesystem type; when unspecified, ext2 is used
     fs-options     parameters for the real filesystem builder
     <device>       path to the device to be used
     <size>         number of blocks to be used on the device
 -V, --verbose      explain what is being done;
                      specifying -V more than once will cause a dry-run
 -h, --help         display this help
 -V, --version      display version

For more details see mkfs(8).
steve@linux-box:~$
```

Think about `mkfs` like the general tool to create several file systems. It's in fact just some kind of mapper that will call the right tool depending on the file system you choose.

As stated in the man page, this tool is deprecated and we should prefer using specific command for each file system like `mkfs.ext4`to create an `ext4` file system.

Let's see what we can find...

```
steve@linux-box:~$ ls /usr/sbin/ | grep -e ^mkfs.
mkfs.bfs
mkfs.cramfs
mkfs.exfat
mkfs.ext2
mkfs.ext3
mkfs.ext4
mkfs.fat
mkfs.minix
mkfs.msdos
mkfs.ntfs
mkfs.vfat
steve@linux-box:~$
```

As you can see, there is a specific tool for each filesystem.

Let's get some quick help

```
steve@linux-box:~$ /usr/sbin/mkfs.ext4 --help
/usr/sbin/mkfs.ext4: invalid option -- '-'
Usage: mkfs.ext4 [-c|-l filename] [-b block-size] [-C cluster-size]
        [-i bytes-per-inode] [-I inode-size] [-J journal-options]
        [-G flex-group-size] [-N number-of-inodes] [-d root-directory]
        [-m reserved-blocks-percentage] [-o creator-os]
        [-g blocks-per-group] [-L volume-label] [-M last-mounted-directory]
        [-O feature[,...]] [-r fs-revision] [-E extended-option[,...]]
        [-t fs-type] [-T usage-type ] [-U UUID] [-e errors_behavior][-z undo_file]
        [-jnqvDFSV] device [blocks-count]
steve@linux-box:~$
```

Let's now create the file system, the process is quite straightforward...

```
steve@linux-box:~$ sudo /usr/sbin/mkfs.ext4 /dev/sdb1
mke2fs 1.46.2 (28-Feb-2021)
Creating filesystem with 1310720 4k blocks and 327680 inodes
Filesystem UUID: d3ace887-686d-4504-8c9b-c0e25ae47bb2
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done
Writing inode tables: done
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done

steve@linux-box:~$ sudo /usr/sbin/fdisk -l
```

We now have a working parition with an `ext4` file system.

We can verify this using the `fdisk` command...

```
steve@linux-box:~$ lsblk -f
NAME   FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINT
sda
├─sda1 ext4   1.0         02a24340-e1cc-46c4-8f66-8a48c40c206d   12.9G    25% /
├─sda2
└─sda5 swap   1           e4520c4e-722f-48af-b3a6-198a99b7e30c                [SWAP]
sdb
└─sdb1 ext4   1.0         d3ace887-686d-4504-8c9b-c0e25ae47bb2
sr0
steve@linux-box:~$
```

Digging a bit deeper you would notice that `/dev/sdb1` won't show in the `df` output.

```
steve@linux-box:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            7.8G     0  7.8G   0% /dev
tmpfs           1.6G  1.2M  1.6G   1% /run
/dev/sda1        19G  4.8G   13G  27% /
tmpfs           7.9G     0  7.9G   0% /dev/shm
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           1.6G  112K  1.6G   1% /run/user/1000
steve@linux-box:~$
```

The reason is simple, our partition is ready but it's actually not mounted in the system. But that's another story ;-)

## Exercices

- Attach a new 20 Go drive to your machine

- Create a DOS partition table on it

- Create the following parition scheme:
  
     - First parition: 5Go, ext4
  
     - Second parition: 5Go, exFAT
  
     - Third parition: space remaining, FAT32

- Verify the partition table

- Suppress the second and third partition

- Create a new parition with all remaining space with an ext4 file system.

- Verify the parition table.
