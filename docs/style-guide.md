# Style guide

**Write for someone who is tired, in a hurry, and reading English as a
second language.**

## Language

Plain English. Short sentences. Common words. No em dashes.

| Instead of | Write |
|---|---|
| utilise, leverage | use |
| in order to | to |
| subsequently | then |
| is capable of | can |

## Sources

Each certification level lists its sources on its overview page. Use only
those. Follow the primary source's section order so readers can move
between the source and these notes.

## Structure

```
---
objective: "102.4"
weight: 3
status: written
---

# 102.4 Use Debian package management

## First section from the primary source

...

## Summary
```

- H1 is the objective number and its official LPI title.
- H2 sections mirror the source order.
- Every page ends with a **Summary** written as prose (not a list), in
  first person, with key terms in `backticks`.

## Content rules

- Include real config samples and command output in full, not summaries.
- Give hard options a real world example, not just a definition.
- Add an ASCII diagram for long or abstract sections.

## Front matter

- `objective` and `weight` must match
  [objectives.py](https://github.com/AmraniCh/lpic1-complete-guide/blob/main/tools/objectives.py).
- Set `status` to `written` when the page is finished.

## Checklist

- [ ] Sections follow the source page order
- [ ] Config samples and command output included in full
- [ ] Hard options have a real world example
- [ ] Long sections have a diagram
- [ ] Summary is prose, first person
- [ ] No em dashes
- [ ] Front matter `weight` matches `objectives.py`
- [ ] `status:` changed to `written`
- [ ] `mkdocs build --strict` passes
