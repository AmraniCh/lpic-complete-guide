#!/usr/bin/env python3
"""
Check pages against the house style rules.

Runs in CI on every pull request. The point is to catch the mechanical
rules automatically, so human reviewers can spend their attention on
whether the explanation is any good.

Only pages marked `status: written` are checked. Stubs are skipped.

Usage:
    python3 tools/check_style.py
"""

import os
import re
import sys

DOCS = "docs"

# Words that make a page harder to read for a non-native speaker, mapped to
# the plainer word we ask for instead.
PLAINER = {
    "utilise": "use",
    "utilize": "use",
    "leverage": "use",
    "subsequently": "then",
    "in order to": "to",
    "is capable of": "can",
    "facilitates": "helps",
    "aforementioned": "this",
    "commence": "start",
    "terminate": "stop or end",
    "prior to": "before",
}


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def check(path, text, weights):
    """Return a list of problems found in one page."""
    problems = []
    fm = front_matter(text)
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)

    # Ignore anything inside a fenced code block. Command output is allowed
    # to contain whatever it contains.
    prose = re.sub(r"```.*?```", "", body, flags=re.S)

    if fm.get("status") != "written":
        return problems

    obj = fm.get("objective", "")

    # 1. front matter must agree with the objective map
    if not obj:
        problems.append("missing `objective` in front matter")
    elif obj not in weights:
        problems.append(f"objective `{obj}` is not in objectives.py")
    else:
        want = str(weights[obj])
        got = fm.get("weight", "")
        if got != want:
            problems.append(
                f"weight is `{got}` but objectives.py says `{want}`"
            )

    # 2. no em dashes or en dashes
    for dash, name in (("\u2014", "em dash"), ("\u2013", "en dash")):
        if dash in prose:
            problems.append(f"contains an {name}, use a plain hyphen instead")

    # 3. every written page ends with a Summary
    if not re.search(r"^##+\s+Summary\s*$", body, re.M):
        problems.append("no `## Summary` section")

    # 4. the Summary should be prose, not a bullet list
    m = re.search(r"^##+\s+Summary\s*$(.*)", body, re.M | re.S)
    if m:
        summary = m.group(1).strip()
        bullets = len(re.findall(r"^\s*[-*]\s", summary, re.M))
        if bullets > 2:
            problems.append(
                f"Summary looks like a list ({bullets} bullets), "
                "the style guide asks for prose"
            )

    # 5. plain English. The objective intro block (Description, Objectives,
    #    Terms) is a verbatim quote of the official LPI objectives. Like
    #    command output, it is external literal text, so it is exempt from
    #    the plain-English rewrite rule.
    prose_words = prose
    intro = re.search(r"^#\s+.+?\n(.*?)(?=^#{2,}\s)", prose, re.S | re.M)
    if intro and "**Objectives**" in intro.group(1):
        prose_words = prose.replace(intro.group(1), "", 1)
    low = prose_words.lower()
    for word, better in PLAINER.items():
        if re.search(rf"\b{re.escape(word)}\b", low):
            problems.append(f'"{word}" -> use "{better}"')

    # 6. an H1 is required, and only one. Checked against prose, because
    #    inside a code block `#` is a shell comment or a root prompt.
    h1s = re.findall(r"^#\s+\S", prose, re.M)
    if len(h1s) != 1:
        problems.append(f"expected exactly one H1, found {len(h1s)}")

    return problems


def main():
    sys.path.insert(0, os.path.dirname(__file__))
    try:
        from objectives import weight_map
    except ImportError:
        print("cannot import objectives.py - run this from the repo root")
        return 1

    weights = weight_map()
    total_problems = 0
    checked = 0

    for root, _, files in os.walk(DOCS):
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()

            problems = check(path, text, weights)
            if front_matter(text).get("status") == "written":
                checked += 1
            if problems:
                total_problems += len(problems)
                print(f"\n{path}")
                for p in problems:
                    print(f"  - {p}")

    print(f"\nchecked {checked} written pages")
    if total_problems:
        print(f"{total_problems} problem(s) found")
        print("See docs/style-guide.md for the rules.")
        return 1

    print("all good")
    return 0


if __name__ == "__main__":
    sys.exit(main())
