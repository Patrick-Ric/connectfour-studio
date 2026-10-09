"""Hilfe + Info für ConnectFour Studio ( ausgelagert 01.10.2026 ).

Enthält die kompletten Hilfe-/Info-Dialoge (show_help/show_info), damit
connectfour_studio.py schlank bleibt. Funktionen bekommen die App als
`app` übergeben (nutzt app._stone_icon() + ENGINE_NAME aus der App).

Sprachen: HELP = {"de": {...}, "en": {...}}. Aktuell ist Deutsch
vollständig, Englisch als Gerüst (Platzhalter-Texte, werden später
übersetzt). Auswahl per lang="de"/"en" in show_help/show_info.
"""

import tkinter as tk
from tkinter import ttk

HELP_LANGS = ("de", "en", "es", "fr", "nl", "it")

# Fenstertexte von show_help/show_info je Sprache (Fallback Deutsch).
_UI = {
    "copy": {"de": "Kopieren", "en": "Copy", "es": "Copiar", "fr": "Copier", "nl": "Kopiëren",
             "it": "Copia"},
    "close": {"de": "Schließen", "en": "Close", "es": "Cerrar",
              "fr": "Fermer", "nl": "Sluiten", "it": "Chiudi"},
    "help_title": {"de": "ConnectFour Studio – Hilfe",
                   "en": "ConnectFour Studio – Help",
                   "es": "ConnectFour Studio – Ayuda",
                   "fr": "ConnectFour Studio – Aide",
                   "nl": "ConnectFour Studio – Help",
                   "it": "ConnectFour Studio – Aiuto"},
    "find_label": {"de": "Suchen:", "en": "Find:", "es": "Buscar:",
                   "fr": "Rechercher :", "nl": "Zoeken:", "it": "Cerca:"},
    "not_found": {"de": "nichts gefunden", "en": "not found",
                  "es": "no se encontró", "fr": "introuvable",
                  "nl": "niets gevonden", "it": "non trovato"},
    "find_btn": {"de": "Suchen", "en": "Find", "es": "Buscar",
                 "fr": "Rechercher", "nl": "Zoeken", "it": "Cerca"},
}


def _ui(key, lang):
    d = _UI[key]
    return d.get(lang, d["de"])

INFO_TEXT = {
    "de": ("ConnectFour Studio\n"
           "Engine: BitBully von Markus Thill\n"
           "Python-Modul bitbully, C++-Kern\n"
           "Suchverfahren: iterative Vertiefung, MTD(f)/Null-Window,\n"
           "Bitboards, Transposition Table, 12-ply-dist-Buch\n"
           "GUI: Python + Tkinter (+ Pillow)\n"
           "Idee & Tests: Patrick Götz, Umsetzung: KI\n"
           "Open Source (GNU AGPL v3)"),
    "en": ("ConnectFour Studio\n"
           "Engine: BitBully by Markus Thill\n"
           "Python module bitbully, C++ core\n"
           "Search: iterative deepening, MTD(f)/null-window,\n"
           "bitboards, transposition table, 12-ply-dist book\n"
           "GUI: Python + Tkinter (+ Pillow)\n"
           "Idea & testing: Patrick Götz, implementation: AI\n"
           "Open source (GNU AGPL v3)"),
    "es": ("ConnectFour Studio\n"
           "Motor: BitBully by Markus Thill\n"
           "Módulo de Python bitbully, núcleo en C++\n"
           "Búsqueda: profundización iterativa, MTD(f)/null-window,\n"
           "bitboards, tabla de transposición, libro 12-ply-dist\n"
           "GUI: Python + Tkinter (+ Pillow)\n"
           "Idea y pruebas: Patrick Götz, implementación: IA\n"
           "Código abierto (GNU AGPL v3)"),
    "fr": ("ConnectFour Studio\n"
           "Moteur : BitBully by Markus Thill\n"
           "Module Python bitbully, noyau C++\n"
           "Recherche : approfondissement itératif, MTD(f)/null-window,\n"
           "bitboards, table de transposition, livre 12-ply-dist\n"
           "GUI : Python + Tkinter (+ Pillow)\n"
           "Idée et tests : Patrick Götz, réalisation : IA\n"
           "Logiciel libre (GNU AGPL v3)"),
    "nl": ("ConnectFour Studio\n"
           "Engine: BitBully by Markus Thill\n"
           "Python-module bitbully, C++-kern\n"
           "Zoeken: iteratieve verdieping, MTD(f)/null-window,\n"
           "bitboards, transpositietabel, 12-ply-dist book\n"
           "GUI: Python + Tkinter (+ Pillow)\n"
           "Idee en tests: Patrick Götz, uitvoering: AI\n"
           "Open source (GNU AGPL v3)"),
    "it": ("ConnectFour Studio\n"
           "Motore: BitBully by Markus Thill\n"
           "Modulo Python bitbully, nucleo C++\n"
           "Ricerca: approfondimento iterativo, MTD(f)/null-window,\n"
           "bitboard, tabella di trasposizione, libro 12-ply-dist\n"
           "GUI: Python + Tkinter (+ Pillow)\n"
           "Idea e test: Patrick Götz, realizzazione: IA\n"
           "Software libero (GNU AGPL v3)"),
}


def show_info(app, lang="de"):
    """Info-Dialog mit kopierbarem Text (Strg+C / Auswahl kopierbar)."""
    lang = lang if lang in HELP_LANGS else "de"
    info_txt = INFO_TEXT[lang]
    win = tk.Toplevel(app)
    import cfs_lang
    win.title(cfs_lang.t("info_title", lang))
    win.geometry("560x260")
    txt = tk.Text(win, wrap="word", width=66, height=12)
    sb = ttk.Scrollbar(win, command=txt.yview)
    txt.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    txt.pack(fill="both", expand=True, padx=8, pady=8)
    txt.insert("end", info_txt)
    txt.config(state="normal")  # kopierbar: Auswahl + Strg+C moeglich
    btn = ttk.Frame(win)
    btn.pack(pady=(0, 8))
    ttk.Button(btn, text=_ui("copy", lang),
               command=lambda: (win.clipboard_clear(),
                                win.clipboard_append(txt.get("1.0", "end-1c")))).pack(side="left", padx=4)
    ttk.Button(btn, text=_ui("close", lang),
               command=win.destroy).pack(side="left", padx=4)


