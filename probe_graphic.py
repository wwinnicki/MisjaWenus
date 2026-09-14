"""Rysunek sondy jako SVG, zależny od wybranych systemów."""

SHIELD_WIDTH = {"light": 80, "medium": 100, "heavy": 124}
HULL_WIDTH = {"none": 56, "standard": 68, "reinforced": 84}


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
