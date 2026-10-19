#!/usr/bin/env python3
"""Generates every SVG used by the profile README, in dark and light variants.

Theme: a U-Space airspace display. Run `python3 build.py` from the repo root;
output goes to assets/dark/ and assets/light/.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).parent
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Inter, Arial, sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', 'JetBrains Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(
        bg0="#070D1A", bg1="#0D1A2F", panel="#0C1628", line="#1C2C46",
        grid="#5EEAD4", grid_op="0.055", text="#E6EDF7", muted="#8A9BB4",
        faint="#4A5B75", accent="#5EEAD4", accent2="#FBBF24", accent3="#A78BFA",
        chip="#13223A", chip_text="#C9D6E8",
    ),
    "light": dict(
        bg0="#F7FAFD", bg1="#E8EFF7", panel="#FFFFFF", line="#D5DFEB",
        grid="#0F766E", grid_op="0.07", text="#0B1626", muted="#4D5E77",
        faint="#94A3B8", accent="#0F766E", accent2="#B45309", accent3="#6D28D9",
        chip="#EEF3F9", chip_text="#24344D",
    ),
}

MONO_W = 0.61  # approximate advance of a monospace glyph, in em
SANS_W = 0.56  # rough average for the sans stack


def e(s):
    return escape(s, {'"': "&quot;"})


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)}">'
        f"<title>{e(title)}</title>{body}</svg>\n"
    )


def drone(t, scale=1.0, color=None):
    """Small top-down quadcopter glyph centred on the origin."""
    c = color or t["accent2"]
    s = scale
    return (
        f'<g transform="scale({s})">'
        f'<line x1="-6" y1="-6" x2="6" y2="6" stroke="{c}" stroke-width="1.6"/>'
        f'<line x1="-6" y1="6" x2="6" y2="-6" stroke="{c}" stroke-width="1.6"/>'
        + "".join(
            f'<circle cx="{x}" cy="{y}" r="3.4" fill="none" stroke="{c}" stroke-width="1.4"/>'
            for x, y in ((-6, -6), (6, -6), (-6, 6), (6, 6))
        )
        + f'<rect x="-2.6" y="-2.6" width="5.2" height="5.2" rx="1.2" fill="{c}"/></g>'
    )


def grid_defs(t, pid, size=40):
    return (
        f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">'
        f'<path d="M {size} 0 L 0 0 0 {size}" fill="none" stroke="{t["grid"]}" '
        f'stroke-opacity="{t["grid_op"]}" stroke-width="1"/></pattern>'
    )


# --------------------------------------------------------------------------- header
def header(t):
    W, H = 1200, 380
    cx, cy = 925, 190
    routes = [
        "M 600 330 C 720 250, 820 260, 900 200 S 1060 90, 1220 70",
        "M 640 40 C 760 110, 860 120, 960 210 S 1110 330, 1220 320",
        "M 1220 190 C 1100 200, 1010 160, 925 190 S 760 250, 610 210",
    ]
    route_svg = ""
    for i, d in enumerate(routes):
        route_svg += (
            f'<path id="r{i}" d="{d}" fill="none" stroke="{t["accent"]}" stroke-opacity="0.35" '
            f'stroke-width="1.4" stroke-dasharray="2 7" stroke-linecap="round">'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-90" dur="{4 + i}s" repeatCount="indefinite"/></path>'
        )
    drones = ""
    for i, (dur, begin) in enumerate(((11, 0), (13, -4), (9, -2))):
        drones += (
            f'<g>{drone(t, 1.05)}'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" rotate="auto">'
            f'<mpath href="#r{i}"/></animateMotion></g>'
        )
    # second wave, more transparent
    for i, (dur, begin) in enumerate(((11, -6), (13, -10))):
        drones += (
            f'<g opacity="0.55">{drone(t, 0.8)}'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" rotate="auto">'
            f'<mpath href="#r{i}"/></animateMotion></g>'
        )
    dash_attr = 'stroke-dasharray="3 6"'
    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["accent"]}" '
        f'stroke-opacity="{op}" stroke-width="1" {dash_attr if dash else ""}/>'
        for r, op, dash in ((52, 0.35, False), (104, 0.25, True), (156, 0.18, False), (208, 0.10, True))
    )
    ticks = "".join(
        f'<line x1="{cx}" y1="{cy - 208}" x2="{cx}" y2="{cy - 200}" stroke="{t["accent"]}" '
        f'stroke-opacity="0.35" transform="rotate({a} {cx} {cy})"/>'
        for a in range(0, 360, 15)
    )
    blips = ""
    for (bx, by, begin) in ((1010, 120, 0.9), (870, 270, 3.6), (1040, 255, 2.4), (845, 130, 4.7)):
        blips += (
            f'<g opacity="0"><circle cx="{bx}" cy="{by}" r="3" fill="{t["accent"]}"/>'
            f'<circle cx="{bx}" cy="{by}" r="3" fill="none" stroke="{t["accent"]}">'
            f'<animate attributeName="r" values="3;14" dur="1.6s" begin="{begin}s;b{bx}.end+4.4s" />'
            f'<animate attributeName="stroke-opacity" values="0.8;0" dur="1.6s" begin="{begin}s;b{bx}.end+4.4s"/></circle>'
            f'<animate id="b{bx}" attributeName="opacity" values="0;1;0" keyTimes="0;0.15;1" dur="1.6s" '
            f'begin="{begin}s;b{bx}.end+4.4s"/></g>'
        )
    waypoints = ""
    for (wx, wy, label) in ((1000, 112, "WP-07"), (760, 255, "WP-03"), (1105, 300, "WP-11")):
        waypoints += (
            f'<rect x="{wx - 4}" y="{wy - 4}" width="8" height="8" fill="none" stroke="{t["muted"]}" '
            f'stroke-width="1.2" transform="rotate(45 {wx} {wy})"/>'
            f'<text x="{wx + 10}" y="{wy + 4}" font-family="{MONO}" font-size="11" fill="{t["muted"]}" '
            f'letter-spacing="1">{label}</text>'
        )
    status = "> modelling fair queues for drones · shipping agents & data pipelines"
    status_w = len(status) * 15 * MONO_W
    body = f"""
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t['bg0']}"/><stop offset="1" stop-color="{t['bg1']}"/>
  </linearGradient>
  <radialGradient id="glow" cx="{cx}" cy="{cy}" r="260" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.13"/>
    <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['accent']}" stop-opacity="0"/>
    <stop offset="1" stop-color="{t['accent']}" stop-opacity="0.32"/>
  </linearGradient>
  <linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['bg0']}" stop-opacity="1"/>
    <stop offset="0.42" stop-color="{t['bg0']}" stop-opacity="0.92"/>
    <stop offset="0.58" stop-color="{t['bg0']}" stop-opacity="0"/>
  </linearGradient>
  {grid_defs(t, 'g')}
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <clipPath id="type"><rect x="64" y="262" width="0" height="26">
    <animate attributeName="width" values="0;{status_w + 20:.0f};{status_w + 20:.0f};0" keyTimes="0;0.38;0.92;1"
      dur="9s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0 0 1 1;0.4 0 0.6 1"/>
  </rect></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#g)"/>
  <circle cx="{cx}" cy="{cy}" r="260" fill="url(#glow)"/>
  {rings}{ticks}
  <line x1="{cx - 220}" y1="{cy}" x2="{cx + 220}" y2="{cy}" stroke="{t['accent']}" stroke-opacity="0.12"/>
  <line x1="{cx}" y1="{cy - 220}" x2="{cx}" y2="{cy + 220}" stroke="{t['accent']}" stroke-opacity="0.12"/>
  <g>
    <path d="M {cx} {cy} L {cx + 208} {cy} A 208 208 0 0 0 {cx + 180} {cy - 104} Z" fill="url(#sweep)"/>
    <line x1="{cx}" y1="{cy}" x2="{cx + 208}" y2="{cy}" stroke="{t['accent']}" stroke-opacity="0.7" stroke-width="1.4"/>
    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="6s" repeatCount="indefinite"/>
  </g>
  {blips}{route_svg}{waypoints}{drones}
  <rect width="{W}" height="{H}" fill="url(#fadeL)"/>

  <g font-family="{MONO}" font-size="12" letter-spacing="2" fill="{t['muted']}">
    <circle cx="70" cy="62" r="5" fill="{t['accent']}">
      <animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="84" y="66">MVC-01 · ONLINE · U-SPACE SECTOR MAD</text>
  </g>
  <text x="62" y="140" font-family="{SANS}" font-size="62" font-weight="700" fill="{t['text']}" letter-spacing="-1.5">Miguel Vera</text>
  <text x="62" y="200" font-family="{SANS}" font-size="62" font-weight="300" fill="{t['text']}" fill-opacity="0.78" letter-spacing="-1.5">del Castillo</text>
  <text x="64" y="240" font-family="{SANS}" font-size="20" fill="{t['muted']}">Data Systems Engineering @ ETSIT-UPM <tspan fill="{t['faint']}">·</tspan> Researcher @ GPDS</text>
  <g clip-path="url(#type)">
    <text x="64" y="281" font-family="{MONO}" font-size="15" fill="{t['accent']}">{e(status)}</text>
  </g>
  <rect x="64" y="266" width="9" height="19" fill="{t['accent']}" opacity="0.8">
    <animate attributeName="x" values="64;{64 + status_w + 8:.0f};{64 + status_w + 8:.0f};64" keyTimes="0;0.38;0.92;1"
      dur="9s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0 0 1 1;0.4 0 0.6 1"/>
    <animate attributeName="opacity" values="0.8;0;0.8" dur="1s" repeatCount="indefinite"/>
  </rect>
  <g font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{t['faint']}">
    <text x="64" y="342">40.4168° N   3.7038° W</text>
    <text x="300" y="342">ALT 657 m</text>
    <text x="420" y="342">FL-QUEUE: FAIR</text>
    <text x="{W - 40}" y="342" text-anchor="end">RANGE 4 NM · SWEEP 6 s</text>
  </g>
  <rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="17.5" fill="none" stroke="{t['line']}" stroke-width="1.5"/>
