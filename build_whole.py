#!/usr/bin/env python3
"""Compose the ENTIRE profile as one continuous cream/charcoal SVG sheet (light + dark)."""
import base64, pathlib
root = pathlib.Path(__file__).parent
FONT = base64.b64encode((root/"assets/fonts/fraunces-700.woff2").read_bytes()).decode()
ACH = {a: base64.b64encode((root/f"assets/ach/{a}-72.png").read_bytes()).decode()
       for a in ["pair-extraordinaire", "yolo", "quickdraw", "starstruck"]}

W, PAD = 1200, 66
SERIF = "'Fraunces',Georgia,'Times New Roman',serif"
SANS  = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO  = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

THEMES = {
 "light": dict(bg="#F0EEE6", border="#E3DDCF", ink="#22201D", sub="#57544E", body="#3C3A34",
               clay="#CC785C", meta="#8A8078", chip="#E7E1D4", wm="#E7E2D6"),
 "dark":  dict(bg="#262624", border="#3B3936", ink="#F5F2EA", sub="#B7B4A8", body="#CBC8BF",
               clay="#D98E6F", meta="#9A968C", chip="#302E2B", wm="#2E2C29"),
}

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

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

INTRO = ("Mark Ellington — call me Marc, or BUG. A vibe coder (a.k.a. silicon-based biological nutritionist) "
         "who feeds AI agents personality, memory, and the occasional bad idea, then pushes most of it to "
         "GitHub for you to fork and remix. I work solo, ship fast, and travel a lot.")

RECENT = [
 ("QuotaLens", "->  Swift · macOS · ★ 172 · brew install --cask quotalens",
  "A macOS menu-bar gauge for Claude & Codex usage — designed, built and open-sourced in a single weekend. Multiple accounts via setup-token, authoritative rate-limit probes, and a ranged statistics window with a smooth trend chart."),
 ("claude-imagegen", "->  Python · Claude Code · gpt-image-2",
  "Gives Claude Code image-generation superpowers — a gpt-image-2 wrapper with transparent cutouts and a one-command /image-c key setup. Ship visuals without ever leaving the terminal."),
]
SHIPPING = [
 ("Pawly · AI Desktop Pet", "->  Desktop · Code Agents · Human-AI · private beta",
  "A desktop companion that quietly drives Claude Code, Codex & Gemini CLI in the background. It handles the agent orchestration; you handle looking unbothered while four terminals do your bidding."),
 ("Resonix · AI Personality Engine", "->  Dynamic Persona · Multi-layer Memory · ★ 31",
  "Personality as a reasoning parameter, not a coat of paint over a prompt. Resonix runs dynamic personas on a multi-layer memory architecture (working context, long-term recall, persistent cache), so an agent stays itself across sessions."),
 ("Horizon-AI · 72-Hour Startup Camp", "->  Startup · Youth · Social Impact · private beta",
  "Three days, one company, a legally questionable amount of coffee. A pressure cooker for young founders who treat ship it as a personality trait — idea to pitch before the weekend ends."),
 ("DiscorverX · Student Community", "->  Community · Social · Students · private beta",
  "X × Discord × Reddit, rebuilt for students — the home feed you'll eventually blame for your GPA and keep opening anyway. Built for the people actually in the group chat."),
]
ECOSYSTEM = ["QuotaLens", "claude-imagegen", "-Re-Code", "awesome-claude-code", "homebrew-tap"]
MANIFESTO = [
 "Agents that read less like tools and more like collaborators",
 "Memory that lets a personality persist, grow, and hold a grudge",
 "Communities where young builders ship instead of doomscroll",
 "Products with the taste of Linear and the depth of Anthropic",
]
STACK = ["TypeScript","JavaScript","Python","Rust","Go","React","Next.js","Tailwind","Vite","Three.js",
         "Node","Bun","Tauri","Electron","Postgres","Supabase","Docker","Vercel","Cloudflare","Git"]
AGENTS = ["Claude Code","OpenAI Codex","Gemini CLI","Antigravity","Copilot","Cursor","Ollama","Raycast",
          "Hugging Face","LangChain","Perplexity","MCP","Vercel AI SDK"]

