# Contributing

Most of this guide is unwritten. If you are studying for an LPIC exam,
writing a page is one of the best ways to learn it.

## Quick fixes

Click the **pencil icon** at the top of any page to fix a typo directly on
GitHub. No setup needed.

## Writing an objective

1. Open a [claim issue](https://github.com/AmraniCh/lpic1-complete-guide/issues/new/choose)
   so nobody duplicates your work.
2. Clone and run locally:

    ```bash
    git clone https://github.com/AmraniCh/lpic1-complete-guide.git
    cd lpic1-complete-guide
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    mkdocs serve
    ```

3. Find the stub under `docs/`, replace it with your content following
   the **[style guide](style-guide.md)**.
4. Change `status: stub` to `status: written` in the front matter.
5. Run `mkdocs build --strict` and `python3 tools/check_style.py`.
6. Open a pull request.

## Sources

Each certification level has its own sources listed on its overview page.
Stick to those sources -- mixing in random blog posts is how notes drift
from what the exam actually tests.

## Licence

By contributing you agree your work is released under the
[MIT licence](https://github.com/AmraniCh/lpic1-complete-guide/blob/main/LICENSE).
Write in your own words -- do not paste from copyrighted material.
