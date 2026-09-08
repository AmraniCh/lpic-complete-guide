---
description: "LPIC-1 exam 101-500 cheatsheet: a condensed command reference for topics 101 to 104, for fast last-minute review before the exam."
---

# Exam 101-500 cheatsheet

A condensed command reference for exam **101-500** (topics 101 to 104), the notes I made for myself right before the exam. It is deliberately terse: commands, flags, and gotchas, no long explanations. For the full write-ups, see the [Exam 101-500](../exam-101/index.md) pages.

---

## 101.1 - Determine and Configure Hardware Settings

```bash
# FIRMWARE
# BIOS: old, boots from MBR (first sector of disk)
# UEFI: modern, boots from EFI System Partition (ESP), FAT32, at /boot/efi
# check if UEFI: ls /sys/firmware/efi (exists = UEFI, missing = BIOS)

# DEVICE TYPES
# PCI: internal cards (network, video, audio, disk controllers)
# USB: external serial devices (keyboard, mouse, storage)
# hda = IDE disk (old), sda = SATA/SCSI/USB disk, nvme0n1 = NVMe SSD

# PSEUDO-FILESYSTEMS (in RAM, not on disk)
# /sys   hardware and kernel info (sysfs)
# /proc  process and kernel runtime info
# /dev   device files, managed by udev

# /proc KEY FILES
cat /proc/cpuinfo              # CPU details
cat /proc/interrupts           # IRQ assignments
cat /proc/ioports              # I/O port assignments
cat /proc/dma                  # DMA channels
# /proc changes are lost on reboot, edit /etc/ configs for permanent changes

# HARDWARE LISTING
lspci                          # list PCI devices
lspci -k                       # show kernel driver/module handling each PCI device
lspci -v                       # verbose information
lspci -s 00:1f.3               # show a specific PCI device

lsusb                          # list USB devices
lsusb -d 8087:0024             # show devices by vendor:product ID
lsusb -s 001:003               # show a specific USB device by bus:device number

lsblk                          # list block devices (disks, partitions)

# KERNEL MODULES (.ko files, like drivers)
lsmod                          # list loaded modules
modprobe iwlwifi               # load a module (handles dependencies)
modprobe -r iwlwifi            # unload a module
# modprobe > insmod (insmod needs full path, no dependency handling)
# persistent loading: add module name to /etc/modules or config in /etc/modprobe.d/
# block a module: add "blacklist modulename" to /etc/modprobe.d/blacklist.conf

# udev (manages /dev, assigns device files dynamically)
# rules in /etc/udev/rules.d/
# char device (c) = byte by byte (keyboard, terminal)
# block device (b) = data in chunks (disk, USB)
```

---

## 101.2 - Boot the System

```bash
# BOOT SEQUENCE
# 1. POST (Power-On Self-Test)
# 2. Firmware (BIOS/UEFI) loads bootloader
# 3. Bootloader (GRUB) loads kernel + initramfs
# 4. Kernel mounts root filesystem, runs init (PID 1)
# 5. Init (systemd/SysV) starts services

# BOOT LOGS
dmesg                          # kernel ring buffer messages (includes boot)
dmesg --clear                  # clear the ring buffer
journalctl -k                  # kernel messages (same as dmesg but from journal)
journalctl -b                  # current boot messages
journalctl -b -1               # previous boot messages
journalctl --list-boots        # list all stored boots
# /var/log/dmesg or /var/log/boot.log also store boot messages

# INIT SYSTEMS
# SysVinit: old, scripts in /etc/init.d/, sequential startup
# Upstart: Ubuntu's old init (awareness only), replaced by systemd
# systemd: modern, parallel startup, uses units

# PID 1
readlink -f /sbin/init         # shows actual init binary (e.g. /usr/lib/systemd/systemd)
ps -p 1                        # shows init process
pstree                         # shows process hierarchy

# SYSTEMD UNITS (12 types: service, target, mount, socket, timer, ...)
systemctl list-units                    # list active units
systemctl list-units --type=target      # list targets only
systemctl get-default                   # show default target
systemctl start sshd                    # start a service
systemctl stop sshd                     # stop a service
systemctl restart sshd                  # restart
systemctl reload sshd                   # re-read service config
systemctl enable sshd                   # start on boot
systemctl disable sshd                  # do not start on boot
systemctl status sshd                   # show service status
systemctl is-active sshd                # quick check: active or not
systemctl is-system-running
systemctl --failed                      # list failed units

# UNIT FILE LOCATIONS (sorted by priority, first wins)
# 1. /etc/systemd/system/
# 2. /run/systemd/system/
# 3. /usr/lib/systemd/system/

# JOURNALCTL
journalctl                     # all journal entries
journalctl -u sshd             # -u (unit): entries for one service
journalctl -n 20               # last 20 lines
journalctl -f                  # -f (follow): live tail
journalctl -xe                 # last few logs with extra context
```

