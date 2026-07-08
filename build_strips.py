#!/usr/bin/env python3
"""Slice the profile into seamless, individually-clickable cream/charcoal strips (light + dark)."""
import base64, pathlib
root = pathlib.Path(__file__).parent
FONT = base64.b64encode((root/"assets/fonts/fraunces-700.woff2").read_bytes()).decode()
ACH = {a: base64.b64encode((root/f"assets/ach/{a}-72.png").read_bytes()).decode()
       for a in ["pair-extraordinaire","yolo","quickdraw","starstruck"]}

W, PAD = 1200, 66
SERIF="'Fraunces',Georgia,'Times New Roman',serif"
SANS ="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO ="'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
THEMES={
 "light":dict(bg="#F0EEE6",border="#E3DDCF",ink="#22201D",sub="#57544E",body="#3C3A34",clay="#CC785C",meta="#8A8078",chip="#E7E1D4",wm="#E7E2D6"),
 "dark": dict(bg="#262624",border="#3B3936",ink="#F5F2EA",sub="#B7B4A8",body="#CBC8BF",clay="#D98E6F",meta="#9A968C",chip="#302E2B",wm="#2E2C29"),
}
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
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

class Ctx:
    def __init__(self,t): self.t=t; self.P=[]; self.y=0
    def txt(self,x,yy,s,font,size,fill,w=None,sp=None,anchor=None):
        a=f'font-family="{font}" font-size="{size}" fill="{fill}"'
        if w:a+=f' font-weight="{w}"'
        if sp is not None:a+=f' letter-spacing="{sp}"'
        if anchor:a+=f' text-anchor="{anchor}"'
        self.P.append(f'<text x="{x}" y="{yy}" {a}>{esc(s)}</text>')
    def heading(self,title):
        t=self.t; self.P.append(oe(PAD+15,self.y+13,t["clay"],14,5))
        self.txt(PAD+42,self.y+26,title,SERIF,37,t["ink"],w=700); self.y+=56
    def block(self,name,meta,desc):
        t=self.t; self.txt(PAD,self.y+24,name,SERIF,27,t["ink"],w=700); self.y+=52
        for ln in wrap(desc,110): self.txt(PAD,self.y,ln,SANS,18,t["body"]); self.y+=26
        self.y+=8; self.txt(PAD,self.y,meta,MONO,15.5,t["clay"]); self.y+=26
    def chips(self,labels):
        t=self.t; x=PAD; ch=32; gap=9
        for lab in labels:
            wd=int(len(lab)*9.0)+26
            if x+wd>W-PAD: x=PAD; self.y+=ch+gap
            self.P.append(f'<rect x="{x}" y="{self.y}" width="{wd}" height="{ch}" rx="16" fill="{t["chip"]}"/>')
            self.txt(x+wd/2,self.y+ch*0.66,lab,MONO,15,t["body"],anchor="middle"); x+=wd+gap
        self.y+=ch

def render(draw, top_round=False, bot_round=False, watermark=False, toppad=34, botpad=34):
    def one(t):
        c=Ctx(t); c.y=toppad; draw(c); H=int(c.y+botpad)
        if top_round: rect=f'<rect x="0" y="0" width="{W}" height="{H+50}" rx="30" fill="{t["bg"]}"/>'
        elif bot_round: rect=f'<rect x="0" y="-50" width="{W}" height="{H+50}" rx="30" fill="{t["bg"]}"/>'
        else: rect=f'<rect x="0" y="0" width="{W}" height="{H}" fill="{t["bg"]}"/>'
        wm=oe(1092,150,t["wm"],112,28) if watermark else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">'
                f'<defs><style>@font-face{{font-family:\'Fraunces\';font-weight:700;'
                f'src:url(data:font/woff2;base64,{FONT}) format(\'woff2\');}}</style></defs>'
                f'{rect}{wm}{"".join(c.P)}</svg>\n')
    return one(THEMES["light"]), one(THEMES["dark"])

def hero(c):
    t=c.t; y=c.y
    c.txt(PAD+122,y+72,"Marc",SERIF,92,t["ink"],w=700)
    c.P.insert(0,oe(PAD+44,y+40,t["clay"],46,13))
    c.txt(PAD+126,y+116,"Founder & Builder   ·   15   ·   Earthlings",SANS,25,t["sub"],w=600,sp=0.3)
    c.y=y+168
    for ln in wrap("Mark Ellington — call me Marc, or BUG. A vibe coder (a.k.a. silicon-based biological nutritionist) who feeds AI agents personality, memory, and the occasional bad idea, then pushes most of it to GitHub for you to fork and remix. I work solo, ship fast, and travel a lot.",112):
        c.txt(PAD,c.y,ln,SANS,18,t["body"]); c.y+=27