</g>"""
    return svg(W, H, body, "Miguel Vera del Castillo — Data Systems Engineering at ETSIT-UPM, researcher at GPDS on fairness in U-Space drone traffic")


# --------------------------------------------------------------------------- section titles
def section(t, code, title):
    W, H = 1200, 76
    tw = len(title) * 30 * SANS_W
    x_line = 150 + tw + 30
    body = f"""
<text x="2" y="48" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{t['accent']}">{code}</text>
<text x="104" y="49" font-family="{SANS}" font-size="30" font-weight="650" fill="{t['text']}" letter-spacing="-0.5">{e(title)}</text>
<line x1="{x_line:.0f}" y1="42" x2="{W - 40}" y2="42" stroke="{t['line']}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>
<rect x="{W - 30}" y="37" width="10" height="10" fill="none" stroke="{t['accent']}" stroke-width="1.5" transform="rotate(45 {W - 25} 42)"/>
<g opacity="0.9">{drone(t, 0.9)}
  <animateMotion dur="7s" repeatCount="indefinite" path="M {x_line:.0f} 42 L {W - 46} 42" keyTimes="0;1" keyPoints="0;1" calcMode="spline" keySplines="0.45 0 0.55 1"/>
  <animate attributeName="opacity" values="0;0.9;0.9;0" keyTimes="0;0.1;0.85;1" dur="7s" repeatCount="indefinite"/>
