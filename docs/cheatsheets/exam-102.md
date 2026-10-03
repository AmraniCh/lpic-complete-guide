---
description: "LPIC-1 exam 102-500 cheatsheet: a condensed command reference for topics 105 to 110, for fast last-minute review before the exam."
---

# Exam 102-500 cheatsheet

A condensed command reference for exam **102-500** (topics 105 to 110), the notes I made for myself right before the exam. It is deliberately terse: commands, flags, and gotchas, no long explanations. For the full write-ups, see the [Exam 102-500](../exam-102/index.md) pages.

---

## 105.1 Customize and use the shell environment

```bash
set -b # -b: tell me at once when a background job ends
set -e # -e (errexit): stop the script at the first failing command

env -u LANG my_command # -u (unset): run my_command without the LANG variable
env -i bash            # -i (ignore): start bash with an empty environment
printenv               # show all environment variables
printenv USER          # show one variable

friend=naruto     # create a local variable
set | grep friend # show the variable
unset friend      # remove it

export friend=nagato # exported: child processes see it too

source config.sh # run config.sh in the current shell
. config.sh      # same as source

alias                         # list all aliases
alias testping="ping 8.8.8.8" # create an alias

funnyls () {
    ls -ltrh # -l (long) -t (time sort) -r (reverse) -h (human sizes)
    echo "This is a funny ls"
}
funnyls      # call the function
```

```bash
# LOGIN SHELL (login with user + pass: SSH, console, su -)
# 1. /etc/profile                      system-wide
# 2. /etc/profile.d/*.sh               run by a line in /etc/profile
# 3. ONE of these (first found wins, then stops):
#      ~/.bash_profile
#      ~/.bash_login
#      ~/.profile
# 4. ~/.bashrc                         only if step 3 sources it

# NON-LOGIN INTERACTIVE SHELL (terminal in GUI, or typing bash)
# 1. /etc/bash.bashrc                  (or /etc/bashrc on some distros)
# 2. ~/.bashrc

# NON-LOGIN NON-INTERACTIVE (bash script.sh)
# reads NO startup files, only $BASH_ENV if set

# LOGOUT
# ~/.bash_logout                       runs when login shell exits
```

## 105.2 Customize or write simple scripts

```bash
cd /tmp; ls; pwd # ; run one after the other, always

cd /tmp && ls # && run ls only if cd worked
FILES=$(ls)   # put the output of ls in a variable
FILES=`ls`    # same, old style (backticks)

exec ping 8.8.8.8 # replace the shell with ping. when ping ends, the shell is gone

test -s filename  # -s (size): file exist && size > 0
test -d /tmp      # -d (directory): is a directory
test -x script.sh # -x (execute): file is executable

read name age # read 2 words into 2 variables
echo $name:$age

read -t 3 -p "entrez votre nom: " nom # -t (timeout) 3 sec | -p (prompt) text
echo $nom

expr 5 + 3  # shows 8
expr 5 \* 4 # shows 20

let result=10+3 # result = 13
let "x = 5 * 4" # x = 20

mail -s "subject" root                            # -s (subject). press Ctrl+D to send
echo "the backup failed" | mail -s "subject" root # body from a pipe
```

## 106.1 The Linux Graphical Stack

The graphical stack, from top (user) to bottom (hardware):

```
                    User
             (You, Nagato, Yoda, ...)
                  /        \
                 /          \
      Desktop Manager    Window Manager
    (GNOME, KDE, ...)    (OpenBox, i3, dwm, awesome, ...)
                 \          /
                  \        /
                Display Server
            (Xorg (X11), Wayland, ...)
                     |
                   Kernel
               (Linux, BSD, ...)
                     |
                  Hardware
          (amd64, ARM, PowerPC, ...)
```

```bash
Xorg -configure       # old command to generate config, nowadays X11 autodetects hardware
/etc/X11/xorg.conf    # main X config file
/etc/X11/xorg.conf.d/ # X config snippets
~/.xsession-errors    # X errors of your session
# VESA = generic fallback graphics driver, works on any card but basic only (no acceleration)


xhost                # show who may connect to your X server
xhost +              # + : allow every host (insecure)
xhost -              # - : only hosts in the list
xhost +192.168.45.28 # allow one host

xauth list # show X auth cookies


# X (X11) = the windowing system / protocol
#   │
#   ├── XFree86   old implementation (dead since 2004)
#   └── Xorg      current implementation (forked from XFree86)

# Wayland = modern replacement for X (not X, a new system)

# TIMELINE
# XFree86 ──forked──> Xorg ──being replaced by──> Wayland
```

## 106.2 Graphical desktops

```bash
# 106.2 - GRAPHICAL DESKTOPS

# DESKTOP ENVIRONMENTS (full bundle: window manager + panels + apps)
#   GNOME    default on Ubuntu/Fedora, uses Mutter
#   KDE      feature-rich, uses KWin
#   XFCE     lightweight, good for old hardware

# DISPLAY MANAGER (the graphical login screen you see at boot)
#   can also offer remote graphical login with XDMCP
#   GDM (GNOME), SDDM (KDE), XDM (general) handle theming and login

# REMOTE CONNECTION TO GUIs
#
#   XDMCP    X Display Manager Control Protocol
#            Remote graphical login, native to X11.
#            Legacy/Obsolete: requires high bandwidth, highly insecure.
#
#   Spice    Simple Protocol for Independent Computing Environment
#            Fully open-source (released by Red Hat post-2008 acquisition).
#            Primary use case: connecting directly to KVM virtual machines.
#            High performance: near-local speed, low CPU overhead.
#
#   RDP      Remote Desktop Protocol
#            Microsoft native, but open to Linux via 'Xrdp' server listeners.
#            Default port 3389. Encrypted by default.
#            Excellent bandwidth compression and native multi-monitor support.
#
#   VNC      Virtual Network Computing
#            Cross-platform standard using the RFB (Remote Frame Buffer) protocol.
#            Default port 5900 + display offset (e.g., :1 = port 5901).
#            Highly compatible, but modern flavors (TigerVNC) require TLS setup for security.
#
#   Waypipe  Wayland Network Proxying
#            The modern successor to X11 forwarding over SSH ('ssh -X').
#            Efficiently pipes hardware-accelerated Wayland windows over network connections.
```

## 106.3 Accessibility

```bash
# KEYBOARD (all provided by AccessX, part of the X keyboard extension)
# command line tool: xkbset
#   Sticky Keys   - press modifier then key separately (Shift then A -> A)
#                   activation gesture: press Shift 5 times
#   Slow Keys     - key registers only if held down (gesture: hold Shift 8 sec)
#   Bounce Keys   - ignores same key pressed twice too fast (helps hand tremors)
#   Toggle Keys   - sound when Caps/Num Lock toggled
#   Mouse Keys    - numpad controls the mouse pointer

# MOUSE ASSIST
#   simulate right-click by holding left button
#   simulate click by hovering (holding pointer still)

# VISUAL (GNOME "Seeing" section)
#   High Contrast     - sharper colors for windows/buttons
#   Large Text        - bigger font
#   Cursor Size       - bigger mouse cursor
#   Screen Magnifier  - zoom part of screen (GNOME "Zoom", KDE "KMagnifier")

# SCREEN READER (text-to-speech)
#   Orca      - most popular, installed by default, GNOME project
#   Emacspeak - command-line option
#   works with Braille Display (hardware, raises pins to show braille)

# ON-SCREEN KEYBOARD
#   GNOME has it built in; other desktops can install "onboard" package
```

