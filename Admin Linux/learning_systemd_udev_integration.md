# Integrating udev rules with systemd

As we saw in [learning udev](./learning_udev.md) we can **run** scripts or commands when certain conditions are met in regards to physical device changes.
The *classic* way to run long running actions, such as a backup, was to have `udev` trigger a script and be done with it.
This behaviour is currently discouraged and will most likely **fail** if your script take too long.
The `man udev` pages state the following.

```
Starting daemons or other long-running processes is not allowed; the forked processes, detached or not, will be
unconditionally killed after the event handling has finished. In order to activate long-running processes from udev
rules, provide a service unit and pull it in from a udev device using the SYSTEMD_WANTS device property. See
systemd.device(5) for details.
```

It's pretty clear what you can't do, but how to do it *right* is less clear.
The idea is to start a systemd service when a device is plugged in.
Udev will tell systemd to start the service but will delegate the responsibility to systemd so the request is non-blocking.

## Writing the service

We start by writing a small script that serves as a placeholder to prove our workflow.
It will just echo a line to `journalctl`.
No need to manage our own logging systemd as we can take full advantage of systemd's built in logging.

```bash
➜  ~ git:(master) ✗ cat backup.sh 
#!/bin/bash

echo "hello world $(date)"
exit 0
➜  ~ git:(master) ✗ 
```

We can now take this mini script and turn it into service by creating a `backup.service` file in `/etc/systemd/system`.
Let's do this and populate as such.

```ini
➜  ~ git:(master) ✗ cat /etc/systemd/system/backup.service 
[Unit]
Description=Our own backup script

[Service]
ExecStart=/bin/bash /home/waldek/backup.sh

[Install]
WantedBy=default.target
➜  ~ git:(master) ✗ 
```

Next we need to reload systemd and test the service.

```bash
➜  ~ git:(master) ✗ sudo systemctl daemon-reload 
➜  ~ git:(master) ✗ sudo systemctl start backup.service 
➜  ~ git:(master) ✗ sudo systemctl status backup.service
● backup.service - Our own backup script
     Loaded: loaded (/etc/systemd/system/backup.service; disabled; vendor preset: enabled)
     Active: inactive (dead)

Aug 23 21:50:38 deathstar systemd[1]: Started Our own backup script.
Aug 23 21:50:38 deathstar bash[956441]: hello world Mon 23 Aug 21:50:38 CEST 2021
Aug 23 21:50:38 deathstar systemd[1]: backup.service: Succeeded.
➜  ~ git:(master) ✗ 
```


## Writing the udev rule

It seems to have worked nicely!
Now we will write the udev rule to start our service when a USB stick is plugged in.
We'll start with a very *generic* rule that triggers for each block device that is plugged in.

```ini
➜  ~ git:(master) ✗ cat /etc/udev/rules.d/99-backup_to_usb_stick.rules  
SUBSYSTEM=="block", ACTION=="add", ENV{SYSTEMD_WANTS}="backup.service"
➜  ~ git:(master) ✗ 
```

To test the rule we need to reload the udev rules and inspect the logs of systemd with journalctl.
We can monitor the logs *live* with the `-f` argument if we want.
You'll see the ourput of the placeholder script appear when you plug in any USB stick!
It will also double or even triple trigger, depending on the number of partitions you have on your stick but we know how to fix this.

```bash
➜  ~ git:(master) ✗ sudo udevadm control --reload           
➜  ~ git:(master) ✗ sudo journalctl -f --unit backup.service 
-- Journal begins at Wed 2021-07-14 22:35:36 CEST, ends at Mon 2021-08-23 21:59:26 CEST. --
Aug 23 21:59:05 deathstar systemd[1]: Started Our own backup script.
Aug 23 21:59:05 deathstar bash[957988]: hello world Mon 23 Aug 21:59:05 CEST 2021
Aug 23 21:59:05 deathstar systemd[1]: backup.service: Succeeded.
Aug 23 21:59:05 deathstar systemd[1]: Started Our own backup script.
Aug 23 21:59:05 deathstar bash[957992]: hello world Mon 23 Aug 21:59:05 CEST 2021
Aug 23 21:59:05 deathstar systemd[1]: backup.service: Succeeded.
```

