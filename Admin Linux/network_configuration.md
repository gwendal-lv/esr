# Network configuration

## Network command-line configuration

Modern Linux distributions generaly use the `ip` command line tool to show and manipulate routing, network devices, interfaces and tunnels.

You can verify the command availability and display the actual version using `ip -V`

```
sdejongh@debian-base:~$ ip -V
ip utility, iproute2-5.9.0, libbpf 0.3.0
sdejongh@debian-base:~$
```

As usual you can get some quick help with the `--help` argument.

```
sdejongh@debian-base:~$ ip --help
Usage: ip [ OPTIONS ] OBJECT { COMMAND | help }
       ip [ -force ] -batch filename
where  OBJECT := { link | address | addrlabel | route | rule | neigh | ntable |
                   tunnel | tuntap | maddress | mroute | mrule | monitor | xfrm |
                   netns | l2tp | fou | macsec | tcp_metrics | token | netconf | ila |
                   vrf | sr | nexthop | mptcp }
       OPTIONS := { -V[ersion] | -s[tatistics] | -d[etails] | -r[esolve] |
                    -h[uman-readable] | -iec | -j[son] | -p[retty] |
                    -f[amily] { inet | inet6 | mpls | bridge | link } |
                    -4 | -6 | -I | -D | -M | -B | -0 |
                    -l[oops] { maximum-addr-flush-attempts } | -br[ief] |
                    -o[neline] | -t[imestamp] | -ts[hort] | -b[atch] [filename] |
                    -rc[vbuf] [size] | -n[etns] name | -N[umeric] | -a[ll] |
                    -c[olor]}
sdejongh@debian-base:~$ 
```

The `ip` command unify the network configuration in a single utility which provides several *objects*, each targeting a specific topic, for example:

- `link`: manage network devices

- `address`: manage IPv4 and IPv6 protocol

- `neighbour`: manage ARP (IPv4) and ICMPv6-ND (IPv6) cache entries

- `route`: manage routing table entries

You can get more help about a specific topic using the `ip <object> help` command.

```
sdejongh@debian-base:~$ ip link help
Usage: ip link add [link DEV] [ name ] NAME
            [ txqueuelen PACKETS ]
            [ address LLADDR ]
            [ broadcast LLADDR ]
            [ mtu MTU ] [index IDX ]
            [ numtxqueues QUEUE_COUNT ]
            [ numrxqueues QUEUE_COUNT ]
            type TYPE [ ARGS ]

    ip link delete { DEVICE | dev DEVICE | group DEVGROUP } type TYPE [ ARGS ]

    ip link set { DEVICE | dev DEVICE | group DEVGROUP }
            [ { up | down } ]
            [ type TYPE ARGS ]
        [ arp { on | off } ]
        [ dynamic { on | off } ]
        [ multicast { on | off } ]
        [ allmulticast { on | off } ]
        [ promisc { on | off } ]
        [ trailers { on | off } ]
        [ carrier { on | off } ]
        [ txqueuelen PACKETS ]
        [ name NEWNAME ]
        [ address LLADDR ]
        [ broadcast LLADDR ]
        [ mtu MTU ]
        [ netns { PID | NAME } ]
        [ link-netns NAME | link-netnsid ID ]
        [ alias NAME ]
        [ vf NUM [ mac LLADDR ]
             [ vlan VLANID [ qos VLAN-QOS ] [ proto VLAN-PROTO ] ]
             [ rate TXRATE ]
             [ max_tx_rate TXRATE ]
             [ min_tx_rate TXRATE ]
             [ spoofchk { on | off} ]
             [ query_rss { on | off} ]
             [ state { auto | enable | disable} ]
             [ trust { on | off} ]
             [ node_guid EUI64 ]
             [ port_guid EUI64 ] ]
        [ { xdp | xdpgeneric | xdpdrv | xdpoffload } { off |
              object FILE [ section NAME ] [ verbose ] |
              pinned FILE } ]
        [ master DEVICE ][ vrf NAME ]
        [ nomaster ]
        [ addrgenmode { eui64 | none | stable_secret | random } ]
        [ protodown { on | off } ]
        [ protodown_reason PREASON { on | off } ]
        [ gso_max_size BYTES ] | [ gso_max_segs PACKETS ]

    ip link show [ DEVICE | group GROUP ] [up] [master DEV] [vrf NAME] [type TYPE]

    ip link xstats type TYPE [ ARGS ]

    ip link afstats [ dev DEVICE ]
    ip link property add dev DEVICE [ altname NAME .. ]
    ip link property del dev DEVICE [ altname NAME .. ]

    ip link help [ TYPE ]

TYPE := { vlan | veth | vcan | vxcan | dummy | ifb | macvlan | macvtap |
       bridge | bond | team | ipoib | ip6tnl | ipip | sit | vxlan |
       gre | gretap | erspan | ip6gre | ip6gretap | ip6erspan |
       vti | nlmon | team_slave | bond_slave | bridge_slave |
       ipvlan | ipvtap | geneve | bareudp | vrf | macsec | netdevsim | rmnet |
       xfrm }
sdejongh@debian-base:~$
```

