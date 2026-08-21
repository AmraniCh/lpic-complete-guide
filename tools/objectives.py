"""
Single source of truth for the LPIC-1 objective map.

Everything else reads from this file: the navigation, the weight bars in
the sidebar, the coverage table on the home page, and the stub generator.
Change an objective here and the whole site follows.

Weights are the official LPI weights for objectives version 5.0:
https://www.lpi.org/our-certifications/exam-101-102-objectives/
"""

# exam -> [(topic number, topic name, folder slug,
#           [(objective, title, weight, file slug), ...]), ...]
OBJECTIVES = {
    "101": [
        ("101", "System Architecture", "101-system-architecture", [
            ("101.1", "Determine and configure hardware settings", 2, "101.1-hardware-settings"),
            ("101.2", "Boot the system", 3, "101.2-boot-the-system"),
            ("101.3", "Change runlevels / boot targets and shutdown or reboot system", 3, "101.3-runlevels-and-boot-targets"),
        ]),
        ("102", "Installation and Package Management", "102-installation-and-package-management", [
            ("102.1", "Design hard disk layout", 2, "102.1-design-hard-disk-layout"),
            ("102.2", "Install a boot manager", 2, "102.2-install-a-boot-manager"),
            ("102.3", "Manage shared libraries", 1, "102.3-manage-shared-libraries"),
            ("102.4", "Use Debian package management", 3, "102.4-debian-package-management"),
            ("102.5", "Use RPM and YUM package management", 3, "102.5-rpm-and-yum-package-management"),
            ("102.6", "Linux as a virtualization guest", 1, "102.6-linux-as-a-virtualization-guest"),
        ]),
        ("103", "GNU and Unix Commands", "103-gnu-and-unix-commands", [
            ("103.1", "Work on the command line", 4, "103.1-work-on-the-command-line"),
            ("103.2", "Process text streams using filters", 2, "103.2-process-text-streams-using-filters"),
            ("103.3", "Perform basic file management", 4, "103.3-perform-basic-file-management"),
            ("103.4", "Use streams, pipes and redirects", 4, "103.4-streams-pipes-and-redirects"),
            ("103.5", "Create, monitor and kill processes", 4, "103.5-create-monitor-and-kill-processes"),
            ("103.6", "Modify process execution priorities", 2, "103.6-modify-process-execution-priorities"),
            ("103.7", "Search text files using regular expressions", 3, "103.7-search-text-files-using-regular-expressions"),
            ("103.8", "Basic file editing", 3, "103.8-basic-file-editing"),
        ]),
        ("104", "Devices, Linux Filesystems, Filesystem Hierarchy Standard", "104-devices-filesystems-fhs", [
            ("104.1", "Create partitions and filesystems", 2, "104.1-create-partitions-and-filesystems"),
            ("104.2", "Maintain the integrity of filesystems", 2, "104.2-maintain-the-integrity-of-filesystems"),
            ("104.3", "Control mounting and unmounting of filesystems", 3, "104.3-control-mounting-and-unmounting"),
            ("104.5", "Manage file permissions and ownership", 3, "104.5-manage-file-permissions-and-ownership"),
            ("104.6", "Create and change hard and symbolic links", 2, "104.6-hard-and-symbolic-links"),
            ("104.7", "Find system files and place files in the correct location", 2, "104.7-find-system-files-and-fhs"),
        ]),
    ],
    "102": [
        ("105", "Shells and Shell Scripting", "105-shells-and-shell-scripting", [
            ("105.1", "Customize and use the shell environment", 4, "105.1-customize-and-use-the-shell-environment"),
            ("105.2", "Customize or write simple scripts", 4, "105.2-customize-or-write-simple-scripts"),
        ]),
        ("106", "User Interfaces and Desktops", "106-user-interfaces-and-desktops", [
            ("106.1", "Install and configure X11", 2, "106.1-install-and-configure-x11"),
            ("106.2", "Graphical desktops", 1, "106.2-graphical-desktops"),
            ("106.3", "Accessibility", 1, "106.3-accessibility"),
        ]),
        ("107", "Administrative Tasks", "107-administrative-tasks", [
            ("107.1", "Manage user and group accounts and related system files", 5, "107.1-manage-user-and-group-accounts"),
            ("107.2", "Automate system administration tasks by scheduling jobs", 4, "107.2-automate-system-administration-tasks"),
            ("107.3", "Localisation and internationalisation", 3, "107.3-localisation-and-internationalisation"),
        ]),
        ("108", "Essential System Services", "108-essential-system-services", [
            ("108.1", "Maintain system time", 3, "108.1-maintain-system-time"),
            ("108.2", "System logging", 4, "108.2-system-logging"),
            ("108.3", "Mail Transfer Agent (MTA) basics", 3, "108.3-mail-transfer-agent-basics"),
            ("108.4", "Manage printers and printing", 2, "108.4-manage-printers-and-printing"),
        ]),
        ("109", "Networking Fundamentals", "109-networking-fundamentals", [
            ("109.1", "Fundamentals of internet protocols", 4, "109.1-fundamentals-of-internet-protocols"),
            ("109.2", "Persistent network configuration", 4, "109.2-persistent-network-configuration"),
            ("109.3", "Basic network troubleshooting", 4, "109.3-basic-network-troubleshooting"),
            ("109.4", "Configure client side DNS", 2, "109.4-configure-client-side-dns"),
        ]),
        ("110", "Security", "110-security", [
            ("110.1", "Perform security administration tasks", 3, "110.1-perform-security-administration-tasks"),
            ("110.2", "Setup host security", 3, "110.2-setup-host-security"),
            ("110.3", "Securing data with encryption", 4, "110.3-securing-data-with-encryption"),
        ]),
    ],
}


def all_objectives():
    """Flat list: (exam, topic_num, topic_name, topic_slug, obj, title, weight, slug)."""
    for exam, topics in OBJECTIVES.items():
        for tnum, tname, tslug, objs in topics:
            for obj, title, weight, slug in objs:
                yield exam, tnum, tname, tslug, obj, title, weight, slug


def doc_path(exam, topic_slug, slug):
    return f"exam-{exam}/{topic_slug}/{slug}.md"


def weight_map():
    """Objective number -> weight. Used to draw the sidebar bars."""
    return {o[4]: o[6] for o in all_objectives()}


def exam_total(exam):
    return sum(o[6] for o in all_objectives() if o[0] == exam)