## 107.1 Manage user and group accounts

```bash
# KEY FILES
	# /etc/passwd       user accounts
	# /etc/shadow       password hashes + aging information
	# /etc/group        group definitions
	# /etc/skel/        template files for new users
	# /etc/login.defs   default user/group settings

# /etc/passwd FIELDS
	# name:x:UID:GID:comment:/home/dir:/bin/bash
	# x = password hash stored in /etc/shadow

# CREATE USERS
	adduser bob                         # high-level, interactive (Debian/Ubuntu)

	useradd bob                         # low-level, non-interactive
	useradd -m bob                      # -m (make home): create home directory
	useradd -d /tmp/bob bob             # -d (directory): home directory
	useradd -m -s /bin/bash bob         # -s (shell): set login shell
	useradd -c "comment!!" bob          # -c (comment): comment

# MODIFY / DELETE USERS
	usermod -g devs bob  # -g (lowercase): change bob's PRIMARY group to devs
	usermod -G devs bob  # -G (uppercase): set bob's SECONDARY groups (REPLACES all)
	usermod -aG devs bob # -a (append) + -G: ADD to secondary groups, keeps existing

	usermod -L bob                      # -L (Lock): lock password
	usermod -U bob                      # -U (Unlock): unlock password

	userdel bob                         # delete user
	userdel -r bob                      # -r (remove): delete user + home directory

# GROUPS
	addgroup devs                       # high-level Debian/Ubuntu tool

	groupadd -g 1200 devs               # -g (GID): specify GID
	groupadd devs                       # create group

	groupmod -n new old                 # -n (new name): rename group

	groupdel devs                       # delete group

	gpasswd devs                        # set a password for the group
	gpasswd -a bob devs                 # -a (add): add user to group

# PASSWORDS
	passwd bob                          # set/change password
	passwd -l bob                       # -l (lock): lock password
	passwd -u bob                       # -u (unlock): unlock password

# PASSWORD AGING
	chage -l bob            # -l (list): show current aging info (read-only)
	chage -M 90 bob         # -M (max): password must change after N days
	chage -m 7 bob          # -m (min): must wait N days before changing again
	chage -W 7 bob          # -W (warn): warn user N days before expiry
	chage -I 14 bob         # -I (inactive): lock account N days after password expires
	chage -E 2026-12-31 bob # -E (expire): account expiry DATE (or -1 = never)
	chage -d 0 bob          # -d (date): last change date. 0 = force change at next login
	chage bob               # interactive mode, asks each value one by one

# LOOKUP
	getent passwd bob                   # query user database
	getent group devs                   # query group database

	id bob                              # show UID, GID, and groups
```

```bash
# /etc/shadow
# Format:
# username:password:lastchange:min:max:warn:inactive:expire:reserved

# FIELDS
# 1. username     → account name
# 2. password     → password hash / lock marker
# 3. lastchange   → days since 1970 when password was last changed
# 4. min          → minimum days before password can be changed
# 5. max          → maximum password age in days
# 6. warn         → days before expiry to warn user
# 7. inactive     → days after password expires before account is disabled
# 8. expire       → account expiration date (days since 1970)
# 9. reserved     → reserved

# PASSWORD FIELD
# $6$...   → password hash
# *        → password authentication disabled
# !        → password locked
# empty    → no password

# EXAMPLE
# bob:$6$abc...:19800:0:90:7:14:19890:
```

## 107.2 Automate system administration tasks

```bash
# THREE WAYS TO SCHEDULE
#   cron          = repeating jobs on a schedule
#   at            = one-time job at a specific time
#   systemd timer = the systemd alternative to cron

# ===== CRON =====

# crontab (user's own scheduled jobs)
crontab -e        # -e (edit): edit your crontab
crontab -l        # -l (list): show your crontab
crontab -r        # -r (remove): delete your crontab
crontab -u bob -e # -u (user): edit another user's crontab (root)

# CRONTAB TIME FORMAT (5 fields + command)
#   min  hour  day-of-month  month  day-of-week  command
#   *    *     *             *      *            /path/script
#   ┌── minute (0-59)
#   │ ┌── hour (0-23)
#   │ │ ┌── day of month (1-31)
#   │ │ │ ┌── month (1-12)
#   │ │ │ │ ┌── day of week (0-7, 0 and 7 = Sunday)
#   * * * * * command
#
# examples:
#   30 2 * * *       every day at 2:30
#   0 * * * *        every hour (on the hour)
#   */15 * * * *     every 15 minutes
#   0 9 * * 1        every Monday at 9:00

# SPECIAL SHORTCUTS (replace the 5 fields)
#   @reboot @hourly @daily @weekly @monthly @yearly

# SYSTEM CRON LOCATIONS
#   /etc/crontab               system-wide crontab (has extra USER field)
#   /etc/cron.d/               drop-in system cron files
#   /etc/cron.hourly/          scripts run hourly
#   /etc/cron.daily/           scripts run daily
#   /etc/cron.weekly/          scripts run weekly
#   /etc/cron.monthly/         scripts run monthly
#   /var/spool/cron/           where user crontabs are stored
# NOTE: system crontab (/etc/crontab) has 7 fields (adds a USER before command)

# WHO CAN USE CRON
#   /etc/cron.allow    if exists, ONLY listed users can use cron
#   /etc/cron.deny     listed users are BLOCKED
#   (allow takes priority; if neither exists, usually all allowed)

# ===== AT (one-time jobs) =====
at 5pm              # schedule a job for 5pm (then type commands, Ctrl+D)
at now + 2 hours    # run 2 hours from now
at 10:00 tomorrow   # specific time
atq                 # list pending at jobs (q = queue)
atrm 3              # remove at job number 3 (rm = remove)
at -f script.sh 5pm # -f (file): run a script file at a time

# WHO CAN USE AT
#   /etc/at.allow   /etc/at.deny   (same logic as cron.allow/cron.deny)

# ===== SYSTEMD TIMERS (modern alternative) =====
systemctl list-timers                                      # show active timers
systemd-run --on-active=10m mycommand                      # run once, 10 min from now
systemd-run --on-calendar="20:00" /usr/bin/touch /tmp/test # run at 20:00
# timer units use OnCalendar= for schedules (like cron)

systemd-run --user --on-active=2m /bin/bash -c 'echo "systemd timerll!" > /home/amranich/test/timer' # --user: as your user, in 2 min
systemctl --user list-timers                                                                         # --user: show your own timers

# Once you have created the new timer, you can enable it and start it by running the following commands as root:
systemctl enable foobar.timer # start the timer at boot
systemctl start foobar.timer  # start the timer now
```

## 107.3 Localisation and internationalisation

