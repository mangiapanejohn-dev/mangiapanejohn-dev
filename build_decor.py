#!/usr/bin/env python3
"""Decorative-only SVGs: theme-adaptive cream/charcoal ø + Fraunces hero and section-header bands."""
import base64, pathlib
root = pathlib.Path(__file__).parent
FONT = base64.b64encode((root/"assets/fonts/fraunces-700.woff2").read_bytes()).decode()
W, PAD = 1200, 60
SERIF="'Fraunces',Georgia,'Times New Roman',serif"
SANS ="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO ="'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
THEMES={
 "light":dict(bg="#F0EEE6",border="#E1DCCE",ink="#1F1E1D",sub="#57544E",body="#3A3833",clay="#CC785C",meta="#8A8078",wm="#E7E2D6"),
 "dark": dict(bg="#262624",border="#3A3835",ink="#F5F2EA",sub="#B7B4A8",body="#C9C6BD",clay="#D98E6F",meta="#9A968C",wm="#2E2C29"),
}
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def style(): return (f"<style>@font-face{{font-family:'Fraunces';font-style:normal;font-weight:700;"
                     f"src:url(data:font/woff2;base64,{FONT}) format('woff2');}}</style>")
def oe(cx,cy,fill,r,sw):
    d=r+sw*0.55
    return (f'<g transform="translate({cx} {cy})"><circle r="{r}" fill="none" stroke="{fill}" stroke-width="{sw}"/>'
            f'<line x1="{-d}" y1="{d}" x2="{d}" y2="{-d}" stroke="{fill}" stroke-width="{sw}" stroke-linecap="round"/></g>')
def wrap(t,mc):
    out,cur=[],""
    for w in t.split():
        if len(cur)+len(w)+(1 if cur else 0)<=mc: cur=(cur+" "+w).strip()
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out
def svg(H,inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">'
            f'<defs>{style()}<clipPath id="c"><rect width="{W}" height="{H}" rx="26"/></clipPath></defs>{inner}</svg>\n')
def frame(t,H,extra=""):
    return (f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{t["bg"]}"/>{extra}</g>'
            f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="24.5" fill="none" stroke="{t["border"]}" stroke-width="3"/>')

INTRO=("Mark Ellington — call me Marc, BUG, or ø. A vibe coder (a.k.a. silicon-based biological nutritionist) who "
       "feeds AI agents personality, memory, and the occasional bad idea, then pushes most of it to GitHub for you "
       "to fork and remix. I work solo, ship fast, and travel a lot.")
def hero(t):
    H=300
    inner=frame(t,H,oe(1050,150,t["wm"],118,30))
    inner+=oe(110,150,t["clay"],46,13)
    inner+=(f'<text x="200" y="118" font-family="{SERIF}" font-size="96" font-weight="700" fill="{t["ink"]}">Marc</text>')
    inner+=(f'<text x="204" y="162" font-family="{SANS}" font-size="26" font-weight="600" letter-spacing="0.3" '
            f'fill="{t["sub"]}">Founder &amp; Builder &#160;&#183;&#160; 15 &#160;&#183;&#160; Earthlings</text>')
    y=206
    for ln in wrap(INTRO,112):
        inner+=f'<text x="204" y="{y}" font-family="{SANS}" font-size="18" fill="{t["body"]}">{esc(ln)}</text>'; y+=27
    return svg(H,inner)

def band(title,t):
    H=94
    inner=frame(t,H,oe(1052,H/2,t["wm"],66,17))
    inner+=oe(PAD+16,H/2,t["clay"],16,6)
    inner+=(f'<text x="{PAD+48}" y="{H/2+15}" font-family="{SERIF}" font-size="40" font-weight="700" '
            f'fill="{t["ink"]}">{esc(title)}</text>')
    return svg(H,inner)

BANDS={
 "recently-shipped":"Recently shipped",
 "currently-shipping":"Currently shipping",
 "claude-ecosystem":"In the Claude ecosystem",
 "building-toward":"What I'm building toward",
 "by-the-numbers":"By the numbers",
 "stack":"Stack",
}
import xml.dom.minidom as M
def write(name,fn):
    for th,t in THEMES.items():
        s=fn(t); (root/f"assets/{name}-{th}.svg").write_text(s); M.parseString(s)
write("hero",hero)
for slug,title in BANDS.items():
    write(f"band-{slug}",(lambda title: (lambda t: band(title,t)))(title))
print("generated hero + 6 bands (light+dark), all valid XML")
