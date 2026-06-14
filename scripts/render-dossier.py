#!/usr/bin/env python3
"""render-dossier.py — turn a war-room dossier into a self-contained HTML page.

The text dossier (STRATEGY / BATTLE-PLAN / BASELINE / HOW-WE-LOSE) stays the
source of truth. This is a VIEW of it: one styled, dependency-free HTML file
you can open, share, or screenshot. Standard library only.

Usage:  python3 scripts/render-dossier.py <dossier-file> ["Decision title"] > dossier.html
"""
import sys
import re
import html
from datetime import datetime, timezone


def parse_dossier(text):
    data = {"strategy": "", "why": "", "battle_plan": [], "baseline": [], "how_we_lose": []}
    section = None
    entry = None
    for raw in text.splitlines():
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip())
        head = re.match(r"^(STRATEGY|BATTLE-PLAN|BASELINE|HOW-WE-LOSE):\s*(.*)$", raw)
        if head and indent == 0:
            section = head.group(1)
            if section == "STRATEGY":
                data["strategy"] = head.group(2).strip()
            entry = None
            continue
        if section == "STRATEGY":
            m = re.match(r"^\s*why-it-wins:\s*(.*)$", raw)
            if m:
                data["why"] = m.group(1).strip()
            continue
        if section in ("BATTLE-PLAN", "BASELINE"):
            m = re.match(r"^\s*-\s*(.*)$", raw)
            if m:
                key = "battle_plan" if section == "BATTLE-PLAN" else "baseline"
                data[key].append(m.group(1).strip().strip('"'))
            continue
        if section == "HOW-WE-LOSE":
            m = re.match(r"^\s*-\s*by:\s*(.*)$", raw)
            if m:
                entry = {"by": m.group(1).strip(), "axis": "", "claim": "",
                         "grounding": "", "failure_world": "", "predictability": "", "status": ""}
                data["how_we_lose"].append(entry)
                continue
            m = re.match(r"^\s*(axis|claim|grounding|failure-world|predictability|status):\s*(.*)$", raw)
            if m and entry is not None:
                entry[m.group(1).replace("-", "_")] = m.group(2).strip().strip('"')
    return data


def esc(s):
    return html.escape(str(s or ""))


def badge(value, kind):
    v = (value or "").strip().lower()
    if not v:
        return ""
    return f'<span class="badge {kind} {kind}-{esc(v)}">{esc(v)}</span>'


def grounding_html(g):
    g = (g or "").strip()
    if not g:
        return ""
    if g.lower() == "speculative":
        return '<span class="grounding speculative">speculative</span>'
    return f'<span class="grounding ref">{esc(g)}</span>'