## Fine tuning the udev rule

I only want my backup do be done to a very specific USB stick I trust.
When I plug it in I can inspect it's attributes and environment variables via `udevadm`.
I'll use the filesystem's UUID to identify the disk.

```bash
➜  ~ git:(master) ✗ sudo udevadm info --name=/dev/sdd1 | grep UUID
E: ID_PART_TABLE_UUID=d9f8a99f-673a-334c-af4f-18697ed888c9
E: ID_FS_UUID=2469ffe5-e066-476d-805a-cde85a58ea3b
E: ID_FS_UUID_ENC=2469ffe5-e066-476d-805a-cde85a58ea3b
E: ID_PART_ENTRY_UUID=73a25ff8-0e0f-1147-8aaa-7976bf921ced
➜  ~ git:(master) ✗ 
```

I modify the rule, reload udev and inspect my logs after plugging in the device.
This works like a charm!

```bash
➜  ~ git:(master) ✗ cat /etc/udev/rules.d/99-backup_to_usb_stick.rules 
SUBSYSTEM=="block", ENV{ID_FS_UUID}=="2469ffe5-e066-476d-805a-cde85a58ea3b", ACTION=="add", ENV{SYSTEMD_WANTS}="backup.service"
➜  ~ git:(master) ✗ sudo udevadm control --reload 
➜  ~ git:(master) ✗ sudo journalctl --unit backup.service
-- Journal begins at Wed 2021-07-14 22:35:36 CEST. --
Aug 23 22:12:34 deathstar systemd[1]: Started Our own backup script.
Aug 23 22:12:34 deathstar bash[960433]: hello world Mon 23 Aug 22:12:34 CEST 2021
Aug 23 22:12:34 deathstar systemd[1]: backup.service: Succeeded.
➜  ~ git:(master) ✗ 
```

Now a **tricky detail**.
The rule works and triggers only once but as my server is a lean machine I do not have automount installed so the script will have to do this for me.
But how will the script *know* which device is the right one?
We can go multiple ways here but I can think of two different ones.

* hardcode the UUID into the script and look for the proper device
* pass the kernel identified to the service

Let's go for the second option as it's the more *mature* one.
The full solution requires multiple steps and we'll go over them one at time.
First we'll have to modify our rule once more by adding the following.
This passes the drive name to the service.

```bash
➜  ~ git:(master) ✗ cat /etc/udev/rules.d/99-backup_to_usb_stick.rules
SUBSYSTEM=="block", ENV{ID_FS_UUID}=="2469ffe5-e066-476d-805a-cde85a58ea3b", ACTION=="add", ENV{SYSTEMD_WANTS}="backup@$name.service"
➜  ~ git:(master) ✗ sudo udevadm control --reload 
```

You should notice two things when looking at the changed rule.

* the added `@` to the service
* the `$name`

When the partition we want to mount is `/dev/sde1` the service that will get triggered will be `backup@sde1.service`.
These are called **template** services and in order to create one, you *just* have to have the `@` symbol in the service name.
We'll move our old backup.service and reload systemd as follows.

```bash
➜  ~ git:(master) ✗ sudo mv /etc/systemd/system/backup.service /etc/systemd/system/backup@.service
➜  ~ git:(master) ✗ sudo systemctl daemon-reload 
```

Inspecting the logs while plugging in our drive now gives us the following output.