```bash
# ===== TIMEZONE =====
# timezone = your time difference from a reference (UTC)
# servers/cloud often use UTC to avoid confusion

date        # show current date/time
cal         # show calendar
timedatectl # show time, timezone, UTC, sync status (systemd)

# tzselect - interactive, asks location, OUTPUTS the TZ name (doesn't set it)
tzselect

# TZ variable - set YOUR OWN timezone (not the system's)
TZ='America/New_York'; export TZ # put in ~/.profile for a personal timezone

# CONFIGURING SYSTEM TIMEZONE
# /etc/localtime  - the file Linux reads for system time
#                   symlink OR copy of a zoneinfo file
ln -s /usr/share/zoneinfo/America/New_York /etc/localtime # link method (-s = symbolic)
cp /usr/share/zoneinfo/America/New_York /etc/localtime    # copy method

# /etc/timezone   - holds timezone NAME (Debian based)
# /etc/sysconfig/clock - same, on RHEL based
# /usr/share/zoneinfo/ - database of all timezone files

timedatectl set-timezone Europe/Amsterdam # systemd way
dpkg-reconfigure tzdata                   # Debian interactive menu

# ===== LANGUAGES / LOCALE =====
# environment variables tell the system which language/format to use
# LANG=en_US.UTF-8  = English, US variant, UTF-8 encoding

locale    # show current locale settings
locale -a # -a (all): list installed locales

dpkg-reconfigure locales # Debian interactive menu for locales

# LC_* variables (each controls one category)
# LANG        default for everything (fallback)
# LC_ALL      OVERRIDES all (highest priority)
# LC_TIME     time format (e.g. en_GB.UTF-8 = British time format)
# LC_NUMERIC, LC_MONETARY, LC_MESSAGES, LC_CTYPE ...
# priority:  LC_ALL > LC_* > LANG

# LANG=C - plain defaults, English, predictable. used in SCRIPTS

# Good script (uses LANG=C)
export LANG=C
date | grep "Thu Sep" # works the same on every machine, because output is always English

localectl # systemd: show/set locale and keyboard layout

# /etc/timezone       → stores system timezone
# /etc/default/locale → stores system locale

# ===== ENCODING =====
# ASCII      basic English, 7-bit
# ISO-8859   (Latin-1) western european, 8-bit
# UTF-8      Unicode, all languages (modern default)
# Unicode    the standard; UTF-8 is an encoding of it

iconv -f ISO-8859-1 -t UTF-8 file.txt # convert encoding (-f from, -t to)


iconv -f UTF-8 -t ASCII//TRANSLIT test.txt > ascii.txt # TRANSLIT: replace special letters (é -> e)
```

## 108.1 Maintain system time

```bash
# System clock = kernel, runs while ON.   Hardware clock (RTC = Real Time Clock) = battery, runs while OFF.
# Keep hardware clock in UTC (Coordinated Universal Time). Local time = UTC + timezone.
#   --systohc : system -> hardware      --hctosys : hardware -> system

# ===== DISPLAY =====
date         # local time
date -u      # -u (UTC): Coordinated Universal Time
date +%s     # Unix time (seconds since 1970 epoch, overflows 2038 on 32-bit)
sudo hwclock # hardware clock (needs root)
timedatectl  # local + UTC + RTC + timezone + NTP (Network Time Protocol) sync status

# ===== SET (systemd way) =====
timedatectl set-time '2011-11-25 14:00:00' # date+time (or HH:MM:SS)
timedatectl set-timezone Africa/Cairo      # exact name, case matters
timedatectl list-timezones                 # grep this, it is long
timedatectl set-ntp true                   # network sync on/off

# ===== SET (legacy) =====
date -s "11 Nov 2011 11:11:11"   ; hwclock --systohc          # -s (set) system, push to hardware
hwclock --set --date "4/12/2019 11:15:19" ; hwclock --hctosys # set hardware, pull to system

# ===== TIMEZONE FILES =====
# /usr/share/zoneinfo/   all zone files
# /etc/localtime         file Linux reads (symlink/copy of a zoneinfo file)
# /etc/timezone          zone NAME, Debian only
ln -s /usr/share/zoneinfo/Canada/Eastern /etc/localtime # -s (symbolic): link localtime to the zone file

# ===== NTP (Network Time Protocol) =====
# Stratum: 0 = reference clocks, 1 = attached to them (private), 2 = public (pool.ntp.org).
# Offset=gap to NTP time | Step=big jump (>128ms) | Slew=slow fix (<128ms) | Insane=>17min, no change

# THREE WAYS TO SYNC (only run ONE at a time):
#   timesyncd = systemd built-in, light, syncs my clock only (cannot serve others)
#   ntpd      = full daemon, can also SERVE time to other machines
#   chrony    = modern alternative to ntpd
# timedatectl set-ntp controls ONLY timesyncd. If ntpd/chrony is installed:
#   -> set-ntp shows "NTP not supported" and timedatectl shows "NTP service: n/a"
#   -> this is normal. check "System clock synchronized: yes" instead.

# --- timesyncd (systemd built-in) ---
timedatectl set-ntp true           # turn timesyncd sync on/off
systemctl status systemd-timesyncd # is it running?

# --- ntpd (NTP daemon, full server, can also serve time) ---
# NOTE: on Debian/Ubuntu the package + service are named "ntp", the program is "ntpd"
systemctl enable ntpd && systemctl start ntpd # start at boot, and start now
# /etc/ntp.conf :  server 0.centos.pool.ntp.org iburst   (iburst = faster first sync)
# pool.ntp.org = free volunteer server pool, DNS (Domain Name System) gives a random one (spreads load)
# NTP is UDP (User Datagram Protocol) port 123
ntpdate pool.ntp.org                          # one-time manual sync (stop ntpd first; used when offset >17min)
ntpq -p                                       # ntpq (NTP query) -p (peers): show servers; * = server in use, -n (numeric) = show IPs

# --- chrony (modern alternative) ---
# chronyd = daemon,  chronyc = client (c = command line)
# config: /etc/chrony.conf (RHEL) | /etc/chrony/chrony.conf (Debian/Ubuntu). "!" = disabled line
chronyc tracking # how well synced (offset, stratum, drift)
chronyc sources  # which servers it uses
chronyc makestep # force an immediate step
```

## 108.2 System logging

