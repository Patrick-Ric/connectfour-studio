"""Stufen (p,s,w) + Turnier/Match + Spielstand + Zufalls-Dialog.

Ausgelagert 01.10.2026 aus connectfour_studio.py (dort nur noch dünne
Methoden-Stubs in der Klasse ConnectFourStudio).

Inhalt:
- Stufen-Tabellen: STUFEN_ORDER, STUFEN_LABELS, STUFEN (+ Verlierer-Key)
- User-p/s/w: USER_KEYS, Labels, Defaults (Klassenattribute der App,
  gelesen IMMER über Klassenattribute – NIEMALS self._user_psw, sonst
  Instanz-Schatten-Bug 30.09.2026)
- Helfer (als Funktionen mit app-Parameter, kein Zirkelimport):
  user_psw_for, is_user_key, stufen_werte, stufe_key, stufe_label_for,
  display_stufe_label, move_stufe, apply_stufe, match_elo ...
- RandomDialog (Tk-Klasse, unverändert)
- Match-/Spielstand-Methoden als freie Funktionen mit app-Parameter:
  Die Klasse ConnectFourStudio bekommt dünne Stubs (eine Zeile je
  Methode), die hierher delegieren. Match-/Stand-State liegt weiter
  auf der App (self._match, self._stand, ...), damit Threads und
  GUI-Variablen unverändert funktionieren.

Regel: dieses Modul importiert NIEMALS connectfour_studio (Zirkel!).
Alles App-spezifische kommt als `app`-Parameter herein.
"""

import tkinter as tk
from tkinter import ttk

import cfs_lang

# --- Stufen-Tabellen (Stand 03.10.2026, p,s,w), 14 Stufen ---
# p = % perfekte Zuege (Patzerquote = (100-p)/100);
# s = Verlustschutz in Gegnerzuegen (Patzer-Zug tabu, wenn ml <= 2*s);
# w = Siegsschutz (kurzer Gewinn mit ml <= 2*w-1 geht immer vor, Variante B).
# ml = untere Zahl (Gewinn-/Verlustdistanz aus eigener Sicht).
# 03.10.2026: finale 14er-Leiter (Ansteiger wieder raus, Nummern 6-15 -> 5-14;
# Starker Meister (88,3,3) gestrichen; Weltklasse heisst Starker Meister).
STUFEN_ORDER = ("verlierer", "zufall", "sehr_leicht", "leicht", "anfaenger",
                "fortgeschritten", "taktiker", "mittel", "fordernd",
                "schwer", "sehr_schwer", "experte", "meister",
                "starker_meister", "perfekt")
STUFEN_LABELS = {"verlierer": "0 Verlierer",
                 "zufall": "1 Zufall",
                 "sehr_leicht": "2 Sehr Leicht", "leicht": "3 Leicht",
                 "anfaenger": "4 Anfänger",
                 "fortgeschritten": "5 Fortgeschritten",
                 "taktiker": "6 Taktiker", "mittel": "7 Mittel",
                 "fordernd": "8 Fordernd", "schwer": "9 Schwer",
                 "sehr_schwer": "10 Sehr Schwer",
                 "experte": "11 Experte", "meister": "12 Meister",
                 "starker_meister": "13 Starker Meister",
                 "perfekt": "14 Perfekt"}


def level_label(key):
    """Stufen-Anzeigename 'Nr Name' in der aktiven Sprache (Fallback 14
    Perfekt). STUFEN_LABELS bleibt die deutsche Referenz."""
    if key not in STUFEN_ORDER:
        key = "perfekt"
    return f"{STUFEN_ORDER.index(key)} {cfs_lang.level_name(key)}"


STUFEN = {
    "zufall": ("1 Zufall", 0, 0, 0),
    "sehr_leicht": ("2 Sehr Leicht", 25, 0, 0),
    "leicht": ("3 Leicht", 40, 0, 0),
    "anfaenger": ("4 Anfänger", 50, 0, 0),
    "fortgeschritten": ("5 Fortgeschritten", 20, 1, 1),
    "taktiker": ("6 Taktiker", 0, 3, 3),
    "mittel": ("7 Mittel", 50, 1, 1),
    "fordernd": ("8 Fordernd", 55, 1, 1),
    "schwer": ("9 Schwer", 65, 1, 1),
    "sehr_schwer": ("10 Sehr Schwer", 70, 2, 2),
    "experte": ("11 Experte", 80, 2, 2),
    "meister": ("12 Meister", 85, 3, 3),
    "starker_meister": ("13 Starker Meister", 92, 4, 4),
    "perfekt": ("14 Perfekt", 100, None, None),
}