```bash
➜  ~ git:(master) ✗ sudo journalctl -f                                                            
-- Journal begins at Wed 2021-07-14 22:35:36 CEST. --
Aug 23 22:40:38 deathstar sudo[964916]:   waldek : TTY=pts/6 ; PWD=/home/waldek ; USER=root ; COMMAND=/usr/bin/mv /etc/systemd/system/backup.service /etc/systemd/system/backup@.service
Aug 23 22:40:38 deathstar sudo[964916]: pam_unix(sudo:session): session opened for user root(uid=0) by (uid=1000)
Aug 23 22:40:38 deathstar sudo[964916]: pam_unix(sudo:session): session closed for user root
Aug 23 22:40:49 deathstar sudo[964959]:   waldek : TTY=pts/6 ; PWD=/home/waldek ; USER=root ; COMMAND=/usr/bin/systemctl daemon-reload
Aug 23 22:40:49 deathstar sudo[964959]: pam_unix(sudo:session): session opened for user root(uid=0) by (uid=1000)
Aug 23 22:40:49 deathstar systemd[1]: Reloading.
Aug 23 22:40:49 deathstar sudo[964959]: pam_unix(sudo:session): session closed for user root
Aug 23 22:41:45 deathstar kernel: usb 3-1.5: USB disconnect, device number 59
Aug 23 22:41:48 deathstar sudo[965130]:   waldek : TTY=pts/6 ; PWD=/home/waldek ; USER=root ; COMMAND=/usr/bin/journalctl -f
Aug 23 22:41:48 deathstar sudo[965130]: pam_unix(sudo:session): session opened for user root(uid=0) by (uid=1000)
Aug 23 22:41:58 deathstar kernel: usb 3-1.5: new high-speed USB device number 60 using ehci-pci
Aug 23 22:41:58 deathstar kernel: usb 3-1.5: New USB device found, idVendor=0781, idProduct=5591, bcdDevice= 1.00
Aug 23 22:41:58 deathstar kernel: usb 3-1.5: New USB device strings: Mfr=1, Product=2, SerialNumber=3
Aug 23 22:41:58 deathstar kernel: usb 3-1.5: Product:  SanDisk 3.2Gen1
Aug 23 22:41:58 deathstar kernel: usb 3-1.5: Manufacturer:  USB
Aug 23 22:41:58 deathstar kernel: usb 3-1.5: SerialNumber: 04018a57f24e4dc0135c1f4666b5f2ca4e8e15e65eedfd157b0146cf1427157522b000000000000000000000a03e3c7e008cb3189155810739aa4777
Aug 23 22:41:58 deathstar kernel: usb-storage 3-1.5:1.0: USB Mass Storage device detected
Aug 23 22:41:58 deathstar kernel: scsi host7: usb-storage 3-1.5:1.0
Aug 23 22:41:59 deathstar kernel: scsi 7:0:0:0: Direct-Access      USB      SanDisk 3.2Gen1 1.00 PQ: 0 ANSI: 6
Aug 23 22:41:59 deathstar kernel: sd 7:0:0:0: Attached scsi generic sg3 type 0
Aug 23 22:41:59 deathstar kernel: sd 7:0:0:0: [sde] 60088320 512-byte logical blocks: (30.8 GB/28.7 GiB)
Aug 23 22:41:59 deathstar kernel: sd 7:0:0:0: [sde] Write Protect is off
Aug 23 22:41:59 deathstar kernel: sd 7:0:0:0: [sde] Mode Sense: 43 00 00 00
Aug 23 22:41:59 deathstar kernel: sd 7:0:0:0: [sde] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
Aug 23 22:41:59 deathstar kernel:  sde: sde1
Aug 23 22:41:59 deathstar kernel: sd 7:0:0:0: [sde] Attached SCSI removable disk
Aug 23 22:41:59 deathstar systemd[1]: Started Our own backup script.
Aug 23 22:41:59 deathstar bash[965178]: hello world Mon 23 Aug 22:41:59 CEST 2021
Aug 23 22:41:59 deathstar systemd[1]: backup@sde1.service: Succeeded.
```

Success!
It's the last three lines that are important here.
We can see the right service get's triggered.
Now, how do we recuperate the `$name` variable in our script?

## Fine tuning the service

We can use the variables passed through via the service name by modifying the `backup@.service` file.
The argument used is the `%I` when calling our script.
Let's look at the final service file and reload systemd.