def build(t):
    P, bg_extra = [], []
    y = 74
    def txt(x, yy, s, font, size, fill, w=None, sp=None, anchor=None):
        a = f'font-family="{font}" font-size="{size}" fill="{fill}"'
        if w: a += f' font-weight="{w}"'
        if sp is not None: a += f' letter-spacing="{sp}"'
        if anchor: a += f' text-anchor="{anchor}"'
        P.append(f'<text x="{x}" y="{yy}" {a}>{esc(s)}</text>')

    # ---- HERO ----
    bg_extra.append(oe(1092, 150, t["wm"], r=112, sw=28))
    P.append(oe(PAD+44, y+40, t["clay"], r=46, sw=13))
    txt(PAD+122, y+72, "Marc", SERIF, 92, t["ink"], w=700)
    txt(PAD+126, y+116, "Founder & Builder   ·   15   ·   Earthlings", SANS, 25, t["sub"], w=600, sp=0.3)
    y += 168
    for ln in wrap(INTRO, 112):
        txt(PAD, y, ln, SANS, 18, t["body"]); y += 27
    y += 26

    def divider():
        nonlocal y
        P.append(f'<line x1="{PAD}" y1="{y}" x2="{W-PAD}" y2="{y}" stroke="{t["border"]}" stroke-width="2"/>')
        y += 40

    def heading(title):
        nonlocal y
        P.append(oe(PAD+15, y+13, t["clay"], r=14, sw=5))
        txt(PAD+42, y+26, title, SERIF, 37, t["ink"], w=700)
        y += 58

    def block(name, meta, desc):
        nonlocal y
        txt(PAD, y+24, name, SERIF, 27, t["ink"], w=700)
        y += 54
        for ln in wrap(desc, 110):
            txt(PAD, y, ln, SANS, 18, t["body"]); y += 26
        y += 8
        txt(PAD, y, meta, MONO, 15.5, t["clay"]); y += 40

    divider(); heading("Recently shipped")
    for n, m, d in RECENT: block(n, m, d)
    y += 4; divider(); heading("Currently shipping")
    for n, m, d in SHIPPING: block(n, m, d)
    y += 4; divider(); heading("In the Claude ecosystem")
    txt(PAD, y, "A large part of what I build plugs straight into Claude — tools, clients, and lists I use every day.", SANS, 18, t["body"]); y += 40

    def chips(labels):
        nonlocal y
        x = PAD; ch = 32; gap = 9
        for lab in labels:
            wd = int(len(lab)*9.0) + 26
            if x + wd > W - PAD: x = PAD; y += ch + gap
            P.append(f'<rect x="{x}" y="{y}" width="{wd}" height="{ch}" rx="16" fill="{t["chip"]}"/>')
            txt(x+wd/2, y+ch*0.66, lab, MONO, 15, t["body"], anchor="middle")
            x += wd + gap
        y += ch + 14

    chips(ECOSYSTEM)
    y += 6; divider(); heading("What I'm building toward")
    for r in MANIFESTO:
        txt(PAD, y, "->", MONO, 19, t["clay"]); txt(PAD+42, y, r, SANS, 20, t["ink"]); y += 38
    y += 6
    txt(PAD, y, "AI Agents · Human-AI Interaction · Product Design · Startups · Open Source · Communities", MONO, 15, t["meta"]); y += 36
    y += 6; divider(); heading("By the numbers")
    txt(PAD, y, "GitHub Followers  ·  QuotaLens ★ 172  ·  Resonix-AG ★ 31  ·  I push to main on Fridays", SANS, 19, t["body"]); y += 42
    # achievements row
    labels = [("pair-extraordinaire","Pair Extraordinaire"),("yolo","YOLO"),("quickdraw","Quickdraw"),("starstruck","Starstruck ×2")]
    ax, sz = PAD, 66
    for key, lab in labels:
        P.append(f'<image x="{ax}" y="{y}" width="{sz}" height="{sz}" href="data:image/png;base64,{ACH[key]}"/>')
        txt(ax+sz/2, y+sz+20, lab, SANS, 14, t["meta"], anchor="middle")
        ax += sz + 150
    y += sz + 44
    y += 6; divider(); heading("Stack")
    txt(PAD, y, "LANGUAGES & FRAMEWORKS", MONO, 13, t["meta"], sp=1); y += 26
    chips(STACK)
    y += 10
    txt(PAD, y, "AI & AGENTS — where I actually live", MONO, 13, t["meta"], sp=1); y += 26
    chips(AGENTS)
    y += 8; divider()
    txt(W/2, y+4, "ø   Building my future company one commit at a time  ·  marcyy.me", MONO, 15, t["meta"], anchor="middle")
    y += 44

    H = y + 20
    body = "".join(P)
    bg = ("".join(bg_extra))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Marc — Founder and Builder">'
            f'<defs><style>@font-face{{font-family:\'Fraunces\';font-style:normal;font-weight:700;'
            f'src:url(data:font/woff2;base64,{FONT}) format(\'woff2\');}}</style>'
            f'<clipPath id="c"><rect width="{W}" height="{H}" rx="30"/></clipPath></defs>'
            f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{t["bg"]}"/>{bg}</g>'
            f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="28.5" fill="none" '
            f'stroke="{t["border"]}" stroke-width="3"/>{body}</svg>\n')

for theme, t in THEMES.items():
    out = build(t)
    (root/f"assets/whole-{theme}.svg").write_text(out)
    print(f"whole-{theme}.svg  {len(out)//1024} KB")
import xml.dom.minidom as M
M.parse(str(root/"assets/whole-light.svg")); M.parse(str(root/"assets/whole-dark.svg"))
print("both valid XML")
