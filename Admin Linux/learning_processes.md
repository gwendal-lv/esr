# Processes	and management in Linux

## Foreground and background

By default a process is launched in the **foreground** of a terminal.
We can observe this behavior by executing a simple `ls -la` command in our home.
It writes it's result to **STDOUT** and gives us back a terminal when the command completes.

```
➜  ~ ls -la
total 184
drwxr-xr-x  8 waldek waldek  4096 Jul  5 08:15 .
drwxr-xr-x  6 root   root    4096 Jun  3 12:41 ..
-rw-------  1 waldek waldek   291 Mar  4 13:10 .bash_history
-rw-r--r--  1 waldek waldek   220 Mar  4 13:05 .bash_logout
-rw-r--r--  1 waldek waldek  3526 Mar  4 13:05 .bashrc
drwx------  4 waldek waldek  4096 May 13 15:14 .config
drwx------  2 waldek waldek  4096 Jul  4 19:05 .elinks
drwx------  3 waldek waldek  4096 Mar  4 13:06 .gnupg
drwxr-xr-x 12 waldek waldek  4096 May  3 20:06 .oh-my-zsh
drwxr-x---  2 waldek waldek  4096 Jul  4 09:25 ovpns
-rw-r--r--  1 waldek waldek   807 Mar  4 13:05 .profile
-rw-------  1 waldek waldek     0 Mar 18 22:32 .python_history
-rw-r--r--  1 waldek waldek    10 Mar  4 13:08 .shell.pre-oh-my-zsh
drwxr-xr-x  2 waldek waldek  4096 Jul  1 12:37 .ssh
-rw-------  1 waldek waldek 15035 Jul  1 12:37 .viminfo
-rw-r--r--  1 waldek waldek   277 Mar 25 12:26 .wget-hsts
-rw-r--r--  1 waldek waldek 49005 Jun 29 11:42 .zcompdump-vps-42975ad1-5.7.1
-rw-------  1 waldek waldek 60990 Jul  5 08:15 .zsh_history
-rw-r--r--  1 waldek waldek  3689 Mar  4 13:08 .zshrc
➜  ~ 
```

This is probably very obvious behaviour by now but now consider the following command `sleep 10`.
This command just **sleeps** for 10 seconds and returns our prompt after.
We use `sleep` to simulate a long running process such as a heavy calculation, think password cracking, or a server of some sort.
We can use **bash syntax** or **signals** to manipulate running processes.

## Jobs

In a new shell execute the `jobs` command.
It will probably return nothing because you don't have any jobs running.
So how can we create jobs?
As mentioned before, we can do it with **bash syntax** or **signals**.
Let's do it with syntax first.

### Bash syntax

If we add a `&` at the end of a command `bash` will send it to the background.
Execute `sleep 10 &` and observe the output.

```
➜  ~ sleep 10 &
[1] 996
➜  ~
```

The sleep command is executed, and running in the background.
We immediately gain control of our terminal again to perform more tasks but after 10 seconds we get the following output indicating our job is done.

```
➜  ~ sleep 10 &
[1] 996
➜  ~ 
[1]  + 996 done       sleep 10
➜  ~ 
```

We can have multiple jobs running at the same time and can inspect them with the `jobs` command.
Try the following in a shell `sleep 5 & sleep 10 & sleep 20 & sleep 30 & sleep 50 &`.
You gain immediate control of the terminal but a list of *background tasks* is displayed first.

```
➜  ~ sleep 5 & sleep 10 & sleep 20 & sleep 30 & sleep 50 &
[1] 1057
[2] 1058
[3] 1059
[4] 1060
[5] 1061
➜  ~ jobs                                                 
[1]    running    sleep 5
[2]    running    sleep 10
[3]    running    sleep 20
[4]  - running    sleep 30
[5]  + running    sleep 50
➜  ~ 
[1]    1057 done       sleep 5
➜  ~ 
[2]    1058 done       sleep 10
➜  ~ 
[3]    1059 done       sleep 20
➜  ~ 
[4]  - 1060 done       sleep 30
➜  ~ 
[5]  + 1061 done       sleep 50
➜  ~ jobs
➜  ~ 
```