---

## 101.3 - Runlevels / Boot Targets & Shutdown

```bash
# SYSV RUNLEVELS (old system)
# 0 = shutdown, 1 = single-user (recovery), 2-4 = multi-user, 5 = multi-user + GUI, 6 = reboot
# default runlevel set in /etc/inittab: id:5:initdefault:
# /etc/inittab format: id:runlevels:action:process
runlevel                       # show current and previous runlevel
telinit 3                      # switch to runlevel 3
init 0                         # shutdown (same as runlevel 0)
# scripts in /etc/init.d/, links in /etc/rc[0-6].d/ (S=start, K=kill)

# SYSTEMD TARGETS (replace runlevels)
systemctl get-default                       # show default target
systemctl set-default multi-user.target     # set default target
systemctl isolate rescue.target             # switch to rescue mode now
systemctl isolate emergency.target          # switch to emergency mode now
# rescue = local fs mounted, no network, root only
# emergency = root fs read-only, no network, root only

# SHUTDOWN
shutdown -h now                # halt now
shutdown -r now                # reboot now
shutdown -r 60 "Rebooting!"   # reboot in 60 min, broadcast message
shutdown -c                    # cancel a scheduled shutdown
halt                           # halt the system
poweroff                       # halt + power off (ACPI signal)
reboot                         # reboot
# shutdown sends SIGTERM first, then SIGKILL after delay

# NOTIFYING USERS
wall "Server going down!"     # broadcast to all logged-in users
# /etc/issue     = text shown before login (tty)
# /etc/issue.net = text shown before remote login
# /etc/motd      = message shown after login

# ACPI (Advanced Configuration and Power Interface)
# lets OS send power signals (shutdown, sleep, wake) to hardware
```

---

## 102.1 - Design Hard Disk Layout

```bash
# PARTITIONING schemes
# MBR: max 2TB, 4 primary, extended+logical workaround (logical starts at 5)
# GPT: 128 partitions, no size limit, used with UEFI

# /dev/sda1 = 1st partition on 1st disk, /dev/sdb5 = 1st logical on 2nd disk

# WHY SEPARATE PARTITIONS
# / (root) = always needed, always local
# /boot    = kernel + bootloader, must be local, accessible by BIOS/UEFI
# /home    = user data, can be on network (NFS) for workstations
# /var     = logs, mail, spool, separate to prevent filling root
# swap     = overflow when RAM is full

# SWAP SIZING
# no strict rule. common: "RAM + 2GB" or "RAM x 2, max 8GB"

# LVM (Logical Volume Manager)
# PV (Physical Volume) -> VG (Volume Group) -> LV (Logical Volume)
# lets you resize, span disks, add space without reformatting

# EFI SYSTEM PARTITION (ESP)
# FAT32, mounted at /boot/efi, holds .efi bootloader files
# needed for UEFI boot
```

---

## 102.2 - Install a Boot Manager

```bash
# GRUB LEGACY (v1)
# config: /boot/grub/menu.lst or /boot/grub/grub.conf (Red Hat symlink)
# format: title, root (hd0,0), kernel, initrd
# install: grub-install /dev/sda
# interactive: press e to edit, c for command line, b to boot

# GRUB2
# config: /boot/grub/grub.cfg or /boot/grub2/grub.cfg
# DO NOT edit grub.cfg directly, it is auto-generated
# edit /etc/default/grub and scripts in /etc/grub.d/
grub-mkconfig -o /boot/grub/grub.cfg     # regenerate config
grub2-mkconfig -o /boot/grub2/grub.cfg   # Red Hat variant
update-grub                               # Debian shortcut for grub-mkconfig
grub-install /dev/sda                     # install GRUB to disk MBR/ESP

# GRUB2 partition naming
# (hd0,1) or (hd0,msdos1) = first partition on first disk (MBR)
# (hd0,gpt1) = first partition on first disk (GPT)

# KERNEL BOOT PARAMETERS (passed via linux line in grub.cfg)
# root=/dev/sda1    root filesystem
# ro / rw           read-only or read-write
# quiet             suppress boot messages
# single / 1 / S    boot in single-user mode (SysV recovery)
# systemd.unit=rescue.target    boot in rescue (systemd)
# init=/bin/bash    skip init, drop to shell (emergency recovery)
```

