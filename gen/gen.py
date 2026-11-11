"""Generates the custom animated SVG assets for the Sr1ya profile README.
Every asset is produced in a dark and a light variant."""
import os, textwrap, math, random
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

SANS = "'Segoe UI', 'Inter', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, 'DejaVu Sans Mono', monospace"

THEMES = {
    "dark": dict(
        bg="#070b14", bg2="#0d1424", panel="#0f172a", border="#1e293b",
        text="#e2e8f0", muted="#94a3b8", faint="#334155", grid="#ffffff",
        gridop="0.035", c1="#00c6ff", c2="#7c3aed", c3="#f472b6", ok="#22c55e",
        warn="#facc15", glowop="0.55", chip="#111c33",
    ),
    "light": dict(
        bg="#f8fafc", bg2="#eef2ff", panel="#ffffff", border="#e2e8f0",
        text="#0f172a", muted="#475569", faint="#cbd5e1", grid="#0f172a",
        gridop="0.05", c1="#0284c7", c2="#7c3aed", c3="#db2777", ok="#16a34a",
        warn="#ca8a04", glowop="0.22", chip="#f1f5f9",
    ),
}


def write(name, theme, svg):
    with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w") as f:
        f.write(svg)


def wrap(text, width_px, size, factor=0.53):
    chars = max(10, int(width_px / (size * factor)))
    return textwrap.wrap(text, chars)


