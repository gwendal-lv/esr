# Archiving and Compression

## Introduction

Archiving and compression tools have different goals but are often used together.

Archiving means combining multiple files into one archive file (e.g. tar file). Compression tools are used to reduce the size of files using lossless algorithms (e.g. gzip).

## Archiving files using `tar`

Most Unix/Linux systems comes at least with `GNU tar` which is a core utility to manipulate achives files named *tarballs*.

> GNU tar is an archiving program designed to store multiple files in a single file (an archive), and  to  manipu‐
>        late  such archives.  The archive can be either a regular file or a device (e.g. a tape drive, hence the name of
>        the program, which stands for tape archiver), which can be located either on the local or on a remote machine.

### Basic `tar` usage

As ususal you can find all needed information using `man tar`.

#### Create a new archive

When creating a new archive you need to give the *archive path* and the files you want to put in the archive.

```
tar -c -f <archive file> <files>
```

You can pass a list of files to include separated by a space or use usual wildcard symbols like `*`.

Let's say i want to create an archive containing `.txt`  files in my current directory...

```
sdejongh@debian-base:~/archives$ ls -al
.rw-r--r--   13 sdejongh  3 Oct 11:17 hello.txt
.rw-r--r-- 2.4k sdejongh  3 Oct 11:11 lorem.txt
drwxr-xr-x    - sdejongh 10 Oct 10:27 otherfiles
.rw-r--r--  121 sdejongh 10 Oct 10:29 README.md
.rw-r--r--   23 sdejongh 10 Oct 10:23 useless.txt
sdejongh@debian-base:~/archives$
```

I can simply list all files...

```
sdejongh@debian-base:~/archives$ tar -c -f archive1.tar hello.txt lorem.txt useless.txt
```

or ... i could use wildcards ...

```
sdejongh@debian-base:~/archives$ tar -c -f archive2.tar *.txt
```

We can also list the content of an archive using the `-t` option.

```
tar -t <archive>
```

Let's see what we find in our two new archives...

```
sdejongh@debian-base:~/archives$ tar -t -f archive1.tar
hello.txt
lorem.txt
useless.txt
sdejongh@debian-base:~/archives$ tar -t -f archive2.tar
hello.txt
lorem.txt
useless.txt
sdejongh@debian-base:~/archives$
```

As expected both archives contain the same files.

By default `tar` recursively reads all sub directories and include their content.

Let's create a new archive containing all files in the current directory and its sub-directory.

```
sdejongh@debian-base:~/archives$ tar -c -f full_archive.tar *
```

Now let's have a look at what we put in the archive...

```
sdejongh@debian-base:~/archives$ tar -t -f full_archive.tar 
archive1.tar
archive2.tar
hello.txt
lorem.txt
otherfiles/
otherfiles/alphabet.txt
otherfiles/alphanum.txt
otherfiles/neofetch.txt
README.md
useless.txt
sdejongh@debian-base:~/archives$
```

As you can see all files and subdirectories have peen packed as well as the two archives we created just before.

#### Analyzing archive content

We can list the archive content using the `-t` option.

```
tar -t -f <archive>
```

There are a lot of other options we can use to get more infirmations. The `-v` option will give us more informations about the content of the archive...

```
sdejongh@debian-base:~/archives$ tar -tv -f full_archive.tar 
-rw-r--r-- sdejongh/sdejongh 10240 2022-10-10 10:30 archive1.tar
-rw-r--r-- sdejongh/sdejongh 10240 2022-10-10 10:31 archive2.tar
-rw-r--r-- sdejongh/sdejongh    13 2022-10-03 11:17 hello.txt
-rw-r--r-- sdejongh/sdejongh  2413 2022-10-03 11:11 lorem.txt
drwxr-xr-x sdejongh/sdejongh     0 2022-10-10 10:27 otherfiles/
-rw-r--r-- sdejongh/sdejongh    52 2022-10-10 10:26 otherfiles/alphabet.txt
-rw-r--r-- sdejongh/sdejongh   780 2022-10-10 10:27 otherfiles/alphanum.txt
-rw-r--r-- sdejongh/sdejongh  1627 2022-10-10 10:25 otherfiles/neofetch.txt
-rw-r--r-- sdejongh/sdejongh   121 2022-10-10 10:29 README.md
-rw-r--r-- sdejongh/sdejongh    23 2022-10-10 10:23 useless.txt
sdejongh@debian-base:~/archives$
```

