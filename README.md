# LPIC Complete Guide

My study notes for taking the **LPIC** certifications, written with
**Claude Opus 4.8** under my concise guidance.

Currently covering **LPIC-1** (exams 101-500 and 102-500, objectives
version 5.0).

[![Publish site](https://github.com/AmraniCh/lpic-complete-guide/actions/workflows/deploy.yml/badge.svg)](https://github.com/AmraniCh/lpic-complete-guide/actions/workflows/deploy.yml)
[![Checks](https://github.com/AmraniCh/lpic-complete-guide/actions/workflows/checks.yml/badge.svg)](https://github.com/AmraniCh/lpic-complete-guide/actions/workflows/checks.yml)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE)

**Read it here:** <https://lpic.amranich.dev/>

---


## Run it locally

```bash
git clone https://github.com/AmraniCh/lpic-complete-guide.git
cd lpic-complete-guide

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
                         The nav and the weight bars read from here.
  scaffold.py            Creates a page for every objective. Copies in the ones
                         already written, makes a stub for the rest. Safe to
                         re-run: it never overwrites a finished page.
  hooks.py               Runs at build time. Adds the weight bars to the
                         sidebar.
  check_style.py         Enforces the house style in CI: plain English, no em
                         dashes, a prose Summary, correct front matter.

docs/                  The pages themselves.
  index.md               Home
  exam-101/, exam-102/   One folder per topic
  style-guide.md         How pages are written here
  stylesheets/           The terminal skin
```

## Sources and thanks

The LPIC-1 notes were built while studying from two free resources, and
both deserve the credit:

- **[linux1st.com](https://linux1st.com)**, Jadi's free book and YouTube
  course. The section order of most LPIC-1 pages follows his.
- **The official LPI learning material** for objectives v5.0, published at
  [learning.lpi.org](https://learning.lpi.org).

Pages are written in my own words: facts and ideas are free to use, exact
wording is not.

## Licence

[MIT](LICENSE). Use it, change it, share it, sell it. Just keep the copyright
notice.