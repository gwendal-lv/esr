# Underdstanding UDEV

## What is udev ?

Udev (userspace /dev) is a Linux sub-system for dynamic device detection and management, since kernel version 2.6. It’s a replacement of [devfs](https://wiki.debian.org/DevFS) and hotplug.
It dynamically creates or removes device nodes (an interface to a device driver that appears in a file system as if it were an ordinary file, stored under the /dev directory) at boot time or if you add a device to or remove a device from the system.
It then propagates information about a device or changes to its state to user space.
The goal of udev, as stated by the [project](https://www.linux.com/news/udev-introduction-device-management-modern-linux-system/) is:

* Run in user space.
* Create persistent device names, take the device naming out of kernel space and implement rule based device naming.
* Create a dynamic /dev with device nodes for devices present in the system and allocate major/minor numbers dynamically.
* Provide a user space API to access the device information in the system.
  One of the pros of udev is that it can use persistent device names to guarantee consistent naming of devices across reboots, despite their order of discovery.
  This feature is useful because the kernel simply assigns unpredictable device names based on the order of discovery.

## How does it work?

![](./assets/userspace.png)

As udev runs in [userland](https://unix.stackexchange.com/questions/137820/whats-the-difference-of-the-userland-vs-the-kernel), it runs a service which on most modern distributions is controlled by [systemd](./learning_systemd.md). If we have a look at our running processes and search for `udev` we find the following.

```
sdejongh@debian-base:~$ ps aux | grep udev
root         290  0.1  0.0  23552  6692 ?        Ss   08:19   0:00 /lib/systemd/systemd-udevd
sdejongh    2215  0.0  0.0   6180   640 pts/0    S+   08:20   0:00 grep udev
sdejongh@debian-base:~$
```

The first line hints us to a process run by root with a pretty low `PID`. It seems to be part of the `systemd` *suite* of programs. As always, let's have a look at the `man systemd-udevd` to learn what it is and how we can interact with it.

```
DESCRIPTION
       systemd-udevd listens to kernel uevents. For every event, systemd-udevd executes matching instructions
       specified in udev rules. See udev(7).

       The behavior of the daemon can be configured using udev.conf(5), its command line options, environment
       variables, and on the kernel command line, or changed dynamically with udevadm control.
```

The description is pretty solid and points us to a specific program we can use to *talk* to the daemon. This is very similar to how we have been talking to `systemd` via `systemctl` but here, to talk to `systemd-udevd`, we'll use `udevadm`.

## Managing UDEV

### Monitoring events

To analyse what udev is receiving we can monitor it with `sudo udevadm monitor`.
You'll see see the following output with a *blinking* cursor on the last line to show we're monitoring *live*.

```
sdejongh@debian-base:~$ sudo udevadm monitor 
monitor will print the received events for:
UDEV - the event which udev sends out after rule processing
KERNEL - the kernel uevent
```

If we now **plug in** a device we'll see a bunch of messages arriving.
He I **added** a USB drive by plugging it into the **USB** port.
You can see a lot of *usb* messages so it's safe to say I plugged in a USB device.
Do notice that once the device is fully recognized and initialized by the system the messages stop.
Udev has done it's work and will remain silent until some changes happen to the system.

```
KERNEL[50.273040] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1 (usb)
KERNEL[50.275045] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0 (usb)
KERNEL[50.275246] bind     /devices/pci0000:00/0000:00:0c.0/usb2/2-1 (usb)
UDEV  [50.301161] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1 (usb)
KERNEL[50.317838] add      /devices/virtual/workqueue/scsi_tmf_3 (workqueue)
KERNEL[50.318205] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3 (scsi)
KERNEL[50.318233] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/scsi_host/host3 (scsi_host)
KERNEL[50.318257] bind     /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0 (usb)
KERNEL[50.318269] add      /bus/usb/drivers/usb-storage (drivers)
KERNEL[50.318276] add      /module/usb_storage (module)
UDEV  [50.319489] add      /devices/virtual/workqueue/scsi_tmf_3 (workqueue)
UDEV  [50.320358] add      /module/usb_storage (module)
KERNEL[50.321052] add      /bus/usb/drivers/uas (drivers)
KERNEL[50.321075] add      /module/uas (module)
UDEV  [50.321376] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0 (usb)
UDEV  [50.321910] add      /bus/usb/drivers/uas (drivers)
UDEV  [50.322260] add      /bus/usb/drivers/usb-storage (drivers)
UDEV  [50.324566] bind     /devices/pci0000:00/0000:00:0c.0/usb2/2-1 (usb)
UDEV  [50.326007] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3 (scsi)
UDEV  [50.326770] add      /module/uas (module)
UDEV  [50.327093] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/scsi_host/host3 (scsi_host)
UDEV  [50.328496] bind     /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0 (usb)
KERNEL[51.345128] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0 (scsi)
KERNEL[51.345204] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0 (scsi)
KERNEL[51.345223] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_device/3:0:0:0 (scsi_device)
KERNEL[51.345429] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_disk/3:0:0:0 (scsi_disk)
KERNEL[51.345454] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_generic/sg2 (scsi_generic)
KERNEL[51.346111] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/bsg/3:0:0:0 (bsg)
UDEV  [51.347494] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0 (scsi)
UDEV  [51.349684] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0 (scsi)
UDEV  [51.352517] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_disk/3:0:0:0 (scsi_disk)
UDEV  [51.352861] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_generic/sg2 (scsi_generic)
UDEV  [51.352895] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_device/3:0:0:0 (scsi_device)
UDEV  [51.354504] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/bsg/3:0:0:0 (bsg)
KERNEL[51.375205] add      /devices/virtual/bdi/8:16 (bdi)
UDEV  [51.375672] add      /devices/virtual/bdi/8:16 (bdi)
KERNEL[51.385111] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb (block)
KERNEL[51.385146] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb/sdb1 (block)
KERNEL[51.412259] bind     /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0 (scsi)
UDEV  [51.448746] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb (block)
UDEV  [51.511758] add      /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb/sdb1 (block)
UDEV  [51.515049] bind     /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0 (scsi)
KERNEL[51.592970] add      /module/exfat (module)
UDEV  [51.595158] add      /module/exfat (module)
KERNEL[51.816112] change   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb/sdb1 (block)
UDEV  [51.874320] change   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb/sdb1 (block)
```

When I **unplug** the USB drive we get the following output. Notice the sequence of events here. The kernel reports changes which udev uses to **trigger** events and actions.

```
KERNEL[192.341891] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/bsg/3:0:0:0 (bsg)
KERNEL[192.342506] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_generic/sg2 (scsi_generic)
KERNEL[192.342576] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_device/3:0:0:0 (scsi_device)
KERNEL[192.342603] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_disk/3:0:0:0 (scsi_disk)
KERNEL[192.346394] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb/sdb1 (block)
UDEV  [192.347398] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_generic/sg2 (scsi_generic)
KERNEL[192.347890] remove   /devices/virtual/bdi/8:16 (bdi)
KERNEL[192.348125] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb (block)
KERNEL[192.348189] unbind   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0 (scsi)
KERNEL[192.348247] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0 (scsi)
UDEV  [192.348439] remove   /devices/virtual/bdi/8:16 (bdi)
UDEV  [192.348517] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_device/3:0:0:0 (scsi_device)
UDEV  [192.348556] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/bsg/3:0:0:0 (bsg)
UDEV  [192.349639] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb/sdb1 (block)
UDEV  [192.349703] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_disk/3:0:0:0 (scsi_disk)
UDEV  [192.351380] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb (block)
UDEV  [192.358745] unbind   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0 (scsi)
UDEV  [192.361215] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0 (scsi)
KERNEL[192.363195] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0 (scsi)
KERNEL[192.363259] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/scsi_host/host3 (scsi_host)
KERNEL[192.363277] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3 (scsi)
KERNEL[192.363404] unbind   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0 (usb)
KERNEL[192.363432] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0 (usb)
KERNEL[192.363854] unbind   /devices/pci0000:00/0000:00:0c.0/usb2/2-1 (usb)
KERNEL[192.363881] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1 (usb)
UDEV  [192.364134] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/scsi_host/host3 (scsi_host)
UDEV  [192.364375] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0 (scsi)
UDEV  [192.365142] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3 (scsi)
UDEV  [192.366112] unbind   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0 (usb)
UDEV  [192.370429] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0 (usb)
UDEV  [192.370453] unbind   /devices/pci0000:00/0000:00:0c.0/usb2/2-1 (usb)
UDEV  [192.370469] remove   /devices/pci0000:00/0000:00:0c.0/usb2/2-1 (usb)
KERNEL[192.383008] remove   /devices/virtual/workqueue/scsi_tmf_3 (workqueue)
UDEV  [192.383341] remove   /devices/virtual/workqueue/scsi_tmf_3 (workqueue)
```

> In Virtualbox you can add or remove USB devices via the menu bar of you virtual machine. If required enable USB3 support ine the VM settings.

We can use `udevadm` for more than just monitoring.

```
sdejongh@debian-base:~$ sudo udevadm --help
udevadm [--help] [--version] [--debug] COMMAND [COMMAND OPTIONS]

Send control commands or test the device manager.

Commands:
  info          Query sysfs or the udev database
  trigger       Request events from the kernel
  settle        Wait for pending udev events
  control       Control the udev daemon
  monitor       Listen to kernel and udev events
  test          Test an event run
  test-builtin  Test a built-in command

See the udevadm(8) man page for details.
sdejongh@debian-base:~$
```

### Gathering informations

#### Using external programs

Udev can be used to query device information via the `info` subcommand but there are a few other programs that are very handy to know.
We'll focus on USB devices for now, but keep in mind that udev manages everything connected to our system (network interfaces, graphic cards, ...).

My USB drive is **not** plugged in for now and below is the output of `lsusb`.

```
sdejongh@debian-base:~$ lsusb
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 002: ID 80ee:0021 VirtualBox USB Tablet
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
sdejongh@debian-base:~$ 
```

Next I plug it **in** and review the output of `lsusb`. A device is added but it's not saying much! You can see the device ID which is vendor dependant and eventually a few words describing the device.

```
dejongh@debian-base:~$ lsusb
Bus 002 Device 003: ID 0781:5591 SanDisk Corp. Ultra Flair
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 002: ID 80ee:0021 VirtualBox USB Tablet
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
sdejongh@debian-base:~$ 
```

The **hexadecimal** numbers you see listed are `VENDOR_ID:PROCUCT_ID` and can be used to digg deeper into a specific device. For this we use the `-d VENDOR_ID:PROCUCT_ID` argument, together with `-v` for verbosity.

```
sdejongh@debian-base:~$ lsusb -d 0781:5591 -v

Bus 002 Device 003: ID 0781:5591 SanDisk Corp. Ultra Flair
Couldn't open device, some information will be missing
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               3.20
  bDeviceClass            0 
  bDeviceSubClass         0 
  bDeviceProtocol         0 
  bMaxPacketSize0         9
  idVendor           0x0781 SanDisk Corp.
  idProduct          0x5591 Ultra Flair
  bcdDevice            1.00
  iManufacturer           1  USB
  iProduct                2  SanDisk 3.2Gen1
  iSerial                 3 01010ac4b3c45b97338088a097b49464e5af8a4ce19fef478b0ce1d7f1e75b3a580e00000000000000000000b7e9a6f0ff09260091558107b52921a5
  bNumConfigurations      1
  Configuration Descriptor:
    bLength                 9
    bDescriptorType         2
    wTotalLength       0x002c
    bNumInterfaces          1
    bConfigurationValue     1
    iConfiguration          0 
    bmAttributes         0x80
      (Bus Powered)
    MaxPower              896mA
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        0
      bAlternateSetting       0
      bNumEndpoints           2
      bInterfaceClass         8 Mass Storage
      bInterfaceSubClass      6 SCSI
      bInterfaceProtocol     80 Bulk-Only
      iInterface              0 
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x81  EP 1 IN
        bmAttributes            2
          Transfer Type            Bulk
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0400  1x 1024 bytes
        bInterval               0
        bMaxBurst               1
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x02  EP 2 OUT
        bmAttributes            2
          Transfer Type            Bulk
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0400  1x 1024 bytes
        bInterval               0
        bMaxBurst              15
sdejongh@debian-base:~$
```

Note that you can gather informations about pci devices using the `lspci` command

```
sdejongh@debian-base:~$ lspci
00:00.0 Host bridge: Intel Corporation 440FX - 82441FX PMC [Natoma] (rev 02)
00:01.0 ISA bridge: Intel Corporation 82371SB PIIX3 ISA [Natoma/Triton II]
00:01.1 IDE interface: Intel Corporation 82371AB/EB/MB PIIX4 IDE (rev 01)
00:02.0 VGA compatible controller: VMware SVGA II Adapter
00:03.0 Ethernet controller: Intel Corporation 82540EM Gigabit Ethernet Controller (rev 02)
00:04.0 System peripheral: InnoTek Systemberatung GmbH VirtualBox Guest Service
00:05.0 Multimedia audio controller: Intel Corporation 82801AA AC'97 Audio Controller (rev 01)
00:07.0 Bridge: Intel Corporation 82371AB/EB/MB PIIX4 ACPI (rev 08)
00:0c.0 USB controller: Intel Corporation 7 Series/C210 Series Chipset Family USB xHCI Host Controller
00:0d.0 SATA controller: Intel Corporation 82801HM/HEM (ICH8M/ICH8M-E) SATA Controller [AHCI mode] (rev 02)
sdejongh@debian-base:~$
```

And if you cant to get both names and device id you need t add the `-nn` options.

```
sdejongh@debian-base:~$ lspci -nn
00:00.0 Host bridge [0600]: Intel Corporation 440FX - 82441FX PMC [Natoma] [8086:1237] (rev 02)
00:01.0 ISA bridge [0601]: Intel Corporation 82371SB PIIX3 ISA [Natoma/Triton II] [8086:7000]
00:01.1 IDE interface [0101]: Intel Corporation 82371AB/EB/MB PIIX4 IDE [8086:7111] (rev 01)
00:02.0 VGA compatible controller [0300]: VMware SVGA II Adapter [15ad:0405]
00:03.0 Ethernet controller [0200]: Intel Corporation 82540EM Gigabit Ethernet Controller [8086:100e] (rev 02)
00:04.0 System peripheral [0880]: InnoTek Systemberatung GmbH VirtualBox Guest Service [80ee:cafe]
00:05.0 Multimedia audio controller [0401]: Intel Corporation 82801AA AC'97 Audio Controller [8086:2415] (rev 01)
00:07.0 Bridge [0680]: Intel Corporation 82371AB/EB/MB PIIX4 ACPI [8086:7113] (rev 08)
00:0c.0 USB controller [0c03]: Intel Corporation 7 Series/C210 Series Chipset Family USB xHCI Host Controller [8086:1e31]
00:0d.0 SATA controller [0106]: Intel Corporation 82801HM/HEM (ICH8M/ICH8M-E) SATA Controller [AHCI mode] [8086:2829] (rev 02)
sdejongh@debian-base:~$
```

Now that we have the device id, we can get some more informations about the pci devices the same way we did for usb devices:

```
sdejongh@debian-base:~$ lspci -d 8086:100e -v
00:03.0 Ethernet controller: Intel Corporation 82540EM Gigabit Ethernet Controller (rev 02)
    Subsystem: Intel Corporation PRO/1000 MT Desktop Adapter
    Flags: bus master, 66MHz, medium devsel, latency 64, IRQ 19
    Memory at e8600000 (32-bit, non-prefetchable) [size=128K]
    I/O ports at c1a0 [size=8]
    Capabilities: <access denied>
    Kernel driver in use: e1000
    Kernel modules: e1000
sdejongh@debian-base:~$
```

#### Using `udevadm`

We can get the same information via `udevadm` with the `info` subcommand.
We'll have to specify *which* device we want to query and this can be done via different identifiers. The USB stick I inserted is still plugged in and represented in my filesystem via `/dev/sdb`.

```
sdejongh@debian-base:~$ sudo udevadm info /dev/sdb
P: /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb
N: sdb
L: 0
S: disk/by-path/pci-0000:00:0c.0-usb-0:1:1.0-scsi-0:0:0:0
S: disk/by-id/usb-USB_SanDisk_3.2Gen1_01010ac4b3c45b97338088a097b49464e5af8a4ce19fef478b0ce1d7f1e75b3a580e00000000000000000000b7e9a6f0ff09260091558107b52921a5-0:0
E: DEVPATH=/devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb
E: DEVNAME=/dev/sdb
E: DEVTYPE=disk
E: MAJOR=8
E: MINOR=16
E: SUBSYSTEM=block
E: USEC_INITIALIZED=1419363794
E: ID_VENDOR=USB
E: ID_VENDOR_ENC=\x20USB\x20\x20\x20\x20
E: ID_VENDOR_ID=0781
E: ID_MODEL=SanDisk_3.2Gen1
E: ID_MODEL_ENC=\x20SanDisk\x203.2Gen1
E: ID_MODEL_ID=5591
E: ID_REVISION=1.00
E: ID_SERIAL=USB_SanDisk_3.2Gen1_01010ac4b3c45b97338088a097b49464e5af8a4ce19fef478b0ce1d7f1e75b3a580e00000000000000000000b7e9a6f0ff09260091558107b52921a5-0:0
E: ID_SERIAL_SHORT=01010ac4b3c45b97338088a097b49464e5af8a4ce19fef478b0ce1d7f1e75b3a580e00000000000000000000b7e9a6f0ff09260091558107b52921a5
E: ID_TYPE=disk
E: ID_INSTANCE=0:0
E: ID_BUS=usb
E: ID_USB_INTERFACES=:080650:
E: ID_USB_INTERFACE_NUM=00
E: ID_USB_DRIVER=usb-storage
E: ID_PATH=pci-0000:00:0c.0-usb-0:1:1.0-scsi-0:0:0:0
E: ID_PATH_TAG=pci-0000_00_0c_0-usb-0_1_1_0-scsi-0_0_0_0
E: ID_PART_TABLE_UUID=c710b5e0
E: ID_PART_TABLE_TYPE=dos
E: DEVLINKS=/dev/disk/by-path/pci-0000:00:0c.0-usb-0:1:1.0-scsi-0:0:0:0 /dev/disk/by-id/usb-USB_SanDisk_3.2Gen1_01010ac4b3c45b97338088a097b49464e5af8a4ce19fef478b0ce1d7f1e75b3a580e00000000000000000000b7e9a6f0ff09260091558107b52921a5-0:0
E: TAGS=:systemd:
E: CURRENT_TAGS=:systemd:

sdejongh@debian-base:~$
```

We can also inspect information about the **partions** on the disk, even without **mounting** them. You would do `sudo udevadm info --name=/dev/sdb1` wich gives us the label, type of format, etc.

### Customizing UDEV

Now that we know how to gather informations about devices, we can use them to tell udev what to do when a device is added, removed or modified.

This is dine by creating *udev rules*. Generaly your linux distribution will comme with several generic rules. They should be stored in `/lib/udev/rules.d/`... *These files should not be edited* because they will me overwritten in case of an udev update.

```
sdejongh@debian-base:~$ ls -al /lib/udev/rules.d/
total 788
drwxr-xr-x 2 root root   4096 Sep  8 07:58 .
drwxr-xr-x 4 root root   4096 Sep  8 08:02 ..
-rw-r--r-- 1 root root    991 Jun 23  2020 39-usbmuxd.rules
-rw-r--r-- 1 root root    998 Jan 20  2019 40-usb-media-players.rules
-rw-r--r-- 1 root root  42861 Feb 24  2020 40-usb_modeswitch.rules
-rw-r--r-- 1 root root    210 Mar 20 19:55 50-firmware.rules
-rw-r--r-- 1 root root   3920 Mar 20 19:55 50-udev-default.rules
-rw-r--r-- 1 root root   7274 Feb 22  2021 55-dm.rules
-rw-r--r-- 1 root root   2420 Feb 22  2021 56-lvm.rules
-rw-r--r-- 1 root root    419 Feb  2  2021 60-autosuspend.rules
-rw-r--r-- 1 root root    703 Feb  2  2021 60-block.rules
-rw-r--r-- 1 root root   1071 Feb  2  2021 60-cdrom_id.rules
-rw-r--r-- 1 root root    413 Feb  2  2021 60-drm.rules
-rw-r--r-- 1 root root    990 Feb  2  2021 60-evdev.rules
-rw-r--r-- 1 root root    491 Mar 20 19:55 60-fido-id.rules
-rw-r--r-- 1 root root    282 Feb  2  2021 60-input-id.rules
-rw-r--r-- 1 root root   7266 Feb 28  2021 60-libgphoto2-6.rules
-rw-r--r-- 1 root root   2097 Nov  6  2017 60-libopenni2-0.rules
-rw-r--r-- 1 root root   3527 Jul 25  2021 60-libsane1.rules
-rw-r--r-- 1 root root    616 Feb  2  2021 60-persistent-alsa.rules
-rw-r--r-- 1 root root   2710 Feb  2  2021 60-persistent-input.rules
-rw-r--r-- 1 root root   1794 Feb 22  2021 60-persistent-storage-dm.rules
-rw-r--r-- 1 root root   8026 Feb  2  2021 60-persistent-storage.rules
-rw-r--r-- 1 root root   2135 Feb  2  2021 60-persistent-storage-tape.rules
-rw-r--r-- 1 root root    769 Feb  2  2021 60-persistent-v4l.rules
-rw-r--r-- 1 root root    736 Feb  2  2021 60-sensor.rules
-rw-r--r-- 1 root root   1302 Feb  2  2021 60-serial.rules
-rw-r--r-- 1 root root    211 Nov 30  2020 60-tpm-udev.rules
-rw-r--r-- 1 root root    356 Dec 18  2020 61-gdm.rules
-rw-r--r-- 1 root root    292 Apr 14  2021 61-gnome-settings-daemon-rfkill.rules
-rw-r--r-- 1 root root     91 Aug 18  2021 61-mutter.rules
-rw-r--r-- 1 root root    612 Mar 20 19:55 64-btrfs.rules
-rw-r--r-- 1 root root    257 Aug  5 09:00 64-xorg-xkb.rules
-rw-r--r-- 1 root root   1157 Jan 29  2021 65-libwacom.rules
-rw-r--r-- 1 root root   4934 Nov 12  2020 69-cd-sensors.rules
-rw-r--r-- 1 root root 230185 Mar 26  2020 69-libmtp.rules
-rw-r--r-- 1 root root   5813 Feb 22  2021 69-lvm-metad.rules
-rw-r--r-- 1 root root   1142 Aug  6  2019 69-wacom.rules
-rw-r--r-- 1 root root    432 Feb  2  2021 70-joystick.rules
-rw-r--r-- 1 root root    734 Feb  2  2021 70-mouse.rules
-rw-r--r-- 1 root root    576 Feb  2  2021 70-power-switch.rules
-rw-r--r-- 1 root root    845 Jan 13  2021 70-printers.rules
-rw-r--r-- 1 root root    473 Feb  2  2021 70-touchpad.rules
-rw-r--r-- 1 root root   2808 Mar 20 19:55 70-uaccess.rules
-rw-r--r-- 1 root root    192 Jul 18  2021 71-ipp-usb.rules
-rw-r--r-- 1 root root   3971 Mar 20 19:55 71-seat.rules
-rw-r--r-- 1 root root    644 Mar 20 19:55 73-seat-late.rules
-rw-r--r-- 1 root root    969 Mar 20 19:55 73-special-net-names.rules
-rw-r--r-- 1 root root    452 Feb  2  2021 75-net-description.rules
-rw-r--r-- 1 root root    174 Feb  2  2021 75-probe_mtd.rules
-rw-r--r-- 1 root root    864 Jul 23  2021 77-mm-broadmobi-port-types.rules
-rw-r--r-- 1 root root   3475 Jul 23  2021 77-mm-cinterion-port-types.rules
-rw-r--r-- 1 root root   1623 Jul 23  2021 77-mm-dell-port-types.rules
-rw-r--r-- 1 root root    830 Jul 23  2021 77-mm-dlink-port-types.rules
-rw-r--r-- 1 root root   7742 Jul 23  2021 77-mm-ericsson-mbm.rules
-rw-r--r-- 1 root root   1173 Jul 23  2021 77-mm-fibocom-port-types.rules
-rw-r--r-- 1 root root   1459 Jul 23  2021 77-mm-foxconn-port-types.rules
-rw-r--r-- 1 root root    507 Jul 23  2021 77-mm-haier-port-types.rules
-rw-r--r-- 1 root root   2028 Jul 23  2021 77-mm-huawei-net-port-types.rules
-rw-r--r-- 1 root root  12940 Jul 23  2021 77-mm-longcheer-port-types.rules
-rw-r--r-- 1 root root   3030 Jul 23  2021 77-mm-mtk-port-types.rules
-rw-r--r-- 1 root root   1942 Jul 23  2021 77-mm-nokia-port-types.rules
-rw-r--r-- 1 root root    388 Jul 23  2021 77-mm-pcmcia-device-blacklist.rules
-rw-r--r-- 1 root root   3155 Jul 23  2021 77-mm-qdl-device-blacklist.rules
-rw-r--r-- 1 root root   3972 Jul 23  2021 77-mm-quectel-port-types.rules
-rw-r--r-- 1 root root   1338 Jul 23  2021 77-mm-sierra.rules
-rw-r--r-- 1 root root   3257 Jul 23  2021 77-mm-simtech-port-types.rules
-rw-r--r-- 1 root root   6737 Jul 23  2021 77-mm-telit-port-types.rules
-rw-r--r-- 1 root root    721 Jul 23  2021 77-mm-tplink-port-types.rules
-rw-r--r-- 1 root root   4215 Jul 23  2021 77-mm-ublox-port-types.rules
-rw-r--r-- 1 root root   8811 Jul 23  2021 77-mm-usb-device-blacklist.rules
-rw-r--r-- 1 root root   2425 Jul 23  2021 77-mm-usb-serial-adapters-greylist.rules
-rw-r--r-- 1 root root   4206 Jul 23  2021 77-mm-x22x-port-types.rules
-rw-r--r-- 1 root root  14947 Jul 23  2021 77-mm-zte-port-types.rules
-rw-r--r-- 1 root root   4816 Feb  2  2021 78-sound-card.rules
-rw-r--r-- 1 root root   1375 Mar 20 19:55 80-debian-compat.rules
-rw-r--r-- 1 root root    615 Feb  2  2021 80-drivers.rules
-rw-r--r-- 1 root root    190 Sep 21  2020 80-ifupdown.rules
-rw-r--r-- 1 root root   1464 Jan 29  2021 80-iio-sensor-proxy.rules
-rw-r--r-- 1 root root    207 Dec 10  2020 80-libinput-device-groups.rules
-rw-r--r-- 1 root root    972 Jul 23  2021 80-mm-candidate.rules
-rw-r--r-- 1 root root    295 Feb  2  2021 80-net-setup-link.rules
-rw-r--r-- 1 root root  10277 Nov  5  2021 80-udisks2.rules
-rw-r--r-- 1 root root    528 Mar 21 14:47 84-nm-drivers.rules
-rw-r--r-- 1 root root    208 Jan 20  2022 85-hwclock.rules
-rw-r--r-- 1 root root   1682 Mar 21 14:47 85-nm-unmanaged.rules
-rw-r--r-- 1 root root    563 Dec  7  2020 90-alsa-restore.rules
-rw-r--r-- 1 root root    350 Dec  1  2020 90-bolt.rules
-rw-r--r-- 1 root root    265 Oct 29  2018 90-console-setup.rules
-rw-r--r-- 1 root root    281 Feb 23  2021 90-fwupd-devices.rules
-rw-r--r-- 1 root root   1850 Nov 28  2020 90-libgpod.rules
-rw-r--r-- 1 root root   1098 Dec 10  2020 90-libinput-fuzz-override.rules
-rw-r--r-- 1 root root    576 Mar 21 14:47 90-nm-thunderbolt.rules
-rw-r--r-- 1 root root  11356 Jan  5  2021 90-pipewire-alsa.rules
-rw-r--r-- 1 root root  10636 Feb 26  2021 90-pulseaudio.rules
-rw-r--r-- 1 root root    847 Nov  2  2020 95-cd-devices.rules
-rw-r--r-- 1 root root    479 Feb 22  2021 95-dm-notify.rules
-rw-r--r-- 1 root root   1621 May 16  2020 95-upower-csr.rules
-rw-r--r-- 1 root root    570 May 16  2020 95-upower-hidpp.rules
-rw-r--r-- 1 root root   8109 May 16  2020 95-upower-hid.rules
-rw-r--r-- 1 root root    354 May 16  2020 95-upower-wup.rules
-rw-r--r-- 1 root root    171 Jun  7  2021 96-e2scrub.rules
-rw-r--r-- 1 root root   1518 Jun 10  2021 97-hid2hci.rules
-rw-r--r-- 1 root root     98 Nov  2  2020 99-libsane1.rules
-rw-r--r-- 1 root root   4690 Mar 20 19:55 99-systemd.rules
sdejongh@debian-base:~$
```

Each *.rules* file is a set of udev rules. When *udev* starts, it will load all those files and apply the included rules following the priority given by the file name. This is the reason why all those wile have a name starting with a number.

Having a look at some of those files can be very helpful to understand how those rules work and how our system handle devices when they are discovered etc.

For example, in the `60-persistent-storage.rules` file we can see this rule:

```
KERNEL=="nvme*[0-9]n*[0-9]", ATTR{wwid}=="?*", SYMLINK+="disk/by-id/nvme-$attr{wwid}"
```

This rule creates a symbolic link in `/dev/by-id` for each nvme (PCIe SSDs) device.

#### UDEV rules syntax

The structure of a rule is simple:

- A rule is made of several comma-separated fields

- A rule must conatin at least one *matching* field

- A rule must contain at least one *set* field.

```
<KEY>[!]=<VALUE>, ..., <KEY>[+]=<VALUE>, ...
```

Each field use an operator:

- `==`    must be equal

- `!=` must be different

- `=` assign a value

- `+=` add a value to a list

- `-=` removes a value from a list

- `:=` assign a value to a key and prevent any later change.

There are a lot of available *keys* with some depending on the nature of the device, a few examples are:

- `ACTION` matches the name of an action (add, remove, ...) on a device

- `KERNEL` matches the device name given by the kernel (ie: /dev/sda)

- `SUBSYSTEM` matches the subsystem of the event

- `ATTRS{key}` matche an attribute of the event device

- `SYMLINK` matches the name of a symbolic link of the device. It can also be used to set or add new symbolic links for a device.

The *value* part of the field supports *shell glob pattern* matching:

- `*` can be used to match zero or more characters

- `?` can be used to match any single character

- `[ ]` can be use to match a list of characters (ie: sd[ab] would match both sda and sdb).

- `|` works like a logical OR (ie: abc|def would match adb or def)

There also some substitution characters yo ucan use in rules definition, lets see some of them:

- `%k` the kernel name for the device

- `%n` the kernel number for the device (would be 3 for sda3)

- `%p` the devpath of the device

- `$driver` the driver name for the device

- etc.

Don't forget to read `man udev` for more options and details.

#### Writing custom UDEV rules

Custom udev rules must be written in `.rules`files and stored in `/etc/udev/rules.d/`. Like the *system standard rules* all files contained in this directory will be loaded following the priority based on their name. 

Here is a general naming convention for those files:

```
    Files should be named xx-descriptive-name.rules, the xx should be
    chosen first according to the following sequence points:

    < 60  most user rules; if you want to prevent an assignment being
    overriden by default rules, use the := operator.

    these cannot access persistent information such as that from
    vol_id

    < 70  rules that run helpers such as vol_id to populate the udev db

    < 90  rules that run other programs (often using information in the
    udev db)

    >=90  rules that should run last
```

Let's write two simple rules in `/etc/udev/rules.d/10-watch-devices.rules`...

```
# Add log entry when a new device is added
ACTION=="add", RUN+="/bin/sh -c '/bin/echo ADDED %k : %p >> /var/log/watch_devices.log'"

# Add log entry when a device is removed
ACTION=="remove", RUN+="/bin/sh -c '/bin/echo REMOVED %k : %p >> /var/log/watch_devices.log'"
```

The first rule will be triggered when a device is added as stated with the `ACTION=="add"` field. The `RUN+=...` field adds a command to run when the rule is triggered.

The second rule works the same way but will be triggered when a device is removed as stated in the `ACTION=="remove"` field.

We can now restart the service...

```
sdejongh@debian-base:~$ sudo systemctl restart systemd-udevd
```

To test it i then pluged in my usb drive and removed it a few seconds later. I can now see the result in the `/var/log/watch_deviles.log` file.

```
sdejongh@debian-base:~$ cat /var/log/watch_devices.log 
ADDED scsi_tmf_3 : /devices/virtual/workqueue/scsi_tmf_3
ADDED 2-1 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1
ADDED 2-1:1.0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0
ADDED host3 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3
ADDED host3 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/scsi_host/host3
ADDED target3:0:0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0
ADDED 3:0:0:0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0
ADDED 3:0:0:0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_disk/3:0:0:0
ADDED sg2 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_generic/sg2
ADDED 3:0:0:0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_device/3:0:0:0
ADDED 3:0:0:0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/bsg/3:0:0:0
ADDED 8:16 : /devices/virtual/bdi/8:16
ADDED sdb : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb
ADDED sdb1 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb/sdb1
REMOVED 3:0:0:0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/bsg/3:0:0:0
REMOVED sg2 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_generic/sg2
REMOVED 3:0:0:0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_disk/3:0:0:0
REMOVED 3:0:0:0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/scsi_device/3:0:0:0
REMOVED 8:16 : /devices/virtual/bdi/8:16
REMOVED host3 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/scsi_host/host3
REMOVED sdb1 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb/sdb1
REMOVED sdb : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0/block/sdb
REMOVED 3:0:0:0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0/3:0:0:0
REMOVED target3:0:0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3/target3:0:0
REMOVED host3 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0/host3
REMOVED 2-1:1.0 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1/2-1:1.0
REMOVED 2-1 : /devices/pci0000:00/0000:00:0c.0/usb2/2-1
REMOVED scsi_tmf_3 : /devices/virtual/workqueue/scsi_tmf_3
```

This is by the way a very basic example but it shows the principe of how udev works. Let's now try to make some more useful rules.

##### Creating an alternate name for network interfaces

Network interfaces are named by the kernel. Their name follows a generic pattern like `enX` or `ethX` or `enpXsY`. It works fine but it would be easier if we could reference them using a more adequate name.

For example, we could use udev to rename the main interface as *lan*.

So we need to write a rule that will be triggered only for the given interface. In the example i want to rename the `enp0s3` interface.

First of all we need to gather some informations... Network interfaces are referenced in `/sys/class/net/` ... Let's call `udevadm info`...

```
sdejongh@debian-base:~$ sudo udevadm info /sys/class/net/enp0s3 
P: /devices/pci0000:00/0000:00:03.0/net/enp0s3
L: 0
E: DEVPATH=/devices/pci0000:00/0000:00:03.0/net/enp0s3
E: INTERFACE=enp0s3
E: IFINDEX=2
E: SUBSYSTEM=net
E: USEC_INITIALIZED=1995814
E: ID_NET_NAMING_SCHEME=v247
E: ID_NET_NAME_MAC=enx080027871c39
E: ID_OUI_FROM_DATABASE=PCS Systemtechnik GmbH
E: ID_NET_NAME_PATH=enp0s3
E: ID_BUS=pci
E: ID_VENDOR_ID=0x8086
E: ID_MODEL_ID=0x100e
E: ID_PCI_CLASS_FROM_DATABASE=Network controller
E: ID_PCI_SUBCLASS_FROM_DATABASE=Ethernet controller
E: ID_VENDOR_FROM_DATABASE=Intel Corporation
E: ID_MODEL_FROM_DATABASE=82540EM Gigabit Ethernet Controller (PRO/1000 MT Desktop Adapter)
E: ID_MM_CANDIDATE=1
E: ID_PATH=pci-0000:00:03.0
E: ID_PATH_TAG=pci-0000_00_03_0
E: ID_NET_DRIVER=e1000
E: ID_NET_LINK_FILE=/usr/lib/systemd/network/99-default.link
E: ID_NET_NAME=enp0s3
E: SYSTEMD_ALIAS=/sys/subsystem/net/devices/enp0s3
E: TAGS=:systemd:
E: CURRENT_TAGS=:systemd:
sdejongh@debian-base:~$
```

This give us enough informations to effectively target the given interface:

- `SUBSYSTEM`: the subsystem managing the device

- `ID_NET_NAME_MAC`: the actual mac address of the interface

- `ID_VENDOR`:`ID_MODEL` : the hexadecimal value representing the device hardware

So we can create a new `.rules` file (or add a new rule to the previous one) and write a new rule. `/etc/udev/rules.d/11-net-rename.rules` 

```
# Add a more friendly name to enp0s3 network interface
SUBSYSTEM=="net", ATTR{address}=="08:00:27:87:1c:39", NAME="lan"
```

The rule will be triggered when something managed by the subsystem *net* and having the attribute *address* with the given value is detected (at boot time in the case of a network interface0), and give it a new name: "lan".

After reboot we can see that the network interface has been renamed...

```
sdejongh@debian-base:~$ ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: lan: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:87:1c:39 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
sdejongh@debian-base:~$
```

Note that the original name is given as an altname, meaning we can use both original and new name to manage the interface.

```
sdejongh@debian-base:~$ sudo ip link set lan down
sdejongh@debian-base:~$ sudo ip link set enp0s3 up
```

##### Disable all USB block devices

If you want to prevent users to use USB storage devices you can simply ask udev to ignore them. We need a rule which targets specifically storage devices (aka block devices) connected to the USB bus.

```
ACTION=="add", SUBSYSTEMS=="usb", SUBSYSTEM=="block", ENV{UDISKS_IGNORE}="1"
```

## Ressources

- [udev](https://www.freedesktop.org/software/systemd/man/udev.html)

- [Une introduction à UDEV | Linux Embedded](https://linuxembedded.fr/2015/05/une-introduction-a-udev)

- [Writing udev rules](http://reactivated.net/writing_udev_rules.html)