Indeed, that's a lot of numbers on your screen.
The numbers between `[]` are the **job ID** numbers and the four digit ones are the **process ID** numbers, or **PID**.
When using the `jobs` command you can sue the job ID to reference a particular job.
For example, run `sleep 30 & sleep 60 & sleep 90 &` and observe the output.
Next run the `jobs` command and not the more verbose output.
All three jobs are **running** and will terminate one by one.
We can bring back a process to the foreground, so we can interact with it from **STDIN**, by running the `fg` command.
If we only have one process running it will bring back this single process but you can choose which one to bring to the foreground by specifying the job ID as such `fg %2` or `fg %3`.

**Can you tell me what the `+` and `-` mean in the jobs list?**

Now, how can we gain control of our terminal again?
Observe the following output:

```
➜  ~ sleep 30 & sleep 60 & sleep 90 &
[1] 13207
[2] 13208
[3] 13209
➜  ~ fg %3
[3]  - 13209 running    sleep 90
^Z
[3]  + 13209 suspended  sleep 90
➜  ~ jobs
[1]    running    sleep 30
[2]  - running    sleep 60
[3]  + suspended  sleep 90
➜  ~
```

First we create three jobs that are sent to the background.
Next we bring job ID number 3 back to the foreground.
We send the **suspend** signal to this job by pressing CTRL-Z.
Note the output from `jobs` which now notes two running jobs and one suspended.
This brings us to **signals**.

### Signals

We use signals all the time without realizing it.
The most common signal we have used is the **SIGINT** that we send when pressing **CTRL-C** on a running process.
A second one most of you know by know is CTRL-Z to suspend a running job.
To see all key combination and their signals we can run the `stty -a` command.

```
speed 38400 baud; rows 30; columns 122; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = <undef>; eol2 = <undef>; swtch = <undef>; start = ^Q;
stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc -ixany -imaxbel iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
```

We can also send signals with the `kill` command.
Contrary to `jobs`, `kill` uses the **PID** numbers to reference running processes.
The PID of a process is shown when you launch it, or you can inspect the PID of all your jobs by executing `jobs -l`.
To demonstrate how to send signals I advise you to run a few long running sleep commands as follows: `sleep 32234 & sleep 324234 & sleep 72552 & sleep 453445 & sleep 96986996 &`

You can now send signals to these processes with the following syntax `kill -$signal_to_send $PID` where `$signal_to_send` is the signal and `$PID` is the process ID.
For example:

```
➜  ~ sleep 32234 & sleep 324234 & sleep 72552 & sleep 453445 & sleep 96986996 &
[1] 13477
[2] 13478
[3] 13479
[4] 13480
[5] 13481
➜  ~ jobs
[1]    running    sleep 32234
[2]    running    sleep 324234
[3]    running    sleep 72552
[4]  - running    sleep 453445
[5]  + running    sleep 96986996
➜  ~ jobs -l    
[1]    13477 running    sleep 32234
[2]    13478 running    sleep 324234
[3]    13479 running    sleep 72552
[4]  - 13480 running    sleep 453445
[5]  + 13481 running    sleep 96986996
➜  ~ kill -STOP 13479
[3]  + 13479 suspended (signal)  sleep 72552                                                                              
➜  ~ jobs -l
[1]    13477 running    sleep 32234
[2]    13478 running    sleep 324234
[3]  + 13479 suspended (signal)  sleep 72552
[4]    13480 running    sleep 453445
[5]  - 13481 running    sleep 96986996
➜  ~ 
```

Analyse the output above step by step to make sense of it.
All of this might seem to complicated but there are some handy features of the shell to help us.
First, to get a list of available signals just type `kill -l` and it will output them to STDOUT.
Secondly, `kill` does **autocomplete** on both **signals** and on the **PID**.
Thirdly, you can specify **multiple PID's** to the `kill` command.

You can use `htop` as well to send signals!
Have a try at this with the same long list of sleep command and not the behavior of the processes.
By stopping and continuing a process you can probably explain me what the `S` column means now no?

