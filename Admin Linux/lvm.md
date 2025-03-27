# Logical Volume Management (LVM)

## Introduction

LVM (Logical Volume Manager) is a system of managing logical volumes, or filesystems, that is more advanced and flexible than the traditional method of partitioning a disk.

## Main concepts

![](./assets/LVM-basic-structure.png)

### Volume groups

A volume group is a named collection of physical and logical volumes.

### Physical volumes

Physical volumes correspond to the disks but can also be disks partitions, meta-devices or loopback files. They provide space to store logical volumes.

### Logical volumes

Logical volumes correspond to partitions, they hold a filesystem, but they get names, can span across multiple disks and do not need to be contiguous.

## LVM specific features

Unlike traditionnal disks management systems, with LVM most operations can be done one the fly. LVM also offers some interresting features...

### Resizing partitions

LVM can expand a partition while in use. The expansion doesn't need to be adjacent and can be anywhere in the volume group.

### Moving partitions

LVM allows to move a partition on the fly without risking data corruption event if the system halts. This allows for example to move a partition to a new disk without any disruption.

### No partitions limit

LVM allows you to create as many logical volumes as you need.

### Snapshots

A snapshot is an image of a logical volume frozen in time. It can be used to create a file system backup or to create a restore point without shutting down the computer. It can also be mounted and edited without altering the original volume.

## Using LVM

### Using LVM during the installation process

The following screenshots refers to the installation of a Debian 11 Virtual Machine using Virtual Box. The VM has a 25GB Disk and EFI Bios features were enabled (but not required for LVM).

During the instllation process, after configuring the hostname, the username etc, you reach the disk parition procedure. The first thing to do is to choose to use LVM as disk management.

![](./assets/debian_install_lvm_01.png)

The next step is to choose the disk where you can to create the LVM structure.

![](./assets/debian_install_lvm_02.png)

Once you choosed the disk, you can choose if you want to keepe everything in a single parition (or Logical Volume for LVM) or ... for advanced usage ... separate several mount points in different logical volumes. This allows for example to move a partition to another disks later.

![](./assets/debian_install_lvm_03.png)

We then need to confirm we want to write the LVM structure to the disk.

![](./assets/debian_install_lvm_04.png)

We can now choose how much space of the disk we want to use. `max` will make LVM use all available disk space, but you can also specify a size (e.g. 10GB) or a percentage of the disk size (e.g. 20%)

![](./assets/debian_install_lvm_05.png)

The VM is configured to emulate an EFI Bios, this screens just ask us to confirm we want to use an UEFI installation mode.

![](./assets/debian_install_lvm_06.png)

The last screen of the disk management process is a recap. We can see here that LVM will create a Virtual Group named *debian-vg* with several logical volumes:

- home: will be mounted as `/home`

- root: will be mounted as `/`

- swap_1: will be mounted as the swap partition

- tmp: will be mounted as `/tmp`

- var: will be mounted as `/var`

The nice thing with such separations is that we could further expand the logical volumes separately as needed by adding new physical volumes, added them to the logical group and then extending the partition of the logical volume.

![](./assets/debian_install_lvm_07.png)

Once you hit the *Continue* button, the installation process will continue as usual.

### Managing LVM from command-line

On debian systems, LVM utilities, like other disk management tools, are stored in `/usr/sbin` which is not always included in `$PATH`.

In the following examples, we'll assume the `/usr/sbin/` directory has been added to the `$PATH`.

#### Analysing current LVM configuration

First of all let's see what we got after the installation process using the well kown `lsblk`command.

```
sdejongh@debian:~$ lsblk
NAME                  MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                     8:0    0   25G  0 disk 
├─sda1                  8:1    0  512M  0 part /boot/efi
├─sda2                  8:2    0  488M  0 part /boot
└─sda3                  8:3    0   24G  0 part 
  ├─debian--vg-root   254:0    0  4.9G  0 lvm  /
  ├─debian--vg-var    254:1    0  1.9G  0 lvm  /var
  ├─debian--vg-swap_1 254:2    0  976M  0 lvm  [SWAP]
  ├─debian--vg-tmp    254:3    0  412M  0 lvm  /tmp
  └─debian--vg-home   254:4    0 15.9G  0 lvm  /home
sr0                    11:0    1 1024M  0 rom  
```