### Common network devices management commands

Network devices management is achieved using the `ip link` command.

#### Displaying network interface devices

```
sdejongh@debian-base:~$ ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: lan: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:87:1c:39 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
3: mgmt: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:f0:db:0f brd ff:ff:ff:ff:ff:ff
    altname enp0s8
sdejongh@debian-base:~$
```

> The network interfaces name `lan` and `mgtm` are not standard. They have been customized by adding `udev` rules.

The command simply lists all network interfaces with some basic low level informations like MAC address, state, ...

#### Enabling or disabling network interface devices

You can enable (turn on) or disable (turn off) any network device using the `ip link set` command.

The following command will disable the *enp0s8* interface.

```
sdejongh@debian-base:~$ sudo ip link set enp0s8 down
```

Using `ip link show` command we can now see that the interface is marked as *state DOWN*.

```
sdejongh@debian-base:~$ ip link show enp0s8
3: mgmt: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT group default qlen 1000
    link/ether 08:00:27:f0:db:0f brd ff:ff:ff:ff:ff:ff
    altname enp0s8
sdejongh@debian-base:~$
```

The next command will enable the interface.

```
sdejongh@debian-base:~$ sudo ip link set enp0s8 up
```

```
sdejongh@debian-base:~$ ip link show enp0s8
3: mgmt: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:f0:db:0f brd ff:ff:ff:ff:ff:ff
    altname enp0s8
sdejongh@debian-base:~$
```

#### Creating and removing network interface devices

Virtual network interfaces like *tunnels*, *sub-interfaces*, *bridges*, ... can be created or deleted using the `ip link add` and `ip link delete` commands.

### Addressing network interfaces

Network interfaces address management is done using the `ip address` command. There are several sub-commands available:

- `ip address add` : add a logical address to the interface.

- `ip address change` : modify an address assigned to an interface.

- `ip address replace` : replace an address assigned to an interface.

- `ip address del` : remove an address from an interface.

- `ip address show` : display addressing informatio,ns about the given interfaceip

- `ip address save` : save the actual address configuration (must be redirected to a file)

- `ip address restore` : restore a saved configuration from a file.

Note: managing dhcp client operations cannot be done using the `ip address` command. To initialize dhcp operations use `dhclient` command.

#### Display addresses related informations

Command:

```
ip address show dev <interface>
```

Example:

```
sdejongh@debian-base:~$ ip add show dev enp0s3
2: lan: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:87:1c:39 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute lan
       valid_lft 86033sec preferred_lft 86033sec
    inet6 fe80::a00:27ff:fe87:1c39/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
sdejongh@debian-base:~$
```

#### Adding an IPv4 address

In case the interface actually use dhcp configuration you can release the lease using the `sudo dhclient -r <interface>` command. You can also request a new lease using the `sudo dhclient` command (the interface must be  defined in the `/etc/network/interfaces` structure)

```
sdejongh@debian-base:~$ sudo dhclient -r enp0s3
Killed old client process
sdejongh@debian-base:~$
```

An important thing to keep in mind with address configuration is that a single interface can have multiple IPv4 and IPv6 addresses. This means that if you need to modify the actual configuration you cannot simply override the it with a new address. You should *delete* the old address and then *add* the new address.

To add a new address use the following command:

```
ip address add <address>/<length> dev <interface>
```

- `address`: the ipv4/6 address

- `length`: the prefix/subnet mask length

- `interface`: the interface name

Examples:

```
sdejongh@debian-base:~$ sudo ip address add 10.0.2.100/24 dev enp0s3
```

```
sdejongh@debian-base:~$ sudo ip address add 2a02:168:4efa:8845:1:cd:ef5:cd01/64 dev enp0s3
```

If you simply repeat the `ip address add` command, you will stack several addresses on the same interface.

