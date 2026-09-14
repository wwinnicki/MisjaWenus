"""Reguły misji: który system zawiedzie pierwszy i dlaczego."""

from dataclasses import dataclass, field

import game_data as gd


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


def total_mass(heat_shielding: str, pressure_hull: str, power_source: str) -> int:
    def mass(system: dict, key: str) -> int:
        return next(o["mass"] for o in system["options"] if o["key"] == key)

    return (
        mass(gd.HEAT_SHIELDING, heat_shielding)
        + mass(gd.PRESSURE_HULL, pressure_hull)
        + mass(gd.POWER_SOURCE, power_source)
    )


def run_mission(
    planet: str,
    heat_shielding: str,
    pressure_hull: str,
    power_source: str,
    landing_site: str,
    fact_index: int,
) -> MissionResult:
    limits: list[tuple[int | None, str]] = []
    wasted_mass: list[str] = []
    landing_note: str | None = None

    if planet == "venus":
        limits.append(gd.HEAT_SHIELDING["venus_limits"][heat_shielding])
        limits.append(gd.PRESSURE_HULL["venus_limits"][pressure_hull])
        limits.append(gd.POWER_SOURCE["venus_limits"][power_source])

        if landing_site != "day":
            landing_note = (
                "Liczyłeś na chłodniejsze miejsce, lecz gęsta atmosfera Wenus rozprowadza "
                "ciepło po całej planecie."
            )
    else:
        wasted_mass.append(
            "Kadłub ciśnieniowy był zbędny — Merkury nie ma atmosfery, która mogłaby "
            "zgnieść sondę."
        )

        if landing_site == "day":
            limits.append(gd.HEAT_SHIELDING["mercury_day_limits"][heat_shielding])
            limits.append(gd.POWER_SOURCE["mercury_day_limits"][power_source])
        else:
            limits.append(gd.POWER_SOURCE["mercury_cold_limits"][power_source])
            wasted_mass.append(
                "Osłona termiczna była zbędna — zagrożeniem jest tu skrajny mróz, a nie upał."
            )

    # Sonda ginie przez system o najniższym limicie; None oznacza brak awarii.
    survival_minutes: int | None = None
    cause = "Wszystkie systemy wytrzymały."

    for minutes, message in limits:
        if minutes is None:
            continue
        if survival_minutes is None or minutes < survival_minutes:
            survival_minutes = minutes
            cause = message

    for _, message in limits:
        if message != cause:
            wasted_mass.append(f"System był mocniejszy niż potrzeba: {message}")

    final_minutes = 9999 if survival_minutes is None else survival_minutes

    return MissionResult(
        survival_minutes=survival_minutes,
        cause=cause,
        wasted_mass=wasted_mass,
        fact=gd.FACTS[fact_index % len(gd.FACTS)],
        rating=get_rating(final_minutes),
        landing_note=landing_note,
    )
