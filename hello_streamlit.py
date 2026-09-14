"""Hello World dla Streamlita — ściąga z mechanizmów użytych w grze „Misja Sonda".

Uruchom:  streamlit run hello_streamlit.py

════════════════════════════════════════════════════════════════════════════
NAJWAŻNIEJSZA ZASADA STREAMLITA
════════════════════════════════════════════════════════════════════════════
Streamlit NIE działa jak zwykła aplikacja z oknami i zdarzeniami.
Ten plik to zwykły skrypt Pythona, który wykonuje się OD GÓRY DO DOŁU.

Za każdym razem, gdy użytkownik kliknie przycisk, przesunie suwak albo wybierze
coś z listy, Streamlit uruchamia CAŁY ten plik jeszcze raz od pierwszej linijki
i rysuje stronę od nowa. Nazywamy to „rerun" (ponowny przebieg).

Wniosek: zwykła zmienna Pythona ginie po każdym kliknięciu, bo skrypt startuje
od zera. Dlatego wszystko, co ma przetrwać kliknięcie, trzymamy w
st.session_state (patrz KROK 2).
"""

import time

import streamlit as st

# ════════════════════════════════════════════════════════════════════════════
# KROK 1: Konfiguracja strony
# ════════════════════════════════════════════════════════════════════════════
# Musi być pierwszym poleceniem Streamlita w pliku. Ustawia tytuł karty
# w przeglądarce, ikonę i szerokość treści ("centered" albo "wide").
st.set_page_config(page_title="Hello Streamlit", page_icon="👋", layout="centered")


# ════════════════════════════════════════════════════════════════════════════
# KROK 2: Pamięć aplikacji — st.session_state
# ════════════════════════════════════════════════════════════════════════════
# st.session_state to słownik, który PRZEŻYWA ponowne przebiegi skryptu.
# Każdy użytkownik (karta przeglądarki) ma własną, oddzielną kopię.
DEFAULTS = {
    "screen": "start",   # który ekran pokazujemy — to serce nawigacji
    "name": "",          # tekst wpisany przez użytkownika
    "color": "blue",     # wybór z listy
    "size": 3,           # wartość suwaka
    "clicks": 0,         # licznik — pokazuje, że wartość przetrwa kliknięcie
    "anim_done": False,  # czy animacja już się odegrała
    # Kopia danych z formularza — wyjaśnienie w KROKU 7a.
    "saved": {"name": "", "color": "blue", "size": 3},
}

# setdefault wpisuje wartość TYLKO wtedy, gdy klucza jeszcze nie ma.
# Dzięki temu przy każdym kolejnym przebiegu NIE nadpisujemy tego,
# co użytkownik zdążył już zmienić.
for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)


# ════════════════════════════════════════════════════════════════════════════
# KROK 3: Nawigacja między ekranami
# ════════════════════════════════════════════════════════════════════════════
# Streamlit sam z siebie nie ma „stron". Robimy je sami: w session_state
# trzymamy nazwę aktualnego ekranu, a na końcu pliku (KROK 9) wywołujemy
# funkcję odpowiadającą tej nazwie.
def go(screen: str) -> None:
    """Przełącza ekran. Używana jako callback przycisku (on_click)."""
    st.session_state.screen = screen


def count_click() -> None:
    st.session_state.clicks += 1


# ════════════════════════════════════════════════════════════════════════════
# KROK 4: Dane oddzielone od kodu
# ════════════════════════════════════════════════════════════════════════════
# W grze wszystkie liczby i teksty siedzą w osobnym pliku game_data.py.
# Dzięki temu zmiana rozgrywki nie wymaga dotykania kodu interfejsu.
COLORS = [
    {"key": "blue", "label": "Niebieski", "hex": "#3b82f6"},
    {"key": "orange", "label": "Pomarańczowy", "hex": "#f97316"},
    {"key": "green", "label": "Zielony", "hex": "#22c55e"},
]


def color_of(key: str) -> dict:
    """Znajduje słownik koloru po jego kluczu."""
    return next(c for c in COLORS if c["key"] == key)


# ════════════════════════════════════════════════════════════════════════════
# KROK 5: Własna grafika jako SVG
# ════════════════════════════════════════════════════════════════════════════
# Streamlit nie ma „płótna" do rysowania. W grze rysujemy sondę i planety
# tak: sklejamy tekst SVG w Pythonie i wstawiamy go jako HTML.
def ball_svg(color_hex: str, radius: int, y: int = 60) -> str:
    """Zwraca kod SVG z kółkiem — im większy suwak, tym większe kółko."""
    return (
        f'<svg viewBox="0 0 200 160" width="200" height="160">'
        f'<circle cx="100" cy="{y}" r="{radius * 8}" fill="{color_hex}" />'
        f"</svg>"
    )


