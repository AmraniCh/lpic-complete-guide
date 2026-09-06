#!/usr/bin/env python3
"""
Generate the docs tree from objectives.py.

Objectives that are already written get copied in from their source file.
Everything else gets a short stub that marks the page as not written yet.

Safe to re-run: a page whose front matter says `status: written` is never
overwritten.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from objectives import all_objectives, doc_path

# objective -> the note file we already wrote for it
WRITTEN = {
    "101.1": "/mnt/user-data/outputs/101.1-hardware-settings.md",
    "101.2": "/mnt/user-data/outputs/101.2-boot-the-system.md",
    "101.3": "/mnt/user-data/outputs/101.3-change-runlevels-boot-targets-shutdown-reboot.md",
    "102.1": "/mnt/user-data/outputs/102.1-design-hard-disk-layout.md",
    "102.2": "/mnt/user-data/outputs/102.2-install-a-boot-manager.md",
    "102.3": "/mnt/user-data/outputs/102.3-manage-shared-libraries.md",
    "102.4": "/mnt/user-data/outputs/102.4-use-debian-package-management.md",
    "102.5": "/mnt/user-data/outputs/102.5-use-rpm-and-yum-package-management.md",
    "102.6": "/mnt/user-data/outputs/102.6-linux-as-a-virtualization-guest.md",
}

DOCS = "docs"

STUB = """---
objective: "{obj}"
weight: {weight}
status: stub
---

# {obj} {title}

!!! note "Not written yet"

    Notes for this objective have not been written yet.

**Exam weight: {weight}.** {weight_note}
"""

WEIGHT_NOTE = {
    1: "One of the smallest objectives on the exam, so keep it tight.",
    2: "A small objective. A focused page is enough.",
    3: "A medium objective. Expect several questions from it.",
    4: "A heavy objective. Roughly four times the questions of a weight 1.",
    5: "The heaviest objective on either exam. Worth the most detail.",
}


def to_page(src_text, obj, title, weight):
    """Turn one of our note files into a site page."""
    body = re.sub(r"\A##\s+.+?\n", "", src_text, count=1)
    body = re.sub(r"\A\s*---\s*\n", "", body, count=1)
    front = (
        f'---\nobjective: "{obj}"\nweight: {weight}\nstatus: written\n---\n\n'
        f"# {obj} {title}\n\n"
    )
    return front + body.lstrip()


def main():
    copied = made = skipped = 0

    for exam, tnum, tname, tslug, obj, title, weight, slug in all_objectives():
        path = os.path.join(DOCS, doc_path(exam, tslug, slug))
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                if "status: written" in fh.read(400):
                    skipped += 1
                    continue

        source = WRITTEN.get(obj)
        if source and os.path.exists(source):
            with open(source, encoding="utf-8") as fh:
                text = fh.read()
            with open(path, "w", encoding="utf-8") as out:
                out.write(to_page(text, obj, title, weight))
            copied += 1
        else:
            with open(path, "w", encoding="utf-8") as out:
                out.write(STUB.format(
                    obj=obj, title=title, weight=weight,
                    weight_note=WEIGHT_NOTE.get(weight, ""),
                ))
            made += 1

    print(f"written pages copied : {copied}")
    print(f"stubs generated      : {made}")
    print(f"left untouched       : {skipped}")


if __name__ == "__main__":
    sys.exit(main())