As you can see we have several LVM related items in the list, and as explained in the introduction, we should find three kind of elements: physical volumes, virtual groups and logical volumes.

We can list existing virtual groups using the `vgdisplay` command.

```
sdejongh@debian:~$ sudo vgdisplay
  --- Volume group ---
  VG Name               debian-vg
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  6
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                5
  Open LV               5
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <24.02 GiB
  PE Size               4.00 MiB
  Total PE              6149
  Alloc PE / Size       6149 / <24.02 GiB
  Free  PE / Size       0 / 0   
  VG UUID               e8hwV4-pZhY-hBqh-tinb-zq3A-29HV-elb7hR

sdejongh@debian:~$
```

So here is our virtual group named `debian-vg` which includes one physical volume ans is used by 5 logical volumes.

We can get a more compact view using the `-C` (Column) option.

```
sdejongh@debian:~$ sudo vgdisplay -C
  VG        #PV #LV #SN Attr   VSize   VFree
  debian-vg   1   5   0 wz--n- <24.02g    0 
sdejongh@debian:~$
```

We can also use the `pvdisplay` command to list the physical volumes.

```
sdejongh@debian:~$ sudo pvdisplay -C -a
  PV         VG        Fmt  Attr PSize   PFree
  /dev/sda1                 ---       0     0 
  /dev/sda2                 ---       0     0 
  /dev/sda3  debian-vg lvm2 a--  <24.02g    0 
sdejongh@debian:~$
```

The `-a` option make the command include all volumes even non-lvm ones.

We can see here that the `/dev/sda3` partition has been add as a lvm physical volume and is include in the `debian-vg` virtual group.

Finally we can get all logical volumes using the `lvdisplay` command.

```
sdejongh@debian:~$ sudo lvdisplay -C
  LV     VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  home   debian-vg -wi-ao---- <15.88g                                                    
  root   debian-vg -wi-ao----  <4.86g                                                    
  swap_1 debian-vg -wi-ao---- 976.00m                                                    
  tmp    debian-vg -wi-ao---- 412.00m                                                    
  var    debian-vg -wi-ao----  <1.93g                                                    
sdejongh@debian:~$ 
```

Here you can see that the `debian-vg` virtual group has been used to create 5 logical volumes.

> Note: You could probably find the `pvs`, `vgs`and `lvs`commands also used to gather LVM informations and are completely equivalent to `pgdisplay`, `vgdisplay`and `lvdisplay`

#### Configure LVM using command-line

Let's dig a bit deeper. For the following examples, I attached a new 50GB virtual disk `/dev/sdb` to te virtual machine.

```
sdejongh@debian:~$ lsblk
NAME                  MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                     8:0    0   25G  0 disk 
├─sda1                  8:1    0  512M  0 part /boot/efi
├─sda2                  8:2    0  488M  0 part /boot
└─sda3                  8:3    0   24G  0 part 
  ├─debian--vg-root   254:0    0  4.9G  0 lvm  /
  ├─debian--vg-var    254:1    0  1.9G  0 lvm  /var
  ├─debian--vg-swap_1 254:2    0  976M  0 lvm  [SWAP]
  ├─debian--vg-tmp    254:3    0  412M  0 lvm  /tmp
  └─debian--vg-home   254:4    0 15.9G  0 lvm  /home
sdb                     8:16   0   50G  0 disk 
sr0                    11:0    1 1024M  0 rom  
sdejongh@debian:~
```

The first thing to to is to create a new physical volume on the disk. This can be done for the while disk or for a specific partition.

##### Physical volume creation

Let's make a physical volume with the whole physical drive using the `pvcreate`command.

```
sdejongh@debian:~$ sudo pvcreate /dev/sdb
  Physical volume "/dev/sdb" successfully created.
sdejongh@debian:~$ 
```