```ini
➜  ~ git:(master) ✗ cat /etc/systemd/system/backup@.service           
[Unit]
Description=Our own backup script

[Service]
ExecStart=/bin/bash /home/waldek/backup.sh %I

[Install]
WantedBy=default.target
➜  ~ git:(master) ✗ sudo systemctl daemon-reload
➜  ~ git:(master) ✗ 
```

## Fine tuning the script

The script should now be receiving the partition location as a first argument.
We can echo it out by modifying the script and inspecting the logs via `journalctl`.

```bash
➜  ~ git:(master) ✗ cat backup.sh 
#!/bin/bash

echo "hello world $(date), will backup to $1"
exit 0
sudo journalctl -f                      
-- Journal begins at Wed 2021-07-14 22:35:36 CEST. --
Aug 23 22:49:59 deathstar kernel: sd 7:0:0:0: [sde] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
Aug 23 22:49:59 deathstar kernel:  sde: sde1
Aug 23 22:49:59 deathstar kernel: sd 7:0:0:0: [sde] Attached SCSI removable disk
Aug 23 22:49:59 deathstar systemd[1]: Started Our own backup script.
Aug 23 22:49:59 deathstar bash[966393]: hello world Mon 23 Aug 22:49:59 CEST 2021, will backup to sde1
Aug 23 22:49:59 deathstar systemd[1]: backup@sde1.service: Succeeded.
```

## Mini conclusion

The entire process might seem a bit convoluted but it's fully in line with the Linux philosophy of separating responsibility.
All the tools are there to chain together a very robust and controlled flow of events.

## An actual useful script

Our placeholder script is a good proof of concept to debug the flow of operations but does not do anything useful.
Let's write a simple backup script though.
I like using `rsync` so you'll have to install it if you want to play around with this script.

```bash
➜  ~ git:(master) ✗ cat backup.sh 
#!/bin/bash

SOURCE_DIR="/home/waldek/Documents/freecad/"
MOUNT_POINT="/media/backup_usb_stick"
DST_DIR="$MOUNT_POINT/backups"

echo "running as $(whoami) will backup to $1"
mkdir -p $MOUNT_POINT && echo "created $MOUNT_POINT"
mount /dev/$1 $MOUNT_POINT && echo "mounted $1"
rsync -av $SOURCE_DIR $DST_DIR && echo "all done"
umount /dev/$1 && echo "unmounted..."
exit 0
➜  ~ git:(master) ✗ 
```

Below is the output of two consecutive plug in and out's.
You can see all the files that get backed up the first time around.
The second time around no files are copied because I made no changes to any files.
This is the behaviour of the `-a` argument to `rsync`.