---

## 102.3 - Manage Shared Libraries

```bash
# LINKING
# static: library compiled into the program (big binary, no dependencies)
# dynamic/shared: library loaded at runtime (.so files, like .dll on Windows)
# lib files: /lib/, /lib64/, /usr/lib/, /usr/lib64/
# naming: libNAME.so.VERSION (e.g. libudev.so.1.4.0)

ldd /bin/ls                    # show shared libraries needed by a program
ldd /sbin/ldconfig             # "not a dynamic executable" = statically linked

# LIBRARY CONFIG
# /etc/ld.so.conf          main config (usually includes /etc/ld.so.conf.d/*.conf)
# /etc/ld.so.cache         binary cache for fast lookups
ldconfig                       # rebuild the cache after changing ld.so.conf
ldconfig -p                    # -p (print): show cached libraries

# LD_LIBRARY_PATH (override library search path)
export LD_LIBRARY_PATH=/usr/lib/myoldlibs:/home/jadi/libs/
# searched BEFORE system libraries, useful for testing or old software

# SEARCH ORDER
# 1. LD_LIBRARY_PATH
# 2. program's own path
# 3. /etc/ld.so.conf (and ld.so.cache)
# 4. /lib/, /lib64/, /usr/lib/, /usr/lib64/
```

---

## 102.4 - Use Debian Package Management

```bash
# TWO LAYERS
# dpkg       low-level, works on .deb files, no dependency resolution
# apt/apt-get  high-level, works with repos, resolves dependencies

# SOURCES
# /etc/apt/sources.list         repo list

# apt-get
apt-get update                 # refresh repo index (does NOT install anything)
apt-get upgrade                # upgrade all installed packages
apt-get install nginx          # install a package
apt-get remove nginx           # remove package (keep config)
apt-get purge nginx            # remove package + config files

# apt-cache
apt-cache search nginx         # search repos by name/description
apt-cache show nginx           # show package details
apt-cache depends nginx        # show dependencies

# dpkg
dpkg -i package.deb            # -i (install): install a .deb file
dpkg -r nginx                  # -r (remove): remove, keep config
dpkg -P nginx                  # -P (purge): remove + config
dpkg -l                        # -l (list): list all installed packages
dpkg -L nginx                  # -L (list-files): files installed by package
dpkg -S /usr/bin/unzip         # -S (search): which package owns this file
dpkg -s nginx                  # -s (status): show package status/info
dpkg --configure -a            # finish interrupted installs
dpkg-reconfigure tzdata        # reconfigure an installed package
```

---

## 102.5 - Use RPM and YUM Package Management

```bash
# TWO LAYERS
# rpm        low-level, works on .rpm files, no dependency resolution
# yum/dnf    high-level, works with repos, resolves dependencies

# SOURCES
# /etc/yum.conf            main config
# /etc/yum.repos.d/        one .repo file per repository

# yum (or dnf on Fedora)
yum install nginx              # install
yum remove nginx               # remove
yum update                     # update all packages
yum search nginx               # search repos
yum info nginx                 # show package details
yum provides /etc/hosts        # which package provides this file
yum list installed             # list installed packages

# rpm
rpm -Uvh package.rpm           # -U (upgrade): install or upgrade, -v verbose, -h hash progress
rpm -e nginx                   # -e (erase): remove package
rpm -qa                        # -q (query) -a (all): list all installed
rpm -qi nginx                  # -q -i (info): show package info
rpm -ql nginx                  # -q -l (list): files installed by package
rpm -qf /usr/bin/unzip         # -q -f (file): which package owns this file
rpm -qip package.rpm           # -p: query an uninstalled .rpm file
rpm -V nginx                   # -V (verify): check if files were modified
rpm -K package.rpm             # -K (checksig): verify .rpm file signature

# rpm2cpio (extract files from .rpm without installing)
rpm2cpio package.rpm | cpio -idv

# zypper (SUSE)
zypper install nginx           # or: zypper in nginx
zypper remove nginx            # or: zypper rm nginx
zypper search nginx            # or: zypper se nginx
zypper update                  # update packages
```

