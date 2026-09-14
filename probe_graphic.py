"""Grafika gry jako SVG: sonda, planety i scena lądowania."""

SHIELD_WIDTH = {"light": 80, "medium": 100, "heavy": 124}
HULL_WIDTH = {"none": 56, "standard": 68, "reinforced": 84}

# Kratery Merkurego: (cx, cy, r) w układzie kuli o środku (100, 100) i promieniu 78.
_CRATERS = [
    (74, 60, 15), (119, 50, 9), (143, 85, 12), (60, 103, 11),
    (96, 121, 17), (136, 133, 8), (77, 149, 10), (45, 74, 6),
    (110, 86, 6), (152, 58, 5), (101, 158, 6), (127, 107, 5),
    (63, 129, 6), (156, 110, 6),
]

# Pasma chmur Wenus: (cy, rx, ry, kolor, krycie) przy cx = 100.
_CLOUD_BANDS = [
    (52, 50, 12, "#fff8e2", 0.50),
    (76, 70, 10, "#c9822f", 0.26),
    (98, 77, 14, "#fff4d0", 0.38),
    (122, 69, 9, "#b3701f", 0.28),
    (146, 52, 12, "#ffeec2", 0.34),
]

PLANET_ART = {
    "mercury": {
        "light": "#d3c8ba",
        "mid": "#9a8f86",
        "dark": "#463f39",
        "glow": "#cbd5e1",
        "label": "Merkury — skalista planeta pokryta kraterami",
    },
    "venus": {
        "light": "#fff6d8",
        "mid": "#e8c07d",
        "dark": "#8a5a1c",
        "glow": "#fcd34d",
        "label": "Wenus — planeta skryta pod gęstymi chmurami",
    },
}


def planet_svg(key: str, size: int = 180) -> str:
    """Stylizowana ilustracja planety — rysowana w kodzie, bez plików zewnętrznych."""
    art = PLANET_ART[key]
    uid = f"planet-{key}-{size}"
    body, shade, halo, clip = f"{uid}-b", f"{uid}-s", f"{uid}-h", f"{uid}-c"

    parts = [
        f'<defs>'
        f'<radialGradient id="{body}" cx="34%" cy="28%" r="78%">'
        f'<stop offset="0%" stop-color="{art["light"]}" />'
        f'<stop offset="55%" stop-color="{art["mid"]}" />'
        f'<stop offset="100%" stop-color="{art["dark"]}" /></radialGradient>'
        f'<radialGradient id="{shade}" cx="32%" cy="26%" r="80%">'
        f'<stop offset="52%" stop-color="#000000" stop-opacity="0" />'
        f'<stop offset="100%" stop-color="#000000" stop-opacity="0.62" /></radialGradient>'
        f'<radialGradient id="{halo}" cx="50%" cy="50%" r="50%">'
        f'<stop offset="72%" stop-color="{art["glow"]}" stop-opacity="0.32" />'
        f'<stop offset="100%" stop-color="{art["glow"]}" stop-opacity="0" /></radialGradient>'
        f'<clipPath id="{clip}"><circle cx="100" cy="100" r="78" /></clipPath>'
        f'</defs>',
        f'<circle cx="100" cy="100" r="98" fill="url(#{halo})" />',
        f'<circle cx="100" cy="100" r="78" fill="url(#{body})" />',
        f'<g clip-path="url(#{clip})">',
    ]

    if key == "mercury":
        for cx, cy, r in _CRATERS:
            parts.append(
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#000000" opacity="0.22" />'
                f'<circle cx="{cx - r * 0.14:.1f}" cy="{cy - r * 0.16:.1f}" r="{r * 0.82:.1f}" '
                f'fill="#ffffff" opacity="0.10" />'
            )
    else:
        parts.append('<g transform="rotate(-14 100 100)">')
        for cy, rx, ry, color, opacity in _CLOUD_BANDS:
            parts.append(
                f'<ellipse cx="100" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" '
                f'opacity="{opacity}" />'
            )
        parts.append(
            '<ellipse cx="72" cy="88" rx="26" ry="7" fill="#fffaf0" opacity="0.40" />'
            '<ellipse cx="132" cy="116" rx="22" ry="6" fill="#a9651b" opacity="0.28" />'
            "</g>"
        )

    parts.append(f'<circle cx="100" cy="100" r="78" fill="url(#{shade})" /></g>')
    parts.append(
        '<ellipse cx="72" cy="66" rx="24" ry="16" fill="#ffffff" opacity="0.16" '
        'transform="rotate(-28 72 66)" />'
    )

    return (
        f'<svg viewBox="0 0 200 200" width="{size}" height="{size}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{art["label"]}">'
        + "".join(parts)
        + "</svg>"
    )