We can now see that the archive contains a lot of metadata associated with the files (owner, permissions, date, ...).

We can also ask `tar` to list informations about specific files/directories:

```
sdejongh@debian-base:~/archives$ tar -tv -f full_archive.tar *.txt
-rw-r--r-- sdejongh/sdejongh 13 2022-10-03 11:17 hello.txt
-rw-r--r-- sdejongh/sdejongh 2413 2022-10-03 11:11 lorem.txt
-rw-r--r-- sdejongh/sdejongh   23 2022-10-10 10:23 useless.txt
sdejongh@debian-base:~/archives$
```

Here we find all files at the root of the archive matching the `*.txt` pattern. Note that the files in the subdirectory isn't list because the directory doesn't match the pattern.

We could also want to list all `.txt` files found in any subdirectory (but not in the root directory) of the archive

```
sdejongh@debian-base:~/archives$ tar -tv -f full_archive.tar */*.txt
-rw-r--r-- sdejongh/sdejongh 52 2022-10-10 10:26 otherfiles/alphabet.txt
-rw-r--r-- sdejongh/sdejongh 780 2022-10-10 10:27 otherfiles/alphanum.txt
-rw-r--r-- sdejongh/sdejongh 1627 2022-10-10 10:25 otherfiles/neofetch.txt
sdejongh@debian-base:~/archives$
```

#### Extracting files from an archive

Extracting files from an archive will simply copy its content to the desired location. The `-x` option tells `tar` to extract files from the archive. We can combine it with the `-v` option to get some verbose output of the extraction

```
tar -x [-v] -f <archive>
```

I created an empty directory `~/destination` where i want to extract the `full_archive.tar`. From the destination directory i simply need to call `tar -xvf <filepath>` command.

```
sdejongh@debian-base:~/destination$ tar -xvf ../archives/full_archive.tar 
archive1.tar
archive2.tar
hello.txt
lorem.txt
otherfiles/
otherfiles/alphabet.txt
otherfiles/alphanum.txt
otherfiles/neofetch.txt
README.md
useless.txt
sdejongh@debian-base:~/destination$
```

It's also possible to only extract needed files, we must simply specify which memeber of the archive we need.

```
sdejongh@debian-base:~/destination$ tar -xvf ../archives/full_archive.tar hello.txt
hello.txt
sdejongh@debian-base:~/destination$
```

We can specify which subdirectory to extract too..

```
sdejongh@debian-base:~/destination$ tar -xv -f ~/archives/full_archive.tar otherfiles/
otherfiles/
otherfiles/alphabet.txt
otherfiles/alphanum.txt
otherfiles/neofetch.txt
sdejongh@debian-base:~/destination$
```

When used as standard user (non-root user), tar will extract files and applies permissions based on your `umask` settings. If you want to preserve permissions as set in the archive, you need to use the `-p` option.

```
tar -xvp -f <archive>
```

Note that this is the default behavious when `tar` is run by a super-user.

#### Adding files at the end of an archive

If you need a append a file to an archive you can use the `-r` flag.

```
tar -r -f <archive> <files>
```

In the following example I previously created an archive *archive.tar*.

```
sdejongh@debian-base:~/archives$ tar -t -f archive.tar 
hello.txt
lorem.txt
otherfiles/
otherfiles/alphabet.txt
otherfiles/alphanum.txt
otherfiles/neofetch.txt
README.md
useless.txt
sdejongh@debian-base:~/archives$
```

Now i will add the *newfile.txt* to the same archive...

```
sdejongh@debian-base:~/archives$ tar -r -f archive.tar newfile.txt
```