</g>"""
    return svg(W, H, body, title)


# --------------------------------------------------------------------------- cards
def chips(t, items, x, y, size=15, gap=10, max_x=None):
    out, cx = "", x
    for it in items:
        w = len(it) * size * MONO_W + 24
        if max_x and cx + w > max_x:
            break
        out += (
            f'<rect x="{cx:.0f}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="{t["chip"]}" stroke="{t["line"]}"/>'
            f'<text x="{cx + w / 2:.0f}" y="{y + 20}" text-anchor="middle" font-family="{MONO}" font-size="{size}" fill="{t["chip_text"]}">{e(it)}</text>'
        )
        cx += w + gap
    return out


def card_frame(t, W, H, inner, title, accent):
    body = f"""
<defs>{grid_defs(t, 'cg', 32)}
  <linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t['panel']}"/><stop offset="1" stop-color="{t['bg1']}"/>
  </linearGradient>
  <clipPath id="cf"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#cf)">
  <rect width="{W}" height="{H}" fill="url(#cbg)"/>
  <rect width="{W}" height="{H}" fill="url(#cg)"/>
  <rect width="5" height="{H}" fill="{accent}"/>
  {inner}
  <rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="15.5" fill="none" stroke="{t['line']}" stroke-width="1.5"/>
</g>"""
    return svg(W, H, body, title)


def text_lines(lines, x, y, size, fill, lh=None, family=SANS, weight=400):
    lh = lh or size * 1.45
    return "".join(
        f'<text x="{x}" y="{y + i * lh:.0f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}">{e(l)}</text>'
        for i, l in enumerate(lines)
    )


def badge(t, label, x, y, color, size=14, anchor_right=True):
    w = len(label) * size * MONO_W + 28
    bx = x - w if anchor_right else x
    return (
        f'<rect x="{bx:.0f}" y="{y}" width="{w:.0f}" height="30" rx="8" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.55"/>'
        f'<text x="{bx + w / 2:.0f}" y="{y + 20}" text-anchor="middle" font-family="{MONO}" font-size="{size}" letter-spacing="1" fill="{color}">{e(label)}</text>'
    )


def research_card(t):
    W, H = 1200, 330
    # mini fairness chart on the right: target vs inferred profile bars
    bx, by, bw, bh = 820, 70, 330, 190
    target = [0.62, 0.48, 0.71, 0.39, 0.55, 0.66, 0.44]
    inferred = [0.60, 0.50, 0.69, 0.42, 0.53, 0.67, 0.46]
    bars = ""
    n = len(target)
    slot = bw / n
    for i, (a, b) in enumerate(zip(target, inferred)):
        x0 = bx + i * slot + 8
        ha, hb = a * bh, b * bh
        bars += (
            f'<rect x="{x0:.0f}" y="{by + bh - ha:.0f}" width="{slot / 2 - 8:.0f}" height="{ha:.0f}" rx="3" fill="{t["faint"]}" fill-opacity="0.45"/>'
            f'<rect x="{x0 + slot / 2 - 6:.0f}" y="{by + bh:.0f}" width="{slot / 2 - 8:.0f}" height="0" rx="3" fill="{t["accent"]}">'
            f'<animate attributeName="height" values="0;{hb:.0f};{hb:.0f};0" keyTimes="0;0.25;0.9;1" dur="8s" begin="{i * 0.12:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{by + bh};{by + bh - hb:.0f};{by + bh - hb:.0f};{by + bh}" keyTimes="0;0.25;0.9;1" dur="8s" begin="{i * 0.12:.2f}s" repeatCount="indefinite"/></rect>'
        )
    chart = f"""
