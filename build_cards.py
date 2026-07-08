#!/usr/bin/env python3
"""Rounded cream/charcoal project cards (light + dark), each meant to be wrapped in a link."""
import base64, pathlib
root = pathlib.Path(__file__).parent
FONT = base64.b64encode((root/"assets/fonts/fraunces-700.woff2").read_bytes()).decode()
W, PAD = 1200, 56
SERIF="'Fraunces',Georgia,'Times New Roman',serif"
SANS ="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO ="'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
THEMES={
 "light":dict(bg="#F0EEE6",border="#E1DCCE",ink="#1F1E1D",body="#3A3833",clay="#CC785C",meta="#8A8078"),
 "dark": dict(bg="#262624",border="#3A3835",ink="#F5F2EA",body="#C9C6BD",clay="#D98E6F",meta="#9A968C"),
}
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def style(): return (f"<style>@font-face{{font-family:'Fraunces';font-style:normal;font-weight:700;"
                     f"src:url(data:font/woff2;base64,{FONT}) format('woff2');}}</style>")
def wrap(t,mc):
    out,cur=[],""
    for w in t.split():
        if len(cur)+len(w)+(1 if cur else 0)<=mc: cur=(cur+" "+w).strip()
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out
def project(name, meta, desc, t):
    lines = wrap(desc, 108)
    top, lh = 42, 28
    y_name = top + 30
    y0 = y_name + 40
    y_meta = y0 + len(lines)*lh + 14
    H = int(y_meta + 36)
    P = (f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{t["bg"]}"/></g>'
         f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="24.5" fill="none" stroke="{t["border"]}" stroke-width="3"/>')
    P += f'<text x="{PAD}" y="{y_name}" font-family="{SERIF}" font-size="31" font-weight="700" fill="{t["ink"]}">{esc(name)}</text>'
    y=y0
    for ln in lines:
        P += f'<text x="{PAD}" y="{y}" font-family="{SANS}" font-size="18" fill="{t["body"]}">{esc(ln)}</text>'; y+=lh
    P += f'<text x="{PAD}" y="{y_meta}" font-family="{MONO}" font-size="15.5" fill="{t["clay"]}">{esc(meta)}</text>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(name)}">'
            f'<defs>{style()}<clipPath id="c"><rect width="{W}" height="{H}" rx="26"/></clipPath></defs>{P}</svg>\n')

CARDS={
 "quotalens":("QuotaLens","->  Swift  ·  macOS  ·  ★ 172  ·  brew install --cask quotalens",
   "A macOS menu-bar gauge for Claude & Codex usage — designed, built and open-sourced in a single weekend. Multiple accounts via setup-token, authoritative rate-limit probes, and a ranged statistics window with a smooth trend chart."),
 "imagegen":("claude-imagegen","->  Python  ·  Claude Code  ·  gpt-image-2",
   "Gives Claude Code image-generation superpowers — a gpt-image-2 wrapper with transparent cutouts and a one-command /image-c key setup. Ship visuals without ever leaving the terminal."),
 "pawly":("Pawly  ·  AI Desktop Pet","->  Desktop  ·  Code Agents  ·  Human-AI  ·  private beta",
   "A desktop companion that quietly drives Claude Code, Codex & Gemini CLI in the background. It handles the agent orchestration; you handle looking unbothered while four terminals do your bidding."),
 "resonix":("Resonix  ·  AI Personality Engine","->  Dynamic Persona  ·  Multi-layer Memory  ·  ★ 31",
   "Personality as a reasoning parameter, not a coat of paint over a prompt. Resonix runs dynamic personas on a multi-layer memory architecture (working context, long-term recall, persistent cache), so an agent stays itself across sessions instead of resetting the moment you close the tab."),
 "horizon":("Horizon-AI  ·  72-Hour Startup Camp","->  Startup  ·  Youth  ·  Social Impact  ·  private beta",
   "Three days, one company, a legally questionable amount of coffee. A pressure cooker for young founders who treat ship it as a personality trait — idea to pitch before the weekend ends."),
 "discorverx":("DiscorverX  ·  Student Community","->  Community  ·  Social  ·  Students  ·  private beta",
   "X × Discord × Reddit, rebuilt for students — the home feed you'll eventually blame for your GPA and keep opening anyway. Built for the people actually in the group chat."),
}
import xml.dom.minidom as M
for key,(nm,meta,desc) in CARDS.items():
    for th,t in THEMES.items():
        s=project(nm,meta,desc,t); (root/f"assets/card-{key}-{th}.svg").write_text(s); M.parseString(s)
print("generated", len(CARDS)*2, "card svgs, all valid")