# ───────────────────────────── HERO ─────────────────────────────
def hero(t, T):
    W, H = 1200, 400
    rnd = random.Random(7)
    # neural net on the right
    layers = [3, 5, 5, 4, 2]
    x0, x1 = 760, 1130
    nodes = []
    for li, n in enumerate(layers):
        x = x0 + (x1 - x0) * li / (len(layers) - 1)
        span = 220 if n > 1 else 0
        for ni in range(n):
            y = 200 - span / 2 + (span * ni / (n - 1) if n > 1 else 0)
            nodes.append((li, ni, x, y))
    edges, k = [], 0
    for (l1, i1, xa, ya) in nodes:
        for (l2, i2, xb, yb) in nodes:
            if l2 == l1 + 1:
                d = 1.6 + rnd.random() * 2.2
                delay = rnd.random() * 3
                op = 0.18 + rnd.random() * 0.25
                edges.append(
                    f'<line x1="{xa:.0f}" y1="{ya:.0f}" x2="{xb:.0f}" y2="{yb:.0f}" stroke="url(#edge)" stroke-width="1.2" opacity="{op:.2f}"/>'
                    f'<line class="pulse" x1="{xa:.0f}" y1="{ya:.0f}" x2="{xb:.0f}" y2="{yb:.0f}" stroke="{T["c1"]}" stroke-width="2" '
                    f'style="animation-duration:{d:.2f}s;animation-delay:{delay:.2f}s"/>'
                )
                k += 1
    circles = []
    for (li, ni, x, y) in nodes:
        delay = rnd.random() * 2.5
        col = [T["c1"], T["c2"], T["c3"], T["c2"], T["c1"]][li]
        circles.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="{col}" opacity="0.12" class="halo" style="animation-delay:{delay:.2f}s"/>'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6.5" fill="{T["panel"]}" stroke="{col}" stroke-width="2.2"/>'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.6" fill="{col}" class="core" style="animation-delay:{delay:.2f}s"/>'
        )
    # floating particles
    parts = []
    for i in range(26):
        x, y = rnd.randint(20, 1180), rnd.randint(20, 380)
        r = rnd.choice([1, 1.2, 1.6, 2])
        d = 6 + rnd.random() * 8
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{rnd.choice([T["c1"], T["c2"], T["c3"]])}" class="float" '
            f'style="animation-duration:{d:.1f}s;animation-delay:-{rnd.random()*d:.1f}s"/>'
        )

    roles = ["AI / GenAI Engineer", "Agent Systems Builder", "LLM Fine-Tuner", "Forecasting & MLOps"]
    # rotating role text: each visible for 3s in a 12s cycle
    role_txt = "".join(
        f'<text x="64" y="252" class="role" style="animation-delay:{i*3}s">{esc(r)}</text>'
        for i, r in enumerate(roles)
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Sriya — AI / GenAI Engineer">
<defs>
  <linearGradient id="title" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="{T["c1"]}"/><stop offset="0.5" stop-color="{T["c2"]}"/><stop offset="1" stop-color="{T["c3"]}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-0.6 0;0.6 0;-0.6 0" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="title2" x1="0" x2="1" spreadMethod="reflect">
    <stop offset="0" stop-color="{T["c1"]}"/><stop offset="0.5" stop-color="{T["c2"]}"/><stop offset="1" stop-color="{T["c3"]}"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{T["c1"]}"/><stop offset="1" stop-color="{T["c2"]}"/></linearGradient>
  <radialGradient id="g1"><stop offset="0" stop-color="{T["c2"]}" stop-opacity="{T["glowop"]}"/><stop offset="1" stop-color="{T["c2"]}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2"><stop offset="0" stop-color="{T["c1"]}" stop-opacity="{T["glowop"]}"/><stop offset="1" stop-color="{T["c1"]}" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{T["grid"]}" stroke-opacity="{T["gridop"]}"/></pattern>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="22"/></clipPath>
  <style>
    .float {{ animation: drift linear infinite; }}
    @keyframes drift {{ 0% {{ transform: translateY(0); opacity:0 }} 15% {{ opacity:.8 }} 85% {{ opacity:.8 }} 100% {{ transform: translateY(-60px); opacity:0 }} }}
    .pulse {{ stroke-dasharray: 10 400; stroke-dashoffset: 410; animation: flow linear infinite; stroke-linecap: round; }}
    @keyframes flow {{ to {{ stroke-dashoffset: 0 }} }}
    .halo {{ transform-box: fill-box; transform-origin: center; animation: halo 2.6s ease-in-out infinite; }}
    @keyframes halo {{ 0%,100% {{ transform: scale(.6); opacity:.05 }} 50% {{ transform: scale(1.5); opacity:.28 }} }}
    .core {{ animation: core 2.6s ease-in-out infinite; }}
    @keyframes core {{ 0%,100% {{ opacity:.35 }} 50% {{ opacity:1 }} }}
    .hi {{ font: 500 22px {MONO}; fill: {T["muted"]}; }}
    .name {{ font: 800 104px {SANS}; letter-spacing: -3px; }}
    .role {{ font: 600 30px {SANS}; fill: {T["text"]}; opacity: 0; animation: role 12s infinite; }}
    @keyframes role {{ 0% {{ opacity:0; transform: translateY(10px) }} 3%,22% {{ opacity:1; transform: translateY(0) }} 25%,100% {{ opacity:0; transform: translateY(-10px) }} }}
    .tag {{ font: 500 15px {MONO}; fill: {T["muted"]}; }}
    .cmd {{ font: 500 17px {MONO}; fill: {T["text"]}; }}
    .cursor {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0 }} }}
    .type {{ animation: type 3.2s steps(46) .6s backwards; }}
    @keyframes type {{ from {{ clip-path: inset(0 100% 0 0) }} to {{ clip-path: inset(0 0 0 0) }} }}
    .scan {{ animation: scan 6s ease-in-out infinite; }}
    @keyframes scan {{ 0%,100% {{ transform: translateX(-200px) }} 50% {{ transform: translateX(1300px) }} }}
  </style>