CSS = """
:root{--bg:#0b1020;--bg2:#111726;--panel:rgba(255,255,255,.03);--line:rgba(245,166,35,.16);
--ink:#e6e9f0;--muted:#8a93a6;--amber:#f5a623;--amber2:#ffb627;
--green:#3fb950;--red:#f0883e;--blue:#58a6ff;}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(1200px 600px at 70% -10%,#16203a 0%,var(--bg) 55%) ,var(--bg);
color:var(--ink);font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;}
.wrap{max-width:820px;margin:0 auto;padding:56px 24px 80px}
.kicker{letter-spacing:.42em;font-size:12px;color:var(--amber);text-transform:uppercase;font-weight:700}
h1{font-size:30px;line-height:1.2;margin:.5rem 0 .25rem;font-weight:700}
.meta{color:var(--muted);font-size:13px;margin-bottom:40px}
.section{margin:34px 0}
.section>h2{font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);
border-bottom:1px solid var(--line);padding-bottom:8px;margin:0 0 16px;font-weight:700}
.strategy{background:linear-gradient(180deg,rgba(245,166,35,.08),rgba(245,166,35,.02));
border:1px solid var(--line);border-radius:14px;padding:22px 24px}
.strategy .course{font-size:21px;font-weight:700;color:var(--amber2)}
.strategy .why{color:var(--muted);margin-top:8px}
ul.lines{list-style:none;padding:0;margin:0}
ul.lines li{padding:10px 0 10px 26px;position:relative;border-bottom:1px solid rgba(255,255,255,.05)}
ul.lines li:before{content:"▸";position:absolute;left:4px;color:var(--amber);opacity:.8}
ul.baseline li:before{content:"○";color:var(--muted)}
.card{background:var(--panel);border:1px solid rgba(255,255,255,.07);border-left:3px solid var(--amber);
border-radius:10px;padding:16px 18px;margin:12px 0}
.card .by{font-weight:700}
.card .axis{color:var(--muted);font-size:13px;margin-left:8px}
.card .claim{margin:8px 0}
.card .fw{color:var(--muted);font-style:italic;margin-top:8px;font-size:14px;
border-left:2px solid rgba(255,255,255,.1);padding-left:12px}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px}
.grounding{font:13px ui-monospace,SFMono-Regular,Menlo,monospace}
.grounding.ref{color:var(--amber2)}
.grounding.speculative{color:var(--muted);font-style:italic;font-family:inherit}
.badge{font-size:11px;font-weight:700;letter-spacing:.04em;padding:3px 9px;border-radius:999px;text-transform:uppercase}
.pred-novel{background:rgba(245,166,35,.18);color:var(--amber2);border:1px solid var(--line)}
.pred-predictable{background:transparent;color:var(--muted);border:1px solid rgba(255,255,255,.15)}
.status-defused{background:rgba(63,185,80,.15);color:var(--green)}
.status-not-defused{background:rgba(240,136,62,.15);color:var(--red)}
.status-bet-accepted{background:rgba(88,166,255,.15);color:var(--blue)}
.foot{margin-top:56px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:16px}
.foot a{color:var(--amber)}
"""


def render(data, title):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out = []
    out.append("<!doctype html><html lang=en><head><meta charset=utf-8>")
    out.append('<meta name=viewport content="width=device-width,initial-scale=1">')
    out.append(f"<title>{esc(title)} — war-room</title><style>{CSS}</style></head><body><div class=wrap>")
    out.append('<div class=kicker>war&#8202;-&#8202;room dossier</div>')
    out.append(f"<h1>{esc(title)}</h1>")
    out.append(f'<div class=meta>Sealed {stamp} · a frozen record, not a replayable verdict</div>')

    out.append('<div class="section"><h2>Strategy</h2><div class=strategy>')
    out.append(f'<div class=course>{esc(data["strategy"]) or "NO_CONVERGENCE"}</div>')
    if data["why"]:
        out.append(f'<div class=why>{esc(data["why"])}</div>')
    out.append("</div></div>")

    if data["battle_plan"]:
        out.append('<div class="section"><h2>Battle plan</h2><ul class=lines>')
        out += [f"<li>{esc(x)}</li>" for x in data["battle_plan"]]
        out.append("</ul></div>")

    if data["baseline"]:
        out.append('<div class="section"><h2>Baseline · the predictable objections</h2><ul class="lines baseline">')
        out += [f"<li>{esc(x)}</li>" for x in data["baseline"]]
        out.append("</ul></div>")

    if data["how_we_lose"]:
        out.append('<div class="section"><h2>How we lose</h2>')
        for e in data["how_we_lose"]:
            out.append('<div class=card>')
            out.append(f'<span class=by>{esc(e["by"])}</span>')
            if e["axis"]:
                out.append(f'<span class=axis>{esc(e["axis"])}</span>')
            if e["claim"]:
                out.append(f'<div class=claim>{esc(e["claim"])}</div>')
            if e["failure_world"]:
                out.append(f'<div class=fw>{esc(e["failure_world"])}</div>')
            out.append('<div class=row>')
            out.append(grounding_html(e["grounding"]))
            out.append(badge(e["predictability"], "pred"))
            out.append(badge(e["status"], "status"))
            out.append("</div></div>")
        out.append("</div>")

    out.append('<div class=foot>Generated by <a href="https://github.com/t1djani/war-room">war-room</a> — '
               "the strategy that wins, and what would make it lose.</div>")
    out.append("</div></body></html>")
    return "".join(out)


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: render-dossier.py <dossier-file> [\"Decision title\"]\n")
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()
    title = sys.argv[2] if len(sys.argv) > 2 else "War-room dossier"
    sys.stdout.write(render(parse_dossier(text), title))


if __name__ == "__main__":
    main()