USER_KEYS = ("user1", "user2")
USER_LABEL_1 = "User (1)"
USER_LABEL_2 = "User (2)"
# Defaults; ECHTE Werte liegen als Klassenattribute auf der App
# (ConnectFourStudio._user_psw_1/_user_psw_2), damit Worker-Threads
# ohne Tk-Variablen lesen koennen.
USER_PSW_DEFAULT = (50, 1, 1)

MATCH_STUFEN = ("mensch", "verlierer", "zufall", "sehr_leicht", "leicht", "anfaenger",
                "fortgeschritten", "taktiker", "mittel", "fordernd",
                "schwer", "sehr_schwer", "experte", "meister",
                "starker_meister", "perfekt", "user1", "user2")


def _psw_of(app, key):
    """(p,s,w) zur User-Seite: IMMER Klassenattribute lesen
    (type(app)._user_psw_1/_user_psw_2, Fallback Defaults) – NIEMALS
    self._user_psw (Instanz-Schatten-Bug 30.09.2026)."""
    try:
        cls = type(app)
        if key == "user1":
            psw = cls._user_psw_1
        elif key == "user2":
            psw = cls._user_psw_2
        else:
            psw = getattr(cls, "_user_psw", USER_PSW_DEFAULT)
        p, s, w = int(psw[0]), int(psw[1]), int(psw[2])
        return (max(0, min(100, p)), max(0, min(9, s)), max(0, min(9, w)))
    except Exception:
        return USER_PSW_DEFAULT


def user_psw_for(app, key):
    return _psw_of(app, key)


def is_user_key(key):
    try:
        return key in USER_KEYS
    except Exception:
        return key in ("user1", "user2")


def stufen_werte(app, key):
    """(key, patzerquote, s, w) zu einem Stufenschluessel. Siehe Modul-Doc."""
    if key == "mensch":
        return "mensch", 0.0, None, None
    if key == "verlierer":
        return "verlierer", 1.0, 0, 0
    if key in ("user1", "user2"):
        p, s, w = _psw_of(app, key)
        try:
            q = (100 - max(0, min(100, int(p)))) / 100.0
        except Exception:
            q = 0.5
        return key, max(0.0, min(1.0, q)), s, w
    try:
        dat = STUFEN.get(key)
    except Exception:
        dat = None
    if not dat:
        return "perfekt", 0.0, None, None
    _label, p, s, w = dat
    try:
        q = (100 - int(p)) / 100.0
    except Exception:
        q = 0.0
    if q < 0.0:
        q = 0.0
    if q > 1.0:
        q = 1.0
    return key, q, s, w


def stufe_key(app):
    """Stufenschluessel thread-sicher lesen (Tk nur im Hauptthread)."""
    try:
        if app.two_player:
            v = "mensch"
        else:
            v = app.depth_var.get()
    except Exception:
        v = getattr(app, "_stufe_cache", "perfekt")
    if v == "mensch":
        return v
    return v if (v in STUFEN or v in ("user1", "user2", "verlierer")) else "perfekt"


def stufe_label_for(app, key, mit_psw=False):
    """Stufen-Anzeigename zu einem Schluessel (fuer Match etc.)."""
    try:
        if key == "mensch":
            return cfs_lang.t("level_human")
        if key == "verlierer":
            return level_label("verlierer")
        if key == "user1":
            p, s, w = _psw_of(app, "user1")
            try:
                lbl1 = app._USER_LABEL_1
            except Exception:
                lbl1 = USER_LABEL_1
            name = f"{lbl1} ({p},{s},{w})"
            return name if mit_psw else lbl1
        if key == "user2":
            p, s, w = _psw_of(app, "user2")
            try:
                lbl2 = app._USER_LABEL_2
            except Exception:
                lbl2 = USER_LABEL_2
            name = f"{lbl2} ({p},{s},{w})"
            return name if mit_psw else lbl2
        name = level_label(key)
        if mit_psw and key not in ("perfekt", "verlierer", "zufall"):
            try:
                dat = STUFEN.get(key)
            except Exception:
                dat = None
            if dat:
                _label, p, s, w = dat
                s_txt = "-" if s is None else str(s)
                w_txt = "-" if w is None else str(w)
                return f"{name} ({p},{s_txt},{w_txt})"
        return name
    except Exception:
        return level_label("perfekt")