<rect x="{bx - 24}" y="{by - 44}" width="{bw + 48}" height="{bh + 100}" rx="12" fill="{t['bg0']}" fill-opacity="0.55" stroke="{t['line']}"/>
<text x="{bx}" y="{by - 18}" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{t['muted']}">AUTHORIZATION PROFILE BY OPERATOR</text>
<line x1="{bx}" y1="{by + bh}" x2="{bx + bw}" y2="{by + bh}" stroke="{t['line']}"/>
{bars}
<g font-family="{MONO}" font-size="12" fill="{t['muted']}">
  <rect x="{bx}" y="{by + bh + 20}" width="12" height="12" rx="2" fill="{t['faint']}" fill-opacity="0.45"/>
  <text x="{bx + 20}" y="{by + bh + 31}">target</text>
  <rect x="{bx + 100}" y="{by + bh + 20}" width="12" height="12" rx="2" fill="{t['accent']}"/>
  <text x="{bx + 120}" y="{by + bh + 31}">inferred rules</text>
</g>"""
    inner = f"""
<text x="44" y="56" font-family="{MONO}" font-size="14" letter-spacing="2" fill="{t['accent']}">RESEARCH · GPDS · ETSIT-UPM</text>
{badge(t, 'FIRST AUTHOR · UNDER REVIEW', 760, 34, t['accent2'])}
{text_lines(['Fairness in U-Space flight queues'], 44, 108, 34, t['text'], weight=700)}
{text_lines([
    'Drones request airspace through a shared queue. Who gets to fly first',
    'is a policy choice. I build the simulator and invert it: given the',
    'fairness profile a regulator wants, infer the queue rules that produce it',
    '(neural posterior estimation and an MLP-surrogate search loop).',
], 44, 152, 19, t['muted'], lh=29)}
{chips(t, ['Python', 'PyTorch', 'sbi · NPE', 'TypeScript sim'], 44, 272, max_x=760)}
{chart}"""
    return card_frame(t, W, H, inner, "Research: fairness in U-Space flight queues — first-author paper under review at SESAR Innovation Days 2026", t["accent"])


def project_card(t, tag, title, lines, chip_items, badge_label, badge_color, accent, alt, glyph=""):
    W, H = 600, 330
    inner = f"""