---

## 102.6 - Linux as a Virtualization Guest

```bash
# CONCEPTS (awareness only, no commands)
# Virtual machine: full OS running on a hypervisor (KVM, VirtualBox, VMware)
# Container: isolated process sharing the host kernel (Docker, LXC)
# IaaS: cloud instances with compute, block storage, networking (AWS, Azure)

# CLONING A VM (things to change on the clone)
# hostname
# machine-id (/etc/machine-id, /var/lib/dbus/machine-id)
# SSH host keys (/etc/ssh/ssh_host_*)
# MAC addresses (network interface)
# IP addresses and network config
# disk UUIDs if copied

# CLOUD-INIT (awareness)
# auto-configures a VM on first boot (hostname, SSH keys, users, network)
# config from cloud provider metadata or user-data

# GUEST DRIVERS / TOOLS
# VirtualBox: guest additions (better display, shared folders, clipboard)
# VMware: open-vm-tools
# D-Bus machine id: unique identifier per system, must differ between clones
```

---

## 103.1 - Work on the command line

```bash
# SHELL BASICS
bash                           # the default shell on most distros
echo $SHELL                    # show current shell
echo $$                        # show current shell PID
pwd                            # print current working directory
exit                           # exit the shell (same as Ctrl+d on empty line)

# ENVIRONMENT VARIABLES
env                            # show exported (environment) variables only
set                            # show ALL variables (exported + local + functions)
export MYVAR="hello"           # create and export a variable (visible to child processes)
unset MYVAR                    # remove a variable
LOCALVAR="test"                # local variable, NOT exported, invisible to child processes
# env shows less than set. set includes local vars that env hides

# $PATH (where the shell looks for commands)
echo $PATH                     # colon-separated list of directories
# shell searches each directory left to right for the command you type
export PATH=$PATH:/opt/myapp   # add a directory to PATH

# QUOTING
# double quotes "..." = variables expand, spaces preserved
# single quotes '...' = everything is literal, no expansion
# backticks `cmd` or $(cmd) = command substitution, runs cmd and inserts output
echo "Home is $HOME"           # $HOME expands
echo 'Home is $HOME'           # prints literal $HOME
echo "Today is $(date)"        # runs date, inserts result

# COMMAND TYPES
type ls                        # shows if alias, builtin, file, function, or keyword
which ls                       # shows full path of external command
# type knows aliases and builtins, which only finds files in PATH

# MAN PAGES
man ls                         # open manual page
man -k keyword                 # search man pages by keyword (same as apropos)
# inside man: / to search, n next match, N previous, q quit

# HISTORY
history                        # show command history list
history -c                     # -c (clear): clear history in memory
!!                             # repeat last command (bash feature, not in dash)
!n                             # repeat command number n
# history stored in ~/.bash_history
# HISTSIZE = how many commands kept in memory
# HISTFILESIZE = how many lines kept in ~/.bash_history

uname                          # -s (kernel name), -n hostname, -r kernel release, -v kernel version, -m machine cpu arch, -o os name, -a all info
```

---

## 103.2 - Process text streams using filters

```bash
od -c textfile
od -a textfile

split -l 2 -d mybigfile my_prefix # l=number (lines)
split -n 2 -d mybigfile my_prefix # n=number (chunks)

cut -d, -f 1 data.txt # -d delimiter, -f field number

sort mytest # -n numerical, -r reverse

sort data.txt | uniq -c # -c count of each item, -u show only non repeated, -d show only repeated (-u is opposite of -d)

paste file1 file2 # side by side

echo "chakir" | tr c s
echo "sss ccdd fdfds sss aaa" | tr -s 'sss' # -s squeeze

sed 's/a/@/' data.txt # 's' replaced by 'a'
sed /a/d data.txt # remove lines that contains 'a'
sed -n /a/p data.txt # -n tells sed to print nothing, 'p' prints only what matched, lines that contains 'a'
sed -e 's/apple/APPLE/' -e 's/cherry/CHERRY/' fruit.txt

wc mydata
  # 9  25 121 mydata
  # lines words characters mydata

sha256sum data.txt > hash1
sha256sum -c hash1
```

---

## 103.3 - File Management