</defs>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="{T["bg"]}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <circle cx="960" cy="120" r="320" fill="url(#g1)"/>
  <circle cx="160" cy="380" r="300" fill="url(#g2)"/>
  {"".join(parts)}
  <g>{"".join(edges)}</g>
  <g>{"".join(circles)}</g>
  <text x="64" y="104" class="hi">&gt; hello_world(<tspan fill="{T["c3"]}">"I'm"</tspan>)</text>
  <text x="58" y="206" class="name" fill="url(#title)">Sriya</text>
  {role_txt}
  <rect x="64" y="290" width="560" height="44" rx="10" fill="{T["panel"]}" stroke="{T["border"]}"/>
  <text x="84" y="318" class="cmd"><tspan fill="{T["ok"]}">$</tspan> <tspan class="type">let the model explain; let the code decide</tspan><tspan class="cursor" fill="{T["c1"]}">▌</tspan></text>
  <text x="64" y="368" class="tag">agents · llms · multimodal rag · forecasting · mlops</text>
  <rect class="scan" x="0" y="0" width="140" height="{H}" fill="url(#title2)" opacity="0.035"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="21" fill="none" stroke="url(#title2)" stroke-opacity="0.6" stroke-width="2"/>
</g>
</svg>'''
    write("hero", t, svg)


# ───────────────────────────── TERMINAL ─────────────────────────────
def terminal(t, T):
    W = 1200
    lines = [
        ("cmd", "whoami"),
        ("out", [("AI / GenAI Engineer", T["text"]), ("  ·  ", T["faint"]), ("agents · LLMs · multimodal RAG · forecasting · MLOps", T["muted"])]),
        ("cmd", "cat now.md"),
        ("out", [("▸ ", T["c1"]), ("Building AI products & automation at ", T["text"]), ("ZyFlux LLP", T["c1"])]),
        ("out", [("▸ ", T["c1"]), ("Going deep on ", T["text"]), ("LLM evals · guardrails · agent memory", T["c3"])]),
        ("cmd", "cat principles.md"),
        ("out", [("“", T["c2"]), ("LLMs reason and explain. Decisions live in deterministic, auditable code.", T["text"]), ("”", T["c2"])]),
        ("cmd", "git log --oneline career/"),
        ("out", [("a3f9c21 ", T["warn"]), ("AI Engineer", T["text"]), (" @ ZyFlux LLP", T["c1"]), ("2026 → now", T["muted"], 560)]),
        ("out", [("7b2e0d4 ", T["warn"]), ("AI Engineer", T["text"]), (" @ LedgerPe", T["c1"]), ("2025 → 2026", T["muted"], 560)]),
        ("out", [("1c8a5f0 ", T["warn"]), ("GenAI Engineer", T["text"]), (" @ StartCoding AI", T["c1"]), ("2025", T["muted"], 560)]),
        ("out", [("0d4e7a9 ", T["warn"]), ("B.E. in AI & ML", T["text"]), ("2020 → 2024", T["muted"], 560)]),
        ("cmd", "ls achievements/"),
        ("out", [("★ ", T["warn"]), ("infra-pulse.hackathon-winner", T["text"]), ("   ★ ", T["warn"]), ("llama-3.1-8b.finetune → huggingface", T["text"])]),
    ]
    lh, top = 30, 92
    H = top + lh * len(lines) + 44
    rows = []
    for i, (kind, content) in enumerate(lines):
        y = top + i * lh
        delay = 0.35 + i * 0.32
        if kind == "cmd":
            body = (f'<tspan fill="{T["ok"]}">sriya@github</tspan><tspan fill="{T["muted"]}">:</tspan>'
                    f'<tspan fill="{T["c1"]}">~</tspan><tspan fill="{T["muted"]}">$ </tspan>'
                    f'<tspan fill="{T["text"]}" font-weight="700">{esc(content)}</tspan>')
        else:
            body = "".join((f'<tspan x="{p[2]}" fill="{p[1]}">{esc(p[0])}</tspan>' if len(p) == 3 else f'<tspan fill="{p[1]}">{esc(p[0])}</tspan>') for p in content)
        rows.append(f'<text x="44" y="{y}" class="ln" style="animation-delay:{delay:.2f}s" xml:space="preserve">{body}</text>')
    last_y = top + len(lines) * lh
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="About Sriya terminal">
<defs>
  <linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="{T["c1"]}"/><stop offset=".5" stop-color="{T["c2"]}"/><stop offset="1" stop-color="{T["c3"]}"/></linearGradient>
  <style>
    .ln {{ font: 500 16.5px {MONO}; animation: in .35s ease-out backwards; }}
    @keyframes in {{ from {{ opacity:0; transform: translateX(-8px) }} to {{ opacity:1; transform: none }} }}
    .cur {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 0%,49% {{ opacity: 1 }} 50%,100% {{ opacity: 0 }} }}
    .ttl {{ font: 600 14px {MONO}; fill: {T["muted"]}; }}
  </style>
</defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{T["panel"]}" stroke="url(#bd)" stroke-width="2"/>
<path d="M1 52H{W-1}" stroke="{T["border"]}"/>
<rect x="2" y="2" width="{W-4}" height="49" rx="15" fill="{T["bg2"]}" opacity="0.6"/>
<circle cx="30" cy="27" r="7" fill="#ff5f57"/><circle cx="54" cy="27" r="7" fill="#febc2e"/><circle cx="78" cy="27" r="7" fill="#28c840"/>
<text x="{W/2}" y="32" text-anchor="middle" class="ttl">sriya@github: ~/about — zsh</text>
{"".join(rows)}
<text x="44" y="{last_y}" class="ln" style="animation-delay:{0.35 + len(lines)*0.32:.2f}s"><tspan fill="{T["ok"]}">sriya@github</tspan><tspan fill="{T["muted"]}">:</tspan><tspan fill="{T["c1"]}">~</tspan><tspan fill="{T["muted"]}">$ </tspan></text>
<rect class="cur" x="{44 + 9.9*16:.0f}" y="{last_y-16}" width="10" height="20" fill="{T["c1"]}"/>
</svg>'''
    write("terminal", t, svg)


# ───────────────────────────── SECTION HEADER ─────────────────────────────
def section(t, T, slug, num, title, sub):
    W, H = 1200, 84
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">
<defs>
  <linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{T["c1"]}"/><stop offset=".5" stop-color="{T["c2"]}"/><stop offset="1" stop-color="{T["c3"]}" stop-opacity="0"/></linearGradient>
  <linearGradient id="tg" x1="0" x2="1"><stop offset="0" stop-color="{T["c1"]}"/><stop offset="1" stop-color="{T["c2"]}"/></linearGradient>
  <style>
    .n {{ font: 600 15px {MONO}; fill: {T["c1"]}; letter-spacing: 2px; }}
    .t {{ font: 800 34px {SANS}; fill: {T["text"]}; letter-spacing: -0.5px; }}
    .s {{ font: 500 15px {MONO}; fill: {T["muted"]}; }}
    .bar {{ transform-box: fill-box; transform-origin: left center; animation: grow 1.4s cubic-bezier(.2,.8,.2,1) backwards; }}
    @keyframes grow {{ from {{ transform: scaleX(0) }} to {{ transform: scaleX(1) }} }}
    .dot {{ transform-box: view-box; animation: run 3.5s ease-in-out infinite; }}
    @keyframes run {{ 0% {{ transform: translateX(0); opacity:0 }} 10% {{ opacity:1 }} 90% {{ opacity:1 }} 100% {{ transform: translateX(760px); opacity:0 }} }}
  </style>
</defs>
<rect x="0" y="14" width="6" height="52" rx="3" fill="url(#tg)"/>
<text x="24" y="34" class="n">{num} //</text>
<text x="24" y="70" class="t">{esc(title)}</text>
<text x="{W}" y="70" text-anchor="end" class="s">{esc(sub)}</text>
<rect class="bar" x="420" y="56" width="560" height="2" rx="1" fill="url(#l)"/>
<circle class="dot" cx="420" cy="57" r="3.5" fill="{T["c1"]}"/>
</svg>'''
    write(f"sec-{slug}", t, svg)


# ───────────────────────────── PROJECT CARD ─────────────────────────────
def card(t, T, slug, title, badge, badge_col, desc, tags, accent_key, icon):
    W, H = 590, 270
    A = T[accent_key]
    lines = wrap(desc, W - 64, 15.5, 0.5)[:4]
    desc_svg = "".join(f'<text x="32" y="{124 + i*24}" class="d">{esc(l)}</text>' for i, l in enumerate(lines))
    # tag pills
    x, pills = 32, []
    for tg in tags:
        w = len(tg) * 8.0 + 22
        if x + w > W - 32:
            break
        pills.append(f'<rect x="{x:.0f}" y="222" width="{w:.0f}" height="26" rx="13" fill="{A}" fill-opacity="0.12" stroke="{A}" stroke-opacity="0.35"/>'
                     f'<text x="{x + w/2:.0f}" y="240" text-anchor="middle" class="p" fill="{A}">{esc(tg)}</text>')
        x += w + 8
    bw = len(badge) * 8.6 + 24 if badge else 0
    badge_svg = (f'<rect x="{W-32-bw:.0f}" y="30" width="{bw:.0f}" height="26" rx="13" fill="{badge_col}" fill-opacity="0.16" stroke="{badge_col}"/>'
                 f'<text x="{W-32-bw/2:.0f}" y="48" text-anchor="middle" class="b" fill="{badge_col}">{esc(badge)}</text>') if badge else ""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">
<defs>
  <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{A}"/><stop offset=".6" stop-color="{T["border"]}"/><stop offset="1" stop-color="{T["border"]}"/></linearGradient>
  <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="{A}" stop-opacity="0"/><stop offset=".5" stop-color="{A}" stop-opacity=".10"/><stop offset="1" stop-color="{A}" stop-opacity="0"/></linearGradient>
  <radialGradient id="gl" cx="0" cy="0" r="1"><stop offset="0" stop-color="{A}" stop-opacity="{float(T["glowop"])*0.5:.2f}"/><stop offset="1" stop-color="{A}" stop-opacity="0"/></radialGradient>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <style>
    .t {{ font: 800 25px {SANS}; fill: {T["text"]}; letter-spacing: -.3px; }}
    .d {{ font: 400 15.5px {SANS}; fill: {T["muted"]}; }}
    .p {{ font: 600 12.5px {MONO}; }}
    .b {{ font: 700 12.5px {MONO}; letter-spacing: 1px; }}
    .i {{ font: 26px {SANS}; }}
    .sh {{ animation: sh 5s ease-in-out infinite; }}
    @keyframes sh {{ 0% {{ transform: translateX(-300px) }} 60%,100% {{ transform: translateX({W+300}px) }} }}
    .ring {{ transform-box: fill-box; transform-origin: center; animation: spin 10s linear infinite; }}
    @keyframes spin {{ to {{ transform: rotate(360deg) }} }}
  </style>
</defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{T["panel"]}"/>
  <rect width="{W}" height="{H}" fill="url(#gl)"/>
  <rect class="sh" x="0" y="0" width="220" height="{H}" fill="url(#sh)" transform="skewX(-20)"/>
  <rect x="0" y="0" width="{W}" height="4" fill="{A}"/>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="url(#bd)" stroke-width="2"/>
<circle cx="56" cy="62" r="24" fill="{A}" fill-opacity="0.14"/>
<circle class="ring" cx="56" cy="62" r="24" fill="none" stroke="{A}" stroke-width="2" stroke-dasharray="18 10"/>
<g transform="translate(56 62)">{icon(A)}</g>
<text x="96" y="72" class="t">{esc(title)}</text>
{badge_svg}
{desc_svg}
{"".join(pills)}
</svg>'''
    write(f"card-{slug}", t, svg)


# small line icons, drawn centred at 0,0 within ~22px
def ic_pulse(c): return f'<path d="M-12 2H-6L-3 -8L2 10L5 -2L7 2H12" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
def ic_video(c): return f'<rect x="-11" y="-8" width="16" height="16" rx="3" fill="none" stroke="{c}" stroke-width="2.2"/><path d="M5 -3L12 -7V7L5 3Z" fill="{c}"/>'
def ic_id(c): return f'<rect x="-12" y="-9" width="24" height="18" rx="3" fill="none" stroke="{c}" stroke-width="2.2"/><circle cx="-5" cy="-1" r="3" fill="{c}"/><path d="M1 -3H8M1 2H6" stroke="{c}" stroke-width="2" stroke-linecap="round"/>'
def ic_route(c): return f'<circle cx="-9" cy="8" r="3" fill="{c}"/><circle cx="9" cy="-8" r="3" fill="{c}"/><path d="M-9 5V0Q-9 -4 -5 -4H5Q9 -4 9 -5" fill="none" stroke="{c}" stroke-width="2.2"/><path d="M-9 5Q-9 -1 0 0Q9 1 9 -5" fill="none" stroke="{c}" stroke-width="1.4" stroke-dasharray="2 3"/>'
def ic_team(c): return f'<circle cx="0" cy="-6" r="4" fill="{c}"/><circle cx="-10" cy="2" r="3" fill="{c}" opacity=".7"/><circle cx="10" cy="2" r="3" fill="{c}" opacity=".7"/><path d="M-7 10Q0 0 7 10" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>'
def ic_search(c): return f'<circle cx="-3" cy="-3" r="7.5" fill="none" stroke="{c}" stroke-width="2.4"/><path d="M3 3L10 10" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/>'
def ic_llama(c): return f'<path d="M-10 8L-10 -2Q-10 -8 -5 -8L-5 -12M5 -8L5 -12M-5 -8H5Q10 -8 10 -2V8" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/><circle cx="-3" cy="-2" r="1.6" fill="{c}"/><circle cx="3" cy="-2" r="1.6" fill="{c}"/>'
def ic_wave(c): return f'<path d="M-12 0Q-8 -10 -4 0T4 0T12 0" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/><path d="M-12 7Q-8 2 -4 7T4 7T12 7" fill="none" stroke="{c}" stroke-width="1.5" opacity=".6"/>'


CARDS = [
    ("infra-pulse", "Infra-Pulse", "WINNER", "warn",
     "Predicts infrastructure damage before it becomes visible. Prophet + LSTM forecast degradation from trend data; an Ollama layer turns predictions into plain-language maintenance advice, not a bare risk score. Full-stack risk dashboard.",
     ["Prophet", "LSTM", "Ollama", "Time-Series", "Full-Stack"], "c1", ic_pulse),
    ("text-to-video", "Text-to-Video Engine", "NEW", "c3",
     "Turns any website or topic into a narrated, captioned 1080p video. Crawls text, images, audio and video into a multimodal FAISS index (CLIP + Whisper + SSIM frame dedup), Llama 4 on Groq writes the script, MoviePy assembles the MP4.",
     ["CLIP", "Whisper", "FAISS", "Llama 4", "MoviePy"], "c3", ic_video),
    ("kyc-agent", "KYC / Onboarding Agent", "FINTECH", "c2",
     "KYC/KYB agent that uses Claude vision to extract facts from documents, then routes every decision through deterministic, auditable code. LangGraph pipeline, LiteLLM gateway logging cost/latency/tokens, PII-redaction guardrails.",
     ["LangGraph", "Claude Vision", "LiteLLM", "Guardrails"], "c2", ic_id),
    ("routing-agent", "Routing Intelligence Agent", "FINTECH", "c2",
     "Adaptive payment routing that learns provider patterns with rigorous statistics (two-proportion z-tests, hysteresis activation, effect-size floors) and explains every decision in audit-friendly language. Deliberately non-LLM for decisions.",
     ["Python", "Statistics", "FastAPI", "Explainable"], "c1", ic_route),
    ("agency", "AI Services Agency", "", "c1",
     "Multi-agent project intake: a brief flows through CEO, CTO, PM, Lead Dev and Client Success agents, each reading and writing typed state on a shared LangGraph graph to produce strategy, architecture, roadmap and go-to-market.",
     ["LangGraph", "Groq", "Streamlit", "Multi-Agent"], "c2", ic_team),
    ("leadflow", "LeadFlow Agent", "", "c1",
     "Self-hosted lead-gen chat agent that searches X and LinkedIn, curates leads, and remembers targeting criteria across conversations using plain markdown as memory. Sandboxed CLI tool-use through an OpenAI-compatible gateway.",
     ["TypeScript", "LangChain v1", "Agent Memory"], "c3", ic_search),
    ("llama-ft", "Fine-Tuned Llama-3.1-8B", "ON HF", "warn",
     "Instruction fine-tuning of Llama-3.1-8B-Instruct in 4-bit on a domain-specific dataset with Unsloth, trained on a single GPU. The fine-tuned weights are published on Hugging Face for public use.",
     ["Unsloth", "QLoRA", "4-bit", "Hugging Face"], "warn", ic_llama),
    ("emotion", "Multimodal Emotion AI", "", "c1",
     "Emotion and sentiment classifier on the MELD dataset that late-fuses BERT text embeddings, CNN audio features and vision frame features, deployed as an AWS SageMaker endpoint behind a full-stack SaaS app.",
     ["PyTorch", "BERT", "SageMaker", "Multimodal"], "c1", ic_wave),
]


# ───────────────────────────── TECH STACK ─────────────────────────────
STACK = [
    ("GenAI · Agents", "c1", ["LangGraph", "LangChain", "Claude", "OpenAI", "Gemini", "Llama 3 / 4", "Groq", "Ollama", "LiteLLM", "Unsloth"]),
    ("Multimodal · RAG", "c2", ["Pinecone", "FAISS", "CLIP", "Whisper", "Transformers", "OpenCV", "MoviePy", "Hugging Face"]),
    ("ML · Forecasting", "c3", ["PyTorch", "TensorFlow", "scikit-learn", "XGBoost", "Prophet", "LSTM", "Pandas", "NumPy"]),
    ("Backend · Apps", "c1", ["Python", "TypeScript", "FastAPI", "Flask", "Node.js", "Streamlit", "React"]),
    ("Cloud · MLOps", "c2", ["AWS SageMaker", "Docker", "GitHub Actions", "MongoDB", "PostgreSQL", "Linux", "Git"]),
]


def stack(t, T):
    W = 1200
    colw, gap, top = 220, 20, 40
    rows = max(len(i) for _, _, i in STACK)
    H = top + 40 + rows * 40 + 20
    out = []
    n = 0
    for ci, (head, key, items) in enumerate(STACK):
        A = T[key]
        x = 10 + ci * (colw + gap)
        out.append(f'<rect x="{x}" y="{top-24}" width="{colw}" height="{H-top+20}" rx="16" fill="{T["panel"]}" stroke="{T["border"]}"/>')
        out.append(f'<rect x="{x+18}" y="{top-24}" width="{colw-36}" height="3" rx="1.5" fill="{A}"/>')
        out.append(f'<text x="{x+18}" y="{top+12}" class="h" fill="{A}">{esc(head.upper())}</text>')
        for ii, it in enumerate(items):
            y = top + 40 + ii * 40
            d = 0.15 + n * 0.035
            out.append(f'<g>'
                       f'<rect x="{x+12}" y="{y}" width="{colw-24}" height="30" rx="9" fill="{T["chip"]}" stroke="{T["border"]}"/>'
                       f'<circle cx="{x+30}" cy="{y+15}" r="4.5" fill="{A}" class="dt" style="animation-delay:{d*2:.2f}s"/>'
                       f'<text x="{x+44}" y="{y+20}" class="c">{esc(it)}</text></g>')
            n += 1
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">
<defs><style>
  .h {{ font: 700 13px {MONO}; letter-spacing: 1.6px; }}
  .c {{ font: 600 15px {SANS}; fill: {T["text"]}; }}
  .dt {{ animation: beat 2.4s ease-in-out infinite; }}
  @keyframes beat {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:.25 }} }}
