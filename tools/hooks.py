"""
Build-time hook.

Two jobs that would otherwise be manual work every time someone finishes an
objective:

1. Tag every sidebar link with its exam weight, so the CSS can draw the
   weight bars. The bars are real information, not decoration: LPI draws
   questions in proportion to weight, so a weight 4 objective is worth
   roughly four times the study time of a weight 1.

2. Count how many objectives are actually written and inject the live
   numbers into the home page. Nobody has to remember to update a table.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from objectives import OBJECTIVES, all_objectives, doc_path

WEIGHTS = {o[4]: o[6] for o in all_objectives()}


def _is_written(docs_dir, rel_path):
    path = os.path.join(docs_dir, rel_path)
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as fh:
        return "status: written" in fh.read(400)


def _coverage(docs_dir):
    rows = []
    done_w = total_w = done_n = total_n = 0

    for exam, topics in OBJECTIVES.items():
        for tnum, tname, tslug, objs in topics:
            t_done = t_total = t_done_w = t_total_w = 0
            for obj, title, weight, slug in objs:
                total_n += 1
                total_w += weight
                t_total += 1
                t_total_w += weight
                if _is_written(docs_dir, doc_path(exam, tslug, slug)):
                    done_n += 1
                    done_w += weight
                    t_done += 1
                    t_done_w += weight
            rows.append({
                "exam": exam, "num": tnum, "name": tname,
                "done": t_done, "total": t_total, "total_w": t_total_w,
            })
    return done_w, total_w, done_n, total_n, rows


def on_page_markdown(markdown, page, config, files, **kwargs):
    """Swap the coverage marker on the home page for live numbers."""
    if "<!-- COVERAGE -->" not in markdown:
        return markdown

    done_w, total_w, done_n, total_n, rows = _coverage(config["docs_dir"])
    pct = round(done_w / total_w * 100) if total_w else 0

    out = [
        f"**{done_n} of {total_n} objectives written.** "
        f"That covers {done_w} of {total_w} exam weight points, or {pct}%.\n",
        '<div class="lp-progress">'
        f'<div class="lp-progress__fill" style="width:{pct}%"></div></div>\n',
        "| Topic | Objectives | Weight | Written |",
        "|---|---|---|---|",
    ]

    for r in rows:
        if r["done"] == r["total"]:
            mark = "done"
        elif r["done"] == 0:
            mark = "planned"
        else:
            mark = f"{r['done']} of {r['total']}"
        out.append(f"| {r['num']} {r['name']} | {r['total']} | {r['total_w']} | {mark} |")

    return markdown.replace("<!-- COVERAGE -->", "\n".join(out))


def on_post_page(output, page, config, **kwargs):
    """Add data-weight to sidebar links so the CSS can draw the bars."""
    def tag(match):
        attrs, label = match.group(1), match.group(2)
        # Material wraps the label in <span class="md-ellipsis">, so the tags
        # have to come off before the objective number can be read.
        text = re.sub(r"<[^>]+>", " ", label).split()
        first = text[0] if text else ""
        weight = WEIGHTS.get(first)
        if weight is None or "data-weight" in attrs:
            return match.group(0)
        return f'<a{attrs} data-weight="{weight}">{label}</a>'

    return re.sub(
        r'<a([^>]*class="[^"]*md-nav__link[^"]*"[^>]*)>(.*?)</a>',
        tag, output, flags=re.S,
    )