```bash
cp -i myfile1 myfile2 # -i interactive (do you want to overwrite ...), -p preserve attributes
mv -i myfile1 myfile2 # -i interactive (do you want to overwrite ...)
rm myfile

touch file2
touch -d 11am file2 # -d date
touch -t 200908121510.59 file2 # -t timestamp
touch -r file1 file2 # -r reference
touch -am file3 # -a access time, -m modification time

dd if=/dev/sda of=backup.dd bs=4096 # if (input file), of (output file), bs (block size)

find ~ -iname "hel*" # -iname: name case insensitive
find ~ -iname "hel*" -type f # -type f: type file
find ~/test -size +10M # file more than 10 megabytes
find ~ -mmin -30 -ls # show last modified files in ~ 30 min ago

gzip file.txt # bzip2, xz
gunzip file.txt.gz # bunzip2, unxz

tar -czf archive.tar.gz hash1 hash2
tar -xf archive.tar
tar -xf archive.tar -C /tmp

ls | cpio -o > files.cpio
mkdir extract
mv myarchivefind.cpio extract
cd extract
cpio -id < files.cpio
```

---

## 103.4 - Streams, Pipes & Redirects

```bash
# tr ' ' '@' <<END # here-documents
# cat <<END > file1

echo files.txt | xargs cat
cat files.txt | xargs -I FILE touch _FILE.txt

ls | tee files.txt # tee add the output to the file but also redirect it to stdout (ls > files.txt don't output in stdout)
```

---

## 103.5 - Process Management

```bash
xeyes # ctrl + z
xclock # ctrl + z
jobs -l # -l: process id
fg %1
bg %2

kill -9 2387 # -9: kill, -1 hup, -15 term (normal termination)
killall python # kill all python 'command' processes (default -15 normal termination)
pkill slee # match pattern

ps -ef # (UNIX style) -e all processes, -f full format
ps aux # (BSD style)
ps -u admin # --user

pgrep sleep | xargs kill

top # q (quit), M (sort by memory usage), k (kill after asking PID)

free # -m (mega), -h (human), -g (giga)

uptime
# 21:18:52 up  1:34,  5 users,  load average: 2.38, 2.64, 2.41

watch free
watch 'df -h | grep nvme0n1p1'
watch -n .5 free -b # -n (interval)
```

---

## 103.5 - Terminal Multiplexers

```bash
screen
screen -d # detach, or CTRL + a D
screen -ls
screen -r 8475 # reattach
# kill with CTRL + a K

tmux
# CTRL + B % => open new vertical
# CTRL + B " => open new horizontally
# CTRL + B D => detach
# CTRL + B & => kill
# CTRL + B -> <- => navigation
tmux ls
tmux att -t 1 # attach to session 1 (-t means target)
```

---

## 103.6 - Process Priorities

```bash
nice ls # get default 10
nice -n 15 ls # 15 niceness
sudo nice -n -20 # nice < 0 use sudo
renice -n 2 497914 # IMPORTANT you need sudo if the new NICE < OLD_NICE
```

---

## 103.7 - Regular Expressions

### Anchors
- `^` start of line (outside brackets)
- `$` end of line

### Negation
- `[^abc]` NOT a, b, or c (`^` right after `[` means NOT)

### Any Character
- `.` any single character

### Quantifiers
- `*` 0 or more
- `+` 1 or more
- `?` 0 or 1
- `{4}` exactly 4 times
- `{2,}` 2 or more times
- `{2,4}` between 2 and 4 times

### Brackets
- `[abc]` match a, b, or c
- `[a-z]` range
- `[^abc]` NOT a, b, or c

### Branches & Groups
- `|` OR
- `()` grouping

### Escape
- `\` remove special meaning (e.g. `\.` matches a literal dot)

### Basic vs Extended (the exam trap)
- **basic** (grep, sed): `+ ? { } ( ) |` are literal. Escape to activate: `\+ \? \{ \}`
- **extended** (grep -E, egrep, sed -E): `+ ? { } ( ) |` are special. Escape to make literal
- `grep` = basic, `egrep` = extended, `fgrep` = no regex at all
- `fgrep` = fixed grep (no regex, treats everything as literal text). Same as `grep -F`
- example: `fgrep '3.0' file.txt` (searches for literal "3.0", the dot is not "any character")

```bash
grep 'hel*' /usr/share/dict/words # lines matching "he" + zero or more "l"
grep -c 'hel*' /usr/share/dict/words # count of matching lines
grep -rl 192.168. /etc/cloud # filenames containing "192.168." recursively
# -v: print lines that do NOT match