def probe_svg(heat_shielding: str, pressure_hull: str, power_source: str, stage: str | None = None) -> str:
    cx = 110
    hull_w = HULL_WIDTH[pressure_hull]
    shield_w = SHIELD_WIDTH[heat_shielding]
    hull_x = cx - hull_w / 2

    parts: list[str] = []

    # Antena
    parts.append(
        f'<line x1="{cx}" y1="28" x2="{cx}" y2="62" stroke="#94a3b8" stroke-width="3" />'
        f'<circle cx="{cx}" cy="24" r="6" fill="#cbd5f5" />'
    )

    # Panele / akumulator / RTG
    if power_source == "solar":
        for sign in (-1, 1):
            px = cx + sign * (hull_w / 2 + 6) - (44 if sign < 0 else 0)
            parts.append(
                f'<rect x="{px}" y="84" width="44" height="26" rx="3" fill="#1d4ed8" '
                f'stroke="#93c5fd" stroke-width="2" />'
                f'<line x1="{px}" y1="97" x2="{px + 44}" y2="97" stroke="#93c5fd" stroke-width="1.5" />'
            )
    elif power_source == "battery":
        parts.append(
            f'<rect x="{cx - 22}" y="150" width="44" height="22" rx="4" fill="#facc15" '
            f'stroke="#a16207" stroke-width="2" />'
            f'<text x="{cx}" y="166" font-size="13" text-anchor="middle" fill="#78350f">+ −</text>'
        )
    else:
        for sign in (-1, 0, 1):
            parts.append(
                f'<rect x="{cx + sign * 16 - 5}" y="150" width="10" height="26" rx="5" '
                f'fill="#22c55e" stroke="#166534" stroke-width="2" />'
            )

    # Kadłub
    hull_fill = "#e2e8f0" if pressure_hull != "reinforced" else "#cbd5e1"
    parts.append(
        f'<rect x="{hull_x}" y="62" width="{hull_w}" height="86" rx="14" fill="{hull_fill}" '
        f'stroke="#475569" stroke-width="{4 if pressure_hull == "reinforced" else 2}" />'
        f'<circle cx="{cx}" cy="92" r="11" fill="#0ea5e9" stroke="#0369a1" stroke-width="2" />'
    )
    for i in range(3):
        parts.append(f'<circle cx="{hull_x + 10}" cy="{114 + i * 11}" r="2.5" fill="#64748b" />')

    # Osłona termiczna
    shield_top = 148
    parts.append(
        f'<path d="M {cx - shield_w / 2} {shield_top} '
        f'Q {cx} {shield_top + 46} {cx + shield_w / 2} {shield_top} Z" '
        f'fill="#f97316" stroke="#9a3412" stroke-width="3" />'
    )

    # Nogi
    parts.append(
        f'<line x1="{cx - 24}" y1="170" x2="{cx - 44}" y2="212" stroke="#475569" stroke-width="4" />'
        f'<line x1="{cx + 24}" y1="170" x2="{cx + 44}" y2="212" stroke="#475569" stroke-width="4" />'
    )

    if stage == "liftoff":
        parts.append(
            f'<path d="M {cx - 18} 196 Q {cx} 250 {cx + 18} 196 Z" fill="#fb923c" opacity="0.9" />'
            f'<path d="M {cx - 9} 196 Q {cx} 232 {cx + 9} 196 Z" fill="#fde047" />'
        )

    return (
        '<svg viewBox="0 0 220 260" width="220" height="260" '
        'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Podgląd twojej sondy">'
        + "".join(parts)
        + "</svg>"
    )


SCENE_W = 480
SCENE_H = 420
GROUND_Y = 330

SKY = {
    "mercury": ("#05060f", "#1c2436"),
    "venus": ("#f7d98f", "#a9531a"),
}
GROUND = {
    "mercury": ("#8d8378", "#5c554d"),
    "venus": ("#cf8a3a", "#8a4d17"),
}

# Stałe pozycje gwiazd, aby scena nie migotała między klatkami.
_STARS = [
    (28, 44), (96, 22), (154, 68), (212, 30), (268, 86), (322, 40),
    (386, 74), (440, 26), (62, 112), (198, 128), (350, 118), (452, 140),
    (120, 176), (288, 166), (418, 196), (42, 208),
]