```bash
➜  ~ git:(master) ✗ sudo journalctl -f                          
-- Journal begins at Wed 2021-07-14 22:35:36 CEST. --
Aug 23 23:04:40 deathstar sudo[969830]:   waldek : TTY=pts/6 ; PWD=/home/waldek ; USER=root ; COMMAND=/usr/bin/journalctl -f
Aug 23 23:04:40 deathstar sudo[969830]: pam_unix(sudo:session): session opened for user root(uid=0) by (uid=1000)
Aug 23 23:04:45 deathstar kernel: usb 3-1.5: new high-speed USB device number 67 using ehci-pci
Aug 23 23:04:45 deathstar kernel: usb 3-1.5: New USB device found, idVendor=0781, idProduct=5591, bcdDevice= 1.00
Aug 23 23:04:45 deathstar kernel: usb 3-1.5: New USB device strings: Mfr=1, Product=2, SerialNumber=3
Aug 23 23:04:45 deathstar kernel: usb 3-1.5: Product:  SanDisk 3.2Gen1
Aug 23 23:04:45 deathstar kernel: usb 3-1.5: Manufacturer:  USB
Aug 23 23:04:45 deathstar kernel: usb 3-1.5: SerialNumber: 04018a57f24e4dc0135c1f4666b5f2ca4e8e15e65eedfd157b0146cf1427157522b000000000000000000000a03e3c7e008cb3189155810739aa4777
Aug 23 23:04:45 deathstar kernel: usb-storage 3-1.5:1.0: USB Mass Storage device detected
Aug 23 23:04:45 deathstar kernel: scsi host8: usb-storage 3-1.5:1.0
Aug 23 23:04:46 deathstar kernel: scsi 8:0:0:0: Direct-Access      USB      SanDisk 3.2Gen1 1.00 PQ: 0 ANSI: 6
Aug 23 23:04:46 deathstar kernel: sd 8:0:0:0: Attached scsi generic sg3 type 0
Aug 23 23:04:46 deathstar kernel: sd 8:0:0:0: [sdf] 60088320 512-byte logical blocks: (30.8 GB/28.7 GiB)
Aug 23 23:04:46 deathstar kernel: sd 8:0:0:0: [sdf] Write Protect is off
Aug 23 23:04:46 deathstar kernel: sd 8:0:0:0: [sdf] Mode Sense: 43 00 00 00
Aug 23 23:04:46 deathstar kernel: sd 8:0:0:0: [sdf] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
Aug 23 23:04:46 deathstar kernel:  sdf: sdf1
Aug 23 23:04:46 deathstar kernel: sd 8:0:0:0: [sdf] Attached SCSI removable disk
Aug 23 23:04:46 deathstar systemd[1]: Started Our own backup script.
Aug 23 23:04:46 deathstar bash[969865]: running as root will backup to sdf1
Aug 23 23:04:46 deathstar bash[969865]: created /media/backup_usb_stick
Aug 23 23:04:46 deathstar bash[969865]: mounted sdf1
Aug 23 23:04:46 deathstar kernel: EXT4-fs (sdf1): mounted filesystem with ordered data mode. Opts: (null)
Aug 23 23:04:46 deathstar bash[969876]: sending incremental file list
Aug 23 23:04:46 deathstar bash[969876]: created directory /media/backup_usb_stick/backups
Aug 23 23:04:46 deathstar bash[969876]: ./
Aug 23 23:04:46 deathstar bash[969876]: arm (Meshed).stl
Aug 23 23:04:46 deathstar bash[969876]: base_pivot (Meshed).stl
Aug 23 23:04:46 deathstar bash[969876]: base_pivot_alt (Meshed).stl
Aug 23 23:04:46 deathstar bash[969876]: base_plate (Meshed).stl
Aug 23 23:04:46 deathstar bash[969876]: base_plate_alt (Meshed).stl
Aug 23 23:04:46 deathstar bash[969876]: filament_guide.FCStd
Aug 23 23:04:46 deathstar bash[969876]: filament_guide.FCStd1
Aug 23 23:04:46 deathstar bash[969876]: filament_guide.stl
Aug 23 23:04:46 deathstar bash[969876]: ivar_riser.FCStd
Aug 23 23:04:46 deathstar bash[969876]: ivar_riser.FCStd1
Aug 23 23:04:46 deathstar bash[969876]: ivar_riser.stl
Aug 23 23:04:46 deathstar bash[969876]: light_pot_office (Meshed).stl
Aug 23 23:04:46 deathstar bash[969876]: light_pot_office.FCStd
Aug 23 23:04:46 deathstar bash[969876]: light_pot_office.FCStd1
Aug 23 23:04:46 deathstar bash[969876]: monitor_arm.FCStd
Aug 23 23:04:46 deathstar bash[969876]: monitor_arm.FCStd1
Aug 23 23:04:46 deathstar bash[969876]: monitor_arm_120mm.stl
Aug 23 23:04:46 deathstar bash[969876]: picam.FCStd
Aug 23 23:04:46 deathstar bash[969876]: picam.FCStd1
Aug 23 23:04:46 deathstar bash[969876]: vat_filter.FCStd
Aug 23 23:04:46 deathstar bash[969876]: vat_filter.FCStd1
Aug 23 23:04:46 deathstar bash[969876]: vat_filter.stl
Aug 23 23:04:46 deathstar bash[969876]: vesa_plate (Meshed).stl
Aug 23 23:04:46 deathstar bash[969876]: sent 1,849,171 bytes  received 510 bytes  3,699,362.00 bytes/sec
Aug 23 23:04:46 deathstar bash[969876]: total size is 1,847,019  speedup is 1.00
Aug 23 23:04:46 deathstar bash[969865]: all done
Aug 23 23:04:46 deathstar bash[969865]: unmounted...
Aug 23 23:04:46 deathstar systemd[1]: backup@sdf1.service: Succeeded.
Aug 23 23:05:01 deathstar kernel: usb 3-1.5: USB disconnect, device number 67
Aug 23 23:05:04 deathstar kernel: usb 3-1.5: new high-speed USB device number 68 using ehci-pci
Aug 23 23:05:04 deathstar kernel: usb 3-1.5: New USB device found, idVendor=0781, idProduct=5591, bcdDevice= 1.00
Aug 23 23:05:04 deathstar kernel: usb 3-1.5: New USB device strings: Mfr=1, Product=2, SerialNumber=3
Aug 23 23:05:04 deathstar kernel: usb 3-1.5: Product:  SanDisk 3.2Gen1
Aug 23 23:05:04 deathstar kernel: usb 3-1.5: Manufacturer:  USB
Aug 23 23:05:04 deathstar kernel: usb 3-1.5: SerialNumber: 04018a57f24e4dc0135c1f4666b5f2ca4e8e15e65eedfd157b0146cf1427157522b000000000000000000000a03e3c7e008cb3189155810739aa4777
Aug 23 23:05:04 deathstar kernel: usb-storage 3-1.5:1.0: USB Mass Storage device detected
Aug 23 23:05:04 deathstar kernel: scsi host8: usb-storage 3-1.5:1.0
Aug 23 23:05:05 deathstar kernel: scsi 8:0:0:0: Direct-Access      USB      SanDisk 3.2Gen1 1.00 PQ: 0 ANSI: 6
Aug 23 23:05:05 deathstar kernel: sd 8:0:0:0: Attached scsi generic sg3 type 0
Aug 23 23:05:05 deathstar kernel: sd 8:0:0:0: [sdf] 60088320 512-byte logical blocks: (30.8 GB/28.7 GiB)
Aug 23 23:05:05 deathstar kernel: sd 8:0:0:0: [sdf] Write Protect is off
Aug 23 23:05:05 deathstar kernel: sd 8:0:0:0: [sdf] Mode Sense: 43 00 00 00
Aug 23 23:05:05 deathstar kernel: sd 8:0:0:0: [sdf] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
Aug 23 23:05:05 deathstar kernel:  sdf: sdf1
Aug 23 23:05:05 deathstar kernel: sd 8:0:0:0: [sdf] Attached SCSI removable disk
Aug 23 23:05:05 deathstar systemd[1]: Started Our own backup script.
Aug 23 23:05:05 deathstar bash[969947]: running as root will backup to sdf1
Aug 23 23:05:05 deathstar bash[969947]: created /media/backup_usb_stick
Aug 23 23:05:05 deathstar bash[969947]: mounted sdf1
Aug 23 23:05:05 deathstar kernel: EXT4-fs (sdf1): mounted filesystem with ordered data mode. Opts: (null)
Aug 23 23:05:05 deathstar bash[969958]: sending incremental file list
Aug 23 23:05:05 deathstar bash[969958]: sent 796 bytes  received 12 bytes  1,616.00 bytes/sec
Aug 23 23:05:05 deathstar bash[969958]: total size is 1,847,019  speedup is 2,285.91
Aug 23 23:05:05 deathstar bash[969947]: all done
Aug 23 23:05:05 deathstar bash[969947]: unmounted...
Aug 23 23:05:05 deathstar systemd[1]: backup@sdf1.service: Succeeded.
```
