#!/usr/bin/env python3
"""Generate cream/charcoal Claude-style SVG panels (light + dark) for the profile."""
import base64, pathlib
root = pathlib.Path(__file__).parent
FONT = base64.b64encode((root/"assets/fonts/fraunces-700.woff2").read_bytes()).decode()

W, PAD = 1200, 58
SERIF = "'Fraunces',Georgia,'Times New Roman',serif"
SANS  = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO  = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

THEMES = {
 "light": dict(bg="#F0EEE6", border="#E1DCCE", ink="#1F1E1D", body="#3A3833",
               clay="#CC785C", meta="#8A8078", wm="#E7E2D6"),
 "dark":  dict(bg="#262624", border="#3A3835", ink="#F5F2EA", body="#C9C6BD",
               clay="#D98E6F", meta="#9A968C", wm="#2E2C29"),
}

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def style(): return (f"<style>@font-face{{font-family:'Fraunces';font-style:normal;"
                     f"font-weight:700;src:url(data:font/woff2;base64,{FONT}) format('woff2');}}</style>")

def oe(cx, cy, fill, r, sw):
    d = r + sw*0.55
    return (f'<g transform="translate({cx} {cy})"><circle r="{r}" fill="none" stroke="{fill}" '
            f'stroke-width="{sw}"/><line x1="{-d}" y1="{d}" x2="{d}" y2="{-d}" stroke="{fill}" '
            f'stroke-width="{sw}" stroke-linecap="round"/></g>')

def wrap(text, maxc):
    out, cur = [], ""
    for w in text.split():
        if len(cur)+len(w)+(1 if cur else 0) <= maxc: cur = (cur+" "+w).strip()
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

def svg(H, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">'
            f'<defs>{style()}<clipPath id="c"><rect width="{W}" height="{H}" rx="26"/></clipPath></defs>{inner}</svg>\n')

def frame(t, H, extra=""):
    return (f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{t["bg"]}"/>{extra}</g>'
            f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="24.5" fill="none" '
            f'stroke="{t["border"]}" stroke-width="3"/>')

def band(title, t):
    H = 96
    inner = frame(t, H, oe(1050, H/2, t["wm"], r=70, sw=18))
    inner += oe(PAD+16, H/2, t["clay"], r=16, sw=6)
    inner += (f'<text x="{PAD+48}" y="{H/2+15}" font-family="{SERIF}" font-size="42" '
              f'font-weight="700" fill="{t["ink"]}">{esc(title)}</text>')
    return svg(H, inner)

def project(name, meta, desc, t):
    lines = wrap(desc, 98)
    top, lh = 40, 28
    y_name = top + 30
    y_body0 = y_name + 40
    y_meta = y_body0 + len(lines)*lh + 12
    H = y_meta + 34
    inner = frame(t, H)
    inner += (f'<text x="{PAD}" y="{y_name}" font-family="{SERIF}" font-size="32" '
              f'font-weight="700" fill="{t["ink"]}">{esc(name)}</text>')
    y = y_body0
    for ln in lines:
        inner += (f'<text x="{PAD}" y="{y}" font-family="{SANS}" font-size="19" '
                  f'fill="{t["body"]}">{esc(ln)}</text>')
        y += lh
    inner += (f'<text x="{PAD}" y="{y_meta}" font-family="{MONO}" font-size="16" '
              f'fill="{t["clay"]}">{esc(meta)}</text>')
    return svg(H, inner)