```bash
# Logging = collect messages from the kernel, services and apps, and store them (usually /var/log).
# TWO systems:
#   rsyslog          = classic logging daemon, writes plain TEXT files in /var/log
#   systemd-journald = modern systemd logging, writes ONE BINARY journal (read with journalctl)
# They can run together. rsyslog can read from the journal.

# ============================================================
# LESSON 1 - rsyslog (classic)
# ============================================================

# LOGGING DAEMONS
#
#   syslog  (the original, now dead)
#      │
#      ├──> syslog-ng   (syslog new generation) ─┐
#      │                                          ├─ two SEPARATE competitors,
#      └──> rsyslog     (rocket-fast)  ──────────┘   both replaced old syslog
#
#   TODAY:
#     rsyslog     = most common (default on Debian, Ubuntu, RHEL)
#     syslog-ng   = still used, less common
#     syslog      = dead
#
#   ON systemd SYSTEMS (two layers):
#     systemd-journald   = base layer, always runs, binary journal
#           │
#           └──> rsyslog = often added on top, writes /var/log text files
#
# rsyslogd = the daemon    klogd = handles kernel messages



# ===== LOG LOCATIONS (/var/log) =====
#   /var/log/auth.log     (Debian)   logins, sudo, ssh, failed logins
#   /var/log/syslog       (Debian)   main log, almost everything
#   /var/log/messages     (RHEL)     main log, non-kernel messages
#   /var/log/kern.log     kernel messages
#   /var/log/daemon.log   background services
#   /var/log/mail.log     mail server
#   /var/log/boot.log     boot messages

# binary logs (need special tools, NOT less/cat):
#   /var/log/wtmp    -> last                 (successful logins)
#   /var/log/btmp    -> last -f / utmpdump   (failed logins, e.g. ssh brute force)
#   /var/log/faillog -> faillog              (failed auth)
#   /var/log/lastlog -> lastlog              (last login per user)

# ===== READING LOGS =====
less /var/log/auth.log       # page through
zless /var/log/auth.log.3.gz # same but for gzip-compressed rotated logs (also zmore)
tail -f /var/log/syslog      # -f (follow): show new lines live
head -5 /var/log/mail.log    # -5: first 5 lines
grep "sshd" /var/log/syslog  # filter

# log line format:  timestamp  hostname  program[PID]:  message   (PID = Process ID)

# ===== rsyslog.conf : FACILITY . PRIORITY  ACTION =====
# /etc/rsyslog.conf   (extra files in /etc/rsyslog.d/)
# 3 sections: MODULES, GLOBAL DIRECTIVES, RULES

# FACILITY = which subsystem made the message
#   kern, user, mail, daemon, auth/authpriv, syslog, lpr, news, cron, ftp, ntp, local0-local7 ...

# PRIORITY = how important (lower number = worse). 8 levels:
#   0 emerg    system unusable
#   1 alert    act now
#   2 crit     critical
#   3 err      error
#   4 warning  warning
#   5 notice   normal but important
#   6 info     informational
#   7 debug    debug
# a priority matches that level AND higher (mail.err = err + crit + alert + emerg)

# RULE format:  <facility>.<priority>   <action = where to send it>
auth,authpriv.*         /var/log/auth.log # all priorities (*) from auth -> auth.log
*.*;auth,authpriv.none  -/var/log/syslog  # everything EXCEPT auth (.none). - = less disk writes
mail.err                /var/log/mail.err # mail, err or worse
#  ; splits selectors   , joins facilities   .none excludes   .=debug means that ONE priority only

# ===== logger (write your own log line, for scripts/testing) =====
logger "this goes into /var/log/syslog"
logger -t backup "done" # -t (tag): a name you can grep later
tail -1 /var/log/syslog # -1: last line. see it

# ===== dmesg (kernel ring buffer) =====
# kernel logs to an in-memory ring buffer at boot, before rsyslog is ready
dmesg | grep usb # print kernel messages

# ===== logrotate (stop logs growing forever) =====
# renames, compresses, and finally deletes old logs. run daily by /etc/cron.daily/logrotate
# config: /etc/logrotate.conf (global) + /etc/logrotate.d/ (per package, overrides global)
# rotation:  messages -> messages.1 -> messages.2.gz -> ... -> deleted
# key directives:
#   rotate 4       keep 4 old copies
#   weekly         rotate every week (also daily, monthly)
#   compress       gzip old logs
#   delaycompress  compress one cycle later (log still being written)
#   create         make a new empty log after rotating
#   missingok      no error if log missing
#   notifempty     skip rotation if log is empty
#   postrotate / endscript   run a command after rotating

# ============================================================
# LESSON 2 - systemd-journald (modern)
# ============================================================

# systemd-journald = systemd's logging service. One central, indexed, BINARY journal.
# no log rotation needed. config: /etc/systemd/journald.conf
# binary = cannot use less/cat, must use journalctl

# ===== journalctl (read the journal, needs root/sudo) =====
journalctl                                       # whole journal, oldest first
journalctl -r                                    # -r (reverse): newest first
journalctl -f                                    # -f (follow): live (like tail -f)
journalctl -e                                    # -e (end): jump to end
journalctl -n 5                                  # -n (number): last 5 lines
journalctl -k                                    # -k (kernel): kernel messages only (= dmesg), also --dmesg
journalctl -b                                    # -b (boot): this boot   (-b -1 = previous boot, needs persistent storage)
journalctl -b -0 -p err                          # -p (priority): err or worse, for current boot
journalctl --since "19:00:00" --until "19:01:00" # time range (YYYY-MM-DD HH:MM:SS)
journalctl --since "2 minutes ago"               # also: yesterday, today, now
journalctl -u ssh.service                        # -u (unit): by systemd unit
journalctl /usr/sbin/sshd                        # by program path
# by field:  journalctl PRIORITY=3   SYSLOG_FACILITY=1   _PID=1
#   two fields together = AND    |    field + field = OR

# ===== systemd-cat (send command output INTO the journal) =====
# like logger, but for the journal. sends stdin, stdout, stderr to journald.
systemd-cat                          # no args: reads stdin, type lines, Ctrl+C to stop
echo "hello" | systemd-cat           # send a piped command's output to the journal
systemd-cat echo "hello too"         # run a command, send its output (and stderr) to journal
systemd-cat -p emerg echo "not real" # -p (priority): set a priority level
journalctl -n 4                      # see the last lines you added

# ===== STORAGE: persistent vs volatile =====
# /var/log/journal/   exists -> logs saved on DISK (survive reboot)
# /run/log/journal/   used when the above is missing -> RAM only, LOST on reboot
# set in /etc/systemd/journald.conf with Storage= :
#   Storage=persistent   disk, /var/log/journal (created if needed)
#   Storage=volatile     RAM only, /run/log/journal
#   Storage=auto         like persistent but does NOT create the dir (this is the DEFAULT)
#   Storage=none         throw logs away
# turn on persistent:  set Storage=persistent (or mkdir /var/log/journal), then restart: sudo systemctl restart systemd-journald

# ===== SIZE / DELETE OLD DATA =====
journalctl --disk-usage          # how much space the journal uses
# limits in journald.conf:  SystemMaxUse=500M  (max space, default 10% of filesystem, cap 4GiB)
#                           SystemKeepFree= , SystemMaxFileSize= , SystemMaxFiles= (default 100)
# manual clean (vacuum), only touches ARCHIVED files:
journalctl --vacuum-time=1months # delete older than 1 month
journalctl --vacuum-size=100M    # keep only 100M
journalctl --vacuum-files=10     # keep only 10 files

# ===== rsyslog <-> journald =====
# in journald.conf:  ForwardToSyslog=yes   -> journald also sends logs to rsyslog
# (also ForwardToKMsg, ForwardToConsole, ForwardToWall)


# ===== journalctl -D (read a journal from another location) =====
# -D (directory) <dir>, --directory=<dir> : read journal files from a given folder, not the default
# real use: a machine is broken. you boot a rescue USB, mount its disk,
#           and read ITS journal to see why it failed.
journalctl -D /mnt/broken/var/log/journal/
```

## 108.3 Mail Transfer Agent (MTA) basics

```bash
# MTA = moves mail (server)   |   MUA (Mail User Agent) = mail client (mail, Thunderbird)

# ===== MTAs =====
#   sendmail   oldest, huge, hard to configure, not security oriented -> few use it as default
#   exim       general and flexible, strong checks on incoming mail (ACLs, authentication)
#   postfix    newer alternative to sendmail, easy config files, multi-domain, encryption
#              -> default MTA on most distros
#   qmail      another MTA, just know the name
# most desktop distros install NO MTA by default. good choice: postfix + mailx (or bsd-mailx)

# ===== sendmail EMULATION LAYER =====
# every MTA copies sendmail's commands -> sendmail, mailq, newaliases work on ANY MTA

# ===== /etc/aliases (root) =====
postmaster:  root      # <alias>: <destination>
www:         webmaster # aliases can chain
test:        /dev/null # throw away
support:     ali, sara # several destinations
newaliases             # MUST run after editing (= sendmail -bi / -I)

# ===== mail =====
mail user                              # send: Subject, body, Ctrl+D to end
mail                                   # read inbox: p print, d delete, r reply, q quit
echo "body" | mail -s "subj" user@host # -s (subject)
mail -a file.gz user@host              # -a (attach)

# ===== ~/.forward (normal user) =====
# user forwards OWN mail: put a user or email address inside
# NO newaliases needed | owner-writable only | hidden file

# ===== queue =====
mailq       # show stuck mail + reason (= sendmail -bp)
sendmail -q # -q (queue): retry now

# ===== EXTRAS =====
# SMTP = TCP port 25
# queue: /var/spool/mqueue/ (sendmail) | /var/spool/postfix/
# inbox: /var/spool/mail/<user> | /var/mail/<user>
# sendmail: "." alone ends message  |  mail: Ctrl+D
```