<text x="36" y="52" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{accent}">{e(tag)}</text>
{text_lines([title], 36, 104, 32, t['text'], weight=700)}
{text_lines(lines, 36, 148, 18, t['muted'], lh=27)}
{chips(t, chip_items, 36, 270, size=14, gap=8, max_x=W - 24)}
{badge(t, badge_label, W - 30, 30, badge_color, size=12)}
{glyph}"""
    return card_frame(t, W, H, inner, alt, accent)


def pipedream(t):
    # tiny animated "diff box" glyph: two boxes, a scanning line, check
    g = f"""
<g transform="translate(470 120)" opacity="0.9">
  <rect x="0" y="0" width="44" height="56" rx="4" fill="none" stroke="{t['faint']}" stroke-width="1.4"/>
  <rect x="56" y="0" width="44" height="56" rx="4" fill="none" stroke="{t['faint']}" stroke-width="1.4"/>
  <rect x="8" y="14" width="18" height="12" fill="none" stroke="{t['accent2']}" stroke-width="1.6"/>
  <rect x="64" y="14" width="18" height="12" fill="none" stroke="{t['accent']}" stroke-width="1.6"/>
  <line x1="-4" y1="0" x2="104" y2="0" stroke="{t['accent']}" stroke-opacity="0.8" stroke-width="1.4">
    <animate attributeName="y1" values="0;56;0" dur="3.2s" repeatCount="indefinite"/>
    <animate attributeName="y2" values="0;56;0" dur="3.2s" repeatCount="indefinite"/>
  </line>
</g>"""
    return project_card(
        t, "HACKATHON PROJECT", "PipeDream",
        ["AI validator for P&ID engineering drawings.",
         "Finds every hand-marked correction with",
         "OpenCV, then a vision LLM audits whether",
         "the final version actually applied it."],
        ["FastAPI", "OpenCV", "Azure OpenAI", "React"],
        "1ST · INDESIAHACK 2025", t["accent2"], t["accent2"],
        "PipeDream — winner of IndesIAhack 2025: AI validator for P&ID engineering drawings", g,
    )


def hackkit(t):
    g = f"""
<g transform="translate(470 118)" font-family="{MONO}" font-size="12" fill="{t['muted']}">
  <rect x="0" y="0" width="100" height="64" rx="6" fill="{t['bg0']}" fill-opacity="0.6" stroke="{t['line']}"/>
  <circle cx="12" cy="11" r="3" fill="{t['accent2']}"/><circle cx="22" cy="11" r="3" fill="{t['faint']}"/><circle cx="32" cy="11" r="3" fill="{t['faint']}"/>
  <text x="10" y="36" fill="{t['accent3']}">/hack</text>
  <text x="10" y="53">ready<tspan fill="{t['accent']}">▍<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
