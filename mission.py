"""Reguły misji: który system zawiedzie pierwszy i dlaczego."""

from dataclasses import dataclass, field

import game_data as gd

# Opcje każdego systemu są uporządkowane od najlżejszej do najcięższej.
SYSTEMS = (
    ("landing_system", gd.LANDING_SYSTEM),
    ("heat_shielding", gd.HEAT_SHIELDING),
    ("pressure_hull", gd.PRESSURE_HULL),
    ("power_source", gd.POWER_SOURCE),
)

NO_FAILURE = "Wszystkie systemy wytrzymały do końca misji."


@dataclass
class MissionResult:
    survival_minutes: int | None
    cause: str
    wasted_mass: list[str] = field(default_factory=list)
    fact: str = ""
    rating: str = ""
    landing_note: str | None = None

    @property
    def final_minutes(self) -> int:
        return 9999 if self.survival_minutes is None else self.survival_minutes


def get_rating(survival_minutes: int) -> str:
    if survival_minutes == 0:
        return "Misja utracona po przybyciu"
    if survival_minutes < 30:
        return "Odebrano część danych"
    if survival_minutes < 120:
        return "Udana misja"
    return "Rekordowy wynik"


def option_of(system: dict, key: str) -> dict:
    return next(o for o in system["options"] if o["key"] == key)


def total_mass(
    heat_shielding: str, pressure_hull: str, power_source: str, landing_system: str
) -> int:
    config = {
        "heat_shielding": heat_shielding,
        "pressure_hull": pressure_hull,
        "power_source": power_source,
        "landing_system": landing_system,
    }
    return sum(option_of(system, config[name])["mass"] for name, system in SYSTEMS)


def _limits(planet: str, landing_site: str, config: dict[str, str]) -> list[tuple[int | None, str]]:
    """Limity czasu działania narzucone przez każdy istotny system."""
    if planet == "venus":
        return [
            gd.LANDING_SYSTEM["venus_limits"][config["landing_system"]],
            gd.HEAT_SHIELDING["venus_limits"][config["heat_shielding"]],
            gd.PRESSURE_HULL["venus_limits"][config["pressure_hull"]],
            gd.POWER_SOURCE["venus_limits"][config["power_source"]],
        ]

    limits = [gd.LANDING_SYSTEM["mercury_limits"][config["landing_system"]]]
    if landing_site == "day":
        limits.append(gd.HEAT_SHIELDING["mercury_day_limits"][config["heat_shielding"]])
        limits.append(gd.POWER_SOURCE["mercury_day_limits"][config["power_source"]])
    else:
        limits.append(gd.POWER_SOURCE["mercury_cold_limits"][config["power_source"]])
        # Krater polarny jest stale zacieniony, więc wschód Słońca grozi tylko nocnej stronie.
        if landing_site == "night":
            limits.append(gd.HEAT_SHIELDING["mercury_night_limits"][config["heat_shielding"]])
    return limits


def _outcome(limits: list[tuple[int | None, str]]) -> tuple[int | None, str]:
    survival: int | None = None
    cause = NO_FAILURE
    for minutes, message in limits:
        if minutes is None:
            continue
        if survival is None or minutes < survival:
            survival, cause = minutes, message
    return survival, cause


def _final(survival: int | None) -> int:
    return 9999 if survival is None else survival


def _wasted_mass(planet: str, landing_site: str, config: dict[str, str], baseline: int) -> list[str]:
    """System jest zbędny, jeśli lżejsza opcja dałaby dokładnie ten sam wynik misji."""
    notes: list[str] = []
    for name, system in SYSTEMS:
        options = system["options"]
        chosen = option_of(system, config[name])
        for lighter in options[: options.index(chosen)]:
            trial = config | {name: lighter["key"]}
            if _final(_outcome(_limits(planet, landing_site, trial))[0]) < baseline:
                continue
            reason = gd.WASTE_REASONS.get((f"{planet}_{landing_site}", name)) or gd.WASTE_REASONS.get(
                (planet, name), ""
            )
            notes.append(
                f"**{system['name']}** — wystarczyłaby opcja „{lighter['label']}”. "
                f"Zaoszczędziłbyś {chosen['mass'] - lighter['mass']} jedn. masy. {reason}".strip()
            )
            break
    return notes


def run_mission(
    planet: str,
    heat_shielding: str,
    pressure_hull: str,
    power_source: str,
    landing_site: str,
    landing_system: str,
    fact_index: int,
) -> MissionResult:
    config = {
        "heat_shielding": heat_shielding,
        "pressure_hull": pressure_hull,
        "power_source": power_source,
        "landing_system": landing_system,
    }

    survival, cause = _outcome(_limits(planet, landing_site, config))
    baseline = _final(survival)

    return MissionResult(
        survival_minutes=survival,
        cause=cause,
        wasted_mass=_wasted_mass(planet, landing_site, config, baseline),
        fact=gd.FACTS[fact_index % len(gd.FACTS)],
        rating=get_rating(baseline),
        landing_note=gd.SITE_NOTES.get((planet, landing_site)),
    )
