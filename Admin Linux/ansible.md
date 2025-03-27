# Introduction to Ansible

## What is Ansible

Ansible is a suite of software tools that enables [infrastructure as code](https://en.wikipedia.org/wiki/Infrastructure_as_code). It is open-source and the suite includes software provisioning, configuration management, and application deployment functionality

## Base Ansible architecture

Ansible automates the management of remote systems based on a defined desired state. The main component of an ansible architecture are:

- The control node: the system where ansible is run and configured.

- The inventory: an organized list of managed nodes located on the control node.

- The managed nodes: the systems remotely controlled by ansible.

Ansible doesn't need any agent/daemon running on the controlled node an relies on SSH connections an remote Python execution.

A controlled node must fulfill the following requirements:

- Having a SSH server acception connections

- A Python 3 interpreter available

## Installing Ansible

Ansible must only be installed on the **contol node**. There are several methods to install it depending on the operating system you are using. The most common one is using `pip` paclage installer for Python. 

### Installing Python

Depending on your Operating System, you have to choose the appropriate procedure. In most Linux based distributions you can install Python from the official repositories using the bultin package manager such as `apt` for Debian/Ubuntyu based distributions.

On Windows systems, you will need to download the installer from [Download Python | Python.org](https://www.python.org/downloads/).

### Installing PIP

PIP is a common Python package manager, but not the only one, a needs to be installed separately most of the time. 

On Debian/Ubuntu based systems it's recommended to use the built-in package manager and install the `python3-pip` package.

There are a few others methods which are described on this page: [Installation - pip documentation](https://pip.pypa.io/en/stable/installation/)

### Installing Ansible itself

Even if Ansible can be installed from your Operating System package manager, it is always better to install it from the official repositories to ensure you work on the latest release.

```shell
python3 -m pip install --user ansible
```

Once the installation is completed you should be able to check the installed version:

```shell
ansible --version
```

This command will you you the version of the installed `ansible-core` module.

### Upgrading Ansible

To upgrade Ansible using the `pip` utility, you can simply run the following command:

```shell
python3 -m pip install --upgrade --user ansible
```

## Configuring Ansible

### General Ansible configuration

Ansible will search for its configuration file in several places in the following order:

1) `ANSIBLE_CONFIG` : an environment variable if it is set

2) `ansible.cfg` : in the current working directory

3) `~/.ansible.cfg` : in the home directory

4) `/etc/ansible/ansible.cfg` 

The first configuration file found will be applied, the orthers will be ignored.

You can generated a fully commented default configuration file using the following command:

```shell
ansible-config init --disabled > ansible.cfg
```

Or a more complete one with this command:

```shell
ansible-config init --disabled -t all > ansible.cfg
```

You can then use the generated file as starting point for your own configuration.

Here is a sample `ansible.cfg` file with only some parameters defined (all others will use their default values)

```ini
[defaults]
# Define the location of the inventory file
inventory = ~/ansible/hosts.yaml

# Define how many concurrent jobs will be run
forks = 20

# Remove warnings for deprecations notifications
deprecation_warnings = False

# Defines how tasks are handled
strategy = linear

# Enable or disable SSH host key checking
host_key_checking = False
```

### Building the inventory

The Ansible inventory is a file where you define managed nodes. The inventory file can be written using an `ini` style or a `yaml` style.

Basically the inventory can me a simple list of managed nodes, and a simple `ini` formatted inventory file could look like this:

```ini
host1.domain.com
host2.domain.com

[servers]
mail.domain.com
dns.domain.com

[routers]
r1.domain.com
r2.domain.com
```

This simple file defines a list of managed nodes, this means you could *execute* ansible commands on them.

The first two hosts are ungrouped, the `[servers]` and `[routers]`  section define groups. This allows to manage nodes by group (ie: run the same commands on several machines).

The same inventory could be defined in a `YAML` style file:

```yaml
all:
    hosts:
        host1.domain.com:
        host2.comain.com:
    children:
        servers:
            hosts:
                mail.domain.com:
                dns.domain.com:
        routers:
            hosts:
                r1.domain.com:
                r2.domain.com:
```

By default there are two groups: `all` and `ungrouped` :

- `all` : contains all managed nodes