</g>"""
    return project_card(
        t, "OPEN SOURCE · CLAUDE CODE PLUGIN", "hackathon-kit",
        ["From challenge statement to first commit:",
         "analysis, approaches, scaffold, team plan",
         "and pitch — plus a live Hackathon OS to",
         "coordinate everyone's agents."],
        ["Claude Code", "agents", "TypeScript", "evals"],
        "v0.4 · MIT", t["accent3"], t["accent3"],
        "hackathon-kit — open-source Claude Code plugin that takes a hackathon team from challenge statement to first commit", g,
    )


# --------------------------------------------------------------------------- flight log (achievements)
def flight_log(t):
    rows = [
        ("2026", "SUBMITTED", "First-author paper · SESAR Innovation Days", t["accent"]),
        ("2026", "AWARDED", "Excellence scholarship · Comunidad de Madrid", t["accent3"]),
        ("2025", "1ST PLACE", "IndesIAhack · Técnicas Reunidas × Bravent challenge", t["accent2"]),
        ("2025", "1ST PLACE", "BeTech Hackathon", t["accent2"]),
        ("2025", "JOINED", "GPDS research group · ETSIT-UPM", t["accent"]),
        ("HIGH SCHOOL", "2× WINNER", "FIRST LEGO League · regional final, Toledo", t["accent3"]),
    ]
    W = 1200
    top, lh = 12, 62
    H = top + lh * len(rows) + 10
    x_line = 196
    body = f'<line x1="{x_line}" y1="{top + 10}" x2="{x_line}" y2="{top + lh * (len(rows) - 1) + 10}" stroke="{t["line"]}" stroke-width="2"/>'
    for i, (year, kind, what, col) in enumerate(rows):
        y = top + i * lh
        body += (
            f'<text x="160" y="{y + 16}" text-anchor="end" font-family="{MONO}" font-size="15" letter-spacing="1.5" fill="{t["muted"]}">{e(year)}</text>'
            f'<circle cx="{x_line}" cy="{y + 10}" r="7" fill="{t["bg0"]}" stroke="{col}" stroke-width="2.2"/>'
            f'<circle cx="{x_line}" cy="{y + 10}" r="2.6" fill="{col}">'
            f'<animate attributeName="opacity" values="0.2;1;0.2" dur="3s" begin="{i * 0.5}s" repeatCount="indefinite"/></circle>'
            f'<text x="232" y="{y + 16}" font-family="{MONO}" font-size="14" letter-spacing="2" fill="{col}">{e(kind)}</text>'
            f'<text x="390" y="{y + 17}" font-family="{SANS}" font-size="21" fill="{t["text"]}">{e(what)}</text>'
            f'<line x1="232" y1="{y + 40}" x2="{W - 40}" y2="{y + 40}" stroke="{t["line"]}" stroke-opacity="0.6" stroke-dasharray="1 5"/>'
        )
    stats = [("8.48", "/10 GPA"), ("7", "Matrículas de Honor"), ("4", "hackathons · 2 wins")]
    # stats live in a strip under the log
    sy = H
    H += 96
    sw = (W - 80 - 2 * 20) / 3
    for i, (num, lab) in enumerate(stats):
        x = 40 + i * (sw + 20)
        body += (
            f'<rect x="{x:.0f}" y="{sy + 12}" width="{sw:.0f}" height="72" rx="12" fill="{t["panel"]}" stroke="{t["line"]}"/>'
            f'<text x="{x + 26:.0f}" y="{sy + 59}" font-family="{SANS}" font-size="34" font-weight="700" fill="{t["text"]}">{num}'
            f'<tspan dx="10" font-size="18" font-weight="400" fill="{t["muted"]}">{e(lab)}</tspan></text>'
        )
    return svg(W, H, body, "Flight log: first-author paper submitted to SESAR Innovation Days 2026; Comunidad de Madrid excellence scholarship 2026; 1st place IndesIAhack 2025; 1st place BeTech Hackathon 2025; joined GPDS 2025; 2x FIRST LEGO League regional winner. GPA 8.48/10, 7 Matrículas de Honor, 4 hackathons with 2 wins.")


# --------------------------------------------------------------------------- stack
def stack(t):
    groups = [
        ("DATA & ML", t["accent"], ["Python", "SQL", "pandas", "NumPy", "PyTorch", "sbi", "Spark", "Kafka", "Airflow", "Jupyter"]),
        ("BACKEND", t["accent2"], ["FastAPI", "Flask", "Django", "PostgreSQL", "MongoDB", "Scala"]),
        ("FRONTEND", t["accent3"], ["TypeScript", "JavaScript", "React"]),
        ("INFRA", t["accent"], ["Docker", "Kubernetes", "Linux", "Bash", "Git"]),
        ("AI TOOLING", t["accent2"], ["Claude Code", "LangGraph", "Azure OpenAI", "agents & evals"]),
    ]
    W = 1200
    lh = 56
    H = 24 + lh * len(groups)
    body = ""
    for i, (name, col, items) in enumerate(groups):
        y = 18 + i * lh
        body += (
            f'<rect x="2" y="{y + 9}" width="8" height="8" fill="{col}" transform="rotate(45 6 {y + 13})"/>'
            f'<text x="24" y="{y + 19}" font-family="{MONO}" font-size="14" letter-spacing="2" fill="{col}">{e(name)}</text>'
            + chips(t, items, 190, y - 1, size=15, gap=10, max_x=W - 4)
        )
    return svg(W, H, body, "Tech stack. Data & ML: " + ", ".join(groups[0][2]) + ". Backend: " + ", ".join(groups[1][2]) + ". Frontend: " + ", ".join(groups[2][2]) + ". Infra: " + ", ".join(groups[3][2]) + ". AI tooling: " + ", ".join(groups[4][2]) + ".")


# --------------------------------------------------------------------------- buttons
def button(t, label, icon):
    size = 15
    w = int(len(label) * size * MONO_W + 70)
    H = 44
    icons = {
        "in": f'<rect x="18" y="13" width="18" height="18" rx="4" fill="{t["accent"]}"/>'
              f'<text x="27" y="27" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" fill="{t["bg0"]}">in</text>',
        "mail": f'<rect x="17" y="14" width="20" height="15" rx="2.5" fill="none" stroke="{t["accent"]}" stroke-width="1.8"/>'
                f'<path d="M 18 16 L 27 23 L 36 16" fill="none" stroke="{t["accent"]}" stroke-width="1.8"/>',
        "doc": f'<path d="M 19 12 h 11 l 6 6 v 14 h -17 z" fill="none" stroke="{t["accent"]}" stroke-width="1.8"/>'
               f'<line x1="23" y1="22" x2="32" y2="22" stroke="{t["accent"]}" stroke-width="1.6"/>'
               f'<line x1="23" y1="27" x2="32" y2="27" stroke="{t["accent"]}" stroke-width="1.6"/>',
    }
    body = (
        f'<rect x="1" y="1" width="{w - 2}" height="{H - 2}" rx="10" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
        + icons[icon]
        + f'<text x="50" y="28" font-family="{MONO}" font-size="{size}" letter-spacing="1" fill="{t["text"]}">{e(label)}</text>'
    )
    return svg(w, H, body, label)


# --------------------------------------------------------------------------- footer
def footer(t):
    W, H = 1200, 150
    gate_x = 900
    path = f"M -30 92 L {gate_x} 92 C {gate_x + 80} 92, {gate_x + 120} 60, {gate_x + 200} 30 S {W + 40} -20, {W + 80} -40"
    n, dur = 7, 14
    drones = ""
    for i in range(n):
        begin = -i * dur / n
        drones += (
            f'<g>{drone(t, 1.0, t["accent2"] if i % 3 else t["accent"])}'
            f'<animateMotion dur="{dur}s" begin="{begin:.2f}s" repeatCount="indefinite" path="{path}" rotate="auto"/></g>'
        )
    body = f"""