def stufe_label(app):
    try:
        v = app.depth_var.get()
    except Exception:
        v = getattr(app, "_stufe_cache", "perfekt")
    return stufe_label_for(app, v)


def move_stufe(app):
    """(stufe_key, patzerquote, s, w) fuer den GERADE zu spielenden Zug."""
    m = getattr(app, "_match", None)
    if m is not None and not m.get("fertig", False):
        try:
            key = app._match_side_stufe()
        except Exception:
            key = "perfekt"
        return stufen_werte(app, key)
    try:
        ms = app._match_stufe
    except Exception:
        ms = None
    if ms == "mensch" or ms in ("user1", "user2") or ms == "verlierer" or ms in STUFEN:
        return stufen_werte(app, ms)
    key = stufe_key(app)
    return stufen_werte(app, key)


def display_stufe_label(app):
    """Stufen-Name fuer die Infobox (Match: Seite am Zug)."""
    try:
        if app._match_mode():
            return stufe_label_for(app, app._match_side_stufe())
    except Exception:
        pass
    try:
        ms = getattr(app, "_match_stufe", None)
        if ms == "mensch" or ms in ("user1", "user2") or ms == "verlierer" or ms in STUFEN:
            return stufe_label_for(app, ms)
    except Exception:
        pass
    return stufe_label(app)


def apply_stufe(app):
    """Engine-Staerke anwenden (Cache + depth_var + agent + Infobox)."""
    v = stufe_key(app)
    try:
        app._stufe_cache = v
        app.depth_var.set(v)
    except Exception:
        pass
    _key, err, _s, _w = stufen_werte(app, v)
    app.agent.max_depth = -1
    app.error_rate = err
    try:
        app.info_vars["Stufe"].set(stufe_label(app))
    except Exception:
        pass


def match_elo(punkte_gelb, partien):
    """Elo-Differenz aus Gelb-Sicht (-400*log10((1-p)/p)), 0/100% -> +/-2000."""
    if partien <= 0:
        return None
    p = punkte_gelb / partien
    if p <= 0.0:
        return -2000.0
    if p >= 1.0:
        return 2000.0
    import math as _m
    import decimal as _d
    raw = -400.0 * _m.log10((1.0 - p) / p)
    return float(_d.Decimal(str(raw)).quantize(
        _d.Decimal("1"), rounding=_d.ROUND_HALF_UP))


class RandomDialog(tk.Toplevel):
    """Steinzahl (1-9) + Wunsch-Ergebnis waehlen."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title(cfs_lang.t("new_random_title"))
        self.result = None
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text=cfs_lang.t("new_random_stones")).grid(row=0, column=0, sticky="w")
        self.n_var = tk.IntVar(value=3)
        ttk.Spinbox(frm, from_=1, to=9, textvariable=self.n_var, width=5).grid(
            row=0, column=1, sticky="w")
        ttk.Label(frm, text=cfs_lang.t("new_random_result")).grid(row=1, column=0, sticky="w", pady=(6, 0))
        # Anzeige lokalisiert; Ergebnis bleibt der interne deutsche
        # Schluessel (Egal/Gewinn/Unentschieden/Verlust), den die
        # Zufalls-Suche der App auswertet.
        self._w_keys = [("Egal", cfs_lang.t("new_random_any")),
                        ("Gewinn", cfs_lang.t("new_random_win")),
                        ("Unentschieden", cfs_lang.t("new_random_draw")),
                        ("Verlust", cfs_lang.t("new_random_loss"))]
        self.w_var = tk.StringVar(value=self._w_keys[1][1])
        ttk.Combobox(frm, textvariable=self.w_var, width=14, state="readonly",
                     values=[lab for _k, lab in self._w_keys]).grid(row=1, column=1, sticky="w", pady=(6, 0))
        ttk.Label(frm, text=cfs_lang.t("new_random_hint"), foreground="grey").grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))
        btn = ttk.Frame(frm)
        btn.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btn, text="OK", command=self.ok).pack(side="left", padx=4)
        ttk.Button(btn, text=cfs_lang.t("btn_cancel"), command=self.destroy).pack(side="left", padx=4)
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)

    def ok(self):
        key = {lab: k for k, lab in self._w_keys}.get(self.w_var.get(), "Egal")
        self.result = (self.n_var.get(), key)
        self.destroy()
