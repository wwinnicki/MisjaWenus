"""Wszystkie liczby i zasady gry — zmieniaj tutaj, aby dostroić rozgrywkę."""

BUDGET = 100

PLANETS = {
    "mercury": {
        "name": "Merkury",
        "teaser": "Najbliżej Słońca, ale prawie bez atmosfery.",
        "badge": "Ogromne wahania temperatury",
        "emoji": "🪨",
        "color": "#9a8f86",
        "details": [
            ("Odległość od Słońca", "58 mln km"),
            ("Temperatura powierzchni", "od −180 °C do 430 °C"),
            ("Atmosfera", "Prawie brak"),
            ("Ciśnienie na powierzchni", "Prawie zerowe"),
            ("Doba słoneczna", "176 dni ziemskich"),
            ("Zagrożenie misji", "Upał, mróz i ciemność"),
        ],
    },
    "venus": {
        "name": "Wenus",
        "teaser": "Gęsta atmosfera CO₂ zatrzymuje ciepło na całej planecie.",
        "badge": "Najgorętsza planeta",
        "emoji": "🟡",
        "color": "#e8c07d",
        "details": [
            ("Odległość od Słońca", "108 mln km"),
            ("Temperatura powierzchni", "Około 465 °C"),
            ("Atmosfera", "96,5% dwutlenku węgla"),
            ("Ciśnienie na powierzchni", "92× większe niż na Ziemi"),
            ("Doba słoneczna", "117 dni ziemskich"),
            ("Zagrożenie misji", "Upał, miażdżące ciśnienie i kwaśne chmury"),
        ],
    },
}

HEAT_SHIELDING = {
    "name": "Osłona termiczna",
    "options": [
        {"key": "light", "label": "Lekka", "mass": 10},
        {"key": "medium", "label": "Średnia", "mass": 25},
        {"key": "heavy", "label": "Ciężka", "mass": 45},
    ],
    "venus_limits": {
        "light": (5, "Wnętrze osiągnęło 465 °C. Elektronika się stopiła."),
        "medium": (30, "Osłona przestała odbierać ciepło. Awaria termiczna."),
        "heavy": (
            None,
            "Osiągnięto granicę termiczną — ten sam problem dotknął lądowniki Wenera.",
        ),
    },
    "mercury_day_limits": {
        "light": (10, "Lekka osłona nie wytrzymała upału po dziennej stronie."),
        "medium": (90, "Średnia osłona przegrzała się po dziennej stronie."),
        "heavy": (None, "Ciężka osłona wytrzymała upał po dziennej stronie."),
    },
}

PRESSURE_HULL = {
    "name": "Kadłub ciśnieniowy",
    "options": [
        {"key": "none", "label": "Brak", "mass": 5},
        {"key": "standard", "label": "Standardowy", "mass": 20},
        {"key": "reinforced", "label": "Wzmocniony", "mass": 40},
    ],
    "venus_limits": {
        "none": (
            0,
            "Kadłub zapadł się 3 km nad powierzchnią. Ciśnienie na Wenus jest 92 razy "
            "większe niż na Ziemi.",
        ),
        "standard": (2, "Kadłub wytrzymał opadanie, ale uległ zniszczeniu na powierzchni."),
        "reinforced": (None, "Kadłub wytrzymał."),
    },
}

POWER_SOURCE = {
    "name": "Źródło energii",
    "options": [
        {"key": "solar", "label": "Panele słoneczne", "mass": 10},
        {"key": "battery", "label": "Akumulator", "mass": 15},
        {"key": "nuclear", "label": "Jądrowe (RTG)", "mass": 35},
    ],
    "venus_limits": {
        "solar": (
            8,
            "Do powierzchni Wenus dociera bardzo mało światła. Panele niemal nie "
            "wytwarzały energii.",
        ),
        "battery": (60, "Akumulator się rozładował."),
        "nuclear": (None, "Zasilanie działa prawidłowo."),
    },
    "mercury_cold_limits": {
        "solar": (0, "Nie ma tu światła. Sonda nie uruchomiła się przy −180 °C."),
        "battery": (40, "Akumulator rozładował się podczas ogrzewania, a sonda zamarzła."),
        "nuclear": (None, "Ciepło z RTG ogrzewało sondę."),
    },
    "mercury_day_limits": {
        "solar": (None, "Światło słoneczne jest tu około 7 razy silniejsze niż na Ziemi."),
        "battery": (120, "Akumulator się rozładował."),
        "nuclear": (None, "Zasilanie działa prawidłowo."),
    },
}

LANDING_SITES = [
    {"key": "day", "label": "Strona dzienna"},
    {"key": "night", "label": "Strona nocna"},
    {"key": "polar", "label": "Krater polarny"},
]

FACTS = [
    "Powierzchnia Wenus ma około 465 °C — dość, by stopić ołów — choć Merkury leży prawie "
    "dwa razy bliżej Słońca.",
    "Atmosfera Wenus składa się w 96,5% z dwutlenku węgla. Dlatego zatrzymuje tak dużo ciepła.",
    "Radzieckie lądowniki Wenera działały na powierzchni od około 23 do rekordowych 127 minut.",
    "Dzienna strona Merkurego osiąga około 430 °C, a nocna spada do około −180 °C.",
    "Jedna doba na Wenus trwa dłużej niż jej rok.",
    "W stale zacienionych kraterach na biegunach Merkurego znajduje się lód wodny.",
    "Wenus obraca się w przeciwnym kierunku niż niemal wszystkie pozostałe planety.",
]

COMPARISON = [
    ("Atmosfera", "Prawie brak", "Gęsta atmosfera CO₂ (96,5%)"),
    ("Temperatura", "Dzień: ~430 °C, noc: ~−180 °C", "~465 °C wszędzie"),
    ("Ciśnienie", "Znikome", "92× większe niż na Ziemi"),
    ("Światło słoneczne", "~7× silniejsze niż na Ziemi", "Tylko 1–2% dociera do powierzchni"),
    ("Główne zagrożenie", "Wahania temperatury i ciemność", "Upał, ciśnienie, kwaśne chmury"),
]

TAKEAWAYS = [
    "Wenus jest gorętsza od Merkurego, bo jej gęsta atmosfera CO₂ zatrzymuje ciepło.",
    "Na Wenus miejsce lądowania prawie nie ma znaczenia — upał jest wszędzie.",
    "Na Merkurym kadłub ciśnieniowy jest zbędnym obciążeniem.",
    "Energia jądrowa działa niemal wszędzie; panele słoneczne zawodzą w ciemności i na Wenus.",
]

BRIEFING_CODE = "orbit"
