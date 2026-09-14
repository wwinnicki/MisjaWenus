"""Misja Sonda — prosta, turowa gra szkolna o Merkurym i Wenus (wersja Streamlit)."""

import time
from collections.abc import Callable

import streamlit as st

import game_data as gd
from mission import run_mission, total_mass
from probe_graphic import descent_scene, probe_svg

st.set_page_config(page_title="Misja Sonda", page_icon="🛰️", layout="centered")

DEFAULTS = {
    "screen": "title",
    "planet": None,
    "heat_shielding": "light",
    "pressure_hull": "none",
    "power_source": "solar",
    "landing_site": "day",
    "briefing_unlocked": False,
    "fact_index": 0,
    "best_time": 0,
    "result": None,
    "sim_frame": 0,
}

for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)


def go(screen: str) -> None:
    st.session_state.screen = screen


def format_minutes(minutes: int | None) -> str:
    if minutes is None or minutes >= 9999:
        return "120+ min"
    return f"{minutes} min"


def label_of(system: dict, key: str) -> str:
    return next(o["label"] for o in system["options"] if o["key"] == key)


def option_caption(system: dict) -> Callable[[str], str]:
    def caption(key: str) -> str:
        mass = next(o["mass"] for o in system["options"] if o["key"] == key)
        return f"{label_of(system, key)} — {mass} jedn. masy"

    return caption


def render_probe(heat_shielding: str, pressure_hull: str, power_source: str) -> None:
    svg = probe_svg(heat_shielding, pressure_hull, power_source)
    st.markdown(f'<div style="text-align:center">{svg}</div>', unsafe_allow_html=True)


# ============================================================
# Ekrany
# ============================================================


def screen_title() -> None:
    st.markdown("<h1 style='text-align:center'>Misja Sonda</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;font-size:1.1rem;opacity:0.8'>"
        "Zbuduj sondę. Wyląduj na Merkurym lub Wenus. Sprawdź, co jej zagraża.</p>",
        unsafe_allow_html=True,
    )
    left, right = st.columns(2)
    left.button("Rozpocznij misję", type="primary", use_container_width=True, on_click=go, args=("select",))
    right.button("Odprawa misji", use_container_width=True, on_click=go, args=("briefing",))


def choose_planet(key: str) -> None:
    st.session_state.planet = key
    st.session_state.screen = "build"