## Disown

Up until now all of the commands and examples should work in both `bash` and `zsh`.
To test the following command I advise you to take a `bash` shell because it's [posix](https://en.wikipedia.org/wiki/POSIX) compliant.
When a process starts it's always the **child** of a **parent** process.
You can investigate who is a process's parent with `htop` in the *tree* mode.
An other handy tool is `ps` which reports a snapshot of the current processes.
Let's give `ps` a go.

If you run `ps` in a new shell you should get output similar to codeblock below which shows all running jobs in the current shell.

```
➜  ~ ps
  PID TTY          TIME CMD
13510 pts/0    00:00:00 zsh
14154 pts/0    00:00:00 ps
➜  ~ 
```

If I add a few background jobs the output becomes as follows:

```
➜  ~ sleep 32234 & sleep 324234 & sleep 72552 & sleep 453445 & sleep 96986996 &
[1] 14164
[2] 14165
[3] 14166
[4] 14167
[5] 14168
➜  ~ ps
  PID TTY          TIME CMD
13510 pts/0    00:00:00 zsh
14164 pts/0    00:00:00 sleep
14165 pts/0    00:00:00 sleep
14166 pts/0    00:00:00 sleep
14167 pts/0    00:00:00 sleep
14168 pts/0    00:00:00 sleep
14171 pts/0    00:00:00 ps
➜  ~ 
```

The information above is already quite interesting but we can add or remove columns to the output by using the `o` argument as follows.
Note that each process has a **unique** PID but they all share the same PPID (parent process ID).
Or do they?
Why does the first line, in my case `zsh` have a different PPID?

```
➜  ~ ps o pid,ppid,cmd
  PID  PPID CMD
13510 13509 -zsh
14164 13510 sleep 32234
14165 13510 sleep 324234
14166 13510 sleep 72552
14167 13510 sleep 453445
14168 13510 sleep 96986996
14199 13510 ps o pid,ppid,cmd
➜  ~ 
```

The list of available columns can be found in the `man ps` pages in the **STANDARD FORMAT SPECIFIERS** section (around line 500).
We can specify a specific process with the `-p $PID` argument.

```
➜  ~ ps o pid,ppid,cmd         
  PID  PPID CMD
14466 14465 -zsh
14640 14466 tmux
14643 14642 -zsh
14681 14643 ps o pid,ppid,cmd
➜  ~ ps o pid,ppid,cmd -p 14643
  PID  PPID CMD
14643 14642 -zsh
➜  ~ 
```
Now in this shell I can start a few specific background jobs, simulated with `sleep`.

```
➜  ~ sleep 1111 & sleep 2222 & sleep 3333 &
[1] 14697
[2] 14698
[3] 14699
➜  ~ ps o pid,ppid,cmd
  PID  PPID CMD
14466 14465 -zsh
14640 14466 tmux
14643 14642 -zsh
14697 14643 sleep 1111
14698 14643 sleep 2222
14699 14643 sleep 3333
14702 14643 ps o pid,ppid,cmd
➜  ~
```

If I now `disown` a specific job ID, or all with the `-a` flag the processes will not be dependent on the parent's existance.
A quick `ps o pid,ppid,cmd` will still show the PPID as parent *but* when you close the parent shell and inspect the specific PID of the disowned process you'll see it's now owned by a *different* parent.
I know it sounds complicated but I urge you to test this all out in a few shells.
The practice will explain it a lot better than some codeblocks.

```
➜  ~ ps o pid,ppid,cmd -p 14698
  PID  PPID CMD
14698     1 sleep 2222
➜  ~ 
```

Now why is the process only changing parent once the original parent terminates?
I'm asking you to look for an answer online but the solution can be found the realm of *signals*, especially the *hang up* [signal](https://en.wikipedia.org/wiki/SIGHUP).

## Nohup

TODO

## Zombie processes

