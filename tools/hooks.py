"""
Build-time hook.

Tags every sidebar link with its exam weight, so the CSS can draw the
weight bars. The bars are real information, not decoration: LPI draws
questions in proportion to weight, so a weight 4 objective is worth
roughly four times the study time of a weight 1.
"""

import re
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from objectives import all_objectives

WEIGHTS = {o[4]: o[6] for o in all_objectives()}


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
