#!/usr/bin/env python3
import base64, pathlib

root = pathlib.Path(__file__).parent
font_b64 = base64.b64encode((root/"assets/fonts/fraunces-700.woff2").read_bytes()).decode()

# ø — Marc's personal mark: a ring with a diagonal stroke through it
def oe(cx, cy, fill, r=44, sw=13, opacity=1.0):
    d = r + sw * 0.55  # slash pokes slightly beyond the ring, like a real ø
    return (f'<g transform="translate({cx} {cy})" opacity="{opacity}">'
            f'<circle r="{r}" fill="none" stroke="{fill}" stroke-width="{sw}"/>'
            f'<line x1="{-d}" y1="{d}" x2="{d}" y2="{-d}" stroke="{fill}" '
            f'stroke-width="{sw}" stroke-linecap="round"/></g>')

INTRO = [
    "Mark Ellington — call me Marc, or BUG. A vibe coder (a.k.a. silicon-based biological",
    "nutritionist) who feeds AI agents personality, memory, and the occasional bad idea, then",
    "pushes most of it to GitHub for you to fork and remix. I work solo, ship fast, travel a lot.",
]

def hero(bg, border, wm, marc, sub, body, clay="#CC785C"):
    intro_spans = "".join(
        f'<text x="204" y="{206+i*27}" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Helvetica,Arial,sans-serif" '
        f'font-size="18" fill="{body}">{line}</text>'
        for i, line in enumerate(INTRO)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" role="img" aria-label="Marc — Founder and Builder">
  <defs>
    <style>@font-face{{font-family:'Fraunces';font-style:normal;font-weight:700;src:url(data:font/woff2;base64,{font_b64}) format('woff2');}}</style>
    <clipPath id="c"><rect width="1200" height="300" rx="28"/></clipPath>
  </defs>
  <g clip-path="url(#c)">
    <rect width="1200" height="300" fill="{bg}"/>
    {oe(1050, 150, wm, r=118, sw=30)}
  </g>
  <rect x="1.5" y="1.5" width="1197" height="297" rx="26.5" fill="none" stroke="{border}" stroke-width="3"/>
  {oe(110, 150, clay, r=46, sw=13)}
  <text x="200" y="118" font-family="'Fraunces',Georgia,'Times New Roman',serif" font-size="96" font-weight="700" fill="{marc}">Marc</text>
  <text x="204" y="162" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="26" font-weight="600" letter-spacing="0.3" fill="{sub}">Founder &amp; Builder &#160;&#183;&#160; 15 &#160;&#183;&#160; Earthlings</text>
  {intro_spans}
</svg>
'''

light = hero(bg="#F0EEE6", border="#E1DCCE", wm="#E7E2D6", marc="#1F1E1D", sub="#57544E", body="#3A3833")
dark  = hero(bg="#262624", border="#3A3835", wm="#2E2C29", marc="#F5F2EA", sub="#B7B4A8", body="#C9C6BD")

(root/"assets/hero-light.svg").write_text(light)
(root/"assets/hero-dark.svg").write_text(dark)
print("wrote hero-light.svg", len(light), "bytes;  hero-dark.svg", len(dark), "bytes")