```
sdejongh@debian-base:~$ sudo ip address add 192.168.0.1/24 dev enp0s3
sdejongh@debian-base:~$
sdejongh@debian-base:~$ ip address show dev enp0s3
2: lan: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:87:1c:39 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    inet 10.0.2.100/24 scope global lan
       valid_lft forever preferred_lft forever
    inet 192.168.0.1/24 scope global lan
       valid_lft forever preferred_lft forever
    inet6 2a02:168:4efa:8845:1:cd:ef5:cd01/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe87:1c39/64 scope link 
       valid_lft forever preferred_lft forever
sdejongh@debian-base:~$
```

> The *inet6* addres strating with fe80:: is automatically assigned by the operating system. You cannot get rid of it.

#### Deleting addresses from an interface

To delete an address from an interface you can simply call the `ip address del` command, or ... if you need to get rid of all addresses configured on an interface you can also *flush* them using the `ip address flush` command.

The following command deletes an address from the interface:

```
ip address del <address>/<length> dev <interface>
```

- `address`: the ipv4/6 address

- `length`: the prefix/subnet mask length

- `interface`: the interface name

Example:

```
sdejongh@debian-base:~$ sudo ip address del 192.168.0.1/24 dev enp0s3
```

The next command flushes all the currently ipv4 and ipv6 configured address on the interface.

```
ip address flush dev <interface>
```

Example:

```
sdejongh@debian-base:~$ sudo ip address flush dev enp0s3
```

As exepected all addresses have been removed from the interface

```
sdejongh@debian-base:~$ ip address show dev enp0s3
2: lan: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:87:1c:39 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
sdejongh@debian-base:~$
```

### Managing the routing table

Using the `ip` tool tou can manage the routing table of the machine with the `ip route`command.

#### Displaying the routing table

You can get the actual routing table content using the `ip route` command:

```
ip [-6] route
```

The `-6` option is needed if you want to display the IPv6 routing table.

Example:

```
sdejongh@debian-base:~$ ip route
default via 10.0.2.2 dev lan 
10.0.2.0/24 dev lan proto kernel scope link src 10.0.2.15 
sdejongh@debian-base:~$
```

Each line represents a route. Some routes are specific to the network configuration of the interfaces. Routes marked with `score link` refer to the actual network address configuration and represents the direcly connected network itself.

#### Adding routes

The routing table can contain several routes. This means that adding a route doesn't modify the existing ones. If you need to modify a route or replace a route, you will have to *delete* the old one before adding the new one.

The command:

```
ip route add <prefix>/<length> via <next-hop> [dev <interface>]
```

Example:

```
sdejongh@debian-base:~$ sudo ip route add 192.168.0.0/24 via 10.0.2.1 dev enp0s3
```

This command will create a route to the 192.168.0.0/24 network via 10.0.2.1 (the next-hop) and using the *enp0s3* interface to reach the next-hop.

```
sdejongh@debian-base:~$ ip route
default via 10.0.2.2 dev lan 
10.0.2.0/24 dev lan proto kernel scope link src 10.0.2.15 
192.168.0.0/24 via 10.0.2.1 dev lan 
sdejongh@debian-base:~$
```

> Note: the interface *enp0s3* is know as *lan* on this machine because of some *udev* configurations to customize the interface name.

The outbound interface is not required *as long as there is a route to the next-hop* in the routing table. For example i could add a route to 192.168.1.0/24 via 10.0.2.1 using the following command.

```
sdejongh@debian-base:~$ sudo ip route add 192.168.1.0/24 via 10.0.2.1
```

The result is exactly the same.

```
sdejongh@debian-base:~$ ip route
default via 10.0.2.2 dev lan 
10.0.2.0/24 dev lan proto kernel scope link src 10.0.2.15 
192.168.0.0/24 via 10.0.2.1 dev lan 
192.168.1.0/24 via 10.0.2.1 dev lan 
sdejongh@debian-base:~$
```

#### Adding a default route

Adding a default route is also done using the `ip route add` command but you an use a special `default` keyword to keep it simple:

```
ip route add default via <next-hop> [dev <interface>]
```

Example:

```
sdejongh@debian-base:~$ sudo ip route add default via 10.0.2.2 dev enp0s3
```

#### Removing a route

To remove a route from the routing table we can use the `ip route del` command with just enough arguments to identify the route(s) we want to remove.

The command:

```
ip route del <prefix>/<length> [via <next-hop>] [dev <interface>]
```

Example:

This is the actual routing table