def descent_scene(
    planet: str,
    heat_shielding: str,
    pressure_hull: str,
    power_source: str,
    progress: float,
    outcome: str | None = None,
) -> str:
    """Sonda opada z góry kadru na powierzchnię planety. outcome: None | 'landed' | 'destroyed'."""
    sky_top, sky_bottom = SKY[planet]
    ground_light, ground_dark = GROUND[planet]

    scale = 0.62
    probe_x = SCENE_W / 2 - 110 * scale
    start_y = -170.0
    land_y = GROUND_Y - 212 * scale
    probe_y = start_y + (land_y - start_y) * min(max(progress, 0.0), 1.0)

    parts: list[str] = [
        f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{sky_top}" />'
        f'<stop offset="100%" stop-color="{sky_bottom}" /></linearGradient>'
        f'<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{ground_light}" />'
        f'<stop offset="100%" stop-color="{ground_dark}" /></linearGradient></defs>',
        f'<rect width="{SCENE_W}" height="{SCENE_H}" fill="url(#sky)" />',
    ]

    if planet == "mercury":
        parts += [f'<circle cx="{x}" cy="{y}" r="1.6" fill="#e2e8f0" opacity="0.85" />' for x, y in _STARS]
        parts.append('<circle cx="430" cy="52" r="30" fill="#fff7cc" opacity="0.95" />')
        parts.append('<circle cx="430" cy="52" r="52" fill="#fde68a" opacity="0.18" />')
    else:
        for i in range(4):
            parts.append(
                f'<ellipse cx="{70 + i * 120}" cy="{70 + (i % 2) * 46}" rx="96" ry="26" '
                f'fill="#fff1c9" opacity="0.28" />'
            )

    parts.append(
        f'<path d="M 0 {GROUND_Y + 22} Q 120 {GROUND_Y - 14} 240 {GROUND_Y + 6} '
        f'T {SCENE_W} {GROUND_Y + 16} L {SCENE_W} {SCENE_H} L 0 {SCENE_H} Z" fill="url(#ground)" />'
    )
    for cx, cy, rx in ((70, 372, 34), (200, 392, 26), (330, 366, 30), (430, 396, 22)):
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx / 3.2}" fill="#00000033" />')

    probe = probe_svg(heat_shielding, pressure_hull, power_source)
    inner = probe.split(">", 1)[1].rsplit("</svg>", 1)[0]

    if outcome == "destroyed":
        parts.append(
            f'<g transform="translate({probe_x} {land_y}) scale({scale}) '
            f'rotate(28 110 130)" opacity="0.55">{inner}</g>'
        )
        burst_x = SCENE_W / 2
        burst_y = land_y + 150 * scale
        parts.append(f'<circle cx="{burst_x}" cy="{burst_y}" r="62" fill="#f97316" opacity="0.45" />')
        parts.append(f'<circle cx="{burst_x}" cy="{burst_y}" r="40" fill="#fb923c" opacity="0.8" />')
        parts.append(f'<circle cx="{burst_x}" cy="{burst_y}" r="20" fill="#fef08a" />')
        for dx, dy in ((-80, -34), (-44, -70), (44, -70), (80, -34), (-70, 20), (70, 20)):
            parts.append(
                f'<line x1="{burst_x}" y1="{burst_y}" x2="{burst_x + dx}" y2="{burst_y + dy}" '
                f'stroke="#fbbf24" stroke-width="5" stroke-linecap="round" opacity="0.85" />'
            )
    else:
        if outcome is None:
            # Hamowanie silnikiem podczas opadania.
            parts.append(
                f'<g transform="translate({probe_x} {probe_y}) scale({scale})">'
                f'<path d="M 92 196 Q 110 244 128 196 Z" fill="#fb923c" opacity="0.85" />'
                f'<path d="M 101 196 Q 110 228 119 196 Z" fill="#fde047" /></g>'
            )
        else:
            parts.append(
                f'<ellipse cx="{SCENE_W / 2}" cy="{GROUND_Y + 14}" rx="72" ry="12" '
                f'fill="#00000044" />'
            )
        parts.append(
            f'<g transform="translate({probe_x} {probe_y}) scale({scale})">{inner}</g>'
        )

    return (
        f'<svg viewBox="0 0 {SCENE_W} {SCENE_H}" width="100%" '
        f'style="max-width:{SCENE_W}px;border-radius:1rem" '
        'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Lądowanie sondy">'
        + "".join(parts)
        + "</svg>"
    )
