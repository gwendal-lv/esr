# Secure Shell (SSH)

## What is SSH

SSH is *the* current standard for remote logins but you might want to read up a bit on what was used before SSH existed. [This](https://www.jeffgeerling.com/blog/brief-history-ssh-and-remote-access) is a pretty good blog post on the history of SSH.
You should never use the following the following programs anymore but it's good to be aware of their historic existance.

* rlogin
* rsh
* rcp
* telnet (still has some legitimate usage such as with munin)

The main advantage of SSH is it's **encryption**.
It works similarly to SSL which you use all the time to do most of your web browsing.
When using encryption it becomes **very** hard to sniff the data traveling between the client and the server.
There are two versions of SSH, version 1 and version 2, and you should only use version 2 as the former is not considered [secure]() anymore.
The recommended encryption used by most SSH servers is [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard). If you're interested in understanding the mathematics behind AES, [this](https://www.youtube.com/channel/UC1usFRN4LCMcfIV7UjHNuQg) class is exceptionally good but not for the faint of heart.
It's however not mandatory to fully understand the math behind encryption to use it though.
The main takeaway would be the number of **bit's used** where **higher** is **better**.
By default ssh uses a very secure cipher but you can specify which one you want with the `-c` flag to `ssh`. Do keep in mind that the server needs to support the cipher you're requesting.

## SSH keypair

We just mentionned that SSH uses encryption to secure the communication between the client and the server. The data flowing between both machines are encrypted using a symetric cypher algorithm (ie: AES).

The base principe of a symetric algorithm is that both sides use the same encryption key to encrypt or decrypt data. This means that the server and the client must exchange the encryption keys, and if they would simply send the key over the network, anybody who would catch the key could decrypt data sent by the machines.

To secure the symetric algorithm key exchange SSH uses an asymetric cypher algorithm like **RSA** or **Deffie Hellman**.

Asymmetric algorithms use pairs of keys. Each pair consists of a **public key** (which may be known to others) and a **private** (which may not be known by anyone except the owner). The key pair is mathematically related so that whatever is encrypted with a public or private key can only be decrypted by its corresponding counterpart.

![](./assets/ssh_keypair.png)

Both side must exchange their public keys tu be able to authenticate each other and be able to establish an ecrypted communication channel.

![](./assets/ssh_key_exchange.png)

Now that they got their respective public keys, they can use them to either *sign* data or *encrypt* data.

### Data encryption/decryption

To *encrypt* data, the sender must use the recipient public key to transform the original data. So here for example, if Bob want to send encrypted data to Alice, he must use Alice's public key. As said before, something encrypted with one of the key (public or private) can only be decrypted with its corresponding counterpart. Thus Alice will use her private key to decrypt the data.

Because the private key should only be known by its owener, only the owner of the corresponding public key will be able to decrypt the data.

![](./assets/ssh_encrypt.png)

### Signing data

The concept of digital signature use the exact opposite principe. The idea is to guarantee that the sender cannot be repudiated.

When sending data to Alice, Bob will encrypt the data and a related hash value with his private key. The result can only be decrypted using Bob's public key. Thus when Alice receive the encrypted data, if she can decrypt it with Bob's public key she knows the data have been encrypted with Bob's private key and therefore only Bob can be the sender.

![](./assets/ssh_sign.png)

## Analyzing an SSH connection estabishment

Let's establish an ssh connection using the `-v` option get some debug informations.

```
sdejongh@debian-base:~$ ssh -v sdejongh@172.30.4.36
```

The command syntax is: `ssh -v userlogin@host`

A lot of stuff is shown with the debug option, so i'll split it into several blocks to make it clear...

The first part is all about reading configuration files and establishing a TCP connection to the destination host.

```
OpenSSH_8.4p1 Debian-5+deb11u1, OpenSSL 1.1.1n  15 Mar 2022
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 19: include /etc/ssh/ssh_config.d/*.conf matched no files
debug1: /etc/ssh/ssh_config line 21: Applying options for *
debug1: Connecting to 172.30.4.36 [172.30.4.36] port 22.
debug1: Connection established.
```

Next, the client tries to identify the available SSH keys. Lines ending with `type -1` mean the corresponding key was not found.

```
debug1: identity file /home/sdejongh/.ssh/id_rsa type 0
debug1: identity file /home/sdejongh/.ssh/id_rsa-cert type -1
debug1: identity file /home/sdejongh/.ssh/id_dsa type -1
debug1: identity file /home/sdejongh/.ssh/id_dsa-cert type -1
debug1: identity file /home/sdejongh/.ssh/id_ecdsa type -1
debug1: identity file /home/sdejongh/.ssh/id_ecdsa-cert type -1
debug1: identity file /home/sdejongh/.ssh/id_ecdsa_sk type -1
debug1: identity file /home/sdejongh/.ssh/id_ecdsa_sk-cert type -1
debug1: identity file /home/sdejongh/.ssh/id_ed25519 type -1
debug1: identity file /home/sdejongh/.ssh/id_ed25519-cert type -1
debug1: identity file /home/sdejongh/.ssh/id_ed25519_sk type -1
debug1: identity file /home/sdejongh/.ssh/id_ed25519_sk-cert type -1
debug1: identity file /home/sdejongh/.ssh/id_xmss type -1
debug1: identity file /home/sdejongh/.ssh/id_xmss-cert type -1
```

Now both client and server compare their SSH version.

```
debug1: Local version string SSH-2.0-OpenSSH_8.4p1 Debian-5+deb11u1
debug1: Remote protocol version 2.0, remote software version OpenSSH_8.9p1 Ubuntu-3
debug1: match: OpenSSH_8.9p1 Ubuntu-3 pat OpenSSH* compat 0x04000000
```

Both versions match, so the client starts the authentication process.

```
debug1: Authenticating to 172.30.4.36:22 as 'sdejongh'
```

The next step is the keys exchange process which implies defining the algorithms and exchanging the keys.

```
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: algorithm: curve25519-sha256
debug1: kex: host key algorithm: ecdsa-sha2-nistp256
debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
```

The client now tries to verify the server identify based on its `known_hosts` file. If the host key does not match the entry in the file, the client will refuse to establish the connection.

```
debug1: Server host key: ecdsa-sha2-nistp256 SHA256:GNknIzloIBJWqdBdN4wyR79hRPoToWWQnytteSEfOoI
debug1: Host '172.30.4.36' is known and matches the ECDSA host key.
debug1: Found key in /home/sdejongh/.ssh/known_hosts:1
```

Next, both client an servers will exchange the sessions keys (used to encrypt the communication). Those keys will generally be regenerated and exchanged after some time.

```
debug1: rekey out after 134217728 blocks
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: SSH2_MSG_NEWKEYS received
debug1: rekey in after 134217728 blocks
```

Now that everything is setup, the client and server will manage the user authentication. They need to agree on key type and exchange method and also on authentication method. By default the client will first try to authenticate using public keys and fallback to password authentication if needed.

```
ebug1: Will attempt key: /home/sdejongh/.ssh/id_rsa RSA SHA256:dQwbkFybgQPzghg+0W0zXTzJxKbIVkfFXCZIfr/i1/0 agent
debug1: Will attempt key: /home/sdejongh/.ssh/id_dsa 
debug1: Will attempt key: /home/sdejongh/.ssh/id_ecdsa 
debug1: Will attempt key: /home/sdejongh/.ssh/id_ecdsa_sk 
debug1: Will attempt key: /home/sdejongh/.ssh/id_ed25519 
debug1: Will attempt key: /home/sdejongh/.ssh/id_ed25519_sk 
debug1: Will attempt key: /home/sdejongh/.ssh/id_xmss 
debug1: SSH2_MSG_EXT_INFO received
debug1: kex_input_ext_info: server-sig-algs=<ssh-ed25519,sk-ssh-ed25519@openssh.com,ssh-rsa,rsa-sha2-256,rsa-sha2-512,ssh-dss,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ecdsa-sha2-nistp256@openssh.com,webauthn-sk-ecdsa-sha2-nistp256@openssh.com>
debug1: kex_input_ext_info: publickey-hostbound@openssh.com (unrecognised)
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,password
debug1: Next authentication method: publickey
debug1: Offering public key: /home/sdejongh/.ssh/id_rsa RSA SHA256:dQwbkFybgQPzghg+0W0zXTzJxKbIVkfFXCZIfr/i1/0 agent
debug1: Authentications that can continue: publickey,password
debug1: Trying private key: /home/sdejongh/.ssh/id_dsa
debug1: Trying private key: /home/sdejongh/.ssh/id_ecdsa
debug1: Trying private key: /home/sdejongh/.ssh/id_ecdsa_sk
debug1: Trying private key: /home/sdejongh/.ssh/id_ed25519
debug1: Trying private key: /home/sdejongh/.ssh/id_ed25519_sk
debug1: Trying private key: /home/sdejongh/.ssh/id_xmss
debug1: Next authentication method: password
sdejongh@172.30.4.36's password: 
debug1: Authentication succeeded (password).
Authenticated to 172.30.4.36 ([172.30.4.36]:22).
```

Finally, the session is established, client and server exchenge some environment settings like session type, language, ...

```
debug1: channel 0: new [client-session]
debug1: Requesting no-more-sessions@openssh.com
debug1: Entering interactive session.
debug1: pledge: network
debug1: client_input_global_request: rtype hostkeys-00@openssh.com want_reply 0
debug1: Sending environment.
debug1: Sending env LANG = en_GB.UTF-8
```

## Generating SSH keypair

If you want to use SSH public key authentication (instead of basic password authentication), you first need to generate your own keypair. By default your private and public keys will be stored in your home directory structure in `~/.ssh/`. 

The standard `openssh-client` package comes with a key management tool: `ssh-keygen`.

It allows you to create several key types: rsa (default), dsa, ecdsa, ecdsa-sk, ed25519 and ed25519-sk. You can get a bit more information about those key types here [SSH keys - ArchWiki](https://wiki.archlinux.org/title/SSH_keys) or if you want to dig deeper [Comparing SSH Keys - RSA, DSA, ECDSA, or EdDSA?](https://goteleport.com/blog/comparing-ssh-keys/)

If you didn't generate any key yet, your `~/.ssh/` folder should only contain ventually a `known_hosts` file.

```
sdejongh@debian-base:~$ ls -al ./.ssh
total 12
drwx------  2 sdejongh sdejongh 4096 Sep 26 10:44 .
drwxr-xr-x 15 sdejongh sdejongh 4096 Sep 26 10:09 ..
-rw-r--r--  1 sdejongh sdejongh  222 Sep 26 09:01 known_hosts
sdejongh@debian-base:~$
```

To generate a new keypair you just need to call the `ssh-keygen` tool.

```
ssh-keygen [-t <type>] [-b <bits>] [-d <filename>] [-N <passphrase>]
```

Without any parameter, *ssh-keygen* will generate a new *rsa* key of 3072 bits and store it as `id_rsa` and `id_rsa.pub`.

```
sdejongh@debian-base:~$ ssh-keygen 
Generating public/private rsa key pair.
Enter file in which to save the key (/home/sdejongh/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/sdejongh/.ssh/id_rsa
Your public key has been saved in /home/sdejongh/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:sUd2+4+fQEquc8Kp0eMe2hRppHA7SCEI0JtZRbdlnkI sdejongh@debian-base
The key's randomart image is:
+---[RSA 3072]----+
|=... +o E o      |
| .. o .o = .     |
|   = o .+.= .    |
|  + . + +*.. .   |
|     . +S+....   |
|        +.+ o.   |
|       ..=.o ..  |
|        *=+.  .o.|
|       oo=+   .oo|
+----[SHA256]-----+
sdejongh@debian-base:~$
```

Keep in mind that generating a new key with the same filename will completely erase the old keys which could prevent you from accessing some remote hosts.

If you cant to generate an *ed25519* keypair you just need to run the command again:

```
sdejongh@debian-base:~$ ssh-keygen -t ed25519
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/sdejongh/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/sdejongh/.ssh/id_ed25519
Your public key has been saved in /home/sdejongh/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:YoxbZwO1MilvBwDF2g6ep0Wig2Awu/Mk1qRpPtA9buc sdejongh@debian-base
The key's randomart image is:
+--[ED25519 256]--+
|  .+o   .        |
|o   .. o .       |
|.o o. * .        |
|o.+.o= =         |
|+==B. B S        |
|O==.*= = .       |
|=* =..           |
| oo o .          |
|  .. oE          |
+----[SHA256]-----+
sdejongh@debian-base:~$
```

You now should find bith *rsa* and *ed25519* pribate and public keys in your `~/.ssh/` folder.

```
sdejongh@debian-base:~$ ls -al ~/.ssh
total 28
drwx------  2 sdejongh sdejongh 4096 Sep 26 10:54 .
drwxr-xr-x 15 sdejongh sdejongh 4096 Sep 26 10:09 ..
-rw-------  1 sdejongh sdejongh  411 Sep 26 10:54 id_ed25519
-rw-r--r--  1 sdejongh sdejongh  102 Sep 26 10:54 id_ed25519.pub
-rw-------  1 sdejongh sdejongh 2610 Sep 26 10:50 id_rsa
-rw-r--r--  1 sdejongh sdejongh  574 Sep 26 10:50 id_rsa.pub
-rw-r--r--  1 sdejongh sdejongh  222 Sep 26 09:01 known_hosts
sdejongh@debian-base:~$
```

> IMPORTANT: you should never share your private keys. Never!

## Deploying SSH keys

If you want to authenticate to a server using your publickey, you first need to install it on the server itself. Each user will have a `~/.ssh/authorized_keys` file containing all public keys that should be accepted.

Let's see what this file looks like on a real host:

```
ssh-ed25519 AAAAF3NzaC1lZDI1NTE5AAAAINHPP1j/fVK0xFMkG106KIZF6s9SpRMkQTPihKtL48AQ sdejongh@debian-base

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCJheJZG06GJkVsNEjfkBOd+1Woj8JJuZwpUXlYgkJB9PaGgJV19MRD9g2ygCWqaSee/V9P3yAlyrEl2tLaroAKT73jOQTVTw7vzHtLd0KwsUt24N/NjGSxINRDhYZ3AFZar5//YDg/o5MUT199Vx84jKJzEqpiBgk6N+75r+COanda6FL0AaYBwUoy9LDhm/IDqI4YZD6QIEF8W5h6GZwfrijGjla7sYK0Ql3T6m7YvOOzuaQj5flIDguyED7oSP1NLPn0BKLG8ORacGfAtkCNpjmfR10bRBI5rGmSGvcaG3pbOWu7iHc5PKy+6U69HaK6GbbAFsVv9KVAFu0WSOLvMbIXxk4E72Vv2yRsKEQTB4xXQW68VPYBEfx4DyqQtjRrJQ+daFbgzO5i9G+n8x2ioRT4eb4+I8Uyjy/rLyGraVncsAHwdIpFO4ijK91Htk0DqjmJqdX46pV5a0LQz2Uc5cOpfzkSL9IubN+qmB/sp+Td1+TrWjapa0/nBTxsjds= sdejongh@jarvis
```

Each line describe a public key authorized for the given user, in this case in `/home/sdejongh/authorized_keys` on the server.

You can manually add or remove keys frim this file. The line formaty is simple:

```
<ssh-type> <key value> <description>
```

Although we can manually edit this file, it's often easier and less risky to use tghe `ssh-copy-id` tool which comes with the `openssh-client` package. Password authentication must be enabled on the ssh server if you don't have any key installed yet. The usage is quite simple:

```
ssh-copy-id [-i <public key file>] username@host [-p <port>]
```

 The `-i` option allows you to specify which key to install on the remote machine.

```
sdejongh@debian-base:~$ ssh-copy-id -i /home/sdejongh/.ssh/id_ed25519.pub sdejongh@172.30.4.5
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/sdejongh/.ssh/id_ed25519.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
sdejongh@172.30.4.5's password: 

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'sdejongh@172.30.4.5'"
and check to make sure that only the key(s) you wanted were added.

sdejongh@debian-base:~$
```

Once the key is installed on the remote server, you should be able to login without password thanks to the public key authentication.

## Using SSH

### Opening a remote session

The most common way to use SSH is to lon into a remote machine.

```
sdejongh@debian-base:~$ ssh
usage: ssh [-46AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface]
           [-b bind_address] [-c cipher_spec] [-D [bind_address:]port]
           [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
           [-i identity_file] [-J [user@]host[:port]] [-L address]
           [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-p port]
           [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
           [-w local_tun[:remote_tun]] destination [command]
sdejongh@debian-base:~$
```

The standard way to log into a machine shoud be:

```
ssh -l <username> <host>
```

But it's also possible and generally prefered to use a more user friendly approach:

```
ssh <username>@<host>
```

By default the ssh client will try to authenticate using all available public keys present in `~/.ssh/` and fallback to password authentication if needed and allowed by the server.

It's also possible to specify which key to use for authentication using the `-i` option:

```
ssh -i <path to public key> <username>@<host>
```

This what i would do to open a remote session on the given host using my public ed25519 key.

```
sdejongh@debian-base:~$ ssh -i /home/sdejongh/.ssh/id_ed25519 sdejongh@172.30.4.5
Linux DeepRed 4.19.66-v7+ #1253 SMP Thu Aug 15 11:49:46 BST 2019 armv7l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Sep 26 11:40:44 2022 from 172.30.4.28
<11:44:50 2022-09-26> [sdejongh] ~ $
```

### Executing remote commands

Another common way to use the ssh client is to execute commands on the remote machine. It works almost as if you forst log into the machine, then execute the command, and finally close the session.

The standard output and error are passed through the ssh connection which means that you can get the output of the remote executed command on your screen.

The main restriction is that you cannot run interactive commands this way.

```
ssh <username>@<host> <command>
```

 Let's for example run the `ip link` command on a remote host:

```
sdejongh@debian-base:~$ ssh sdejongh@172.30.4.5 ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether b8:27:eb:ca:12:f9 brd ff:ff:ff:ff:ff:ff
3: wlan0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN mode DORMANT group default qlen 1000
    link/ether b8:27:eb:9f:47:ac brd ff:ff:ff:ff:ff:ff
4: eth0.300@eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether b8:27:eb:ca:12:f9 brd ff:ff:ff:ff:ff:ff
6: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/none 
sdejongh@debian-base:~$
```

It's important to understand that the `ip link` command has been run on the `172.30.4.5` host and only the output of the command is shown on your local computer.

If you need to pass special characters (pipe, redirection, conditions, ... ) within the command line, you will need to put the command between quotes or double-quotes.

```
sdejongh@debian-base:~$ ssh sdejongh@172.30.4.5 "echo Hello World! > ~/hello.txt"
```

This command will establish an ssh connection to the `172.30.4.5` host and write *Hello World!* to the `~/hello.txt` file.

Let's verify...

```
sdejongh@debian-base:~$ ssh sdejongh@172.30.4.5 cat ~/hello.txt
Hello World!
sdejongh@debian-base:~$
```

### Transfering files

#### SCP (Secure Copy Protocol) vs SFTP (SSH File Transfer Protocol)

Both `scp` and `sftp` are transfer protocols working through an SSH channel. While `scp` allows you to easily an securely transfer (and only transfer files) between twho hosts, `sftp` provides all required function to fully manage the remote file system (creating/deleting directories, deleting files, copying files, ...)

#### Using SCP

`scp` usage is straightforward and is based on the same principes as `cp` and `ssh`.

```
scp [options] <source> <destination>
```

Both source and destination can be either a local or remote path. For example, I can copy my *lorem.txt* file to my remote home folder on the `172.30.4.5` host:

```
sdejongh@debian-base:~$ scp ./lorem.txt sdejongh@172.30.4.5:/home/sdejongh/
lorem.txt                                                                                                                                  100% 2413   633.7KB/s   00:00    
sdejongh@debian-base:~$
```

- `./lorem.txt` : the source file on the local machine

- `sdejongh@172.30.4.5:/home/sdejongh/` : the remote path

The remote path must follow the following structure:

```
[<user>@]<host>:<absolute path>
```

Using the same principe I can copy the `~/hello.txt` file on the remote host to my local current directory:

```
sdejongh@debian-base:~$ scp sdejongh@172.30.4.5:/home/sdejongh/hello.txt ./
hello.txt                                                                                                                                  100%   13     4.4KB/s   00:00    
sdejongh@debian-base:~$
```

It's also possible to copy a file between two remote hosts with a single `scp` command but it actualy requires a few more steps. For more informations you can read this detailed post: [linux - scp between two remote hosts from my (third) pc - Super User]().

If you need to copy a whole directory instead of a single file, you'll need to use the `-r` option:

```
sdejongh@debian-base:~$ scp -r sdejongh@172.30.4.36:/home/sdejongh/Projects/tests ./
main.py                                                                                                                                    100%  526   265.2KB/s   00:00    
async_server.py                                                                                                                            100%  651   307.5KB/s   00:00    
modules.xml                                                                                                                                100%  262   123.2KB/s   00:00    
workspace.xml                                                                                                                              100% 4447     1.8MB/s   00:00    
tests.iml                                                                                                                                  100%  284   157.8KB/s   00:00    
.gitignore                                                                                                                                 100%   47     7.0KB/s   00:00    
Project_Default.xml                                                                                                                        100%  902   329.6KB/s   00:00    
profiles_settings.xml                                                                                                                      100%  174    77.1KB/s   00:00    
misc.xml                                                                                                                                   100%  185    76.6KB/s   00:00    
sdejongh@debian-base:~$
```

As you can see `scp` copied all files and directories recursively including to my local system:

```
sdejongh@debian-base:~$ ls -al ./tests
total 20
drwxr-xr-x  3 sdejongh sdejongh 4096 Oct  3 11:28 .
drwxr-xr-x 16 sdejongh sdejongh 4096 Oct  3 11:28 ..
-rw-r--r--  1 sdejongh sdejongh  651 Oct  3 11:28 async_server.py
drwxr-xr-x  3 sdejongh sdejongh 4096 Oct  3 11:28 .idea
-rw-r--r--  1 sdejongh sdejongh  526 Oct  3 11:28 main.py
sdejongh@debian-base:~$
```

#### Using SFTP

`sftp` usage is similar to classical command line ftp clients. The idea is to establish a connection to the remote system and then pass commands to the server.

```
sdejongh@debian-base:~$ sftp -h
usage: sftp [-46AaCfNpqrv] [-B buffer_size] [-b batchfile] [-c cipher]
          [-D sftp_server_path] [-F ssh_config] [-i identity_file]
          [-J destination] [-l limit] [-o ssh_option] [-P port]
          [-R num_requests] [-S program] [-s subsystem | sftp_server]
          destination
sdejongh@debian-base:~$
```

You should notice that there is no *source* information to specify. In fact `sftp` works a bit like a two panel file file manager. 

##### Establishing the connection

Before anything else you must establish a connection to the remote host

```
sdejongh@debian-base:~$ sftp sdejongh@172.30.4.5
Connected to 172.30.4.5.
sftp>
```

 Once you areconnected to the remote host, `sftp` will provide you with a new prompt and wait for your insttructions.

The are several commands available, the most important are:

- `help`: will obviously shows the help file

- `ls`: list files of the current directory on the remote host

- `lls`: list files of the current directory on the local host

- `cd`: change directory on the remote side

- `lcd`: change directory locally

- `pwd`: display the current remote directory

- `lpwd`: display the current local directory

- `mkdir`: create a new directory on the remote side

- `lmkdir`: create a new directory locally

- `put`: upload a local file to the remote host

- `get`: download a file from remote host to the local system 

- `quit`: quit sftp interface.

##### Working remotely

In the following example, i created the `/home/sdejongh/Documents/upload/` directory on the remote host and then i uploaded the `lorem.txt` file from the current local directory.

```
sftp> pwd
Remote working directory: /home/sdejongh
sftp> ls
Bureau             Documents          Images             Modèles           Musique            Public             Python             Téléchargements  Vidéos            
configs            hello.txt          lorem.txt          rssh.py            rssh2.py           rssh3.py           vlans
sftp> cd Documents
sftp> pwd
Remote working directory: /home/sdejongh/Documents
sftp> mkdir upload
sftp> cd upload
sftp> pwd
Remote working directory: /home/sdejongh/Documents/upload
sftp> lls
Desktop  Documents  Downloads  hello.txt  lorem.txt  Music  Pictures  Public  Templates  test  tests  Videos
sftp> put lorem.txt
Uploading lorem.txt to /home/sdejongh/Documents/upload/lorem.txt
lorem.txt                                                                                                                                  100% 2413   174.3KB/s   00:00    
sftp> ls
lorem.txt  
sftp> quit
```

As you can see, using `sftp` interactively is straightforward, just simply need to use commands as if you were directly on the remote host.

In the last example I simply used commands successively, but with most commands like `cd`, `ls`, `put`, `get`... you can also use relative and absolute path. The next example would do exactly the same thing than the previous one:

```
sftp> mkdir Documents/upload
sftp> put lorem.txt Documents/upload/lorem.txt
```

##### Using sftp scripts

It's also possible to automate `sftp` operations using sftp scripts. You first need to create a file containing all needed commands you want to send like in my `test.sftp`file:

```
sdejongh@debian-base:~$ cat test.sftp 
mkdir /home/sdejongh/Documents/newfiles
put /home/sdejongh/lorem.txt /home/sdejongh/Documents/newfiles/lorem.txt
sdejongh@debian-base:~$
```

And finally you need to pass the script (also named *batch*) with the `-b` option to the sftp command ... and voila!

```
sdejongh@debian-base:~$ sftp -b ./test.sftp sdejongh@172.30.4.5
sftp> mkdir /home/sdejongh/Documents/newfiles
sftp> put /home/sdejongh/lorem.txt /home/sdejongh/Documents/newfiles/lorem.txt
sdejongh@debian-base:~$
```

### Running remote GUI applications

SSH allows you to forward X-Server based GUI through its encrypted channel. In other words you can run remote graphical applications on your local computer.

For X-Forwarding to work properly, there are some requirements:

- The remote host must have X-Server running, many graphical linux distribution use X as its graphical engine acctually, but a new engine called *wayland* appeared a few years ago and will probably replace X in most distributions. Debian/Ubuntu based system use Wayland when there is no dedicated GPU (NVidia/AMD graphic cards).

- The ssh server on the remote host must allow X-Forwarding which is the default setting with `open-ssh` server. (We'll see later how to customize both client and server configurations).

- The client must allow X-forwarding, this is done using the `-X` option when establising the remote session.

If all requirements are met, the process is simple:

1) Establish the ssh connection using the `-X` option.

2) Call the graphical application as if you were on the remote command line locally.

```
sdejongh@jarvis:~$ ssh -X sdejongh@192.168.56.25
Linux debian-base 5.10.0-17-amd64 #1 SMP Debian 5.10.136-1 (2022-08-13) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Oct  4 08:44:52 2022 from 192.168.56.1
sdejongh@debian-base:~$ 
sdejongh@debian-base:~$ xclock
```

`xclock` is a graphical clock application. You should now see the clock app on your screen as if it was run locally, but it really runs on the remote host.

## Customizing SSH

Both SSH client and SSH servers work out of the box, but they also both have configuration files allowing us to customize their behaviour.

### Customizing SSH Client

The main configuration of the SSH client is `/etc/ssh/ssh_config` and it defines all default parameters of the `ssh` command.

This file also dynamically include all `.conf` files found in `/etc/ssh/ssh_config.d/` which is a good place to define all the system wide custom parameters.

The last place where SSH client configuration can be found is in the `~/.ssh/config` file. This file doesn't exist by default but can be created to store all your personnal ssh settings.

There are a lot of available parameters and everything is explained in `man ssh_config`.

#### Some interesting SSH client paramteters

##### Host

```
Host    Restricts the following declarations (up to the next Host or Match keyword) to be only for those hosts that match one of the patterns given after the key‐
             word.  If more than one pattern is provided, they should be separated by whitespace.  A single ‘*’ as a pattern can be used to provide global defaults for
             all hosts.  The host is usually the hostname argument given on the command line (see the CanonicalizeHostname keyword for exceptions).

             A pattern entry may be negated by prefixing it with an exclamation mark (‘!’).  If a negated entry is matched, then the Host entry is ignored, regardless
             of whether any other patterns on the line match.  Negated matches are therefore useful to provide exceptions for wildcard matches.
```



##### Ciphers

```
Ciphers
             Specifies the ciphers allowed and their order of preference.  Multiple ciphers must be comma-separated.  If the specified list begins with a ‘+’ character,
             then the specified ciphers will be appended to the default set instead of replacing them.  If the specified list begins with a ‘-’ character, then the
             specified ciphers (including wildcards) will be removed from the default set instead of replacing them.  If the specified list begins with a ‘^’ character,
             then the specified ciphers will be placed at the head of the default set.

             The supported ciphers are:

                   3des-cbc
                   aes128-cbc
                   aes192-cbc
                   aes256-cbc
                   aes128-ctr
                   aes192-ctr
                   aes256-ctr
                   aes128-gcm@openssh.com
                   aes256-gcm@openssh.com
                   chacha20-poly1305@openssh.com

             The default is:

                   chacha20-poly1305@openssh.com,
                   aes128-ctr,aes192-ctr,aes256-ctr,
                   aes128-gcm@openssh.com,aes256-gcm@openssh.com

             The list of available ciphers may also be obtained using "ssh -Q cipher".

```



##### HostKeyAlgorithms

```
HostKeyAlgorithms
             Specifies the host key signature algorithms that the client wants to use in order of preference.  Alternately if the specified list begins with a ‘+’ char‐
             acter, then the specified signature algorithms will be appended to the default set instead of replacing them.  If the specified list begins with a ‘-’
             character, then the specified signature algorithms (including wildcards) will be removed from the default set instead of replacing them.  If the specified
             list begins with a ‘^’ character, then the specified signature algorithms will be placed at the head of the default set.  The default for this option is:

                ssh-ed25519-cert-v01@openssh.com,
                ecdsa-sha2-nistp256-cert-v01@openssh.com,
                ecdsa-sha2-nistp384-cert-v01@openssh.com,
                ecdsa-sha2-nistp521-cert-v01@openssh.com,
                sk-ssh-ed25519-cert-v01@openssh.com,
                sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,
                rsa-sha2-512-cert-v01@openssh.com,
                rsa-sha2-256-cert-v01@openssh.com,
                ssh-ed25519,
                ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,
                sk-ecdsa-sha2-nistp256@openssh.com,
                sk-ssh-ed25519@openssh.com,
                rsa-sha2-512,rsa-sha2-256

             If hostkeys are known for the destination host then this default is modified to prefer their algorithms.

             The list of available signature algorithms may also be obtained using "ssh -Q HostKeyAlgorithms".

```



##### Hostname

```
Hostname
             Specifies the real host name to log into.  This can be used to specify nicknames or abbreviations for hosts.  Arguments to Hostname accept the tokens de‐
             scribed in the TOKENS section.  Numeric IP addresses are also permitted (both on the command line and in Hostname specifications).  The default is the name
             given on the command line.
```

##### KexAlgorithms

```
KexAlgorithms
             Specifies the available KEX (Key Exchange) algorithms.  Multiple algorithms must be comma-separated.  If the specified list begins with a ‘+’ character,
             then the specified algorithms will be appended to the default set instead of replacing them.  If the specified list begins with a ‘-’ character, then the
             specified algorithms (including wildcards) will be removed from the default set instead of replacing them.  If the specified list begins with a ‘^’ charac‐
             ter, then the specified algorithms will be placed at the head of the default set.  The default is:

                   curve25519-sha256,curve25519-sha256@libssh.org,
                   ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,
                   sntrup761x25519-sha512@openssh.com,
                   diffie-hellman-group-exchange-sha256,
                   diffie-hellman-group16-sha512,
                   diffie-hellman-group18-sha512,
                   diffie-hellman-group14-sha256

             The list of available key exchange algorithms may also be obtained using "ssh -Q kex".
```

##### Port

```
Port    Specifies the port number to connect on the remote host.  The default is 22.##### User
```

##### User

```
User    Specifies the user to log in as.  This can be useful when a different user name is used on different machines.  This saves the trouble of having to remem‐
             ber to give the user name on the command line.
```

#### Configuration sample

Here is an example of a working `~/.ssh/config` file.

```
KexAlgorithms +diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha1,diffie-hellman-group-exchange-sha1,diffie-hellman-group1-sha1
Ciphers +aes256-ctr,aes128-ctr,aes256-cbc,aes128-cbc,3des-cbc
HostKeyAlgorithms +ssh-rsa

Host metal.*.lan
    User steve
    Port 22
```

The first three lines add some algorithms for key exchange, ciphers and host keys which are needed for some legacy devices (which does not support latest algorithms).

The *Host* block defines default parameters for any host matching the wildcard definition. This allows me to simply call `ssh metal.brussels.lan` without specify the user, port, etc.

Those settings are handy for interactive commands but can also be really helpful when you need to use `ssh` inside scripts. Combining those definitions and public key authentication allows you to simplify the script and put all connection parameters elsewhere. If you later need to change the username or anything else, you con't need to modify your script. Only the `ssh_config` must be updated.

### Customizing the SSH server

The SSH server configuration can be found in `/etc/ssh/sshd_config`. This file also dynamicaly includes all `.conf` files in `/etc/ssh/sshd_config.d/` directory.

As usual all parameters are explained in `man sshd_config`.

#### Some interresting SSH server settings

##### AddressFamily

```
AddressFamily
             Specifies which address family should be used by sshd(8).  Valid arguments are any (the default), inet (use IPv4 only), or inet6 (use IPv6 only).
```

##### AllowGroups

```
AllowGroups
             This keyword can be followed by a list of group name patterns, separated by spaces.  If specified, login is allowed only for users whose primary group or
             supplementary group list matches one of the patterns.  Only group names are valid; a numerical group ID is not recognized.  By default, login is allowed
             for all groups.  The allow/deny groups directives are processed in the following order: DenyGroups, AllowGroups.
```

##### AllowUsers

```
AllowUsers
             This keyword can be followed by a list of user name patterns, separated by spaces.  If specified, login is allowed only for user names that match one of
             the patterns.  Only user names are valid; a numerical user ID is not recognized.  By default, login is allowed for all users.  If the pattern takes the
             form USER@HOST then USER and HOST are separately checked, restricting logins to particular users from particular hosts.  HOST criteria may additionally
             contain addresses to match in CIDR address/masklen format.  The allow/deny users directives are processed in the following order: DenyUsers, AllowUsers.
```

##### AuthenticationMethods

```
AuthenticationMethods
             Specifies the authentication methods that must be successfully completed for a user to be granted access.  This option must be followed by one or more
             lists of comma-separated authentication method names, or by the single string any to indicate the default behaviour of accepting any single authentication
             method.  If the default is overridden, then successful authentication requires completion of every method in at least one of these lists.

             For example, "publickey,password publickey,keyboard-interactive" would require the user to complete public key authentication, followed by either password
             or keyboard interactive authentication.  Only methods that are next in one or more lists are offered at each stage, so for this example it would not be
             possible to attempt password or keyboard-interactive authentication before public key.

             For keyboard interactive authentication it is also possible to restrict authentication to a specific device by appending a colon followed by the device
             identifier bsdauth or pam.  depending on the server configuration.  For example, "keyboard-interactive:bsdauth" would restrict keyboard interactive authen‐
             tication to the bsdauth device.

             If the publickey method is listed more than once, sshd(8) verifies that keys that have been used successfully are not reused for subsequent authentica‐
             tions.  For example, "publickey,publickey" requires successful authentication using two different public keys.

             Note that each authentication method listed should also be explicitly enabled in the configuration.

             The available authentication methods are: "gssapi-with-mic", "hostbased", "keyboard-interactive", "none" (used for access to password-less accounts when
             PermitEmptyPasswords is enabled), "password" and "publickey".
```

##### Banner

```
Banner  The contents of the specified file are sent to the remote user before authentication is allowed.  If the argument is none then no banner is displayed.  By
             default, no banner is displayed.
```

##### Ciphers

```
Ciphers
             Specifies the ciphers allowed.  Multiple ciphers must be comma-separated.  If the specified list begins with a ‘+’ character, then the specified ciphers
             will be appended to the default set instead of replacing them.  If the specified list begins with a ‘-’ character, then the specified ciphers (including
             wildcards) will be removed from the default set instead of replacing them.  If the specified list begins with a ‘^’ character, then the specified ciphers
             will be placed at the head of the default set.

             The supported ciphers are:

                   3des-cbc
                   aes128-cbc
                   aes192-cbc
                   aes256-cbc
                   aes128-ctr
                   aes192-ctr
                   aes256-ctr
                   aes128-gcm@openssh.com
                   aes256-gcm@openssh.com
                   chacha20-poly1305@openssh.com

             The default is:

                   chacha20-poly1305@openssh.com,
                   aes128-ctr,aes192-ctr,aes256-ctr,
                   aes128-gcm@openssh.com,aes256-gcm@openssh.com

             The list of available ciphers may also be obtained using "ssh -Q cipher".
```

##### DenyGroups

```
DenyGroups
             This keyword can be followed by a list of group name patterns, separated by spaces.  Login is disallowed for users whose primary group or supplementary
             group list matches one of the patterns.  Only group names are valid; a numerical group ID is not recognized.  By default, login is allowed for all groups.
             The allow/deny groups directives are processed in the following order: DenyGroups, AllowGroups.

             See PATTERNS in ssh_config(5) for more information on patterns.
```

##### DenyUsers

``` 
DenyUsers
             This keyword can be followed by a list of user name patterns, separated by spaces.  Login is disallowed for user names that match one of the patterns.
             Only user names are valid; a numerical user ID is not recognized.  By default, login is allowed for all users.  If the pattern takes the form USER@HOST
             then USER and HOST are separately checked, restricting logins to particular users from particular hosts.  HOST criteria may additionally contain addresses
             to match in CIDR address/masklen format.  The allow/deny users directives are processed in the following order: DenyUsers, AllowUsers.

             See PATTERNS in ssh_config(5) for more information on patterns.

```

##### HostKeyAlgorithms

```
HostKeyAlgorithms
             Specifies the host key algorithms that the server offers.  The default for this option is:

                ecdsa-sha2-nistp256-cert-v01@openssh.com,
                ecdsa-sha2-nistp384-cert-v01@openssh.com,
                ecdsa-sha2-nistp521-cert-v01@openssh.com,
                sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,
                ssh-ed25519-cert-v01@openssh.com,
                sk-ssh-ed25519-cert-v01@openssh.com,
                rsa-sha2-512-cert-v01@openssh.com,
                rsa-sha2-256-cert-v01@openssh.com,
                ssh-rsa-cert-v01@openssh.com,
                ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,
                sk-ecdsa-sha2-nistp256@openssh.com,
                ssh-ed25519,sk-ssh-ed25519@openssh.com,
                rsa-sha2-512,rsa-sha2-256,ssh-rsa

             The list of available key types may also be obtained using "ssh -Q HostKeyAlgorithms".
```

##### KexAlgorithms

```
KexAlgorithms
             Specifies the available KEX (Key Exchange) algorithms.  Multiple algorithms must be comma-separated.  Alternately if the specified list begins with a ‘+’
             character, then the specified methods will be appended to the default set instead of replacing them.  If the specified list begins with a ‘-’ character,
             then the specified methods (including wildcards) will be removed from the default set instead of replacing them.  If the specified list begins with a ‘^’
             character, then the specified methods will be placed at the head of the default set.  The supported algorithms are:

                   curve25519-sha256
                   curve25519-sha256@libssh.org
                   diffie-hellman-group1-sha1
                   diffie-hellman-group14-sha1
                   diffie-hellman-group14-sha256
                   diffie-hellman-group16-sha512
                   diffie-hellman-group18-sha512
                   diffie-hellman-group-exchange-sha1
                   diffie-hellman-group-exchange-sha256
                   ecdh-sha2-nistp256
                   ecdh-sha2-nistp384
                   ecdh-sha2-nistp521
                   sntrup4591761x25519-sha512@tinyssh.org

             The default is:

                   curve25519-sha256,curve25519-sha256@libssh.org,
                   ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,
                   diffie-hellman-group-exchange-sha256,
                   diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,
                   diffie-hellman-group14-sha256

             The list of available key exchange algorithms may also be obtained using "ssh -Q KexAlgorithms".
```

##### ListenAddress

```
ListenAddress
             Specifies the local addresses sshd(8) should listen on.  The following forms may be used:

                   ListenAddress hostname|address [rdomain domain]
                   ListenAddress hostname:port [rdomain domain]
                   ListenAddress IPv4_address:port [rdomain domain]
                   ListenAddress [hostname|address]:port [rdomain domain]

             The optional rdomain qualifier requests sshd(8) listen in an explicit routing domain.  If port is not specified, sshd will listen on the address and all
             Port options specified.  The default is to listen on all local addresses on the current default routing domain.  Multiple ListenAddress options are permit‐
             ted.  For more information on routing domains, see rdomain(4).

```

##### UsePAM

```
UsePAM  Enables the Pluggable Authentication Module interface.  If set to yes this will enable PAM authentication using ChallengeResponseAuthentication and
             PasswordAuthentication in addition to PAM account and session module processing for all authentication types.

             Because PAM challenge-response authentication usually serves an equivalent role to password authentication, you should disable either
             PasswordAuthentication or ChallengeResponseAuthentication.

             If UsePAM is enabled, you will not be able to run sshd(8) as a non-root user.  The default is no.
```

##### X11Forwarding

```
X11Forwarding
             Specifies whether X11 forwarding is permitted.  The argument must be yes or no.  The default is no.

             When X11 forwarding is enabled, there may be additional exposure to the server and to client displays if the sshd(8) proxy display is configured to listen
             on the wildcard address (see X11UseLocalhost), though this is not the default.  Additionally, the authentication spoofing and authentication data verifica‐
             tion and substitution occur on the client side.  The security risk of using X11 forwarding is that the client's X11 display server may be exposed to attack
             when the SSH client requests forwarding (see the warnings for ForwardX11 in ssh_config(5)).  A system administrator may have a stance in which they want to
             protect clients that may expose themselves to attack by unwittingly requesting X11 forwarding, which can warrant a no setting.

             Note that disabling X11 forwarding does not prevent users from forwarding X11 traffic, as users can always install their own forwarders.

```
