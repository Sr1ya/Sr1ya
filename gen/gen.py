"""Generates the banner for the Sr1ya profile README (dark + light).
Run: python gen/gen.py"""
import os, random

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

SANS = "'Segoe UI', 'Inter', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, 'DejaVu Sans Mono', monospace"

THEMES = {
    "dark": dict(bg="#0d1117", text="#e6edf3", muted="#8b949e", line="#30363d",
                 c1="#00c6ff", c2="#7c3aed", c3="#f472b6"),
    "light": dict(bg="#ffffff", text="#1f2328", muted="#59636e", line="#d1d9e0",
                  c1="#0284c7", c2="#7c3aed", c3="#db2777"),
}


def banner(t, T):
    W, H = 1200, 240
    rnd = random.Random(3)
    # sparse constellation on the right
    pts = [(rnd.randint(760, 1150), rnd.randint(40, 200)) for _ in range(11)]
    edges = []
    for i, (x, y) in enumerate(pts):
        near = sorted(pts, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)[1:3]
        for (u, v) in near:
            edges.append(f'<line x1="{x}" y1="{y}" x2="{u}" y2="{v}" stroke="{T["line"]}" stroke-width="1"/>')
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="3" fill="{[T["c1"], T["c2"], T["c3"]][i % 3]}" class="d" style="animation-delay:{i*0.35:.2f}s"/>'
        for i, (x, y) in enumerate(pts))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Sriya — AI / GenAI Engineer">
<defs>
  <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{T["c1"]}"/><stop offset=".5" stop-color="{T["c2"]}"/><stop offset="1" stop-color="{T["c3"]}"/></linearGradient>
  <style>
    .n {{ font: 700 64px {SANS}; fill: {T["text"]}; letter-spacing: -1.5px; }}
    .r {{ font: 400 22px {SANS}; fill: {T["muted"]}; }}
    .m {{ font: 400 16px {MONO}; fill: {T["muted"]}; }}
    .d {{ animation: p 3.5s ease-in-out infinite; }}
    @keyframes p {{ 0%,100% {{ opacity: .35 }} 50% {{ opacity: 1 }} }}
    .c {{ animation: b 1.1s steps(1) infinite; }}
    @keyframes b {{ 50% {{ opacity: 0 }} }}
  </style>
</defs>
<rect width="{W}" height="{H}" fill="{T["bg"]}"/>
{"".join(edges)}{dots}
<text x="40" y="104" class="n">Sriya</text>
<text x="42" y="146" class="r">AI / GenAI Engineer — agents, LLMs &amp; applied ML</text>
<text x="42" y="196" class="m">let the model explain; let the code decide<tspan class="c" fill="{T["c1"]}"> ▌</tspan></text>
<rect x="40" y="226" width="220" height="3" rx="1.5" fill="url(#g)"/>
</svg>'''
    with open(os.path.join(OUT, f"banner-{t}.svg"), "w") as f:
        f.write(svg)


for t, T in THEMES.items():
    banner(t, T)
print("ok")