We can verify that the disk has been enabled for LVM using the `lvmdiskscan` command.

```
sdejongh@debian:~$ sudo lvmdiskscan 
  /dev/sda1 [     512.00 MiB] 
  /dev/sda2 [     488.00 MiB] 
  /dev/sda3 [      24.02 GiB] LVM physical volume
  /dev/sdb  [      50.00 GiB] LVM physical volume
  0 disks
  2 partitions
  1 LVM physical volume whole disk
  1 LVM physical volume
sdejongh@debian:~$
```

As you can see there are two physical volumes: `/dev/sda3` which is a partition and `/dev/sdb` which is the new disk.

From here we could either create a new volume group using the `vgcreate` command or either extend the `debian-vg`volume group with the new physical volume with the `vgextend` command.

##### Virtual group creation

Let's create a new volume group named `custom-vg`.

```
sdejongh@debian:~$ sudo vgcreate custom-vg /dev/sdb
  Volume group "custom-vg" successfully created
sdejongh@debian:~$
```

We can now verify the result using the `vgs`command (`vgdisplay -C` would do the same).

```
sdejongh@debian:~$ sudo vgs
  VG        #PV #LV #SN Attr   VSize   VFree  
  custom-vg   1   0   0 wz--n- <50.00g <50.00g
  debian-vg   1   5   0 wz--n- <24.02g      0 
sdejongh@debian:~$
```

The new `custom-vg` volume group had been created and has 50GB free space.

##### Logical volume creation

Let's now create a new logical volume.

```
sdejongh@debian:~$ sudo lvcreate -n sample-lv -L10G custom-vg
  Logical volume "sample-lv" created.
sdejongh@debian:~$
```

This created a new 10GB logical voulme named `sample-lv` out of the `custom-vg`volume group.

We can see the logical volumes using the `vgs` command.

```
sdejongh@debian:~$ sudo lvs
  LV        VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  sample-lv custom-vg -wi-a-----  10.00g                                                    
  home      debian-vg -wi-ao---- <15.88g                                                    
  root      debian-vg -wi-ao----  <4.86g                                                    
  swap_1    debian-vg -wi-ao---- 976.00m                                                    
  tmp       debian-vg -wi-ao---- 412.00m                                                    
  var       debian-vg -wi-ao----  <1.93g                                                    
sdejongh@debian:~$
```

As we only used 10GB from the `custom-vg`volume groupe, it should still have plenty a free space left.

```
sdejongh@debian:~$ sudo vgs
  VG        #PV #LV #SN Attr   VSize   VFree  
  custom-vg   1   1   0 wz--n- <50.00g <40.00g
  debian-vg   1   5   0 wz--n- <24.02g      0 
sdejongh@debian:~$ 
```

The logical volume can now be used as any classical partition.

```
sdejongh@debian:~$ lsblk
NAME                    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                       8:0    0   25G  0 disk 
├─sda1                    8:1    0  512M  0 part /boot/efi
├─sda2                    8:2    0  488M  0 part /boot
└─sda3                    8:3    0   24G  0 part 
  ├─debian--vg-root     254:0    0  4.9G  0 lvm  /
  ├─debian--vg-var      254:1    0  1.9G  0 lvm  /var
  ├─debian--vg-swap_1   254:2    0  976M  0 lvm  [SWAP]
  ├─debian--vg-tmp      254:3    0  412M  0 lvm  /tmp
  └─debian--vg-home     254:4    0 15.9G  0 lvm  /home
sdb                       8:16   0   50G  0 disk 
└─custom--vg-sample--lv 254:5    0   10G  0 lvm  
sr0                      11:0    1 1024M  0 rom  
sdejongh@debian:~$
```

So let's create an `ext4` file system on the logical volume

```
sdejongh@debian:~$ sudo mkfs.ext4 /dev/custom-vg/sample-lv 
mke2fs 1.46.2 (28-Feb-2021)
Creating filesystem with 2621440 4k blocks and 655360 inodes
Filesystem UUID: 42d1d3c5-e162-4c30-8d13-117d7dd9bd90
Superblock backups stored on blocks: 
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done 

sdejongh@debian:~$
```