sed -r "s/(Z|R|J)/starts with ZRJ/" friends.txt # -r to tell sed that we use regex
```

---

## 103.8 - Vim

### Modes
- **normal** - default mode. navigate, delete, copy, paste. Esc to return here
- **insert** - type text into the file. enter with i, a, o
- **command** - type commands at bottom. enter with `:` from normal mode

### Entering Insert Mode (from normal)
- `i` insert before cursor
- `a` insert after cursor
- `o` open new line below and insert
- `O` open new line above and insert
- `Esc` back to normal mode

### Navigation (normal mode)
- `h` left
- `j` down
- `k` up
- `l` right

### Editing (normal mode)
- `dd` delete (cut) whole line
- `yy` copy (yank) whole line
- `p` paste below cursor
- `d` delete (combine with movement, e.g. dw = delete word)
- `y` yank (combine with movement, e.g. yw = yank word)
- `x` delete character under cursor (like Del key)
- `X` delete character before cursor (like Backspace)

### Search (normal mode)
- `/pattern` search forward
- `?pattern` search backward
- `n` next match
- `N` previous match

### Command Mode (after `:`)
- `:w` save
- `:q` quit
- `:wq` save and quit
- `:q!` quit without saving
- `:w!` force save (if possible)
- `ZZ` save and quit (shortcut, no colon needed, normal mode)
- `:w /tmp/test.txt`

### Undo / Redo (normal mode)
- `u` undo last change (repeat for more)
- `Ctrl+r` redo (reverse the undo)

> **EXAM:** know i/o/a for insert, dd/yy/p for edit, /? for search, :wq :q! for save/quit

---

## 104.1 - Partitions & Filesystems

```bash
fdisk -l /dev/sdb # list disk partitions
```

### Two Partition Schemes
- **MBR**: max 2TB, max 4 primary, extended+logical workaround, BIOS boot
- **GPT**: no size limit, 128 partitions, no primary/extended, UEFI boot

### Three Partition Tools
- `fdisk` - MBR disks. interactive. writes on "w" only
- `gdisk` - GPT disks. same interface as fdisk. writes on "w" only
- `parted` - both MBR and GPT. **WARNING: writes IMMEDIATELY, no "w" step**

### fdisk Commands (same for gdisk)
- `p` print table
- `n` new partition
- `d` delete partition
- `t` change partition type (83=Linux, 82=Swap)
- `a` toggle boot flag (MBR only)
- `l` list type codes
- `w` write and quit
- `q` quit without saving

### Check Disk Type

```bash
fdisk -l /dev/sda  # look for "Disklabel type: dos" (MBR) or "gpt"
```

### Creating Filesystems (after partitioning)

```bash
mkfs.ext2 /dev/sdX1   # Linux - no journal. fast but risky
mkfs.ext3 /dev/sdX1   # Linux - ext2 + journal
mkfs.ext4 /dev/sdX1   # Linux - default everywhere
mkfs.xfs  /dev/sdX1   # Linux - fast with large files - WARNING: cannot shrink
mkfs.vfat /dev/sdX1   # Windows/Linux/Mac - 4 GB file limit
mkfs.exfat /dev/sdX1  # Windows/Linux/Mac - no 4 GB limit
mkfs.btrfs /dev/sdX1  # Linux - snapshots, compression, subvolumes

mkfs -t ext4 /dev/sdX1 # -t (type)
```

### Btrfs (awareness only)
Features: snapshots, compression, multi-device, subvolumes

### Swap (partition method)

```bash
mkswap /dev/sdX2 # format partition as swap
```

---

## 104.2 - Filesystem Integrity

```bash
# df (shows free space per mounted filesystem)
df -h                        # -h (human): readable sizes
df -i                        # -i (inodes): show inode usage instead of space
df -hT                       # -T (type): add filesystem type column

# du (shows space used by files/dirs)
du -h -s                     # -s (summary): total only
du -h --max-depth 2          # show 2 levels deep
```

> **NEVER run fsck on a mounted filesystem**

```bash
fsck /dev/sdb1               # assumes ext if no type given
fsck -t vfat /dev/sdc        # -t (type): specify filesystem type
fsck -A                      # -A (all): check all in /etc/fstab
fsck -N /dev/sdb1            # -N (no-act): dry run, no changes
fsck -p /dev/sdb1            # -p (preen): auto-fix safe errors, stop on serious
```

### How fsck Works

```
                      fsck /dev/sdX
                           │
                 detects filesystem type
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
     ext2/3/4            vfat             xfs
         │                 │                 │
     e2fsck           fsck.vfat         NO fsck.xfs
         │                 │                 │
     repairs            repairs        use xfs_repair
                                       directly instead