## 108.4 Manage printers and printing

```bash
# CUPS (Common Unix Printing System) = the printing system on most distros. daemon: cupsd

# ===== INSTALL / START =====
sudo apt install cups             # (dnf install cups on RHEL)
sudo systemctl start cups.service # start CUPS now

# ===== CONFIG FILES (/etc/cups/) =====
# /etc/cups/cupsd.conf      main config.  Listen localhost:631 = listen on port 631
# /etc/cups/printers.conf   all printers. written by cupsd, DO NOT edit while cupsd runs
# /etc/cups/ppd/            PPD files (PostScript Printer Description) = text file describing each printer's features
# /var/log/cups/            access_log, error_log, page_log

# ===== WEB INTERFACE =====
# cupsd.conf: WebInterface Yes  ->  http://localhost:631
#   Administration = add printers, manage jobs, configure CUPS
#   Jobs           = active, pending, completed jobs
#   Printers       = list installed printers
# users can VIEW. changes need admin (set by <Limit ...> blocks at bottom of cupsd.conf)

# ===== LPD LEGACY INTERFACE (may need package: cups-bsd) =====
# LPD (Line Printer Daemon) = old BSD printing system, before CUPS.
# CUPS still accepts its commands, so old scripts keep working. CUPS does the real work.
lpr -PMyPrinter file.txt # -P (printer): print. no printer = default printer
lpq                      # show queue (q = queue). -a (all) printers | -PMyPrinter one printer
lprm 2                   # remove job ID 2 (rm = remove). only root removes others' jobs
lprm -                   # remove ALL your jobs
lpc status               # printer status (c = control)
#   NOTE: no space after -P  ->  -PMyPrinter
#   lpc status output:
#     queuing is enabled   -> queue ACCEPTS new jobs
#     printing is enabled  -> printer really PRINTS on paper

# ===== CONTROL QUEUE / PRINTING =====
cupsaccept  MyPrinter                      # queue accepts new jobs
cupsreject  MyPrinter                      # queue refuses new jobs
cupsenable  MyPrinter                      # physical printing ON
cupsdisable MyPrinter -r "need more paper" # printing OFF. -r (reason)
```

## 109.1 Fundamentals of internet protocols

```bash
# TCP/IP = the protocol stack of the Internet. includes TCP, UDP, ICMP, DNS ...

# ===== IPv4 =====
# format A.B.C.D, each part = octet (8 bits, 0-255). total 32 bits
# about 4.3 billion addresses -> not enough -> NAT and IPv6

# CLASSES (first octet)
#   A   1-126     255.0.0.0     /8
#   B   128-191   255.255.0.0   /16
#   C   192-223   255.255.255.0 /24
#   127.x.x.x = loopback (127.0.0.1)
#   224+      = multicast, not for hosts

# PRIVATE RANGES (not routed on the Internet)
#   10.0.0.0      - 10.255.255.255     (/8,  16M IPs)
#   172.16.0.0    - 172.31.255.255     (/12, 1M IPs)
#   192.168.0.0   - 192.168.255.255    (/16, 65K IPs)
# NAT (Network Address Translation) = many private IPs go out through ONE public IP

# ===== SUBNETTING =====
# netmask splits the IP: NETWORK bits (left) | HOST bits (right)
# CIDR (Classless Inter-Domain Routing) = number of network bits
#   /8  = 255.0.0.0     /16 = 255.255.0.0     /24 = 255.255.255.0
# usable hosts = 2^(host bits) - 2      (/24 -> 2^8 - 2 = 254)

# NETWORK + BROADCAST
#   network   = IP AND mask
#   broadcast = network OR flipped mask
# 192.168.4.12/24 -> network 192.168.4.0 | broadcast 192.168.4.255
ipcalc 192.168.4.12/24 # calculates it for you

# BINARY:  128 64 32 16 8 4 2 1   ->  11000000 = 128+64 = 192
# ===== PROTOCOLS =====
#   TCP   reliable, checks every packet     -> web, ssh, downloads
#   UDP   fast, no checks, can lose packets -> video calls, DNS
#   ICMP  diagnostics (ping), no user data

# ===== PORTS =====
# port = which program gets the packet. 0-65535
#   1-1023 = services (privileged)   |   1024+ = clients
# full list: /etc/services
#   20,21 FTP      53  DNS      139 NetBIOS    389 LDAP    636 LDAPS
#   22    SSH      80  HTTP     143 IMAP       443 HTTPS   993 IMAPS
#   23    Telnet   110 POP3     161,162 SNMP   465 SMTPS   995 POP3S
#   25    SMTP     123 NTP      514 Syslog
# tip: above 400 + ends in S = Secure

# ===== /etc/services =====
# text file: maps service names to port numbers + protocol
grep -w 22 /etc/services  # -w (word): exact word only. ssh   22/tcp
grep -w ssh /etc/services # find the port of a service

# ===== IPv6 =====
# 128 bits, 8 hex groups:  2001:0db8:0000:0000:0000:0000:0000:7344
# short: drop leading 0s, "::" for zero groups (only once) -> 2001:db8::7344
#
# unicast = one machine | multicast = all in group | anycast = nearest in group
#
# ===== IPv4 vs IPv6 =====
#   Feature          IPv4          IPv6
#   ---------------  ------------  ------------------------
#   size             32 bits       128 bits
#   send to all      broadcast     no broadcast -> multicast ff02::1
#   packet counter   TTL           Hop Limit
#   find neighbors   ARP           NDP
#   local address    -             fe80:: (link-local)
```

## 109.2 Persistent network configuration