... and finally verify if it has been added.

```
sdejongh@debian-base:~/archives$ tar -t -f archive.tar 
hello.txt
lorem.txt
otherfiles/
otherfiles/alphabet.txt
otherfiles/alphanum.txt
otherfiles/neofetch.txt
README.md
useless.txt
newfile.txt
sdejongh@debian-base:~/archives$
```

As you can see the *newfile.txt* has been added at the end of the archive.

#### Comparing archive content with the local files

`tar` also allows you to compare the archive content with the actual files on your drive using the `-d` option.

```
tar -dv -f <archive>
```

I modified the `~/destination/hello.txt` file. this means its size and date changed.

We can now compare the archive content with the current directory...

```
sdejongh@debian-base:~/destination$ tar -d -f ../archives/full_archive.tar 
hello.txt: Mod time differs
hello.txt: Size differs
sdejongh@debian-base:~/destination$
```

### Advanced `tar` usage

Creating and extracting archives allows us to package files into one single file and store/share it easily. It's especially more efficient than transferring each file separately. By the way this could be done using other tools. The real power of an achive management tool is to allow us to package files wisely, in other words, without storing several time the same file if it has not been modified.

There are three main principes often referenced as *full backup*, *incremental backup* and *differential backup*.

A *full backup* is the first stage of a backup strategy and will store any file wether or not it has previously been stored in another backup.

An *incremental backup* only stores file which have been modified or created since the last backup regardless of its nature.

A *differential backup* only stores files which have been modified or created since the last  *full* or *incremental* backup. This means that if you make successive *differential backups*, each one will also contain files stored in the previous differential. The differential backup is not part of tar features.

#### Creating incremental backups

Let's say i want to backup data in my `~/Documents/` directory using an incremental strategy. This is the actual content of the folder:

```
sdejongh@debian-base:~/backups$ ls -al  ~/Documents/
.rw-r--r-- 0 sdejongh 14 Oct  9:28 one.txt
.rw-r--r-- 0 sdejongh 14 Oct  9:28 three.txt
.rw-r--r-- 0 sdejongh 14 Oct  9:28 two.txt
sdejongh@debian-base:~/backups$
```

Let's now create the initial backup.

```
sdejongh@debian-base:~/backups$ tar -cv -g documents.snar -f documents_00.tar ~/Documents/*
tar: Removing leading `/' from member names
/home/sdejongh/Documents/one.txt
tar: Removing leading `/' from hard link targets
/home/sdejongh/Documents/three.txt
/home/sdejongh/Documents/two.txt
sdejongh@debian-base:~/backups$
sdejongh@debian-base:~/backups$
sdejongh@debian-base:~/backups$ tar -t -f documents_00.tar 
home/sdejongh/Documents/one.txt
home/sdejongh/Documents/three.txt
home/sdejongh/Documents/two.txt
sdejongh@debian-base:~/backups$
```