Yes, there are such things as zombie processes.
Learning how to create them is a bit out of our scope but I highly advise you to read up a bit on [what](https://en.wikipedia.org/wiki/Zombie_process) they are and [how](https://www.howtogeek.com/701971/how-to-kill-zombie-processes-on-linux/) to deal with them.

## Process priorities

Life is all about setting priorities and while Linux is very good at managing it's CPU time all by itself, sometimes we know better.
We've seen the priorities before in `htop` in the `NI` column but we can view them as well via `ps o nice`.
A more detailed command would be `ps o nice,pid,ppid,args` which for my laptop returns the following:

```
➜  ~ git:(master) ✗ ps o nice,pid,args
 NI   PID COMMAND
  0  2220 zsh
  0  2283 -zsh
  0  2323 /bin/sh /usr/bin/startx
  0  2345 xinit /etc/X11/xinit/xinitrc -- /etc/X11/xinit/xserverrc :0 vt1 -keeptty -auth /tmp/serverauth.8jVsAiU2KQ
  0  2346 /usr/lib/xorg/Xorg -nolisten tcp :0 vt1 -keeptty -auth /tmp/serverauth.8jVsAiU2KQ
  0  2354 x-window-manager -a --restart /run/user/1000/i3/restart-state.2354
  0  5848 zsh
  0  8365 zsh
  0  9036 zsh
  0  9065 newsboat
  0 10478 ssh waldek@86thumbs.net
  0 13113 vim learning_processes.md
  0 13860 ps o nice,pid,args
  0 28084 zsh
➜  ~ git:(master) ✗
```

All my processes are neutral on a scale from *nice* to *not-very-nice*.
You can tell because they are at `0`.
The **nice** scale goes from `-20` being not-at-all-nice to `20` being super friendly towards other processes.
The nicer a process the less aggressive it will be when demanding CPU time.

### Nice

Depending on your system a new process will get a specific nice value.
On my Debian laptop by default processes get `5` as nice value.
We can inspect this as follows where the `ping` command is the new process:

```
➜  ~ git:(master) ✗ ping 8.8.8.8 > /dev/null &
[1] 15428
➜  ~ git:(master) ✗ ps o nice,pid,args -p 15428 
 NI   PID COMMAND
  5 15428 ping 8.8.8.8
➜  ~ git:(master) ✗
```

Let's be nice to start with and set the process to be not aggressive at all.
You can launch a command with a specific nice value by prepending `nice -n 15` before the command.
The value you set will be **added** to the default value as seen below (but tops out at 19 and -19).

```
➜  ~ git:(master) ✗ nice -n 15 ping 8.8.8.8 > /dev/null &
[1] 15632
➜  ~ git:(master) ✗ ps o nice,pid,args -p 15632
 NI   PID COMMAND
 19 15632 ping 8.8.8.8
➜  ~ git:(master) ✗ 
```

Now what about *aggressive* processes?
I would like you to try and set a very *not-nice* value for a `ping` or `sleep` process?
You can probably guess but it won't work.
Why do you think this is?

### Renice

Nice values are not that practical if we need to set them before we start a process no?
That's where the `renice` program comes into play.
It allows us to change the nice value of a running process with a very simple syntax.
I would advise you to use `sudo` when changing the nice values because otherwise you'll constantly run into either `operation not permitted` or `permission denied` errors.

```
➜  ~ git:(master) ✗ ping 8.8.8.8 > /dev/null &
[1] 16877
➜  ~ git:(master) ✗ ps o nice,pid,args -p 16877
 NI   PID COMMAND
  5 16877 ping 8.8.8.8
➜  ~ git:(master) ✗ sudo renice -n 20 -p 16877
16877 (process ID) old priority 5, new priority 19
➜  ~ git:(master) ✗
```

## /proc virtual filesystem

TODO

## Exercises

To help you understand what happens to running and stopped processes I made a few python scripts you can download below.
Run them either with `python3 $SCRIPT_NAME` or `./$SCRIPT_NAME`.

* [simple timer](./assets/processes_ex_01.py)
* [timer with random keyboard prompt](./assets/processes_ex_02.py)
* [custom callback function for SIGALRM](./assets/processes_ex_03.py)