```bash
# ===== NETWORK INTERFACES =====
# NIC (Network Interface Card) = the network hardware
# old names: eth0, eth1, wlan0      new names: eno1, ens1, enp3s5, wlp3s0
# lo = loopback, always there, = 127.0.0.1
ip link show # list interfaces

# ===== ifconfig (LEGACY, deprecated) =====
ifconfig                                          # show active interfaces   (-a (all) = even down)
ifconfig eth0 192.168.42.42 netmask 255.255.255.0 # set IP (root)
ifconfig eth0 down                                # turn off  (up = on)

# ===== ifup / ifdown (use saved config) =====
ifup eth0   # bring interface up using its config file
ifdown eth0 # bring it down
# config files:
#   Debian: /etc/network/interfaces        (all interfaces in ONE file)
#   RHEL:   /etc/sysconfig/network-scripts/ifcfg-eth0   (+ gateway in /etc/sysconfig/network)

# /etc/network/interfaces example:
# auto eth0                      # "auto" = bring up at boot
# iface eth0 inet static         # or: iface eth0 inet dhcp
# address 192.168.1.10
# netmask 255.255.255.0
# gateway 192.168.1.1

# ===== ip (modern, TEMPORARY changes) =====
ip addr add 172.19.1.10/24 dev eth2  # add IP (dev = device: which card)
ip addr show eth2                    # show IPs of eth2
ip addr del 172.19.1.10/24 dev eth2  # delete IP
ip link set eth2 up                  # turn on
ip route show                        # show routing table
ip route add default via 192.168.1.1 # add default gateway (via = through this gateway)

# ===== NetworkManager + nmcli =====
# NetworkManager = daemon that manages networks (auto wifi, DHCP)
# it manages interfaces NOT listed in /etc/network/interfaces
# DHCP (Dynamic Host Configuration Protocol) = get IP, mask, gateway, DNS automatically
# frontends: GUI applet | nmtui (text menu) | nmcli (command line)
nmcli general                                    # overall status
nmcli device                                     # list devices
nmcli device wifi                                # list wifi networks (= wifi list)
nmcli device wifi connect MyWifi password MyPass # connect to a wifi network

# ===== HOSTNAME =====
# /etc/hostname = the machine's name (static hostname)
hostnamectl set-hostname mycoolmachine          # sets all 3 types
hostnamectl --pretty set-hostname "LAN Storage" # nice name, spaces allowed
hostnamectl --transient set-hostname temp       # temporary
hostnamectl --static set-hostname firewall      # ONLY static
hostnamectl                                     # show status
# only the STATIC name is saved in /etc/hostname

# ===== /etc/hosts =====
# local list: IP -> name (checked before DNS by default)
127.0.0.1      localhost
::1            localhost
192.168.1.10   foo.mydomain.org  foo # extra names = aliases

# ===== /etc/resolv.conf (DNS) =====
nameserver 192.168.1.1        # DNS server. up to 3
nameserver 4.2.2.4            # fallback
domain nagato.net             # local domain -> short names work
search nagato.net company.com # domains to try for short names
# NOTE: the file is resolv.conf (no e), not resolve.conf

# ===== /etc/nsswitch.conf =====
# says WHERE and in WHICH ORDER to look up names, users, groups
hosts: files dns # first /etc/hosts, then DNS
# hosts: dns files             # DNS first, /etc/hosts only if DNS does not know

# ============================================================
# EXTRAS
# ============================================================
# NAME PREFIXES:  en = Ethernet | wl = WLAN (wifi) | ww = WWAN | ib = InfiniBand | sl = serial
# NAMING ORDER (Linux uses the first rule that works):
#   1. eno1    o = onboard card, number from BIOS
#   2. ens1    s = PCIe slot number
#   3. enp3s5  p = bus 3, slot 5 (see lspci)
#   4. enx...  x = MAC address (e.g. USB adapters)
#   5. eth0    old style, nothing else worked

# MORE nmcli
nmcli connection show                    # saved connections
nmcli connection up|down MyWifi          # activate / deactivate
nmcli connection delete "Hotel Internet" # delete a saved connection
nmcli device disconnect wlo1             # (connect = reconnect)
nmcli device wifi rescan                 # scan now (root)
nmcli radio wifi off                     # turn wifi off  (on = back)
# nmcli general CONNECTIVITY = portal -> needs web login (hotel wifi)

# systemd-networkd (awareness)
# systemd-networkd = manages interfaces | systemd-resolved = manages DNS
# /etc/systemd/network   -> your config files go here (highest priority)

# NOTE: ifup/ifdown + /etc/network/interfaces = legacy. modern Ubuntu/Debian use netplan
#   (/etc/netplan/*.yaml).
```

## 109.3 Basic network troubleshooting

```bash
# ===== TROUBLESHOOTING STEPS ("I cannot open webpages") =====
#   1. interface UP + has IP?     ip addr
#   2. can I reach the gateway?   ping <gateway>
#   3. can I reach the Internet?  ping 4.2.2.4    (IP, no DNS needed)
#   4. does DNS work?             ping google.com / dig google.com
#   5. where does it break?       traceroute

# ===== ifconfig & ip (check IP) =====
ip addr show   # needs correct IP + netmask
ifconfig       # legacy
man ip-address # help for one ip subcommand

# ===== ping & ping6 =====
ping 192.168.70.1       # gateway: should always answer (unless ICMP blocked)
ping 4.2.2.4            # Internet by IP
ping google.com         # "unknown host" = DNS problem -> check /etc/resolv.conf
ping -c 3 192.168.50.2  # -c (count): send 3 then stop (else Ctrl+C)
ping6 -c 3 2001:db8::10 # IPv6

# ===== ROUTING (temporary, lost at reboot) =====
# "Network is unreachable" + gateway pings OK = default gateway MISSING
ip route show                              # "default via 192.168.70.1" = default gateway
sudo ip route del default                  # delete the default gateway
sudo ip route add default via 192.168.70.1 # add it back (via = through this gateway)
netstat -nr                                # routing table, legacy (-n numeric, -r routes)

# ===== traceroute & tracepath =====
traceroute 4.2.2.4 # each router (hop) on the way. * * * = hop blocks ICMP
tracepath 4.2.2.4  # same idea (for LPIC-1 "essentially the same")

# ===== ss & netstat (ports and connections) =====
# ss = new, netstat = legacy. same options mostly
ss -na | grep LISTEN # -n numeric, -a all
ss -tulpn            # t tcp | u udp | l listening | p process | n numeric
netstat -tulpn       # same, legacy

# ===== netcat (nc) =====
nc -l 1337        # -l (listen): listen on port 1337
nc localhost 1337 # connect, type text -> shows on the listener

# ===== dig =====
dig google.com # SERVER: line shows which DNS answered

# ============================================================
# EXTRAS
# ============================================================
# LEGACY (net-tools)  ->  MODERN (iproute2)
#   ifconfig          ->  ip addr / ip link
#   route             ->  ip route
#   netstat           ->  ss
#   arp               ->  ip neighbour

# ROUTES
ip route save > backup  |  ip route restore < backup # save the routing table / load it back
ip neighbour                                         # ARP / neighbor table
```

## 109.4 Configure client side DNS

```bash
# DNS (Domain Name System) = turns names into IPs  (yahoo.com -> 206.190.36.45)

# ===== /etc/resolv.conf (which DNS server to use) =====
nameserver 192.168.1.1
nameserver 4.2.2.4
# often "# Generated by NetworkManager" -> hand edits get OVERWRITTEN (temporary)

# ===== host (simple lookup) =====
host kernel.org      # A (IPv4), AAAA (IPv6), MX (mail) records
host -t A kernel.org # -t (type): only one record type
host 208.80.154.224  # IP -> name (reverse lookup, PTR record)

# ===== dig (detailed lookup, for troubleshooting) =====
dig x.org               # ANSWER section: x.org. 1625 IN A 131.252.210.176
#   1625 = TTL: seconds this answer stays in cache
#   SERVER: 192.168.1.1#53 = which DNS answered (port 53)
dig @8.8.8.8 google.com # @ = ask THIS DNS server, not the one in resolv.conf
dig -t MX lpi.org       # -t (type): record type

# ===== /etc/hosts (static, local names) =====
192.168.59.231  mass1        # works even if DNS does not know "mass1"
127.0.0.1       facebook.com # block a site: name points to your own machine
# dig ignores /etc/hosts (asks DNS only) -> dig mass1 fails, ping mass1 works

# ===== /etc/nsswitch.conf (lookup ORDER) =====
hosts: files mdns4_minimal [NOTFOUND=return] dns
#   files = /etc/hosts first -> then mdns -> then dns
#   [NOTFOUND=return] = stop here if the service answered "not found"

# ===== getent (lookup like a real program, follows nsswitch) =====
getent hosts              # all hosts entries
getent hosts dns1.lpi.org # one name

# ===== systemd-resolved (awareness) =====
# systemd's local DNS service, listens on 127.0.0.53
# asks the real servers from /etc/systemd/resolved.conf or /etc/resolv.conf

# ============================================================
# EXTRAS
# ============================================================
# resolv.conf limits:
#   max 3 nameserver | max 6 search domains
#   domain and search: use ONE. if both, the LAST one wins
options timeout:3 # seconds to wait for a DNS answer

# nsswitch actions:
#   [NOTFOUND=return]   service answered "not found" -> stop
#   [!UNAVAIL=return]   DNS is reachable -> stop, even if no answer
#   [SUCCESS=continue]  found, but keep going (later source wins)

# record types (use with -t):
#   A = IPv4 | AAAA = IPv6 | MX = mail | NS = name servers | SOA = zone info | PTR = IP -> name
host -t MX lpi.org dns1.easydns.com # last argument = which DNS server to ask
dig +short lpi.org                  # +short: only the IP, no extra text
# ~/.digrc = your default dig options

getent -s files hosts learning.lpi.org # -s (source): force one source (files or dns)
getent group openldap                  # works for users/groups too, not just hosts

# KEY DIFFERENCE:
#   getent, ping, ssh, curl -> follow nsswitch (files, dns, ...) = what programs really see
#   host / dig / nslookup   -> ask DNS ONLY (ignore /etc/hosts)
```