<line x1="0" y1="92" x2="{gate_x}" y2="92" stroke="{t['line']}" stroke-width="1.5" stroke-dasharray="2 6"/>
<line x1="{gate_x}" y1="70" x2="{gate_x}" y2="114" stroke="{t['accent']}" stroke-width="2"/>
<text x="{gate_x - 10}" y="132" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{t['muted']}">AUTHORIZATION GATE</text>
{drones}
<text x="0" y="40" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{t['faint']}">QUEUE STATUS <tspan fill="{t['accent']}">● FAIR</tspan></text>
<text x="0" y="132" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{t['faint']}">MADRID · 2026</text>"""
    return svg(W, H, body, "Animated queue of drones passing an authorization gate one by one")


# --------------------------------------------------------------------------- build
def main():
    files = {
        "header.svg": header,
        "research.svg": research_card,
        "pipedream.svg": pipedream,
        "hackathon-kit.svg": hackkit,
        "flight-log.svg": flight_log,
        "stack.svg": stack,
        "footer.svg": footer,
        "sec-about.svg": lambda t: section(t, "WP-01", "About"),
        "sec-work.svg": lambda t: section(t, "WP-02", "Featured work"),
        "sec-log.svg": lambda t: section(t, "WP-03", "Flight log"),
        "sec-stack.svg": lambda t: section(t, "WP-04", "Stack"),
        "btn-linkedin.svg": lambda t: button(t, "LinkedIn", "in"),
        "btn-email.svg": lambda t: button(t, "Email", "mail"),
    }
    for theme, t in THEMES.items():
        out = ROOT / "assets" / theme
        out.mkdir(parents=True, exist_ok=True)
        for name, fn in files.items():
            (out / name).write_text(fn(t), encoding="utf-8")
    print(f"built {len(files)} SVGs × {len(THEMES)} themes")


if __name__ == "__main__":
    main()