RECENT={
 "quotalens":("QuotaLens","->  Swift · macOS · ★ 172 · brew install --cask quotalens",
   "A macOS menu-bar gauge for Claude & Codex usage — designed, built and open-sourced in a single weekend. Multiple accounts via setup-token, authoritative rate-limit probes, and a ranged statistics window with a smooth trend chart."),
 "imagegen":("claude-imagegen","->  Python · Claude Code · gpt-image-2",
   "Gives Claude Code image-generation superpowers — a gpt-image-2 wrapper with transparent cutouts and a one-command /image-c key setup. Ship visuals without ever leaving the terminal."),
}
SHIP={
 "pawly":("Pawly · AI Desktop Pet","->  Desktop · Code Agents · Human-AI · private beta",
   "A desktop companion that quietly drives Claude Code, Codex & Gemini CLI in the background. It handles the agent orchestration; you handle looking unbothered while four terminals do your bidding."),
 "resonix":("Resonix · AI Personality Engine","->  Dynamic Persona · Multi-layer Memory · ★ 31",
   "Personality as a reasoning parameter, not a coat of paint over a prompt. Resonix runs dynamic personas on a multi-layer memory architecture (working context, long-term recall, persistent cache), so an agent stays itself across sessions."),
 "horizon":("Horizon-AI · 72-Hour Startup Camp","->  Startup · Youth · Social Impact · private beta",
   "Three days, one company, a legally questionable amount of coffee. A pressure cooker for young founders who treat ship it as a personality trait — idea to pitch before the weekend ends."),
 "discorverx":("DiscorverX · Student Community","->  Community · Social · Students · private beta",
   "X × Discord × Reddit, rebuilt for students — the home feed you'll eventually blame for your GPA and keep opening anyway. Built for the people actually in the group chat."),
}
STACK=["TypeScript","JavaScript","Python","Rust","Go","React","Next.js","Tailwind","Vite","Three.js","Node","Bun","Tauri","Electron","Postgres","Supabase","Docker","Vercel","Cloudflare","Git"]
AGENTS=["Claude Code","OpenAI Codex","Gemini CLI","Antigravity","Copilot","Cursor","Ollama","Raycast","Hugging Face","LangChain","Perplexity","MCP","Vercel AI SDK"]

def s_qlens(c): c.heading("Recently shipped"); c.y+=6; c.block(*RECENT["quotalens"])
def s_imagegen(c): c.block(*RECENT["imagegen"])
def s_pawly(c): c.heading("Currently shipping"); c.y+=6; c.block(*SHIP["pawly"])
def s_resonix(c): c.block(*SHIP["resonix"])
def s_hordis(c):
    c.block(*SHIP["horizon"]); c.y+=22; c.block(*SHIP["discorverx"])
def s_eco_build(c):
    t=c.t; c.heading("In the Claude ecosystem")
    c.txt(PAD,c.y,"A large part of what I build plugs straight into Claude — tools, clients, and lists I use every day.",SANS,18,t["body"]); c.y+=40
    c.chips(["QuotaLens","claude-imagegen","-Re-Code","awesome-claude-code","homebrew-tap"]); c.y+=44
    c.heading("What I'm building toward")
    for r in ["Agents that read less like tools and more like collaborators","Memory that lets a personality persist, grow, and hold a grudge","Communities where young builders ship instead of doomscroll","Products with the taste of Linear and the depth of Anthropic"]:
        c.txt(PAD,c.y,"->",MONO,19,t["clay"]); c.txt(PAD+42,c.y,r,SANS,20,t["ink"]); c.y+=38
    c.y+=6; c.txt(PAD,c.y,"AI Agents · Human-AI Interaction · Product Design · Startups · Open Source · Communities",MONO,15,t["meta"])
def s_numbers(c):
    t=c.t; c.heading("By the numbers")
    c.txt(PAD,c.y,"GitHub Followers  ·  QuotaLens ★ 172  ·  Resonix-AG ★ 31  ·  I push to main on Fridays",SANS,19,t["body"]); c.y+=42
    ax,sz=PAD,66
    for key,lab in [("pair-extraordinaire","Pair Extraordinaire"),("yolo","YOLO"),("quickdraw","Quickdraw"),("starstruck","Starstruck ×2")]:
        c.P.append(f'<image x="{ax}" y="{c.y}" width="{sz}" height="{sz}" href="data:image/png;base64,{ACH[key]}"/>')
        c.txt(ax+sz/2,c.y+sz+20,lab,SANS,14,t["meta"],anchor="middle"); ax+=sz+150
    c.y+=sz+30
def s_stack(c):
    t=c.t; c.heading("Stack")
    c.txt(PAD,c.y,"LANGUAGES & FRAMEWORKS",MONO,13,t["meta"],sp=1); c.y+=26; c.chips(STACK); c.y+=24
    c.txt(PAD,c.y,"AI & AGENTS — where I actually live",MONO,13,t["meta"],sp=1); c.y+=26; c.chips(AGENTS); c.y+=34
    c.P.append(f'<line x1="{PAD}" y1="{c.y}" x2="{W-PAD}" y2="{c.y}" stroke="{t["border"]}" stroke-width="2"/>'); c.y+=36
    c.txt(W/2,c.y,"ø   Building my future company one commit at a time  ·  marcyy.me",MONO,15,t["meta"],anchor="middle"); c.y+=16

STRIPS=[
 ("hero",       lambda: render(hero, top_round=True, watermark=True, toppad=74, botpad=40)),
 ("quotalens",  lambda: render(s_qlens, toppad=30)),
 ("imagegen",   lambda: render(s_imagegen)),
 ("pawly",      lambda: render(s_pawly, toppad=30)),
 ("resonix",    lambda: render(s_resonix)),
 ("hordis",     lambda: render(s_hordis)),
 ("ecobuild",   lambda: render(s_eco_build, toppad=30)),
 ("numbers",    lambda: render(s_numbers, toppad=30)),
 ("stack",      lambda: render(s_stack, toppad=30, bot_round=True, botpad=54)),
]
import xml.dom.minidom as M
for name,fn in STRIPS:
    L,D=fn()
    (root/f"assets/s-{name}-light.svg").write_text(L)
    (root/f"assets/s-{name}-dark.svg").write_text(D)
    M.parseString(L); M.parseString(D)
print("generated", len(STRIPS)*2, "strip svgs, all valid")
