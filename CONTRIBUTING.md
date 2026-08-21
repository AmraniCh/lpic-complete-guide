# Contributing

The full contributor guide lives in [docs/contributing.md](docs/contributing.md),
and is published at the **Contributing** page on the site.

Quick version:

1. **Found a mistake?** Open an issue, or click the pencil icon on any page.
2. **Want to write a whole objective?** Claim it in an issue first, so nobody
   duplicates your work.
3. **Read the [style guide](docs/style-guide.md)** before writing. It is short.

Run the site locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Before opening a pull request:

```bash
mkdocs build --strict
python3 tools/check_style.py
```