# ════════════════════════════════════════════════════════════════════════════
# KROK 6: Ekran powitalny — tekst i przyciski
# ════════════════════════════════════════════════════════════════════════════
def screen_start() -> None:
    st.title("👋 Hello, Streamlit!")

    # Kilka sposobów wypisania tekstu:
    st.write("st.write — uniwersalne, przyjmie tekst, liczbę, tabelę…")
    st.markdown("st.markdown — rozumie **pogrubienie** i *kursywę*.")
    st.caption("st.caption — drobny, szary podpis.")
    st.info("st.info — niebieska ramka. Są też st.warning, st.error, st.success.")

    # st.columns dzieli stronę na kolumny obok siebie.
    # Zwraca listę, którą można od razu rozpakować do zmiennych.
    left, right = st.columns(2)

    # Przycisk z callbackiem: gdy użytkownik kliknie, Streamlit najpierw
    # wywoła funkcję z on_click (przekazując jej args), a DOPIERO POTEM
    # uruchomi skrypt od nowa. Dlatego nowy ekran pojawi się od razu.
    left.button(
        "Przejdź do formularza",
        type="primary",
        use_container_width=True,
        on_click=go,
        args=("form",),
    )
    right.button("Policz kliknięcia", use_container_width=True, on_click=count_click)

    # Ta wartość rośnie, mimo że skrypt startuje od zera — bo siedzi
    # w session_state, a nie w zwykłej zmiennej.
    st.write(f"Liczba kliknięć: **{st.session_state.clicks}**")


# ════════════════════════════════════════════════════════════════════════════
# KROK 7: Formularz — widgety podpięte do session_state
# ════════════════════════════════════════════════════════════════════════════
def screen_form() -> None:
    st.subheader("Widgety")

    # Sztuczka używana w całej grze: key="name" sprawia, że widget
    # AUTOMATYCZNIE zapisuje swoją wartość do st.session_state["name"]
    # i sam odtwarza ją po każdym przebiegu. Nie trzeba niczego przypisywać.
    st.text_input("Jak masz na imię?", key="name", placeholder="np. Ala")
    preview, controls = st.columns([2, 3])

    with controls:  # "with" kieruje wszystko poniżej do tej kolumny
        # Lista wyboru pokazuje KLUCZE, ale format_func decyduje,
        # jaki tekst zobaczy użytkownik. W grze tak wyświetlamy
        # nazwę opcji razem z jej masą.
        st.selectbox(
            "Kolor",
            [c["key"] for c in COLORS],
            format_func=lambda key: color_of(key)["label"],
            key="color",
        )

        # DRUGI SPOSÓB zapamiętywania: bez key=, za to zapisujemy to,
        # co widget ZWRACA. Wartość z session_state podajemy jako value,
        # więc po ponownym przebiegu suwak wraca w to samo miejsce.
        st.session_state.size = st.slider(
            "Rozmiar", min_value=1, max_value=5, value=st.session_state.size
        )

        # st.radio z horizontal=True — tak w grze wybiera się miejsce lądowania.
        st.radio("Przykładowy wybór", ["A", "B", "C"], horizontal=True, key="choice")

    with preview:
        st.caption("PODGLĄD")
        color = color_of(st.session_state.color)
        # unsafe_allow_html=True jest konieczne, żeby Streamlit potraktował
        # tekst jako HTML/SVG, a nie wypisał go dosłownie.
        # Używaj go tylko dla treści, którą sam tworzysz w kodzie.
        st.markdown(
            f'<div style="text-align:center">{ball_svg(color["hex"], st.session_state.size)}</div>',
            unsafe_allow_html=True,
        )

    # st.container(border=True) rysuje ramkę wokół grupy elementów.
    with st.container(border=True):
        st.markdown(f"**Pasek postępu** — {st.session_state.size} / 5")
        st.progress(st.session_state.size / 5)  # oczekuje wartości 0.0–1.0

    # Walidacja: przycisk można wyłączyć, zamiast chować.
    ready = bool(st.session_state.name.strip())
    if not ready:
        st.error("Wpisz imię, aby ruszyć dalej.")

    back, start = st.columns(2)
    back.button("Wróć", use_container_width=True, on_click=go, args=("start",))
    start.button(
        "Uruchom animację",
        type="primary",
        use_container_width=True,
        disabled=not ready,
        on_click=start_animation,
    )


def start_animation() -> None:
    """Zapisuje dane z formularza i przechodzi do animacji."""
    # ════════════════════════════════════════════════════════════════════════
    # KROK 7a: PUŁAPKA — Streamlit kasuje dane znikających widgetów
    # ════════════════════════════════════════════════════════════════════════
    # Klucz podpięty do widgetu (key="name") żyje tylko tak długo, jak długo ten
    # widget jest rysowany na stronie. Gdy przejdziemy na inny ekran, Streamlit
    # usunie go z session_state — i na podsumowaniu imię byłoby już puste!
    #
    # Dlatego w momencie kliknięcia przepisujemy wartości do WŁASNEGO klucza,
    # który nie należy do żadnego widgetu. Gra robi dokładnie to samo:
    # w chwili startu misji liczy wynik i chowa go w session_state.result.
    st.session_state.saved = {
        "name": st.session_state.name,
        "color": st.session_state.color,
        "size": st.session_state.size,
    }
    st.session_state.anim_done = False
    st.session_state.screen = "animation"