</style></defs>
{"".join(out)}
</svg>'''
    write("stack", t, svg)


# ───────────────────────────── FOOTER ─────────────────────────────
def footer(t, T):
    W, H = 1200, 170
    def wave(amp, ph, y, col, op, dur):
        pts = " ".join(f"{x},{y + amp*math.sin((x/W)*2*math.pi*1.5 + ph):.1f}" for x in range(0, W*2 + 1, 20))
        return (f'<g><polygon points="0,{H} {pts} {W*2},{H}" fill="{col}" opacity="{op}">'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;-{W} 0" dur="{dur}s" repeatCount="indefinite"/></polygon></g>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Thanks for visiting">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{T["c1"]}"/><stop offset=".5" stop-color="{T["c2"]}"/><stop offset="1" stop-color="{T["c3"]}"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath>
<style>.q {{ font: 600 20px {MONO}; fill: {T["text"]}; }} .s {{ font: 500 14px {MONO}; fill: {T["muted"]}; }}</style></defs>
<g clip-path="url(#c)">
{wave(14, 0, 100, T["c2"], 0.18, 14)}
{wave(10, 1.5, 112, T["c1"], 0.22, 10)}
{wave(8, 3, 126, "url(#g)", 0.9, 7)}
</g>
<text x="{W/2}" y="44" text-anchor="middle" class="q">thanks for stopping by <tspan fill="{T["c3"]}">♥</tspan></text>
<text x="{W/2}" y="70" text-anchor="middle" class="s">open to collaborations on agents, GenAI products &amp; applied ML</text>
</svg>'''
    write("footer", t, svg)


SECTIONS = [
    ("about", "01", "About me", "~/whoami"),
    ("stack", "02", "Tech stack", "tools i ship with"),
    ("projects", "03", "Featured builds", "agents · genai · ml"),
    ("more", "04", "More projects", "rag · data science · mlops"),
    ("stats", "05", "GitHub activity", "auto-updated daily"),
    ("connect", "06", "Let's connect", "say hi"),
]

for t, T in THEMES.items():
    hero(t, T)
    terminal(t, T)
    stack(t, T)
    footer(t, T)
    for s in SECTIONS:
        section(t, T, *s)
    for slug, title, badge, bkey, desc, tags, akey, icon in CARDS:
        card(t, T, slug, title, badge, T[bkey], desc, tags, akey, icon)
print("ok", len(os.listdir(OUT)))