Logical volumes are referenced under the `/dev` directory following this simple sheme: `/dev/<vg_name>/<lv_name>`

##### Resizing a logical volume

A logical volume can be resized `lvresize`, reduced `lvreduce` or extended `lvextend`.

We can for example extend the logical volume to 15GB

```
sdejongh@debian:~$ sudo lvextend -L 15G -r /dev/custom-vg/sample-lv
fsck from util-linux 2.36.1
/dev/mapper/custom--vg-sample--lv: clean, 11/655360 files, 66753/2621440 blocks
  Size of logical volume custom-vg/sample-lv changed from 10.00 GiB (2560 extents) to 15.00 GiB (3840 extents).
  Logical volume custom-vg/sample-lv successfully resized.
resize2fs 1.46.2 (28-Feb-2021)
Resizing the filesystem on /dev/mapper/custom--vg-sample--lv to 3932160 (4k) blocks.
The filesystem on /dev/mapper/custom--vg-sample--lv is now 3932160 (4k) blocks long.

sdejongh@debian:~$
```

The `-L` option gives the target volume size. The `-r` option is used to resize the filesystem.

The process of resizing or reducing is almost the same except that you cannot reduce the volume size more than available free space.

##### Merging volume groups

It's also possible to merge two volume groups. Le'ts say we want to merge the `custom-vg` into the `debian-vg` volume group, we first need to deactivate the logical volumes of the `custom-vg` group.

```
sdejongh@debian:~$ sudo lvchange -a n /dev/custom-vg/sample-lv
```

Now we can merge both groups.

```
sdejongh@debian:~$ sudo vgmerge debian-vg custom-vg
  WARNING: updating old metadata to 7 on /dev/sdb for VG debian-vg.
  Volume group "custom-vg" successfully merged into "debian-vg"
sdejongh@debian:~$
```

We now have one volume group containing all the physical volumes

```
sdejongh@debian:~$ sudo vgs
  VG        #PV #LV #SN Attr   VSize   VFree  
  debian-vg   2   6   0 wz--n- <74.02g <35.00g
sdejongh@debian:~$
```

We can now reactivate the `sample-lv` logical volume.

```
sdejongh@debian:~$ sudo lvchange -a y /dev/debian-vg/sample-lv
```

And finally check our logical volumes

```
sdejongh@debian:~$ sudo lvs
  LV        VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  home      debian-vg -wi-ao---- <15.88g                                                    
  root      debian-vg -wi-ao----  <4.86g                                                    
  sample-lv debian-vg -wi-a-----  15.00g                                                    
  swap_1    debian-vg -wi-ao---- 976.00m                                                    
  tmp       debian-vg -wi-ao---- 412.00m                                                    
  var       debian-vg -wi-ao----  <1.93g                                                    
sdejongh@debian:~$
```

Because we merged both volume groups, we pu all physical volumes into `debian-vg` this means that the 35GB free space available in the old `custom-vg` is now available in the `debian-vg`. We can use this free space to extend any logical volume of the `debian-vg`.

Let's finally extend the `home` logical volume using all remaining free space in `debian-vg`.

```
sdejongh@debian:~$ sudo lvextend -r -l +100%FREE /dev/debian-vg/home
  Size of logical volume debian-vg/home changed from <15.88 GiB (4065 extents) to <50.88 GiB (13024 extents).
  Logical volume debian-vg/home successfully resized.
resize2fs 1.46.2 (28-Feb-2021)
Filesystem at /dev/mapper/debian--vg-home is mounted on /home; on-line resizing required
old_desc_blocks = 2, new_desc_blocks = 7
The filesystem on /dev/mapper/debian--vg-home is now 13336576 (4k) blocks long.

sdejongh@debian:~$
```

Note the `-l +100%FREE`  option which specifies that we want to add 100% of the available free space to the actual logical volume size.

The `-r` option is used to resize the filesystem at the same time.
