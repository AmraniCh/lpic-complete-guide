# LPIC Complete Guide

Open study notes for **LPIC** certifications. Currently covering
**LPIC-1** (exams 101-500 and 102-500, objectives version 5.0).

[![Publish site](https://github.com/AmraniCh/lpic1-complete-guide/actions/workflows/deploy.yml/badge.svg)](https://github.com/AmraniCh/lpic1-complete-guide/actions/workflows/deploy.yml)
[![Checks](https://github.com/AmraniCh/lpic1-complete-guide/actions/workflows/checks.yml/badge.svg)](https://github.com/AmraniCh/lpic1-complete-guide/actions/workflows/checks.yml)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE)

**Read it here:** <https://lpic.amranich.dev/>

---


## Status

**9 of 42 objectives written.** Topics 101 and 102 are complete. Everything
else is a stub, and **every stub is free to claim**.

| Exam | Topic | Objectives | Weight | Written |
|---|---|---|---|---|
| 101 | 101 System Architecture | 3 | 8 | done |
| 101 | 102 Installation and Package Management | 6 | 12 | done |
| 101 | 103 GNU and Unix Commands | 8 | 26 | help wanted |
| 101 | 104 Devices, Filesystems, FHS | 6 | 14 | help wanted |
| 102 | 105 Shells and Shell Scripting | 2 | 8 | help wanted |
| 102 | 106 User Interfaces and Desktops | 3 | 4 | help wanted |
| 102 | 107 Administrative Tasks | 3 | 12 | help wanted |
| 102 | 108 Essential System Services | 4 | 12 | help wanted |
| 102 | 109 Networking Fundamentals | 4 | 14 | help wanted |
| 102 | 110 Security | 3 | 10 | help wanted |

The site rebuilds this table automatically from the pages themselves, so it
is never out of date.

## Run it locally

```bash
git clone https://github.com/AmraniCh/lpic1-complete-guide.git
cd lpic1-complete-guide

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
mkdocs serve
```

Open <http://127.0.0.1:8000>. Pages reload as you save them.

## How the project fits together

```
tools/                 All project scripts live here.
  objectives.py          One source of truth: all 42 objectives and weights.
                         The nav, the weight bars, and the coverage table all
                         read from here.
  scaffold.py            Creates a page for every objective. Copies in the ones
                         already written, makes a stub for the rest. Safe to
                         re-run: it never overwrites a finished page.
  hooks.py               Runs at build time. Adds the weight bars to the
                         sidebar, and rewrites the coverage table from what is
                         actually on disk.
  check_style.py         Enforces the house style in CI: plain English, no em
                         dashes, a prose Summary, correct front matter.

docs/                  The pages themselves.
  index.md               Home
  exam-101/, exam-102/   One folder per topic
  style-guide.md         How pages are written here
  contributing.md        How to help
  stylesheets/           The terminal skin
```

## Contributing

Every unwritten objective is free to claim, and **you do not need to be an
expert.** If you are studying for LPIC-1 right now, writing a page is one of
the best ways to actually learn it.

1. Read the **[style guide](docs/style-guide.md)**. It is short.
2. Claim an objective by opening an issue, so nobody duplicates your work.
3. Write the page, then change `status: stub` to `status: written`.
4. Run `mkdocs build --strict` and `python3 tools/check_style.py`.
5. Open a pull request.

Full details in **[CONTRIBUTING.md](CONTRIBUTING.md)**.

Fixing a typo needs no setup at all: click the pencil icon at the top of any
page on the site.

## Sources and thanks

The LPIC-1 notes were built while studying from two free resources, and
both deserve the credit:

- **[linux1st.com](https://linux1st.com)**, Jadi's free book and YouTube
  course. The section order of most LPIC-1 pages follows his.
- **The official LPI learning material** for objectives v5.0, published at
  [learning.lpi.org](https://learning.lpi.org).

Pages are written in contributors' own words. Please keep it that way: facts
and ideas are free to use, exact wording is not.

## Licence

[MIT](LICENSE). Use it, change it, share it, sell it. Just keep the copyright
notice.