## 110.1 Perform security administration tasks

```bash
# ===== su vs sudo =====
su -       # become root. asks ROOT's password. "-" = load target's environment
su - carol # become carol. asks CAROL's password
su         # no "-" -> keeps your old environment (stays in /home/you)
sudo ls    # run ONE command as root. asks YOUR password
sudo su -  # become root using your own password
# sudo is safer: no root password shared, only single commands

sudo -u carol ping 8.8.8.8 # -u (user): run as carol

# ===== /etc/sudoers (edit ONLY with visudo) =====
root    ALL=(ALL:ALL) ALL   # user  host=(as_user:as_group)  commands
%sudo   ALL=(ALL:ALL) ALL   # %  = a group
%admin  ALL=(ALL) ALL
nagato  ALL=(ALL) /bin/ping # nagato can run ONLY ping as root
#includedir /etc/sudoers.d  # extra files, preferred place for your rules
visudo                      # checks syntax before saving. a broken sudoers = no sudo

# ===== WHO IS / WAS LOGGED IN =====
w                     # logged in now + what they are doing (+ uptime, load)
who                   # logged in now (user, tty, time, host)
last                  # past logins, newest first. reads /var/log/wtmp
last -f /var/log/btmp # -f (file): FAILED logins (same as: lastb)

# ===== passwd =====
passwd             # change your own password
sudo passwd nagato # change another user's password
passwd -S          # -S (Status): nagato P 2023-09-14 0 99999 7 -1
#   P = has password | L = locked | NP = no password
passwd -l nagato # -l (lock)    (-u unlock, -e expire)
# shell, home... -> use usermod, not passwd

# ===== chage (password aging) =====
chage -l nagato   # -l (list): list aging info
chage nagato      # interactive mode (root)
chage -m 7 nagato # -m (min): min days between changes  (-M = max days)

# ===== SUID / SGID =====
# SUID (s in user part) = runs as the file OWNER, not as the runner
ls -l /usr/bin/passwd  # -l (long). -rwsr-xr-x root  -> passwd can edit /etc/shadow for normal users
# danger: SUID on vi = anyone edits any file as root. audit regularly:
sudo find / -perm -u+s # -perm (permissions): all SUID files
# SGID = same idea, runs with the file's GROUP

# ===== LIMITS =====
ulimit -a   # -a (all): show all limits
ulimit -t 1 # -t (time): CPU time max 1 second. TEMPORARY (this shell only)
# permanent, system-wide: /etc/security/limits.conf
#   <domain>   <type>  <item>     <value>
#   @student   hard    nproc      20        # group student: max 20 processes
#   @student   -       maxlogins  4         # "-" = soft and hard
#   domain: user | @group | * (default)    type: soft | hard
# soft = user can change it | hard = the real maximum

# ===== OPEN PORTS =====
netstat -tuna        # t tcp | u udp | n numeric | a all  ("tuna" sandwich)
#   LISTEN = server waiting | ESTABLISHED = active connection | 0.0.0.0 = any address
ss -tuna             # modern
lsof -i              # -i (internet): open network connections + command, PID, user
sudo fuser -v 22/tcp # -v (verbose): which process uses port 22

# ===== nmap =====
nmap localhost # scan ports 1-1000, show open ones

# ============================================================
# EXTRAS
# ============================================================
# find -perm, the 3 forms:
find . -perm 4000         # ONLY SUID, exactly
find /usr/bin -perm -4000 # SUID + any other perms   (= -perm -u+s)
find /usr/bin -perm -2000 # SGID                      (= -perm -g+s)
find /usr/bin -perm /6000 # SUID OR SGID              (4 + 2 = 6)

# lock also with usermod
usermod -L carol            # -L (Lock)   (-U Unlock)
usermod -f 3 carol          # -f: disable account 3 days after password expires (= chage -I)
usermod -e 2050-12-13 carol # -e (expire): account expire date (= chage -E)

# chage options
#   -m min | -M max | -d last change (0 = force change at login)
#   -I inactive days | -E account expire date | -W warn days

# lsof / fuser
lsof -i@192.168.1.7 # -i (internet): connections to one host
lsof -i :22         # one port
fuser -vn tcp 80    # -v (verbose) -n (namespace) tcp: who uses tcp port 80
fuser -k 80/tcp     # -k (kill): KILL the processes using it

# nmap
nmap -p 22 localhost    # -p (port): one port (= -p ssh)
nmap -p 22-80 localhost # range
nmap -p- localhost      # ALL 65535 ports
nmap -F localhost       # -F (fast): top 100 ports
nmap 192.168.1.0/24     # whole subnet (--exclude 192.168.1.7)

# ulimit soft / hard
ulimit -Ha     # -H (hard) + -a (all): all HARD limits (-a alone = soft)
ulimit -Sf 200 # -S (soft) + -f (file size): set only soft file size
ulimit -f 500  # no -S/-H = sets BOTH
# normal user: can LOWER hard, raise soft only up to hard

# who / w / last
who -b     # -b (boot): last boot time  (-r runlevel, -H headings)
last carol # one user only

# sudo
sudo -u carol cmd                                               # -u (user): run as another user
carol ALL=(ALL:ALL) NOPASSWD: /usr/bin/systemctl status apache2 # no password asked
# sudo remembers your password 15 min. change: Defaults timestamp_timeout=1
# aliases: Host_Alias | User_Alias | Cmnd_Alias | Runas_Alias
User_Alias ADMINS = carol, %sudo, !john # ! = exclude
Cmnd_Alias SERVICES = /usr/bin/systemctl *
ADMINS ALL = SERVICES
```

## 110.2 Setup host security

