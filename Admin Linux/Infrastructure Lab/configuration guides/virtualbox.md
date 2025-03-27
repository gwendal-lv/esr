# Adding more than 4 network interfaces to a VM
The Virtualbox GUI only allows 4 network interfaces, but Vbox comes with a cli tool allowing to manage VM completely: *vboxmanage*

## Adding more interfaces on a Windows Host computer

The *VboxManage.exe* tool is by default located in *C:\Program Files\Oracle\VirtualBox*. The folder isn't defined in window PATH, so you forst need to *cd* there.

General command structure
```
VBoxManage.exe modifyvm <vmname|vmid> <option> <value>
```

Defining the network interface
- vmname: textual name of the VM
- vmid: vbox id of the VM
- id: vbox VM interface id range from 1 to N
```
VBoxManage.exe modifyvm <vmname|vmid> --nic<id> none|null|nat|natnetwork|bridged|intnet|hostonly|generic
```

Defining interface type
```
VboxManage.exe modifyvm <vmname|vmid> --nictype<id> Am79C970A|Am79C973|82540EM|82543GC|82545EM|virti
```

(Dis)connect virtual cable of the interface
```
VboxManage.exe modifyvm <vmname|vmid> --cableconnected<id> on|off
```

Defining HotsOnly adapter (for interface defined as *hostonly*)
```
VboxManage.exe modifyvm <vmname|vmid> --hostonlyadapter<id> none|<devicename>
```

Defining internal network for the interface (for interface defined as *intnet*)
```
VboxManage.exe modifyvm <vmname|vmid> --intnet<id> <intnet name>
```

## Linux based hosts
The only difference is the name of the tool filename: *VboxManage*  
File location can be different depending on the host operating system.

## More informations
See official page: [https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-modifyvm.html](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-modifyvm.html)