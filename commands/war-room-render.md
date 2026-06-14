---
description: Render a sealed war-room dossier to a shareable, self-contained HTML page
argument-hint: "<dossier-file> [\"Decision title\"]"
---

Render a war-room dossier to HTML:

$ARGUMENTS

Run:

```bash
python3 scripts/render-dossier.py <dossier-file> "<decision title>" > <dossier-file>.html
```

The text dossier stays the source of truth; this just produces a styled, dependency-free HTML view of it (one file — open it, share it, screenshot it). If no dossier file is given, render the most recent one from this session.