```

```bash
# e2fsck (fsck for ext2/ext3/ext4 only)
e2fsck /dev/sdb1             # interactive, asks y/n per error

# mke2fs (create ext2/ext3/ext4 filesystem, same as mkfs.extN)
mke2fs /dev/sdb1             # creates ext2 by default
mke2fs -t ext4 /dev/sdb1     # -t (type): specify ext type

# tune2fs (view/modify ext2/ext3/ext4 parameters)
tune2fs -l /dev/sda1         # -l (list): show current parameters

# XFS TOOLS (all from xfsprogs package)
xfs_repair /dev/sda1         # repair XFS filesystem
xfs_repair -n /dev/sda1      # -n (no): check only, no changes
xfs_fsr                      # defragment all mounted XFS
xfs_db /dev/sda1             # inspect XFS parameters
```

---

## 104.3 - Mounting & Unmounting

```bash
# mount (attach a filesystem to a directory)
mount /dev/sdb1 /mnt/data                # mount device to mount point
mount -t ext4 /dev/sdb1 /mnt/data        # -t (type): specify filesystem type
mount -o ro /dev/sdb1 /mnt/data          # -o (options): ro = read only
mount -o remount,ro /dev/sdb1            # remount with new options, no unmount needed
mount -a                                 # -a (all): mount everything in /etc/fstab
mount UUID=6e2c... /mnt/data             # mount by UUID
mount LABEL=MyDisk /mnt/data             # mount by label

# umount (detach a filesystem)
umount /mnt/data                         # unmount by mount point
umount /dev/sdb1                         # unmount by device
umount -f /mnt/server                    # -f (force): force unmount
# "target is busy" = files still open. use lsof /dev/sdb1 to find them

# blkid (shows UUID, TYPE, LABEL per device)
blkid                                    # all devices
blkid /dev/sdb1                          # one device

# lsblk (shows devices, filesystems, mount points)
lsblk                                   # tree view of all disks and partitions
lsblk -f                                # -f (filesystem): adds FSTYPE, UUID, LABEL columns
```

### /etc/fstab (auto-mount on boot, 6 fields)

```
DEVICE        MOUNTPOINT  TYPE  OPTIONS    DUMP  PASS
/dev/sda1     /           ext4  defaults   0     1
UUID=6e2c...  /home       ext4  noatime    0     2
```

- **DUMP**: 0 = no backup, 1 = backup
- **PASS**: 0 = no fsck, 1 = fsck first (root), 2 = fsck after root
- `noauto` in OPTIONS = skip on `mount -a`

### Mount Directories
- `/media/` = where removable media (USB, CD) gets auto-mounted
- `/mnt/` = for temporary manual mounts

---

## 104.5 - Permissions & Ownership

### Reading Permissions: `ls -l`

```
-rwxr-xr-- 1 carol users 1024 Jan 18 file.txt
│└──┘└──┘└──┘
│  u    g    o
│ user group others
│
file type: - = file, d = dir, l = symlink, b = block, c = char
```

### Permission Values
- `r` = 4 read
- `w` = 2 write
- `x` = 1 execute
- `rwx` = 7, `rw-` = 6, `r-x` = 5, `r--` = 4

```bash
# chmod (change permissions)
# SYMBOLIC MODE
chmod u+x file.txt               # u (user): add execute
chmod g-w file.txt               # g (group): remove write
chmod o=r file.txt               # o (others): set to read only
chmod u+x,go-wx file.txt         # combine with commas

# OCTAL MODE
chmod 755 file.txt               # rwxr-xr-x
chmod 644 file.txt               # rw-r--r--
chmod 600 file.txt               # rw-------

# chown (change owner and/or group)
chown alice file.txt             # change owner to alice
chown alice:devs file.txt        # change owner and group
chown :devs file.txt             # change group only (same as chgrp)