As you can see I used `-c` to create the archive, `-v` to display informations about the process and `-f` to define the archive file name. The new `-g` is used to specify the journal of the archive, *documents.snar* in this case (note that the extension doens't matter, but *.snar* is commonly used for that), the file where all metadata of the backup process will be stored. This file will allow `tar` to keep track of changes made for the next backup.

You should notice that `tar` stored all files in the archive. This is because the journal didn't exist, and thus tar proceed to a *full backup*.

Now i will make some changes to my `~/Documents` folder...

```
sdejongh@debian-base:~/backups$ touch ~/Documents/four.txt 
sdejongh@debian-base:~/backups$ echo "a bunch of words" > ~/Documents/two.txt
```

I will now backup again my documents using the incremental strategy. It's important to keep in mind that an incremental backup will only stores changes made since previous backup regardless of its nature. This means that the actual state of my data will be split into different files (the successive incremental archives), that's the reason why its **mandatory** to give a newfile name for the next backup...

```
sdejongh@debian-base:~/backups$ tar -cv -g documents.snar -f documents_01.tar ~/Documents/*
tar: Removing leading `/' from member names
/home/sdejongh/Documents/four.txt
tar: Removing leading `/' from hard link targets
/home/sdejongh/Documents/two.txt
sdejongh@debian-base:~/backups$
sdejongh@debian-base:~/backups$
sdejongh@debian-base:~/backups$ tar -t -f documents_01.tar 
home/sdejongh/Documents/four.txt
home/sdejongh/Documents/two.txt
sdejongh@debian-base:~/backups$
```

Now we can see that only the new file and the file which has been modifed were stored in the second archive.

Each time i will need to make a backup of my data, i will call the same commabnd, using the same journal file *documents.snar* **but** with a new archive filename.

#### Restoring incremental backups

Extracting files from an incremental backup is a bit more tricky than a standard archive file. There a few things to keep in mind:

- By default the archive will store file and their original full path.

- When extracting a file using the `-G` flag, `tar` will restore the state of the data based on the archive deleting files not present in the archive.
  
  > At least this is what the official documentation says... Sometimes `tar` won't delete those files. This behaviour is related to the version of `tar` you are using.

- To restore a specific state, you need to extract all the incremental steps following their creation order.

So, If i want to restore the original state of my documents, here's what i need to do:

```
sdejongh@debian-base:~/backups$ tar -xv -G -C / -f ./documents_00.tar
home/sdejongh/Documents/one.txt
home/sdejongh/Documents/three.txt
home/sdejongh/Documents/two.txt
sdejongh@debian-base:~/backups$
```

To restore the last state of my documents, i'd need to extract all the incremental archives, one by one, in the same order they were created.

## File compression

File compression is a data compression method in which the logical size of a file is reduced to save disk space for easier and faster transmission over a network or the Internet. It enables the creation of a version of one or more files with the same data at a size substantially smaller than the original file.

There are several compression format and tools available like zip/unzip, gzip, bz2, lzh, ... They all deserve the same goal: reduce the size of data staored or transfered.

### GZIP

`gzip` is one of the most used compression tool on *-nix* systems. Most of the dime gzip file will end with the `.gz` extension.

#### (un)Compressiong a single file using `gzip`

Let's take a basic set of files...

```
sdejongh@debian-base:~/archives$ ls -al
.rw-r--r--  20k sdejongh 14 Oct  9:12 archive.tar
.rw-r--r--   13 sdejongh  3 Oct 11:17 hello.txt
.rw-r--r-- 2.4k sdejongh  3 Oct 11:11 lorem.txt
.rw-r--r--   19 sdejongh 14 Oct  9:12 newfile.txt
drwxr-xr-x    - sdejongh 10 Oct 10:27 otherfiles
.rw-r--r--  121 sdejongh 10 Oct 10:29 README.md
.rw-r--r--   23 sdejongh 10 Oct 10:23 useless.txt
sdejongh@debian-base:~/archives$
```

To compress a single file we can simply call the `gzip` command and pass the file name:

```
sdejongh@debian-base:~/archives$ gzip lorem.txt
```

The original file is replaced with a new file with the extension *.gz*, while keeping the same ownership modes, access and modification times.

```
sdejongh@debian-base:~/archives$ ls -al
.rw-r--r--  20k sdejongh 14 Oct  9:12 archive.tar
.rw-r--r--   13 sdejongh  3 Oct 11:17 hello.txt
.rw-r--r-- 1.1k sdejongh  3 Oct 11:11 lorem.txt.gz
.rw-r--r--   19 sdejongh 14 Oct  9:12 newfile.txt
drwxr-xr-x    - sdejongh 10 Oct 10:27 otherfiles
.rw-r--r--  121 sdejongh 10 Oct 10:29 README.md
.rw-r--r--   23 sdejongh 10 Oct 10:23 useless.txt
sdejongh@debian-base:~/archives$
```

To uncompress the file, we simply need to add the `-d` flag to the command.

```
sdejongh@debian-base:~/archives$ gzip -d lorem.txt.gz 
sdejongh@debian-base:~/archives$ ls -al
.rw-r--r--  20k sdejongh 14 Oct  9:12 archive.tar
.rw-r--r--   13 sdejongh  3 Oct 11:17 hello.txt
.rw-r--r-- 2.4k sdejongh  3 Oct 11:11 lorem.txt
.rw-r--r--   19 sdejongh 14 Oct  9:12 newfile.txt
drwxr-xr-x    - sdejongh 10 Oct 10:27 otherfiles
.rw-r--r--  121 sdejongh 10 Oct 10:29 README.md
.rw-r--r--   23 sdejongh 10 Oct 10:23 useless.txt
sdejongh@debian-base:~/archives$
```

> Note: you can also uncompress file using `gunzip` without any flag.

In some case you need to uncompress a file to the standard output, this can be done uzing the `zcat` command.

```
sdejongh@debian-base:~/archives$ zcat lorem.txt.gz 
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus nunc nibh, ultricies quis venenatis sed, porttitor id nulla. In hac habitasse platea dictumst. Nullam feugiat nisl dolor, nec iaculis leo aliquam quis. Nulla facilisi. In lectus nisl, convallis ac orci ac, sodales sodales justo. Phasellus sed interdum massa. Etiam quis fringilla dui, sit amet ultricies enim.

Phasellus eu dapibus ante. Quisque ultrices eget neque id bibendum. Integer eleifend lorem vel rutrum consectetur. Quisque a massa tortor. Quisque ut feugiat sapien, in cursus enim. Integer luctus magna rhoncus pretium varius. Donec viverra sollicitudin leo, et malesuada ipsum efficitur eu. Sed convallis est ac nisl porta, id scelerisque diam lacinia. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Morbi in sapien sapien. Nulla ante nibh, auctor sed porta nec, consectetur sed ligula.

Morbi eget quam ut elit vehicula efficitur malesuada quis diam. Aliquam mollis lectus nulla, vel imperdiet massa scelerisque eu. Vestibulum laoreet tincidunt commodo. Proin congue est tellus. Suspendisse ac sapien sed odio mollis venenatis vel non elit. Ut ultricies nunc sed lacinia viverra. Sed suscipit ullamcorper nisl nec pharetra. In tempus lectus velit, ut fringilla ex fermentum a.

Morbi fringilla, erat quis faucibus bibendum, nisi mauris volutpat quam, non dignissim dolor ex eu mauris. Donec efficitur, lorem at posuere vehicula, magna ipsum aliquam neque, eget ornare nisi ipsum non dui. Ut non ipsum eu risus auctor tempus in ac sapien. Phasellus porttitor volutpat ipsum. Nam a neque venenatis lacus eleifend cursus. Nulla commodo posuere justo nec tincidunt. Donec pellentesque, dui at ultricies placerat, ex dolor interdum velit, quis tincidunt sem dolor ut massa. Aliquam erat volutpat. Sed et vestibulum nulla, id tincidunt nulla. Fusce elit nulla, consequat non varius nec, ultricies nec erat. Sed bibendum eros accumsan, fringilla lacus ut, sodales erat.

Nulla hendrerit eros et finibus accumsan. Curabitur porta, tellus ac imperdiet lobortis, justo ipsum viverra metus, eget ultricies enim arcu vel turpis. Maecenas congue sit amet lacus nec scelerisque. Aliquam vitae placerat eros. Maecenas quis neque ligula. Nam fermentum a justo sit amet fringilla. Donec accumsan massa id mollis placerat. Donec in neque massa. Ut consectetur diam sed vestibulum pellentesque. Nulla facilisi.
sdejongh@debian-base:~/archives$
```

This is helpful if you need to pass the content of a gzip file to another command.

> Note: you can also get the content of a gzip file to the standard output using `gzip -c` or `gunzip -c`

It's important to understand that `gzip` is made to compress a single file, it doesn't pack multiple files into one simple archive (that's what `tar` is used for).

You can use *wildcards* with `gzip` but it wil compress files separately:

```
sdejongh@debian-base:~/archives$ gzip *
gzip: otherfiles is a directory -- ignored
sdejongh@debian-base:~/archives$ ls
archive.tar.gz  hello.txt.gz  lorem.txt.gz  newfile.txt.gz  otherfiles  README.md.gz  useless.txt.gz
sdejongh@debian-base:~/archives$
```

The same principe applies for `gunzip` and `zcat` .

```
sdejongh@debian-base:~/archives$ gunzip *
gzip: otherfiles is a directory -- ignored
sdejongh@debian-base:~/archives$ ls
archive.tar  hello.txt  lorem.txt  newfile.txt  otherfiles  README.md  useless.txt
sdejongh@debian-base:~/archives$
```

You can still works recursively if you need to (un)compress files include in subfolders using the `-r` flag

```
sdejongh@debian-base:~/archives$ gzip -r *
sdejongh@debian-base:~/archives$
sdejongh@debian-base:~/archives$ ls -R
archive.tar.gz  hello.txt.gz  lorem.txt.gz  newfile.txt.gz  otherfiles  README.md.gz  useless.txt.gz

./otherfiles:
alphabet.txt.gz  alphanum.txt.gz  neofetch.txt.gz
sdejongh@debian-base:~/archives$
```

And by the way, `gunzip` and `zcat` work the same way...

```
sdejongh@debian-base:~/archives$ gunzip -r *
sdejongh@debian-base:~/archives$ 
sdejongh@debian-base:~/archives$ ls -R
archive.tar  hello.txt  lorem.txt  newfile.txt  otherfiles  README.md  useless.txt

./otherfiles:
alphabet.txt  alphanum.txt  neofetch.txt
sdejongh@debian-base:~/archives$
```

### BZIP2

`bzip2` is another compression tool using different compression algorithm, generaly more efficient than `gzip` . The principe is about the same as `gzip`, it (un)compress each file individually and use by default the `bz2` extension.

Compressing a file:

```
sdejongh@debian-base:~/archives$ bzip2 lorem.txt
sdejongh@debian-base:~/archives$ ls -al
.rw-r--r--  20k sdejongh 14 Oct  9:12 archive.tar
.rw-r--r--   13 sdejongh  3 Oct 11:17 hello.txt
.rw-r--r-- 1.0k sdejongh  3 Oct 11:11 lorem.txt.bz2
.rw-r--r--   19 sdejongh 14 Oct  9:12 newfile.txt
drwxr-xr-x    - sdejongh 14 Oct 12:05 otherfiles
.rw-r--r--  121 sdejongh 10 Oct 10:29 README.md
.rw-r--r--   23 sdejongh 10 Oct 10:23 useless.txt
sdejongh@debian-base:~/archives$
```

Uncompressing a file:

```
sdejongh@debian-base:~/archives$ bzip2 -d lorem.txt.bz2 
sdejongh@debian-base:~/archives$ ls -al
.rw-r--r--  20k sdejongh 14 Oct  9:12 archive.tar
.rw-r--r--   13 sdejongh  3 Oct 11:17 hello.txt
.rw-r--r-- 2.4k sdejongh  3 Oct 11:11 lorem.txt
.rw-r--r--   19 sdejongh 14 Oct  9:12 newfile.txt
drwxr-xr-x    - sdejongh 14 Oct 12:05 otherfiles
.rw-r--r--  121 sdejongh 10 Oct 10:29 README.md
.rw-r--r--   23 sdejongh 10 Oct 10:23 useless.txt
sdejongh@debian-base:~/archives$
```

To work recursively you can also use the `-r` flag.

`bzip2` comes with `bunzip2` to uncompress and `bzcat` to uncompress thefile to the standard output.

## Archiving and compressing files

### TAR+GZIP or TAR+BZIP2

If you need to package multiple files and compress the archive, you obviously use `tar` and either `gzip` or `bzip2`.

```
sdejongh@debian-base:~/archives$ tar -cvf archive.tar *
hello.txt
lorem.txt
newfile.txt
otherfiles/
otherfiles/alphabet.txt
otherfiles/alphanum.txt
otherfiles/neofetch.txt
README.md
useless.txt
sdejongh@debian-base:~/archives$ gzip archive.tar 
sdejongh@debian-base:~/archives$ ls
archive.tar.gz  hello.txt  lorem.txt  newfile.txt  otherfiles  README.md  useless.txt
sdejongh@debian-base:~/archives$
```

This works perfectly but `tar` allows you to do it in a single command using the `-z` flag to use gzip compression or the `-j` flag for bzip2 compression.

So we could achieve the same result as before in a single command:

```
sdejongh@debian-base:~/archives$ tar -cvzf archive.tar.gz *
hello.txt
lorem.txt
newfile.txt
otherfiles/
otherfiles/alphabet.txt
otherfiles/alphanum.txt
otherfiles/neofetch.txt
README.md
useless.txt
sdejongh@debian-base:~/archives$ ls -al
.rw-r--r-- 2.7k sdejongh 14 Oct 12:25 archive.tar.gz
.rw-r--r--   13 sdejongh  3 Oct 11:17 hello.txt
.rw-r--r-- 2.4k sdejongh  3 Oct 11:11 lorem.txt
.rw-r--r--   19 sdejongh 14 Oct  9:12 newfile.txt
drwxr-xr-x    - sdejongh 14 Oct 12:05 otherfiles
.rw-r--r--  121 sdejongh 10 Oct 10:29 README.md
.rw-r--r--   23 sdejongh 10 Oct 10:23 useless.txt
sdejongh@debian-base:~/archives$
```

And obviously you can extrct from a compressed achive using the same flags.

```
sdejongh@debian-base:~/archives$ tar -xvzf archive.tar.gz 
hello.txt
lorem.txt
newfile.txt
otherfiles/
otherfiles/alphabet.txt
otherfiles/alphanum.txt
otherfiles/neofetch.txt
README.md
useless.txt
sdejongh@debian-base:~/archives$
```

### ZIP

Less used in linux/unix world, `zip` is another compression tool mostly found on MS-DOS/Windows systems. It's generally not included in standard Linux distribution but can be installed from repositories.

However you'll often (but not always) find the `unzip` tool already installed on your system.

```
sdejongh@debian-base:~/archives$ zip --help
Copyright (c) 1990-2008 Info-ZIP - Type 'zip "-L"' for software license.
Zip 3.0 (July 5th 2008). Usage:
zip [-options] [-b path] [-t mmddyyyy] [-n suffixes] [zipfile list] [-xi list]
  The default action is to add or replace zipfile entries from list, which
  can include the special name - to compress standard input.
  If zipfile and list are omitted, zip compresses stdin to stdout.
  -f   freshen: only changed files  -u   update: only changed or new files
  -d   delete entries in zipfile    -m   move into zipfile (delete OS files)
  -r   recurse into directories     -j   junk (don't record) directory names
  -0   store only                   -l   convert LF to CR LF (-ll CR LF to LF)
  -1   compress faster              -9   compress better
  -q   quiet operation              -v   verbose operation/print version info
  -c   add one-line comments        -z   add zipfile comment
  -@   read names from stdin        -o   make zipfile as old as latest entry
  -x   exclude the following names  -i   include only the following names
  -F   fix zipfile (-FF try harder) -D   do not add directory entries
  -A   adjust self-extracting exe   -J   junk zipfile prefix (unzipsfx)
  -T   test zipfile integrity       -X   eXclude eXtra file attributes
  -y   store symbolic links as the link instead of the referenced file
  -e   encrypt                      -n   don't compress these suffixes
  -h2  show more help
  
sdejongh@debian-base:~/archives$
```

As you can seen, there are some features related to archive management.

As it's not often used on linux system, this document won't cover `zip` or `unzip`usage. 

If needed you can find sample usages of the `zip` and `unzip`commandes here: [All zip and unzip File Operations on Linux](https://linuxhint.com/all-zip-and-unzip-file-operations-on-linux/)
