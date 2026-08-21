# Contributing

Thanks for helping. Most of this guide is unwritten, and every page you add
helps someone else pass this exam.

**You do not need to be an expert.** If you are studying for LPIC-1 right
now, you are exactly the right person. Writing a page is one of the best
ways to actually learn it.

## Ways to help

| What | Effort | How |
|---|---|---|
| Report a mistake | 2 minutes | Open a [correction issue](https://github.com/AmraniCh/lpic1-complete-guide/issues/new/choose) |
| Fix a typo | 5 minutes | Click the pencil icon at the top of any page |
| Improve an existing page | 30 minutes | Add a missing example or a clearer explanation |
| Write a whole objective | A few hours | Claim one first, so nobody duplicates your work |

## Fix a typo without installing anything

Every page has a **pencil icon** at the top right. Click it, edit the text
on GitHub, and open a pull request. No setup needed.

## Write a whole objective

### 1. Claim it first

Open a [claim issue](https://github.com/AmraniCh/lpic1-complete-guide/issues/new/choose)
saying which objective you are taking. This stops two people writing the
same page.

### 2. Run the site on your machine

```bash
git clone https://github.com/AmraniCh/lpic1-complete-guide.git
cd lpic1-complete-guide

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
mkdocs serve
```

Open <http://127.0.0.1:8000>. The page reloads as you type.

### 3. Write the page

Find the stub file for your objective under `docs/`. The path follows the
objective number, for example:

```
docs/exam-101/103-gnu-and-unix-commands/103.7-search-text-files-using-regular-expressions.md
```

Replace the stub with your content, following the
**[style guide](style-guide.md)**. Please read it before you start. It is
short, and it is what keeps the pages consistent.

Then change the front matter:

```yaml
status: written
```

The coverage table on the home page updates itself from that line.

### 4. Check it builds

```bash
mkdocs build --strict
```

`--strict` turns warnings into errors, which catches broken links.

### 5. Open a pull request

Use the checklist at the end of the [style guide](style-guide.md). Ticking
it yourself makes review much faster.

## Where the content comes from

Pages are written from **two sources only**:

1. [linux1st.com](https://linux1st.com), Jadi's free book
2. The official LPI learning material for objectives v5.0

This is deliberate. Mixing in random blog posts is how notes drift away
from what the exam actually tests.

## Reviewing

Pull requests need one approval. Reviewers check:

- Does it follow the source order?
- Are the config samples real and complete?
- Is the English simple enough?
- Does the Summary read as prose?

Reviews are about the page, never the person. If you are reviewing, be
kind. Someone spent their study time on this.

## Code of conduct

Be decent to each other. People here are studying for a hard exam, often
in a second language, often after a full day of work. Assume good faith,
explain rather than criticise, and remember that "obvious" is relative.

Harassment of any kind means removal from the project.

## Licence

By contributing, you agree your work is released under the
[MIT licence](https://github.com/AmraniCh/lpic1-complete-guide/blob/main/LICENSE),
athe same as the rest of the project.

Please write in your own words. Do not paste text from copyrighted
material, including the LPI PDF. Facts and ideas are fine to use freely,
but exact wording is not.