# chgrp (change group only)
chgrp devs file.txt              # change group to devs
```

### umask (default permission mask for new files)

```bash
umask                            # show current mask
umask 027                        # set mask
# new files get:  666 - 027 = 640 (rw-r-----)
# new dirs  get:  777 - 027 = 750 (rwxr-x---)
# files never get execute from umask, only dirs do
```

### Special Permissions (4-digit octal: Xugp)
- **sticky bit** = 1 - on dirs: only owner can delete their own files
- **SGID** = 2 - on dirs: new files inherit group. on files: run as group
- **SUID** = 4 - on files: run as file owner (e.g. passwd runs as root)

```bash
chmod 1755 /tmp                  # sticky bit + rwxr-xr-x
chmod 2755 shared/               # SGID + rwxr-xr-x
chmod 4755 script.sh             # SUID + rwxr-xr-x

# SYMBOLIC MODE FOR SPECIAL PERMISSIONS
chmod o+t dir/                   # sticky bit
chmod g+s dir/                   # SGID
chmod u+s file                   # SUID
```

### Special Bits in `ls -l`
- `s` in user spot = **SUID** (runs as file owner, e.g. passwd runs as root)
- `s` in group spot = **SGID** (on dirs: new files inherit group)
- `t` in others spot = **sticky** (on dirs: only owner can delete their files, e.g. /tmp)

```
-rwsr-xr-x  SUID        chmod 4755 file   or   chmod u+s file
-rwxr-sr-x  SGID        chmod 2755 dir    or   chmod g+s dir
drwxr-xr-t  sticky      chmod 1755 dir    or   chmod o+t dir
```

> lowercase `s`/`t` = special bit + execute
> UPPERCASE `S`/`T` = special bit, NO execute

---

## 104.6 - Hard & Symbolic Links

```bash
# ln (create links)
ln target.txt hardlink             # hard link (default)
ln -s target.txt softlink          # -s (symbolic): soft link
ls -li                             # -i (inode): show inode numbers
```

| | Hard Link | Symbolic Link |
|---|---|---|
| Points to | inode (data) | filename (path) |
| Delete original | data survives | link breaks |
| Scope | files only | files and directories |
| Filesystem | same filesystem only | can cross filesystems |
| In `ls -l` | same inode, link count goes up | different inode, shows `l` and `->` |

### Exam Traps
- hard link across filesystems = error
- symlink with relative path + move = breaks. always use full path
- symlink shows `rwxrwxrwx` but real permissions = target's

---

## 104.7 - Find System Files & FHS

```bash
# find (search files by name, type, size, time, permissions)
find /home -name "*.txt"              # -name: match filename
find /home -iname "*.txt"             # -iname: case-insensitive match
find / -type f -size +100M            # -type f (file), -size +100M (over 100 MB)
find . -mtime -7                      # -mtime (modified): less than 7 days ago

# locate (fast search using a pre-built database)
locate report.pdf                     # search database for pattern
locate -i report.pdf                  # -i: case-insensitive
locate -c .jpg                        # -c (count): show number of matches

# updatedb (rebuild the locate database)
updatedb                              # scans filesystem, updates /var/lib/mlocate.db
# /etc/updatedb.conf controls what updatedb scans
# PRUNEFS=    filesystems to skip (e.g. ntfs nfs)
# PRUNEPATHS= directories to skip (e.g. /tmp /var/spool)

# which (shows full path of an executable)
which bash                            # /usr/bin/bash
which -a mkfs.ext3                    # -a (all): show all matches in PATH

# type (shows what a command name is)
type ls                               # alias, builtin, file, function, or keyword
type -a ls                            # -a (all): show all matches
type -t ls                            # -t (type): show only the type word

# whereis (shows binary, man page, source locations)
whereis bash                          # shows binary + man page paths
whereis -b bash                       # -b (binary): binaries only
whereis -m bash                       # -m (manual): man pages only
```

### FHS Key Directories

| Directory | Purpose |
|---|---|
| `/` | root, top of everything |
| `/bin` | essential user binaries |
| `/sbin` | essential system/admin binaries |
| `/boot` | kernel, initrd, bootloader files |
| `/dev` | device files (sda, tty, null) |
| `/etc` | config files |
| `/home` | user home directories |
| `/lib` | shared libraries for /bin and /sbin |
| `/media` | auto-mounted removable media (USB, CD) |
| `/mnt` | temporary manual mounts |
| `/opt` | optional/third-party software |
| `/proc` | virtual fs, kernel and process info |
| `/root` | root user's home directory |
| `/run` | runtime data, cleared on boot |