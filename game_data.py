"""Wszystkie liczby i zasady gry — zmieniaj tutaj, aby dostroić rozgrywkę."""

# Merkury wymaga znacznie więcej paliwa na dolot, więc zostaje mniej masy na samą sondę.
PLANETS = {
    "mercury": {
        "name": "Merkury",
        "teaser": "Najbliżej Słońca, ale prawie bez atmosfery.",
        "badge": "Ogromne wahania temperatury",
        "emoji": "🪨",
        "color": "#9a8f86",
        "budget": 100,
        "details": [
            ("Odległość od Słońca", "58 mln km"),
            ("Temperatura powierzchni", "od −180 °C do 430 °C"),
            ("Atmosfera", "Prawie brak"),
            ("Ciśnienie na powierzchni", "Prawie zerowe"),
            ("Doba słoneczna", "176 dni ziemskich"),
            ("Zagrożenie misji", "Upał, mróz, ciemność i brak czym hamować"),
        ],
    },
    "venus": {
        "name": "Wenus",
        "teaser": "Gęsta atmosfera CO₂ zatrzymuje ciepło na całej planecie.",
        "badge": "Najgorętsza planeta",
        "emoji": "🟡",
        "color": "#e8c07d",
        "budget": 120,
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
    # Noc na Merkurym trwa 88 dni ziemskich, ale potem nadchodzi świt i +430 °C.
    "mercury_night_limits": {
        "light": (60, "Nastał świt. Temperatura skoczyła o ponad 600 °C i lekka osłona odpadła."),
        "medium": (110, "Po wschodzie Słońca średnia osłona stopniowo się przegrzała."),
        "heavy": (None, "Ciężka osłona przetrwała wschód Słońca."),
    },
}

PRESSURE_HULL = {
    "name": "Kadłub ciśnieniowy",
    "options": [
        {"key": "none", "label": "Brak", "mass": 0},
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
        "solar": (100, "Sonda działała aż do zachodu Słońca, a potem zamarzła w ciemności."),
        "battery": (70, "Akumulator się rozładował."),
        "nuclear": (None, "Zasilanie działa prawidłowo."),
    },
}

LANDING_SYSTEM = {
    "name": "Układ lądowania",
    "options": [
        {"key": "parachute", "label": "Spadochron", "mass": 5},
        {"key": "small_retro", "label": "Małe silniki hamujące", "mass": 15},
        {"key": "full_retro", "label": "Pełne silniki hamujące", "mass": 28},
    ],
    "venus_limits": {
        "parachute": (None, "Spadochron wyhamował sondę w gęstej atmosferze."),
        "small_retro": (None, "Silniki wyhamowały sondę."),
        "full_retro": (None, "Silniki wyhamowały sondę."),
    },
    "mercury_limits": {
        "parachute": (
            0,
            "Spadochron nie miał o co się oprzeć — Merkury prawie nie ma atmosfery. "
            "Sonda roztrzaskała się o powierzchnię.",
        ),
        "small_retro": (
            0,
            "Małe silniki nie wyhamowały sondy. Bez atmosfery całą prędkość trzeba "
            "wytracić samymi silnikami.",
        ),
        "full_retro": (None, "Silniki hamujące posadziły sondę miękko na powierzchni."),
    },
}

LANDING_SITES = [
    {"key": "day", "label": "Strona dzienna"},
    {"key": "night", "label": "Strona nocna"},
    {"key": "polar", "label": "Krater polarny"},
]

# Dlaczego dany system był zbędny — klucz: (planeta lub "planeta_miejsce", system).
WASTE_REASONS = {
    ("mercury", "pressure_hull"): (
        "Merkury nie ma atmosfery, która mogłaby zgnieść sondę."
    ),
    ("mercury_polar", "heat_shielding"): (
        "Krater polarny jest stale zacieniony — nigdy nie dociera tu słoneczny żar."
    ),
    ("venus", "landing_system"): (
        "Gęsta atmosfera Wenus sama hamuje sondę — wystarczy spadochron."
    ),
}

SITE_NOTES = {
    ("mercury", "day"): (
        "Słońce świeci tu około 7 razy mocniej niż na Ziemi, a grunt nagrzewa się do 430 °C. "
        "Za to energii ze Słońca jest tu pod dostatkiem — dopóki nie zajdzie."
    ),
    ("mercury", "night"): (
        "Noc na Merkurym trwa 88 dni ziemskich i panuje w niej −180 °C. Potem jednak "
        "nadchodzi świt, a temperatura skacze o ponad 600 °C."
    ),
    ("mercury", "polar"): (
        "Kratery na biegunach Merkurego są stale zacienione — nigdy nie zagląda tu Słońce. "
        "Jest lodowato, ale nigdy gorąco, i właśnie dlatego zachował się tam lód wodny."
    ),
    ("venus", "night"): (
        "Liczyłeś na chłodniejsze miejsce, lecz gęsta atmosfera Wenus rozprowadza "
        "ciepło po całej planecie."
    ),
    ("venus", "polar"): (
        "Liczyłeś na chłodniejsze miejsce, lecz gęsta atmosfera Wenus rozprowadza "
        "ciepło po całej planecie."
    ),
}

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
    ("Hamowanie przy lądowaniu", "Tylko silniki — nie ma o co oprzeć spadochronu", "Spadochron — atmosfera hamuje sondę"),
    ("Główne zagrożenie", "Wahania temperatury i ciemność", "Upał, ciśnienie, kwaśne chmury"),
]

TAKEAWAYS = [
    "Wenus jest gorętsza od Merkurego, bo jej gęsta atmosfera CO₂ zatrzymuje ciepło.",
    "Na Wenus miejsce lądowania prawie nie ma znaczenia — upał jest wszędzie.",
    "Na Merkurym kadłub ciśnieniowy jest zbędnym obciążeniem.",
    "Bez atmosfery spadochron jest bezużyteczny — na Merkurym trzeba hamować silnikami, "
    "a to kosztuje mnóstwo masy.",
    "Stale zacienione kratery polarne Merkurego to jedyne miejsce, w którym nie ma ani "
    "żaru, ani wschodu Słońca.",
    "Energia jądrowa działa niemal wszędzie; panele słoneczne zawodzą w ciemności i na Wenus.",
]

BRIEFING_CODE = "orbit"