- `ungrouped` : contains all managed nodes not associated with a group

Note that you can add hosts to multiple groups...

```yaml
all:
    children:
        webservers:
            hosts:
                www1.domain.com:
                www2.domain.com:
        dbservers:
            hosts:
                db1.domain.com:
                db2.domain.com:
        servers:
            hosts:
                www1.domain.com:
                www2.domain.com:
                db1.domain.com:
                db2.domain.com:
```

Hosts can also be added using range syntax:

```ini
[clients]
host[01:20].domain.com
```

or

```yaml
all:
    children:
        clients:
            hosts:
                host[01:20].domain.com
```

This would add host01.domain.com to host20.domain.com to the inventory.

### Adding variables to hosts

There are several parameters needed for ansible to work properly, like connection type, host address (if not resolvable using dns), user, password, priviledge method, ...

All those parameters can be defined ( but there are better ways ) in the inventory:

```ini
[servers]
server01    ansible_host=192.168.0.10    ansible_user=admin
server02    ansible_host=192.168.0.20    ansible_user=admin
```

or in YAML style...

```yaml
all:
    children:
        servers:
            hosts:
                server1:
                    ansible_host: 192.168.0.10
                    ansible_user: admin
                server2:
                    ansible_host: 192.168.0.20
                    ansible_user: admin
```

As you can notice, the `ansible_user` variable has the same value for multiple hosts which are in the same group. It's also possible to define thos variables at the group level:

```yaml
all:
    children:
        servers:
            hosts:
                server1:
                    ansible_host: 192.168.0.10
                server2:
                    ansible_host: 192.168.0.20
            vars:
                ansible_user: admin
```

You propably noticed the `children:` key which tells that the `server` group is a children al the default `all` group. You can create groups inside groups using the `children:` key the same way it is done under the `all` group.

Child groups have some special properties:

- Any host that is member of a child group is automatically a member of the parent group.

- A child group’s variables will have higher precedence (override) a parent group’s variables.

- Groups can have multiple parents and children, but not circular relationships.

- Hosts can also be in multiple groups, but there will only be one instance of a host, merging the data from the multiple groups.

### Organizing host and group variables

Having all variables defined in the inventory could result in a real mess. To organize group and host variables we can put them in dedicated files using `YAML` or `JSON` format and with an optionnal valid extension: `.yaml`, `.yml` or `.json`.

Those files must be named accoring to the related group or host name and should be located in sub-directories based on the inventory file path:

```bash
...
inventory.yaml
group_vars/
    servers.yaml    # servers group variables
host_vars/
    server1.yaml    # server1 host variables
    server2.yaml    # server2 host variables
```

### Behavioral inventory parameters

There is a huge list of available behavioral varaibles that can be set for hosts or groups which defines how Ansible will interact with the managed nodes. The following variables are the most commonly used:

| Parameter             | Description                                                                             | Value                                  |
| --------------------- | --------------------------------------------------------------------------------------- | -------------------------------------- |
| ansible_host          | The name of the host to connect to, if different from the alias you wish to give to it. | a domain name or ip address            |
| ansible_port          | The connection port number, if not the default (22 for ssh)                             | the port number                        |
| ansible_user          | The user name to use when connecting to the host.                                       | the user login                         |
| ansible_password      | The password to use to authenticate to the host.                                        | the password                           |
| ansible_become        | Will use privilege escalation or not                                                    | *yes* or *no*                          |
| ansible_become_method | Escalation method to use                                                                | ex: *sudo*, *enable*, ...              |
| ansible_connection    | The connection plugin to use                                                            | ex: *ssh*, *local*, *network_cli*, ... |

## Working with ansible

One you build your inventory you can begin to work with ansible to manage remote hosts.

### Testing hosts reachability

Ansible comes with some basic fuctions like `ping` wich will test the managed nodes reacability. There are two mains things that will be checked:

- Can Ansible establish an SSH connection to the host

- Can Ansible fin a remote python interpreter on the managed host

To do that you simply need to issue the following command:

```shell
ansible -m ping <host/group>
```

The command should return a JSON formatted message like the one below:

```json
08:38:31 sdejongh@jarvis ansible ±|master|→ ansible -m ping gns3-server
gns3-server | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
08:38:37 sdejongh@jarvis ansible ±|master|→
```