def show_help(app, lang="de"):
    """Hilfe: scrollbare Seite (Fliesstext, blaue Links)."""
    lang = lang if lang in HELP_LANGS else "de"
    win = tk.Toplevel(app)
    win.title(_ui("help_title", lang))
    win.geometry("660x560")
    # Suchleiste oben: Textfeld + Button + Strg-F (Wunsch Patrick).
    # Sucht vorwaerts ab Cursor (wrap), Treffer gelb, Enter = weiter.
    findbar = ttk.Frame(win)
    findbar.pack(fill="x", padx=8, pady=(8, 0))
    ttk.Label(findbar, text=_ui("find_label", lang)).pack(side="left")
    find_var = tk.StringVar(value="")
    find_ent = ttk.Entry(findbar, textvariable=find_var, width=28)
    find_ent.pack(side="left", padx=(4, 4))
    find_info = tk.StringVar(value="")
    ttk.Label(findbar, textvariable=find_info).pack(side="left", padx=(4, 0))
    txt = tk.Text(win, wrap="word", width=76, height=28)
    sb = ttk.Scrollbar(win, command=txt.yview)
    txt.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    txt.pack(fill="both", expand=True, padx=8, pady=8)

    def _find_next(_ev=None):
        txt.tag_remove("findhit", "1.0", "end")
        needle = find_var.get()
        if not needle:
            find_info.set("")
            return "break"
        start = txt.index("insert")
        pos = txt.search(needle, start, nocase=True, stopindex="end")
        if not pos:
            pos = txt.search(needle, "1.0", nocase=True, stopindex="end")
        if not pos:
            find_info.set(_ui("not_found", lang))
            return "break"
        last = f"{pos}+{len(needle)}c"
        txt.tag_add("findhit", pos, last)
        txt.tag_config("findhit", background="yellow")
        txt.mark_set("insert", last)
        txt.see(pos)
        find_info.set("")
        try:
            find_ent.focus_set()
        except Exception:
            pass
        return "break"

    find_btn = ttk.Button(findbar, text=_ui("find_btn", lang),
                          command=_find_next)
    find_btn.pack(side="left")
    find_ent.bind("<Return>", _find_next)
    find_ent.bind("<KP_Enter>", _find_next)
    win.bind("<Control-f>", lambda e: (find_ent.focus_set(), "break")[1])
    win.bind("<Control-F>", lambda e: (find_ent.focus_set(), "break")[1])

    # Text-Zoom (Wunsch Patrick 04.10.2026): Strg + / Strg - / Strg 0
    # plus A+/A--Buttons und Strg+Mausrad. Skaliert Fliesstext,
    # Ueberschriften und Mono-Bloecke gemeinsam.
    # Hinweis: _mono_fam wird weiter unten (vor der Rendering-Schleife)
    # definiert; _apply_zoom() laeuft erst danach.
    _zoom = {"f": 1.0}
    _zoom_basen = {"body": 10, "h": 13, "sh": 11, "b": 10, "mono": 9}
    zoom_info = tk.StringVar(value="100%")

    def _apply_zoom():
        f = _zoom["f"]
        bbody = max(7, round(_zoom_basen["body"] * f))
        bh = max(8, round(_zoom_basen["h"] * f))
        bsh = max(8, round(_zoom_basen["sh"] * f))
        bb = max(7, round(_zoom_basen["b"] * f))
        bm = max(7, round(_zoom_basen["mono"] * f))
        try:
            txt.configure(font=("TkDefaultFont", bbody))
        except Exception:
            pass
        try:
            txt.tag_config("h", font=("TkDefaultFont", bh, "bold"),
                           foreground="#1e3a8a")
        except Exception:
            pass
        try:
            txt.tag_config("sh", font=("TkDefaultFont", bsh, "bold"),
                           foreground="#1e3a8a")
        except Exception:
            pass
        try:
            txt.tag_config("b", font=("TkDefaultFont", bb, "bold"))
        except Exception:
            pass
        try:
            txt.tag_config("mono", font=(_mono_fam[0], bm))
        except Exception:
            pass
        for _in in list(_table_inners):
            try:
                _in.configure(font=(_mono_fam[0], bm))
            except Exception:
                pass
        try:
            zoom_info.set(f"{round(f * 100)}%")
        except Exception:
            pass

    def _zoom_in(_ev=None):
        _zoom["f"] = min(1.8, round(_zoom["f"] + 0.1, 2))
        _apply_zoom()
        return "break"

    def _zoom_out(_ev=None):
        _zoom["f"] = max(0.7, round(_zoom["f"] - 0.1, 2))
        _apply_zoom()
        return "break"

    def _zoom_reset(_ev=None):
        _zoom["f"] = 1.0
        _apply_zoom()
        return "break"

    try:
        ttk.Button(findbar, text="A+", width=3, command=_zoom_in).pack(side="left", padx=(8, 0))
        ttk.Button(findbar, text="A-", width=3, command=_zoom_out).pack(side="left")
        ttk.Label(findbar, textvariable=zoom_info, width=5).pack(side="left")
    except Exception:
        pass
    for _seq, _fn in (("<Control-plus>", _zoom_in), ("<Control-KP_Add>", _zoom_in),
                      ("<Control-minus>", _zoom_out), ("<Control-KP_Subtract>", _zoom_out),
                      ("<Control-0>", _zoom_reset), ("<Control-KP_0>", _zoom_reset)):
        try:
            win.bind(_seq, _fn)
        except Exception:
            pass
    try:
        win.bind("<Control-MouseWheel>",
                 lambda e: _zoom_in() if getattr(e, "delta", 0) > 0 else _zoom_out())
    except Exception:
        pass
    try:
        win.bind("<Control-Button-4>", lambda e: _zoom_in())
        win.bind("<Control-Button-5>", lambda e: _zoom_out())
    except Exception:
        pass

    yellow_icon = app._stone_icon("yellow", 22)
    red_icon = app._stone_icon("red", 22)
    txt.image_create("end", image=yellow_icon)
    txt.insert("end", "  ")
    txt.image_create("end", image=red_icon)
    txt.insert("end", "\n")
    txt._icons = (yellow_icon, red_icon)  # Referenzen behalten

    # Zoom-State: muss VOR _apply_zoom()/table()/der Rendering-Schleife
    # existieren. _apply_zoom() selbst wird erst nach dem Rendern (nach
    # der Schleife) einmal aufgerufen, sonst NameError.
    _mono_fam = ["DejaVu Sans Mono"]
    _table_inners = []
    try:
        import tkinter.font as _tkfont
        for _c in ("DejaVu Sans Mono", "Liberation Mono",
                   "Courier New", "Courier"):
            if _c in set(_tkfont.families()):
                _mono_fam = [_c]
                break
    except Exception:
        pass

    anchors = {}
    link_no = [0]  # eindeutige Tag-Namen (gleiche Ziele mehrfach!)

    def head(name, title):
        txt.insert("end", "\n" + title + "\n", "h")
        # Titelposition immer auch als Textindex merken – dient als
        # Fallback in goto(), falls die Marke verloren geht.
        anchors[name] = txt.index("end-2l")
        try:
            txt.mark_set(f"anker_{name}", "end-2l")
        except Exception:
            pass

    def sub(name, title):
        # Untertitel (Fix 04.10.2026): kleinere Ueberschrift _innerhalb_
        # eines Themas (z.B. 3-Schritte-Zugwahl unter "Die Spielstufen").
        # Eigener Anker, damit alte Links (Inhalt/Querverweise) weiter
        # springen – im Inhaltsverzeichnis steht nur das Oberthema.
        txt.insert("end", "\n" + title + "\n", "sh")
        anchors[name] = txt.index("end-2l")
        try:
            txt.mark_set(f"anker_{name}", "end-2l")
        except Exception:
            pass

    def para(*parts):
        for p in parts:
            if isinstance(p, tuple):
                if len(p) == 3 and p[0] == "LINK":
                    # Datentupel aus HELP_CONTENT -> echter Link.
                    _, text, target = p
                    link(text, target)
                elif len(p) == 2:
                    text, tag = p
                    if isinstance(tag, (list, tuple)):
                        for t in tag:
                            txt.insert("end", text, t)
                    else:
                        txt.insert("end", text, tag)
                else:
                    txt.insert("end", str(p))
            else:
                txt.insert("end", p)
        txt.insert("end", "\n\n")

    def goto(name):
        mark_name = f"anker_{name}"
        try:
            if mark_name not in txt.mark_names() and name in anchors:
                # Marke ist weg – auf die gemerkte Titelposition neu setzen
                txt.mark_set(mark_name, anchors[name])
            # Fix 02.10.2026: Ziel an den OBEREN Fensterrand holen
            # (see() scrollt nur bis sichtbar – bei nahem Ziel kein
            # sichtbarer Sprung, wirkte wie "Link tot").
            # yview(mark) setzt die Marke an den oberen Rand.
            try:
                txt.yview(mark_name)
            except Exception:
                txt.see(mark_name)
        except Exception:
            try:
                txt.see(anchors[name])
            except Exception:
                pass

    def link(text, target):
        link_no[0] += 1
        tag = f"lk_{target}_{link_no[0]}"
        txt.tag_config(tag, foreground="blue", underline=True)
        # Fix 02.10.2026: KEIN tag_bind (synthetische Button-Events
        # erreichen Tag-Bindings unter Xvfb/X11 nicht zuverlaessig) –
        # stattdessen EIN zentrales Widget-Binding, das per
        # "@x,y"-Koordinate das Link-Tag bestimmt (auch fuer echte
        # Mausklicks robust). target per Default-Arg (kein
        # Spaetbindungs-Bug).
        txt.insert("end", text, tag)
        _link_tags[tag] = target

    # Zentraler Link-Klick (Fix 02.10.2026, s. link()): bestimmt aus der
    # Klick-Koordinate das oberste lk_*-Tag und springt dessen Ziel an.
    # Cursor-Feedback ebenfalls zentral (Enter/Motion statt pro Tag).
    def _help_click(ev):
        try:
            idx = txt.index(f"@{ev.x},{ev.y}")
        except Exception:
            return None
        try:
            names = txt.tag_names(idx)
        except Exception:
            return None
        for tg in names:
            if tg in _link_tags:
                goto(_link_tags[tg])
                return "break"
        return None

    def _help_motion(ev):
        try:
            idx = txt.index(f"@{ev.x},{ev.y}")
            names = txt.tag_names(idx)
        except Exception:
            return None
        try:
            if any(tg in _link_tags for tg in names):
                txt.config(cursor="hand2")
            else:
                txt.config(cursor="")
        except Exception:
            pass
        return None

    _link_tags = {}
    txt.bind("<Button-1>", _help_click)
    txt.bind("<Motion>", _help_motion, "+")

    txt.tag_config("h", font=("TkDefaultFont", 13, "bold"),
                   foreground="#1e3a8a")
    txt.tag_config("b", font=("TkDefaultFont", 10, "bold"))
    try:
        txt.tag_config("sh", font=("TkDefaultFont", 11, "bold"),
                       foreground="#1e3a8a")
    except Exception:
        pass
    # Monospace-Block (Fix 04.10.2026): Spielstärke-Tabelle + Kreuztabelle als
    # Festschrift (dicktengleich). WICHTIG: TkFixedFont ist unter Linux
    # KEINE echte Festschrift (space=3px, 0=7px, X=8px -> Spalten schief!).
    # Darum DejaVu Sans Mono / Courier / Liberation Mono bevorzugen.
    # Hinweis: wrap="none" gibt es als TAG-Option nicht (nur Widget) ->
    # kein tag_config(wrap)! Die Tabellenzeilen sind kuerzer als die
    # Fensterbreite (max 46 Zeichen < 76), so bricht nichts um.
    _mono_ok = False
    for _fam in ("DejaVu Sans Mono", "Liberation Mono", "Courier", "Courier New"):
        try:
            txt.tag_config("mono", font=(_fam, 9))
            _mono_ok = True
            break
        except Exception:
            continue
    if not _mono_ok:
        try:
            txt.tag_config("mono", font=("TkFixedFont", 9))
        except Exception:
            pass

    # Einteilige Kreuztabelle (Fix 04.10.2026): Die 14x14-Tabelle passt
    # nicht in die 76-Zeichen-Fliesstextbreite (mit Namen ~116 Zeichen).
    # Darum wird sie als eingebettetes, horizontal scrollbares Textfeld
    # (wrap="none") in den Hilfetext gesetzt – ein Stueck, mit
    # Stufennamen + (p,s,w) vor jeder Zeile.
    _KREUZ_ALL = {
        "de": ["Zufall", "Sehr Leicht", "Leicht", "Anfänger",
               "Fortgeschritten", "Taktiker", "Mittel", "Fordernd",
               "Schwer", "Sehr Schwer", "Experte", "Meister",
               "Starker Meister", "Perfekt"],
        "en": ["Random", "Very Easy", "Easy", "Beginner",
               "Advanced", "Tactician", "Intermediate", "Demanding",
               "Hard", "Very Hard", "Expert", "Master",
               "Strong Master", "Perfect"],
        "es": ["Aleatorio", "Muy fácil", "Fácil", "Principiante",
               "Avanzado", "Táctico", "Intermedio", "Exigente",
               "Difícil", "Muy difícil", "Experto", "Maestro",
               "Maestro fuerte", "Perfecto"],
        "fr": ["Aléatoire", "Très facile", "Facile", "Débutant",
               "Avancé", "Tacticien", "Intermédiaire", "Exigeant",
               "Difficile", "Très difficile", "Expert", "Maître",
               "Maître supérieur", "Parfait"],
        "nl": ["Willekeurig", "Zeer makkelijk", "Makkelijk", "Beginner",
               "Gevorderd", "Tacticus", "Gemiddeld", "Veeleisend",
               "Moeilijk", "Zeer moeilijk", "Expert", "Meester",
               "Sterke meester", "Perfect"],
        "it": ["Casuale", "Molto facile", "Facile", "Principiante",
               "Avanzato", "Tattico", "Intermedio", "Impegnativo",
               "Difficile", "Molto difficile", "Esperto", "Maestro",
               "Maestro forte", "Perfetto"],
    }
    _KREUZ_NAMEN = _KREUZ_ALL.get(lang, _KREUZ_ALL["de"])
    _KREUZ_PSW = ["", "(25,0,0)", "(40,0,0)", "(50,0,0)",
                  "(20,1,1)", "(0,3,3)", "(50,1,1)", "(55,1,1)",
                  "(65,1,1)", "(70,2,2)", "(80,2,2)", "(85,3,3)",
                  "(92,4,4)", "(100,-,-)"]
    # Punkte Zeile vs Spalte, aus 200 (Stand 03.10.2026, NoRemis).
    # Quelle: elo_run/kreuztabelle_14final_95.txt. None = Diagonale.
    _KREUZ_WERTE = [
        [None, 55.0, 20.0, 16.0, 6.5, 1.0, 2.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [145.0, None, 69.5, 51.0, 35.5, 10.5, 10.5, 10.0, 6.5, 4.0, 0.5, 1.5, 0.0, 0.0],
        [180.0, 130.5, None, 75.5, 53.5, 29.5, 25.0, 15.5, 13.5, 5.5, 3.0, 2.5, 4.5, 2.0],
        [184.0, 149.0, 124.5, None, 63.0, 50.5, 33.0, 37.0, 28.5, 7.0, 6.5, 9.5, 5.0, 2.0],
        [193.5, 164.5, 146.5, 137.0, None, 72.5, 37.0, 33.0, 28.0, 7.5, 10.0, 6.0, 3.0, 0.5],
        [199.0, 189.5, 170.5, 149.5, 127.5, None, 75.0, 65.0, 50.5, 21.0, 12.5, 5.5, 0.5, 0.0],
        [198.0, 189.5, 175.0, 167.0, 163.0, 125.0, None, 85.0, 70.5, 49.5, 29.0, 21.0, 10.5, 11.0],
        [200.0, 190.0, 184.5, 163.0, 167.0, 135.0, 115.0, None, 80.0, 52.5, 39.5, 23.5, 22.0, 22.0],
        [199.0, 193.5, 186.5, 171.5, 172.0, 149.5, 129.5, 120.0, None, 67.0, 54.0, 37.0, 33.0, 31.5],
        [200.0, 196.0, 194.5, 193.0, 192.5, 179.0, 150.5, 147.5, 133.0, None, 83.5, 51.5, 46.0, 36.5],
        [200.0, 199.5, 197.0, 193.5, 190.0, 187.5, 171.0, 160.5, 146.0, 116.5, None, 79.0, 68.5, 51.5],
        [200.0, 198.5, 197.5, 190.5, 194.0, 194.5, 179.0, 176.5, 163.0, 148.5, 121.0, None, 85.0, 62.0],
        [200.0, 200.0, 195.5, 195.0, 197.0, 199.5, 189.5, 178.0, 167.0, 154.0, 131.5, 115.0, None, 81.0],
        [200.0, 200.0, 198.0, 198.0, 199.5, 200.0, 189.0, 178.0, 168.5, 163.5, 148.5, 138.0, 119.0, None],
    ]

    # Kreuztabelle als reiner Mono-Text (Fix 04.10.2026):
    # Kein eingebettetes Widget, kein Scrollbalken. Zwei Bloecke mit
    # Stufennamen + (p,s,w) vor jeder Zeile (Wunsch Patrick). Jede Zeile
    # max 74 Zeichen < 76 Fensterbreite -> kein Umbruch, Spalten stehen
    # uebereinander (dicktengleiche Mono-Schrift).
    def _kreuz_block(cols):
        lines = [" " * 32 + "".join(f"{c:>5d} " for c in cols).rstrip()]
        for i, (nm, ps) in enumerate(zip(_KREUZ_NAMEN, _KREUZ_PSW), start=1):
            row = f"{i:>2d} {nm:<18s} {ps:<9s} " + "".join(
                ("  X   " if _KREUZ_WERTE[i - 1][c - 1] is None
                 else f"{_KREUZ_WERTE[i - 1][c - 1]:5.1f} ")
                for c in cols).rstrip()
            lines.append(row)
        return "\n".join(lines)

    def table(kind):
        # Historisch: eingebettetes Textfeld. Entfernt 04.10.2026.
        # Fällt auf zwei normale Mono-Bloecke zurück (1-7, 8-14).
        if kind == "kreuz14":
            txt.insert("end", _kreuz_block([1, 2, 3, 4, 5, 6, 7]) + "\n\n", "mono")
            txt.insert("end", _kreuz_block([8, 9, 10, 11, 12, 13, 14]) + "\n\n", "mono")
            return
        txt.insert("end", str(kind) + "\n\n", "mono")

    for kind, *rest in HELP_CONTENT.get(lang, HELP_CONTENT["de"]):
        if kind == "head":
            head(*rest)
        elif kind == "sub":
            sub(*rest)
        elif kind == "para":
            para(*rest)
        elif kind == "table":
            table(*rest)
        elif kind == "mono":
            # Festschrift-Block (nur noch Spielstärke-Tabelle): kurz genug, bricht
            # nicht um (max ~36 Zeichen < 76).
            txt.insert("end", (rest[0] if rest else "") + "\n\n", "mono")

    # Zoom-Basisschriften einmal setzen (nach dem Rendern, damit Tags
    # und Tabelle existieren). Faktor steht noch auf 1.0.
    try:
        _apply_zoom()
    except Exception:
        pass

    # Read-only statt state="disabled" (Fix 02.10.2026): Ein disabled
    # Text-Widget schluckt Tag-Klicks (Button-1) je nach                   # Tk-Version/WM – Links sahen klickbar aus, sprangen aber nicht.
    # Stattdessen: normal lassen, nur Tasten filtern (Kopieren mit
    # Strg+C/Mausauswahl bleibt erlaubt, Tippen wird geblockt).
    def _ro_key(ev):
        try:
            ks = ev.keysym
        except Exception:
            return "break"
        if ks in ("c", "C", "Insert") and (int(getattr(ev, "state", 0)) & 0x4):
            return None  # Strg+C / Strg+Insert = Kopieren erlauben
        if ks in ("Shift_L", "Shift_R", "Control_L", "Control_R",
                  "Alt_L", "Alt_R", "Caps_Lock", "Num_Lock",
                  "Left", "Right", "Up", "Down", "Home", "End",
                  "Prior", "Next"):
            return None  # Navigation/Marker erlauben
        return "break"
    txt.bind("<Key>", _ro_key)
    try:
        txt.bind("<<Paste>>", lambda e: "break")
        txt.bind("<<Paste-Selection>>", lambda e: "break")
        txt.bind("<Button-2>", lambda e: "break")
    except Exception:
        pass


HELP_CONTENT = {
    "de": [
        ("head", "inhalt", "Inhalt"),
        ("para", ("LINK", "Das Spiel", "spiel"), " · ",
                 ("LINK", "Züge eingeben", "ziehen"), " · ",
                 ("LINK", "Die Schaltflächen unter dem Brett", "buttons"), " · ",
                 ("LINK", "Die Wertung (+, =, –)", "wertung"), " · ",
                 ("LINK", "Spielstand (Mensch gegen Engine)", "spielstand"), " · ",
                 ("LINK", "Die Spielmodi", "gegner"), " · ",
                 ("LINK", "Eigene Stufen: User (1) und User (2)", "userstufen"), " · ",
                 ("LINK", "Die Spielstufen", "stufen"), " · ",
                 ("LINK", "Spielstärke & Kreuztabelle", "elorang"), " · ",
                 ("LINK", "Datei-Menü", "datei"), " · ",
                 ("LINK", "Kommandos-Menü", "kommandos"), " · ",
                 ("LINK", "Ansicht-Menü", "ansicht"), " · ",
                 ("LINK", "Info-Feld, Am Zuge und Statuszeile", "info"), " · ",
                 ("LINK", "Einstellungen-Menü", "einstellungen"), " · ",
                 ("LINK", "Sprache wählen", "sprache"), " · ",
                 ("LINK", "Engine und Eröffnungsbuch", "engine"), " · ",
                 ("LINK", "Tastenkürzel", "tasten"), "."),

        ("head", "spiel", "Das Spiel"),
        ("para", "ConnectFour Studio ist eine Open-Source-Anwendung für "
                 "„Vier gewinnt“ mit 15 Spielstufen, 20 wählbaren "
                 "Brett-Designs, einem Turniermodus, detaillierten "
                 "Match-Statistiken und einer exakten Echtzeitanalyse."),
        ("para", "Die Grundregeln von „Vier gewinnt“ sind einfach: Gelb "
                 "(Spieler 1) beginnt stets die Partie. Es gewinnt die Seite, der es "
                 "zuerst gelingt, vier eigene Steine waagerecht, senkrecht oder diagonal "
                 "in einer geschlossenen Reihe zu platzieren. Sind alle 42 Felder des "
                 "Gitters besetzt, ohne dass eine Viererreihe zustande kam, endet das "
                 "Spiel ", ("unentschieden", "b"), ". Eine vollendete Gewinnreihe wird "
                 "auf dem Brett ", ("grün hervorgehoben", "b"), "."),
        ("para", "Züge lassen sich auf drei Wegen ausführen: per ",
                 ("LINK", "Mausklick", "ziehen"), ", über die ",
                 ("LINK", "Zifferntasten 1–7", "ziehen"), " oder mit der Schaltfläche ",
                 ("Ziehen (F5)", "b"), ". Eine detaillierte Übersicht bietet der "
                 "Abschnitt ", ("LINK", "„Züge eingeben“", "ziehen"), "."),

        ("head", "ziehen", "Züge eingeben"),
        ("para", ("Mauseingabe: ", "b"), "Ein Klick in die gewünschte "
                 "Spalte wirft den Stein dort ein. Bewegt man den Mauszeiger über "
                 "das Spielfeld, deutet ein halbtransparenter ", ("Ghost-Stein", "b"),
                 " die Landeposition an. Diese Vorschau kann im Menü ",
                 ("LINK", "Ansicht", "ansicht"), " jederzeit deaktiviert werden."),
        ("para", ("Tastatursteuerung: ", "b"), "Über die Zifferntasten ",
                 ("1 bis 7", "b"), " lässt sich direkt in die jeweilige Spalte ziehen. "
                 "Die Tasten ", ("Pfeil links / Pfeil rechts", "b"), " nehmen den letzten "
                 "Zug zurück bzw. spielen ihn wieder vor. ", ("Pfeil hoch / Pfeil runter", "b"),
                 " springt unmittelbar an den Anfang bzw. an das Ende der Partie. Dieselben "
                 "Aktionen lassen sich über die Schaltflächen ", ("<", "b"), ", ",
                 (">", "b"), ", ", ("<<", "b"), " und ", (">>", "b"), " auslösen. "
                 "Die Taste ", ("F5", "b"), " veranlasst die ",
                 ("LINK", "Engine", "engine"), ", den nächsten Zug für die am Zug "
                 "befindliche Seite zu berechnen – auch bei leerem Brett, womit der "
                 "Computer die Partie eröffnet (siehe ",
                 ("LINK", "Schaltflächen unter dem Brett", "buttons"), ")."),
        ("para", ("Wertungszeile: ", "b"), "Ein Mausklick auf eines der sieben "
                 "Felder unterhalb des Brettes führt den entsprechenden Spaltenzug "
                 "ebenfalls aus (siehe ", ("LINK", "Wertungszeile", "wertung"), ")."),
        ("para", "Der jeweils zuletzt ausgeführte Zug wird durch einen ",
                 ("weißen Ring", "b"), " markiert (auf Wunsch abschaltbar unter ",
                 ("LINK", "Ansicht", "ansicht"), ")."),

        ("head", "buttons", "Die Schaltflächen unter dem Brett"),
        ("para", ("Neu: ", "b"), "Setzt das Brett zurück und eröffnet eine neue "
                 "Partie aus der Grundstellung (siehe auch ",
                 ("LINK", "Datei-Menü", "datei"), ")."),
        ("para", ("<< und >>: ", "b"), "Springen direkt an den Partiestart "
                 "beziehungsweise an das aktuelle Partieende."),
        ("para", ("< und >: ", "b"), "Nehmen Züge schrittweise zurück oder "
                 "stellen sie wieder her, um Zugfolgen beliebig zu rekonstruieren."),
        ("para", ("Ziehen (F5): ", "b"), "Übergibt die Zugausführung an die ",
                 ("LINK", "Engine", "engine"), ", die gemäß der aktuell eingestellten ",
                 ("LINK", "Spielstufe", "stufen"), " zieht."),
        ("para", ("Analyse (F7): ", "b"), "Aktiviert oder pausiert die ",
                 ("Dauer-Analyse", "b"), ". Bei eingeschalteter Analyse wird jede "
                 "Stellung unmittelbar nach einem Zug im Hintergrund voll durchgerechnet. "
                 "Ist die Analyse deaktiviert, zeigt die Leiste unter dem Spielfeld "
                 "nur die neutralen Spaltennummern ", ("1–7", "b"), " (siehe ",
                 ("LINK", "Wertungszeile", "wertung"), ")."),
        ("para", "Weitere Sonderfunktionen stehen über die Menüleiste zur Verfügung: ",
                 ("Datei > Neu mit Zufallsstellung…", "b"), " erzeugt eine "
                 "balancierte Stellung mit 1 bis 9 Steinen, wahlweise mit vorgegebenem "
                 "Ergebnis (siehe ", ("LINK", "Datei-Menü", "datei"), "); der Befehl ",
                 ("Kommandos > Alle Züge bewerten (1x)", "b"), " (", ("F6", "b"),
                 ") stößt eine einmalige Bewertung aller sieben Spalten an (siehe ",
                 ("LINK", "Wertungszeile", "wertung"), ")."),

        ("head", "wertung", "Die Wertung (+, =, –)"),
        ("para", "Die Wertungszeile unter dem Brett zeigt für jede verfügbare Spalte "
                 "oben ein symbolisches Bewertungsergebnis und darunter die verbleibende "
                 "Steinzahl bis zum Spielende bei beiderseits perfekter Spielführung: ",
                 ("+ (grün)", "b"), " = Forcierter Gewinn, ",
                 ("= (gelb)", "b"), " = Sicheres Unentschieden, ",
                 ("- (rot)", "b"), " = Zwangsläufiger Verlust. ",
                 ("Vollständig besetzte Spalten werden durch ein „X“ gekennzeichnet.", "b")),
        ("para", "Ist keine Bewertung aktiv, werden lediglich die Spaltenziffern ",
                 ("1–7", "b"), " eingeblendet. Das ", ("LINK", "Info-Feld", "info"),
                 " am rechten Fensterrand formuliert die beste Fortsetzung zudem als "
                 "Klartext, beispielsweise ", ("„Sp. 4: Gelb gewinnt“", "b"), "."),
        ("para", "Die Stellungsbewertung erfolgt stets ", ("mathematisch perfekt", "b"),
                 " (Vollsuche mit 12-ply-Distanzbuch) – unabhängig von der "
                 "eingestellten ", ("LINK", "Spielstufe", "stufen"), ". Nur die "
                 "tatsächlichen Spielzüge der ", ("LINK", "Engine", "engine"), " fallen "
                 "auf niedrigeren Stufen bewusst fehlerhaft aus. Die Distanzzahl "
                 "beziffert die genaue Zahl der noch zu setzenden Steine bis zur Entscheidung: "
                 "Ein kleiner Wert signalisiert ein rasches Partieende, eine hohe Zahl "
                 "ein langes, zähes Endspiel."),

        ("head", "spielstand", "Spielstand (Mensch gegen Engine)"),
        ("para", "Das Anzeigefeld ", ("Spielstand", "b"), " rechts unterhalb des ",
                 ("LINK", "Info-Feldes", "info"), " erfasst die fortlaufende "
                 "Sitzungsbilanz im Duell Mensch gegen Computer. In großer Schrift "
                 "wird das Punktverhältnis ", ("Mensch – Engine", "b"), " angezeigt "
                 "(beispielsweise ", ("2–1", "b"), "), ergänzt durch die Detailstatistik ",
                 ("(+Siege / =Remis / –Niederlagen)", "b"), " aus Sicht des menschlichen "
                 "Spielers sowie die Gesamtzahl der absolvierten Partien. Eine geschätzte "
                 "Elo-Differenz wird eingeblendet, sobald beiden Seiten mindestens ein "
                 "halber Punkt gutgeschrieben wurde."),
        ("para", "Für jede ", ("Gegnerstufe", "b"), " wird eine separate Statistik "
                 "geführt. Wird die Stufe gewechselt (über ",
                 ("LINK", "Einstellungen", "einstellungen"), "), startet die Zählung "
                 "beim neuen Gegner wieder bei 0–0; die vorangegangene Bilanz wird "
                 "dabei verworfen. Gewertet werden ausschließlich regulär beendete "
                 "Partien: Setzt ein Spieler den siegbringenden Stein, erhält er den "
                 "vollen Punkt. Bei einem Remis erhalten beide Parteien je einen halben "
                 "Punkt. Vorzeitig abgebrochene Partien (etwa über ", ("Neu", "b"),
                 " oder ", ("Stop Auto Play", "b"), ") fließen nicht in die Wertung ein."),
        ("para", ("An/Aus: ", "b"), "Blendet die numerische Anzeige aus oder ein; "
                 "der umschließende Rahmen bleibt erhalten. Bei deaktivierter Anzeige "
                 "pausiert die Punkterfassung. ", ("Reset: ", "b"), "Setzt das "
                 "Punkteverhältnis der aktuellen Stufe wieder auf 0–0 zurück. Beide "
                 "Funktionen sind auch über das Menü ", ("LINK", "Ansicht", "ansicht"),
                 " (", ("Spielstand ein/aus", "b"), ", ", ("Spielstand reset", "b"),
                 ") erreichbar. Standardmäßig ist die Erfassung ausgeschaltet; die "
                 "Zählung beginnt erst nach dem Einschalten."),

        ("head", "gegner", "Die Spielmodi"),
        ("para", "Im Menü ", ("Einstellungen", "b"), " wird der "
                 "Spielmodus festgelegt: ", ("Mensch-Computer", "b"), " (mit frei wählbarer ",
                 ("LINK", "Gegnerstufe", "stufen"), ") oder ",
                 ("2-Spieler (beide Mensch)", "b"), ". Im Zwei-Spieler-Modus dient "
                 "ConnectFour Studio als virtuelles Spielbrett mit Schiedsrichterfunktion "
                 "und optional zuschaltbarer ", ("LINK", "Dauer-Analyse", "buttons"),
                 " – ein gutes Werkzeug zum gemeinsamen Analysieren und Trainieren."),
        ("para", ("Computer-Computer (ausspielen): ", "b"), "Lässt die Engine die "
                 "aktuelle Stellung gegen sich selbst vollenden – und zwar stets in der "
                 "höchsten Stufe ", ("Perfekt", "b"), ", unabhängig von der sonstigen "
                 "Konfiguration. Die Funktion kann jederzeit erneut aufgerufen werden "
                 "und setzt dann an der aktuellen Brettstellung an."),
        ("para", ("Computer-Computer Match: ", "b"), "Führt eine Serie automatisierter "
                 "Partien durch. Einstellbar sind die ", ("Partienzahl", "b"), " (1 bis 10.000), "
                 "die Spielertypen für beide Farben (", ("Mensch", "b"), ", eine ",
                 ("LINK", "feste Stufe", "stufen"), " oder eine ",
                 ("LINK", "benutzerdefinierte Stufe User (1)/(2)", "userstufen"), "), ",
                 ("Farbwechsel", "b"), " nach jeder Einzelpartie (Gelb und Rot tauschen "
                 "die Rollen) sowie das ", ("Tempo", "b"), " (Normal / Schnell / Nur "
                 "Ergebnisse). Nimmt ein Mensch am Match teil (eine Seite steht auf ",
                 ("Mensch", "b"), ") und ist das ", ("Tempo", "b"), " auf ",
                 ("Normal", "b"), " gesetzt, pausiert die Ausführung 3 Sekunden "
                 "nach Partieende, damit sich das Ergebnis prüfen lässt. ",
                 ("Start", "b"), " startet die Serie, ", ("Stop", "b"), " (auch "
                 "über das Menü ", ("Stop Auto Play", "b"), ") bricht sie ab; der "
                 "bisherige Zwischenstand bleibt erhalten. Nach Abschluss des Matches "
                 "tritt das Dialogfenster automatisch in den Vordergrund; die "
                 "Schaltfläche ", ("Kopieren", "b"), " überträgt den gesamten "
                 "Ergebnisbericht (Punkte, Sieg-/Remisbilanz und Elo-Auswertung) in "
                 "die Zwischenablage."),

        ("head", "userstufen", "Eigene Stufen: User (1) und User (2)"),
        ("para", "Im Konfigurationsdialog von ",
                 ("LINK", "Computer-Computer Match", "gegner"), " stehen neben den "
                 "fest programmierten Stufen zwei frei konfigurierbare Profile zur Verfügung: ",
                 ("User (1) (eigene p, s, w)", "b"), " und ",
                 ("User (2) (eigene p, s, w)", "b"), ". Sobald ein solches Profil "
                 "für Gelb oder Rot gewählt wird, wird das entsprechende "
                 "Eingabefeld freigeschaltet (Feld 1 steuert User 1, Feld 2 steuert "
                 "User 2). Hier lassen sich die drei Verhaltensparameter ",
                 ("p, s und w", "b"), " individuell festlegen (zur genauen Wirkungsweise siehe ",
                 ("LINK", "Die Spielstufen", "stufen"), "). Da beide Profile unabhängig sind, "
                 "lassen sich auch Duelle zweier "
                 "eigener Spielweisen austragen."),
        ("para", ("p = Anteil perfekter Züge in Prozent", "b"),
                 " (Wertebereich 0 bis 100): Die Patzerquote berechnet sich als ",
                 ("100 – p", "b"), ". Ein Wert von ", ("p = 100", "b"), " (wie bei ",
                 ("14 Perfekt", "b"), ") garantiert für jeden Zug Fehlerfreiheit. "
                 "Der Extremwert ", ("p = 0", "b"), " (wie bei Stufe ", ("6 Taktiker", "b"),
                 " oder in eigenen User-Profilen) bedeutet eine ",
                 ("Patzerquote von 100 %", "b"), " – hier wird nie der theoretische Bestzug "
                 "gewählt, sondern stets die Patzer-Routine durchlaufen. Das ist nicht "
                 "reiner Zufall (wie auf Stufe 1), denn das Spielverhalten steuern "
                 "die Parameter s und w: Stufe 6 Taktiker zeigt, "
                 "wie stark ein Profil mit (0, 3, 3) allein durch taktische Absicherung spielt. "
                 "Bei Zwischenwerten wie ", ("p = 50", "b"), " (etwa Stufe 4 Anfänger oder "
                 "Stufe 7 Mittel) fällt statistisch jeder zweite Zug perfekt aus, während die "
                 "übrigen 50 % in den Patzer-Zweig abbiegen."),
        ("para", ("Entscheidungsablauf pro Zug: ", "b"), "Ein kurzer forcierter Gewinn ",
                 ("(w)", "b"), " geht stets vor – noch vor dem p-Zufallsentscheid. Liegt kein "
                 "solcher Kurzgewinn vor, entscheidet der ", ("p-Wurf", "b"),
                 ": Fällt die Wahl auf ", ("„perfekt“", "b"), ", spielt der ",
                 ("s-Filter", "b"), " keine Rolle – die Engine wählt unmittelbar unter den "
                 "theoretischen Bestzügen (bei Gleichstand greift die 10-Halbzüge-Regel). "
                 "Fällt die Entscheidung dagegen auf ", ("„Patzer“", "b"), ", greift die "
                 "Filterkette: Zunächst ", ("w", "b"), " (Siegsschutz), dann der Verlustfilter ",
                 ("s", "b"), " und erst am Ende die gleichverteilte Wahl unter allen verbliebenen, "
                 "zulässigen Zügen. Ein Remis (Unentschieden) gegen drohende Niederlagen wird "
                 "dabei nicht erzwungen oder bevorzugt – es zählt wie jeder andere erlaubte Zug."),
        ("para", ("s = Verlustschutz in gegnerischen Zügen", "b"), " (Wertebereich 0 bis 9): "
                 "Dieser Filter wirkt nur im Patzer-Zweig: Ein schwächerer Zug "
                 "gilt als unzulässig, sofern der Kontrahent daraufhin innerhalb von maximal "
                 "s eigenen Zügen forciert gewinnen könnte. ", ("s = 0", "b"),
                 " bedeutet den Verzicht auf diesen Filter – taktische Einsteller werden in Kauf "
                 "genommen (wie auf den Stufen 1–4, dort ist im Patzerfall jeder legale Zug "
                 "gleich wahrscheinlich). ", ("s = 1", "b"), " sperrt Züge, "
                 "die dem Gegner bereits im nächsten Zug den Sieg schenken würden; ",
                 ("s = 2, 3 oder 4", "b"), " dehnen diesen Schutz auf 2, 3 "
                 "bzw. 4 gegnerische Züge aus. Gewinne und Remisvarianten sind im Patzer-Zweig "
                 "stets erlaubt."),
        ("para", ("w = Siegsschutz", "b"), " (Wertebereich 0 bis 9): Kurze forcierte "
                 "Gewinne gehen immer vor – noch vor dem p-Zufallsentscheid: Findet die "
                 "Engine einen Gewinnweg, dessen Zugdistanz innerhalb von w Zügen liegt, "
                 "wird dieser Sieg gespielt. ", ("w = 1", "b"), " sichert den "
                 "direkten Sofortgewinn im nächsten Zug ab, ", ("w = 2", "b"), " garantiert den "
                 "Sieg in maximal 2 eigenen Zügen; analog wirken ", ("w = 3", "b"), " und ",
                 ("w = 4", "b"), " (zur Einordnung siehe ", ("LINK", "Die Spielstufen", "stufen"), "). Liegt kein "
                 "solch naher Gewinn vor, greift die reguläre p-Entscheidung. ",
                 ("w = 0", "b"), " deaktiviert diesen Vorgriff (im perfekten Zugzweig werden "
                 "Gewinne über die reguläre Bewertung weiterhin genutzt)."),
        ("para", ("Gleichstand (perfekte Züge, alle Stufen): ", "b"),
                 "Bieten sich mehrere gleichwertige Züge mit Best-Score an, ermittelt ein "
                 "Zufallsgenerator die Auswahl, um stereotype Partiewiederholungen zu vermeiden. "
                 "Führen Züge innerhalb von 10 Halbzügen zum Gewinn, wird der schnellste Gewinnweg "
                 "gewählt – bei mehreren gleich schnellen wird unter diesen gewürfelt. Liegt kein "
                 "Gewinn so nah, wird aus allen Gewinnzügen gelost. Gibt es ausschließlich "
                 "Remisvarianten (Unentschieden), wird unter diesen gewürfelt. In reinen "
                 "Verluststellungen meidet Stufe ", ("14 Perfekt", "b"),
                 " Niederlagen innerhalb von 10 Halbzügen; gibt es langsamere Verlustzüge, "
                 "wird unter diesen gewählt. Sind alle Verlustzüge weiter "
                 "als 10 Halbzüge entfernt, wird zur Varianz unter allen Verlustzügen gelost."),
        ("para", "Vergleichende Beispiele zur Orientierung: Die Stufe ",
                 ("Anfänger (50, 0, 0)", "b"), " spielt jeden zweiten Zug schwach und "
                 "ungeschützt; die Stufe ", ("Mittel (50, 1, 1)", "b"),
                 " spielt ebenfalls jeden zweiten Zug schwach, verhindert jedoch "
                 "elementare Einsteller im Folgezug und verwertet direkte Sofortgewinne "
                 "konsequent. Die konfigurierten Parameter werden in den Berichten des ",
                 ("Computer-Computer-Matches", "b"), " ausgewiesen "
                 "(beispielsweise als ", ("„User (1) (70, 1, 1)“", "b"), ")."),

        ("head", "stufen", "Die Spielstufen"),
        ("para", "Die regulären Spielstufen werden durch die Parameter ",
                 ("(p, s, w)", "b"), " beschrieben (Stufe 0 verliert vorsätzlich, "
                 "Stufe 1 spielt reinen Zufall, Stufe 14 fehlerfrei): ",
                 ("p", "b"), " steht für den prozentualen Anteil perfekter Züge, ",
                 ("s", "b"), " definiert den Verlustschutz in gegnerischen Zügen "
                 "(verhindert Fehlzüge, die binnen s Gegnerzügen zur Niederlage führen), "
                 "und ", ("w", "b"), " bezeichnet den Siegsschutz (forcierte Gewinne "
                 "binnen w eigenen Zügen werden stets gespielt). "
                 "Die Distanzangabe unter dem Symbol in der ",
                 ("LINK", "Wertungszeile", "wertung"), " beziffert die Zahl "
                 "der noch zu setzenden Steine bis zum Partieende: 1 steht für den unmittelbaren "
                 "Gewinnstein, kleine Werte markieren kurze, große Werte langwierige "
                 "Abwicklungen (vertiefende Erläuterungen im Abschnitt ",
                 ("LINK", "Info-Feld", "info"), ")."),
        ("para", ("0 Verlierer (Spaß-Stufe): ", "b"), "Spielt vorsätzlich schwach "
                 "und wählt bevorzugt zufällige Verlustzüge. Steht kein Verlustzug zur "
                 "Wahl, weicht das Programm auf ein Remis (Unentschieden) oder einen "
                 "Zufallszug aus. Eine reine Spaßstufe ohne Wertung im Elo-System."),
        ("para", ("1 Zufall: ", "b"), "Spielt reinen Zufall: Jeder legale Zug hat "
                 "exakt dieselbe Wahrscheinlichkeit. Auf dieser Stufe gibt es keinerlei "
                 "(p, s, w)-Logik, keine Stellungsbewertung und keine Filter – die "
                 "Wahl erfolgt völlig gleichverteilt aus allen offenen Spalten."),
        ("para", ("2 Sehr Leicht (25, 0, 0): ", "b"), "Spielt zu 25 % optimal und zu "
                 "75 % rein zufällig; begeht gravierende Einsteller – ideal für Einsteiger "
                 "und Kinder."),
        ("para", ("3 Leicht (40, 0, 0): ", "b"), "Spielt zu 40 % optimal, verzichtet "
                 "jedoch auf taktische Schutzmechanismen (s = 0, w = 0)."),
        ("para", ("4 Anfänger (50, 0, 0): ", "b"), "Jeder zweite Zug wird theoretisch "
                 "perfekt geführt (50 %). Da s = 0 und w = 0 anliegen, unterbleibt "
                 "jegliche Fehlerfilterung."),
        ("para", ("5 Fortgeschritten (20, 1, 1): ", "b"), "Wählt zu 20 % den theoretischen "
                 "Bestzug, übersieht jedoch dank s = 1 und w = 1 weder eigene Sofortgewinne "
                 "noch gegnerische Direktbedrohungen im nächsten Zug."),
        ("para", ("6 Taktiker (0, 3, 3): ", "b"), "Spielt nie den theoretischen Bestzug "
                 "(p = 0), spielt aber taktisch aufmerksam: Forcierte Gewinne in "
                 "bis zu 3 eigenen Zügen werden gespielt (w = 3) und drohende "
                 "Niederlagen in den nächsten 3 gegnerischen Zügen konsequent abgewendet "
                 "(s = 3). Ein taktisch zäher Gegner ohne strategische Weitsicht."),
        ("para", ("7 Mittel (50, 1, 1): ", "b"), "Solider Amateurstandard: Jeder zweite "
                 "Zug perfekt (50 %), zuverlässige Verwertung von Sofortgewinnen (w = 1) und "
                 "konsequente Vermeidung unmittelbarer Einsteller (s = 1)."),
        ("para", ("8 Fordernd (55, 1, 1): ", "b"), "Baut auf Stufe 7 auf, agiert jedoch "
                 "in mehr als der Hälfte aller Züge (55 %) vollkommen fehlerfrei."),
        ("para", ("9 Schwer (65, 1, 1): ", "b"), "Mit 65 % optimalen Zügen und sicherem "
                 "Einstellerschutz ein ernstzunehmender Kontrahent für geübte Klubspieler."),
        ("para", ("10 Sehr Schwer (70, 2, 2): ", "b"), "Verbindet hohe Präzision (70 %) "
                 "mit taktischem Gespür: Erkennt und pariert Angriffe über "
                 "2 gegnerische Züge (s = 2) und setzt eigene Gewinne in 2 Zügen "
                 "sicher durch (w = 2) – eine Hürde für Turnierspieler."),
        ("para", ("11 Experte (80, 2, 2): ", "b"), "Spielt zu 80 % fehlerfrei und "
                 "pariert Angriffe über 2 gegnerische Züge zuverlässig ab. Eigene "
                 "Gewinndrohungen über 2 Züge werden sicher verwertet; Tor zu den Meisterklassen."),
        ("para", ("12 Meister (85, 3, 3): ", "b"), "Spielt sehr stark (85 % Bestzüge) mit "
                 "weitreichender taktischer Absicherung: Erkennt Drohungen und eigene "
                 "Gewinnwege über 3 Züge (s = 3, w = 3). Selbst "
                 "erfahrene Turnierspieler punkten hier kaum noch."),
        ("para", ("13 Starker Meister (92, 4, 4): ", "b"), "Nahezu unfehlbar (92 % Bestzüge): "
                 "Vermeidet forcierte Verlustvarianten bis zu 4 Züge im Voraus "
                 "(s = 4) und setzt eigene Gewinne über 4 Züge sicher "
                 "durch (w = 4)."),
        ("para", ("14 Perfekt (100, -, -): ", "b"), "Spielt fehlerfrei nach den "
                 "Gesetzen des gelösten Spiels: Als Anziehender (Gelb) gewinnt die "
                 "Engine jede Partie forciert; als Nachziehender (Rot) nutzt sie jede "
                 "Ungenauigkeit des Gegners zum vollen Punktgewinn aus. "
                 "Gleichwertige Züge werden statistisch variiert (siehe ",
                 ("Gleichstand", "b"), " oben). Zur Schulung des eigenen Spiels empfiehlt "
                 "sich die Stellungsanalyse unter ", ("LINK", "Analyse", "wertung"), "."),
        ("para", "Orientierungswerte der relativen Spielstärke (ermittelt in "
                 "Engine-gegen-Engine-Turnieren mit insgesamt 18.200 Partien – "
                 "200 Partien je Paarung – unter "
                 "fortlaufendem Farbwechsel; Referenzbasis Stufe Zufall = 1000 Elo): "
                 "1 Zufall, 2 Sehr Leicht ~1204, 3 Leicht ~1340, "
                 "4 Anfänger ~1431, 5 Fortgeschritten ~1498, 6 Taktiker ~1614, "
                 "7 Mittel ~1702, 8 Fordernd ~1752, "
                 "9 Schwer ~1817, 10 Sehr Schwer ~1929, 11 Experte ~2010, "
                 "12 Meister ~2080, 13 Starker Meister ~2132, 14 Perfekt ~2174. "
                 "In Partien gegen menschliche Kontrahenten können sich diese Differenzen "
                 "psychologisch und taktisch verschieben. Spielstärke-Tabelle und Kreuztabelle stehen "
                 "vollständig im Abschnitt ", ("LINK", "„Spielstärke & Kreuztabelle“", "elorang"), "."),
        ("head", "elorang", "Spielstärke & Kreuztabelle"),
        ("para", "Alle 91 Paarungen wurden mit je 200 Partien und Farbwechsel ausgespielt (insgesamt 18.200). "
                 "Referenzbasis Stufe Zufall = 1000 Elo (relativ, kein FIDE-Elo)."),
        ("para", ("Spielstärke (Elo):", "b")),
        ("mono",
         " 1 Zufall                      1000\n"
         " 2 Sehr Leicht      (25,0,0)   1204\n"
         " 3 Leicht           (40,0,0)   1340\n"
         " 4 Anfänger         (50,0,0)   1431\n"
         " 5 Fortgeschritten  (20,1,1)   1498\n"
         " 6 Taktiker         (0,3,3)    1614\n"
         " 7 Mittel           (50,1,1)   1702\n"
         " 8 Fordernd         (55,1,1)   1752\n"
         " 9 Schwer           (65,1,1)   1817\n"
         "10 Sehr Schwer      (70,2,2)   1929\n"
         "11 Experte          (80,2,2)   2010\n"
         "12 Meister          (85,3,3)   2080\n"
         "13 Starker Meister  (92,4,4)   2132\n"
         "14 Perfekt          (100,-,-)  2174"),
        ("para", ("Kreuztabelle (Punkte der Zeilen-Stufe gegen die Spalten-Stufe, aus 200):", "b")),
        ("table", "kreuz14"),
        ("sub", "zugwahl", "Hinter den Kulissen: Die 3-Schritte-Zugwahl"),
        ("para", ("So entscheidet die Engine jeden einzelnen Zug (Stufen 1–14): ", "b"),
                 "Jeder Spielzug durchläuft eine feste dreistufige Entscheidungskette. "
                 "Aus ihr erklärt sich das Zusammenspiel von Spielstärke, Filtern "
                 "und scheinbaren Paradoxien:"),
        ("para", ("1. Siegsschutz (w) vorab – ganz ohne Würfeln: ", "b"),
                 "Bietet die Stellung einen forcierten Gewinn innerhalb von ",
                 ("w", "b"), " eigenen Zügen, wird dieser Zug sofort ausgeführt – noch vor dem ",
                 ("p", "b"), "-Zufallsentscheid. ",
                 ("w = 1", "b"), " bedeutet direkter Sofortgewinn. ",
                 ("w = 2", "b"), " bedeutet Gewinn in höchstens 2 Zügen. ",
                 ("w = 3", "b"), " bedeutet Gewinn in bis zu 3 Zügen. ",
                 ("(w = 0 schaltet diesen Vorgriff aus.)", "b"),
                 " Nur wenn kein solcher Kurzgewinn vorliegt, folgt Schritt 2."),
        ("para", ("2. Der p-Wurf (perfekt oder Patzer): ", "b"),
                 "Bei jedem Zug isoliert und ohne Gedächtnis entscheidet die Wahrscheinlichkeit ",
                 ("p", "b"), ", ob die Engine gut oder schwach zieht. ",
                 "Bei ", ("p = 50", "b"), " (Anfänger, Mittel) fällt statistisch jeder zweite Zug perfekt aus. ",
                 "Bei ", ("p = 20", "b"), " (Fortgeschritten) nur jeder fünfte. ",
                 "Bei ", ("p = 80", "b"), " (Experte) vier von fünf. ",
                 "Serien sind rein zufällig: Auch bei ", ("p = 50", "b"),
                 " können dreimal hintereinander Patzer – oder dreimal perfekte Züge – fallen."),
        ("para", ("3a. Perfekt gewürfelt: Best-Score und 10-Halbzüge-Regel: ", "b"),
                 "Die Engine wählt direkt unter den theoretischen Bestzügen: ",
                 "Bei mehreren gleich guten Gewinnzügen wird der schnellste innerhalb von "
                 "10 Halbzügen gespielt; bei mehreren gleich schnellen wird unter diesen gewürfelt. ",
                 "Liegt kein einziger Gewinn innerhalb von 10 Halbzügen, wird unter allen übrigen "
                 "Gewinnzügen gewürfelt (die dann alle weiter als 10 Halbzüge entfernt sind). ",
                 "Gibt es nur Remis (Unentschieden), wird unter diesen gewürfelt. ",
                 "Gibt es nur Verlustzüge, gilt die Verlustregel (längster Widerstand, gewichtet – "
                 "bei Perfekt mit 10-Halbzüge-Schutz)."),
        ("para", ("3b. Schwach gewürfelt: Die Patzer-Routine: ", "b"),
                 "Das ist kein blindes Würfeln, sondern ein gefilterter Zug: ",
                 "Der Filter ", ("s", "b"), " sperrt alle Züge, bei denen der Gegner in maximal ",
                 ("s", "b"), " Zügen gewinnen würde (", ("s = 1", "b"),
                 " verbietet Einsteller im nächsten Zug; ", ("s = 0", "b"),
                 " filtert gar nichts). ",
                 "Unter allen verbliebenen, erlaubten Zügen wird ", ("gleichverteilt gewürfelt", "b"),
                 " – ein Remis wird dabei nicht bevorzugt, es zählt wie jeder andere zulässige Zug. ",
                 ("Sonderfälle: ", "b"), ("p = 100", "b"), " (Perfekt) geht immer nach 3a. ",
                 ("p = 0", "b"), " (Taktiker) geht immer nach 3b. ",
                 ("s = 0, w = 0", "b"), " (Stufen 1–4) würfelt in 3b völlig ungefiltert."),
        ("sub", "filterparadox", "Das Filter-Paradoxon: Taktiker vs. Anfänger (149,5 : 50,5)"),
        ("para", "Im Direktduell schlägt Stufe ", ("6 Taktiker (0, 3, 3)", "b"),
                 " den ", ("4 Anfänger (50, 0, 0)", "b"),
                 " deutlich mit fast 3 : 1, obwohl der Taktiker keinen perfekten Zug spielt. ",
                 "Der Grund liegt im Zusammenspiel von ", ("Schild und Schwert", "b"), ": ",
                 "Dank ", ("s = 3", "b"), " verschenkt der Taktiker fast nichts durch schnelle Einsteller. ",
                 "Und dank ", ("w = 3", "b"), " setzt er jeden gebotenen Gewinn in 1 bis 3 Zügen durch. ",
                 "Der Anfänger dagegen verschenkt seine Eröffnungsvorteile durch ungefilterte Sofort-Einsteller (",
                 ("s = 0", "b"), ") und lässt gegnerische Fehler mangels Siegsschutz (",
                 ("w = 0", "b"), ") oft ungestraft entkommen. ",
                 "Dasselbe Prinzip zeigt sich bei ", ("5 Fortgeschritten (20, 1, 1)", "b"),
                 ", der den Anfänger trotz weit geringerem ", ("p", "b"), " mit 137 : 63 bezwingt."),
        ("sub", "spitzenumkehr", "Die Umkehrung an der Spitze: Punkte gegen Meister"),
        ("para", "Gegen die stärksten Gegner (Starker Meister und Perfekt) kehrt sich das Bild um: ",
                 "Hier holt der Anfänger aus 400 Partien ", ("7,0 Punkte", "b"),
                 " – der Taktiker aber nur ", ("0,5 Punkte", "b"), " (nur ein Vierzehntel davon). ",
                 "Starke Gegner stellen praktisch nie ein. Da nützt weder ",
                 ("s = 3", "b"), " noch ", ("w = 3", "b"),
                 " etwas, weil der Meister kaum Angriffsfläche bietet. ",
                 "Um gegen fast fehlerfreie Meister zu punkten, braucht es perfekte Züge mit tiefem "
                 "strategischem Plan – kurzzügiger Verlustschutz oder Siegsschutz reicht dafür nicht. "
                 "Der Anfänger spielt etwa jeden zweiten Zug perfekt; "
                 "ab und an reicht einer davon für ein Remis. Dem Taktiker fehlen solche Züge völlig."),

        ("head", "datei", "Datei-Menü"),
        ("para", ("Neues Spiel: ", "b"), "Setzt das Brett auf die leere Ausgangsstellung zurück. ",
                 ("Neu mit Zufallsstellung…: ", "b"), "Erzeugt eine zufällig aufgebaute "
                 "Mittelspielstellung mit 1 bis 9 Steinen, wahlweise mit garantiertem "
                 "theoretischen Ausgang (Gewinn, Remis oder Verlust). ",
                 ("Stellung laden… ", "b"), "und ", ("Stellung speichern…: ", "b"),
                 "Öffnen einen Standard-Dateidialog für das ",
                 (".4gp-Format", "b"), ". Eine gespeicherte Partie besteht aus der "
                 "chronologischen Ziffernkette der gewählten Spalten, wie etwa ",
                 ("4433221", "b"), ". ", ("Schnell speichern (F3) ", "b"), "und ",
                 ("Schnell laden (F4): ", "b"), "Speichern bzw. laden den aktuellen "
                 "Partieverlauf ohne Zwischendialog direkt in die bzw. aus der Datei ",
                 ("quicksave.4gp", "b"), " im Hauptverzeichnis des Programms. ",
                 ("Ende: ", "b"), "Schließt ConnectFour Studio ordnungsgemäß."),

        ("head", "kommandos", "Kommandos-Menü"),
        ("para", ("Erster / letzter Zug (Pfeil hoch / Pfeil runter): ", "b"),
                 "Springt an den Partiestart bzw. das Partieende; zurückgenommene "
                 "Züge bleiben im Speicher erhalten und lassen sich jederzeit "
                 "wieder vorführen. ", ("Zug zurück / vor: ", "b"), "Ermöglicht das "
                 "schrittweise Manövrieren durch die Partie (analog zu den Knöpfen ",
                 ("<", "b"), " und ", (">", "b"), "). ",
                 ("Ziehen (Computer): ", "b"), "Entspricht dem Tastenkürzel ", ("F5", "b"), ". ",
                 ("Alle Züge bewerten (1x): ", "b"), "Entspricht ", ("F6", "b"), " (siehe ",
                 ("LINK", "Wertungszeile", "wertung"), "). ",
                 ("Dauer-Analyse: ", "b"), "Entspricht ", ("F7", "b"), " (siehe ",
                 ("LINK", "Ansicht-Menü", "ansicht"), ")."),

        ("head", "ansicht", "Ansicht-Menü"),
        ("para", ("Ghost-Stein: ", "b"), "Schaltet die halbtransparente Einwurf-Vorschau ein oder aus. ",
                 ("Drop-Animation: ", "b"), "Steuert die flüssige Fallbewegung eingeworfener Steine. ",
                 ("Letzten Zug zeigen: ", "b"), "Aktiviert oder deaktiviert den weißen Markierungsring "
                 "auf dem jüngsten Spielstein. ",
                 ("Spielstand ein/aus ", "b"), "sowie ",
                 ("Spielstand reset: ", "b"), "Entsprechen den Schaltflächen des ",
                 ("LINK", "Spielstand-Bereichs", "spielstand"), ". Das Hilfefenster lässt "
                 "sich jederzeit über das Menü oder mit ", ("F1", "b"), " öffnen."),

        ("head", "info", "Info-Feld, Am Zuge und Statuszeile"),
        ("para", "Oben rechts signalisiert das Feld ", ("Am Zuge", "b"),
                 " anhand des Steinsymbols und des Namens, wer am Zug ist: ",
                 ("Mensch", "b"), " oder die Engine unter Nennung der aktiven Stufe "
                 "(beispielsweise „User (1) (70,1,1)“). Im Zwei-Spieler-Modus wird "
                 "hier durchgehend Mensch angezeigt."),
        ("para", "Unmittelbar darunter liefert das ", ("Info-Feld", "b"),
                 " Kenngrößen zur aktuellen Brettsituation:"),
        ("para", ("Zug: ", "b"), "Fortlaufende Nummer des nächsten Halbzugs (beginnend bei 1)."),
        ("para", ("Stufe: ", "b"), "Aktivierte ",
                 ("LINK", "Spielstufe", "stufen"),
                 " der Engine (im Turniermodus die Stufe der ziehenden Farbe)."),
        ("para", ("Tiefe: ", "b"), "Zuletzt erzielte Suchtiefe in Halbzügen (Ply). ",
                 ("Voll: ", "b"), "Vollständige Berechnung bis zum rechnerischen Spielende. ",
                 ("Buch 12d: ", "b"), "Bis zu 12 Steinen endet die Suche, sobald jede Variante das Eröffnungsbuch erreicht – die Werte sind exakt. ", ("Buch 2d: ", "b"), "Stellung mit höchstens zwei Steinen: exakte Werte aus dem eingebauten Mini-Buch, ganz ohne Suche. "
                 "Ein angehängtes Auslassungszeichen (z. B. „8...“) visualisiert eine noch "
                 "laufende Vertiefung. Ein Gedankenstrich (–) bedeutet, dass noch keine "
                 "Berechnung vorliegt."),
        ("para", ("Wert: ", "b"), "Theoretische Stellungsbewertung des jüngsten Zugs in "
                 "kompakter Notation – beispielsweise „Gelb (31)“, „Rot (28)“ oder "
                 "„Remis (40)“. Das Kürzel benennt die siegreiche Seite bei beiderseits "
                 "optimalem Weiterspiel. Die Zahl in Klammern beziffert die Zahl "
                 "der noch zu setzenden Steine bis zur endgültigen Entscheidung: Kleine Zahlen "
                 "(1–6) signalisieren eine unmittelbar bevorstehende Entscheidung – eine ",
                 ("1", "b"), " in Klammern markiert den direkten Sofortgewinn im nächsten Zug. "
                 "Hohe Werte (30–42) verweisen auf ein langwieriges Endspiel (42 entspräche "
                 "einem Remis von der leeren Stellung aus). Bei jeder Zugausführung zählt dieser "
                 "Wert mit jedem Zug um 1 herunter. Die Distanzzahl unter dem Symbol in der ",
                 ("LINK", "Wertungszeile", "wertung"), " nach einer Analyse (",
                 ("F6", "b"), "/", ("F7", "b"),
                 ") zeigt dieselbe Steinzahl je Spalte. "
                 "Vor der ersten Analyse erscheint ein Strich (–). Nach Vollendung der Partie wird hier das "
                 "Endergebnis vermeldet, beispielsweise „Gelb gewinnt!“."),
        ("para", ("Knoten: ", "b"), "Anzahl der durchsuchten Stellungen im Suchbaum "
                 "(Echtzeit-Rückmeldung des C++-Kerns mit lesbaren Tausendertrennpunkten). ",
                 ("Zeit: ", "b"), "Reine Berechnungsdauer der letzten Analyse in Millisekunden. ",
                 ("Tempo: ", "b"), "Suchgeschwindigkeit in Knoten pro Sekunde "
                 "(beispielsweise 2,3 M/s = 2,3 Millionen Stellungen/s). Alle Werte "
                 "beziehen sich auf den jeweils jüngsten Rechenschritt."),
        ("para", ("Quelle: ", "b"), "Herkunft der Stellungsdaten: ",
                 ("Buch 12d", "b"), " = Abruf aus dem integrierten Eröffnungsbuch (bis "
                 "zu einer Tiefe von 12 Steinen), ", ("berechnet", "b"), " = freie "
                 "Echtzeitberechnung der Engine. Ein Gedankenstrich (–) signalisiert "
                 "den Ausgangszustand vor Beginn der Suche."),
        ("para", "Die ", ("Statuszeile", "b"), " am unteren Fensterrand informiert über "
                 "ausgeführte Züge (z. B. „Computer zog 4 in 0,35 s“), Analyseberichte "
                 "und Dateioperationen. Während eines laufenden Rechenvorgangs meldet "
                 "sie „Computer denkt noch – bitte warten.“ Ein Ladeversuch während der "
                 "Suche wird mit dem Hinweis „Computer denkt noch – erst anhalten, dann laden.“ "
                 "abgewiesen. Die Berechnung ist in diesem Fall zuerst über die "
                 "Stopp-Funktion zu unterbrechen."),

        ("head", "einstellungen", "Einstellungen-Menü"),
        ("para", "Das Menü ", ("Einstellungen", "b"), " bündelt zentrale Optionen: ",
                 ("Computer-Stufe", "b"), " (regelt die Spielstärke von Stufe ",
                 ("LINK", "0 bis 14", "stufen"), "; lässt sich auch während der laufenden "
                 "Partie ändern – der ", ("LINK", "Spielstand", "spielstand"),
                 " beginnt bei einem Wechsel wieder bei 0–0), ",
                 ("Mensch-Computer", "b"), " (Partie gegen die künstliche Intelligenz), ",
                 ("2-Spieler (beide Mensch)", "b"), " (zwei Personen spielen gegeneinander; "
                 "das Programm übernimmt die Schiedsrichterfunktion und die Visualisierung), ",
                 ("Computer-Computer (ausspielen)", "b"), " (die Engine übernimmt beide "
                 "Seiten ab der vorliegenden Stellung, siehe ",
                 ("LINK", "Spielmodi", "gegner"), "), ",
                 ("Computer-Computer Match", "b"), " (konfiguriert automatisierte Partien "
                 "und Turniere, siehe ", ("LINK", "Spielmodi", "gegner"), "), ",
                 ("Stop Auto Play", "b"), " (stoppt ein laufendes Match unverzüglich; "
                 "der Zwischenstand bleibt erhalten) sowie ",
                 ("Stein-Sets", "b"), " (Auswahl aus 20 Brett- und "
                 "Steindesigns; durchblättern lässt sich auch mit dem "
                 "Mausrad über dem Spielfeld oder über die Tasten Bild-rauf / Bild-runter)."),

        ("head", "sprache", "Sprache wählen"),
        ("para", "Im Menü ", ("Hilfe", "b"), " unter ", ("Sprache", "b"), " stehen "
                 "die verfügbaren Sprachen: ", ("Deutsch", "b"), ", ", ("English", "b"), ", ",
                 ("Français", "b"), ", ", ("Español", "b"), ", ", ("Nederlands", "b"), " und ",
                 ("Italiano", "b"), ". "
                 "Die Auswahl als Radio-Button wirkt sofort für Hilfe und Info."),

        ("head", "engine", "Engine und Eröffnungsbuch"),
        ("para", "Als mathematischer Rechenkern fungiert ",
                 ("BitBully von Markus Thill", "b"), " – ein effizientes Python-Modul "
                 "mit C++-Kern. Zum Einsatz kommen optimierte Bitboards, "
                 "eine iterative Vertiefung mit MTD(f)/Null-Window-Suchalgorithmus "
                 "sowie dynamische Transpositionstabellen. Das integrierte Eröffnungsbuch ",
                 ("12-ply-dist", "b"), " liefert theoretische Bewertungen und exakte "
                 "Distanzwerte für sämtliche Stellungen mit bis zu 12 gesetzten Steinen; "
                 "in tieferen Varianten setzt die Such-Engine die Berechnung fort."),
        ("para", "ConnectFour Studio verbindet eine schlanke Desktop-Oberfläche (Python, Tkinter, "
                 "Grafik-Rendering über Pillow) mit einem gelösten Spiel. "
                 "Lizenziert als freie Software unter der ",
                 ("GNU Affero General Public License (AGPL v3)", "b"), "."),

        ("head", "tasten", "Tastenkürzel"),
        ("para", ("1–7", "b"), " = Spaltenzug ausführen · ",
                 ("Pfeil links / Pfeil rechts", "b"), " = Zug zurücknehmen / wiederholen · ",
                 ("Pfeil hoch / Pfeil runter", "b"), " = An Partiestart / Partieende springen · ",
                 ("Bild-rauf / Bild-runter oder Mausrad über dem Brett", "b"), " = Stein-Set wechseln · ",
                 ("F1", "b"), " = Hilfedialog aufrufen · ",
                 ("F3 / F4", "b"), " = Schnell speichern / laden · ",
                 ("F5", "b"), " = Engine ziehen lassen · ",
                 ("F6", "b"), " = Einmalige Stellungsanalyse · ",
                 ("F7", "b"), " = ", ("LINK", "Dauer-Analyse", "buttons"), " ein- oder ausschalten · ",
                 ("Escape", "b"), " = Geöffnetes Menü schließen. "
                 "Hinweis: Tastenkürzel greifen, solange der Eingabefokus nicht in einem "
                 "Textfeld liegt."),
    ],
    "en": [
        ("head", "inhalt", "Contents"),
        ("para", ("LINK", "The Game", "spiel"), " · ",
                 ("LINK", "Entering Moves", "ziehen"), " · ",
                 ("LINK", "The Buttons Below the Board", "buttons"), " · ",
                 ("LINK", "The Evaluation (+, =, –)", "wertung"), " · ",
                 ("LINK", "Score (Human vs. Engine)", "spielstand"), " · ",
                 ("LINK", "Game Modes", "gegner"), " · ",
                 ("LINK", "Custom Levels: User (1) and User (2)", "userstufen"), " · ",
                 ("LINK", "The Levels", "stufen"), " · ",
                 ("LINK", "Playing Strength & Cross Table", "elorang"), " · ",
                 ("LINK", "File Menu", "datei"), " · ",
                 ("LINK", "Commands Menu", "kommandos"), " · ",
                 ("LINK", "View Menu", "ansicht"), " · ",
                 ("LINK", "Info Box, To Move and Status Bar", "info"), " · ",
                 ("LINK", "Settings Menu", "einstellungen"), " · ",
                 ("LINK", "Choosing the Language", "sprache"), " · ",
                 ("LINK", "Engine and Opening Book", "engine"), " · ",
                 ("LINK", "Keyboard Shortcuts", "tasten"), "."),

        ("head", "spiel", "The Game"),
        ("para", "ConnectFour Studio is an open-source application for “Connect Four” "
                 "with 15 levels, 20 selectable board designs, a tournament mode, "
                 "detailed match statistics and an exact real-time analysis."),
        ("para", "The basic rules of “Connect Four” are simple: Yellow (player 1) always "
                 "starts the game. The side that first manages to place four of its own "
                 "stones in an unbroken row – horizontally, vertically or diagonally – "
                 "wins. If all 42 cells of the grid are filled without a row of four, "
                 "the game ends in a ", ("draw", "b"), ". A completed winning row is ",
                 ("highlighted in green", "b"), " on the board."),
        ("para", "Moves can be made in three ways: with a ",
                 ("LINK", "mouse click", "ziehen"), ", with the ",
                 ("LINK", "number keys 1–7", "ziehen"), " or with the ",
                 ("Move (F5)", "b"), " button. The section ",
                 ("LINK", "“Entering Moves”", "ziehen"), " gives a detailed overview."),

        ("head", "ziehen", "Entering Moves"),
        ("para", ("Mouse input: ", "b"), "A click in the desired column drops a stone "
                 "there. When the pointer moves over the board, a semi-transparent ",
                 ("ghost stone", "b"), " shows where it will land. This preview can be "
                 "switched off at any time in the ",
                 ("LINK", "View", "ansicht"), " menu."),
        ("para", ("Keyboard control: ", "b"), "The number keys ",
                 ("1 to 7", "b"), " drop a stone directly into the corresponding column. "
                 "The keys ", ("Left arrow / Right arrow", "b"), " take back the last "
                 "move or replay it. ", ("Up arrow / Down arrow", "b"),
                 " jump straight to the start or the end of the game. The same "
                 "actions are available with the buttons ", ("<", "b"), ", ",
                 (">", "b"), ", ", ("<<", "b"), " and ", (">>", "b"), ". "
                 "The ", ("F5", "b"), " key makes the ",
                 ("LINK", "engine", "engine"), " calculate the next move for the side "
                 "to move – even on an empty board, in which case the computer "
                 "opens the game (see ",
                 ("LINK", "buttons below the board", "buttons"), ")."),
        ("para", ("Evaluation row: ", "b"), "A mouse click on one of the seven "
                 "cells below the board also makes the corresponding column move "
                 "(see ", ("LINK", "evaluation row", "wertung"), ")."),
        ("para", "The most recently played move is marked by a ",
                 ("white ring", "b"), " (can be switched off under ",
                 ("LINK", "View", "ansicht"), ")."),

        ("head", "buttons", "The Buttons Below the Board"),
        ("para", ("New: ", "b"), "Resets the board and starts a new game from the "
                 "starting position (see also ",
                 ("LINK", "File menu", "datei"), ")."),
        ("para", ("<< and >>: ", "b"), "Jump directly to the start of the game "
                 "or to the current end of the game."),
        ("para", ("< and >: ", "b"), "Take moves back or restore them step by step, "
                 "so that any move sequence can be reconstructed."),
        ("para", ("Move (F5): ", "b"), "Hands the move over to the ",
                 ("LINK", "engine", "engine"), ", which plays according to the "
                 "currently selected ", ("LINK", "level", "stufen"), "."),
        ("para", ("Analyze (F7): ", "b"), "Turns the ",
                 ("permanent analysis", "b"), " on or pauses it. While it is on, every "
                 "position is fully calculated in the background right after a move. "
                 "While it is off, the bar below the board shows only the neutral "
                 "column numbers ", ("1–7", "b"), " (see ",
                 ("LINK", "evaluation row", "wertung"), ")."),
        ("para", "More special functions are available from the menu bar: ",
                 ("File > New with random position…", "b"), " creates a "
                 "balanced position with 1 to 9 stones, optionally with a given "
                 "result (see ", ("LINK", "File menu", "datei"), "); the command ",
                 ("Commands > Evaluate all moves (1x)", "b"), " (", ("F6", "b"),
                 ") starts a one-time evaluation of all seven columns (see ",
                 ("LINK", "evaluation row", "wertung"), ")."),

        ("head", "wertung", "The Evaluation (+, =, –)"),
        ("para", "For each available column, the evaluation row below the board shows "
                 "a symbolic result at the top and, below it, the number of stones still "
                 "to be placed until the end of the game with perfect play from both "
                 "sides: ",
                 ("+ (green)", "b"), " = forced win, ",
                 ("= (yellow)", "b"), " = certain draw, ",
                 ("- (red)", "b"), " = unavoidable loss. ",
                 ("Completely filled columns are marked with an “X”.", "b")),
        ("para", "If no evaluation is active, only the column numbers ",
                 ("1–7", "b"), " are shown. The ", ("LINK", "Info box", "info"),
                 " at the right edge of the window also states the best continuation "
                 "in plain text, for example ", ("“Col. 4: Yellow wins”", "b"), "."),
        ("para", "The position evaluation is always ", ("mathematically perfect", "b"),
                 " (full search with the 12-ply-dist book) – independent of the "
                 "selected ", ("LINK", "level", "stufen"), ". Only the actual moves of the ",
                 ("LINK", "engine", "engine"), " are deliberately flawed at "
                 "lower levels. The distance number gives the exact number of stones "
                 "still to be placed until the decision: "
                 "a small value signals a quick end of the game, a high number "
                 "a long, tough endgame."),

        ("head", "spielstand", "Score (Human vs. Engine)"),
        ("para", "The ", ("Score", "b"), " display at the lower right, below the ",
                 ("LINK", "Info box", "info"), ", records the running session balance "
                 "in the duel of human against computer. In large type it shows the "
                 "score ", ("Human – Engine", "b"), " (for example ", ("2–1", "b"),
                 "), supplemented by the detailed statistics ",
                 ("(+wins / =draws / –losses)", "b"), " from the human player's point of "
                 "view and the total number of games played. An estimated Elo "
                 "difference is displayed as soon as both sides have been credited with "
                 "at least half a point."),
        ("para", "A separate statistic is kept for each ", ("opponent level", "b"),
                 ". When the level is changed (via ",
                 ("LINK", "Settings", "einstellungen"), "), counting starts "
                 "again at 0–0 for the new opponent; the previous balance is "
                 "discarded. Only games that ended regularly are scored: "
                 "the player who places the winning stone receives the full point. "
                 "In a draw each side receives half a point. Games ended early "
                 "(for example via ", ("New", "b"),
                 " or ", ("Stop auto play", "b"), ") do not count."),
        ("para", ("On/Off: ", "b"), "Hides or shows the numeric display; "
                 "the surrounding frame stays. While the display is off, "
                 "scoring is paused. ", ("Reset: ", "b"), "Sets the "
                 "score of the current level back to 0–0. Both "
                 "functions are also available from the ", ("LINK", "View", "ansicht"),
                 " menu (", ("Score on/off", "b"), ", ", ("Reset score", "b"),
                 "). By default, recording is switched off; counting "
                 "only starts once it is switched on."),

        ("head", "gegner", "Game Modes"),
        ("para", "The ", ("Settings", "b"), " menu sets the basic "
                 "game mode: ", ("Human-Computer", "b"), " (with a freely selectable ",
                 ("LINK", "opponent level", "stufen"), ") or ",
                 ("2 players (both human)", "b"), ". In two-player mode, "
                 "ConnectFour Studio serves as a virtual board with referee function "
                 "and an optional ", ("LINK", "permanent analysis", "buttons"),
                 " – a good tool for analyzing and training together."),
        ("para", ("Computer-Computer (play out): ", "b"), "Lets the engine finish "
                 "the current position against itself – always at the highest "
                 "level ", ("Perfect", "b"), ", regardless of the other "
                 "settings. The function can be called again at any time "
                 "and then continues from the current board position."),
        ("para", ("Computer-Computer match: ", "b"), "Runs a series of automated "
                 "games. You can set the ", ("number of games", "b"), " (1 to 10,000), "
                 "the player types for both colors (", ("Human", "b"), ", a ",
                 ("LINK", "fixed level", "stufen"), " or a ",
                 ("LINK", "custom level User (1)/(2)", "userstufen"), "), ",
                 ("color swap", "b"), " after every single game (Yellow and Red exchange "
                 "roles) and the ", ("speed", "b"), " (Normal / Fast / Results only). "
                 "If a human takes part in the match (one side is set to ",
                 ("Human", "b"), ") and the ", ("speed", "b"), " is set to ",
                 ("Normal", "b"), ", the program pauses for 3 seconds "
                 "after the end of a game so that the result can be checked. ",
                 ("Start", "b"), " starts the series, ", ("Stop", "b"), " (also "
                 "via the menu item ", ("Stop auto play", "b"), ") aborts it; the "
                 "interim result is kept. When the match is finished, "
                 "the dialog window comes to the front automatically; the "
                 "button ", ("Copy", "b"), " copies the complete "
                 "result report (points, win/draw balance and Elo evaluation) to "
                 "the clipboard."),

        ("head", "userstufen", "Custom Levels: User (1) and User (2)"),
        ("para", "In the configuration dialog of the ",
                 ("LINK", "Computer-Computer match", "gegner"), ", two freely "
                 "configurable profiles are available alongside the built-in levels: ",
                 ("User (1) (own p, s, w)", "b"), " and ",
                 ("User (2) (own p, s, w)", "b"), ". As soon as such a profile "
                 "is chosen for Yellow or Red, the corresponding "
                 "input field is enabled (field 1 controls User 1, field 2 controls "
                 "User 2). Here the three behavior parameters ",
                 ("p, s and w", "b"), " can be set individually (for how exactly they work, see ",
                 ("LINK", "The Levels", "stufen"), "). Since the two profiles are independent, "
                 "duels between two custom playing styles are also possible."),
        ("para", ("p = share of perfect moves in percent", "b"),
                 " (range 0 to 100): The blunder rate is calculated as ",
                 ("100 – p", "b"), ". A value of ", ("p = 100", "b"), " (as for ",
                 ("14 Perfect", "b"), ") guarantees flawless play on every move. "
                 "The extreme value ", ("p = 0", "b"), " (as for level ", ("6 Tactician", "b"),
                 " or in custom User profiles) means a ",
                 ("blunder rate of 100%", "b"), " – here the theoretical best move is never "
                 "chosen, the blunder routine is always run instead. This is not "
                 "pure chance (as on level 1), because the parameters s and w "
                 "steer the playing behavior: level 6 Tactician shows how strong a "
                 "profile with (0, 3, 3) plays through tactical safeguards alone. "
                 "With intermediate values such as ", ("p = 50", "b"), " (for example level 4 "
                 "Beginner or level 7 Intermediate), statistically every second move is "
                 "perfect, while the other 50% go into the blunder branch."),
        ("para", ("Decision sequence per move: ", "b"), "A short forced win ",
                 ("(w)", "b"), " always takes precedence – even before the p random "
                 "decision. If there is no such short win, the ", ("p draw", "b"),
                 " decides: if the choice is ", ("“perfect”", "b"), ", the ",
                 ("s filter", "b"), " plays no role – the engine chooses directly among "
                 "the theoretical best moves (ties are resolved by the 10-ply rule). "
                 "If the decision falls on ", ("“blunder”", "b"), " instead, the "
                 "filter chain applies: first ", ("w", "b"), " (win priority), then the loss filter ",
                 ("s", "b"), " and only at the end an evenly distributed choice among all "
                 "remaining admissible moves. A draw against a threatening defeat "
                 "is neither forced nor preferred here – it counts like any other allowed move."),
        ("para", ("s = loss protection in opponent moves", "b"), " (range 0 to 9): "
                 "This filter acts only in the blunder branch: a weaker move "
                 "is considered inadmissible if the opponent could then force a win "
                 "within at most s of their own moves. ", ("s = 0", "b"),
                 " means no filter – immediate blunders are accepted "
                 "(as on levels 1–4, where in the blunder case every legal move "
                 "is equally likely). ", ("s = 1", "b"), " blocks moves "
                 "that would hand the opponent the win on the very next move; ",
                 ("s = 2, 3 or 4", "b"), " extend this protection to 2, 3 "
                 "or 4 opponent moves. Wins and drawing lines are "
                 "always allowed in the blunder branch."),
        ("para", ("w = win priority", "b"), " (range 0 to 9): Short forced "
                 "wins always come first – even before the p random decision: if the "
                 "engine spots a winning path whose distance is within w moves, "
                 "this win is played. ", ("w = 1", "b"), " secures the "
                 "immediate win on the next move, ", ("w = 2", "b"), " guarantees the "
                 "win in at most 2 of its own moves; ", ("w = 3", "b"), " and ",
                 ("w = 4", "b"), " work analogously (for context see ",
                 ("LINK", "The Levels", "stufen"), "). If there is no such near win, the "
                 "regular p decision applies. ",
                 ("w = 0", "b"), " disables this look-ahead (in the perfect branch, wins "
                 "are of course still taken through the regular evaluation)."),
        ("para", ("Ties (perfect moves, all levels): ", "b"),
                 "If several equally good moves with the best score are available, "
                 "a random generator picks one, to avoid stereotypical repetitions of games. "
                 "If moves lead to a win within 10 plies, the fastest winning path "
                 "is chosen – among several equally fast ones, one is picked at random. "
                 "If no win is that close, one is drawn from all winning moves. "
                 "If there are only drawing lines, one of them is picked at random. "
                 "In purely losing positions, level ", ("14 Perfect", "b"),
                 " avoids defeats within 10 plies; if slower losing moves exist, "
                 "one of these is chosen. If all losing moves are "
                 "more than 10 plies away, one is drawn at random among all losing moves for variety."),
        ("para", "Comparative examples for orientation: the level ",
                 ("Beginner (50, 0, 0)", "b"), " plays every second move weakly and "
                 "completely unprotected; the level ", ("Intermediate (50, 1, 1)", "b"),
                 " also plays every second move weakly, but prevents "
                 "elementary immediate blunders on the following move and consistently "
                 "takes direct immediate wins. The configured parameters are shown in the reports of the ",
                 ("Computer-Computer match", "b"), " "
                 "(for example as ", ("“User (1) (70, 1, 1)”", "b"), ")."),

        ("head", "stufen", "The Levels"),
        ("para", "The regular levels are described by the parameters ",
                 ("(p, s, w)", "b"), " (level 0 loses on purpose, "
                 "level 1 plays pure chance, level 14 plays flawlessly): ",
                 ("p", "b"), " is the percentage of perfect moves, ",
                 ("s", "b"), " defines the loss protection in opponent moves "
                 "(prevents faulty moves that lead to defeat within s opponent moves), "
                 "and ", ("w", "b"), " denotes the win priority (forced wins "
                 "within w own moves are always played). "
                 "The distance figure below the symbol in the ",
                 ("LINK", "evaluation row", "wertung"), " gives the number "
                 "of stones still to be placed until the end of the game: 1 stands for the immediate "
                 "winning stone, small values mark short endings, large values long ones "
                 "(further explanation in the section ",
                 ("LINK", "Info box", "info"), ")."),
        ("para", ("0 Loser (fun level): ", "b"), "Plays deliberately weakly "
                 "and preferably chooses random losing moves. If no losing move is "
                 "available, the program falls back on a draw or a "
                 "random move. A pure fun level without a rating in the Elo system."),
        ("para", ("1 Random: ", "b"), "Plays pure chance: every legal move has "
                 "exactly the same probability. This level has no "
                 "(p, s, w) logic at all, no position evaluation and no filters – the "
                 "choice is made completely evenly from all open columns."),
        ("para", ("2 Very Easy (25, 0, 0): ", "b"), "Plays optimally 25% of the time and "
                 "purely at random 75% of the time; makes grave blunders – ideal for beginners "
                 "and children."),
        ("para", ("3 Easy (40, 0, 0): ", "b"), "Plays optimally 40% of the time, but "
                 "forgoes tactical safeguards (s = 0, w = 0)."),
        ("para", ("4 Beginner (50, 0, 0): ", "b"), "Every second move is played "
                 "theoretically perfectly (50%). Since s = 0 and w = 0, there is "
                 "no error filtering at all."),
        ("para", ("5 Advanced (20, 1, 1): ", "b"), "Chooses the theoretical "
                 "best move 20% of the time, but thanks to s = 1 and w = 1 overlooks neither its own immediate wins "
                 "nor the opponent's direct threats on the next move."),
        ("para", ("6 Tactician (0, 3, 3): ", "b"), "Never plays the theoretical best move "
                 "(p = 0), but plays tactically alert: forced wins within "
                 "up to 3 own moves are played (w = 3) and threatening "
                 "defeats within the next 3 opponent moves are averted "
                 "(s = 3). A tactically tough opponent without strategic foresight."),
        ("para", ("7 Intermediate (50, 1, 1): ", "b"), "Solid amateur standard: every second "
                 "move perfect (50%), reliable use of immediate wins (w = 1) and "
                 "consistent avoidance of immediate blunders (s = 1)."),
        ("para", ("8 Demanding (55, 1, 1): ", "b"), "Builds on level 7, but plays "
                 "completely flawlessly in more than half of all moves (55%)."),
        ("para", ("9 Hard (65, 1, 1): ", "b"), "With 65% optimal moves and reliable "
                 "protection against immediate blunders, a serious opponent for experienced club players."),
        ("para", ("10 Very Hard (70, 2, 2): ", "b"), "Combines high precision (70%) "
                 "with tactical instinct: recognizes and parries attacks over "
                 "2 opponent moves (s = 2) and reliably converts its own wins in 2 moves "
                 "(w = 2) – a hurdle for tournament players."),
        ("para", ("11 Expert (80, 2, 2): ", "b"), "Plays flawlessly 80% of the time and "
                 "reliably parries attacks over 2 opponent moves. Its own "
                 "winning threats over 2 moves are converted safely; the gateway to the master classes."),
        ("para", ("12 Master (85, 3, 3): ", "b"), "Plays very strongly (85% best moves) with "
                 "far-reaching tactical safeguards: sees threats and its own "
                 "winning paths over 3 moves (s = 3, w = 3). Even "
                 "experienced tournament players hardly score here any more."),
        ("para", ("13 Strong Master (92, 4, 4): ", "b"), "Almost infallible (92% best moves): "
                 "avoids forced losing variations up to 4 moves ahead "
                 "(s = 4) and converts its own wins over 4 moves "
                 "safely (w = 4)."),
        ("para", ("14 Perfect (100, -, -): ", "b"), "Plays flawlessly according to the "
                 "laws of the solved game: as the first player (Yellow) the "
                 "engine wins every game by force; as the second player (Red) it exploits every "
                 "inaccuracy of the opponent to take the full point. "
                 "Equivalent moves are varied statistically (see ",
                 ("Ties", "b"), " above). To train your own play, the position analysis "
                 "is recommended, see ", ("LINK", "Analysis", "wertung"), "."),
        ("para", "Orientation values for relative playing strength (determined in "
                 "engine-versus-engine tournaments with a total of 18,200 games – "
                 "200 games per pairing – with "
                 "continuous color swapping; reference basis level Random = 1000 Elo): "
                 "1 Random, 2 Very Easy ~1204, 3 Easy ~1340, "
                 "4 Beginner ~1431, 5 Advanced ~1498, 6 Tactician ~1614, "
                 "7 Intermediate ~1702, 8 Demanding ~1752, "
                 "9 Hard ~1817, 10 Very Hard ~1929, 11 Expert ~2010, "
                 "12 Master ~2080, 13 Strong Master ~2132, 14 Perfect ~2174. "
                 "In games against human opponents these differences can shift "
                 "psychologically and tactically. The strength table and cross table are given "
                 "in full in the section ", ("LINK", "“Playing Strength & Cross Table”", "elorang"), "."),
        ("head", "elorang", "Playing Strength & Cross Table"),
        ("para", "All 91 pairings were played with 200 games each and color swapping "
                 "(18,200 in total). Reference basis level Random = 1000 Elo "
                 "(relative, not FIDE Elo)."),
        ("para", ("Playing strength (Elo):", "b")),
        ("mono",
        " 1 Random                      1000\n"
        " 2 Very Easy        (25,0,0)   1204\n"
        " 3 Easy             (40,0,0)   1340\n"
        " 4 Beginner         (50,0,0)   1431\n"
        " 5 Advanced         (20,1,1)   1498\n"
        " 6 Tactician        (0,3,3)    1614\n"
        " 7 Intermediate     (50,1,1)   1702\n"
        " 8 Demanding        (55,1,1)   1752\n"
        " 9 Hard             (65,1,1)   1817\n"
        "10 Very Hard        (70,2,2)   1929\n"
        "11 Expert           (80,2,2)   2010\n"
        "12 Master           (85,3,3)   2080\n"
        "13 Strong Master    (92,4,4)   2132\n"
        "14 Perfect          (100,-,-)  2174"),
        ("para", ("Cross table (points of the row level against the column level, out of 200):", "b")),
        ("table", "kreuz14"),
        ("sub", "zugwahl", "Behind the Scenes: The 3-Step Move Selection"),
        ("para", ("This is how the engine decides every single move (levels 1–14): ", "b"),
                 "Every move goes through a fixed three-step decision chain. "
                 "It explains the whole interplay of playing strength, filters "
                 "and apparent paradoxes:"),
        ("para", ("1. Win priority (w) first – no dice at all: ", "b"),
                 "If the position offers a forced win within ",
                 ("w", "b"), " own moves, that move is played at once – even before the ",
                 ("p", "b"), " random decision. ",
                 ("w = 1", "b"), " means an immediate win. ",
                 ("w = 2", "b"), " means a win in at most 2 moves. ",
                 ("w = 3", "b"), " means a win in up to 3 moves. ",
                 ("(w = 0 switches this look-ahead off.)", "b"),
                 " Only if there is no such short win does step 2 follow."),
        ("para", ("2. The p draw (perfect or blunder): ", "b"),
                 "For each move, in isolation and without memory, the probability ",
                 ("p", "b"), " decides whether the engine plays well or weakly. ",
                 "At ", ("p = 50", "b"), " (Beginner, Intermediate) statistically every second move is perfect. ",
                 "At ", ("p = 20", "b"), " (Advanced) only every fifth. ",
                 "At ", ("p = 80", "b"), " (Expert) four out of five. ",
                 "Streaks are purely random: even at ", ("p = 50", "b"),
                 " three blunders in a row – or three perfect moves – can occur."),
        ("para", ("3a. Perfect drawn: best score and the 10-ply rule: ", "b"),
                 "The engine chooses directly among the theoretical best moves: ",
                 "among several equally good winning moves, the fastest one within "
                 "10 plies is played; among several equally fast ones, one is picked at random. ",
                 "If no win lies within 10 plies, one is picked at random among all remaining "
                 "winning moves (all of which are then more than 10 plies away). ",
                 "If there are only draws, one of them is picked at random. ",
                 "If there are only losing moves, the loss rule applies (longest resistance, weighted – "
                 "with 10-ply protection at Perfect)."),
        ("para", ("3b. Weak drawn: the blunder routine: ", "b"),
                 "This is not blind dice rolling, but a filtered move: ",
                 "the filter ", ("s", "b"), " blocks all moves after which the opponent would win in at most ",
                 ("s", "b"), " moves (", ("s = 1", "b"),
                 " forbids immediate blunders on the next move; ", ("s = 0", "b"),
                 " filters nothing). ",
                 "Among all remaining allowed moves one is picked ", ("evenly at random", "b"),
                 " – a draw is not preferred here, it counts like any other admissible move. ",
                 ("Special cases: ", "b"), ("p = 100", "b"), " (Perfect) always goes to 3a. ",
                 ("p = 0", "b"), " (Tactician) always goes to 3b. ",
                 ("s = 0, w = 0", "b"), " (levels 1–4) picks completely unfiltered in 3b."),
        ("sub", "filterparadox", "The Filter Paradox: Tactician vs. Beginner (149.5 : 50.5)"),
        ("para", "In a direct duel, level ", ("6 Tactician (0, 3, 3)", "b"),
                 " beats ", ("4 Beginner (50, 0, 0)", "b"),
                 " clearly, by almost 3 : 1, although the Tactician does not play a single perfect move. ",
                 "The reason lies in the interplay of ", ("shield and sword", "b"), ": ",
                 "thanks to ", ("s = 3", "b"), " the Tactician gives away almost nothing through quick blunders. ",
                 "And thanks to ", ("w = 3", "b"), " it converts every available win in 1 to 3 moves. ",
                 "The Beginner, by contrast, throws away its opening advantages through unfiltered immediate blunders (",
                 ("s = 0", "b"), ") and, lacking win priority (",
                 ("w = 0", "b"), "), often lets the opponent's mistakes go unpunished. ",
                 "The same principle shows with ", ("5 Advanced (20, 1, 1)", "b"),
                 ", which beats the Beginner 137 : 63 despite a far lower ", ("p", "b"), "."),
        ("sub", "spitzenumkehr", "The Reversal at the Top: Points against Masters"),
        ("para", "Against the strongest opponents (Strong Master and Perfect) the picture reverses: ",
                 "here, out of 400 games, the Beginner scores ", ("7.0 points", "b"),
                 " – the Tactician only ", ("0.5 points", "b"), " (a fourteenth of that). ",
                 "Strong opponents practically never blunder. Neither ",
                 ("s = 3", "b"), " nor ", ("w = 3", "b"),
                 " helps much, because the Master offers hardly any target. ",
                 "To score against nearly flawless Masters at all, you need perfect moves "
                 "with a deep strategic plan – short-range loss protection or win priority is not enough. "
                 "The Beginner plays about every second move perfectly; "
                 "now and then one of them is enough for a draw. The Tactician lacks such moves entirely."),

        ("head", "datei", "File Menu"),
        ("para", ("New game: ", "b"), "Resets the board to the empty starting position. ",
                 ("New with random position…: ", "b"), "Creates a randomly built "
                 "middlegame position with 1 to 9 stones, optionally with a guaranteed "
                 "theoretical outcome (win, draw or loss). ",
                 ("Load position… ", "b"), "and ", ("Save position…: ", "b"),
                 "Open a standard file dialog for the universal ",
                 (".4gp format", "b"), ". A saved game consists of the "
                 "chronological digit string of the chosen columns, such as ",
                 ("4433221", "b"), ". ", ("Quick save (F3) ", "b"), "and ",
                 ("Quick load (F4): ", "b"), "Save or load the current "
                 "game record directly to or from the file ",
                 ("quicksave.4gp", "b"), " in the main directory of the program, without an intermediate dialog. ",
                 ("Quit: ", "b"), "Closes ConnectFour Studio properly."),

        ("head", "kommandos", "Commands Menu"),
        ("para", ("First / last move (Up arrow / Down arrow): ", "b"),
                 "Jumps to the start or the end of the game; moves that were taken back "
                 "stay in memory and can be replayed at any time. ",
                 ("Move back / forward: ", "b"), "Steps through the game "
                 "(like the buttons ", ("<", "b"), " and ", (">", "b"), "). ",
                 ("Move (computer): ", "b"), "Corresponds to the shortcut ", ("F5", "b"), ". ",
                 ("Evaluate all moves (1x): ", "b"), "Corresponds to ", ("F6", "b"), " (see ",
                 ("LINK", "evaluation row", "wertung"), "). ",
                 ("Permanent analysis: ", "b"), "Corresponds to ", ("F7", "b"), " (see ",
                 ("LINK", "View menu", "ansicht"), ")."),

        ("head", "ansicht", "View Menu"),
        ("para", ("Ghost stone: ", "b"), "Switches the semi-transparent drop preview on or off. ",
                 ("Drop animation: ", "b"), "Controls the smooth falling movement of dropped stones. ",
                 ("Show last move: ", "b"), "Enables or disables the white marker ring "
                 "on the most recent stone. ",
                 ("Score on/off ", "b"), "and ",
                 ("Reset score: ", "b"), "Correspond to the buttons of the ",
                 ("LINK", "Score area", "spielstand"), ". The help window can be opened "
                 "at any time via the menu or with ", ("F1", "b"), "."),

        ("head", "info", "Info Box, To Move and Status Bar"),
        ("para", "At the top right, the ", ("To move", "b"),
                 " box shows, by means of the stone symbol and the name, who is to move: ",
                 ("Human", "b"), " or the engine, naming the active level "
                 "(for example “User (1) (70,1,1)”). In two-player mode, "
                 "Human is always shown here."),
        ("para", "Directly below, the ", ("Info box", "b"),
                 " provides key figures on the current board situation:"),
        ("para", ("Move: ", "b"), "Running number of the next ply (starting at 1)."),
        ("para", ("Level: ", "b"), "Active ",
                 ("LINK", "level", "stufen"),
                 " of the engine (in tournament mode, the level of the color to move)."),
        ("para", ("Depth: ", "b"), "Most recently reached search depth in plies. ",
                 ("Full: ", "b"), "Complete calculation to the end of the game. ",
                 ("Book 12d: ", "b"), "Up to 12 stones the search stops as soon as every line reaches the opening book – the values are exact. ", ("Book 2d: ", "b"), "Position with at most two stones: exact values from the built-in mini book, without any search. "
                 "A trailing ellipsis (e.g. “8...”) shows a deepening that is still "
                 "running. A dash (–) means that no calculation is available yet."),
        ("para", ("Value: ", "b"), "Theoretical evaluation of the latest move in "
                 "compact notation – for example “Yellow (31)”, “Red (28)” or "
                 "“Draw (40)”. The label names the winning side with optimal play "
                 "from both sides. The number in brackets is the number "
                 "of stones still to be placed until the final decision: small numbers "
                 "(1–6) signal an imminent decision – a ",
                 ("1", "b"), " in brackets marks the direct immediate win on the next move. "
                 "High values (30–42) indicate a long endgame (42 would be "
                 "a draw from the empty position). With every move played, this "
                 "value counts down by 1. The distance number below the symbol in the ",
                 ("LINK", "evaluation row", "wertung"), " after an analysis (",
                 ("F6", "b"), "/", ("F7", "b"),
                 ") shows the same stone count per column. "
                 "Before the first analysis a dash (–) appears. After the game is completed, the "
                 "final result is announced here, for example “Yellow wins!”."),
        ("para", ("Nodes: ", "b"), "Number of positions searched in the search tree "
                 "(real-time feedback from the C++ core, with readable thousands separators). ",
                 ("Time: ", "b"), "Pure calculation time of the last analysis in milliseconds. ",
                 ("Speed: ", "b"), "Search speed in nodes per second "
                 "(for example 2.3 M/s = 2.3 million positions/s). All values "
                 "refer to the most recent calculation step."),
        ("para", ("Source: ", "b"), "Origin of the position data: ",
                 ("Book 12d", "b"), " = lookup in the integrated opening book (up "
                 "to a depth of 12 stones), ", ("computed", "b"), " = free "
                 "real-time calculation by the engine. A dash (–) indicates "
                 "the initial state before the search begins."),
        ("para", "The ", ("status bar", "b"), " at the bottom edge of the window reports "
                 "moves played (e.g. “Computer played 4 in 0.35 s”), analysis reports "
                 "and file operations. While a calculation is running, "
                 "it shows “Computer is still thinking – please wait.” A load attempt during the "
                 "search is rejected with the message “Computer is still thinking – stop it first, then load.” "
                 "In that case the calculation must first be interrupted with "
                 "the stop function."),

        ("head", "einstellungen", "Settings Menu"),
        ("para", "The ", ("Settings", "b"), " menu bundles the central options: ",
                 ("Computer level", "b"), " (sets the playing strength from level ",
                 ("LINK", "0 to 14", "stufen"), "; can also be changed during a running "
                 "game – the ", ("LINK", "score", "spielstand"),
                 " starts again at 0–0 after a change), ",
                 ("Human-Computer", "b"), " (a game against the artificial intelligence), ",
                 ("2 players (both human)", "b"), " (two people play against each other; "
                 "the program takes over the referee function and the visualization), ",
                 ("Computer-Computer (play out)", "b"), " (the engine plays both "
                 "sides from the current position, see ",
                 ("LINK", "game modes", "gegner"), "), ",
                 ("Computer-Computer match", "b"), " (configures automated games "
                 "and tournaments, see ", ("LINK", "game modes", "gegner"), "), ",
                 ("Stop auto play", "b"), " (stops a running match immediately; "
                 "the interim result is kept) and ",
                 ("Stone set", "b"), " (choice of 20 board and stone designs; "
                 "you can also browse through them with the mouse wheel over the "
                 "board or with the Page Up / Page Down keys)."),

        ("head", "sprache", "Choosing the Language"),
        ("para", "In the ", ("Help", "b"), " menu under ", ("Language", "b"), " the "
                 "available languages are listed: ", ("Deutsch", "b"), ", ", ("English", "b"), ", ",
                 ("Français", "b"), ", ", ("Español", "b"), ", ", ("Nederlands", "b"), " and ",
                 ("Italiano", "b"), ". "
                 "The selection (a radio button) takes effect immediately for Help and Info."),

        ("head", "engine", "Engine and Opening Book"),
        ("para", "The mathematical calculation core is ",
                 ("BitBully by Markus Thill", "b"), " – an efficient Python module "
                 "with a C++ core. It uses optimized bitboards, "
                 "iterative deepening with an MTD(f)/null-window search algorithm "
                 "and dynamic transposition tables. The integrated opening book ",
                 ("12-ply-dist", "b"), " provides theoretical evaluations and exact "
                 "distance values for all positions with up to 12 stones placed; "
                 "in deeper variations the search engine continues the calculation."),
        ("para", "ConnectFour Studio combines a lean desktop interface (Python, Tkinter, "
                 "graphics rendering with Pillow) with a solved game. "
                 "Licensed as free software under the ",
                 ("GNU Affero General Public License (AGPL v3)", "b"), "."),

        ("head", "tasten", "Keyboard Shortcuts"),
        ("para", ("1–7", "b"), " = make a column move · ",
                 ("Left arrow / Right arrow", "b"), " = take back / replay a move · ",
                 ("Up arrow / Down arrow", "b"), " = jump to start / end of the game · ",
                 ("Page Up / Page Down or mouse wheel over the board", "b"), " = change stone set · ",
                 ("F1", "b"), " = open the help dialog · ",
                 ("F3 / F4", "b"), " = quick save / load · ",
                 ("F5", "b"), " = let the engine move · ",
                 ("F6", "b"), " = one-time position analysis · ",
                 ("F7", "b"), " = switch ", ("LINK", "permanent analysis", "buttons"), " on or off · ",
                 ("Escape", "b"), " = close an open menu. "
                 "Note: shortcuts work as long as the input focus is not in a "
                 "text field."),
    ],
    "es": [
        ("head", "inhalt", "Contenido"),
        ("para", ("LINK", "El juego", "spiel"), " · ",
                 ("LINK", "Introducir jugadas", "ziehen"), " · ",
                 ("LINK", "Los botones bajo el tablero", "buttons"), " · ",
                 ("LINK", "La evaluación (+, =, –)", "wertung"), " · ",
                 ("LINK", "Marcador (humano contra motor)", "spielstand"), " · ",
                 ("LINK", "Modos de juego", "gegner"), " · ",
                 ("LINK", "Niveles personalizados: User (1) y User (2)", "userstufen"), " · ",
                 ("LINK", "Los niveles", "stufen"), " · ",
                 ("LINK", "Fuerza de juego y tabla cruzada", "elorang"), " · ",
                 ("LINK", "Menú Archivo", "datei"), " · ",
                 ("LINK", "Menú Comandos", "kommandos"), " · ",
                 ("LINK", "Menú Ver", "ansicht"), " · ",
                 ("LINK", "Cuadro de información, turno y barra de estado", "info"), " · ",
                 ("LINK", "Menú Configuración", "einstellungen"), " · ",
                 ("LINK", "Elegir el idioma", "sprache"), " · ",
                 ("LINK", "Motor y libro de aperturas", "engine"), " · ",
                 ("LINK", "Atajos de teclado", "tasten"), "."),

        ("head", "spiel", "El juego"),
        ("para", "ConnectFour Studio es una aplicación de código abierto para “Cuatro en Raya” "
                 "con 15 niveles, 20 diseños de tablero a elegir, un modo de torneo, "
                 "estadísticas detalladas de partidos y un análisis exacto en tiempo real."),
        ("para", "Las reglas básicas de “Cuatro en Raya” son sencillas: el Amarillo (jugador 1) "
                 "siempre empieza la partida. Gana el bando que primero consigue colocar "
                 "cuatro fichas propias en una fila ininterrumpida, en horizontal, "
                 "en vertical o en diagonal. Si las 42 casillas de la cuadrícula se llenan "
                 "sin que haya una fila de cuatro, la partida termina en ", ("tablas", "b"),
                 ". Una fila ganadora completada se ", ("resalta en verde", "b"),
                 " sobre el tablero."),
        ("para", "Las jugadas se pueden hacer de tres maneras: con un ",
                 ("LINK", "clic del ratón", "ziehen"), ", con las ",
                 ("LINK", "teclas numéricas 1–7", "ziehen"), " o con el botón ",
                 ("Jugar (F5)", "b"), ". La sección ",
                 ("LINK", "“Introducir jugadas”", "ziehen"), " ofrece una visión detallada."),

        ("head", "ziehen", "Introducir jugadas"),
        ("para", ("Entrada con el ratón: ", "b"), "Un clic en la columna deseada deja caer "
                 "allí una ficha. Cuando el puntero pasa por el tablero, una ",
                 ("ficha fantasma", "b"), " semitransparente muestra dónde caerá. "
                 "Esta vista previa se puede desactivar en cualquier momento en el menú ",
                 ("LINK", "Ver", "ansicht"), "."),
        ("para", ("Control con el teclado: ", "b"), "Las teclas numéricas ",
                 ("1 a 7", "b"), " dejan caer una ficha directamente en la columna "
                 "correspondiente. Las teclas ", ("Flecha izquierda / Flecha derecha", "b"),
                 " deshacen la última jugada o la repiten. ", ("Flecha arriba / Flecha abajo", "b"),
                 " saltan directamente al principio o al final de la partida. Las mismas "
                 "acciones están disponibles con los botones ", ("<", "b"), ", ",
                 (">", "b"), ", ", ("<<", "b"), " y ", (">>", "b"), ". "
                 "La tecla ", ("F5", "b"), " hace que el ",
                 ("LINK", "motor", "engine"), " calcule la siguiente jugada del bando "
                 "al que le toca, incluso con el tablero vacío; en ese caso el ordenador "
                 "abre la partida (véase ",
                 ("LINK", "botones bajo el tablero", "buttons"), ")."),
        ("para", ("Fila de evaluación: ", "b"), "Un clic del ratón en una de las siete "
                 "casillas situadas bajo el tablero también ejecuta la jugada en la "
                 "columna correspondiente (véase ", ("LINK", "fila de evaluación", "wertung"), ")."),
        ("para", "La última jugada realizada se marca con un ",
                 ("anillo blanco", "b"), " (se puede desactivar en ",
                 ("LINK", "Ver", "ansicht"), ")."),

        ("head", "buttons", "Los botones bajo el tablero"),
        ("para", ("Nueva: ", "b"), "Reinicia el tablero y empieza una nueva partida "
                 "desde la posición inicial (véase también ",
                 ("LINK", "menú Archivo", "datei"), ")."),
        ("para", ("<< y >>: ", "b"), "Saltan directamente al principio de la partida "
                 "o al final actual de la partida."),
        ("para", ("< y >: ", "b"), "Deshacen jugadas o las restablecen paso a paso, "
                 "para poder reconstruir cualquier secuencia de jugadas."),
        ("para", ("Jugar (F5): ", "b"), "Cede la jugada al ",
                 ("LINK", "motor", "engine"), ", que juega según el ",
                 ("LINK", "nivel", "stufen"), " seleccionado en ese momento."),
        ("para", ("Analizar (F7): ", "b"), "Activa o pausa el ",
                 ("análisis permanente", "b"), ". Mientras está activado, cada "
                 "posición se calcula por completo en segundo plano justo después de "
                 "una jugada. Mientras está desactivado, la barra situada bajo el tablero "
                 "solo muestra los números de columna neutros ", ("1–7", "b"), " (véase ",
                 ("LINK", "fila de evaluación", "wertung"), ")."),
        ("para", "Otras funciones especiales están disponibles en la barra de menús: ",
                 ("Archivo > Nueva con posición aleatoria…", "b"), " crea una "
                 "posición equilibrada con 1 a 9 fichas, opcionalmente con un "
                 "resultado dado (véase ", ("LINK", "menú Archivo", "datei"), "); el comando ",
                 ("Comandos > Evaluar todas las jugadas (1x)", "b"), " (", ("F6", "b"),
                 ") inicia una evaluación única de las siete columnas (véase ",
                 ("LINK", "fila de evaluación", "wertung"), ")."),

        ("head", "wertung", "La evaluación (+, =, –)"),
        ("para", "Para cada columna disponible, la fila de evaluación situada bajo el tablero muestra "
                 "arriba un resultado simbólico y, debajo, el número de fichas que aún "
                 "quedan por colocar hasta el final de la partida con juego perfecto de ambos "
                 "bandos: ",
                 ("+ (verde)", "b"), " = victoria forzada, ",
                 ("= (amarillo)", "b"), " = tablas seguras, ",
                 ("- (rojo)", "b"), " = derrota inevitable. ",
                 ("Las columnas completamente llenas se marcan con una “X”.", "b")),
        ("para", "Si no hay ninguna evaluación activa, solo se muestran los números de columna ",
                 ("1–7", "b"), ". El ", ("LINK", "cuadro de información", "info"),
                 " del borde derecho de la ventana indica además la mejor continuación "
                 "en texto claro, por ejemplo ", ("“Col. 4: gana el Amarillo”", "b"), "."),
        ("para", "La evaluación de la posición es siempre ", ("matemáticamente perfecta", "b"),
                 " (búsqueda completa con el libro 12-ply-dist), con independencia del ",
                 ("LINK", "nivel", "stufen"), " seleccionado. Solo las jugadas reales del ",
                 ("LINK", "motor", "engine"), " son deliberadamente defectuosas en los "
                 "niveles bajos. El número de distancia indica el número exacto de fichas "
                 "que aún quedan por colocar hasta la decisión: "
                 "un valor pequeño indica un final rápido de la partida, un número alto "
                 "un final largo y duro."),

        ("head", "spielstand", "Marcador (humano contra motor)"),
        ("para", "El indicador de ", ("Marcador", "b"), ", situado abajo a la derecha, bajo el ",
                 ("LINK", "cuadro de información", "info"), ", registra el balance continuo de la sesión "
                 "en el duelo de humano contra ordenador. En letra grande muestra el "
                 "resultado ", ("Humano – Motor", "b"), " (por ejemplo ", ("2–1", "b"),
                 "), completado con la estadística detallada ",
                 ("(+victorias / =tablas / –derrotas)", "b"), " desde el punto de "
                 "vista del jugador humano y con el número total de partidas jugadas. Se muestra una "
                 "diferencia de Elo estimada en cuanto ambos bandos suman "
                 "al menos medio punto."),
        ("para", "Se lleva una estadística aparte para cada ", ("nivel del rival", "b"),
                 ". Cuando se cambia el nivel (mediante ",
                 ("LINK", "Configuración", "einstellungen"), "), el recuento vuelve a empezar "
                 "en 0–0 con el nuevo rival; el balance anterior "
                 "se descarta. Solo cuentan las partidas terminadas con normalidad: "
                 "quien coloca la ficha ganadora recibe el punto completo. "
                 "En caso de tablas, cada bando recibe medio punto. Las partidas terminadas "
                 "antes de tiempo (por ejemplo con ", ("Nueva", "b"),
                 " o ", ("Detener juego automático", "b"), ") no cuentan."),
        ("para", ("Sí/No: ", "b"), "Oculta o muestra la indicación numérica; "
                 "el marco que la rodea permanece. Mientras la indicación está desactivada, "
                 "el registro de puntos está en pausa. ", ("Reiniciar: ", "b"), "Devuelve "
                 "el marcador del nivel actual a 0–0. Ambas "
                 "funciones también están disponibles en el menú ", ("LINK", "Ver", "ansicht"),
                 " (", ("Marcador sí/no", "b"), ", ", ("Reiniciar marcador", "b"),
                 "). Por defecto el registro está desactivado; el recuento "
                 "solo empieza cuando se activa."),

        ("head", "gegner", "Modos de juego"),
        ("para", "El menú ", ("Configuración", "b"), " establece el "
                 "modo de juego básico: ", ("Humano-Ordenador", "b"), " (con un ",
                 ("LINK", "nivel del rival", "stufen"), " de libre elección) o ",
                 ("2 jugadores (ambos humanos)", "b"), ". En el modo de dos jugadores, "
                 "ConnectFour Studio sirve como tablero virtual con función de árbitro "
                 "y un ", ("LINK", "análisis permanente", "buttons"),
                 " opcional: una buena herramienta para analizar y entrenar juntos."),
        ("para", ("Ordenador-Ordenador (jugar hasta el final): ", "b"), "Hace que el motor termine "
                 "la posición actual jugando contra sí mismo, siempre en el "
                 "nivel más alto, ", ("Perfecto", "b"), ", con independencia del resto de "
                 "ajustes. La función se puede volver a llamar en cualquier momento "
                 "y continúa desde la posición actual del tablero."),
        ("para", ("Partido Ordenador-Ordenador: ", "b"), "Ejecuta una serie de partidas "
                 "automáticas. Se pueden ajustar el ", ("número de partidas", "b"), " (de 1 a 10.000), "
                 "los tipos de jugador de ambos colores (", ("Humano", "b"), ", un ",
                 ("LINK", "nivel fijo", "stufen"), " o un ",
                 ("LINK", "nivel personalizado User (1)/(2)", "userstufen"), "), el ",
                 ("cambio de color", "b"), " tras cada partida (el Amarillo y el Rojo intercambian "
                 "sus papeles) y la ", ("velocidad", "b"), " (Normal / Rápido / Solo resultados). "
                 "Si un humano participa en el partido (un bando está en ",
                 ("Humano", "b"), ") y la ", ("velocidad", "b"), " está en ",
                 ("Normal", "b"), ", el programa hace una pausa de 3 segundos "
                 "al terminar una partida para que se pueda revisar el resultado. ",
                 ("Iniciar", "b"), " inicia la serie, ", ("Detener", "b"), " (también "
                 "mediante el elemento de menú ", ("Detener juego automático", "b"), ") la cancela; el "
                 "resultado parcial se conserva. Cuando termina el partido, "
                 "la ventana de diálogo pasa automáticamente al primer plano; el "
                 "botón ", ("Copiar", "b"), " copia el informe completo "
                 "de resultados (puntos, balance de victorias y tablas y evaluación Elo) al "
                 "portapapeles."),

        ("head", "userstufen", "Niveles personalizados: User (1) y User (2)"),
        ("para", "En el diálogo de configuración del ",
                 ("LINK", "partido Ordenador-Ordenador", "gegner"), ", además de los niveles "
                 "integrados hay dos perfiles configurables libremente: ",
                 ("User (1) (p,s,w propios)", "b"), " y ",
                 ("User (2) (p,s,w propios)", "b"), ". En cuanto se elige uno de esos perfiles "
                 "para el Amarillo o el Rojo, se habilita el "
                 "campo de entrada correspondiente (el campo 1 controla a User 1, el campo 2 controla a "
                 "User 2). Aquí se pueden fijar individualmente los tres parámetros de comportamiento ",
                 ("p, s y w", "b"), " (para saber exactamente cómo funcionan, véase ",
                 ("LINK", "Los niveles", "stufen"), "). Como los dos perfiles son independientes, "
                 "también son posibles duelos entre dos estilos de juego personalizados."),
        ("para", ("p = proporción de jugadas perfectas en porcentaje", "b"),
                 " (rango de 0 a 100): La tasa de errores se calcula como ",
                 ("100 – p", "b"), ". Un valor de ", ("p = 100", "b"), " (como en el nivel ",
                 ("14 Perfecto", "b"), ") garantiza un juego sin fallos en cada jugada. "
                 "El valor extremo ", ("p = 0", "b"), " (como en el nivel ", ("6 Táctico", "b"),
                 " o en los perfiles User personalizados) significa una ",
                 ("tasa de errores del 100 %", "b"), ": aquí nunca se elige la mejor jugada "
                 "teórica, sino que siempre se ejecuta la rutina de errores. Esto no es "
                 "azar puro (como en el nivel 1), porque los parámetros s y w "
                 "controlan el comportamiento de juego: el nivel 6 Táctico muestra lo fuerte que juega un "
                 "perfil con (0, 3, 3) solo gracias a la protección táctica. "
                 "Con valores intermedios como ", ("p = 50", "b"), " (por ejemplo el nivel 4 "
                 "Principiante o el nivel 7 Intermedio), estadísticamente una de cada dos jugadas es "
                 "perfecta, mientras que el otro 50 % va a la rama de errores."),
        ("para", ("Secuencia de decisión por jugada: ", "b"), "Una victoria forzada corta ",
                 ("(w)", "b"), " tiene siempre prioridad, incluso antes de la decisión aleatoria de p. "
                 "Si no hay una victoria corta así, decide el ", ("sorteo de p", "b"),
                 ": si la elección es ", ("“perfecta”", "b"), ", el ",
                 ("filtro s", "b"), " no interviene: el motor elige directamente entre "
                 "las mejores jugadas teóricas (los empates se resuelven con la regla de las 10 semijugadas). "
                 "Si la decisión recae en cambio en ", ("“error”", "b"), ", se aplica la "
                 "cadena de filtros: primero ", ("w", "b"), " (prioridad de victoria), después el filtro de derrota ",
                 ("s", "b"), " y solo al final una elección con distribución uniforme entre todas las "
                 "jugadas admisibles restantes. Unas tablas frente a una derrota inminente "
                 "ni se fuerzan ni se prefieren aquí: cuentan como cualquier otra jugada permitida."),
        ("para", ("s = protección contra la derrota en jugadas del rival", "b"), " (rango de 0 a 9): "
                 "Este filtro actúa solo en la rama de errores: una jugada más débil "
                 "se considera inadmisible si el rival pudiera entonces forzar la victoria "
                 "en como máximo s jugadas propias. ", ("s = 0", "b"),
                 " significa sin filtro: se aceptan los errores inmediatos "
                 "(como en los niveles 1–4, donde en caso de error todas las jugadas legales "
                 "son igual de probables). ", ("s = 1", "b"), " bloquea las jugadas "
                 "que regalarían la victoria al rival en la siguiente jugada; ",
                 ("s = 2, 3 o 4", "b"), " amplían esta protección a 2, 3 "
                 "o 4 jugadas del rival. Las victorias y las líneas de tablas "
                 "siempre están permitidas en la rama de errores."),
        ("para", ("w = prioridad de victoria", "b"), " (rango de 0 a 9): Las victorias forzadas "
                 "cortas van siempre primero, incluso antes de la decisión aleatoria de p: si el "
                 "motor descubre un camino ganador cuya distancia está dentro de w jugadas, "
                 "esa victoria se juega. ", ("w = 1", "b"), " asegura la "
                 "victoria inmediata en la siguiente jugada, ", ("w = 2", "b"), " garantiza la "
                 "victoria en como máximo 2 jugadas propias; ", ("w = 3", "b"), " y ",
                 ("w = 4", "b"), " funcionan de forma análoga (para el contexto, véase ",
                 ("LINK", "Los niveles", "stufen"), "). Si no hay una victoria tan cercana, se aplica la "
                 "decisión normal de p. ",
                 ("w = 0", "b"), " desactiva esta anticipación (en la rama perfecta, las victorias "
                 "se siguen aprovechando, por supuesto, mediante la evaluación normal)."),
        ("para", ("Jugadas equivalentes (jugadas perfectas, todos los niveles): ", "b"),
                 "Si hay varias jugadas igual de buenas con la mejor puntuación, "
                 "un generador aleatorio elige una, para evitar repeticiones estereotipadas de partidas. "
                 "Si hay jugadas que llevan a la victoria dentro de 10 semijugadas, se elige "
                 "el camino ganador más rápido; entre varios igual de rápidos se elige uno al azar. "
                 "Si no hay ninguna victoria tan cercana, se sortea entre todas las jugadas ganadoras. "
                 "Si solo hay líneas de tablas, se elige una de ellas al azar. "
                 "En posiciones puramente perdidas, el nivel ", ("14 Perfecto", "b"),
                 " evita derrotas dentro de 10 semijugadas; si existen jugadas perdedoras más lentas, "
                 "se elige una de ellas. Si todas las jugadas perdedoras están "
                 "a más de 10 semijugadas, se sortea entre todas las jugadas perdedoras para dar variedad."),
        ("para", "Ejemplos comparativos como orientación: el nivel ",
                 ("Principiante (50, 0, 0)", "b"), " juega una de cada dos jugadas débilmente y "
                 "completamente sin protección; el nivel ", ("Intermedio (50, 1, 1)", "b"),
                 " también juega una de cada dos jugadas débilmente, pero evita los "
                 "errores inmediatos elementales en la jugada siguiente y aprovecha de forma consecuente "
                 "las victorias inmediatas directas. Los parámetros configurados se muestran en los informes del ",
                 ("partido Ordenador-Ordenador", "b"), " "
                 "(por ejemplo como ", ("“User (1) (70, 1, 1)”", "b"), ")."),

        ("head", "stufen", "Los niveles"),
        ("para", "Los niveles regulares se describen mediante los parámetros ",
                 ("(p, s, w)", "b"), " (el nivel 0 pierde a propósito, "
                 "el nivel 1 juega al puro azar, el nivel 14 juega sin fallos): ",
                 ("p", "b"), " es el porcentaje de jugadas perfectas, ",
                 ("s", "b"), " define la protección contra la derrota en jugadas del rival "
                 "(evita jugadas erróneas que llevan a la derrota en s jugadas del rival), "
                 "y ", ("w", "b"), " designa la prioridad de victoria (las victorias forzadas "
                 "en w jugadas propias se juegan siempre). "
                 "La cifra de distancia bajo el símbolo de la ",
                 ("LINK", "fila de evaluación", "wertung"), " indica el número "
                 "de fichas que aún quedan por colocar hasta el final de la partida: 1 es la ficha "
                 "ganadora inmediata, los valores pequeños marcan finales cortos y los grandes finales largos "
                 "(más explicaciones en la sección ",
                 ("LINK", "Cuadro de información", "info"), ")."),
        ("para", ("0 Perdedor (nivel de diversión): ", "b"), "Juega deliberadamente mal "
                 "y elige de preferencia jugadas perdedoras al azar. Si no hay ninguna jugada "
                 "perdedora disponible, el programa recurre a tablas o a una "
                 "jugada al azar. Un nivel puramente de diversión, sin puntuación en el sistema Elo."),
        ("para", ("1 Aleatorio: ", "b"), "Juega al puro azar: cada jugada legal tiene "
                 "exactamente la misma probabilidad. Este nivel no tiene ninguna "
                 "lógica (p, s, w), ni evaluación de posiciones, ni filtros: la "
                 "elección se hace de forma totalmente uniforme entre todas las columnas abiertas."),
        ("para", ("2 Muy fácil (25, 0, 0): ", "b"), "Juega de forma óptima el 25 % de las veces y "
                 "al puro azar el 75 %; comete errores graves: ideal para principiantes "
                 "y niños."),
        ("para", ("3 Fácil (40, 0, 0): ", "b"), "Juega de forma óptima el 40 % de las veces, pero "
                 "prescinde de las protecciones tácticas (s = 0, w = 0)."),
        ("para", ("4 Principiante (50, 0, 0): ", "b"), "Una de cada dos jugadas se juega "
                 "de forma teóricamente perfecta (50 %). Como s = 0 y w = 0, no hay "
                 "ningún filtrado de errores."),
        ("para", ("5 Avanzado (20, 1, 1): ", "b"), "Elige la mejor jugada "
                 "teórica el 20 % de las veces, pero gracias a s = 1 y w = 1 no pasa por alto ni sus propias victorias inmediatas "
                 "ni las amenazas directas del rival en la jugada siguiente."),
        ("para", ("6 Táctico (0, 3, 3): ", "b"), "Nunca juega la mejor jugada teórica "
                 "(p = 0), pero juega con atención táctica: las victorias forzadas en "
                 "hasta 3 jugadas propias se juegan (w = 3) y las derrotas "
                 "amenazantes en las 3 jugadas siguientes del rival se evitan "
                 "(s = 3). Un rival tácticamente duro, sin visión estratégica."),
        ("para", ("7 Intermedio (50, 1, 1): ", "b"), "Nivel aficionado sólido: una de cada dos "
                 "jugadas perfecta (50 %), aprovechamiento fiable de las victorias inmediatas (w = 1) y "
                 "evitación consecuente de los errores inmediatos (s = 1)."),
        ("para", ("8 Exigente (55, 1, 1): ", "b"), "Se basa en el nivel 7, pero juega "
                 "sin ningún fallo en más de la mitad de las jugadas (55 %)."),
        ("para", ("9 Difícil (65, 1, 1): ", "b"), "Con un 65 % de jugadas óptimas y una protección fiable "
                 "contra los errores inmediatos, un rival serio para jugadores de club con experiencia."),
        ("para", ("10 Muy difícil (70, 2, 2): ", "b"), "Combina una gran precisión (70 %) "
                 "con instinto táctico: reconoce y para ataques de hasta "
                 "2 jugadas del rival (s = 2) y convierte con fiabilidad sus propias victorias en 2 jugadas "
                 "(w = 2): un obstáculo para jugadores de torneo."),
        ("para", ("11 Experto (80, 2, 2): ", "b"), "Juega sin fallos el 80 % de las veces y "
                 "para con fiabilidad los ataques de hasta 2 jugadas del rival. Sus propias "
                 "amenazas de victoria en 2 jugadas se convierten con seguridad; la puerta de entrada a las clases de maestros."),
        ("para", ("12 Maestro (85, 3, 3): ", "b"), "Juega muy fuerte (85 % de mejores jugadas) con "
                 "una protección táctica de gran alcance: ve las amenazas y sus propios "
                 "caminos ganadores en 3 jugadas (s = 3, w = 3). Incluso "
                 "los jugadores de torneo con experiencia apenas puntúan ya aquí."),
        ("para", ("13 Maestro fuerte (92, 4, 4): ", "b"), "Casi infalible (92 % de mejores jugadas): "
                 "evita variantes perdedoras forzadas con hasta 4 jugadas de antelación "
                 "(s = 4) y convierte sus propias victorias en 4 jugadas "
                 "con seguridad (w = 4)."),
        ("para", ("14 Perfecto (100, -, -): ", "b"), "Juega sin fallos según las "
                 "leyes del juego resuelto: como primer jugador (Amarillo) el "
                 "motor gana todas las partidas por la fuerza; como segundo jugador (Rojo) aprovecha cada "
                 "imprecisión del rival para llevarse el punto completo. "
                 "Las jugadas equivalentes se varían estadísticamente (véase ",
                 ("Jugadas equivalentes", "b"), " arriba). Para entrenar el propio juego, se recomienda el análisis de posiciones, "
                 "véase ", ("LINK", "Análisis", "wertung"), "."),
        ("para", "Valores orientativos de la fuerza de juego relativa (determinados en "
                 "torneos motor contra motor con un total de 18.200 partidas, "
                 "200 partidas por emparejamiento, con "
                 "cambio de color continuo; base de referencia nivel Aleatorio = 1000 Elo): "
                 "1 Aleatorio, 2 Muy fácil ~1204, 3 Fácil ~1340, "
                 "4 Principiante ~1431, 5 Avanzado ~1498, 6 Táctico ~1614, "
                 "7 Intermedio ~1702, 8 Exigente ~1752, "
                 "9 Difícil ~1817, 10 Muy difícil ~1929, 11 Experto ~2010, "
                 "12 Maestro ~2080, 13 Maestro fuerte ~2132, 14 Perfecto ~2174. "
                 "En partidas contra rivales humanos estas diferencias pueden variar "
                 "por factores psicológicos y tácticos. La tabla de fuerza y la tabla cruzada se ofrecen "
                 "completas en la sección ", ("LINK", "“Fuerza de juego y tabla cruzada”", "elorang"), "."),
        ("head", "elorang", "Fuerza de juego y tabla cruzada"),
        ("para", "Los 91 emparejamientos se jugaron con 200 partidas cada uno y cambio de color "
                 "(18.200 en total). Base de referencia nivel Aleatorio = 1000 Elo "
                 "(relativo, no es Elo FIDE)."),
        ("para", ("Fuerza de juego (Elo):", "b")),
        ("mono",
        " 1 Aleatorio                   1000\n"
        " 2 Muy fácil        (25,0,0)   1204\n"
        " 3 Fácil            (40,0,0)   1340\n"
        " 4 Principiante     (50,0,0)   1431\n"
        " 5 Avanzado         (20,1,1)   1498\n"
        " 6 Táctico          (0,3,3)    1614\n"
        " 7 Intermedio       (50,1,1)   1702\n"
        " 8 Exigente         (55,1,1)   1752\n"
        " 9 Difícil          (65,1,1)   1817\n"
        "10 Muy difícil      (70,2,2)   1929\n"
        "11 Experto          (80,2,2)   2010\n"
        "12 Maestro          (85,3,3)   2080\n"
        "13 Maestro fuerte   (92,4,4)   2132\n"
        "14 Perfecto         (100,-,-)  2174"),
        ("para", ("Tabla cruzada (puntos del nivel de la fila contra el nivel de la columna, sobre 200):", "b")),
        ("table", "kreuz14"),
        ("sub", "zugwahl", "Entre bastidores: la selección de jugada en 3 pasos"),
        ("para", ("Así decide el motor cada jugada (niveles 1–14): ", "b"),
                 "Cada jugada pasa por una cadena de decisión fija de tres pasos. "
                 "Con ella se explica todo el juego conjunto de fuerza de juego, filtros "
                 "y aparentes paradojas:"),
        ("para", ("1. Primero la prioridad de victoria (w), sin dados: ", "b"),
                 "Si la posición ofrece una victoria forzada en ",
                 ("w", "b"), " jugadas propias, esa jugada se hace de inmediato, incluso antes de la decisión aleatoria de ",
                 ("p", "b"), ". ",
                 ("w = 1", "b"), " significa una victoria inmediata. ",
                 ("w = 2", "b"), " significa una victoria en como máximo 2 jugadas. ",
                 ("w = 3", "b"), " significa una victoria en hasta 3 jugadas. ",
                 ("(w = 0 desactiva esta anticipación.)", "b"),
                 " Solo si no hay una victoria corta así, sigue el paso 2."),
        ("para", ("2. El sorteo de p (perfecta o error): ", "b"),
                 "En cada jugada, de forma aislada y sin memoria, la probabilidad ",
                 ("p", "b"), " decide si el motor juega bien o mal. ",
                 "Con ", ("p = 50", "b"), " (Principiante, Intermedio) estadísticamente una de cada dos jugadas es perfecta. ",
                 "Con ", ("p = 20", "b"), " (Avanzado) solo una de cada cinco. ",
                 "Con ", ("p = 80", "b"), " (Experto) cuatro de cada cinco. ",
                 "Las rachas son puramente aleatorias: incluso con ", ("p = 50", "b"),
                 " pueden darse tres errores seguidos, o tres jugadas perfectas seguidas."),
        ("para", ("3a. Sale perfecta: mejor puntuación y regla de las 10 semijugadas: ", "b"),
                 "El motor elige directamente entre las mejores jugadas teóricas: ",
                 "entre varias jugadas ganadoras igual de buenas, se juega la más rápida dentro de "
                 "10 semijugadas; entre varias igual de rápidas, se elige una al azar. ",
                 "Si ninguna victoria queda dentro de 10 semijugadas, se elige al azar entre todas las "
                 "jugadas ganadoras restantes (todas ellas entonces a más de 10 semijugadas). ",
                 "Si solo hay tablas, se elige una de ellas al azar. ",
                 "Si solo hay jugadas perdedoras, se aplica la regla de derrota (máxima resistencia, ponderada, "
                 "con protección de 10 semijugadas en Perfecto)."),
        ("para", ("3b. Sale débil: la rutina de errores: ", "b"),
                 "No es tirar los dados a ciegas, sino una jugada filtrada: ",
                 "el filtro ", ("s", "b"), " bloquea todas las jugadas tras las cuales el rival ganaría en como máximo ",
                 ("s", "b"), " jugadas (", ("s = 1", "b"),
                 " prohíbe los errores inmediatos en la jugada siguiente; ", ("s = 0", "b"),
                 " no filtra nada). ",
                 "Entre todas las jugadas permitidas restantes se elige una ", ("uniformemente al azar", "b"),
                 ": unas tablas no se prefieren aquí, cuentan como cualquier otra jugada admisible. ",
                 ("Casos especiales: ", "b"), ("p = 100", "b"), " (Perfecto) va siempre al 3a. ",
                 ("p = 0", "b"), " (Táctico) va siempre al 3b. ",
                 ("s = 0, w = 0", "b"), " (niveles 1–4) elige en el 3b sin ningún filtro."),
        ("sub", "filterparadox", "La paradoja del filtro: Táctico contra Principiante (149,5 : 50,5)"),
        ("para", "En un duelo directo, el nivel ", ("6 Táctico (0, 3, 3)", "b"),
                 " vence al ", ("4 Principiante (50, 0, 0)", "b"),
                 " con claridad, por casi 3 : 1, aunque el Táctico no juega ni una sola jugada perfecta. ",
                 "La razón está en el juego conjunto de ", ("escudo y espada", "b"), ": ",
                 "gracias a ", ("s = 3", "b"), " el Táctico no regala casi nada con errores rápidos. ",
                 "Y gracias a ", ("w = 3", "b"), " convierte toda victoria disponible en 1 a 3 jugadas. ",
                 "El Principiante, en cambio, malgasta sus ventajas de apertura con errores inmediatos sin filtrar (",
                 ("s = 0", "b"), ") y, al carecer de prioridad de victoria (",
                 ("w = 0", "b"), "), a menudo deja sin castigo los fallos del rival. ",
                 "El mismo principio se observa con el ", ("5 Avanzado (20, 1, 1)", "b"),
                 ", que vence al Principiante por 137 : 63 a pesar de una ", ("p", "b"), " mucho menor."),
        ("sub", "spitzenumkehr", "La inversión en la cima: puntos contra los maestros"),
        ("para", "Contra los rivales más fuertes (Maestro fuerte y Perfecto) la imagen se invierte: ",
                 "aquí, sobre 400 partidas, el Principiante logra ", ("7,0 puntos", "b"),
                 ", mientras que el Táctico solo ", ("0,5 puntos", "b"), " (una catorceava parte). ",
                 "Los rivales fuertes prácticamente nunca cometen errores. De poco sirven ",
                 ("s = 3", "b"), " ni ", ("w = 3", "b"),
                 ", porque el Maestro apenas ofrece un blanco. ",
                 "Para puntuar siquiera contra maestros casi perfectos hacen falta jugadas perfectas "
                 "con un plan estratégico profundo; la protección contra la derrota o la prioridad de victoria de corto alcance no bastan. "
                 "El Principiante juega perfecta una de cada dos jugadas; "
                 "de vez en cuando una de ellas basta para unas tablas. Al Táctico le faltan por completo esas jugadas."),

        ("head", "datei", "Menú Archivo"),
        ("para", ("Nueva partida: ", "b"), "Devuelve el tablero a la posición inicial vacía. ",
                 ("Nueva con posición aleatoria…: ", "b"), "Crea una posición "
                 "de medio juego construida al azar, con 1 a 9 fichas, opcionalmente con un resultado "
                 "teórico garantizado (victoria, tablas o derrota). ",
                 ("Cargar posición… ", "b"), "y ", ("Guardar posición…: ", "b"),
                 "Abren un diálogo de archivos estándar para el formato universal ",
                 (".4gp", "b"), ". Una partida guardada consiste en la "
                 "cadena cronológica de dígitos de las columnas elegidas, como por ejemplo ",
                 ("4433221", "b"), ". ", ("Guardado rápido (F3) ", "b"), "y ",
                 ("Carga rápida (F4): ", "b"), "Guardan o cargan el registro de la partida "
                 "actual directamente en o desde el archivo ",
                 ("quicksave.4gp", "b"), " del directorio principal del programa, sin diálogo intermedio. ",
                 ("Salir: ", "b"), "Cierra ConnectFour Studio correctamente."),

        ("head", "kommandos", "Menú Comandos"),
        ("para", ("Primera / última jugada (Flecha arriba / Flecha abajo): ", "b"),
                 "Salta al principio o al final de la partida; las jugadas deshechas "
                 "permanecen en memoria y se pueden repetir en cualquier momento. ",
                 ("Jugada atrás / adelante: ", "b"), "Recorre la partida paso a paso "
                 "(como los botones ", ("<", "b"), " y ", (">", "b"), "). ",
                 ("Jugar (ordenador): ", "b"), "Equivale al atajo ", ("F5", "b"), ". ",
                 ("Evaluar todas las jugadas (1x): ", "b"), "Equivale a ", ("F6", "b"), " (véase ",
                 ("LINK", "fila de evaluación", "wertung"), "). ",
                 ("Análisis permanente: ", "b"), "Equivale a ", ("F7", "b"), " (véase ",
                 ("LINK", "menú Ver", "ansicht"), ")."),

        ("head", "ansicht", "Menú Ver"),
        ("para", ("Ficha fantasma: ", "b"), "Activa o desactiva la vista previa semitransparente de la caída. ",
                 ("Animación de caída: ", "b"), "Controla el movimiento fluido de caída de las fichas. ",
                 ("Mostrar última jugada: ", "b"), "Activa o desactiva el anillo de marca blanco "
                 "sobre la ficha más reciente. ",
                 ("Marcador sí/no ", "b"), "y ",
                 ("Reiniciar marcador: ", "b"), "Se corresponden con los botones del ",
                 ("LINK", "área del marcador", "spielstand"), ". La ventana de ayuda se puede abrir "
                 "en cualquier momento desde el menú o con ", ("F1", "b"), "."),

        ("head", "info", "Cuadro de información, turno y barra de estado"),
        ("para", "Arriba a la derecha, el cuadro ", ("Turno", "b"),
                 " muestra, mediante el símbolo de la ficha y el nombre, a quién le toca: ",
                 ("Humano", "b"), " o el motor, indicando el nivel activo "
                 "(por ejemplo “User (1) (70,1,1)”). En el modo de dos jugadores, "
                 "aquí siempre se muestra Humano."),
        ("para", "Justo debajo, el ", ("cuadro de información", "b"),
                 " ofrece datos clave sobre la situación actual del tablero:"),
        ("para", ("Jugada: ", "b"), "Número correlativo de la siguiente semijugada (empezando en 1)."),
        ("para", ("Nivel: ", "b"), "",
                 ("LINK", "Nivel", "stufen"),
                 " activo del motor (en el modo de torneo, el nivel del color al que le toca)."),
        ("para", ("Profundidad: ", "b"), "Última profundidad de búsqueda alcanzada, en semijugadas. ",
                 ("Completa: ", "b"), "Cálculo completo hasta el final de la partida. ",
                 ("Libro 12d: ", "b"), "Hasta 12 fichas la búsqueda termina en cuanto cada variante alcanza el libro de aperturas; los valores son exactos. ", ("Libro 2d: ", "b"), "Posición con dos fichas como máximo: valores exactos del minilibro integrado, sin ninguna búsqueda. "
                 "Unos puntos suspensivos al final (p. ej. “8...”) indican una profundización que "
                 "aún está en curso. Un guion (–) significa que todavía no hay ningún cálculo."),
        ("para", ("Valor: ", "b"), "Evaluación teórica de la última jugada en "
                 "notación compacta, por ejemplo “Amarillo (31)”, “Rojo (28)” o "
                 "“Tablas (40)”. La etiqueta nombra al bando ganador con juego óptimo "
                 "de ambos bandos. El número entre paréntesis es el número "
                 "de fichas que aún quedan por colocar hasta la decisión final: los números pequeños "
                 "(1–6) indican una decisión inminente; un ",
                 ("1", "b"), " entre paréntesis marca la victoria inmediata directa en la siguiente jugada. "
                 "Los valores altos (30–42) indican un final largo (42 sería "
                 "unas tablas desde la posición vacía). Con cada jugada realizada, este "
                 "valor baja en 1. El número de distancia bajo el símbolo de la ",
                 ("LINK", "fila de evaluación", "wertung"), " tras un análisis (",
                 ("F6", "b"), "/", ("F7", "b"),
                 ") muestra el mismo recuento de fichas por columna. "
                 "Antes del primer análisis aparece un guion (–). Cuando la partida termina, aquí se anuncia el "
                 "resultado final, por ejemplo “¡Gana el Amarillo!”."),
        ("para", ("Nodos: ", "b"), "Número de posiciones exploradas en el árbol de búsqueda "
                 "(información en tiempo real del núcleo C++, con separadores de millares legibles). ",
                 ("Tiempo: ", "b"), "Duración pura del cálculo del último análisis, en milisegundos. ",
                 ("Velocidad: ", "b"), "Velocidad de búsqueda en nodos por segundo "
                 "(por ejemplo 2,3 M/s = 2,3 millones de posiciones/s). Todos los valores "
                 "se refieren al paso de cálculo más reciente."),
        ("para", ("Fuente: ", "b"), "Origen de los datos de la posición: ",
                 ("Libro 12d", "b"), " = consulta del libro de aperturas integrado (hasta "
                 "una profundidad de 12 fichas), ", ("calculado", "b"), " = cálculo libre "
                 "en tiempo real del motor. Un guion (–) indica "
                 "el estado inicial antes de que empiece la búsqueda."),
        ("para", "La ", ("barra de estado", "b"), " del borde inferior de la ventana informa de "
                 "las jugadas realizadas (p. ej. “El ordenador jugó 4 en 0,35 s”), de los informes de análisis "
                 "y de las operaciones con archivos. Mientras hay un cálculo en curso, "
                 "muestra “El ordenador aún está pensando – espere, por favor.” Un intento de carga durante la "
                 "búsqueda se rechaza con el mensaje “El ordenador aún está pensando – deténgalo primero y luego cargue.” "
                 "En ese caso hay que interrumpir primero el cálculo con "
                 "la función de detener."),

        ("head", "einstellungen", "Menú Configuración"),
        ("para", "El menú ", ("Configuración", "b"), " reúne las opciones principales: ",
                 ("Nivel del ordenador", "b"), " (fija la fuerza de juego del nivel ",
                 ("LINK", "0 al 14", "stufen"), "; también se puede cambiar durante una "
                 "partida en curso; el ", ("LINK", "marcador", "spielstand"),
                 " vuelve a empezar en 0–0 tras un cambio), ",
                 ("Humano-Ordenador", "b"), " (una partida contra la inteligencia artificial), ",
                 ("2 jugadores (ambos humanos)", "b"), " (dos personas juegan una contra otra; "
                 "el programa asume la función de árbitro y la visualización), ",
                 ("Ordenador-Ordenador (jugar hasta el final)", "b"), " (el motor juega ambos "
                 "bandos desde la posición actual, véase ",
                 ("LINK", "modos de juego", "gegner"), "), ",
                 ("Partido Ordenador-Ordenador", "b"), " (configura partidas automáticas "
                 "y torneos, véase ", ("LINK", "modos de juego", "gegner"), "), ",
                 ("Detener juego automático", "b"), " (detiene de inmediato un partido en curso; "
                 "el resultado parcial se conserva) y ",
                 ("Juego de fichas", "b"), " (selección entre 20 diseños de tablero y fichas; "
                 "también se pueden recorrer con la rueda del ratón sobre el "
                 "tablero o con las teclas Re Pág / Av Pág)."),

        ("head", "sprache", "Elegir el idioma"),
        ("para", "En el menú ", ("Ayuda", "b"), " bajo ", ("Idioma", "b"), " figuran los "
                 "idiomas disponibles: ", ("Deutsch", "b"), ", ", ("English", "b"), ", ",
                 ("Français", "b"), ", ", ("Español", "b"), ", ", ("Nederlands", "b"), " e ",
                 ("Italiano", "b"), ". "
                 "La selección (un botón de opción) surte efecto de inmediato en la Ayuda y la Información."),

        ("head", "engine", "Motor y libro de aperturas"),
        ("para", "El núcleo de cálculo matemático es ",
                 ("BitBully by Markus Thill", "b"), ", un módulo de Python eficiente "
                 "con núcleo en C++. Utiliza bitboards optimizados, "
                 "profundización iterativa con un algoritmo de búsqueda MTD(f)/null-window "
                 "y tablas de transposición dinámicas. El libro de aperturas integrado ",
                 ("12-ply-dist", "b"), " proporciona evaluaciones teóricas y valores exactos de "
                 "distancia para todas las posiciones con hasta 12 fichas colocadas; "
                 "en variantes más profundas el motor de búsqueda continúa el cálculo."),
        ("para", "ConnectFour Studio combina una interfaz de escritorio ligera (Python, Tkinter, "
                 "renderizado gráfico con Pillow) con un juego resuelto. "
                 "Se distribuye como software libre bajo la ",
                 ("GNU Affero General Public License (AGPL v3)", "b"), "."),

        ("head", "tasten", "Atajos de teclado"),
        ("para", ("1–7", "b"), " = hacer una jugada en una columna · ",
                 ("Flecha izquierda / Flecha derecha", "b"), " = deshacer / repetir una jugada · ",
                 ("Flecha arriba / Flecha abajo", "b"), " = saltar al principio / al final de la partida · ",
                 ("Re Pág / Av Pág o rueda del ratón sobre el tablero", "b"), " = cambiar el juego de fichas · ",
                 ("F1", "b"), " = abrir el diálogo de ayuda · ",
                 ("F3 / F4", "b"), " = guardado / carga rápidos · ",
                 ("F5", "b"), " = que el motor juegue · ",
                 ("F6", "b"), " = análisis único de la posición · ",
                 ("F7", "b"), " = activar o desactivar el ", ("LINK", "análisis permanente", "buttons"), " · ",
                 ("Escape", "b"), " = cerrar un menú abierto. "
                 "Nota: los atajos funcionan mientras el foco de entrada no esté en un "
                 "campo de texto."),
    ],
    "fr": [
        ("head", "inhalt", "Sommaire"),
        ("para", ("LINK", "Le jeu", "spiel"), " · ",
                 ("LINK", "Saisir les coups", "ziehen"), " · ",
                 ("LINK", "Les boutons sous le plateau", "buttons"), " · ",
                 ("LINK", "L'évaluation (+, =, –)", "wertung"), " · ",
                 ("LINK", "Score (humain contre moteur)", "spielstand"), " · ",
                 ("LINK", "Modes de jeu", "gegner"), " · ",
                 ("LINK", "Niveaux personnalisés : User (1) et User (2)", "userstufen"), " · ",
                 ("LINK", "Les niveaux", "stufen"), " · ",
                 ("LINK", "Force de jeu et tableau croisé", "elorang"), " · ",
                 ("LINK", "Menu Fichier", "datei"), " · ",
                 ("LINK", "Menu Commandes", "kommandos"), " · ",
                 ("LINK", "Menu Affichage", "ansicht"), " · ",
                 ("LINK", "Zone d'informations, trait et barre d'état", "info"), " · ",
                 ("LINK", "Menu Paramètres", "einstellungen"), " · ",
                 ("LINK", "Choisir la langue", "sprache"), " · ",
                 ("LINK", "Moteur et livre d'ouvertures", "engine"), " · ",
                 ("LINK", "Raccourcis clavier", "tasten"), "."),

        ("head", "spiel", "Le jeu"),
        ("para", "ConnectFour Studio est une application libre pour « Puissance quatre » "
                 "avec 15 niveaux, 20 designs de plateau au choix, un mode tournoi, "
                 "des statistiques de match détaillées et une analyse exacte en temps réel."),
        ("para", "Les règles de base de « Puissance quatre » sont simples : le Jaune (joueur 1) "
                 "commence toujours la partie. Gagne le camp qui réussit le premier à aligner "
                 "quatre de ses pions sans interruption, à l'horizontale, "
                 "à la verticale ou en diagonale. Si les 42 cases de la grille sont remplies "
                 "sans alignement de quatre, la partie se termine par une ", ("partie nulle", "b"),
                 ". Un alignement gagnant complété est ", ("surligné en vert", "b"),
                 " sur le plateau."),
        ("para", "Les coups peuvent être joués de trois façons : par un ",
                 ("LINK", "clic de souris", "ziehen"), ", avec les ",
                 ("LINK", "touches numériques 1–7", "ziehen"), " ou avec le bouton ",
                 ("Jouer (F5)", "b"), ". La section ",
                 ("LINK", "« Saisir les coups »", "ziehen"), " en donne un aperçu détaillé."),

        ("head", "ziehen", "Saisir les coups"),
        ("para", ("Saisie à la souris : ", "b"), "Un clic dans la colonne souhaitée y fait tomber "
                 "un pion. Lorsque le pointeur passe sur le plateau, un ",
                 ("pion fantôme", "b"), " semi-transparent montre où il atterrira. "
                 "Cet aperçu peut être désactivé à tout moment dans le menu ",
                 ("LINK", "Affichage", "ansicht"), "."),
        ("para", ("Commande au clavier : ", "b"), "Les touches numériques ",
                 ("1 à 7", "b"), " font tomber un pion directement dans la colonne "
                 "correspondante. Les touches ", ("Flèche gauche / Flèche droite", "b"),
                 " annulent le dernier coup ou le rejouent. ", ("Flèche haut / Flèche bas", "b"),
                 " sautent directement au début ou à la fin de la partie. Les mêmes "
                 "actions sont disponibles avec les boutons ", ("<", "b"), ", ",
                 (">", "b"), ", ", ("<<", "b"), " et ", (">>", "b"), ". "
                 "La touche ", ("F5", "b"), " fait calculer au ",
                 ("LINK", "moteur", "engine"), " le prochain coup du camp "
                 "au trait, même sur un plateau vide ; dans ce cas l'ordinateur "
                 "ouvre la partie (voir ",
                 ("LINK", "boutons sous le plateau", "buttons"), ")."),
        ("para", ("Ligne d'évaluation : ", "b"), "Un clic de souris sur l'une des sept "
                 "cases situées sous le plateau joue aussi le coup dans la "
                 "colonne correspondante (voir ", ("LINK", "ligne d'évaluation", "wertung"), ")."),
        ("para", "Le dernier coup joué est marqué par un ",
                 ("anneau blanc", "b"), " (désactivable sous ",
                 ("LINK", "Affichage", "ansicht"), ")."),

        ("head", "buttons", "Les boutons sous le plateau"),
        ("para", ("Nouvelle : ", "b"), "Réinitialise le plateau et commence une nouvelle "
                 "partie depuis la position de départ (voir aussi ",
                 ("LINK", "menu Fichier", "datei"), ")."),
        ("para", ("<< et >> : ", "b"), "Sautent directement au début de la partie "
                 "ou à la fin actuelle de la partie."),
        ("para", ("< et > : ", "b"), "Annulent des coups ou les rétablissent pas à pas, "
                 "afin de pouvoir reconstituer n'importe quelle suite de coups."),
        ("para", ("Jouer (F5) : ", "b"), "Confie le coup au ",
                 ("LINK", "moteur", "engine"), ", qui joue selon le ",
                 ("LINK", "niveau", "stufen"), " actuellement sélectionné."),
        ("para", ("Analyser (F7) : ", "b"), "Active ou met en pause l'",
                 ("analyse permanente", "b"), ". Lorsqu'elle est activée, chaque "
                 "position est entièrement calculée en arrière-plan juste après "
                 "un coup. Lorsqu'elle est désactivée, la barre située sous le plateau "
                 "n'affiche que les numéros de colonne neutres ", ("1–7", "b"), " (voir ",
                 ("LINK", "ligne d'évaluation", "wertung"), ")."),
        ("para", "D'autres fonctions spéciales sont disponibles dans la barre de menus : ",
                 ("Fichier > Nouvelle avec position aléatoire…", "b"), " crée une "
                 "position équilibrée de 1 à 9 pions, éventuellement avec un "
                 "résultat donné (voir ", ("LINK", "menu Fichier", "datei"), ") ; la commande ",
                 ("Commandes > Évaluer tous les coups (1x)", "b"), " (", ("F6", "b"),
                 ") lance une évaluation unique des sept colonnes (voir ",
                 ("LINK", "ligne d'évaluation", "wertung"), ")."),

        ("head", "wertung", "L'évaluation (+, =, –)"),
        ("para", "Pour chaque colonne disponible, la ligne d'évaluation située sous le plateau affiche "
                 "en haut un résultat symbolique et, dessous, le nombre de pions qui "
                 "restent à poser jusqu'à la fin de la partie avec un jeu parfait des deux "
                 "camps : ",
                 ("+ (vert)", "b"), " = victoire forcée, ",
                 ("= (jaune)", "b"), " = nulle assurée, ",
                 ("- (rouge)", "b"), " = défaite inévitable. ",
                 ("Les colonnes entièrement remplies sont marquées d'un « X ».", "b")),
        ("para", "Si aucune évaluation n'est active, seuls les numéros de colonne ",
                 ("1–7", "b"), " sont affichés. La ", ("LINK", "zone d'informations", "info"),
                 " au bord droit de la fenêtre indique en outre la meilleure suite "
                 "en clair, par exemple ", ("« Col. 4 : le Jaune gagne »", "b"), "."),
        ("para", "L'évaluation de la position est toujours ", ("mathématiquement parfaite", "b"),
                 " (recherche complète avec le livre 12-ply-dist), indépendamment du ",
                 ("LINK", "niveau", "stufen"), " sélectionné. Seuls les coups réellement joués par le ",
                 ("LINK", "moteur", "engine"), " sont volontairement imparfaits aux "
                 "niveaux bas. Le nombre de distance indique le nombre exact de pions "
                 "qui restent à poser jusqu'à la décision : "
                 "une petite valeur annonce une fin de partie rapide, un grand nombre "
                 "une fin longue et difficile."),

        ("head", "spielstand", "Score (humain contre moteur)"),
        ("para", "L'affichage du ", ("Score", "b"), ", en bas à droite sous la ",
                 ("LINK", "zone d'informations", "info"), ", enregistre le bilan courant de la session "
                 "dans le duel humain contre ordinateur. En gros caractères il montre le "
                 "score ", ("Humain – Moteur", "b"), " (par exemple ", ("2–1", "b"),
                 "), complété par la statistique détaillée ",
                 ("(+victoires / =nulles / –défaites)", "b"), " du point de "
                 "vue du joueur humain et par le nombre total de parties jouées. Une "
                 "différence Elo estimée s'affiche dès que les deux camps ont obtenu "
                 "au moins un demi-point."),
        ("para", "Une statistique distincte est tenue pour chaque ", ("niveau de l'adversaire", "b"),
                 ". Lorsque le niveau change (via ",
                 ("LINK", "Paramètres", "einstellungen"), "), le décompte repart "
                 "à 0–0 avec le nouvel adversaire ; le bilan précédent "
                 "est effacé. Seules les parties terminées normalement comptent : "
                 "celui qui pose le pion gagnant reçoit le point entier. "
                 "En cas de nulle, chaque camp reçoit un demi-point. Les parties interrompues "
                 "(par exemple via ", ("Nouvelle", "b"),
                 " ou ", ("Arrêter le jeu automatique", "b"), ") ne comptent pas."),
        ("para", ("Oui/Non : ", "b"), "Masque ou affiche l'affichage numérique ; "
                 "le cadre qui l'entoure reste. Lorsque l'affichage est désactivé, "
                 "la saisie des points est suspendue. ", ("Réinit. : ", "b"), "Remet "
                 "le score du niveau actuel à 0–0. Les deux "
                 "fonctions sont aussi disponibles dans le menu ", ("LINK", "Affichage", "ansicht"),
                 " (", ("Score activé/désactivé", "b"), ", ", ("Réinitialiser le score", "b"),
                 "). Par défaut, l'enregistrement est désactivé ; le décompte "
                 "ne commence qu'une fois l'affichage activé."),

        ("head", "gegner", "Modes de jeu"),
        ("para", "Le menu ", ("Paramètres", "b"), " définit le "
                 "mode de jeu de base : ", ("Humain-Ordinateur", "b"), " (avec un ",
                 ("LINK", "niveau d'adversaire", "stufen"), " librement choisi) ou ",
                 ("2 joueurs (deux humains)", "b"), ". En mode deux joueurs, "
                 "ConnectFour Studio sert de plateau virtuel avec fonction d'arbitre "
                 "et d'", ("LINK", "analyse permanente", "buttons"),
                 " en option : un bon outil pour analyser et s'entraîner ensemble."),
        ("para", ("Ordinateur-Ordinateur (jouer jusqu'au bout) : ", "b"), "Fait terminer par le moteur "
                 "la position actuelle en jouant contre lui-même, toujours au "
                 "niveau le plus élevé, ", ("Parfait", "b"), ", quels que soient les autres "
                 "réglages. La fonction peut être rappelée à tout moment "
                 "et reprend alors à partir de la position actuelle du plateau."),
        ("para", ("Match Ordinateur-Ordinateur : ", "b"), "Lance une série de parties "
                 "automatiques. On peut régler le ", ("nombre de parties", "b"), " (de 1 à 10 000), "
                 "les types de joueur pour les deux couleurs (", ("Humain", "b"), ", un ",
                 ("LINK", "niveau fixe", "stufen"), " ou un ",
                 ("LINK", "niveau personnalisé User (1)/(2)", "userstufen"), "), le ",
                 ("changement de couleur", "b"), " après chaque partie (le Jaune et le Rouge échangent "
                 "leurs rôles) ainsi que la ", ("vitesse", "b"), " (Normal / Rapide / Résultats seulement). "
                 "Si un humain participe au match (un camp est réglé sur ",
                 ("Humain", "b"), ") et que la ", ("vitesse", "b"), " est sur ",
                 ("Normal", "b"), ", le programme fait une pause de 3 secondes "
                 "à la fin d'une partie afin de pouvoir examiner le résultat. ",
                 ("Démarrer", "b"), " lance la série, ", ("Arrêter", "b"), " (aussi "
                 "via l'élément de menu ", ("Arrêter le jeu automatique", "b"), ") l'interrompt ; le "
                 "résultat intermédiaire est conservé. Lorsque le match est terminé, "
                 "la fenêtre de dialogue passe automatiquement au premier plan ; le "
                 "bouton ", ("Copier", "b"), " copie le rapport de résultats "
                 "complet (points, bilan victoires et nulles et évaluation Elo) dans le "
                 "presse-papiers."),

        ("head", "userstufen", "Niveaux personnalisés : User (1) et User (2)"),
        ("para", "Dans la boîte de configuration du ",
                 ("LINK", "match Ordinateur-Ordinateur", "gegner"), ", deux profils librement "
                 "configurables sont disponibles en plus des niveaux intégrés : ",
                 ("User (1) (p,s,w personnalisés)", "b"), " et ",
                 ("User (2) (p,s,w personnalisés)", "b"), ". Dès qu'un tel profil "
                 "est choisi pour le Jaune ou le Rouge, le "
                 "champ de saisie correspondant est activé (le champ 1 commande User 1, le champ 2 commande "
                 "User 2). On peut y régler individuellement les trois paramètres de comportement ",
                 ("p, s et w", "b"), " (pour leur fonctionnement exact, voir ",
                 ("LINK", "Les niveaux", "stufen"), "). Comme les deux profils sont indépendants, "
                 "des duels entre deux styles de jeu personnalisés sont aussi possibles."),
        ("para", ("p = part de coups parfaits en pourcentage", "b"),
                 " (plage de 0 à 100) : Le taux d'erreurs se calcule ainsi : ",
                 ("100 – p", "b"), ". Une valeur de ", ("p = 100", "b"), " (comme pour le niveau ",
                 ("14 Parfait", "b"), ") garantit un jeu sans faille à chaque coup. "
                 "La valeur extrême ", ("p = 0", "b"), " (comme pour le niveau ", ("6 Tacticien", "b"),
                 " ou dans les profils User personnalisés) signifie un ",
                 ("taux d'erreurs de 100 %", "b"), " : ici le meilleur coup théorique n'est jamais "
                 "choisi, c'est toujours la routine d'erreur qui s'exécute. Ce n'est pas "
                 "du pur hasard (comme au niveau 1), car les paramètres s et w "
                 "pilotent le comportement de jeu : le niveau 6 Tacticien montre à quel point un "
                 "profil (0, 3, 3) joue bien grâce à la seule protection tactique. "
                 "Avec des valeurs intermédiaires comme ", ("p = 50", "b"), " (par exemple le niveau 4 "
                 "Débutant ou le niveau 7 Intermédiaire), statistiquement un coup sur deux est "
                 "parfait, tandis que les 50 % restants vont dans la branche d'erreur."),
        ("para", ("Séquence de décision par coup : ", "b"), "Une courte victoire forcée ",
                 ("(w)", "b"), " a toujours la priorité, même avant la décision aléatoire de p. "
                 "S'il n'y a pas une telle victoire courte, le ", ("tirage de p", "b"),
                 " décide : si le choix est ", ("« parfait »", "b"), ", le ",
                 ("filtre s", "b"), " ne joue aucun rôle : le moteur choisit directement parmi "
                 "les meilleurs coups théoriques (les égalités sont départagées par la règle des 10 demi-coups). "
                 "Si la décision tombe en revanche sur ", ("« erreur »", "b"), ", la "
                 "chaîne de filtres s'applique : d'abord ", ("w", "b"), " (priorité de victoire), puis le filtre de défaite ",
                 ("s", "b"), " et enfin seulement un choix uniformément réparti parmi tous les "
                 "coups admissibles restants. Une nulle face à une défaite menaçante "
                 "n'est ici ni forcée ni préférée : elle compte comme tout autre coup autorisé."),
        ("para", ("s = protection contre la défaite en coups de l'adversaire", "b"), " (plage de 0 à 9) : "
                 "Ce filtre n'agit que dans la branche d'erreur : un coup plus faible "
                 "est jugé inadmissible si l'adversaire pouvait alors forcer la victoire "
                 "en au plus s de ses coups. ", ("s = 0", "b"),
                 " signifie aucun filtre : les erreurs immédiates sont acceptées "
                 "(comme aux niveaux 1–4, où en cas d'erreur chaque coup légal "
                 "est également probable). ", ("s = 1", "b"), " bloque les coups "
                 "qui offriraient la victoire à l'adversaire dès le coup suivant ; ",
                 ("s = 2, 3 ou 4", "b"), " étendent cette protection à 2, 3 "
                 "ou 4 coups de l'adversaire. Les victoires et les lignes de nulle sont "
                 "toujours autorisées dans la branche d'erreur."),
        ("para", ("w = priorité de victoire", "b"), " (plage de 0 à 9) : Les victoires forcées "
                 "courtes passent toujours en premier, même avant la décision aléatoire de p : si le "
                 "moteur repère un chemin gagnant dont la distance est d'au plus w coups, "
                 "cette victoire est jouée. ", ("w = 1", "b"), " assure la "
                 "victoire immédiate au coup suivant, ", ("w = 2", "b"), " garantit la "
                 "victoire en au plus 2 de ses propres coups ; ", ("w = 3", "b"), " et ",
                 ("w = 4", "b"), " fonctionnent de manière analogue (pour le contexte, voir ",
                 ("LINK", "Les niveaux", "stufen"), "). S'il n'y a pas de victoire aussi proche, la "
                 "décision normale de p s'applique. ",
                 ("w = 0", "b"), " désactive cette anticipation (dans la branche parfaite, les victoires "
                 "sont bien sûr toujours exploitées via l'évaluation normale)."),
        ("para", ("Égalités (coups parfaits, tous les niveaux) : ", "b"),
                 "Si plusieurs coups également bons ont le meilleur score, "
                 "un générateur aléatoire en choisit un, afin d'éviter des répétitions stéréotypées de parties. "
                 "Si des coups mènent à la victoire en moins de 10 demi-coups, le chemin "
                 "gagnant le plus rapide est choisi ; parmi plusieurs aussi rapides, l'un est tiré au hasard. "
                 "Si aucune victoire n'est aussi proche, on tire parmi tous les coups gagnants. "
                 "S'il n'y a que des lignes de nulle, l'une d'elles est tirée au hasard. "
                 "Dans des positions purement perdantes, le niveau ", ("14 Parfait", "b"),
                 " évite les défaites en moins de 10 demi-coups ; s'il existe des coups perdants plus lents, "
                 "l'un d'eux est choisi. Si tous les coups perdants sont "
                 "à plus de 10 demi-coups, on tire au hasard parmi tous les coups perdants pour varier."),
        ("para", "Exemples comparatifs pour s'orienter : le niveau ",
                 ("Débutant (50, 0, 0)", "b"), " joue un coup sur deux faiblement et "
                 "sans aucune protection ; le niveau ", ("Intermédiaire (50, 1, 1)", "b"),
                 " joue aussi un coup sur deux faiblement, mais évite les "
                 "erreurs immédiates élémentaires au coup suivant et exploite systématiquement "
                 "les victoires immédiates directes. Les paramètres configurés figurent dans les rapports du ",
                 ("match Ordinateur-Ordinateur", "b"), " "
                 "(par exemple sous la forme ", ("« User (1) (70, 1, 1) »", "b"), ")."),

        ("head", "stufen", "Les niveaux"),
        ("para", "Les niveaux réguliers sont décrits par les paramètres ",
                 ("(p, s, w)", "b"), " (le niveau 0 perd volontairement, "
                 "le niveau 1 joue au pur hasard, le niveau 14 joue sans faille) : ",
                 ("p", "b"), " est le pourcentage de coups parfaits, ",
                 ("s", "b"), " définit la protection contre la défaite en coups de l'adversaire "
                 "(évite les coups fautifs qui mènent à la défaite en s coups de l'adversaire), "
                 "et ", ("w", "b"), " désigne la priorité de victoire (les victoires forcées "
                 "en w coups propres sont toujours jouées). "
                 "Le chiffre de distance sous le symbole dans la ",
                 ("LINK", "ligne d'évaluation", "wertung"), " indique le nombre "
                 "de pions qui restent à poser jusqu'à la fin de la partie : 1 correspond au pion "
                 "gagnant immédiat, les petites valeurs marquent des fins courtes, les grandes des fins longues "
                 "(explications complémentaires dans la section ",
                 ("LINK", "Zone d'informations", "info"), ")."),
        ("para", ("0 Perdant (niveau amusant) : ", "b"), "Joue volontairement mal "
                 "et choisit de préférence des coups perdants au hasard. Si aucun coup perdant "
                 "n'est disponible, le programme se rabat sur une nulle ou sur un "
                 "coup aléatoire. Un niveau purement amusant, sans classement dans le système Elo."),
        ("para", ("1 Aléatoire : ", "b"), "Joue au pur hasard : chaque coup légal a "
                 "exactement la même probabilité. Ce niveau n'a aucune "
                 "logique (p, s, w), aucune évaluation de position et aucun filtre : le "
                 "choix se fait de façon totalement uniforme parmi toutes les colonnes ouvertes."),
        ("para", ("2 Très facile (25, 0, 0) : ", "b"), "Joue de façon optimale 25 % du temps et "
                 "au pur hasard 75 % du temps ; commet de graves erreurs : idéal pour les débutants "
                 "et les enfants."),
        ("para", ("3 Facile (40, 0, 0) : ", "b"), "Joue de façon optimale 40 % du temps, mais "
                 "renonce aux protections tactiques (s = 0, w = 0)."),
        ("para", ("4 Débutant (50, 0, 0) : ", "b"), "Un coup sur deux est joué "
                 "de façon théoriquement parfaite (50 %). Comme s = 0 et w = 0, il n'y a "
                 "aucun filtrage des erreurs."),
        ("para", ("5 Avancé (20, 1, 1) : ", "b"), "Choisit le meilleur coup "
                 "théorique 20 % du temps, mais grâce à s = 1 et w = 1 ne laisse passer ni ses propres victoires immédiates "
                 "ni les menaces directes de l'adversaire au coup suivant."),
        ("para", ("6 Tacticien (0, 3, 3) : ", "b"), "Ne joue jamais le meilleur coup théorique "
                 "(p = 0), mais joue avec vigilance tactique : les victoires forcées en "
                 "jusqu'à 3 coups propres sont jouées (w = 3) et les défaites "
                 "menaçantes dans les 3 coups suivants de l'adversaire sont écartées "
                 "(s = 3). Un adversaire tactiquement coriace, sans vision stratégique."),
        ("para", ("7 Intermédiaire (50, 1, 1) : ", "b"), "Niveau amateur solide : un coup sur deux "
                 "parfait (50 %), exploitation fiable des victoires immédiates (w = 1) et "
                 "évitement systématique des erreurs immédiates (s = 1)."),
        ("para", ("8 Exigeant (55, 1, 1) : ", "b"), "S'appuie sur le niveau 7, mais joue "
                 "sans aucune faille dans plus de la moitié des coups (55 %)."),
        ("para", ("9 Difficile (65, 1, 1) : ", "b"), "Avec 65 % de coups optimaux et une protection fiable "
                 "contre les erreurs immédiates, un adversaire sérieux pour des joueurs de club expérimentés."),
        ("para", ("10 Très difficile (70, 2, 2) : ", "b"), "Allie une grande précision (70 %) "
                 "à un instinct tactique : reconnaît et pare les attaques sur "
                 "2 coups de l'adversaire (s = 2) et convertit fiablement ses propres victoires en 2 coups "
                 "(w = 2) – un obstacle pour les joueurs de tournoi."),
        ("para", ("11 Expert (80, 2, 2) : ", "b"), "Joue sans faille 80 % du temps et "
                 "pare fiablement les attaques sur 2 coups de l'adversaire. Ses propres "
                 "menaces de victoire en 2 coups sont converties avec sûreté ; la porte d'entrée vers les classes de maîtres."),
        ("para", ("12 Maître (85, 3, 3) : ", "b"), "Joue très fort (85 % de meilleurs coups) avec "
                 "une protection tactique de grande portée : voit les menaces et ses propres "
                 "chemins gagnants sur 3 coups (s = 3, w = 3). Même "
                 "des joueurs de tournoi expérimentés ne marquent presque plus ici."),
        ("para", ("13 Maître supérieur (92, 4, 4) : ", "b"), "Presque infaillible (92 % de meilleurs coups) : "
                 "évite les variantes perdantes forcées jusqu'à 4 coups à l'avance "
                 "(s = 4) et convertit ses propres victoires sur 4 coups "
                 "avec sûreté (w = 4)."),
        ("para", ("14 Parfait (100, -, -) : ", "b"), "Joue sans faille selon les "
                 "lois du jeu résolu : en tant que premier joueur (Jaune) le "
                 "moteur gagne chaque partie de force ; en tant que second joueur (Rouge) il exploite chaque "
                 "imprécision de l'adversaire pour prendre le point entier. "
                 "Les coups équivalents sont variés statistiquement (voir ",
                 ("Égalités", "b"), " ci-dessus). Pour travailler son propre jeu, l'analyse de position "
                 "est recommandée, voir ", ("LINK", "Analyse", "wertung"), "."),
        ("para", "Valeurs indicatives de la force de jeu relative (déterminées lors de "
                 "tournois moteur contre moteur totalisant 18 200 parties, "
                 "200 parties par appariement, avec "
                 "changement de couleur continu ; base de référence niveau Aléatoire = 1000 Elo) : "
                 "1 Aléatoire, 2 Très facile ~1204, 3 Facile ~1340, "
                 "4 Débutant ~1431, 5 Avancé ~1498, 6 Tacticien ~1614, "
                 "7 Intermédiaire ~1702, 8 Exigeant ~1752, "
                 "9 Difficile ~1817, 10 Très difficile ~1929, 11 Expert ~2010, "
                 "12 Maître ~2080, 13 Maître supérieur ~2132, 14 Parfait ~2174. "
                 "Dans les parties contre des adversaires humains, ces écarts peuvent varier "
                 "sur le plan psychologique et tactique. Le tableau de force et le tableau croisé figurent "
                 "en entier dans la section ", ("LINK", "« Force de jeu et tableau croisé »", "elorang"), "."),
        ("head", "elorang", "Force de jeu et tableau croisé"),
        ("para", "Les 91 appariements ont été joués à raison de 200 parties chacun, avec changement de couleur "
                 "(18 200 au total). Base de référence niveau Aléatoire = 1000 Elo "
                 "(relatif, pas un Elo FIDE)."),
        ("para", ("Force de jeu (Elo) :", "b")),
        ("mono",
        " 1 Aléatoire                   1000\n"
        " 2 Très facile      (25,0,0)   1204\n"
        " 3 Facile           (40,0,0)   1340\n"
        " 4 Débutant         (50,0,0)   1431\n"
        " 5 Avancé           (20,1,1)   1498\n"
        " 6 Tacticien        (0,3,3)    1614\n"
        " 7 Intermédiaire    (50,1,1)   1702\n"
        " 8 Exigeant         (55,1,1)   1752\n"
        " 9 Difficile        (65,1,1)   1817\n"
        "10 Très difficile   (70,2,2)   1929\n"
        "11 Expert           (80,2,2)   2010\n"
        "12 Maître           (85,3,3)   2080\n"
        "13 Maître supérieur (92,4,4)   2132\n"
        "14 Parfait          (100,-,-)  2174"),
        ("para", ("Tableau croisé (points du niveau de la ligne contre le niveau de la colonne, sur 200) :", "b")),
        ("table", "kreuz14"),
        ("sub", "zugwahl", "Dans les coulisses : le choix du coup en 3 étapes"),
        ("para", ("Voici comment le moteur décide chaque coup (niveaux 1–14) : ", "b"),
                 "Chaque coup passe par une chaîne de décision fixe en trois étapes. "
                 "Elle explique tout le jeu d'ensemble entre force de jeu, filtres "
                 "et paradoxes apparents :"),
        ("para", ("1. D'abord la priorité de victoire (w), sans dés : ", "b"),
                 "Si la position offre une victoire forcée en ",
                 ("w", "b"), " coups propres, ce coup est joué immédiatement, même avant la décision aléatoire de ",
                 ("p", "b"), ". ",
                 ("w = 1", "b"), " signifie une victoire immédiate. ",
                 ("w = 2", "b"), " signifie une victoire en au plus 2 coups. ",
                 ("w = 3", "b"), " signifie une victoire en jusqu'à 3 coups. ",
                 ("(w = 0 désactive cette anticipation.)", "b"),
                 " Ce n'est que s'il n'y a pas une telle victoire courte que l'étape 2 suit."),
        ("para", ("2. Le tirage de p (parfait ou erreur) : ", "b"),
                 "À chaque coup, isolément et sans mémoire, la probabilité ",
                 ("p", "b"), " décide si le moteur joue bien ou mal. ",
                 "Avec ", ("p = 50", "b"), " (Débutant, Intermédiaire) statistiquement un coup sur deux est parfait. ",
                 "Avec ", ("p = 20", "b"), " (Avancé) seulement un sur cinq. ",
                 "Avec ", ("p = 80", "b"), " (Expert) quatre sur cinq. ",
                 "Les séries sont purement aléatoires : même avec ", ("p = 50", "b"),
                 " il peut arriver trois erreurs de suite, ou trois coups parfaits de suite."),
        ("para", ("3a. Parfait tiré : meilleur score et règle des 10 demi-coups : ", "b"),
                 "Le moteur choisit directement parmi les meilleurs coups théoriques : ",
                 "parmi plusieurs coups gagnants également bons, le plus rapide en moins de "
                 "10 demi-coups est joué ; parmi plusieurs aussi rapides, l'un est tiré au hasard. ",
                 "Si aucune victoire n'est atteignable en 10 demi-coups, on tire au hasard parmi tous les "
                 "coups gagnants restants (tous alors à plus de 10 demi-coups). ",
                 "S'il n'y a que des nulles, l'une d'elles est tirée au hasard. ",
                 "S'il n'y a que des coups perdants, la règle de défaite s'applique (résistance la plus longue, pondérée, "
                 "avec protection de 10 demi-coups au niveau Parfait)."),
        ("para", ("3b. Faible tiré : la routine d'erreur : ", "b"),
                 "Ce n'est pas un jet de dés à l'aveugle, mais un coup filtré : ",
                 "le filtre ", ("s", "b"), " bloque tous les coups après lesquels l'adversaire gagnerait en au plus ",
                 ("s", "b"), " coups (", ("s = 1", "b"),
                 " interdit les erreurs immédiates au coup suivant ; ", ("s = 0", "b"),
                 " ne filtre rien). ",
                 "Parmi tous les coups autorisés restants, l'un est tiré ", ("uniformément au hasard", "b"),
                 " : une nulle n'est pas préférée ici, elle compte comme tout autre coup admissible. ",
                 ("Cas particuliers : ", "b"), ("p = 100", "b"), " (Parfait) va toujours en 3a. ",
                 ("p = 0", "b"), " (Tacticien) va toujours en 3b. ",
                 ("s = 0, w = 0", "b"), " (niveaux 1–4) tire en 3b sans aucun filtre."),
        ("sub", "filterparadox", "Le paradoxe du filtre : Tacticien contre Débutant (149,5 : 50,5)"),
        ("para", "Dans un duel direct, le niveau ", ("6 Tacticien (0, 3, 3)", "b"),
                 " bat le ", ("4 Débutant (50, 0, 0)", "b"),
                 " nettement, par près de 3 : 1, bien que le Tacticien ne joue pas un seul coup parfait. ",
                 "La raison tient à l'interaction du ", ("bouclier et de l'épée", "b"), " : ",
                 "grâce à ", ("s = 3", "b"), " le Tacticien ne donne presque rien par des erreurs rapides. ",
                 "Et grâce à ", ("w = 3", "b"), " il convertit toute victoire disponible en 1 à 3 coups. ",
                 "Le Débutant, lui, gaspille ses avantages d'ouverture par des erreurs immédiates non filtrées (",
                 ("s = 0", "b"), ") et, faute de priorité de victoire (",
                 ("w = 0", "b"), "), laisse souvent impunies les fautes de l'adversaire. ",
                 "Le même principe se retrouve avec le ", ("5 Avancé (20, 1, 1)", "b"),
                 ", qui bat le Débutant 137 : 63 malgré un ", ("p", "b"), " bien plus faible."),
        ("sub", "spitzenumkehr", "Le renversement au sommet : points contre les maîtres"),
        ("para", "Contre les adversaires les plus forts (Maître supérieur et Parfait) le tableau s'inverse : ",
                 "ici, sur 400 parties, le Débutant obtient ", ("7,0 points", "b"),
                 ", alors que le Tacticien n'en obtient que ", ("0,5 point", "b"), " (un quatorzième de cela). ",
                 "Les adversaires forts ne commettent pratiquement jamais d'erreur. Ni ",
                 ("s = 3", "b"), " ni ", ("w = 3", "b"),
                 " n'aident beaucoup, car le Maître n'offre presque aucune prise. ",
                 "Pour marquer ne serait-ce qu'un point contre des maîtres presque parfaits, il faut des coups parfaits "
                 "avec un plan stratégique profond ; une protection contre la défaite ou une priorité de victoire à courte portée ne suffisent pas. "
                 "Le Débutant joue parfaitement un coup sur deux environ ; "
                 "de temps à autre l'un d'eux suffit pour une nulle. Le Tacticien n'a absolument pas de tels coups."),

        ("head", "datei", "Menu Fichier"),
        ("para", ("Nouvelle partie : ", "b"), "Remet le plateau à la position de départ vide. ",
                 ("Nouvelle avec position aléatoire… : ", "b"), "Crée une position "
                 "de milieu de partie construite au hasard, de 1 à 9 pions, éventuellement avec un résultat "
                 "théorique garanti (victoire, nulle ou défaite). ",
                 ("Charger une position… ", "b"), "et ", ("Enregistrer la position… : ", "b"),
                 "Ouvrent une boîte de dialogue de fichiers standard pour le format universel ",
                 (".4gp", "b"), ". Une partie enregistrée se compose de la "
                 "chaîne chronologique de chiffres des colonnes choisies, par exemple ",
                 ("4433221", "b"), ". ", ("Sauvegarde rapide (F3) ", "b"), "et ",
                 ("Chargement rapide (F4) : ", "b"), "Enregistrent ou chargent le déroulement de la partie "
                 "actuelle directement dans ou depuis le fichier ",
                 ("quicksave.4gp", "b"), " du répertoire principal du programme, sans boîte de dialogue intermédiaire. ",
                 ("Quitter : ", "b"), "Ferme correctement ConnectFour Studio."),

        ("head", "kommandos", "Menu Commandes"),
        ("para", ("Premier / dernier coup (Flèche haut / Flèche bas) : ", "b"),
                 "Saute au début ou à la fin de la partie ; les coups annulés "
                 "restent en mémoire et peuvent être rejoués à tout moment. ",
                 ("Coup précédent / suivant : ", "b"), "Parcourt la partie pas à pas "
                 "(comme les boutons ", ("<", "b"), " et ", (">", "b"), "). ",
                 ("Jouer (ordinateur) : ", "b"), "Correspond au raccourci ", ("F5", "b"), ". ",
                 ("Évaluer tous les coups (1x) : ", "b"), "Correspond à ", ("F6", "b"), " (voir ",
                 ("LINK", "ligne d'évaluation", "wertung"), "). ",
                 ("Analyse permanente : ", "b"), "Correspond à ", ("F7", "b"), " (voir ",
                 ("LINK", "menu Affichage", "ansicht"), ")."),

        ("head", "ansicht", "Menu Affichage"),
        ("para", ("Pion fantôme : ", "b"), "Active ou désactive l'aperçu semi-transparent de la chute. ",
                 ("Animation de chute : ", "b"), "Commande le mouvement fluide de chute des pions. ",
                 ("Afficher le dernier coup : ", "b"), "Active ou désactive l'anneau de marquage blanc "
                 "sur le pion le plus récent. ",
                 ("Score activé/désactivé ", "b"), "et ",
                 ("Réinitialiser le score : ", "b"), "Correspondent aux boutons de la ",
                 ("LINK", "zone du score", "spielstand"), ". La fenêtre d'aide peut être ouverte "
                 "à tout moment via le menu ou avec ", ("F1", "b"), "."),

        ("head", "info", "Zone d'informations, trait et barre d'état"),
        ("para", "En haut à droite, la zone ", ("Au trait", "b"),
                 " indique, à l'aide du symbole du pion et du nom, qui doit jouer : ",
                 ("Humain", "b"), " ou le moteur, avec le niveau actif "
                 "(par exemple « User (1) (70,1,1) »). En mode deux joueurs, "
                 "Humain est toujours affiché ici."),
        ("para", "Juste en dessous, la ", ("zone d'informations", "b"),
                 " fournit des chiffres clés sur la situation actuelle du plateau :"),
        ("para", ("Coup : ", "b"), "Numéro courant du prochain demi-coup (à partir de 1)."),
        ("para", ("Niveau : ", "b"), "",
                 ("LINK", "Niveau", "stufen"),
                 " actif du moteur (en mode tournoi, le niveau de la couleur au trait)."),
        ("para", ("Profondeur : ", "b"), "Dernière profondeur de recherche atteinte, en demi-coups. ",
                 ("Complète : ", "b"), "Calcul complet jusqu'à la fin de la partie. ",
                 ("Livre 12d : ", "b"), "Jusqu'à 12 pions, la recherche s'arrête dès que chaque variante atteint le livre d'ouvertures ; les valeurs sont exactes. ", ("Livre 2d : ", "b"), "Position d'au plus deux pions : valeurs exactes issues du mini-livre intégré, sans aucune recherche. "
                 "Des points de suspension à la fin (p. ex. « 8... ») indiquent un approfondissement "
                 "encore en cours. Un tiret (–) signifie qu'aucun calcul n'est encore disponible."),
        ("para", ("Valeur : ", "b"), "Évaluation théorique du dernier coup en "
                 "notation compacte – par exemple « Jaune (31) », « Rouge (28) » ou "
                 "« Nulle (40) ». L'étiquette désigne le camp gagnant avec un jeu optimal "
                 "des deux camps. Le nombre entre parenthèses est le nombre "
                 "de pions qui restent à poser jusqu'à la décision finale : les petits nombres "
                 "(1–6) signalent une décision imminente ; un ",
                 ("1", "b"), " entre parenthèses marque la victoire immédiate directe au coup suivant. "
                 "Les valeurs élevées (30–42) indiquent une longue fin de partie (42 serait "
                 "une nulle depuis la position vide). À chaque coup joué, cette "
                 "valeur diminue de 1. Le nombre de distance sous le symbole dans la ",
                 ("LINK", "ligne d'évaluation", "wertung"), " après une analyse (",
                 ("F6", "b"), "/", ("F7", "b"),
                 ") montre le même nombre de pions par colonne. "
                 "Avant la première analyse, un tiret (–) apparaît. Une fois la partie terminée, le "
                 "résultat final est annoncé ici, par exemple « Le Jaune gagne ! »."),
        ("para", ("Nœuds : ", "b"), "Nombre de positions explorées dans l'arbre de recherche "
                 "(retour en temps réel du noyau C++, avec des séparateurs de milliers lisibles). ",
                 ("Temps : ", "b"), "Durée de calcul pure de la dernière analyse, en millisecondes. ",
                 ("Vitesse : ", "b"), "Vitesse de recherche en nœuds par seconde "
                 "(par exemple 2,3 M/s = 2,3 millions de positions/s). Toutes les valeurs "
                 "se rapportent à la dernière étape de calcul."),
        ("para", ("Source : ", "b"), "Origine des données de position : ",
                 ("Livre 12d", "b"), " = consultation du livre d'ouvertures intégré (jusqu'à "
                 "une profondeur de 12 pions), ", ("calculé", "b"), " = calcul libre "
                 "en temps réel par le moteur. Un tiret (–) indique "
                 "l'état initial avant le début de la recherche."),
        ("para", "La ", ("barre d'état", "b"), " en bas de la fenêtre renseigne sur "
                 "les coups joués (p. ex. « L'ordinateur a joué 4 en 0,35 s »), les rapports d'analyse "
                 "et les opérations sur fichiers. Pendant un calcul en cours, "
                 "elle affiche « L'ordinateur réfléchit encore – veuillez patienter. » Une tentative de chargement pendant la "
                 "recherche est refusée avec le message « L'ordinateur réfléchit encore – arrêtez-le d'abord, puis chargez. » "
                 "Dans ce cas, il faut d'abord interrompre le calcul avec "
                 "la fonction d'arrêt."),

        ("head", "einstellungen", "Menu Paramètres"),
        ("para", "Le menu ", ("Paramètres", "b"), " regroupe les options principales : ",
                 ("Niveau de l'ordinateur", "b"), " (règle la force de jeu du niveau ",
                 ("LINK", "0 à 14", "stufen"), " ; peut aussi être modifié pendant une "
                 "partie en cours – le ", ("LINK", "score", "spielstand"),
                 " repart à 0–0 après un changement), ",
                 ("Humain-Ordinateur", "b"), " (une partie contre l'intelligence artificielle), ",
                 ("2 joueurs (deux humains)", "b"), " (deux personnes jouent l'une contre l'autre ; "
                 "le programme assure la fonction d'arbitre et la visualisation), ",
                 ("Ordinateur-Ordinateur (jouer jusqu'au bout)", "b"), " (le moteur joue les deux "
                 "camps à partir de la position actuelle, voir ",
                 ("LINK", "modes de jeu", "gegner"), "), ",
                 ("Match Ordinateur-Ordinateur", "b"), " (configure des parties automatiques "
                 "et des tournois, voir ", ("LINK", "modes de jeu", "gegner"), "), ",
                 ("Arrêter le jeu automatique", "b"), " (arrête immédiatement un match en cours ; "
                 "le résultat intermédiaire est conservé) et ",
                 ("Jeu de pions", "b"), " (choix parmi 20 designs de plateau et de pions ; "
                 "on peut aussi les parcourir avec la molette de la souris au-dessus du "
                 "plateau ou avec les touches Page préc. / Page suiv.)."),

        ("head", "sprache", "Choisir la langue"),
        ("para", "Dans le menu ", ("Aide", "b"), " sous ", ("Langue", "b"), " figurent les "
                 "langues disponibles : ", ("Deutsch", "b"), ", ", ("English", "b"), ", ",
                 ("Français", "b"), ", ", ("Español", "b"), ", ", ("Nederlands", "b"), " et ",
                 ("Italiano", "b"), ". "
                 "Le choix (un bouton radio) prend effet immédiatement pour l'Aide et les Informations."),

        ("head", "engine", "Moteur et livre d'ouvertures"),
        ("para", "Le noyau de calcul mathématique est ",
                 ("BitBully by Markus Thill", "b"), ", un module Python efficace "
                 "avec un noyau C++. Il utilise des bitboards optimisés, "
                 "un approfondissement itératif avec un algorithme de recherche MTD(f)/null-window "
                 "et des tables de transposition dynamiques. Le livre d'ouvertures intégré ",
                 ("12-ply-dist", "b"), " fournit des évaluations théoriques et des valeurs exactes de "
                 "distance pour toutes les positions comptant jusqu'à 12 pions posés ; "
                 "dans les variantes plus profondes, le moteur de recherche poursuit le calcul."),
        ("para", "ConnectFour Studio associe une interface de bureau légère (Python, Tkinter, "
                 "rendu graphique avec Pillow) à un jeu résolu. "
                 "Distribué comme logiciel libre sous la ",
                 ("GNU Affero General Public License (AGPL v3)", "b"), "."),

        ("head", "tasten", "Raccourcis clavier"),
        ("para", ("1–7", "b"), " = jouer un coup dans une colonne · ",
                 ("Flèche gauche / Flèche droite", "b"), " = annuler / rejouer un coup · ",
                 ("Flèche haut / Flèche bas", "b"), " = sauter au début / à la fin de la partie · ",
                 ("Page préc. / Page suiv. ou molette de la souris au-dessus du plateau", "b"), " = changer de jeu de pions · ",
                 ("F1", "b"), " = ouvrir la boîte de dialogue d'aide · ",
                 ("F3 / F4", "b"), " = sauvegarde / chargement rapides · ",
                 ("F5", "b"), " = faire jouer le moteur · ",
                 ("F6", "b"), " = analyse unique de la position · ",
                 ("F7", "b"), " = activer ou désactiver l'", ("LINK", "analyse permanente", "buttons"), " · ",
                 ("Escape", "b"), " = fermer un menu ouvert. "
                 "Remarque : les raccourcis fonctionnent tant que le focus de saisie n'est pas dans un "
                 "champ de texte."),
    ],
    "nl": [
        ("head", "inhalt", "Inhoud"),
        ("para", ("LINK", "Het spel", "spiel"), " · ",
                 ("LINK", "Zetten invoeren", "ziehen"), " · ",
                 ("LINK", "De knoppen onder het bord", "buttons"), " · ",
                 ("LINK", "De beoordeling (+, =, –)", "wertung"), " · ",
                 ("LINK", "Stand (mens tegen engine)", "spielstand"), " · ",
                 ("LINK", "Spelmodi", "gegner"), " · ",
                 ("LINK", "Eigen niveaus: User (1) en User (2)", "userstufen"), " · ",
                 ("LINK", "De niveaus", "stufen"), " · ",
                 ("LINK", "Speelsterkte en kruistabel", "elorang"), " · ",
                 ("LINK", "Menu Bestand", "datei"), " · ",
                 ("LINK", "Menu Opdrachten", "kommandos"), " · ",
                 ("LINK", "Menu Weergave", "ansicht"), " · ",
                 ("LINK", "Infovak, Aan zet en statusbalk", "info"), " · ",
                 ("LINK", "Menu Instellingen", "einstellungen"), " · ",
                 ("LINK", "De taal kiezen", "sprache"), " · ",
                 ("LINK", "Engine en openingsboek", "engine"), " · ",
                 ("LINK", "Sneltoetsen", "tasten"), "."),

        ("head", "spiel", "Het spel"),
        ("para", "ConnectFour Studio is een open-sourceprogramma voor “Vier op een rij” "
                 "met 15 niveaus, 20 kiesbare bordontwerpen, een toernooimodus, "
                 "uitgebreide wedstrijdstatistieken en een exacte realtime-analyse."),
        ("para", "De basisregels van “Vier op een rij” zijn eenvoudig: Geel (speler 1) begint "
                 "altijd het spel. Wie als eerste vier eigen stenen in een "
                 "ononderbroken rij weet te plaatsen – horizontaal, verticaal of diagonaal – "
                 "wint. Zijn alle 42 vakjes van het raster gevuld zonder rij van vier, "
                 "dan eindigt het spel in een ", ("remise", "b"), ". Een voltooide winnende rij wordt op het bord ",
                 ("groen gemarkeerd", "b"), "."),
        ("para", "Zetten kunnen op drie manieren worden gedaan: met een ",
                 ("LINK", "muisklik", "ziehen"), ", met de ",
                 ("LINK", "cijfertoetsen 1–7", "ziehen"), " of met de knop ",
                 ("Zet (F5)", "b"), ". De sectie ",
                 ("LINK", "“Zetten invoeren”", "ziehen"), " geeft een uitgebreid overzicht."),

        ("head", "ziehen", "Zetten invoeren"),
        ("para", ("Muisbediening: ", "b"), "Een klik in de gewenste kolom laat daar een steen "
                 "vallen. Beweegt de aanwijzer over het bord, dan toont een halfdoorzichtige ",
                 ("spooksteen", "b"), " waar de steen terechtkomt. Dit voorbeeld kan op elk moment "
                 "worden uitgeschakeld in het menu ",
                 ("LINK", "Weergave", "ansicht"), "."),
        ("para", ("Toetsenbordbediening: ", "b"), "De cijfertoetsen ",
                 ("1 tot 7", "b"), " laten een steen direct in de bijbehorende kolom vallen. "
                 "De toetsen ", ("pijl links / pijl rechts", "b"), " nemen de laatste "
                 "zet terug of spelen die opnieuw af. ", ("Pijl omhoog / pijl omlaag", "b"),
                 " springen direct naar het begin of het einde van het spel. Dezelfde "
                 "acties zijn beschikbaar met de knoppen ", ("<", "b"), ", ",
                 (">", "b"), ", ", ("<<", "b"), " en ", (">>", "b"), ". "
                 "De toets ", ("F5", "b"), " laat de ",
                 ("LINK", "engine", "engine"), " de volgende zet berekenen voor de speler "
                 "die aan zet is – ook op een leeg bord; dan opent de computer "
                 "het spel (zie ",
                 ("LINK", "knoppen onder het bord", "buttons"), ")."),
        ("para", ("Beoordelingsrij: ", "b"), "Een muisklik op een van de zeven "
                 "vakjes onder het bord laat ook de bijbehorende kolom spelen "
                 "(zie ", ("LINK", "beoordelingsrij", "wertung"), ")."),
        ("para", "De laatst gespeelde zet is gemarkeerd met een ",
                 ("witte ring", "b"), " (uit te schakelen onder ",
                 ("LINK", "Weergave", "ansicht"), ")."),

        ("head", "buttons", "De knoppen onder het bord"),
        ("para", ("Nieuw: ", "b"), "Zet het bord terug en begint een nieuw spel vanuit de "
                 "beginstelling (zie ook ",
                 ("LINK", "menu Bestand", "datei"), ")."),
        ("para", ("<< en >>: ", "b"), "Springen direct naar het begin van het spel "
                 "of naar het huidige einde van het spel."),
        ("para", ("< en >: ", "b"), "Nemen zetten stap voor stap terug of herstellen ze, "
                 "zodat elke zettenreeks kan worden nagespeeld."),
        ("para", ("Zet (F5): ", "b"), "Geeft de zet over aan de ",
                 ("LINK", "engine", "engine"), ", die speelt volgens het "
                 "momenteel gekozen ", ("LINK", "niveau", "stufen"), "."),
        ("para", ("Analyseren (F7): ", "b"), "Schakelt de ",
                 ("permanente analyse", "b"), " in of onderbreekt die. Zolang ze aan staat, wordt elke "
                 "stelling direct na een zet volledig op de achtergrond doorgerekend. "
                 "Staat ze uit, dan toont de balk onder het bord alleen de neutrale "
                 "kolomnummers ", ("1–7", "b"), " (zie ",
                 ("LINK", "beoordelingsrij", "wertung"), ")."),
        ("para", "Meer speciale functies vindt u in de menubalk: ",
                 ("Bestand > Nieuw met willekeurige stelling…", "b"), " maakt een "
                 "evenwichtige stelling met 1 tot 9 stenen, desgewenst met een gegeven "
                 "uitslag (zie ", ("LINK", "menu Bestand", "datei"), "); de opdracht ",
                 ("Opdrachten > Alle zetten beoordelen (1x)", "b"), " (", ("F6", "b"),
                 ") start een eenmalige beoordeling van alle zeven kolommen (zie ",
                 ("LINK", "beoordelingsrij", "wertung"), ")."),

        ("head", "wertung", "De beoordeling (+, =, –)"),
        ("para", "Voor elke beschikbare kolom toont de beoordelingsrij onder het bord "
                 "bovenaan een symbolisch resultaat en daaronder het aantal stenen dat nog "
                 "geplaatst moet worden tot het einde van het spel bij perfect spel van beide "
                 "kanten: ",
                 ("+ (groen)", "b"), " = gedwongen winst, ",
                 ("= (geel)", "b"), " = zekere remise, ",
                 ("- (rood)", "b"), " = onvermijdelijk verlies. ",
                 ("Volledig gevulde kolommen zijn gemarkeerd met een “X”.", "b")),
        ("para", "Is er geen beoordeling actief, dan worden alleen de kolomnummers ",
                 ("1–7", "b"), " getoond. Het ", ("LINK", "Infovak", "info"),
                 " aan de rechterrand van het venster noemt de beste voortzetting ook "
                 "in gewone tekst, bijvoorbeeld ", ("“Kol. 4: Geel wint”", "b"), "."),
        ("para", "De stellingbeoordeling is altijd ", ("wiskundig perfect", "b"),
                 " (volledig doorzoeken met het 12-ply-dist-boek) – onafhankelijk van het "
                 "gekozen ", ("LINK", "niveau", "stufen"), ". Alleen de eigenlijke zetten van de ",
                 ("LINK", "engine", "engine"), " zijn op lagere niveaus opzettelijk "
                 "gebrekkig. Het afstandsgetal geeft het exacte aantal stenen dat nog "
                 "geplaatst moet worden tot de beslissing: "
                 "een kleine waarde wijst op een snel einde van het spel, een hoog getal "
                 "op een lang, taai eindspel."),

        ("head", "spielstand", "Stand (mens tegen engine)"),
        ("para", "De weergave ", ("Stand", "b"), " rechtsonder, onder het ",
                 ("LINK", "Infovak", "info"), ", houdt de lopende balans van de sessie "
                 "bij in het duel van mens tegen computer. In grote letters toont ze de "
                 "stand ", ("Mens – Engine", "b"), " (bijvoorbeeld ", ("2–1", "b"),
                 "), aangevuld met de gedetailleerde statistiek ",
                 ("(+winst / =remise / –verlies)", "b"), " vanuit het gezichtspunt van de "
                 "menselijke speler en het totale aantal gespeelde partijen. Een geschat Elo-"
                 "verschil wordt getoond zodra beide kanten minstens een half punt "
                 "hebben gekregen."),
        ("para", "Voor elk ", ("tegenstanderniveau", "b"), " wordt een aparte statistiek bijgehouden. "
                 "Wordt het niveau gewijzigd (via ",
                 ("LINK", "Instellingen", "einstellungen"), "), dan begint het tellen "
                 "opnieuw bij 0–0 voor de nieuwe tegenstander; de vorige balans "
                 "vervalt. Alleen partijen die regulier zijn geëindigd worden geteld: "
                 "de speler die de winnende steen plaatst krijgt het volle punt. "
                 "Bij remise krijgt elke kant een half punt. Vroegtijdig beëindigde partijen "
                 "(bijvoorbeeld via ", ("Nieuw", "b"),
                 " of ", ("Automatisch spel stoppen", "b"), ") tellen niet mee."),
        ("para", ("Aan/uit: ", "b"), "Verbergt of toont de cijferweergave; "
                 "het kader eromheen blijft staan. Zolang de weergave uit staat, "
                 "wordt er niet geteld. ", ("Wissen: ", "b"), "Zet de "
                 "stand van het huidige niveau terug op 0–0. Beide "
                 "functies zijn ook beschikbaar in het menu ", ("LINK", "Weergave", "ansicht"),
                 " (", ("Stand aan/uit", "b"), ", ", ("Stand wissen", "b"),
                 "). Standaard staat het bijhouden uit; er wordt "
                 "pas geteld zodra het is ingeschakeld."),

        ("head", "gegner", "Spelmodi"),
        ("para", "Het menu ", ("Instellingen", "b"), " bepaalt de basis-"
                 "spelmodus: ", ("Mens-computer", "b"), " (met een vrij te kiezen ",
                 ("LINK", "tegenstanderniveau", "stufen"), ") of ",
                 ("2 spelers (beide mens)", "b"), ". In de modus voor twee spelers "
                 "dient ConnectFour Studio als virtueel bord met scheidsrechterfunctie "
                 "en een optionele ", ("LINK", "permanente analyse", "buttons"),
                 " – een goed hulpmiddel om samen te analyseren en te trainen."),
        ("para", ("Computer-computer (uitspelen): ", "b"), "Laat de engine "
                 "de huidige stelling tegen zichzelf uitspelen – altijd op het hoogste "
                 "niveau ", ("Perfect", "b"), ", ongeacht de overige "
                 "instellingen. De functie kan op elk moment opnieuw worden aangeroepen "
                 "en gaat dan verder vanaf de huidige bordstelling."),
        ("para", ("Computer-computerwedstrijd: ", "b"), "Speelt een reeks geautomatiseerde "
                 "partijen. U kunt het ", ("aantal partijen", "b"), " instellen (1 tot 10.000), "
                 "de speltypen voor beide kleuren (", ("Mens", "b"), ", een ",
                 ("LINK", "vast niveau", "stufen"), " of een ",
                 ("LINK", "eigen niveau User (1)/(2)", "userstufen"), "), ",
                 ("kleurwissel", "b"), " na elke partij (Geel en Rood wisselen van "
                 "rol) en het ", ("tempo", "b"), " (Normaal / Snel / Alleen resultaten). "
                 "Doet een mens mee aan de wedstrijd (een kant staat op ",
                 ("Mens", "b"), ") en staat het ", ("tempo", "b"), " op ",
                 ("Normaal", "b"), ", dan pauzeert het programma 3 seconden "
                 "na het einde van een partij, zodat de uitslag gecontroleerd kan worden. ",
                 ("Start", "b"), " start de reeks, ", ("Stop", "b"), " (ook "
                 "via het menu-item ", ("Automatisch spel stoppen", "b"), ") breekt ze af; de "
                 "tussenstand blijft behouden. Is de wedstrijd afgelopen, "
                 "dan komt het dialoogvenster automatisch op de voorgrond; de "
                 "knop ", ("Kopiëren", "b"), " kopieert het volledige "
                 "resultaatverslag (punten, balans winst/remise en Elo-beoordeling) naar "
                 "het klembord."),

        ("head", "userstufen", "Eigen niveaus: User (1) en User (2)"),
        ("para", "In het configuratievenster van de ",
                 ("LINK", "computer-computerwedstrijd", "gegner"), " zijn naast de ingebouwde niveaus "
                 "twee vrij instelbare profielen beschikbaar: ",
                 ("User (1) (eigen p, s, w)", "b"), " en ",
                 ("User (2) (eigen p, s, w)", "b"), ". Zodra zo'n profiel "
                 "voor Geel of Rood wordt gekozen, wordt het bijbehorende "
                 "invoerveld actief (veld 1 stuurt User 1, veld 2 stuurt "
                 "User 2). Hier kunnen de drie gedragsparameters ",
                 ("p, s en w", "b"), " afzonderlijk worden ingesteld (hoe ze precies werken, staat bij ",
                 ("LINK", "De niveaus", "stufen"), "). Omdat de twee profielen onafhankelijk zijn, "
                 "zijn ook duels tussen twee eigen speelstijlen mogelijk."),
        ("para", ("p = aandeel perfecte zetten in procenten", "b"),
                 " (bereik 0 tot 100): De blunderkans wordt berekend als ",
                 ("100 – p", "b"), ". Een waarde van ", ("p = 100", "b"), " (zoals bij ",
                 ("14 Perfect", "b"), ") garandeert foutloos spel bij elke zet. "
                 "De extreme waarde ", ("p = 0", "b"), " (zoals bij niveau ", ("6 Tacticus", "b"),
                 " of in eigen User-profielen) betekent een ",
                 ("blunderkans van 100%", "b"), " – hier wordt de theoretisch beste zet nooit "
                 "gekozen, steeds wordt de blunderroutine doorlopen. Dit is geen "
                 "puur toeval (zoals op niveau 1), want de parameters s en w "
                 "sturen het speelgedrag: niveau 6 Tacticus laat zien hoe sterk een "
                 "profiel met (0, 3, 3) alleen al door tactische beveiligingen speelt. "
                 "Bij tussenwaarden zoals ", ("p = 50", "b"), " (bijvoorbeeld niveau 4 "
                 "Beginner of niveau 7 Gemiddeld) is statistisch gezien elke tweede zet "
                 "perfect, terwijl de andere 50% in de blunder-tak terechtkomt."),
        ("para", ("Beslisvolgorde per zet: ", "b"), "Een korte gedwongen winst ",
                 ("(w)", "b"), " gaat altijd voor – zelfs vóór de toevalsbeslissing van p. "
                 "Is er zo'n korte winst niet, dan beslist de ", ("trekking van p", "b"),
                 ": valt de keuze op ", ("“perfect”", "b"), ", dan speelt het ",
                 ("s-filter", "b"), " geen rol – de engine kiest rechtstreeks uit "
                 "de theoretisch beste zetten (gelijke zetten worden beslist met de 10-ply-regel). "
                 "Valt de beslissing daarentegen op ", ("“blunder”", "b"), ", dan geldt de "
                 "filterketen: eerst ", ("w", "b"), " (winstprioriteit), dan het verliesfilter ",
                 ("s", "b"), " en pas aan het eind een gelijkmatig verdeelde keuze uit alle "
                 "resterende toegestane zetten. Een remise tegen een dreigende nederlaag "
                 "wordt hier niet afgedwongen en ook niet voorgetrokken – ze telt als elke andere toegestane zet."),
        ("para", ("s = verliesbescherming in zetten van de tegenstander", "b"), " (bereik 0 tot 9): "
                 "Dit filter werkt alleen in de blunder-tak: een zwakkere zet "
                 "geldt als ontoelaatbaar als de tegenstander daarna een winst zou kunnen afdwingen "
                 "binnen hooguit s eigen zetten. ", ("s = 0", "b"),
                 " betekent geen filter – directe blunders worden geaccepteerd "
                 "(zoals op niveau 1–4, waar bij een blunder elke geldige zet "
                 "even waarschijnlijk is). ", ("s = 1", "b"), " blokkeert zetten "
                 "die de tegenstander meteen bij de volgende zet de winst zouden geven; ",
                 ("s = 2, 3 of 4", "b"), " breiden die bescherming uit tot 2, 3 "
                 "of 4 zetten van de tegenstander. Winst en remiselijnen zijn "
                 "in de blunder-tak altijd toegestaan."),
        ("para", ("w = winstprioriteit", "b"), " (bereik 0 tot 9): Korte gedwongen "
                 "winsten gaan altijd voor – zelfs vóór de toevalsbeslissing van p: ziet de "
                 "engine een winnend pad waarvan de afstand binnen w zetten ligt, "
                 "dan wordt die winst gespeeld. ", ("w = 1", "b"), " zekert de "
                 "directe winst bij de volgende zet, ", ("w = 2", "b"), " garandeert de "
                 "winst in hooguit 2 eigen zetten; ", ("w = 3", "b"), " en ",
                 ("w = 4", "b"), " werken analoog (zie voor de context ",
                 ("LINK", "De niveaus", "stufen"), "). Is er zo'n nabije winst niet, dan geldt de "
                 "gewone beslissing van p. ",
                 ("w = 0", "b"), " schakelt dit vooruitkijken uit (in de perfecte tak worden winsten "
                 "uiteraard nog steeds genomen via de gewone beoordeling)."),
        ("para", ("Gelijkwaardige zetten (perfecte zetten, alle niveaus): ", "b"),
                 "Zijn er meerdere even goede zetten met de beste score beschikbaar, "
                 "dan kiest een toevalsgenerator er een, om stereotiepe herhalingen van partijen te vermijden. "
                 "Leiden zetten binnen 10 ply tot winst, dan wordt het snelste winnende pad "
                 "gekozen – bij meerdere even snelle wordt er willekeurig een gekozen. "
                 "Ligt geen winst zo dichtbij, dan wordt er een getrokken uit alle winnende zetten. "
                 "Zijn er alleen remiselijnen, dan wordt er willekeurig een van gekozen. "
                 "In puur verliezende stellingen vermijdt niveau ", ("14 Perfect", "b"),
                 " nederlagen binnen 10 ply; bestaan er tragere verliezende zetten, "
                 "dan wordt een daarvan gekozen. Liggen alle verliezende zetten "
                 "meer dan 10 ply ver weg, dan wordt voor de afwisseling willekeurig een uit alle verliezende zetten getrokken."),
        ("para", "Vergelijkende voorbeelden ter oriëntatie: het niveau ",
                 ("Beginner (50, 0, 0)", "b"), " speelt elke tweede zet zwak en "
                 "volledig onbeschermd; het niveau ", ("Gemiddeld (50, 1, 1)", "b"),
                 " speelt eveneens elke tweede zet zwak, maar voorkomt "
                 "elementaire directe blunders bij de volgende zet en neemt consequent "
                 "directe winsten. De ingestelde parameters staan in de verslagen van de ",
                 ("computer-computerwedstrijd", "b"), " "
                 "(bijvoorbeeld als ", ("“User (1) (70, 1, 1)”", "b"), ")."),

        ("head", "stufen", "De niveaus"),
        ("para", "De reguliere niveaus worden beschreven door de parameters ",
                 ("(p, s, w)", "b"), " (niveau 0 verliest opzettelijk, "
                 "niveau 1 speelt puur toeval, niveau 14 speelt foutloos): ",
                 ("p", "b"), " is het percentage perfecte zetten, ",
                 ("s", "b"), " bepaalt de verliesbescherming in zetten van de tegenstander "
                 "(voorkomt foute zetten die binnen s zetten van de tegenstander tot een nederlaag leiden), "
                 "en ", ("w", "b"), " duidt de winstprioriteit aan (gedwongen winsten "
                 "binnen w eigen zetten worden altijd gespeeld). "
                 "Het afstandsgetal onder het symbool in de ",
                 ("LINK", "beoordelingsrij", "wertung"), " geeft het aantal "
                 "stenen dat nog geplaatst moet worden tot het einde van het spel: 1 staat voor de directe "
                 "winnende steen, kleine waarden markeren korte einden, grote waarden lange "
                 "(verdere uitleg in de sectie ",
                 ("LINK", "Infovak", "info"), ")."),
        ("para", ("0 Verliezer (grapniveau): ", "b"), "Speelt opzettelijk zwak "
                 "en kiest bij voorkeur willekeurige verliezende zetten. Is er geen verliezende zet "
                 "beschikbaar, dan valt het programma terug op een remise of een "
                 "willekeurige zet. Een puur grapniveau zonder rating in het Elo-systeem."),
        ("para", ("1 Willekeurig: ", "b"), "Speelt puur toeval: elke geldige zet heeft "
                 "precies dezelfde kans. Dit niveau heeft helemaal geen "
                 "(p, s, w)-logica, geen stellingbeoordeling en geen filters – de "
                 "keuze wordt volledig gelijkmatig uit alle open kolommen gemaakt."),
        ("para", ("2 Zeer makkelijk (25, 0, 0): ", "b"), "Speelt in 25% van de gevallen optimaal en "
                 "in 75% puur willekeurig; maakt zware blunders – ideaal voor beginners "
                 "en kinderen."),
        ("para", ("3 Makkelijk (40, 0, 0): ", "b"), "Speelt in 40% van de gevallen optimaal, maar "
                 "ziet af van tactische beveiligingen (s = 0, w = 0)."),
        ("para", ("4 Beginner (50, 0, 0): ", "b"), "Elke tweede zet wordt "
                 "theoretisch perfect gespeeld (50%). Omdat s = 0 en w = 0 is er "
                 "helemaal geen foutfiltering."),
        ("para", ("5 Gevorderd (20, 1, 1): ", "b"), "Kiest in 20% van de gevallen de theoretisch "
                 "beste zet, maar ziet dankzij s = 1 en w = 1 noch zijn eigen directe winsten "
                 "noch de directe dreigingen van de tegenstander bij de volgende zet over het hoofd."),
        ("para", ("6 Tacticus (0, 3, 3): ", "b"), "Speelt nooit de theoretisch beste zet "
                 "(p = 0), maar speelt tactisch alert: gedwongen winsten binnen "
                 "maximaal 3 eigen zetten worden gespeeld (w = 3) en dreigende "
                 "nederlagen binnen de volgende 3 zetten van de tegenstander worden afgewend "
                 "(s = 3). Een tactisch taaie tegenstander zonder strategisch vooruitzicht."),
        ("para", ("7 Gemiddeld (50, 1, 1): ", "b"), "Solide amateurstandaard: elke tweede "
                 "zet perfect (50%), betrouwbaar gebruik van directe winsten (w = 1) en "
                 "consequent vermijden van directe blunders (s = 1)."),
        ("para", ("8 Veeleisend (55, 1, 1): ", "b"), "Bouwt voort op niveau 7, maar speelt "
                 "in meer dan de helft van alle zetten volledig foutloos (55%)."),
        ("para", ("9 Moeilijk (65, 1, 1): ", "b"), "Met 65% optimale zetten en betrouwbare "
                 "bescherming tegen directe blunders een serieuze tegenstander voor ervaren clubspelers."),
        ("para", ("10 Zeer moeilijk (70, 2, 2): ", "b"), "Combineert hoge precisie (70%) "
                 "met tactisch instinct: herkent en pareert aanvallen over "
                 "2 zetten van de tegenstander (s = 2) en zet eigen winsten in 2 zetten betrouwbaar om "
                 "(w = 2) – een hindernis voor toernooispelers."),
        ("para", ("11 Expert (80, 2, 2): ", "b"), "Speelt in 80% van de gevallen foutloos en "
                 "pareert aanvallen over 2 zetten van de tegenstander betrouwbaar. Eigen "
                 "winstdreigingen over 2 zetten worden veilig omgezet; de toegangspoort tot de meesterklassen."),
        ("para", ("12 Meester (85, 3, 3): ", "b"), "Speelt zeer sterk (85% beste zetten) met "
                 "verregaande tactische beveiligingen: ziet dreigingen en eigen "
                 "winstpaden over 3 zetten (s = 3, w = 3). Zelfs "
                 "ervaren toernooispelers scoren hier nauwelijks nog."),
        ("para", ("13 Sterke meester (92, 4, 4): ", "b"), "Bijna onfeilbaar (92% beste zetten): "
                 "vermijdt gedwongen verliezende varianten tot 4 zetten vooruit "
                 "(s = 4) en zet eigen winsten over 4 zetten "
                 "veilig om (w = 4)."),
        ("para", ("14 Perfect (100, -, -): ", "b"), "Speelt foutloos volgens de "
                 "wetten van het opgeloste spel: als eerste speler (Geel) wint de "
                 "engine elke partij met geweld; als tweede speler (Rood) benut ze elke "
                 "onnauwkeurigheid van de tegenstander om het volle punt te pakken. "
                 "Gelijkwaardige zetten worden statistisch gevarieerd (zie ",
                 ("Gelijkwaardige zetten", "b"), " hierboven). Om het eigen spel te trainen wordt de stellinganalyse "
                 "aanbevolen, zie ", ("LINK", "Analyse", "wertung"), "."),
        ("para", "Oriëntatiewaarden voor de relatieve speelsterkte (bepaald in "
                 "engine-tegen-enginetoernooien met in totaal 18.200 partijen – "
                 "200 partijen per paring – met "
                 "doorlopende kleurwissel; referentieniveau Willekeurig = 1000 Elo): "
                 "1 Willekeurig, 2 Zeer makkelijk ~1204, 3 Makkelijk ~1340, "
                 "4 Beginner ~1431, 5 Gevorderd ~1498, 6 Tacticus ~1614, "
                 "7 Gemiddeld ~1702, 8 Veeleisend ~1752, "
                 "9 Moeilijk ~1817, 10 Zeer moeilijk ~1929, 11 Expert ~2010, "
                 "12 Meester ~2080, 13 Sterke meester ~2132, 14 Perfect ~2174. "
                 "In partijen tegen menselijke tegenstanders kunnen deze verschillen "
                 "psychologisch en tactisch verschuiven. De sterktetabel en de kruistabel staan "
                 "volledig in de sectie ", ("LINK", "“Speelsterkte en kruistabel”", "elorang"), "."),
        ("head", "elorang", "Speelsterkte en kruistabel"),
        ("para", "Alle 91 paringen zijn gespeeld met telkens 200 partijen en kleurwissel "
                 "(18.200 in totaal). Referentieniveau Willekeurig = 1000 Elo "
                 "(relatief, geen FIDE-Elo)."),
        ("para", ("Speelsterkte (Elo):", "b")),
        ("mono",
        " 1 Willekeurig                 1000\n"
        " 2 Zeer makkelijk   (25,0,0)   1204\n"
        " 3 Makkelijk        (40,0,0)   1340\n"
        " 4 Beginner         (50,0,0)   1431\n"
        " 5 Gevorderd        (20,1,1)   1498\n"
        " 6 Tacticus         (0,3,3)    1614\n"
        " 7 Gemiddeld        (50,1,1)   1702\n"
        " 8 Veeleisend       (55,1,1)   1752\n"
        " 9 Moeilijk         (65,1,1)   1817\n"
        "10 Zeer moeilijk    (70,2,2)   1929\n"
        "11 Expert           (80,2,2)   2010\n"
        "12 Meester          (85,3,3)   2080\n"
        "13 Sterke meester   (92,4,4)   2132\n"
        "14 Perfect          (100,-,-)  2174"),
        ("para", ("Kruistabel (punten van het rijniveau tegen het kolomniveau, uit 200):", "b")),
        ("table", "kreuz14"),
        ("sub", "zugwahl", "Achter de schermen: de zetkeuze in 3 stappen"),
        ("para", ("Zo beslist de engine over elke afzonderlijke zet (niveaus 1–14): ", "b"),
                 "Elke zet doorloopt een vaste beslisketen van drie stappen. "
                 "Die verklaart het hele samenspel van speelsterkte, filters "
                 "en schijnbare paradoxen:"),
        ("para", ("1. Eerst winstprioriteit (w) – helemaal zonder dobbelsteen: ", "b"),
                 "Biedt de stelling een gedwongen winst binnen ",
                 ("w", "b"), " eigen zetten, dan wordt die zet meteen gespeeld – zelfs vóór de ",
                 ("p", "b"), "-toevalsbeslissing. ",
                 ("w = 1", "b"), " betekent een directe winst. ",
                 ("w = 2", "b"), " betekent winst in hooguit 2 zetten. ",
                 ("w = 3", "b"), " betekent winst in maximaal 3 zetten. ",
                 ("(w = 0 schakelt dit vooruitkijken uit.)", "b"),
                 " Alleen als er geen zo'n korte winst is, volgt stap 2."),
        ("para", ("2. De trekking van p (perfect of blunder): ", "b"),
                 "Voor elke zet, afzonderlijk en zonder geheugen, bepaalt de kans ",
                 ("p", "b"), " of de engine goed of zwak speelt. ",
                 "Bij ", ("p = 50", "b"), " (Beginner, Gemiddeld) is statistisch gezien elke tweede zet perfect. ",
                 "Bij ", ("p = 20", "b"), " (Gevorderd) slechts elke vijfde. ",
                 "Bij ", ("p = 80", "b"), " (Expert) vier van de vijf. ",
                 "Reeksen zijn puur toeval: zelfs bij ", ("p = 50", "b"),
                 " kunnen drie blunders op rij – of drie perfecte zetten – voorkomen."),
        ("para", ("3a. Perfect getrokken: beste score en de 10-ply-regel: ", "b"),
                 "De engine kiest rechtstreeks uit de theoretisch beste zetten: ",
                 "bij meerdere even goede winnende zetten wordt de snelste binnen "
                 "10 ply gespeeld; bij meerdere even snelle wordt er willekeurig een gekozen. ",
                 "Ligt er geen winst binnen 10 ply, dan wordt er willekeurig een gekozen uit alle overige "
                 "winnende zetten (die dan allemaal meer dan 10 ply ver weg zijn). ",
                 "Zijn er alleen remises, dan wordt er willekeurig een van gekozen. ",
                 "Zijn er alleen verliezende zetten, dan geldt de verliesregel (langste tegenstand, gewogen – "
                 "met 10-ply-bescherming bij Perfect)."),
        ("para", ("3b. Zwak getrokken: de blunderroutine: ", "b"),
                 "Dit is geen blind dobbelen, maar een gefilterde zet: ",
                 "het filter ", ("s", "b"), " blokkeert alle zetten waarna de tegenstander in hooguit ",
                 ("s", "b"), " zetten zou winnen (", ("s = 1", "b"),
                 " verbiedt directe blunders bij de volgende zet; ", ("s = 0", "b"),
                 " filtert niets). ",
                 "Uit alle overgebleven toegestane zetten wordt er een ", ("gelijkmatig willekeurig", "b"),
                 " gekozen – een remise wordt hier niet voorgetrokken, ze telt als elke andere toelaatbare zet. ",
                 ("Bijzondere gevallen: ", "b"), ("p = 100", "b"), " (Perfect) gaat altijd naar 3a. ",
                 ("p = 0", "b"), " (Tacticus) gaat altijd naar 3b. ",
                 ("s = 0, w = 0", "b"), " (niveaus 1–4) kiest in 3b volledig ongefilterd."),
        ("sub", "filterparadox", "De filterparadox: Tacticus tegen Beginner (149,5 : 50,5)"),
        ("para", "In een direct duel verslaat niveau ", ("6 Tacticus (0, 3, 3)", "b"),
                 " ", ("4 Beginner (50, 0, 0)", "b"),
                 " duidelijk, met bijna 3 : 1, hoewel de Tacticus geen enkele perfecte zet speelt. ",
                 "De reden ligt in het samenspel van ", ("schild en zwaard", "b"), ": ",
                 "dankzij ", ("s = 3", "b"), " geeft de Tacticus bijna niets weg door snelle blunders. ",
                 "En dankzij ", ("w = 3", "b"), " zet hij elke beschikbare winst in 1 tot 3 zetten om. ",
                 "De Beginner daarentegen gooit zijn openingsvoordeel weg door ongefilterde directe blunders (",
                 ("s = 0", "b"), ") en laat bij gebrek aan winstprioriteit (",
                 ("w = 0", "b"), ") fouten van de tegenstander vaak ongestraft. ",
                 "Hetzelfde principe zie je bij ", ("5 Gevorderd (20, 1, 1)", "b"),
                 ", dat de Beginner met 137 : 63 verslaat ondanks een veel lagere ", ("p", "b"), "."),
        ("sub", "spitzenumkehr", "De omkering aan de top: punten tegen meesters"),
        ("para", "Tegen de sterkste tegenstanders (Sterke meester en Perfect) keert het beeld om: ",
                 "hier haalt de Beginner uit 400 partijen ", ("7,0 punten", "b"),
                 " – de Tacticus slechts ", ("0,5 punten", "b"), " (een veertiende daarvan). ",
                 "Sterke tegenstanders blunderen praktisch nooit. Noch ",
                 ("s = 3", "b"), " noch ", ("w = 3", "b"),
                 " helpt veel, omdat de meester nauwelijks een doelwit biedt. ",
                 "Om tegen bijna foutloze meesters eigenlijk te scoren heb je perfecte zetten "
                 "met een diep strategisch plan nodig – verliesbescherming of winstprioriteit op korte afstand is niet genoeg. "
                 "De Beginner speelt ongeveer elke tweede zet perfect; "
                 "af en toe is een daarvan genoeg voor remise. De Tacticus mist zulke zetten volledig."),

        ("head", "datei", "Menu Bestand"),
        ("para", ("Nieuw spel: ", "b"), "Zet het bord terug op de lege beginstelling. ",
                 ("Nieuw met willekeurige stelling…: ", "b"), "Maakt een willekeurig opgebouwde "
                 "middenspelstelling met 1 tot 9 stenen, desgewenst met een gegarandeerde "
                 "theoretische uitkomst (winst, remise of verlies). ",
                 ("Stelling laden… ", "b"), "en ", ("Stelling opslaan…: ", "b"),
                 "Openen een standaard bestandsdialoog voor het universele ",
                 (".4gp-formaat", "b"), ". Een opgeslagen spel bestaat uit de "
                 "chronologische cijferreeks van de gekozen kolommen, zoals ",
                 ("4433221", "b"), ". ", ("Snel opslaan (F3) ", "b"), "en ",
                 ("Snel laden (F4): ", "b"), "Slaan het huidige "
                 "partijverloop direct op in of laden het uit het bestand ",
                 ("quicksave.4gp", "b"), " in de hoofdmap van het programma, zonder tussenliggende dialoog. ",
                 ("Afsluiten: ", "b"), "Sluit ConnectFour Studio netjes af."),

        ("head", "kommandos", "Menu Opdrachten"),
        ("para", ("Eerste / laatste zet (pijl omhoog / pijl omlaag): ", "b"),
                 "Springt naar het begin of het einde van het spel; zetten die zijn teruggenomen "
                 "blijven in het geheugen en kunnen op elk moment opnieuw worden gespeeld. ",
                 ("Zet terug / vooruit: ", "b"), "Loopt stapsgewijs door het spel "
                 "(zoals de knoppen ", ("<", "b"), " en ", (">", "b"), "). ",
                 ("Zet (computer): ", "b"), "Komt overeen met de sneltoets ", ("F5", "b"), ". ",
                 ("Alle zetten beoordelen (1x): ", "b"), "Komt overeen met ", ("F6", "b"), " (zie ",
                 ("LINK", "beoordelingsrij", "wertung"), "). ",
                 ("Permanente analyse: ", "b"), "Komt overeen met ", ("F7", "b"), " (zie ",
                 ("LINK", "menu Weergave", "ansicht"), ")."),

        ("head", "ansicht", "Menu Weergave"),
        ("para", ("Spooksteen: ", "b"), "Schakelt het halfdoorzichtige valvoorbeeld in of uit. ",
                 ("Valanimatie: ", "b"), "Bepaalt de vloeiende valbeweging van de gelaten stenen. ",
                 ("Laatste zet tonen: ", "b"), "Schakelt de witte markeerring "
                 "op de meest recente steen in of uit. ",
                 ("Stand aan/uit ", "b"), "en ",
                 ("Stand wissen: ", "b"), "Komen overeen met de knoppen van het ",
                 ("LINK", "standgedeelte", "spielstand"), ". Het helpvenster kan op elk moment "
                 "worden geopend via het menu of met ", ("F1", "b"), "."),

        ("head", "info", "Infovak, Aan zet en statusbalk"),
        ("para", "Rechtsboven toont het vak ", ("Aan zet", "b"),
                 " met het stensymbool en de naam wie er aan zet is: ",
                 ("Mens", "b"), " of de engine, met vermelding van het actieve niveau "
                 "(bijvoorbeeld “User (1) (70,1,1)”). In de modus voor twee spelers "
                 "wordt hier altijd Mens getoond."),
        ("para", "Direct daaronder geeft het ", ("Infovak", "b"),
                 " kerncijfers over de actuele bordsituatie:"),
        ("para", ("Zet: ", "b"), "Lopend nummer van de volgende halve zet (te beginnen bij 1)."),
        ("para", ("Niveau: ", "b"), "Actief ",
                 ("LINK", "niveau", "stufen"),
                 " van de engine (in de toernooimodus het niveau van de kleur die aan zet is)."),
        ("para", ("Diepte: ", "b"), "Laatst bereikte zoekdiepte in ply. ",
                 ("Volledig: ", "b"), "Volledige berekening tot het einde van het spel. ",
                 ("Boek 12d: ", "b"), "Tot 12 stenen stopt het zoeken zodra elke variant het openingsboek bereikt – de waarden zijn exact. ", ("Boek 2d: ", "b"), "Stelling met hoogstens twee stenen: exacte waarden uit het ingebouwde miniboek, zonder te zoeken. "
                 "Een afsluitend beletselteken (bijv. “8...”) toont een verdieping die nog "
                 "loopt. Een streepje (–) betekent dat er nog geen berekening beschikbaar is."),
        ("para", ("Waarde: ", "b"), "Theoretische beoordeling van de laatste zet in "
                 "compacte notatie – bijvoorbeeld “Geel (31)”, “Rood (28)” of "
                 "“Remise (40)”. Het label noemt de winnende kant bij optimaal spel "
                 "van beide kanten. Het getal tussen haakjes is het aantal "
                 "stenen dat nog geplaatst moet worden tot de eindbeslissing: kleine getallen "
                 "(1–6) wijzen op een nakende beslissing – een ",
                 ("1", "b"), " tussen haakjes markeert de directe winst bij de volgende zet. "
                 "Hoge waarden (30–42) wijzen op een lang eindspel (42 zou een "
                 "remise vanuit de lege stelling zijn). Bij elke gespeelde zet telt deze "
                 "waarde met 1 af. Het afstandsgetal onder het symbool in de ",
                 ("LINK", "beoordelingsrij", "wertung"), " na een analyse (",
                 ("F6", "b"), "/", ("F7", "b"),
                 ") toont hetzelfde aantal stenen per kolom. "
                 "Vóór de eerste analyse verschijnt een streepje (–). Na afloop van het spel wordt hier de "
                 "einduitslag gemeld, bijvoorbeeld “Geel wint!”."),
        ("para", ("Knopen: ", "b"), "Aantal doorzochte stellingen in de zoekboom "
                 "(realtime terugmelding van de C++-kern, met leesbare duizendtalscheiding). ",
                 ("Tijd: ", "b"), "Pure rekentijd van de laatste analyse in milliseconden. ",
                 ("Snelheid: ", "b"), "Zoeksnelheid in knopen per seconde "
                 "(bijvoorbeeld 2,3 M/s = 2,3 miljoen stellingen/s). Alle waarden "
                 "hebben betrekking op de meest recente rekenstap."),
        ("para", ("Bron: ", "b"), "Herkomst van de stellinggegevens: ",
                 ("Boek 12d", "b"), " = opzoeken in het geïntegreerde openingsboek (tot "
                 "een diepte van 12 stenen), ", ("berekend", "b"), " = vrije "
                 "realtimeberekening door de engine. Een streepje (–) geeft "
                 "de beginstatus aan voordat het zoeken begint."),
        ("para", "De ", ("statusbalk", "b"), " onderaan het venster meldt "
                 "gespeelde zetten (bijv. “Computer speelde 4 in 0,35 s”), analyseverslagen "
                 "en bestandsbewerkingen. Zolang er een berekening loopt, "
                 "toont ze “Computer denkt nog na - even wachten.” Een laadpoging tijdens het "
                 "zoeken wordt afgewezen met de melding “Computer denkt nog na - stop eerst, laad daarna.” "
                 "In dat geval moet de berekening eerst worden onderbroken met "
                 "de stopfunctie."),

        ("head", "einstellungen", "Menu Instellingen"),
        ("para", "Het menu ", ("Instellingen", "b"), " bundelt de centrale opties: ",
                 ("Computerniveau", "b"), " (stelt de speelsterkte in van niveau ",
                 ("LINK", "0 tot 14", "stufen"), "; kan ook tijdens een lopend "
                 "spel worden gewijzigd – de ", ("LINK", "stand", "spielstand"),
                 " begint na een wijziging weer bij 0–0), ",
                 ("Mens-computer", "b"), " (een spel tegen de kunstmatige intelligentie), ",
                 ("2 spelers (beide mens)", "b"), " (twee mensen spelen tegen elkaar; "
                 "het programma neemt de scheidsrechterfunctie en de visualisatie over), ",
                 ("Computer-computer (uitspelen)", "b"), " (de engine speelt beide "
                 "kanten vanuit de huidige stelling, zie ",
                 ("LINK", "spelmodi", "gegner"), "), ",
                 ("Computer-computerwedstrijd", "b"), " (configureert geautomatiseerde partijen "
                 "en toernooien, zie ", ("LINK", "spelmodi", "gegner"), "), ",
                 ("Automatisch spel stoppen", "b"), " (stopt een lopende wedstrijd onmiddellijk; "
                 "de tussenstand blijft behouden) en ",
                 ("Steenset", "b"), " (keuze uit 20 bord- en steenontwerpen; "
                 "u kunt er ook doorheen bladeren met het muiswiel boven het "
                 "bord of met de toetsen Page Up / Page Down)."),

        ("head", "sprache", "De taal kiezen"),
        ("para", "In het menu ", ("Help", "b"), " staan onder ", ("Taal", "b"), " de "
                 "beschikbare talen: ", ("Deutsch", "b"), ", ", ("English", "b"), ", ",
                 ("Français", "b"), ", ", ("Español", "b"), ", ", ("Nederlands", "b"), " en ",
                 ("Italiano", "b"), ". "
                 "De keuze (een keuzerondje) werkt direct door in Help en Info."),

        ("head", "engine", "Engine en openingsboek"),
        ("para", "De wiskundige rekenkern is ",
                 ("BitBully by Markus Thill", "b"), " – een efficiënte Python-module "
                 "met een C++-kern. Ze gebruikt geoptimaliseerde bitboards, "
                 "iteratieve verdieping met een MTD(f)/null-window-zoekalgoritme "
                 "en dynamische transpositietabellen. Het geïntegreerde openingsboek ",
                 ("12-ply-dist", "b"), " levert theoretische beoordelingen en exacte "
                 "afstandswaarden voor alle stellingen met maximaal 12 geplaatste stenen; "
                 "bij diepere varianten zet de zoekengine de berekening voort."),
        ("para", "ConnectFour Studio combineert een slanke desktopinterface (Python, Tkinter, "
                 "grafische weergave met Pillow) met een opgelost spel. "
                 "Gelicentieerd als vrije software onder de ",
                 ("GNU Affero General Public License (AGPL v3)", "b"), "."),

        ("head", "tasten", "Sneltoetsen"),
        ("para", ("1–7", "b"), " = een kolomzet doen · ",
                 ("Pijl links / pijl rechts", "b"), " = een zet terugnemen / opnieuw spelen · ",
                 ("Pijl omhoog / pijl omlaag", "b"), " = naar het begin / einde van het spel springen · ",
                 ("Page Up / Page Down of muiswiel boven het bord", "b"), " = steenset wisselen · ",
                 ("F1", "b"), " = het helpvenster openen · ",
                 ("F3 / F4", "b"), " = snel opslaan / laden · ",
                 ("F5", "b"), " = de engine laten zetten · ",
                 ("F6", "b"), " = eenmalige stellinganalyse · ",
                 ("F7", "b"), " = de ", ("LINK", "permanente analyse", "buttons"), " in- of uitschakelen · ",
                 ("Escape", "b"), " = een geopend menu sluiten. "
                 "Let op: sneltoetsen werken zolang de invoerfocus niet in een "
                 "tekstveld staat."),
    ],
    "it": [

        ("head", "inhalt", "Contenuti"),
        ("para", ("LINK", "Il gioco", "spiel"), " · ",
                 ("LINK", "Inserire le mosse", "ziehen"), " · ",
                 ("LINK", "I pulsanti sotto la scacchiera", "buttons"), " · ",
                 ("LINK", "La valutazione (+, =, –)", "wertung"), " · ",
                 ("LINK", "Punteggio (umano contro motore)", "spielstand"), " · ",
                 ("LINK", "Modalità di gioco", "gegner"), " · ",
                 ("LINK", "Livelli personalizzati: User (1) e User (2)", "userstufen"), " · ",
                 ("LINK", "I livelli", "stufen"), " · ",
                 ("LINK", "Forza di gioco e tabella incrociata", "elorang"), " · ",
                 ("LINK", "Menu File", "datei"), " · ",
                 ("LINK", "Menu Comandi", "kommandos"), " · ",
                 ("LINK", "Menu Vista", "ansicht"), " · ",
                 ("LINK", "Riquadro info, A chi tocca e barra di stato", "info"), " · ",
                 ("LINK", "Menu Impostazioni", "einstellungen"), " · ",
                 ("LINK", "Scegliere la lingua", "sprache"), " · ",
                 ("LINK", "Motore e libro di aperture", "engine"), " · ",
                 ("LINK", "Scorciatoie da tastiera", "tasten"), "."),

        ("head", "spiel", "Il gioco"),
        ("para", "ConnectFour Studio è un programma open source per “Forza quattro” "
                 "con 15 livelli, 20 design di scacchiera selezionabili, una modalità torneo, "
                 "statistiche dettagliate degli incontri e un'analisi esatta in tempo reale."),
        ("para", "Le regole di base di “Forza quattro” sono semplici: il Giallo (giocatore 1) inizia "
                 "sempre la partita. Vince chi per primo riesce a mettere quattro proprie pietre in una "
                 "fila ininterrotta – orizzontale, verticale o diagonale. "
                 "Se tutte le 42 caselle della griglia sono piene senza una fila da quattro, "
                 "la partita finisce in ", ("pareggio", "b"), ". Una fila vincente completata viene sulla scacchiera ",
                 ("evidenziata in verde", "b"), "."),
        ("para", "Le mosse si possono fare in tre modi: con un ",
                 ("LINK", "clic del mouse", "ziehen"), ", con i ",
                 ("LINK", "tasti numerici 1–7", "ziehen"), " o con il pulsante ",
                 ("Mossa (F5)", "b"), ". La sezione ",
                 ("LINK", "“Inserire le mosse”", "ziehen"), " dà una panoramica dettagliata."),

        ("head", "ziehen", "Inserire le mosse"),
        ("para", ("Controllo con il mouse: ", "b"), "Un clic nella colonna desiderata fa cadere lì una pietra. "
                 "Quando il puntatore si sposta sulla scacchiera, una ",
                 ("pietra fantasma", "b"), " semitrasparente mostra dove cadrà. Questa anteprima può essere "
                 "disattivata in qualsiasi momento nel menu ",
                 ("LINK", "Vista", "ansicht"), "."),
        ("para", ("Controllo con la tastiera: ", "b"), "I tasti numerici ",
                 ("1 a 7", "b"), " fanno cadere una pietra direttamente nella colonna corrispondente. "
                 "I tasti ", ("freccia sinistra / freccia destra", "b"), " ritirano l'ultima "
                 "mossa o la rigiocano. ", ("Freccia su / freccia giù", "b"),
                 " saltano direttamente all'inizio o alla fine della partita. Le stesse "
                 "azioni sono disponibili con i pulsanti ", ("<", "b"), ", ",
                 (">", "b"), ", ", ("<<", "b"), " e ", (">>", "b"), ". "
                 "Il tasto ", ("F5", "b"), " fa calcolare al ",
                 ("LINK", "motore", "engine"), " la mossa successiva per il giocatore "
                 "a cui tocca muovere – anche su una scacchiera vuota; in tal caso il computer "
                 "apre la partita (vedi ",
                 ("LINK", "pulsanti sotto la scacchiera", "buttons"), ")."),
        ("para", ("Riga di valutazione: ", "b"), "Un clic su una delle sette "
                 "caselle sotto la scacchiera gioca anche la colonna corrispondente "
                 "(vedi ", ("LINK", "riga di valutazione", "wertung"), ")."),
        ("para", "L'ultima mossa giocata è contrassegnata da un ", ("anello bianco", "b"), " (disattivabile in ",
                 ("LINK", "Vista", "ansicht"), ")."),
        ("head", "buttons", "I pulsanti sotto la scacchiera"),
        ("para", ("Nuovo: ", "b"), "Ripristina la scacchiera e inizia una nuova partita dalla posizione iniziale (vedi anche ",
                 ("LINK", "menu File", "datei"), ")."),
        ("para", ("<< e >>: ", "b"), "Saltano direttamente all'inizio della partita o alla fine corrente della partita."),
        ("para", ("< e >: ", "b"), "Ritirano le mosse passo passo o le ripristinano, così si può ricostruire qualsiasi sequenza di mosse."),
        ("para",
                 ("Mossa (F5): ", "b"),
                 "Passa la mossa al ",
                 ("LINK", "motore", "engine"),
                 ", che gioca secondo il ",
                 ("LINK", "livello", "stufen"),
                 " selezionato."),
        ("para",
                 ("Analizza (F7): ", "b"),
                 "Attiva l'",
                 ("analisi permanente", "b"),
                 " o la mette in pausa. Finché è attiva, ogni posizione viene calcolata completamente in background subito dopo una mossa. "
                 "Quando è spenta, la barra sotto la scacchiera mostra solo i numeri neutri delle colonne ",
                 ("1–7", "b"),
                 " (vedi ",
                 ("LINK", "riga di valutazione", "wertung"),
                 ")."),
        ("para",
                 "Altre funzioni speciali sono disponibili dalla barra dei menu: ",
                 ("File > Nuova con posizione casuale…", "b"),
                 " crea una posizione equilibrata con da 1 a 9 pietre, su richiesta con un risultato dato (vedi ",
                 ("LINK", "menu File", "datei"),
                 "); il comando ",
                 ("Comandi > Valuta tutte le mosse (1x)", "b"),
                 " (",
                 ("F6", "b"),
                 ") avvia una valutazione unica di tutte e sette le colonne (vedi ",
                 ("LINK", "riga di valutazione", "wertung"),
                 ")."),
        ("head", "wertung", "La valutazione (+, =, –)"),
        ("para",
                 "Per ogni colonna disponibile, la riga di valutazione sotto la scacchiera mostra in alto un risultato simbolico e, sotto, il numero di pietre "
                 "ancora da mettere fino alla fine della partita con gioco perfetto da entrambe le parti: ",
                 ("+ (verde)", "b"),
                 " = vittoria forzata, ",
                 ("= (giallo)", "b"),
                 " = pareggio certo, ",
                 ("- (rosso)", "b"),
                 " = sconfitta inevitabile. ",
                 ("Le colonne completamente piene sono contrassegnate con una “X”.", "b")),
        ("para",
                 "Se non è attiva alcuna valutazione, vengono mostrati solo i numeri delle colonne ",
                 ("1–7", "b"),
                 ". Il ",
                 ("LINK", "riquadro Info", "info"),
                 " sul bordo destro della finestra indica la migliore continuazione anche in testo chiaro, per esempio ",
                 ("“Col. 4: il Giallo vince”", "b"),
                 "."),
        ("para",
                 "La valutazione della posizione è sempre ",
                 ("matematicamente perfetta", "b"),
                 " (ricerca completa con il libro 12-ply-dist) – indipendentemente dal ",
                 ("LINK", "livello", "stufen"),
                 " selezionato. Solo le mosse effettive del ",
                 ("LINK", "motore", "engine"),
                 " sono volutamente imperfette ai livelli più bassi. Il numero di distanza indica l'esatto numero di pietre ancora da mettere fino alla decisione: "
                 "un valore piccolo segnala una fine rapida della partita, un numero alto un finale lungo e difficile."),
        ("head", "spielstand", "Punteggio (umano contro motore)"),
        ("para",
                 "Il display ",
                 ("Punteggio", "b"),
                 " in basso a destra, sotto il ",
                 ("LINK", "riquadro Info", "info"),
                 ", registra il bilancio corrente della sessione nel duello tra umano e computer. In caratteri grandi mostra il punteggio ",
                 ("Umano – Motore", "b"),
                 " (per esempio ",
                 ("2–1", "b"),
                 "), integrato dalla statistica dettagliata ",
                 ("(+vittorie / =pareggi / –sconfitte)", "b"),
                 " dal punto di vista del giocatore umano e dal numero totale di partite giocate. Una differenza Elo stimata viene mostrata appena entrambe "
                 "le parti hanno ottenuto almeno mezzo punto."),
        ("para",
                 "Per ogni ",
                 ("livello avversario", "b"),
                 " viene tenuta una statistica separata. Quando si cambia livello (tramite ",
                 ("LINK", "Impostazioni", "einstellungen"),
                 "), il conteggio ricomincia da 0–0 per il nuovo avversario; il bilancio precedente viene scartato. Solo le partite finite regolarmente "
                 "vengono conteggiate: il giocatore che mette la pietra vincente riceve il punto intero. In caso di pareggio ogni parte riceve mezzo punto. Le partite "
                 "interrotte in anticipo (per esempio tramite ",
                 ("Nuovo", "b"),
                 " o ",
                 ("Interrompi gioco automatico", "b"),
                 ") non contano."),
        ("para",
                 ("On/Off: ", "b"),
                 "Nasconde o mostra il display numerico; la cornice intorno resta. Finché il display è spento, il conteggio è in pausa. ",
                 ("Azzera: ", "b"),
                 "Riporta il punteggio del livello corrente a 0–0. Entrambe le funzioni sono disponibili anche dal menu ",
                 ("LINK", "Vista", "ansicht"),
                 " (",
                 ("Punteggio on/off", "b"),
                 ", ",
                 ("Azzera punteggio", "b"),
                 "). Per impostazione predefinita la registrazione è spenta; il conteggio inizia solo una volta attivato."),
        ("head", "gegner", "Modalità di gioco"),
        ("para",
                 "Il menu ",
                 ("Impostazioni", "b"),
                 " imposta la modalità di gioco di base: ",
                 ("Umano-Computer", "b"),
                 " (con un ",
                 ("LINK", "livello avversario", "stufen"),
                 " liberamente selezionabile) o ",
                 ("2 giocatori (entrambi umani)", "b"),
                 ". Nella modalità a due giocatori, ConnectFour Studio serve da scacchiera virtuale con funzione di arbitro e un'opzionale ",
                 ("LINK", "analisi permanente", "buttons"),
                 " – un buon strumento per analizzare e allenarsi insieme."),
        ("para",
                 ("Computer-Computer (gioca): ", "b"),
                 "Fa finire al motore la posizione corrente contro sé stesso – sempre al livello più alto ",
                 ("Perfetto", "b"),
                 ", indipendentemente dalle altre impostazioni. La funzione può essere richiamata in qualsiasi momento e prosegue dalla posizione corrente sulla scacchiera."),
        ("para",
                 ("Incontro Computer-Computer: ", "b"),
                 "Esegue una serie di partite automatiche. Si possono impostare il ",
                 ("numero di partite", "b"),
                 " (da 1 a 10.000), i tipi di giocatore per entrambi i colori (",
                 ("Umano", "b"),
                 ", un ",
                 ("LINK", "livello fisso", "stufen"),
                 " o un ",
                 ("LINK", "livello personalizzato User (1)/(2)", "userstufen"),
                 "), lo ",
                 ("scambio colori", "b"),
                 " dopo ogni singola partita (il Giallo e il Rosso si scambiano i ruoli) e la ",
                 ("velocità", "b"),
                 " (Normale / Veloce / Solo risultati). Se un umano partecipa all'incontro (un lato è impostato su ",
                 ("Umano", "b"),
                 ") e la ",
                 ("velocità", "b"),
                 " è impostata su ",
                 ("Normale", "b"),
                 ", il programma fa una pausa di 3 secondi dopo la fine di una partita, così si può controllare il risultato. ",
                 ("Avvia", "b"),
                 " avvia la serie, ",
                 ("Ferma", "b"),
                 " (anche tramite la voce di menu ",
                 ("Interrompi gioco automatico", "b"),
                 ") la interrompe; il risultato parziale viene conservato. Quando l'incontro è finito, la finestra di dialogo viene automaticamente in primo piano; il pulsante ",
                 ("Copia", "b"),
                 " copia l'intero resoconto del risultato (punti, bilancio vittorie/pareggi e valutazione Elo) negli appunti."),
        ("head", "userstufen", "Livelli personalizzati: User (1) e User (2)"),
        ("para",
                 "Nella finestra di configurazione dell'",
                 ("LINK", "incontro computer-computer", "gegner"),
                 ", oltre ai livelli integrati sono disponibili due profili liberamente configurabili: ",
                 ("User (1) (p,s,w propri)", "b"),
                 " e ",
                 ("User (2) (p,s,w propri)", "b"),
                 ". Appena si sceglie un tale profilo per il Giallo o il Rosso, il campo di input corrispondente viene attivato (il campo 1 controlla User 1, il campo 2 controlla User "
                 "2). Qui i tre parametri di comportamento ",
                 ("p, s e w", "b"),
                 " possono essere impostati individualmente (per il funzionamento esatto, vedi ",
                 ("LINK", "I livelli", "stufen"),
                 "). Poiché i due profili sono indipendenti, sono possibili anche duelli tra due stili di gioco personalizzati."),
        ("para",
                 ("p = quota di mosse perfette in percento", "b"),
                 " (intervallo da 0 a 100): Il tasso di errori si calcola come ",
                 ("100 – p", "b"),
                 ". Un valore di ",
                 ("p = 100", "b"),
                 " (come per ",
                 ("14 Perfetto", "b"),
                 ") garantisce un gioco impeccabile a ogni mossa. Il valore estremo ",
                 ("p = 0", "b"),
                 " (come per il livello ",
                 ("6 Tattico", "b"),
                 " o nei profili User personalizzati) significa un ",
                 ("tasso di errori del 100%", "b"),
                 " – qui la mossa teoricamente migliore non viene mai scelta, viene sempre eseguita la routine degli errori. Questo non è puro caso (come al livello 1), perché "
                 "i parametri s e w guidano il comportamento di gioco: il livello 6 Tattico mostra quanto forte giochi un profilo con (0, 3, 3) già solo grazie alle protezioni "
                 "tattiche. Con valori intermedi come ",
                 ("p = 50", "b"),
                 " (per esempio livello 4 Principiante o livello 7 Intermedio), statisticamente ogni seconda mossa è perfetta, mentre l'altro 50% finisce nel ramo "
                 "degli errori."),
        ("para",
                 ("Sequenza di decisione per mossa: ", "b"),
                 "Una breve vittoria forzata ",
                 ("(w)", "b"),
                 " ha sempre la precedenza – persino prima della decisione casuale di p. Se non c'è una tale breve vittoria, decide l'",
                 ("estrazione di p", "b"),
                 ": se la scelta cade su ",
                 ("“perfetta”", "b"),
                 ", il ",
                 ("filtro s", "b"),
                 " non ha alcun ruolo – il motore sceglie direttamente tra le mosse teoricamente migliori (le mosse pari vengono decise con la regola dei 10 ply). Se invece la decisione cade su ",
                 ("“errore”", "b"),
                 ", vale la catena di filtri: prima ",
                 ("w", "b"),
                 " (priorità alle vittorie), poi il filtro di sconfitta ",
                 ("s", "b"),
                 " e solo alla fine una scelta uniformemente distribuita tra tutte le mosse ammissibili rimanenti. Un pareggio contro una sconfitta minacciosa non viene qui "
                 "né forzato né preferito – conta come qualsiasi altra mossa consentita."),
        ("para",
                 ("s = protezione contro le sconfitte in mosse dell'avversario", "b"),
                 " (intervallo da 0 a 9): Questo filtro agisce solo nel ramo degli errori: una mossa più debole è considerata inammissibile se l'avversario potrebbe poi forzare una vittoria "
                 "entro al massimo s proprie mosse. ",
                 ("s = 0", "b"),
                 " significa nessun filtro – gli errori diretti vengono accettati (come ai livelli 1–4, dove in caso di errore ogni mossa legale è ugualmente probabile). ",
                 ("s = 1", "b"),
                 " blocca le mosse che regalerebbero all'avversario la vittoria già alla mossa successiva; ",
                 ("s = 2, 3 o 4", "b"),
                 " estendono questa protezione a 2, 3 o 4 mosse dell'avversario. Vittorie e linee di pareggio sono sempre consentite nel ramo degli errori."),
        ("para",
                 ("w = priorità alle vittorie", "b"),
                 " (intervallo da 0 a 9): Le brevi vittorie forzate vengono sempre per prime – persino prima della decisione casuale di p: se il motore individua un percorso vincente la cui distanza "
                 "rientra in w mosse, questa vittoria viene giocata. ",
                 ("w = 1", "b"),
                 " assicura la vittoria diretta alla mossa successiva, ",
                 ("w = 2", "b"),
                 " garantisce la vittoria in al massimo 2 proprie mosse; ",
                 ("w = 3", "b"),
                 " e ",
                 ("w = 4", "b"),
                 " funzionano in modo analogo (per il contesto vedi ",
                 ("LINK", "I livelli", "stufen"),
                 "). Se non c'è una tale vittoria vicina, vale la normale decisione di p. ",
                 ("w = 0", "b"),
                 " disattiva questa previsione (nel ramo perfetto, le vittorie vengono naturalmente prese comunque tramite la normale valutazione)."),
        ("para",
                 ("Mosse pari (mosse perfette, tutti i livelli): ", "b"),
                 "Se sono disponibili più mosse ugualmente buone con il miglior punteggio, un generatore casuale ne sceglie una, per evitare ripetizioni stereotipate delle partite. "
                 "Se delle mosse portano alla vittoria entro 10 ply, viene scelto il percorso vincente più veloce – tra più percorsi ugualmente veloci ne viene scelto uno a caso. "
                 "Se nessuna vittoria è così vicina, ne viene estratta una tra tutte le mosse vincenti. Se ci sono solo linee di pareggio, ne viene scelta una a caso. "
                 "In posizioni puramente perdenti, il livello ",
                 ("14 Perfetto", "b"),
                 " evita le sconfitte entro 10 ply; se esistono mosse perdenti più lente, ne viene scelta una di queste. Se tutte le mosse perdenti sono a più di 10 ply "
                 "di distanza, per varietà ne viene estratta una a caso tra tutte le mosse perdenti."),
        ("para",
                 "Esempi comparativi per orientarsi: il livello ",
                 ("Principiante (50, 0, 0)", "b"),
                 " gioca ogni seconda mossa in modo debole e completamente senza protezione; il livello ",
                 ("Intermedio (50, 1, 1)", "b"),
                 " gioca anche lui ogni seconda mossa in modo debole, ma impedisce errori diretti elementari alla mossa successiva e prende costantemente vittorie dirette immediate. I "
                 "parametri impostati sono riportati nei resoconti dell'",
                 ("incontro Computer-Computer", "b"),
                 " (per esempio come ",
                 ("“User (1) (70, 1, 1)”", "b"),
                 ")."),
        ("head", "stufen", "I livelli"),
        ("para",
                 "I livelli regolari sono descritti dai parametri ",
                 ("(p, s, w)", "b"),
                 " (il livello 0 perde di proposito, il livello 1 gioca puro caso, il livello 14 gioca in modo impeccabile): ",
                 ("p", "b"),
                 " è la percentuale di mosse perfette, ",
                 ("s", "b"),
                 " definisce la protezione contro le sconfitte in mosse dell'avversario (impedisce mosse errate che portano alla sconfitta entro s mosse dell'avversario), e ",
                 ("w", "b"),
                 " indica la priorità alle vittorie (le vittorie forzate entro w proprie mosse vengono sempre giocate). La cifra di distanza sotto il simbolo nella ",
                 ("LINK", "riga di valutazione", "wertung"),
                 " indica il numero di pietre ancora da mettere fino alla fine della partita: 1 sta per la pietra vincente immediata, valori piccoli segnano "
                 "finali brevi, valori grandi quelli lunghi (ulteriori spiegazioni nella sezione ",
                 ("LINK", "riquadro Info", "info"),
                 ")."),
        ("para",
                 ("0 Perdente (livello divertente): ", "b"),
                 "Gioca volutamente in modo debole e sceglie preferibilmente mosse perdenti casuali. Se non è disponibile alcuna mossa perdente, il programma ripiega su un pareggio o una "
                 "mossa casuale. Un puro livello divertente senza valutazione nel sistema Elo."),
        ("para",
                 ("1 Casuale: ", "b"),
                 "Gioca puro caso: ogni mossa legale ha esattamente la stessa probabilità. Questo livello non ha affatto logica (p, s, w), nessuna valutazione della posizione e nessun "
                 "filtro – la scelta avviene in modo completamente uniforme tra tutte le colonne aperte."),
        ("para",
                 ("2 Molto facile (25, 0, 0): ", "b"),
                 "Gioca in modo ottimale il 25% delle volte e in modo puramente casuale il 75% delle volte; commette gravi errori – ideale per principianti e bambini."),
        ("para", ("3 Facile (40, 0, 0): ", "b"), "Gioca in modo ottimale il 40% delle volte, ma rinuncia alle protezioni tattiche (s = 0, w = 0)."),
        ("para",
                 ("4 Principiante (50, 0, 0): ", "b"),
                 "Ogni seconda mossa è giocata in modo teoricamente perfetto (50%). Poiché s = 0 e w = 0, non c'è alcun filtraggio degli errori."),
        ("para",
                 ("5 Avanzato (20, 1, 1): ", "b"),
                 "Sceglie la mossa teoricamente migliore il 20% delle volte, ma grazie a s = 1 e w = 1 non trascura né le proprie vittorie immediate né le minacce "
                 "dirette dell'avversario alla mossa successiva."),
        ("para",
                 ("6 Tattico (0, 3, 3): ", "b"),
                 "Non gioca mai la mossa teoricamente migliore (p = 0), ma gioca tatticamente attento: le vittorie forzate entro fino a 3 proprie mosse vengono giocate (w = 3) e "
                 "le sconfitte minacciose entro le successive 3 mosse dell'avversario vengono evitate (s = 3). Un avversario tatticamente ostico senza "
                 "visione strategica."),
        ("para",
                 ("7 Intermedio (50, 1, 1): ", "b"),
                 "Solido standard amatoriale: ogni seconda mossa perfetta (50%), uso affidabile delle vittorie immediate (w = 1) ed evitamento costante di errori diretti (s = 1)."),
        ("para", ("8 Impegnativo (55, 1, 1): ", "b"), "Si basa sul livello 7, ma gioca in modo completamente impeccabile in più della metà di tutte le mosse (55%)."),
        ("para",
                 ("9 Difficile (65, 1, 1): ", "b"),
                 "Con il 65% di mosse ottimali e una protezione affidabile contro gli errori diretti, un avversario serio per giocatori di club esperti."),
        ("para",
                 ("10 Molto difficile (70, 2, 2): ", "b"),
                 "Combina alta precisione (70%) con istinto tattico: riconosce e para gli attacchi su 2 mosse dell'avversario (s = 2) e converte in modo affidabile le proprie "
                 "vittorie in 2 mosse (w = 2) – un ostacolo per i giocatori di torneo."),
        ("para",
                 ("11 Esperto (80, 2, 2): ", "b"),
                 "Gioca in modo impeccabile l'80% delle volte e para in modo affidabile gli attacchi su 2 mosse dell'avversario. Le proprie minacce di vittoria su 2 mosse "
                 "vengono convertite in sicurezza; la porta d'ingresso alle classi dei maestri."),
        ("para",
                 ("12 Maestro (85, 3, 3): ", "b"),
                 "Gioca molto forte (85% mosse migliori) con protezioni tattiche di ampia portata: vede minacce e propri percorsi vincenti su 3 mosse (s = 3, w = 3). "
                 "Persino giocatori di torneo esperti qui fanno ben pochi punti."),
        ("para",
                 ("13 Maestro forte (92, 4, 4): ", "b"),
                 "Quasi infallibile (92% mosse migliori): evita varianti perdenti forzate fino a 4 mosse in avanti (s = 4) e converte in sicurezza le proprie vittorie su 4 mosse (w = 4)."),
        ("para",
                 ("14 Perfetto (100, -, -): ", "b"),
                 "Gioca in modo impeccabile secondo le leggi del gioco risolto: come primo giocatore (Giallo) il motore vince ogni partita per forza; come secondo giocatore "
                 "(Rosso) sfrutta ogni imprecisione dell'avversario per prendere il punto intero. Le mosse equivalenti vengono variate statisticamente (vedi ",
                 ("Mosse pari", "b"),
                 " sopra). Per allenare il proprio gioco si raccomanda l'analisi della posizione, vedi ",
                 ("LINK", "Analisi", "wertung"),
                 "."),
        ("para",
                 "Valori di orientamento per la forza di gioco relativa (determinati in tornei motore contro motore con un totale di 18.200 partite – 200 partite per "
                 "abbinamento – con scambio continuo dei colori; base di riferimento livello Casuale = 1000 Elo): 1 Casuale, 2 Molto facile ~1204, 3 Facile ~1340, 4 "
                 "Principiante ~1431, 5 Avanzato ~1498, 6 Tattico ~1614, 7 Intermedio ~1702, 8 Impegnativo ~1752, 9 Difficile ~1817, 10 Molto difficile ~1929, 11 Esperto "
                 "~2010, 12 Maestro ~2080, 13 Maestro forte ~2132, 14 Perfetto ~2174. Nelle partite contro avversari umani queste differenze possono spostarsi "
                 "psicologicamente e tatticamente. La tabella delle forze e la tabella incrociata sono riportate per intero nella sezione ",
                 ("LINK", "“Forza di gioco e tabella incrociata”", "elorang"),
                 "."),
        ("head", "elorang", "Forza di gioco e tabella incrociata"),
        ("para",
                 "Tutti i 91 abbinamenti sono stati giocati con 200 partite ciascuno e scambio dei colori (18.200 in totale). Base di riferimento livello Casuale = 1000 Elo (relativo, "
                 "non Elo FIDE)."),
        ("para", ("Forza di gioco (Elo):", "b")),
        ("mono",
                 " 1 Casuale                   1000\n"
                 " 2 Molto facile   (25,0,0)   1204\n"
                 " 3 Facile         (40,0,0)   1340\n"
                 " 4 Principiante   (50,0,0)   1431\n"
                 " 5 Avanzato       (20,1,1)   1498\n"
                 " 6 Tattico        (0,3,3)    1614\n"
                 " 7 Intermedio     (50,1,1)   1702\n"
                 " 8 Impegnativo    (55,1,1)   1752\n"
                 " 9 Difficile      (65,1,1)   1817\n"
                 "10 Molto difficile (70,2,2)  1929\n"
                 "11 Esperto        (80,2,2)   2010\n"
                 "12 Maestro        (85,3,3)   2080\n"
                 "13 Maestro forte  (92,4,4)   2132\n"
                 "14 Perfetto       (100,-,-)  2174"),
        ("para", ("Tabella incrociata (punti del livello di riga contro il livello di colonna, su 200):", "b")),
        ("table", "kreuz14"),
        ("sub", "zugwahl", "Dietro le quinte: la scelta della mossa in 3 passi"),
        ("para",
                 ("Così il motore decide ogni singola mossa (livelli 1–14): ", "b"),
                 "Ogni mossa passa attraverso una catena di decisione fissa in tre passi. Spiega l'intero intreccio di forza di gioco, filtri e paradossi apparenti:"),
        ("para",
                 ("1. Prima la priorità alle vittorie (w) – senza dadi: ", "b"),
                 "Se la posizione offre una vittoria forzata entro ",
                 ("w", "b"),
                 " proprie mosse, quella mossa viene giocata subito – persino prima della ",
                 ("p", "b"),
                 " decisione casuale. ",
                 ("w = 1", "b"),
                 " significa una vittoria immediata. ",
                 ("w = 2", "b"),
                 " significa una vittoria in al massimo 2 mosse. ",
                 ("w = 3", "b"),
                 " significa una vittoria in fino a 3 mosse. ",
                 ("(w = 0 disattiva questa previsione.)", "b"),
                 " Solo se non c'è una tale breve vittoria segue il passo 2."),
        ("para",
                 ("2. L'estrazione di p (perfetta o errore): ", "b"),
                 "Per ogni mossa, isolatamente e senza memoria, la probabilità ",
                 ("p", "b"),
                 " decide se il motore gioca bene o in modo debole. ",
                 "Con ",
                 ("p = 50", "b"),
                 " (Principiante, Intermedio) statisticamente ogni seconda mossa è perfetta. ",
                 "Con ",
                 ("p = 20", "b"),
                 " (Avanzato) solo ogni quinta. ",
                 "Con ",
                 ("p = 80", "b"),
                 " (Esperto) quattro su cinque. ",
                 "Le serie sono puro caso: persino con ",
                 ("p = 50", "b"),
                 " possono capitare tre errori di fila – o tre mosse perfette."),
        ("para",
                 ("3a. Estratta perfetta: miglior punteggio e regola dei 10 ply: ", "b"),
                 "Il motore sceglie direttamente tra le mosse teoricamente migliori: ",
                 "tra più mosse vincenti ugualmente buone viene giocata la più veloce entro 10 ply; tra più mosse ugualmente veloci ne viene scelta una a caso. "
                 "Se nessuna vittoria è entro 10 ply, ne viene scelta una a caso tra tutte le restanti mosse vincenti (tutte allora a più di 10 ply di distanza). "
                 "Se ci sono solo pareggi, ne viene scelto uno a caso. "
                 "Se ci sono solo mosse perdenti, vale la regola delle sconfitte (resistenza più lunga, ponderata – con protezione a 10 ply al Perfetto)."),
        ("para",
                 ("3b. Estratto errore: la routine degli errori: ", "b"),
                 "Non è un lancio cieco di dadi, ma una mossa filtrata: ",
                 "il filtro ",
                 ("s", "b"),
                 " blocca tutte le mosse dopo le quali l'avversario vincerebbe in al massimo ",
                 ("s", "b"),
                 " mosse (",
                 ("s = 1", "b"),
                 " vieta errori diretti alla mossa successiva; ",
                 ("s = 0", "b"),
                 " non filtra nulla). "
                 "Tra tutte le restanti mosse consentite ne viene scelta una ",
                 ("uniformemente a caso", "b"),
                 " – un pareggio qui non è preferito, conta come qualsiasi altra mossa ammissibile. ",
                 ("Casi speciali: ", "b"),
                 ("p = 100", "b"),
                 " (Perfetto) va sempre a 3a. ",
                 ("p = 0", "b"),
                 " (Tattico) va sempre a 3b. ",
                 ("s = 0, w = 0", "b"),
                 " (livelli 1–4) sceglie in 3b in modo completamente non filtrato."),
        ("sub", "filterparadox", "Il paradosso dei filtri: Tattico contro Principiante (149,5 : 50,5)"),
        ("para",
                 "In un duello diretto, il livello ",
                 ("6 Tattico (0, 3, 3)", "b"),
                 " batte ",
                 ("4 Principiante (50, 0, 0)", "b"),
                 " nettamente, per quasi 3 : 1, sebbene il Tattico non giochi una sola mossa perfetta. "
                 "La ragione sta nell'intreccio di ",
                 ("scudo e spada", "b"),
                 ": "
                 "grazie a ",
                 ("s = 3", "b"),
                 " il Tattico regala quasi nulla con rapidi errori. "
                 "E grazie a ",
                 ("w = 3", "b"),
                 " converte ogni vittoria disponibile in 1–3 mosse. "
                 "Il Principiante invece butta via i suoi vantaggi di apertura con errori diretti non filtrati (",
                 ("s = 0", "b"),
                 ") e, mancando di priorità alle vittorie (",
                 ("w = 0", "b"),
                 "), lascia spesso impuniti gli errori dell'avversario. "
                 "Lo stesso principio si vede con ",
                 ("5 Avanzato (20, 1, 1)", "b"),
                 ", che batte il Principiante per 137 : 63 nonostante una ",
                 ("p", "b"),
                 " molto più bassa."),
        ("sub", "spitzenumkehr", "L'inversione al vertice: punti contro i maestri"),
        ("para",
                 "Contro gli avversari più forti (Maestro forte e Perfetto) il quadro si inverte: "
                 "qui, su 400 partite, il Principiante ottiene ",
                 ("7,0 punti", "b"),
                 " – il Tattico solo ",
                 ("0,5 punti", "b"),
                 " (un quattordicesimo). "
                 "Gli avversari forti non sbagliano praticamente mai. Né ",
                 ("s = 3", "b"),
                 " né ",
                 ("w = 3", "b"),
                 " aiutano molto, perché il maestro offre a malapena un bersaglio. "
                 "Per fare punti contro maestri quasi impeccabili servono mosse perfette con un piano strategico profondo – protezione contro le sconfitte o priorità "
                 "alle vittorie a corto raggio non bastano. Il Principiante gioca perfetta circa ogni seconda mossa; ogni tanto una di esse basta per un pareggio. Il Tattico non ha tali "
                 "mosse."),
        ("head", "datei", "Menu File"),
        ("para",
                 ("Nuova partita: ", "b"),
                 "Ripristina la scacchiera sulla posizione iniziale vuota. ",
                 ("Nuova con posizione casuale…: ", "b"),
                 "Crea una posizione di mediogioco costruita a caso con da 1 a 9 pietre, su richiesta con un esito teorico garantito (vittoria, pareggio o "
                 "sconfitta). ",
                 ("Carica posizione… ", "b"),
                 "e ",
                 ("Salva posizione…: ", "b"),
                 "Aprono una finestra di dialogo file standard per il formato universale ",
                 (".4gp", "b"),
                 ". Una partita salvata consiste nella stringa cronologica di cifre delle colonne scelte, come ",
                 ("4433221", "b"),
                 ". ",
                 ("Salvataggio rapido (F3) ", "b"),
                 "e ",
                 ("Caricamento rapido (F4): ", "b"),
                 "Salvano il record della partita corrente direttamente nel file o lo caricano dal file ",
                 ("quicksave.4gp", "b"),
                 " nella cartella principale del programma, senza finestra intermedia. ",
                 ("Esci: ", "b"),
                 "Chiude ConnectFour Studio correttamente."),
        ("head", "kommandos", "Menu Comandi"),
        ("para",
                 ("Prima / ultima mossa (freccia su / freccia giù): ", "b"),
                 "Salta all'inizio o alla fine della partita; le mosse ritirate restano in memoria e possono essere rigiocate in qualsiasi momento. ",
                 ("Mossa indietro / avanti: ", "b"),
                 "Scorre la partita passo passo (come i pulsanti ",
                 ("<", "b"),
                 " e ",
                 (">", "b"),
                 "). ",
                 ("Mossa (computer): ", "b"),
                 "Corrisponde alla scorciatoia ",
                 ("F5", "b"),
                 ". ",
                 ("Valuta tutte le mosse (1x): ", "b"),
                 "Corrisponde a ",
                 ("F6", "b"),
                 " (vedi ",
                 ("LINK", "riga di valutazione", "wertung"),
                 "). ",
                 ("Analisi permanente: ", "b"),
                 "Corrisponde a ",
                 ("F7", "b"),
                 " (vedi ",
                 ("LINK", "menu Vista", "ansicht"),
                 ")."),
        ("head", "ansicht", "Menu Vista"),
        ("para",
                 ("Pietra fantasma: ", "b"),
                 "Attiva o disattiva l'anteprima semitrasparente di caduta. ",
                 ("Animazione di caduta: ", "b"),
                 "Controlla il movimento fluido di caduta delle pietre lasciate cadere. ",
                 ("Mostra ultima mossa: ", "b"),
                 "Attiva o disattiva l'anello marcatore bianco sull'ultima pietra. ",
                 ("Punteggio on/off ", "b"),
                 "e ",
                 ("Azzera punteggio: ", "b"),
                 "Corrispondono ai pulsanti dell'",
                 ("LINK", "area punteggio", "spielstand"),
                 ". La finestra di aiuto può essere aperta in qualsiasi momento tramite il menu o con ",
                 ("F1", "b"),
                 "."),
        ("head", "info", "Riquadro info, A chi tocca e barra di stato"),
        ("para",
                 "In alto a destra, il riquadro ",
                 ("A chi tocca", "b"),
                 " mostra, tramite il simbolo della pietra e il nome, a chi tocca muovere: ",
                 ("Umano", "b"),
                 " o il motore, indicando il livello attivo (per esempio “User (1) (70,1,1)”). Nella modalità a due giocatori qui viene sempre mostrato Umano."),
        ("para", "Subito sotto, il ", ("riquadro Info", "b"), " fornisce cifre chiave sulla situazione corrente sulla scacchiera:"),
        ("para", ("Mossa: ", "b"), "Numero progressivo della prossima semimossa (a partire da 1)."),
        ("para", ("Livello: ", "b"), ("LINK", "livello", "stufen"), " attivo del motore (nella modalità torneo, il livello del colore a cui tocca muovere)."),
        ("para",
                 ("Profondità: ", "b"),
                 "Ultima profondità di ricerca raggiunta in ply. ",
                 ("Completa: ", "b"),
                 "Calcolo completo fino alla fine della partita. ",
                 ("Libro 12d: ", "b"),
                 "Fino a 12 pedine la ricerca si ferma non appena ogni variante raggiunge il libro di aperture: i valori sono esatti. ",
                 ("Libro 2d: ", "b"),
                 "Posizione con al massimo due pedine: valori esatti dal mini-libro integrato, senza alcuna ricerca. Puntini di sospensione finali (p. es. “8...”) mostrano un approfondimento ancora in corso. Un trattino (–) significa "
                 "che non è ancora disponibile alcun calcolo."),
        ("para",
                 ("Valore: ", "b"),
                 "Valutazione teorica dell'ultima mossa in notazione compatta – per esempio “Giallo (31)”, “Rosso (28)” o “Pareggio (40)”. L'etichetta indica la parte "
                 "vincente con gioco ottimale da entrambe le parti. Il numero tra parentesi è il numero di pietre ancora da mettere fino alla decisione finale: numeri piccoli "
                 "(1–6) segnalano una decisione imminente – un ",
                 ("1", "b"),
                 " tra parentesi segna la vittoria diretta immediata alla mossa successiva. Valori alti (30–42) indicano un lungo finale (42 sarebbe un pareggio dalla posizione vuota). "
                 "A ogni mossa giocata, questo valore scende di 1. Il numero di distanza sotto il simbolo nella ",
                 ("LINK", "riga di valutazione", "wertung"),
                 " dopo un'analisi (",
                 ("F6", "b"),
                 "/",
                 ("F7", "b"),
                 ") mostra lo stesso conteggio di pietre per colonna. Prima della prima analisi appare un trattino (–). Dopo che la partita è finita, qui viene "
                 "annunciato il risultato finale, per esempio “il Giallo vince!”."),
        ("para",
                 ("Nodi: ", "b"),
                 "Numero di posizioni cercate nell'albero di ricerca (feedback in tempo reale dal nucleo C++, con separatori delle migliaia leggibili). ",
                 ("Tempo: ", "b"),
                 "Puro tempo di calcolo dell'ultima analisi in millisecondi. ",
                 ("Velocità: ", "b"),
                 "Velocità di ricerca in nodi al secondo (per esempio 2,3 M/s = 2,3 milioni di posizioni/s). Tutti i valori si riferiscono all'ultimo passo di calcolo."),
        ("para",
                 ("Fonte: ", "b"),
                 "Origine dei dati della posizione: ",
                 ("Libro 12d", "b"),
                 " = consultazione nel libro di aperture integrato (fino a una profondità di 12 pietre), ",
                 ("calcolato", "b"),
                 " = calcolo libero in tempo reale del motore. Un trattino (–) indica lo stato iniziale prima dell'inizio della ricerca."),
        ("para",
                 "La ",
                 ("barra di stato", "b"),
                 " sul bordo inferiore della finestra riporta le mosse giocate (p. es. “Il computer ha giocato 4 in 0,35 s”), i resoconti di analisi e le operazioni sui file. Mentre è "
                 "in corso un calcolo, mostra “Il computer sta ancora pensando – attendere.” Un tentativo di caricamento durante la ricerca viene respinto con il messaggio "
                 "“Il computer sta ancora pensando – fermalo prima, poi carica.” In tal caso il calcolo deve prima essere interrotto con la funzione di stop."),
        ("head", "einstellungen", "Menu Impostazioni"),
        ("para",
                 "Il menu ",
                 ("Impostazioni", "b"),
                 " raggruppa le opzioni centrali: ",
                 ("Livello computer", "b"),
                 " (imposta la forza di gioco dal livello ",
                 ("LINK", "0 a 14", "stufen"),
                 "; può essere cambiato anche durante una partita in corso – il ",
                 ("LINK", "punteggio", "spielstand"),
                 " dopo una modifica ricomincia da 0–0), ",
                 ("Umano-Computer", "b"),
                 " (una partita contro l'intelligenza artificiale), ",
                 ("2 giocatori (entrambi umani)", "b"),
                 " (due persone giocano l'una contro l'altra; il programma assume la funzione di arbitro e la visualizzazione), ",
                 ("Computer-Computer (gioca)", "b"),
                 " (il motore gioca entrambi i lati dalla posizione corrente, vedi ",
                 ("LINK", "modalità di gioco", "gegner"),
                 "), ",
                 ("Incontro Computer-Computer", "b"),
                 " (configura partite e tornei automatici, vedi ",
                 ("LINK", "modalità di gioco", "gegner"),
                 "), ",
                 ("Interrompi gioco automatico", "b"),
                 " (ferma immediatamente un incontro in corso; il risultato parziale viene conservato) e ",
                 ("Set di pietre", "b"),
                 " (scelta tra 20 design di scacchiera e pietre; si può anche sfogliare con la rotella del mouse sulla scacchiera o con i tasti PagSu / PagGiù)."),
        ("head", "sprache", "Scegliere la lingua"),
        ("para",
                 "Nel menu ",
                 ("Aiuto", "b"),
                 " sotto ",
                 ("Lingua", "b"),
                 " sono elencate le lingue disponibili: ",
                 ("Deutsch", "b"),
                 ", ",
                 ("English", "b"),
                 ", ",
                 ("Français", "b"),
                 ", ",
                 ("Español", "b"),
                 ", ",
                 ("Nederlands", "b"),
                 " e ",
                 ("Italiano", "b"),
                 ". La selezione (un pulsante radio) ha effetto immediato per Aiuto e Info."),
        ("head", "engine", "Motore e libro di aperture"),
        ("para",
                 "Il nucleo di calcolo matematico è ",
                 ("BitBully by Markus Thill", "b"),
                 " – un efficiente modulo Python con nucleo C++. Usa bitboard ottimizzate, approfondimento iterativo con algoritmo di ricerca MTD(f)/null-window "
                 "e tabelle di trasposizione dinamiche. Il libro di aperture integrato ",
                 ("12-ply-dist", "b"),
                 " fornisce valutazioni teoriche e valori di distanza esatti per tutte le posizioni con fino a 12 pietre messe; nelle varianti più profonde il motore di ricerca "
                 "prosegue il calcolo."),
        ("para",
                 "ConnectFour Studio combina un'interfaccia desktop snella (Python, Tkinter, resa grafica con Pillow) con un gioco risolto. Concesso in licenza come software libero sotto la ",
                 ("GNU Affero General Public License (AGPL v3)", "b"),
                 "."),
        ("head", "tasten", "Scorciatoie da tastiera"),
        ("para",
                 ("1–7", "b"),
                 " = fare una mossa di colonna · ",
                 ("Freccia sinistra / freccia destra", "b"),
                 " = ritirare / rigiocare una mossa · ",
                 ("Freccia su / freccia giù", "b"),
                 " = saltare all'inizio / alla fine della partita · ",
                 ("PagSu / PagGiù o rotella del mouse sulla scacchiera", "b"),
                 " = cambiare set di pietre · ",
                 ("F1", "b"),
                 " = aprire la finestra di aiuto · ",
                 ("F3 / F4", "b"),
                 " = salvataggio / caricamento rapido · ",
                 ("F5", "b"),
                 " = far muovere il motore · ",
                 ("F6", "b"),
                 " = analisi unica della posizione · ",
                 ("F7", "b"),
                 " = attivare o disattivare l'",
                 ("LINK", "analisi permanente", "buttons"),
                 " · ",
                 ("Escape", "b"),
                 " = chiudere un menu aperto. Nota: le scorciatoie funzionano finché il focus di input non è in un campo di testo."),

    ],
}