```
sdejongh@debian-base:~$ ip route
default via 10.0.2.2 dev lan 
10.0.2.0/24 dev lan proto kernel scope link src 10.0.2.15 
192.168.0.0/24 via 10.0.2.1 dev lan 
192.168.1.0/24 via 10.0.2.1 dev lan 
sdejongh@debian-base:~$
```

If I want to remove the route to 192.168.0.0/24 i could call the following command:

```
sdejongh@debian-base:~$ sudo ip route del 192.168.0.0/24
```

The route has been deleted:

```
sdejongh@debian-base:~$ ip route
default via 10.0.2.2 dev lan 
10.0.2.0/24 dev lan proto kernel scope link src 10.0.2.15 
192.168.1.0/24 via 10.0.2.1 dev lan 
sdejongh@debian-base:~$
```

By the way, you can also pass all available arguments to the command as long as they match the route you want to delete.

```
sdejongh@debian-base:~$ sudo ip route del 192.168.1.0/24 via 10.0.2.1 dev lan
```

This can be usefull if you have multiple routes to the same destination having different next-hop and/or outbound interface.

## Network configuration using configuration files.

### Introduction

By default, if there's not specific network manager (ie: NetworkManager when you install Debian with a graphical interface), or network configuration tool like *netplan* (fount by default with Ubuntu Server 20.04 and later), the network configuration is managed by the **networking** service.

You can manage the *networking* service like any other service on the machine using *systemd*.

```
sdejongh@debian-base:~$ sudo systemctl status networking
● networking.service - Raise network interfaces
     Loaded: loaded (/lib/systemd/system/networking.service; enabled; vendor preset: enabled)
     Active: active (exited) since Wed 2022-09-14 10:18:46 CEST; 1h 11min ago
       Docs: man:interfaces(5)
    Process: 529 ExecStart=/sbin/ifup -a --read-environment (code=exited, status=0/SUCCESS)
   Main PID: 529 (code=exited, status=0/SUCCESS)
      Tasks: 0 (limit: 9473)
     Memory: 4.6M
        CPU: 77ms
     CGroup: /system.slice/networking.service

Sep 14 10:18:46 debian-base ifup[591]: DHCPDISCOVER on lan to 255.255.255.255 port 67 interval 7
Sep 14 10:18:46 debian-base ifup[591]: DHCPOFFER of 10.0.2.15 from 10.0.2.2
Sep 14 10:18:46 debian-base ifup[591]: DHCPREQUEST for 10.0.2.15 on lan to 255.255.255.255 port 67
Sep 14 10:18:46 debian-base dhclient[591]: DHCPOFFER of 10.0.2.15 from 10.0.2.2
Sep 14 10:18:46 debian-base ifup[591]: DHCPACK of 10.0.2.15 from 10.0.2.2
Sep 14 10:18:46 debian-base dhclient[591]: DHCPREQUEST for 10.0.2.15 on lan to 255.255.255.255 port 67
Sep 14 10:18:46 debian-base dhclient[591]: DHCPACK of 10.0.2.15 from 10.0.2.2
Sep 14 10:18:46 debian-base dhclient[591]: bound to 10.0.2.15 -- renewal in 36728 seconds.
Sep 14 10:18:46 debian-base ifup[591]: bound to 10.0.2.15 -- renewal in 36728 seconds.
Sep 14 10:18:46 debian-base systemd[1]: Finished Raise network interfaces.
sdejongh@debian-base:~$
```

As usual you can start/stop/restart/... the service:

```
systemctl <start|stop|restart|...> networking.service
```

And also use `journalctl` to read the logs:

```
sdejongh@debian-base:~$ sudo journalctl -u networking.service
```

The *networking service* will manage all interfaces defined in the `/etc/network/interfaces` file.

The file on the debian system I use along this guide looks like this:

```shell
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

auto lan
iface lan inet dhcp
```

The two last lines won't be present by default. I added them manually to make the *networking service* manage my ethernet interface (as mentionned before the real name of this interface is *enp0s3* but i used *udev* to rename it). 

Let's try to understand each section...

```shell
source /etc/network/interfaces.d/*
```

This line tells the service to load all files in the given directory. This allows us to leave the `/etc/network/interfaces` unchanged and add custom configurations in separated files.

```
auto lo
iface lo inet loopback
```

This section handles the *loopback* interface of the system. The `auto` commands tells the service to try to automatically enable the interface when the service starts.