or in case of failure...

```json
08:38:37 sdejongh@jarvis ansible ±|master|→ ansible -m ping l213-00
l213-00 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: ssh: connect to host 172.30.12.100 port 22: Connection timed out",
    "unreachable": true
}
08:40:25 sdejongh@jarvis ansible ±|master|→
```

### Creating playbooks

Ansiple playbooks contain *plays* which are the basic units of Ansible Execution. Ansiple playbooks are written in YAML.

Here is an example of a simple playbook:

```yaml
---
- name: Check hosts reachability
  hosts: all
  
  tasks:
    - name: Ansible ping
      ansible.builtin.ping:

- name: Update debian linux servers packages
  host: servers

  tasks:
    - name: Update repositories cache database
      ansible.builtin.apt:
        update_cache: yes

    - name: Update all packages to their latest version
      ansible.builtin.apt:
        name: "*"
        state: latest
```

As usual, the usage of the YAML format keep the fil extremely readable. The `---` at the start of the file is mandatory ans marks the begining of the YAML document.

This playbook contains two plays. The first one use the builtin ansible ping module to test the reachability on all hosts defined in the inventory.

The second play will be applied only on the hosts in the *servers* group, will update the reprository cache database and upgrade all installed packages to their latest version. As you can see each play can also be composed of several tasks.

Each task can be based on a specific module or use the same depending on what you want to do. Ypou can find more information about availables modules here: [Ansible - Collection index](https://docs.ansible.com/ansible/latest/collections/index.html)

### Checking playbook syntax

Before running a plybook it's always a good idea to check its syntax. This can be achieved using the `ansible-playbook` command with the `--syntax-check` option.

```bash
ansible-playbook <path_to_the_playbook_file> --syntax-check
```

If no error is reported you should see an output like this:

```bash
09:03:42 sdejongh@jarvis l209 ±|master|→ ansible-playbook ./81_shutdown.yaml --syntax-check

playbook: ./81_shutdown.yaml
09:03:57 sdejongh@jarvis l209 ±|master|→ 
```

### Running playbooks

To run a playbook you need to call the `ansible-playbook` command. Basically you just need to pass the playbook file path...

```bash
ansible-playbook <path_to_the_playbook_file>
```

You can eventually filter hosts to which the playbook is applied using the `-l <host/group>` option (but they must be defined in the playbook).

```shell
ansible-playbook -l <host|group> <path_to_the_playbook_file>
```

When a playbook is run, Ansible will report status informations about each task for each host and a general summary.

In the example below I simply ran a playbook which restarts the hosts:

```
09:10:29 sdejongh@jarvis l213 ±|master|→ ansible-playbook ./80_reboot.yaml 

PLAY [Reboot hosts] *********************************************************************************************************************************************************

TASK [Reboot] ***************************************************************************************************************************************************************
changed: [l213-04]
changed: [l213-11]
changed: [l213-08]
changed: [l213-02]
changed: [l213-05]
changed: [l213-10]
changed: [l213-09]
changed: [l213-06]
changed: [l213-12]
changed: [l213-07]
changed: [l213-01]
changed: [l213-03]
changed: [l213-00]

PLAY RECAP ******************************************************************************************************************************************************************
l213-00                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-01                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-02                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-03                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-04                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-05                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-06                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-07                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-08                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-09                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-10                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-11                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
l213-12                    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

09:11:35 sdejongh@jarvis l213 ±|master|→
```

As you can see, the recap tells you what has been done, what has failed, which host was unreachable etc.

### Digging deeper

This is just the emerged part of the iceberg. Ansible has a lot of features and functionnalities, but you should now have a good idea of what it is and what is is used for.

Here is a list of some ressouces to dig deeper in the world of Ansible:

- [User Guide &mdash; Ansible Documentation](https://docs.ansible.com/ansible/latest/user_guide/index.html) : Learn to write tasks, plays and playbooks

- [Roles &mdash; Ansible Documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) : Ansible roles or reusing what you already created

- [Encrypting content with Ansible Vault &mdash; Ansible Documentation](https://docs.ansible.com/ansible/latest/user_guide/vault.html) : Encrypting file content, passwords, ...