def manifesto(t):
    title = "What I'm building toward"
    rows = [
        "Agents that read less like tools and more like collaborators",
        "Memory that lets a personality persist, grow, and hold a grudge",
        "Communities where young builders ship instead of doomscroll",
        "Products with the taste of Linear and the depth of Anthropic",
    ]
    tags = "AI Agents  ·  Human-AI Interaction  ·  Product Design  ·  Startups  ·  Open Source  ·  Communities"
    top, lh = 40, 40
    y_title = top + 30
    y0 = y_title + 46
    y_tags = y0 + len(rows)*lh + 20
    H = y_tags + 34
    inner = frame(t, H, oe(1050, H/2, t["wm"], r=70, sw=18))
    inner += oe(PAD+16, y_title-12, t["clay"], r=16, sw=6)
    inner += (f'<text x="{PAD+48}" y="{y_title}" font-family="{SERIF}" font-size="40" '
              f'font-weight="700" fill="{t["ink"]}">{esc(title)}</text>')
    y = y0
    for r in rows:
        inner += (f'<text x="{PAD}" y="{y}" font-family="{MONO}" font-size="20" fill="{t["clay"]}">&#8594;</text>'
                  f'<text x="{PAD+40}" y="{y}" font-family="{SANS}" font-size="20" fill="{t["ink"]}">{esc(r)}</text>')
        y += lh
    inner += (f'<text x="{PAD}" y="{y_tags}" font-family="{MONO}" font-size="15.5" '
              f'fill="{t["meta"]}">{esc(tags)}</text>')
    return svg(H, inner)

BANDS = ["Recently shipped", "Currently shipping", "In the Claude ecosystem", "By the numbers", "Stack"]
def slug(s):
    return s.lower().replace("'", "").replace("—","").replace("  "," ").strip().replace(" ", "-")

PROJECTS = {
 "quotalens": ("QuotaLens", "->  Swift  ·  macOS  ·  ★ 172  ·  brew install --cask quotalens",
    "A macOS menu-bar gauge for Claude & Codex usage — designed, built and open-sourced in a single weekend. Multiple accounts via setup-token, authoritative rate-limit probes, and a ranged statistics window with a smooth trend chart."),
 "imagegen": ("claude-imagegen", "->  Python  ·  Claude Code  ·  gpt-image-2",
    "Gives Claude Code image-generation superpowers — a gpt-image-2 wrapper with transparent cutouts and a one-command /image-c key setup. Ship visuals without ever leaving the terminal."),
 "pawly": ("Pawly · AI Desktop Pet", "->  Desktop  ·  Code Agents  ·  Human-AI  ·  private beta",
    "A desktop companion that quietly drives Claude Code, Codex & Gemini CLI in the background. It handles the agent orchestration; you handle looking unbothered while four terminals do your bidding."),
 "resonix": ("Resonix · AI Personality Engine", "->  Dynamic Persona  ·  Multi-layer Memory  ·  ★ 31",
    "Personality as a reasoning parameter, not a coat of paint over a prompt. Resonix runs dynamic personas on a multi-layer memory architecture (working context, long-term recall, persistent cache), so an agent stays itself across sessions."),
 "horizon": ("Horizon-AI · 72-Hour Startup Camp", "->  Startup  ·  Youth  ·  Social Impact  ·  private beta",
    "Three days, one company, a legally questionable amount of coffee. A pressure cooker for young founders who treat ship it as a personality trait — idea to pitch before the weekend ends."),
 "discorverx": ("DiscorverX · Student Community", "->  Community  ·  Social  ·  Students  ·  private beta",
    "X × Discord × Reddit, rebuilt for students — the home feed you'll eventually blame for your GPA and keep opening anyway. Built for the people actually in the group chat."),
}

def write_pair(name, fn):
    for theme, t in THEMES.items():
        (root/f"assets/{name}-{theme}.svg").write_text(fn(t))

for b in BANDS:
    write_pair(f"band-{slug(b)}", (lambda title: (lambda t: band(title, t)))(b))
for key, (nm, meta, desc) in PROJECTS.items():
    write_pair(f"proj-{key}", (lambda nm=nm, meta=meta, desc=desc: (lambda t: project(nm, meta, desc, t)))())
write_pair("building", manifesto)

import xml.dom.minidom as M
count = 0
for f in sorted(root.glob("assets/*.svg")):
    M.parse(str(f)); count += 1
print(f"generated + validated {count} svg files")
print("bands:", [slug(b) for b in BANDS])