```bash
# ===== SHADOW PASSWORDS =====
# problem: /etc/passwd must be readable by ALL users -> hashes would be visible
# fix: hash moves to /etc/shadow, passwd shows only "x"
ls -l /etc/passwd       # -rw-r--r--  root root     everyone can read
ls -l /etc/shadow       # -rw-r-----  root shadow   only root (and group shadow)
grep nagato /etc/passwd # nagato:x:1000:1000:nagato,,,:/home/nagato:/bin/bash
grep nagato /etc/shadow # Permission denied  -> needs sudo

# ===== /etc/nologin (maintenance) =====
# file exists -> nobody can log in, its text is shown to them. delete it -> logins work again
# root CAN still log in
sudo usermod -s /sbin/nologin baduser # -s (shell): this user has no shell, but mail/ftp still work

# ===== SUPER-SERVERS (inetd, xinetd) =====
# one daemon listens for many services, starts the real service ONLY when a request comes
# old, rarely used today. modern replacement: systemd .socket units
# /etc/xinetd.conf   main config (includedir /etc/xinetd.d)
# /etc/xinetd.d/     one file per service
service telnet
{
    disable      = no                   # no = ACTIVE, yes = off
    socket_type  = stream               # stream = TCP, dgram = UDP
    wait         = no                   # no = handle many connections at once
    user         = root
    server       = /usr/sbin/in.telnetd # full path of the real service
    no_access    = 10.0.1.0/24          # blocked network
    access_times = 09:45-16:15          # allowed hours
}

# systemd .socket = modern xinetd: systemd waits on the port, starts the service on demand
sudo systemctl stop ssh.service # stop the always-running sshd
sudo systemctl start ssh.socket # systemd now watches port 22
sudo lsof -i :22 -P             # -P: show port numbers. listener = systemd, not sshd

# ===== TCP WRAPPERS: /etc/hosts.allow & /etc/hosts.deny =====
# work only for programs linked with libwrap:
ldd /usr/sbin/vsftpd | grep libwrap # ldd = list the libraries a program uses
# format:  service: hosts
vsftpd: 10.10.100.                  # in hosts.allow -> only 10.10.100.* may use vsftpd
sshd: ALL                           # in hosts.deny  -> block everyone
sshd: LOCAL                         # in hosts.allow -> except local network
# ALL = all services or all hosts

# ===== REMOVE UNUSED SERVICES =====
sudo service --status-all                          # SysV list: [+] running, [-] stopped
sudo chkconfig vsftpd off                          # RedHat, old
sudo update-rc.d vsftpd remove                     # Debian, old
systemctl list-units --state active --type service # list running services
sudo systemctl disable vsftpd.service --now        # systemd: stop now + off at boot
ss -ltu    /  netstat -ltu                         # -l listening -t tcp -u udp: listening services

# ===== /etc/inittab (SysV, old) =====
# format:  id:runlevel:action:process
1:2345:respawn:/sbin/mingetty tty1 # runlevels 2-5: start getty, restart if killed
id:3:initdefault:                  # boot into runlevel 3
# /etc/init.d/  = old init scripts
```

## 110.3 Securing data with encryption

```bash
# ===== KEY PAIRS =====
# symmetric  = one shared password encrypts AND decrypts
# asymmetric = key PAIR: what one key locks, only the other opens
#   public key  -> give to everyone      private key -> keep secret
#   encrypt: others use YOUR public key -> only your private key opens it
#   sign:    you use YOUR private key   -> anyone checks it with your public key

# ===== SSH HOST KEYS (server identity) =====
ssh 192.168.70.2           # 1st time: "authenticity can't be established" + fingerprint -> yes
# saved in ~/.ssh/known_hosts (per user) | /etc/ssh/ssh_known_hosts (system-wide)
# key changed -> "REMOTE HOST IDENTIFICATION HAS CHANGED!" (maybe man-in-the-middle)
ssh-keygen -R 192.168.70.2 # -R (remove): remove old key from known_hosts (after checking it's safe)
# server keys: /etc/ssh/ssh_host_{rsa,dsa,ecdsa,ed25519}_key (+ .pub)

# ===== YOUR OWN KEYS =====
ssh-keygen          # default: rsa -> ~/.ssh/id_rsa + id_rsa.pub
ssh-keygen -t ecdsa # -t (type): rsa | dsa | ecdsa | ed25519 -> ~/.ssh/id_ecdsa(.pub)
# passphrase = password on the private key (asked on every use)

# ===== KEY-BASED LOGIN (no password) =====
ssh-copy-id 192.168.70.2 # copies your PUBLIC key into server's ~/.ssh/authorized_keys
# server needs in /etc/ssh/sshd_config:  PubkeyAuthentication yes

# ===== ssh-agent / ssh-add =====
ssh-agent /bin/bash # start a shell with the agent
ssh-add             # load your keys -> passphrase asked ONCE, then remembered

# ===== SSH TUNNELS =====
ssh -L 5433:localhost:5432 admin@ec2
#   -L (local): my localhost:5433 -> through ec2 -> ec2's Postgres (localhost:5432)
#   use: open a server DB that only listens on localhost, from my PC

ssh -R 8000:localhost:3000 admin@ec2
#   -R (remote): ec2's port 8000 -> back to MY localhost:3000
#   use: show my local dev site to someone through the server

ssh -R 0.0.0.0:8000:localhost:3000 admin@ec2
#   same, but port 8000 opens on ALL ec2 interfaces (reachable from internet)
#   needs GatewayPorts in the server's sshd_config (default: localhost only)

ssh -D 1080 192.168.70.2 # -D (dynamic): localhost:1080 becomes a SOCKS proxy
ssh -X 192.168.70.2      # -X: X11 forwarding: remote GUI apps show on my screen
#   needs X11Forwarding yes in sshd_config

# -L  LOCAL:  bring a remote port to my machine
#     ssh -L 5433:localhost:5432 admin@ec2
#
#     [devbox]                              [EC2]
#     DBeaver -> :5433 ===== SSH =====> localhost:5432 (Postgres)
#                ▲ port opens here
#
# -R  REMOTE: send my port to the remote machine
#     ssh -R 8000:localhost:3000 admin@ec2
#
#     [devbox]                              [EC2]                    [friend]
#     my site :3000 <==== SSH ===== :8000 <---------------------- browser
#                                   ▲ port opens here
#
# -D  DYNAMIC: remote machine becomes my proxy
#     ssh -D 1080 admin@ec2
#
#     [devbox]                              [EC2]               [internet]
#     browser -> :1080 ===== SSH =====> EC2 ------------------> google.com
#                ▲ port opens here             ├--------------> youtube.com
#                                              └--------------> any site
#
# =====  inside the SSH tunnel (encrypted)
# ---->  normal traffic
# ▲      where the listening port opens


# ===== GPG =====
gpg --gen-key                                                  # create key pair in ~/.gnupg/
gpg --list-keys                                                # list the keys in your keyring
gpg --export nagato > nagato.pub.key                           # share your public key (-a (armor) = ASCII text)
gpg --import nagato.pub.key                                    # import someone's public key
gpg --output nagato.revoke.asc --gen-revoke nagato@example.com # revoke if key is stolen

# encrypt / decrypt
gpg --out file.txt.encrypted --recipient nagato@example.com --encrypt file.txt # encrypt with nagato's public key
gpg --out out.txt --decrypt file.txt.encrypted                                 # decrypt with your private key

# sign / verify
gpg --output msg.sig --sign msg.txt # sign with MY private key (binary)
gpg --verify msg.sig                # check signature with sender's public key
gpg --output msg --decrypt msg.sig  # verify + get the content
gpg --clearsign msg.txt             # -> msg.txt.asc: readable text + signature

# gpg-agent = like ssh-agent, keeps gpg key passphrases in memory

# ============================================================
# EXTRAS
# ============================================================
ssh-keygen -t ecdsa -b 521 # -b (bits) = key size in bits
```