The second lince defines how the interface should be configured. Here it tells that the interface *lo* should use ipv4 addressing scheme *(inet)* and treated as a loopback interface (configured with the 127.0.0.1/8 address).

The last section is the one I added to make the service handle the ethernet interface.

```
auto lan
iface lan inet dhcp
```

This makes *networking service* try to enable the *lan* interface when it starts and then configure it with an IPv4 address that should be acquired from a dhcp server.

### Enabling/disabling an interface

All interfaces handled by the *networking service* can me enabled or disabled using the `ifup` and `ifdown` commands.

You can also get a list of the interfaces handled by the service using the `ifquery --list` command.

```
sdejongh@debian-base:~$ sudo ifquery --list
lo
lan
sdejongh@debian-base:~$
```

To disable an interface i simply have to call the `ifdown` command.

```
sdejongh@debian-base:~$ sudo ifdown lan
Killed old client process
Internet Systems Consortium DHCP Client 4.4.1
Copyright 2004-2018 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/lan/08:00:27:87:1c:39
Sending on   LPF/lan/08:00:27:87:1c:39
Sending on   Socket/fallback
DHCPRELEASE of 10.0.2.15 on lan to 10.0.2.2 port 67
sdejongh@debian-base:~$
```

As you can see, the network interface was using a dhcp server to get its configuration, when the interface is disabled properly using the `ifdown` command, the dhclp client releases its lease (that's how it should always work).

Now if I want to (re-)enable the interface I can simplyu call the `ifup` command:

```
sdejongh@debian-base:~$ sudo ifup lan
Internet Systems Consortium DHCP Client 4.4.1
Copyright 2004-2018 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/lan/08:00:27:87:1c:39
Sending on   LPF/lan/08:00:27:87:1c:39
Sending on   Socket/fallback
DHCPDISCOVER on lan to 255.255.255.255 port 67 interval 7
DHCPOFFER of 10.0.2.15 from 10.0.2.2
DHCPREQUEST for 10.0.2.15 on lan to 255.255.255.255 port 67
DHCPACK of 10.0.2.15 from 10.0.2.2
bound to 10.0.2.15 -- renewal in 40638 seconds.
sdejongh@debian-base:~$
```

This makes the *networking service* use the interface configuration and in this case launch the dhcp client to retrieve the configuration.

Using `ifup` and `ifdown` is the best way to enable and disable interfaces managed by the *networking service*. Other commands may also work but could interfere with the service and prevent configuration to be correctly applied.

### Configuring interfaces using `/etc/network/interfaces`

Wether you add the configuiration to the main file `/etc/network/interfaces` or in custom files placed in the `/etc/network/interfaces.d/` directory, you have to define each interface you want to handle using the *networking service*.

Each interface must be at least defined by an *iface* line:

```
iface <interface> <protocol> <method>
```

- `interface`: the interface name

- `protocol`: may be *inet* for ipv4 or `inet6`for ipv6

- `method`: may be `dhcp` for dhcp client usage, `static` for manual configuration 

**Before** the *iface* statement you can add optionnal instruction:

- `auto <interface>`: the service wil try to enable the interface when it starts

- `allow-hotplug <interface>`: enable hutplug event detection for the given interface (service will try to enable/disable the interface when it detects a state change)

For example, if we want an interface named `enp0s8` to be enabled when a cable is plugged-in and use dhcp to retrieve its configuration, we should thje following lines to the configuration files:

```
allow-hotplug enp0s8
iface enp0s8 inet dhcp
```

If we want to manually configure the interface, we need to add a few statements to define main settings like the address, the mask, the gateway, ... Those settings must follow the *iface* line.

```
auto enp0s3
iface enp0s3 inet static
    address 192.168.0.50/24            # Sets the ip address and mask:q
    gateway 192.168.0.1                # Address of the default gateway
    dns-nameservers 1.1.1.1 8.8.8.8    # Adresse(s) of the dns server(s)
    
```

This is a typical sample configuration for a network interface. There are a lot of additionnal parameter you can set in the interface definition:

- `up <command>`: will execute the given command when the interface change state to UP

- `down <command>`: will execute the given command when the interface change state to down

- `pre-up <command>`: will execute the given command just before enabling the interface

- `post-down <command>`: will execute the given command after the interface has been disabled

Working with IPv6 is really similar, you cimpli need to add an *iface* section for each interface on which you want to enable IPv6.

Example:

```
iface enp0s3 inet6 static
    address 2a02:acd:201a:49:c00::21ec/64
    gateway fe80::1
```

For more informations you can read `man interfaces`.