# ════════════════════════════════════════════════════════════════════════════
# KROK 8: Animacja — st.empty() i pętla
# ════════════════════════════════════════════════════════════════════════════
def screen_animation() -> None:
    st.subheader("Animacja")

    # Czytamy z kopii (saved), a nie z klucza widgetu — widgetów formularza
    # nie ma już na tym ekranie, więc ich klucze przestały istnieć.
    saved = st.session_state.saved
    color = color_of(saved["color"])

    # st.empty() rezerwuje puste miejsce na stronie. Można je potem
    # nadpisywać w kółko — treść PODMIENIA się zamiast dopisywać niżej.
    slot = st.empty()
    caption = st.empty()

    # Cała animacja dzieje się w JEDNYM przebiegu skryptu: rysujemy klatkę,
    # czekamy chwilę, rysujemy następną. Flaga anim_done pilnuje, żeby przy
    # kolejnych przebiegach (np. po kliknięciu przycisku) animacja nie ruszała
    # od nowa — wtedy od razu pokazujemy ostatnią klatkę.
    if not st.session_state.anim_done:
        steps = 20
        for frame in range(steps):
            slot.markdown(
                f'<div style="text-align:center">'
                f'{ball_svg(color["hex"], saved["size"], y=10 + frame * 5)}</div>',
                unsafe_allow_html=True,
            )
            caption.caption(f"Klatka {frame + 1} z {steps}…")
            time.sleep(0.05)  # bez tego wszystko mignęłoby za szybko
        st.session_state.anim_done = True

    # Klatka końcowa — rysowana zawsze, także po zakończonej animacji.
    slot.markdown(
        f'<div style="text-align:center">'
        f'{ball_svg(color["hex"], saved["size"], y=105)}</div>',
        unsafe_allow_html=True,
    )
    caption.caption("Gotowe!")

    # Nawigacja tylko po kliknięciu — aplikacja nie przeskakuje sama z siebie.
    st.button(
        "Zobacz podsumowanie",
        type="primary",
        use_container_width=True,
        on_click=go,
        args=("summary",),
    )


# ════════════════════════════════════════════════════════════════════════════
# KROK 9: Podsumowanie — odczyt zebranych danych
# ════════════════════════════════════════════════════════════════════════════
def screen_summary() -> None:
    st.subheader("Podsumowanie")

    # Znowu czytamy z kopii — dzięki temu dane przetrwały zmianę ekranu.
    saved = st.session_state.saved

    with st.container(border=True):
        st.markdown(f"Cześć, **{saved['name']}**!")
        st.markdown(f"- Kolor: **{color_of(saved['color'])['label']}**")
        st.markdown(f"- Rozmiar: **{saved['size']}**")
        st.markdown(f"- Kliknięcia na starcie: **{st.session_state.clicks}**")

    st.caption(
        "Zajrzyj teraz w panel boczny: klucze „name” i „color” są tam puste, "
        "bo Streamlit skasował je razem z widgetami formularza. Imię i kolor "
        "widzisz powyżej tylko dlatego, że zawczasu skopiowaliśmy je do „saved”."
    )

    # st.table wyświetla słownik list jako tabelę.
    st.table({"Mechanizm": ["session_state", "on_click", "st.empty"],
              "Do czego służy": ["pamięć", "reakcja na klik", "animacja"]})

    again, home = st.columns(2)
    again.button("Jeszcze raz", type="primary", use_container_width=True,
                 on_click=go, args=("form",))
    home.button("Na początek", use_container_width=True, on_click=go, args=("start",))


# ════════════════════════════════════════════════════════════════════════════
# KROK 10: Router — tu decyduje się, co zobaczy użytkownik
# ════════════════════════════════════════════════════════════════════════════
# Słownik zamiast długiego if/elif: nazwa ekranu → funkcja go rysująca.
# Ta część wykonuje się przy KAŻDYM przebiegu skryptu, czyli po każdym kliknięciu.
SCREENS = {
    "start": screen_start,
    "form": screen_form,
    "animation": screen_animation,
    "summary": screen_summary,
}

SCREENS[st.session_state.screen]()

# Pasek boczny (st.sidebar) rysuje się z lewej strony, niezależnie od ekranu.
with st.sidebar:
    st.markdown("### Co się dzieje pod spodem")
    st.write(f"Aktualny ekran: `{st.session_state.screen}`")
    st.caption("Każde kliknięcie uruchamia ten plik od nowa od pierwszej linijki.")
    st.json({k: st.session_state[k] for k in DEFAULTS})