def screen_select() -> None:
    st.subheader("Wybierz cel misji")
    st.caption("Porównaj warunki, zanim wyślesz sondę.")

    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:1rem;padding:1rem;border-radius:1rem;
                    background:linear-gradient(90deg,#fde68a22,#0f172a22)">
          <div style="font-size:2rem">☀️ <strong style="font-size:1rem">Słońce</strong></div>
          <div style="flex:1;border-top:2px dashed #94a3b8"></div>
          <div style="text-align:center">🪨<br><small>Merkury<br>58 mln km</small></div>
          <div style="flex:1;border-top:2px dashed #94a3b8"></div>
          <div style="text-align:center">🟡<br><small>Wenus<br>108 mln km</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for column, key in zip(st.columns(2), gd.PLANETS):
        planet = gd.PLANETS[key]
        with column, st.container(border=True):
            st.markdown(
                f"<div style='font-size:3rem;text-align:center'>{planet['emoji']}</div>",
                unsafe_allow_html=True,
            )
            st.caption(planet["badge"].upper())
            st.markdown(f"### {planet['name']}")
            st.write(planet["teaser"])
            for label, value in planet["details"][:5]:
                st.markdown(f"**{label}:** {value}")
            st.button(
                f"Wybierz: {planet['name']}",
                key=f"pick_{key}",
                type="primary",
                use_container_width=True,
                on_click=choose_planet,
                args=(key,),
            )


def launch() -> None:
    result = run_mission(
        planet=st.session_state.planet,
        heat_shielding=st.session_state.heat_shielding,
        pressure_hull=st.session_state.pressure_hull,
        power_source=st.session_state.power_source,
        landing_site=st.session_state.landing_site,
        fact_index=st.session_state.fact_index,
    )
    st.session_state.result = result
    st.session_state.fact_index += 1
    st.session_state.best_time = max(st.session_state.best_time, result.final_minutes)
    st.session_state.sim_frame = 0
    st.session_state.screen = "simulation"


def screen_build() -> None:
    planet = gd.PLANETS[st.session_state.planet]

    header, target = st.columns([3, 2])
    header.subheader("Zbuduj swoją sondę")
    target.markdown(f"<p style='text-align:right;padding-top:0.8rem'><strong>Cel:</strong> {planet['name']}</p>", unsafe_allow_html=True)

    preview, controls = st.columns([2, 3])

    with controls:
        st.selectbox(
            gd.HEAT_SHIELDING["name"],
            [o["key"] for o in gd.HEAT_SHIELDING["options"]],
            format_func=option_caption(gd.HEAT_SHIELDING),
            key="heat_shielding",
        )
        st.selectbox(
            gd.PRESSURE_HULL["name"],
            [o["key"] for o in gd.PRESSURE_HULL["options"]],
            format_func=option_caption(gd.PRESSURE_HULL),
            key="pressure_hull",
        )
        st.selectbox(
            gd.POWER_SOURCE["name"],
            [o["key"] for o in gd.POWER_SOURCE["options"]],
            format_func=option_caption(gd.POWER_SOURCE),
            key="power_source",
        )
        st.radio(
            "Miejsce lądowania",
            [s["key"] for s in gd.LANDING_SITES],
            format_func=lambda k: next(s["label"] for s in gd.LANDING_SITES if s["key"] == k),
            horizontal=True,
            key="landing_site",
        )

    mass = total_mass(
        st.session_state.heat_shielding,
        st.session_state.pressure_hull,
        st.session_state.power_source,
    )
    over_budget = mass > gd.BUDGET

    with preview:
        st.caption("TWOJA SONDA")
        render_probe(
            st.session_state.heat_shielding,
            st.session_state.pressure_hull,
            st.session_state.power_source,
        )
        st.caption(
            f"{label_of(gd.HEAT_SHIELDING, st.session_state.heat_shielding)} osłona · "
            f"{label_of(gd.PRESSURE_HULL, st.session_state.pressure_hull)} kadłub · "
            f"{label_of(gd.POWER_SOURCE, st.session_state.power_source)}"
        )

    with st.container(border=True):
        st.markdown(f"**Limit masy** — {mass} / {gd.BUDGET}")
        st.progress(min(mass / gd.BUDGET, 1.0))
        if over_budget:
            st.error("Przekroczono limit! Wybierz lżejsze systemy.")

    start, change = st.columns([3, 2])
    start.button("START", type="primary", use_container_width=True, disabled=over_budget, on_click=launch)
    change.button("Zmień planetę", use_container_width=True, on_click=change_planet)


def screen_simulation() -> None:
    planet_key = st.session_state.planet
    planet = gd.PLANETS[planet_key]
    result = st.session_state.result
    destroyed = result is not None and result.survival_minutes == 0

    steps = 26
    frame = st.session_state.sim_frame
    last = frame == steps

    # Klatka jest wyświetlana, gdy skrypt śpi na początku kolejnego przebiegu.
    if frame > 0:
        time.sleep(1.4 if frame > steps else 0.07)

    if frame > steps:
        st.session_state.sim_frame = 0
        go("result")
        st.rerun()

    scene = descent_scene(
        planet_key,
        st.session_state.heat_shielding,
        st.session_state.pressure_hull,
        st.session_state.power_source,
        min(frame / steps, 1.0),
        ("destroyed" if destroyed else "landed") if last else None,
    )
    caption = (
        ("Utrata sygnału po przybyciu" if destroyed else "Sonda wylądowała!")
        if last
        else f"Opadanie nad {planet['name']}…"
    )
    st.markdown(f"<div style='text-align:center'>{scene}</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center'>{caption}</h3>", unsafe_allow_html=True)

    st.session_state.sim_frame = frame + 1
    st.rerun()


def screen_result() -> None:
    result = st.session_state.result
    display_time = "120+" if result.survival_minutes is None else result.survival_minutes

    with st.container(border=True):
        st.markdown(
            f"<div style='text-align:center'>"
            f"<p style='letter-spacing:0.08em;opacity:0.7;margin-bottom:0'>CZAS DZIAŁANIA</p>"
            f"<p style='font-size:3.5rem;font-weight:700;margin:0'>{display_time}</p>"
            f"<p style='opacity:0.7;margin:0'>minut</p>"
            f"<p style='font-size:1.25rem;font-weight:600;margin-top:1rem'>{result.rating}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

    with st.container(border=True):
        st.markdown("#### Przyczyna awarii")
        st.write(result.cause)

    if result.landing_note:
        st.warning(f"**Wniosek dotyczący miejsca lądowania**\n\n{result.landing_note}")

    if result.wasted_mass:
        with st.container(border=True):
            st.markdown("#### Zmarnowana masa")
            st.markdown("\n".join(f"- {item}" for item in result.wasted_mass))

    st.info(f"**Ciekawostka**\n\n{result.fact}")

    st.caption(f"Najlepszy czas w tej sesji: **{format_minutes(st.session_state.best_time)}**")

    retry, change = st.columns(2)
    retry.button("Spróbuj ponownie", type="primary", use_container_width=True, on_click=go, args=("build",))
    change.button("Zmień planetę", use_container_width=True, on_click=change_planet)


def change_planet() -> None:
    st.session_state.planet = None
    st.session_state.screen = "select"


def unlock_briefing() -> None:
    if st.session_state.get("brief_code", "").strip().lower() == gd.BRIEFING_CODE:
        st.session_state.briefing_unlocked = True


def screen_briefing() -> None:
    title, back = st.columns([3, 1])
    title.subheader("Odprawa misji")
    back.button("Wróć", use_container_width=True, on_click=go, args=("title",))

    if not st.session_state.briefing_unlocked:
        with st.container(border=True):
            st.write("Zablokowane do czasu odblokowania rundy 2 przez nauczyciela.")
            code, unlock = st.columns([3, 1])
            code.text_input(
                "Kod klasy", placeholder="Wpisz kod klasy", key="brief_code", label_visibility="collapsed"
            )
            unlock.button("Odblokuj", type="primary", use_container_width=True, on_click=unlock_briefing)
            st.caption("Podpowiedź: kod to ORBIT.")
        return

    for column, key in zip(st.columns(2), gd.PLANETS):
        planet = gd.PLANETS[key]
        with column, st.container(border=True):
            st.markdown(
                f"<div style='font-size:3rem;text-align:center'>{planet['emoji']}</div>",
                unsafe_allow_html=True,
            )
            st.caption(planet["badge"].upper())
            st.markdown(f"### {planet['name']}")
            st.write(planet["teaser"])
            for label, value in planet["details"]:
                st.markdown(f"**{label}:** {value}")

    with st.container(border=True):
        st.markdown("#### Porównanie planet")
        st.table(
            {
                "Cecha": [row[0] for row in gd.COMPARISON],
                "Merkury": [row[1] for row in gd.COMPARISON],
                "Wenus": [row[2] for row in gd.COMPARISON],
            }
        )

    with st.container(border=True):
        st.markdown("#### Najważniejsze wnioski")
        for item in gd.TAKEAWAYS:
            st.markdown(f"- {item}")


# ============================================================
# Nagłówek i aktywny ekran
# ============================================================

home, briefing = st.columns([3, 1])
home.button("🛰️ Misja Sonda", use_container_width=False, on_click=go, args=("title",))
briefing.button(
    f"Odprawa {'' if st.session_state.briefing_unlocked else '🔒'}",
    use_container_width=True,
    on_click=go,
    args=("briefing",),
)
st.divider()

SCREENS = {
    "title": screen_title,
    "select": screen_select,
    "build": screen_build,
    "simulation": screen_simulation,
    "result": screen_result,
    "briefing": screen_briefing,
}

SCREENS[st.session_state.screen]()
