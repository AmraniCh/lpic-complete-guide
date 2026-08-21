# Style guide

Every page here follows the same rules. They exist so the notes read as one
book written by one person, not forty pages written by forty people.

If you only remember one thing: **write for someone who is tired, in a
hurry, and reading English as a second language.**

## Language

**Use plain English.** Short sentences. Common words.

Many people preparing for LPIC-1 are not native English speakers. A page
that needs a dictionary is a page that does not get read.

| Instead of | Write |
|---|---|
| utilise, leverage | use |
| in order to | to |
| subsequently | then, after that |
| is capable of | can |
| it is recommended that you | you should |
| facilitates the process of | helps you |

One idea per sentence. If a sentence has two commas and an "although",
split it in two.

**Do not use em dashes.** Use a plain hyphen with spaces around it, or
start a new sentence.

## Sources

Content comes from **two sources only**:

1. The matching page on **[linux1st.com](https://linux1st.com)**, Jadi's
   free book.
2. The matching section of the **official LPI learning material** for
   objectives v5.0.

Do not add material from blogs, Stack Overflow, or your own memory. If you
know something useful that is not in either source, it can still go in, but
say so plainly in the text, for example: *"This is not in the official
material, but in real work you will see..."*

**Follow the linux1st.com section order exactly.** Do not reorganise a page
into what you think is a better order. Readers move between the video, the
book, and these notes, and the order has to match.

## Structure

Every page looks like this:

```
---
objective: "102.4"
weight: 3
status: written
---

# 102.4 Use Debian package management

## First section from linux1st.com

...

## Summary
```

- The H1 is the objective number and its official LPI title.
- H2 sections mirror the source page order.
- The page ends with a Summary.

## Include the real thing

**Always include the config samples and command output shown in the
sources.** Do not summarise them.

Bad:

> The `yum.conf` file contains settings for the cache directory and GPG
> checking.

Good:

````
Sample `/etc/yum.conf`:

```
[main]
cachedir=/var/cache/yum/$basearch/$releasever
keepcache=0
gpgcheck=1
plugins=1
```
````

A reader revising the night before the exam needs to recognise the real
file, not a description of it.

## Explain hard things

For any option or flag that is not obvious from its name, give a **real
world reason** to use it, not just a definition.

Bad:

| Option | Description |
|---|---|
| `init=` | Run a specific program instead of the default init |

Good:

| Option | Description |
|---|---|
| `init=` | Run something else instead of the normal init. For example `init=/bin/bash` drops you straight into a root shell with no login prompt, which is how you recover a system when you have forgotten the root password |

## Diagrams

**Long or abstract sections get an ASCII diagram**, so the reader can see
the shape of the idea before reading the text.

Keep them plain. No colour, no Unicode box drawing, just characters that
work everywhere:

```
BIOS path:
  Power on --> POST --> MBR (512 bytes) --> GRUB core --> kernel

UEFI path:
  Power on --> Security phase --> ESP --> grubx64.efi --> kernel
```

## The Summary

Every page ends with a Summary. It has rules of its own:

- Write it as **prose paragraphs**, not a bullet list.
- Write it in the **first person**: *"I have a Linux system that..."*
- Three or four short paragraphs.
- Put commands, paths, and key terms in `backticks`.
- Do not dump a command reference into it. It is a recap, not a cheat
  sheet.

Example opening:

> I have a Debian-based Linux system where software is distributed as
> `.deb` packages. There are two layers of tools: `dpkg` at the bottom
> works directly with individual `.deb` files, but it cannot resolve
> dependencies on its own.

## Weight and front matter

Every page starts with front matter:

```yaml
---
objective: "102.4"
weight: 3
status: written
---
```

- `objective` and `weight` must match
  [objectives.py](https://github.com/AmraniCh/lpic1-complete-guide/blob/main/objectives.py).
  Do not invent weights.
- `status` is `stub` or `written`. Change it to `written` when the page is
  finished. The coverage table on the home page counts this automatically.

## Scope

Cover what the **official LPI objective** lists, and stop there.

Each objective has a "key knowledge areas" list and a "partial list of the
used files, terms and utilities" on the
[LPI objectives page](https://www.lpi.org/our-certifications/exam-101-102-objectives/).
That list is the scope. It is not random, and it is what the exam draws
from.

Going deeper is not automatically better. A reader with twelve days left
needs the objective covered, not everything that exists.

## Checklist before you open a pull request

- [ ] Sections follow the linux1st.com page order
- [ ] Config samples and command output are included in full
- [ ] Hard options have a real world example
- [ ] Long sections have a diagram
- [ ] Summary is prose, first person, with backticks on key terms
- [ ] No em dashes
- [ ] Front matter `weight` matches `objectives.py`
- [ ] `status:` changed to `written`
- [ ] `mkdocs build --strict` runs with no warnings
