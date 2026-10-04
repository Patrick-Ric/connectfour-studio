"""ConnectFour Studio GUI (Tkinter + BitBully-Engine).

Rechenmotor: BitBully von Markus Thill (Python-Modul bitbully, C++-Kern).
Lizenz: GNU AGPL v3 (BitBully-Paket) – dieses Programm ist Open Source.

Start:  python3 connectfour_studio.py [stellung.4gp]

Computer-Stufen (14), Kurzformat (p, s, w): p = % perfekte Zuege,
s = Verlustschutz in Gegnerzuegen (Filter, tabu wenn ml <= 2*s),
w = Siegsschutz (kurzer Gewinn mit ml <= 2*w-1 geht immer vor).
1 Zufall (0, 0, 0), 2 Sehr Leicht (25, 0, 0), 3 Leicht (40, 0, 0),
4 Anfaenger (50, 0, 0), 5 Fortgeschritten (20, 1, 1),
6 Taktiker (0, 3, 3), 7 Mittel (50, 1, 1),
8 Fordernd (55, 1, 1), 9 Schwer (65, 1, 1),
10 Sehr Schwer (70, 2, 2), 11 Experte (80, 2, 2),
12 Meister (85, 3, 3), 13 Starker Meister (92, 4, 4),
14 Perfekt (100, -, -).
Analyse (Alle/Dauer) IMMER perfekt.
Buch: fest 12-ply-dist (keine Auswahl).

Neu in v19:
- Ansicht: Ghost-Stein an/aus (Standard: an).
- Dauer-Analyse Standard: AUS (per Menue/Button zuschaltbar).
- Info-Dialog kopierbar (Text + Kopieren-Button statt Messagebox).
- Umbenannt: 'Engine-Stufe' -> 'Computer-Stufe', 'Engine' -> 'Computer'
  (Menue, Status, Hilfe).
- Neu: Computer-Computer (ausspielen) - spielt ab aktueller Stellung perfekt
  gegen sich selbst bis zum Ende (Stop Auto Play / Moduswechsel haelt an).
- Buttons: wieder 7 einzeilig (Neu, Zufall, <, >, Ziehen, Alle, Analyse);
  Stop nur als 'Stop Auto Play' unter Kommandos (kein Designwechsel).
- KRITISCH: Thread-Tod behoben - Tk-Variablen duerfen NICHT aus Workern
  gelesen/gesetzt werden (RuntimeError). _safe_after nutzt Queue + Poll,
  _iterative_scores hat getrennte Abbruchkennungen (Engine: cancel-Flag,
  Analyse: _ana_seq), prog-Callback baut nur reine Python-Werte.


Start:  python3 connectfour_studio.py [stellung.4gp]

Engine-Stufen (14), Kurzformat (p, s, w) wie oben:
1 Zufall (0, 0, 0), 2 Sehr Leicht (25, 0, 0), 3 Leicht (40, 0, 0),
4 Anfaenger (50, 0, 0), 5 Fortgeschritten (20, 1, 1),
6 Taktiker (0, 3, 3), 7 Mittel (50, 1, 1),
8 Fordernd (55, 1, 1), 9 Schwer (65, 1, 1),
10 Sehr Schwer (70, 2, 2), 11 Experte (80, 2, 2),
12 Meister (85, 3, 3), 13 Starker Meister (92, 4, 4),
14 Perfekt (100, -, -).
Analyse (Alle/Dauer) IMMER perfekt.
Buch: fest 12-ply-dist (keine Auswahl).

Neu in v18:
- 1-Zueger-Filter umgebaut: statt moves_left-Semantik (mehrdeutig) wird
  ECHT simuliert - nach jedem Patzer-Kandidaten werden ALLE Gegnerzuege auf
  sofortiges Matt (is_game_over) geprueft. Verifiziert: Leicht/Mittel spielen
  an der Drohstellung nur noch Sp.4 (Block) + Sp.7 (Remis), nie 1-zuegige
  Patzer. Sehr Leicht weiter ungefiltert.
- Schwer-Filter (2-zuegig): Restdistanz moves_left<=4 tabu (Fehler davor:
  moves_left=2 wurde mit Halbzuegen verwechselt).
- Zufallsdialog-Default: 3 Steine + Gewinn. Info/Hilfe: GNU AGPL v3.
- Layout: Holder-Reihe weight=1 (Brettbereich nutzt Fensterhoehe), Boardbox
  klebt oben, Statuszeile weight=0 am Fensterrand -> kein Graufeld unter den
  Buttons. Zoom: Breite aus Fenster, Hoehe aus Holder (keine Spirale).
- Hilfe-Links: eindeutige Tags (jeder Link klickt), Anker als Textmarken.
- Info/Hilfe: ConnectFour Studio, Open Source (GNU AGPL v3).
  (Neuprogrammierung), Open Source.

Neu in v15 (4 echte Bugfixes hinter 'ohne Buch friert ein'):
- 'Alle' (refresh) lief VOLLSUCHE (-1) im GUI-Thread -> minutenlanger Freeze
  ohne Buch. Jetzt iterativ wie die Analyse.
- Engine-Zug rief best_move (Vollsuche) nach den Stufen -> wieder Minuten
  ohne Buch. Jetzt: bester Zug der letzten Stufe (Sekunden statt Minuten).
- Ohne Buch nur bis Tiefe 12 (0,2 s); 14+ nur mit Buch (Minuten-Lock).
- after_human pruefte startswith('Engine') -> Menue-Label 'Engine (Stufe N)'
  erfuellte das nie -> Engine antwortete nach Mensch-Zug gar nicht. Jetzt ==.
- Dazu: iterative Vertiefung (4,6,8,...) mit Live Tiefe/kKn/Zeit im Info-
  Fenster wie ein Schachprogramm; Stop/Neuzug bricht zwischen Stufen ab;
  Checkbox-Variable direkt am Menueeintrag (war entkoppelt -> Analyse lief
  trotz 'aus'); Callbacks ausserhalb Solver-Lock (Deadlock); GUI-Throttle.

Neu in v12 (Basis):
- Stufe 1 spielt wirklich schwach: Patzerquote DIREKT am Zuganfang
  (uniform-zufaellig, blockt Drohungen oft nicht). 40x leer: ~82% Patzer.
- Boards kleben unten (sticky sw): kein Leerfeld ueber der Statuszeile.
- Nach Engine-Zug: echte Knoten/Zeit/Tempo aus der Zugberechnung, auch bei
  Analyse-aus (keine Zwangsbewertung, nur Kennzahlen).
- F4/laden startet keine Analyse mehr; 'default' heisst '12-ply-dist
  (Standard, mit Zugzahl)' + 'ohne Buch'; Ziehen = F5.
- Unterschied 12-ply vs 12-ply-dist: dist hat zusaetzlich die Zugzahl bis
  Gewinn/Verlust (braucht die Score-Zeile + Engine-Varianz).

Neu in v11 (Basis):
- Hash ehrlich: 'Buch 8/12/12d' nur im Buch-Horizont, danach 'Suche'.
- Tiefe ehrlich: 'Buch 8/12' statt Zug-1; danach 'Suche' (exakt bis Ende).
- kKn/Zeit/Tempo sind echte Live-Werte vom C++-Kern (keine Deko).
- Analyse-Button = Menue (Umschalter, synchron, kein Nachstart).
- F3/F4: Schnell speichern/laden ohne Dialog (quicksave.4gp).
- Perfekt als eigene Stufe ueber 12; Stufe in Infobox; Grauluecke unten weg.
- Gegen Computer keine Zwangsbewertung mehr bei Analyse-aus.

Neu in v10 (Basis):
- Layout FIX: Holder waechst nicht mit (weight=0) -> Infobox klebt direkt
  am Brett, keine Grauzone; Zoom aus FENSTER-Groesse (Fenster-Configure).
- 'Rot gewinnt!'/'Gelb gewinnt!' auch im Wert-Feld der Analyse
  ('Sp. X: Gelb gewinnt' / 'Sp. X: Rot gewinnt' / 'Sp. X: Unentschieden').
- Engine-Stufe 1-12 fliessend (12=perfekt); Menue zeigt 'Engine (Stufe N)'.
- Letzter Zug als Property (live aus history+board) -> immer korrekt.
- Thread-Callbacks mit Default-Args (kein NameError mehr); -1 statt None
  als 'unbegrenzt' (C++-Binding akzeptiert kein None).
Neu in v9 (Basis):
- Layout: Boardbox linksbuendig statt zentriert -> Infobox direkt am Brett,
  keine Grauflaeche; Zoom nutzt Fenster minus Infobreite (bis 4x).
- Wert bei Partieende: 'Rot gewinnt!'/'Gelb gewinnt!'.
- Einstellungen: Engine-Staerke (perfekt/12/8/6/4 via max_depth) +
  'Hashtabelle loeschen' (Groesse ist im BitBully-C++-Kern fix).
- Engine-Zug + Analyse respektieren die eingestellte Staerke.
Neu in v8:
- Am-Zuge nur noch "Spieler 1"/"Spieler 2" (Farbe zeigt der Stein).
- Score-Zeile: oben fett +,-,= passend zur Farbe, unten Zugzahl bis Ende.
- 'Alle' und 'Analyse' sind Umschalter: 2. Klick -> Zahlen 1-7 zurueck.
- Info ehrlich: exakte Knoten (1.234 statt 1 kKn), ms-Zeit, echte Knoten/s.
Neu in v7:
- Caption-Text ueber den Scores ersatzlos gestrichen.
- Brett-Groesse stabil: Score-Hoehe fix (44px), Button-Font fix (9pt) ->
  kein Feedback-Loop mehr (Zoom bleibt ueber Fenster und Zuege konstant).
- Sieg-Highlight: alle Steine einer 4er+-Reihe bekommen gruenen Doppelring.
- Buttons kuerzer beschriftet (<, >, Alle, Analyse) -> passen immer.
Neu in v6:
- Engine-Varianz bei reinen Verluststellungen: gewichtete Zufallswahl mit
  Gewicht = (Verlustlaenge ^ POWER, POWER=8). 5 vs 10 -> praktisch immer
  der lange Zug; 40 vs 39 -> ca. 50/50. Nur wenn ALLE Zuege verlieren.
- Layout: Brett-Canvas exakt auf Boardgroesse (kein Stretch -> kein dicker
  blauer Rand, highlightthickness=0), Zuege-Leiste + Buttons ohne padx im
  gleichen 7er-Uniform-Grid -> spaltenexakt. Buttons einzeilig, gleiche
  Schrift, keine Umbrueche -> gleichmaessig gross. Hash-Anzeige kurz.
Neu in v5:
- "alle Zuege" liegt UNTER dem Brett, spaltenexakt (zoomt mit), mit
  Trennlinien und anklickbar (Klick = Zug ausfuehren). Tasten 1-7 ebenso.
- Buttonleiste: genau 7 Buttons (Neu, Zufall, Zurueck, Vor, Ziehen,
  Alle Zuege, Dauer-An.), je eine Spaltenbreite, zoomen mit.
- Pfeiltasten links/rechts = Zug zurueck/vor.
- Info schmaler; darueber "Am Zuge"-Feld mit Stein + Spieler 1/2.
- Dauer-Analyse ohne Verzoegerung (sofort, neueste Stellung gewinnt).
- Hover-Farbe korrigiert (BitBully: 1=Gelb/Anziehender, 2=Rot; Brett hat
  vertauscht gezeichnet, Vorschau stimmte). Gewinnmeldung nennt Gelb/Rot.
- Ansicht fest auf Auto-Fenster (manueller Zoom + Themes entfernt).
- Gewinnsuche entfernt – "Alle Züge"/Dauer-Analyse übernimmt das.
Neu in v3:
- Auto-Zoom: Brett waechst/schrumpft automatisch mit dem Fenster
  (debounced <Configure>). Immer an, kein Schalter.
- Dauer-Analyse (v.a. 2-Spieler): nach jedem Stellungswechsel laeuft
  automatisch score_all_moves im Hintergrund (250 ms Debounce,
  Stellungs-ID gegen veraltete Ergebnisse). Schalter in Ansicht+Leiste.
Neu in v2:
- "Neu mit Zufallsstellung": Dialog mit Steinzahl (1-9) + Wunsch-Ergebnis
  (Gewinn / Unentschieden / Verlust aus Sicht des Spielers am Zug). Die Engine
  wuerfelt legale Stellungen und prueft sie per mtdf, bis Wunsch passt.
- Brett folgt der Fenstergroesse (Auto-Zoom, kein Schalter).
- "alle Zuege": Farbcodierung gruen=Gewinn, gelb=Unentschieden, rot=Verlust
  (helle Pastelltoene, schwarze Schrift bleibt lesbar).
- Drop-Animation: Stein faellt mit 60fps in die Spalte (abschaltbar).
- Hover-Vorschau: halbtransparenter Stein ueber der Zielspalte.
- Feiner Letzter-Zug-Rahmen statt klobigem Weiss-Rechteck.
- Statuszeile zeigt Engine + Buch (BitBully/Thill) an.

Engine-Hinweis: Der Rechenmotor IST BitBully (Markus Thill, C++-Kern mit
MTD(f)/Null-Window-Suche, Bitboards, Transposition Table + 12-ply-dist
Eroeffnungsbuch). Tkinter und diese Datei sind nur die GUI-Huelle drumherum.
"""
import os
import sys
import time
import queue
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

import bitbully as bb
import cfs_sets
import cfs_levels
import cfs_lang

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
ENGINE_NAME = "BitBully von Markus Thill"

# --- Sets (ausgelagert in cfs_sets, 01.10.2026): Konstanten werden
# re-exportiert, damit Rest-Code unveraendert funktioniert. ---
SET = cfs_sets.START_SET
SET_IDS = cfs_sets.SET_IDS
_SET_ORDER = cfs_sets._SET_ORDER
_MENU_SETS = cfs_sets._MENU_SETS
SET_NAMES = cfs_sets.SET_NAMES
DATA_DIR = cfs_sets.DATA_DIR


def set_menu_order(raw):
    """Menue-Reihenfolge der Sets: exakt _SET_ORDER (1-21)."""
    return cfs_sets.set_menu_order(raw)


def available_sets():
    return cfs_sets.available_sets()

COLS, ROWS = 7, 6

C_WIN = "#b8e6b8"    # gruen pastel: Gewinn
C_DRAW = "#fff3a0"   # gelb pastel: Unentschieden
C_LOSS = "#f5b8b8"   # rot pastel: Verlust

LOSS_POWER = 8  # Engine-Varianz: Gewicht = Verlustlaenge^POWER (nur wenn alles verliert)

BOARD_BG = "#1e3a8a"  # Brett-Blau, fest


RandomDialog = cfs_levels.RandomDialog


class ConnectFourStudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ConnectFour Studio")
        # Startsprache (04.10.2026): gespeicherte Wahl > Systemsprache
        # (en/* -> en, sonst de). Merken bei jedem Wechsel (lang.cfg).
        try:
            cfs_lang.set_lang(cfs_lang.detect_start_lang())
        except Exception:
            pass
        self.agent = bb.BitBully()
        self.agent.max_depth = -1  # -1 = unbegrenzt = Perfekt
        self.error_rate = 0.0  # Patzerquote Leicht/Mittel/Schwer (0.85/0.15/0.08)
        try:
            self.agent.load_book("12-ply-dist")  # fest verdrahtet
        except Exception:
            pass
        self.board = bb.Board()
        self.history = []          # gespielte Spalten 0..6
        self.future = []           # fuer Zug-vor
        self.two_player = False
        self.selfplay = False      # Computer-Computer (ausspielen) laeuft
        self._stufe_cache = "perfekt"  # thread-sicherer Stufen-Cache (Tk nur Hauptthread)
        # Normalmodus Mensch-Computer: WER zog zuerst? True = Mensch begann
        # (Normalfall: Mensch ist Gelb), False = Computer begann ('ziehen'
        # liess den Computer anfangen -> Mensch ist Rot). Bestimmt, wem der
        # Sieg im Spielstand gutgeschrieben wird (Bugfix 30.09.2026: vorher
        # war 'Gelb = Mensch' fest verdrahtet -> Rot-Siege des Menschen
        # wurden dem Computer gutgeschrieben). Reset in new_game/_load_moves.
        self._human_first = True
        # Match-Modus (Computer-Computer mit Stufen + Partiezahl): die Stufe
        # des ziehenden Spielers bestimmt _move_stufe() pro Zug (Gelb/Rot
        # getrennt einstellbar). _match = None oder dict(gelb, rot, spiele,
        # wechsel, nr, punkte_gelb, punkte_rot, remis, fertig). Thread-sicher:
        # Worker lesen NUR _match_stufe (reine Python-Werte, kein Tk).
        self._match = None
        self._match_stufe = None   # Stufe des gerade rechnenden Zugs
        self._match_after = None   # ausstehender Match-Weiter-Trigger
        self._match_win = None     # offenes Match-Fenster (Toplevel)
        self.thinking = False
        self.cancel = False
        self.rand_job = None       # fuer Zufallsstellung (Abbruch)
        self.set_no = SET if SET in SET_IDS else (SET_IDS[0] if SET_IDS else 3)
        self.show_last = True
        self.anim = True           # Drop-Animation an/aus
        self.ghost = True          # Ghost-Stein (Hover-Vorschau) an/aus
        self.anim_after = None
        # Natuerliche Startgroesse (Wunsch Patrick 30.09.2026): Kachel-
        # mass (256-px-HiRes) x Start-Zoom -> Brett in "natuerlicher"
        # Natuerliche Startgroesse, KEIN Vollbild. Danach
        # Auto-Zoom per Fenster-Resize (User/Maximieren) wie gehabt.
        self.zoom = 0.30
        self._resize_after = None
        # Start-Stabilisierung (Fix Schrumpf-Spirale): Fit-Sperre, bis das
        # Fenster erstmals sichtbar ist; danach genau EIN Start-Fit, dann
        # freigeben. Nur echter User-Resize (Fenstergroesse) loest Fits aus.
        self._startup = True
        self._fitting = False
        self._pending_shrink = False
        self._last_win_wh = (0, 0)
        self._was_zoomed = False  # Maximiert-Status (fuer Max/Unmax-Wechsel)
        self._shrink_veto_n = 0  # Zaehler: wiederholtes Selbst-Schrumpfen
        self._shrink_veto_t = 0.0
        self.hover_col = None
        # Dauer-Analyse: Hintergrund-Bewertung nach jedem Stellungswechsel
        # (Standard: AUS, per Menue/Button zuschaltbar).
        self.scores_visible = False  # True, sobald eine Bewertung angezeigt wird
        self.auto_analyze = False
        self._ana_seq = 0        # hochzaehlende Analyse-Anfrage (gegen Race)
        self._ana_busy = False
        self._ana_pending = None  # wartende Anfrage, falls Analyse noch laeuft
        self._ana_running_snap = None  # Stellung, die gerade berechnet wird
        self._last_depth = None  # zuletzt erreichte Iterationstiefe (Anzeige)
        self._solver_lock = threading.Lock()  # BitBully ist nicht threadsicher
        self.move_times = []
        # UI-Queue (Fix 01.10.2026, DeepSeek-Review Punkt 1): Worker-Threads
        # legen GUI-Callbacks hier ab (_safe_after); _ui_poll_tick arbeitet
        # sie im Main-Thread ab. _closed = Fenster zu -> verwerfen.
        self._ui_queue = queue.Queue()
        self._closed = False
        self._ui_tick_id = None
        try:
            self._ui_tick_id = self.after(30, self._ui_poll_tick)
        except Exception:
            pass
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        # Kachel-Rohdaten (PIL, via cfs_sets.SetArt), Zoom-Cache
        # (via cfs_sets.SetTiles). tile_cache bleibt als Kompat-Alias.
        self.raw = {}
        self.tiles = cfs_sets.SetTiles(self)
        self.tile_cache = self.tiles.cache
        self._load_raw()
        self._build_menu()
        self._build_widgets()
        self.refresh(all_scores=False)

    def destroy(self):
        """Sauberes Schliessen (Fix 01.10.2026, DeepSeek-Review Punkt 2):
        Timer + Poll stoppen, Worker entwerten, Queue leeren, dann Tk zu.
        Verhindert TclError-Spam aus daemon-Threads nach Fenster-Schluss."""
        try:
            self._closed = True
        except Exception:
            pass
        for attr in ("_resize_after", "_box_after", "anim_after",
                     "_match_after", "_menu_away_id", "_ui_tick_id",
                     "_startup_after", "_startup_idle"):
            try:
                _id = getattr(self, attr, None)
                if _id is not None:
                    self.after_cancel(_id)
            except Exception:
                pass
            try:
                setattr(self, attr, None)
            except Exception:
                pass
        try:
            self._menu_away_cancel()
        except Exception:
            pass
        try:
            self.cancel = True
            self._ana_seq += 1
            self._ana_pending = None
            self._ana_busy = False
            if isinstance(getattr(self, "rand_job", None), dict):
                self.rand_job["stop"] = True
        except Exception:
            pass
        try:
            q = getattr(self, "_ui_queue", None)
            if q is not None:
                while True:
                    q.get_nowait()
        except Exception:
            pass
        try:
            super().destroy()
        except Exception:
            pass

    def _on_close(self):
        """Fenster-X / 'Ende' -> destroy() mit Aufraeumen (s. dort)."""
        try:
            self.destroy()
        except Exception:
            pass

    # ---------- Grafiken (ausgelagert in cfs_sets, 01.10.2026) ----------
    def _load_raw(self):
        """Rohgrafiken laden (via cfs_sets.SetArt)."""
        self.raw = cfs_sets.SetArt.load_all()
        # Cache-Objekt ggf. neu verdrahten (falls raw ersetzt wurde).
        try:
            self.tiles.cache = self.tile_cache = {}
        except Exception:
            pass

    def _tile(self, kind):
        """Skalierte Kachel, Zoom-cached (via cfs_sets.SetTiles)."""
        return self.tiles.tile(kind)

    def _tile_img(self, kind, w, h):
        """PIL-Kachel exakt auf w x h (via cfs_sets.SetTiles)."""
        return self.tiles.tile_img(kind, w, h)

    @property
    def cell(self):
        w0, _ = self.raw[self.set_no]["back"].size
        return max(8, int(round(w0 * self.zoom)))

    # ---------- Menue ----------
    def _build_menu(self):
        mb = tk.Menu(self)
        # Referenzen auf die Untermenues (fuer _open_menu/_close_menus).
        self._menubar = mb
        self._menu_guard = None  # (which, monotonic) gegen Doppel-Feuern
        self._menu_file = None
        self._menu_view = None
        self._menu_set = None
        self._menu_cmd = None
        self._menu_help = None
        self._menu_depth = None  # Kaskade Computer-Stufe (fuer Popup-Scan)
        self._kb_menu = None  # per Tastatur geoeffnetes Untermenue (Fix 01.10.2026)
        # Aktuell offenes Menue-Popup (Fix 01.10.2026, Bug: Menue liess sich
        # nicht mehr schliessen, weil _open_menu() nie unpostete + kein
        # Modus verfolgt wurde). _menu_open haelt den Zustand, _menu_away_id
        # den Auto-Close-Timer fuer Klicks ausserhalb.
        self._menu_open = None
        self._menu_away_id = None
        self._menu_click_away = self._make_menu_click_away()
        m_file = tk.Menu(mb, tearoff=0)
        m_file.add_command(label=cfs_lang.t("new_game"), command=self.new_game)
        m_file.add_command(label=cfs_lang.t("new_random"), command=self.new_random_dialog)
        m_file.add_separator()
        m_file.add_command(label=cfs_lang.t("load_position"), command=self.load_pos)
        m_file.add_command(label=cfs_lang.t("save_position"), command=self.save_pos)
        m_file.add_separator()
        m_file.add_command(label=cfs_lang.t("quick_save"), command=self.quick_save,
                           accelerator="F3")
        m_file.add_command(label=cfs_lang.t("quick_load"), command=self.quick_load,
                           accelerator="F4")
        m_file.add_separator()
        m_file.add_command(label=cfs_lang.t("quit"), command=self._on_close)
        mb.add_cascade(label=cfs_lang.t("menu_file"), menu=m_file)
        self._menu_file = m_file
        self._menu_index = {"file": 0}

        m_view = tk.Menu(mb, tearoff=0)
        # HINWEIS: ana_var MUSS weiterleben (Rest der GUI liest/schreibt sie),
        # aber der Menueeintrag ist raus — Dauer-Analyse wohnt unter
        # Kommandos (F7) + Analyse-Button. (Wunsch Patrick 30.09.2026.)
        self.ana_var = tk.BooleanVar(value=False)
        self.ghost_var = tk.BooleanVar(value=True)
        m_view.add_checkbutton(label=cfs_lang.t("ghost_stone"), variable=self.ghost_var,
                               command=self.toggle_ghost)
        self.anim_var = tk.BooleanVar(value=True)
        m_view.add_checkbutton(label=cfs_lang.t("drop_animation"), variable=self.anim_var,
                               command=self.toggle_anim)
        self.show_var = tk.BooleanVar(value=True)
        m_view.add_checkbutton(label=cfs_lang.t("show_last_move"), variable=self.show_var,
                               command=self.toggle_show_last)
        m_view.add_separator()
        # Spielstand (Wunsch Patrick 30.09.2026): gleiche Befehle wie die
        # Buttons im Spielstand-Feld (An/Aus + Reset); Menue spiegelt den
        # Zustand (Haken = Anzeige aktiv). Kein An/Aus-Doppel ueber
        # checkbutton-Variable: der Button toggelt, das Menue folgt.
        self.stand_var = tk.BooleanVar(value=False)
        m_view.add_checkbutton(label=cfs_lang.t("score_onoff"), variable=self.stand_var,
                               command=self.toggle_stand_menu)
        m_view.add_command(label=cfs_lang.t("score_reset"), command=self._stand_reset)
        mb.add_cascade(label=cfs_lang.t("menu_view"), menu=m_view)
        self._menu_view = m_view
        self._menu_index["view"] = 1

        m_set = tk.Menu(mb, tearoff=0)
        self.settings_menu = m_set
        # Engine-Stufen (Patzerquote + Gegnerzug-Filter ueber moves_left:
        # moves_left (untere Zahl) = Gewinn-/Verlustdistanz aus eigener Sicht;
        # Gegner mattet in seinem N-ten Zug genau bei moves_left = 2*N.
        # Filter (Verlustschutz s): Patzer-Zug tabu, wenn ml <= 2*s.
        # Siegsschutz w (Variante B): kurzer Gewinn mit ml <= 2*w-1 geht
        # IMMER vor (zufaellig aus der Gewinnmenge), p-Wurf nur bei leerer
        # Menge. Stufen (p, s, w): Zufall (Sonderfall, reiner Zufall
        # ohne p/s/w-Logik), Sehr Leicht (25,0,0),
        # Leicht (40,0,0), Anfaenger (50,0,0), Fortgeschritten (20,1,1),
        # Taktiker (0,3,3), Mittel (50,1,1), Fordernd (55,1,1),
        # Schwer (65,1,1), Sehr Schwer (70,2,2), Experte (80,2,2),
        # Meister (85,3,3), Starker Meister (92,4,4), Perfekt (100,-,-).
        # Filter aus bei s = 0/None (Zufall/Sehr Leicht/Leicht/Anfaenger).
        self.depth_var = tk.StringVar(value="perfekt")
        self.depth_menu = tk.Menu(m_set, tearoff=0)
        self._menu_depth = self.depth_menu  # fuer Popup-Scan (_active_popups)
        for stufe in self.STUFEN_ORDER:
            self.depth_menu.add_radiobutton(label=cfs_levels.level_label(stufe),
                                            variable=self.depth_var,
                                            value=stufe, command=self.switch_depth)
        m_set.add_cascade(label=cfs_lang.t("computer_level"), menu=self.depth_menu)
        m_set.add_separator()
        self.opp_var = tk.StringVar(value="Computer")
        self._engine_label = "Mensch-Computer"  # Radiotext ohne Stufenzusatz
        m_set.add_radiobutton(label=cfs_lang.t("human_computer"), variable=self.opp_var, value="Computer",
                              command=self._select_engine)
        m_set.add_radiobutton(label=cfs_lang.t("two_player"), variable=self.opp_var, value="2-Spieler (beide Mensch)",
                              command=self.toggle_two_player)
        m_set.add_radiobutton(label=cfs_lang.t("selfplay"), variable=self.opp_var,
                              value="Computer-Computer (ausspielen)",
                              command=self._select_selfplay)
        # Turnier (Match): eigener Dialog mit Seiten, Partienzahl,
        # Farbwechsel und Tempo (Normal/Schnell/Turbo). Gehoert zu den
        # Auto-Play-Modi wie Computer-Computer (ausspielen), daher hier
        # platziert (Wunsch Patrick).
        m_set.add_command(label=cfs_lang.t("match"), command=self.match_dialog)
        m_set.add_command(label=cfs_lang.t("stop_autoplay"), command=self.stop)
        m_set.add_separator()
        # Kein Buch-Menue mehr: fest verdrahtet 12-ply-dist (Gewinn + Zugzahl).
        # Das entfernt 8-ply/12-ply-Sonderfaelle und 'ohne Buch'-Freezes.
        self.book_var = tk.StringVar(value="12-ply-dist")
        self._book_names = {
            "12-ply-dist": cfs_lang.t("book_name_12"),
        }
        self.set_var = tk.IntVar(value=self.set_no)
        # Blaetter-Befehle OBEN im Sets-Menue (Wunsch Patrick 03.10.2026):
        # 'vorheriges'/'naechstes' zuerst, damit sie in der langen
        # Liste (20 Sets) nicht uebersehen werden.
        # Dezente Blaetterhinweise (Wunsch Patrick 01.10.2026): wie F5 im
        # Kommandos-Menü – als accelerator-Spalte, nicht als extra Text.
        m_set.add_command(label=cfs_lang.t("prev_set"), command=lambda: self.cycle_set(-1),
                          accelerator=cfs_lang.t("acc_pgup"))
        m_set.add_command(label=cfs_lang.t("next_set"), command=lambda: self.cycle_set(+1),
                          accelerator=cfs_lang.t("acc_pgdn"))
        m_set.add_separator()
        # Menue-Sets (20 freigegebene Sets): nur
        # freigegebene Sets mit Anzeige-Namen (Rest ladbar, nicht im Menue).
        # Reihenfolge: set_menu_order (_SET_ORDER, Wunsch Patrick 30.09.2026).
        for s in set_menu_order(self.raw):
            if s not in _MENU_SETS:
                continue
            m_set.add_radiobutton(label=cfs_lang.tf("set_menu_item", no=s,
                                                name=cfs_sets.set_display_name(s)),
                                  variable=self.set_var, value=s,
                                  command=self.switch_set)
        mb.add_cascade(label=cfs_lang.t("menu_settings"), menu=m_set)
        self._menu_set = m_set
        self._menu_index["set"] = 2

        m_cmd = tk.Menu(mb, tearoff=0)
        m_cmd.add_command(label=cfs_lang.t("first_move"), command=self.goto_first,
                          accelerator=cfs_lang.t("acc_up"))
        m_cmd.add_command(label=cfs_lang.t("move_back"), command=self.undo,
                          accelerator=cfs_lang.t("acc_left"))
        m_cmd.add_command(label=cfs_lang.t("move_forward"), command=self.redo,
                          accelerator=cfs_lang.t("acc_right"))
        m_cmd.add_command(label=cfs_lang.t("last_move"), command=self.goto_last,
                          accelerator=cfs_lang.t("acc_down"))
        m_cmd.add_separator()
        m_cmd.add_command(label=cfs_lang.t("engine_move"), command=self.engine_move,
                           accelerator="F5")
        m_cmd.add_command(label=cfs_lang.t("score_all"), command=self.toggle_scores,
                           accelerator="F6")
        m_cmd.add_command(label=cfs_lang.t("permanent_analysis"), command=self.toggle_auto_analyze_btn,
                           accelerator="F7")
        mb.add_cascade(label=cfs_lang.t("menu_commands"), menu=m_cmd)
        self._menu_cmd = m_cmd
        self._menu_index["cmd"] = 3

        m_help = tk.Menu(mb, tearoff=0)
        m_help.add_command(label=cfs_lang.t("help_contents"), command=self.show_help,
                           accelerator="F1")
        m_help.add_command(label=cfs_lang.t("help_info"), command=self.show_info)
        m_help.add_separator()
        # Sprache (Vorbereitung 04.10.2026): Radio-Einträge für alle
        # geplanten Sprachen (de/en/fr/es/nl/it). Radio = runder
        # Auswahlpunkt, genau eine Sprache aktiv (wie Computer-Stufe).
        # Noch ohne Wirkung ausser de/en (Rest fällt auf Deutsch zurück,
        # bis die Übersetzungen in cfs_lang.py stehen).
        self.lang_var = tk.StringVar(value=cfs_lang.LANG)
        m_lang = tk.Menu(m_help, tearoff=0)
        for _code in cfs_lang.LANG_ORDER:
            _lab = cfs_lang.t(cfs_lang.LANG_LABEL_KEY[_code])
            m_lang.add_radiobutton(label=_lab, variable=self.lang_var,
                                   value=_code, command=self.switch_lang)
        m_help.add_cascade(label=cfs_lang.t("lang_menu"), menu=m_lang)
        self._menu_lang = m_lang
        mb.add_cascade(label=cfs_lang.t("menu_help"), menu=m_help)
        self._menu_help = m_help
        self._menu_index["help"] = 4
        self.config(menu=mb)
        self._register_menu_labels()
        # Tastatur im Menue (Stand 01.10.2026, Wunsch Patrick):
        # KEIN Menue-Zugriff per Tastatur (F10/Alt/Strg entfernt – reines
        # Anzeige-Menue ohne Pfeil-Navigation ist nutzlos, Maus ist schneller).
        # F10 wird explizit neutralisiert (Tk-Standard tk::FirstMenu wuerde
        # sonst das erste Menue oeffnen). F1 oeffnet die Hilfe, ESC schliesst
        # ein offenes Menue.
        try:
            self.bind_all("<F10>", lambda e: "break")
            self.bind_all("<F1>", lambda e: self.show_help())
            self.bind_all("<Key-F1>", lambda e: self.show_help())
            self.bind_all("<Help>", lambda e: self.show_help())
            self.bind_all("<Escape>", lambda e: self._close_menus())
        except Exception:
            pass
        # Klick irgendwo ins Hauptfenster schliesst ein offenes Tastatur-
        # Menue (Fix 01.10.2026). Gebunden an Root (nicht bind_all, damit
        # Dialoge unberuehrt bleiben).
        try:
            self.bind("<Button-1>", self._menu_click_away, add="+")
        except Exception:
            pass

    def _make_menu_click_away(self):
        """Klick-Handler: offenes Menue schliessen, sobald irgendwo ins
        Hauptfenster geklickt wird (Fix 01.10.2026 gegen Doppel-Menues:
        das per .post() geoeffnete Menue blieb offen, das per Maus
        geoeffnete kam dazu).

        WICHTIG: Tk schliesst ein Menue, das den Fokus hat, von sich aus
        beim naechsten Button-Press - aber erst NACH den Widget-Bindings.
        Der Handler prueft daher erst, ob das Popup noch offen ist
        (winfo_ismapped), und schliesst es dann selbst. So ist auch der
        Kaskaden-Klick (dessen Bindung vor dieser Root-Bindung laeuft)
        abgedeckt: er wird hier nur noch aufgeraeumt, falls das neue
        Untermenue NICHT im selben 'Tab' liegt."""
        def handler(ev):
            try:
                kb = getattr(self, "_kb_menu", None)
                if kb is not None and kb.winfo_exists() and kb.winfo_ismapped():
                    self._close_menus()
            except Exception:
                pass
            return None
        return handler

    def _menu_away_cancel(self):
        """Auto-Close-Timer (Klick ausserhalb) abbrechen (Fix 01.10.2026)."""
        try:
            if self._menu_away_id is not None:
                self.after_cancel(self._menu_away_id)
        except Exception:
            pass
        self._menu_away_id = None

    def _menu_away_check(self):
        """Menue offen halten, solange der Zeiger im Menue-Baum steht;
        sonst schliessen. Laeuft als after-Poll, weil Button-Events auf
        Tk-Menue-Popups nicht zuverlaessig durchkommen. Der Klick ins
        eigene Fenster wird zusaetzlich von _make_menu_click_away
        behandelt."""
        self._menu_away_id = None
        try:
            kb = getattr(self, "_kb_menu", None)
            if kb is None:
                return
            if not (kb.winfo_exists() and kb.winfo_ismapped()):
                self._kb_menu = None
                self._menu_open = None
                return
            try:
                w = self.winfo_pointerxy()
            except Exception:
                w = None
            # ECHTER Klick-Check: gemerktes Zeiger-Referenzpaar (beim Oeffnen)
            # mit der aktuellen Position vergleichen. Nur bei BEWEGLICHEM
            # Zeiger (echte Maus) darf das als "Klick woanders" werten –
            # ein starrer Test-Zeiger schliesst sonst alles sofort.
            try:
                w = self.winfo_pointerxy()
            except Exception:
                w = None
            if w is None:
                self._menu_away_id = self.after(250, self._menu_away_check)
                return
            try:
                ref = getattr(self, "_menu_pointer_ref", None)
            except Exception:
                ref = None
            if ref is None:
                try:
                    self._menu_pointer_ref = w
                except Exception:
                    pass
                self._menu_away_id = self.after(250, self._menu_away_check)
                return
            try:
                moved = (abs(w[0] - ref[0]) + abs(w[1] - ref[1])) > 8
            except Exception:
                moved = False
            if not moved:
                # Zeiger ruht: offen lassen, weiter pollen.
                self._menu_away_id = self.after(250, self._menu_away_check)
                return
            # Zeiger WURDE bewegt: jetzt zaehlt die Geometrie.
            try:
                mx, my = kb.winfo_rootx(), kb.winfo_rooty()
                mw, mh = kb.winfo_width(), kb.winfo_height()
            except Exception:
                self._menu_away_id = self.after(250, self._menu_away_check)
                return
            pad = 4
            inside = (mx - pad <= w[0] <= mx + mw + pad
                      and my - pad <= w[1] <= my + mh + pad)
            if not inside:
                try:
                    inside = self._in_menu_tree(kb, w)
                except Exception:
                    inside = True
            if inside:
                try:
                    self._menu_pointer_ref = w
                except Exception:
                    pass
                self._menu_away_id = self.after(250, self._menu_away_check)
            else:
                self._close_menus()
        except Exception:
            pass

    def _in_menu_tree(self, menu, pt):
        """True, wenn pt (Screenkoordinaten) im Menue oder in einem seiner
        offenen Sub-/Kaskadenmenues liegt. Reines Geometrie-Pruefung ueber
        winfo_ismapped/winfo_rootx/y - so wird auch ein Klick auf einen
        Eintrag, der ein Untermenue aufzieht, korrekt erkannt."""
        try:
            if not (menu.winfo_exists() and menu.winfo_ismapped()):
                return False
            x0 = menu.winfo_rootx(); y0 = menu.winfo_rooty()
            x1 = x0 + menu.winfo_width(); y1 = y0 + menu.winfo_height()
            if x0 <= pt[0] <= x1 and y0 <= pt[1] <= y1:
                return True
            for i in range(menu.index("end") + 1):
                if menu.type(i) == "cascade":
                    sm = menu.entrycget(i, "menu")
                    try:
                        sub = self.nametowidget(sm)
                    except Exception:
                        sub = None
                    if sub is not None and self._in_menu_tree(sub, pt):
                        return True
        except Exception:
            pass
        return False

    def _active_popups(self):
        """Alle Menue-Popups, die gerade sichtbar (mapped) sind - inklusive
        verschachtelter Kaskaden (Stufe -> Stein-Set). Genutzt zum
        Schliessen, unabhaengig davon, welcher Weg sie geoeffnet hat."""
        tops = []
        try:
            mb = getattr(self, "_menubar", None)
            if mb is not None:
                tops.append(mb)
        except Exception:
            pass
        for name in ("_menu_file", "_menu_view", "_menu_set",
                     "_menu_cmd", "_menu_help", "_menu_depth"):
            m = getattr(self, name, None)
            if m is not None:
                tops.append(m)
        popups = []
        seen = set()

        def walk(m):
            if m is None or id(m) in seen:
                return
            seen.add(id(m))
            try:
                if m.winfo_ismapped():
                    popups.append(m)
            except Exception:
                pass
            try:
                for i in range(m.index("end") + 1):
                    if m.type(i) == "cascade":
                        try:
                            walk(self.nametowidget(m.entrycget(i, "menu")))
                        except Exception:
                            pass
            except Exception:
                pass

        for t in tops:
            walk(t)
        return popups

    def _close_menus(self, *_args):
        """ALLE Menue-Popups schliessen (auch Kaskaden) + Zustand/Timer
        aufraeumen. Wird von ESC, Klick-ins-Fenster, Klick-ausserhalb und
        _open_menu() gerufen."""
        self._menu_away_cancel()
        try:
            self._menu_pointer_ref = None
        except Exception:
            pass
        for m in self._active_popups():
            try:
                m.unpost()
            except Exception:
                pass
        try:
            self.tk.call(self._menubar._w, "unpost")
        except Exception:
            pass
        self._kb_menu = None
        self._menu_open = None
        return "break"

    def _open_menu(self, which, source="f10"):
        """Datei-Menue per F10 oeffnen (einziger Tastatur-Menueweg,
        Stand 01.10.2026). Position linksbuendig im Programmfenster.
        Schreibt den Ausloeser in die Statuszeile.
        Es ist garantiert hoechstens EIN Menue offen (erst alles zu,
        dann oeffnen; Toggle schliesst). Kein Grab, ESC/Klick schliesst.
        """
        try:
            mb = getattr(self, "_menubar", None)
            idx = getattr(self, "_menu_index", {}).get(which)
            if mb is None or idx is None:
                return None
            sub = {"file": getattr(self, "_menu_file", None),
                   "view": getattr(self, "_menu_view", None),
                   "set": getattr(self, "_menu_set", None),
                   "cmd": getattr(self, "_menu_cmd", None),
                   "help": getattr(self, "_menu_help", None)}.get(which)
            if sub is None:
                return None
            # Doppel-Feuern-Guard: derselbe Aufruf innerhalb von 50 ms
            # = Duplikat, verwerfen (sonst Toggle-Schliess-Blitzen).
            try:
                import time as _time
                g = getattr(self, "_menu_guard", None)
                if g is not None and g[0] == which and \
                        (_time.monotonic() - g[1]) < 0.05:
                    return "break"
            except Exception:
                pass
            try:
                import time as _time
                self._menu_guard = (which, _time.monotonic())
            except Exception:
                pass
            # Toggle: dasselbe Menue erneut -> schliessen.
            if getattr(self, "_menu_open", None) is sub or \
               getattr(self, "_kb_menu", None) is sub:
                self._close_menus()
                return "break"
            # Alle ANDEREN Menues zu (nicht das Zielmenue). Danach oeffnen.
            for m in [x for x in self._active_popups() if x is not sub]:
                try:
                    m.unpost()
                except Exception:
                    pass
            try:
                self.tk.call(self._menubar._w, "unpost")
            except Exception:
                pass
            # Statuszeile.
            try:
                _names = {"file": cfs_lang.t("menu_file"),
                          "view": cfs_lang.t("menu_view"),
                          "set": cfs_lang.t("menu_settings"),
                          "cmd": cfs_lang.t("menu_commands"),
                          "help": cfs_lang.t("menu_help")}
                _src = {"f10": "F10"}.get(source, source)
                self.status.set(cfs_lang.tf("status_menu_opened",
                                            name=_names.get(which, which),
                                            src=_src))
            except Exception:
                pass
            self.update_idletasks()
            # Position linksbuendig unter der Menueleiste im Fenster.
            x = self.winfo_rootx() + 2
            y = self.winfo_rooty() + 2
            try:
                req_h = sub.winfo_reqheight()
                scr_h = self.winfo_screenheight()
            except Exception:
                req_h = 0
                scr_h = 0
            try:
                if req_h and scr_h and req_h > scr_h - 60:
                    # Langes Menue (Einstellungen: viele Sets): oben UND
                    # unten sichtbar halten (Tk klappt sonst nach oben).
                    y = max(0, self.winfo_rooty() + 2 - (req_h - scr_h + 60))
            except Exception:
                pass
            try:
                sub.post(x, y)
                self._kb_menu = sub
                self._menu_open = sub
                try:
                    self._menu_pointer_ref = self.winfo_pointerxy()
                except Exception:
                    self._menu_pointer_ref = None
            except Exception:
                pass
            # KEIN Grab aufs Menue; Poll unten schliesst bei Klick
            # ausserhalb; ESC laeuft ueber bind_all am Hauptfenster.
            self._menu_away_cancel()
            try:
                self._menu_away_id = self.after(250, self._menu_away_check)
            except Exception:
                pass
        except Exception:
            pass
        return "break"

    def show_info(self):
        """Info-Dialog (ausgelagert in cfs_help, aktive Sprache)."""
        import cfs_help
        cfs_help.show_info(self, lang=cfs_lang.LANG)

    def show_help(self):
        """Hilfe-Dialog (ausgelagert in cfs_help, aktive Sprache)."""
        import cfs_help
        cfs_help.show_help(self, lang=cfs_lang.LANG)

    def switch_lang(self):
        """Sprache umschalten (Hilfe-Menü, Radio). Wahl wird gemerkt
        (data/lang.cfg), Startsprache = gespeicherte Wahl > System."""
        try:
            cfs_lang.set_lang(self.lang_var.get())
            cfs_lang.save_start_lang(self.lang_var.get())
        except Exception:
            pass
        self._relabel_all()

    # Menue-Eintraege, deren Text/Accelerator aus cfs_lang kommt. Die
    # Zuordnung (Menue, Index, Schluessel) wird einmal nach dem Bau aus den
    # Eintraegen zurueckgelesen; _relabel_all() setzt sie bei Sprachwechsel
    # neu. Dynamische Eintraege (Stufen, Sets) werden separat behandelt.
    _MENU_LABEL_KEYS = ("menu_file", "menu_view", "menu_settings",
                        "menu_commands", "menu_help", "new_game", "new_random",
                        "load_position", "save_position", "quick_save",
                        "quick_load", "quit", "ghost_stone", "drop_animation",
                        "show_last_move", "score_onoff", "score_reset",
                        "computer_level", "human_computer", "two_player",
                        "selfplay", "match", "stop_autoplay", "prev_set",
                        "next_set", "first_move", "move_back", "move_forward",
                        "last_move", "engine_move", "score_all",
                        "permanent_analysis", "help_contents", "help_info",
                        "lang_menu")
    _MENU_ACC_KEYS = ("acc_pgup", "acc_pgdn", "acc_up", "acc_down",
                      "acc_left", "acc_right")

    def _register_menu_labels(self):
        """Merkt sich je Menue-Eintrag den cfs_lang-Schluessel (aus dem
        aktuell angezeigten Text rueckgelesen)."""
        rev = {cfs_lang.t(k): k for k in self._MENU_LABEL_KEYS}
        arev = {cfs_lang.t(k): k for k in self._MENU_ACC_KEYS}
        reg = []
        menus = [self._menubar, self._menu_file, self._menu_view,
                 self._menu_set, self._menu_cmd, self._menu_help]
        for m in menus:
            try:
                last = m.index("end")
            except Exception:
                last = None
            if last is None:
                continue
            for i in range(last + 1):
                try:
                    if m.type(i) in ("separator", "tearoff"):
                        continue
                    lab = m.entrycget(i, "label")
                except Exception:
                    continue
                if lab in rev:
                    reg.append((m, i, "label", rev[lab]))
                try:
                    acc = m.entrycget(i, "accelerator")
                except Exception:
                    acc = ""
                if acc in arev:
                    reg.append((m, i, "accelerator", arev[acc]))
        self._menu_reg = reg

    def _relabel_all(self):
        """Sichtbare Texte der Oberflaeche in der aktiven Sprache neu setzen
        (Menues, Buttons, Rahmen, Infobox, Spielstand, Am-Zuge, Stufen)."""
        t = cfs_lang.t
        for m, i, opt, key in getattr(self, "_menu_reg", []):
            try:
                m.entryconfigure(i, **{opt: t(key)})
            except Exception:
                pass
        try:  # Computer-Stufe-Kaskade
            for i, stufe in enumerate(self.STUFEN_ORDER):
                self.depth_menu.entryconfigure(
                    i, label=cfs_levels.level_label(stufe))
        except Exception:
            pass
        try:  # Stein-Set-Radios im Einstellungen-Menue
            last = self._menu_set.index("end")
            for i in range(last + 1):
                if self._menu_set.type(i) != "radiobutton":
                    continue
                if str(self._menu_set.entrycget(i, "variable")) != str(self.set_var):
                    continue
                no = int(self._menu_set.entrycget(i, "value"))
                self._menu_set.entryconfigure(
                    i, label=cfs_lang.tf("set_menu_item", no=no,
                                         name=cfs_sets.set_display_name(no)))
        except Exception:
            pass
        try:
            self._book_names["12-ply-dist"] = t("book_name_12")
        except Exception:
            pass
        for b, key in zip(getattr(self, "bar_buttons", []),
                          getattr(self, "_bar_keys", [])):
            try:
                b.config(text=t(key))
            except Exception:
                pass
        for fr, key in ((getattr(self, "_turn_frame", None), "info_turn"),
                        (getattr(self, "_info_frame", None), "info_box"),
                        (getattr(self, "_stand_frame", None), "score_box")):
            try:
                fr.config(text=t(key))
            except Exception:
                pass
        for key, lab in getattr(self, "_info_labels", {}).items():
            try:
                lab.config(text=t(key) + ":")
            except Exception:
                pass
        try:
            self._stand_toggle_btn.config(text=t("score_on"))
            self._stand_reset_btn.config(text=t("score_reset_btn"))
        except Exception:
            pass
        for fn in (self._update_turn,):
            try:
                fn()
            except Exception:
                pass
        try:
            self.info_vars["Stufe"].set(self._display_stufe_label())
        except Exception:
            pass
        try:
            if getattr(self, "_stand_enabled", False):
                self._stand_show()
        except Exception:
            pass
        try:
            self.set_status_ready_if_idle()
        except Exception:
            pass

    def set_status_ready_if_idle(self):
        """Nach Sprachwechsel: Statuszeile nur neu setzen, wenn sie noch das
        Startwort zeigt (andere Meldungen bleiben stehen)."""
        if self.status.get() in {cfs_lang.t("status_ready", c)
                                 for c in cfs_lang.STRINGS}:
            self.status.set(cfs_lang.t("status_ready"))

    # ---------- Widgets ----------
    # Layout: Holder fuellt das Fenster links; darin liegt die Boardbox
    # (Brett + Scores + Buttons) zentriert mit EXAKT Boardbreite. Canvas wird
    # nie gestretcht -> kein blauer Ueberstand; Scores sind im Canvas
    # gezeichnet (pixel-exakt unter den Spalten); Buttons teilen sich per
    # Uniform-Grid exakt dieselbe Breite.
    def _build_widgets(self):
        self.main = ttk.Frame(self, padding=8)
        self.main.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        # Zeile 0 (Brett) waechst, Zeile 1 (Status) bleibt unten fixiert:
        # die Statuszeile klebt IMMER am Fensterrand, kein Graufeld darunter.
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        self.holder = ttk.Frame(self.main)
        # sticky nsew: Holder fuellt die Reihenhoehe; die Boardbox klebt per
        # sticky=n OBEN darin (Brett direkt unter der Menueleiste wie vorher).
        # Die Boardbox selbst ist nur so hoch wie ihr Inhalt (kein weight):
        # Restluft liegt INNERHALB des Holders unterm Brett, die Statuszeile
        # (Zeile 1, weight=0) klebt trotzdem am Fensterrand.
        self.holder.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        # Spalten: weight=0 -> Holder exakt Boardbreite, Infobox klebt am Brett.
        # Holder-Reihe: weight=1 (fuellt die Fensterhoehe, Boardbox klebt oben).
        # Main-Zeile 0: weight=1 (Brettbereich waechst), Zeile 1: weight=0
        # (Statuszeile fix am Fensterrand -> kein Graufeld darunter).
        self.holder.rowconfigure(0, weight=0)
        self.main.columnconfigure(0, weight=0)
        self.main.columnconfigure(1, weight=0)
        self.main.rowconfigure(0, weight=1)
        self.main.rowconfigure(1, weight=0)
        self.boardbox = tk.Frame(self.holder)
        # sticky n: Box klebt OBEN (direkt unter Menueleiste wie vorher).
        self.boardbox.grid(row=0, column=0, sticky="n")
        self.boardbox.columnconfigure(0, weight=1)
        self.boardbox.bind("<Configure>", self.on_box_resize)
        self._box_after = None

        # Brett-Canvas in exakter Boardgroesse (+ Score-Zeile darunter)
        self.last_scores = None  # dict Spalte -> (Text, BG) oder None
        self.canvas = tk.Canvas(self.boardbox, width=COLS * self.cell,
                                height=self.canvas_h(),
                                background=self.raw[self.set_no].get("edge", BOARD_BG),
                                highlightthickness=0, borderwidth=0)
        self.canvas.grid(row=0, column=0, sticky="n")
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Motion>", self.on_hover)
        self.canvas.bind("<Leave>", lambda e: self.set_hover(None))
        # Set-Wechsel: Mausrad ueber dem Brett = Menue-Sets durchscrollen
        # (Wunsch Patrick). Linux: Button-4/5 (Rad), Windows: MouseWheel.
        # Einheitlich: Rad-hoch = vorheriges, Rad-runter = naechstes.
        self.canvas.bind("<Button-4>", lambda e: self.cycle_set(-1))
        self.canvas.bind("<Button-5>", lambda e: self.cycle_set(+1))
        self.canvas.bind("<MouseWheel>", self._on_set_wheel)

        # Buttonleiste: genau 7 Buttons, gleiche Spalten, einzeilig
        # (Wunsch Patrick 30.09.2026: Neu, <<, <, >, >>, Ziehen, Analyse;
        # 'Zufall' weiter ueber Datei > Neu mit Zufallsstellung...,
        # 'Alle' weiter ueber Kommandos > alle Züge bewerten).
        self.bar = tk.Frame(self.boardbox)
        self.bar.grid(row=1, column=0, sticky="ew", pady=(2, 0))
        for c in range(COLS):
            self.bar.columnconfigure(c, weight=1, uniform="cols")
        self.bar_buttons = []
        self._bar_keys = []
        buttons = [
            ("btn_new", self.new_game),
            ("btn_first", self.goto_first), ("btn_back", self.undo),
            ("btn_forward", self.redo), ("btn_last", self.goto_last),
            ("btn_move", self.engine_move),
            ("btn_analyze", self.toggle_auto_analyze_btn),
        ]
        for c, (key, cmd) in enumerate(buttons):
            b = tk.Button(self.bar, text=cfs_lang.t(key), command=cmd, font=("TkDefaultFont", 9))
            b.grid(row=0, column=c, sticky="ew")
            self.bar_buttons.append(b)
            self._bar_keys.append(key)

        # Rechte Seite: "Am Zuge" oben (Stein + echter Spielername),
        # darunter Info schmal
        right = ttk.Frame(self.main)
        right.grid(row=0, column=1, sticky="new", padx=(0, 0))
        self.right_panel = right
        turn = ttk.LabelFrame(right, text=cfs_lang.t("info_turn"), padding=6)
        turn.pack(fill="x")
        self._turn_frame = turn
        self.turn_img = tk.Label(turn)
        self.turn_img.pack(side="left", padx=(0, 6))
        self._turn_icons = {}  # Am-Zuge-Icons (Fix 01.10.2026, s. _stone_icon)
        self.turn_var = tk.StringVar(value=cfs_lang.t("info_human"))
        ttk.Label(turn, textvariable=self.turn_var).pack(side="left")
        info = ttk.LabelFrame(right, text=cfs_lang.t("info_box"), padding=6)
        info.pack(fill="x", pady=(6, 0))
        self._info_frame = info
        self.info_vars = {}
        self._info_labels = {}
        for i, key in enumerate(["info_move", "info_level", "info_depth", "info_value", "info_nodes", "info_time", "info_nodes_per_sec", "info_book"]):
            lab = ttk.Label(info, text=cfs_lang.t(key) + ":")
            lab.grid(row=i, column=0, sticky="w")
            v = tk.StringVar(value="\u2013")
            ttk.Label(info, textvariable=v, width=11).grid(row=i, column=1, sticky="w")
            self.info_vars[key] = v
            self._info_labels[key] = lab
        # Stabile Aliase fuer bestehende Zugriffe mit alten deutschen Keys.
        for _alias, _target in (("Zug", "info_move"), ("Stufe", "info_level"),
                                ("Tiefe", "info_depth"), ("Wert", "info_value"),
                                ("Kn", "info_nodes"), ("Zeit", "info_time"),
                                ("Kn/s", "info_nodes_per_sec"), ("Buch", "info_book")):
            self.info_vars[_alias] = self.info_vars[_target]

        # Spielstand (Mensch vs. Computer): IMMER sichtbar, Frame bleibt
        # stehen (User-Wunsch: 'Spielstand'-Titel nie weg). An/Aus loescht
        # nur den Inhalt (0-0 etc.); Reset setzt auf 0-0 zurueck. Zaehlt
        # im Turnier mit Mensch UND beim normalen Mensch-vs-Computer-Spiel
        # (Standard aus, per An/Aus aktivieren -> 0-0, dann zaehlen).
        # Haupt: _stand_pair[comp_key] = [siege_mensch, siege_comp, remis].
        # comp_key = Gegnerstufe ('perfekt' etc.); bei Turnier mit Mensch
        # farbwechsel-sicher ueber Brettgewinner + _match_gelb_beginnt.
        # Hauptergebnis gross (ca. 4x), (+/=/-) darunter normal, Elo erst
        # ab je >= 0,5 Punkten auf beiden Seiten.
        stand = ttk.LabelFrame(right, text=cfs_lang.t("score_box"), padding=6)
        self._stand_frame = stand
        self._stand_head_var = tk.StringVar(value="")
        ttk.Label(stand, textvariable=self._stand_head_var,
                  justify="left").pack(fill="x")
        self._stand_big_var = tk.StringVar(value="")
        try:
            import tkinter.font as _tkfont
            _big = _tkfont.Font(font=("TkDefaultFont", 9))
            _big.configure(size=int(round(_big.cget("size") * 4)))
        except Exception:
            _big = ("TkDefaultFont", 36, "bold")
        ttk.Label(stand, textvariable=self._stand_big_var, font=_big,
                  justify="center").pack(fill="x")
        self._stand_sub_var = tk.StringVar(value="")
        ttk.Label(stand, textvariable=self._stand_sub_var,
                  justify="center").pack(fill="x")
        self._stand_elo_var = tk.StringVar(value="")
        ttk.Label(stand, textvariable=self._stand_elo_var,
                  justify="center").pack(fill="x")
        sbtn = ttk.Frame(stand)
        sbtn.pack(fill="x", pady=(4, 0))
        self._stand_toggle_btn = ttk.Button(sbtn, text=cfs_lang.t("score_on"),
                   command=self._stand_toggle)
        self._stand_toggle_btn.pack(side="left")
        self._stand_reset_btn = ttk.Button(sbtn, text=cfs_lang.t("score_reset_btn"),
                   command=self._stand_reset)
        self._stand_reset_btn.pack(side="left", padx=(4, 0))
        # Start: Frame sichtbar, aber leer (Standard aus). Erst per An/Aus
        # aktivieren -> 0-0, danach wird gezaehlt.
        # (pack erfolgt einmalig hier; _stand_show/_stand_hide fassen den
        # Frame nie mehr an - nur noch die Text-Variablen.)
        stand.pack(fill="x", pady=(6, 0))
        self._stand_visible = True
        self._stand_enabled = False  # Standard: aus (User-Wunsch)
        # Sitzungs-Zaehler Mensch vs. Computer: {comp_key (Gegnerstufe):
        # [siege_mensch, siege_comp, remis]}. 'mensch' als Mensch-Seite
        # steckt im Paar implizit (Anzeige 'Mensch vs <Stufe>').
        # Farbwechsel-sicher im Turnier: gezaehlt wird pro IDENTITAET
        # (wer gewann), nicht pro Brettfarbe (vgl. Turnier-Punktelogik).
        self._stand = {}

        # Statuszeile
        self.status = tk.StringVar(value=cfs_lang.t("status_ready"))
        self._status_label = ttk.Label(self.main, textvariable=self.status, relief="sunken", anchor="w")
        self._status_label.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 0))
        self._scale_chrome()
        self._update_turn()
        self._layout_boardbox()
        # Zoom auf Fenster-Groesse; danach bei echtem Fenster-Resize neu.
        # Start: Fit-Sperre, bis das Fenster sichtbar/stabil ist (gegen die
        # Shrink-Wrap-Kette Fit -> Inhalt kleiner -> Fenster kleiner ...).
        self.bind("<Configure>", self._on_win_configure)
        try:
            self._startup_idle = self.after_idle(self._startup_fit)
        except Exception:
            self._startup_idle = None

        # Tastatur: 1-7 Zugeingabe, Pfeile zurueck/vor, hoch/runter
        # an Anfang/Ende. WICHTIG (Fix 30.09.2026 + 01.10.2026, Wunsch
        # Patrick): Die Brett-Tasten wirken NUR im Hauptfenster – NICHT in
        # Dialogen (z.B. Turnier-Partienzahl/Dateiname, Datei-Dialoge,
        # Random-Dialog, Hilfe-Suche), sonst wuerde Tippen dort Zuege
        # ausloesen. _board_key() prueft das AUSLOESENDE Widget (ev.widget)
        # statt focus_get(): focus_get() ist unter X11/Xvfb unzuverlaessig
        # (native Dateidialoge melden gar keinen Tk-Fokus) und zeigt nach
        # Dialog-Schliessen teils noch das tote Widget. Erlaubt sind nur
        # Tasten-Events aus dem Hauptfenster (Toplevel is self) UND aus
        # nicht-editierbaren Widgets (kein Entry/Text/Spinbox/Combobox/
        # Listbox – sonst wuerde z.B. Tippen im Dateinamen-Feld Zuege
        # ausloesen oder Pfeile in der Combobox-Auswahl Undo triggern).
        # Alles andere wird ignoriert (None = Taste ans Widget geben).
        _EDIT_CLASSES = ("Entry", "TEntry", "Text", "Spinbox", "TSpinbox",
                         "TCombobox", "Combobox", "Listbox")
        def _board_key(fn):
            def handler(ev):
                try:
                    w = getattr(ev, "widget", None)
                except Exception:
                    w = None
                if w is None:
                    try:
                        w = self.focus_get()
                    except Exception:
                        w = None
                if w is None:
                    return None
                try:
                    cls = w.winfo_class()
                except Exception:
                    return None
                if cls in _EDIT_CLASSES:
                    return None  # im Eingabefeld: Taste ans Widget geben
                try:
                    top = w.winfo_toplevel()
                except Exception:
                    return None
                if top is not self:
                    return None  # fremder Dialog: Taste ans Widget geben
                fn()
                return "break"  # am Brett: Taste verbrauchen
            return handler
        self.bind_all("<Key-1>", _board_key(lambda: self.human_move(0)))
        self.bind_all("<Key-2>", _board_key(lambda: self.human_move(1)))
        self.bind_all("<Key-3>", _board_key(lambda: self.human_move(2)))
        self.bind_all("<Key-4>", _board_key(lambda: self.human_move(3)))
        self.bind_all("<Key-5>", _board_key(lambda: self.human_move(4)))
        self.bind_all("<Key-6>", _board_key(lambda: self.human_move(5)))
        self.bind_all("<Key-7>", _board_key(lambda: self.human_move(6)))
        self.bind_all("<Left>", _board_key(self.undo))
        self.bind_all("<Right>", _board_key(self.redo))
        self.bind_all("<Up>", _board_key(self.goto_first))
        self.bind_all("<Down>", _board_key(self.goto_last))
        self.bind_all("<F3>", _board_key(self.quick_save))
        self.bind_all("<F4>", _board_key(self.quick_load))
        self.bind_all("<F5>", _board_key(self.engine_move))
        self.bind_all("<F6>", _board_key(self.toggle_scores))
        self.bind_all("<F7>", _board_key(self.toggle_auto_analyze_btn))
        # Set-Wechsel per Tastatur: Bild-rauf/runter (Wunsch Patrick
        # 30.09.2026: OHNE Strg). Bild-runter = naechstes, Bild-rauf =
        # vorheriges (wie Mausrad-runter/hoch); Wrap-around in cycle_set.
        # Ebenfalls Brett-Fokus-geschuetzt (kein Blaettern beim Tippen).
        self.bind_all("<Prior>", _board_key(lambda: self.cycle_set(-1)))
        self.bind_all("<Next>", _board_key(lambda: self.cycle_set(+1)))

    def _on_set_wheel(self, ev):
        """Mausrad auf dem Brett: Sets wechseln (Windows: delta)."""
        try:
            d = getattr(ev, "delta", 0) or 0
            if d > 0:
                self.cycle_set(-1)
            elif d < 0:
                self.cycle_set(+1)
            else:
                return None
        except Exception:
            return None
        return "break"

    def _safe_after(self, ms, fn):
        """Thread-sicherer GUI-Callback via Queue + Main-Thread-Poll
        (Fix 01.10.2026, DeepSeek-Review Punkt 1): Worker-Threads rufen
        NIEMALS mehr Tk-after() direkt (nicht thread-safe, stiller
        Callback-Verlust -> GUI hing bei 'denkt...'). Stattdessen wird
        (ms, fn) in _ui_queue gelegt; _ui_poll_tick (after-Ticker im
        Main-Thread) arbeitet sie ab. Schutz gegen Event-Flut: max. 60
        offene Eintraege (danach verwerfen). Nach destroy(): verwerfen."""
        try:
            q = getattr(self, "_ui_queue", None)
            if q is None:
                return
            if getattr(self, "_closed", False):
                return
            if q.qsize() > 60:
                return
            try:
                import time as _t
                q.put((int(ms), fn, _t.monotonic()))
            except Exception:
                q.put((int(ms), fn))
        except Exception:
            pass

    def _ui_poll_tick(self):
        """Main-Thread-Ticker: _ui_queue abarbeiten (alle 30 ms).
        Faellige Eintraege (ms abgelaufen) ausfuehren, Rest behalten."""
        try:
            if getattr(self, "_closed", False):
                return
            import time as _t
            now = _t.monotonic()
            q = getattr(self, "_ui_queue", None)
            rest = []
            try:
                while True:
                    rest.append(q.get_nowait())
            except Exception:
                pass
            for (ms, fn, t0) in rest:
                if (now - t0) * 1000.0 >= ms:
                    try:
                        fn()
                    except Exception:
                        pass
                else:
                    try:
                        q.put((ms, fn, t0))
                    except Exception:
                        pass
        except Exception:
            pass
        finally:
            try:
                self._ui_tick_id = None
                if not getattr(self, "_closed", False):
                    self._ui_tick_id = self.after(30, self._ui_poll_tick)
            except Exception:
                pass

    def _set_prog_geo(self, w, h):
        """Fenster per Code auf w/h setzen (User-/Test-Resize): Veto-Zaehler
        zuruecksetzen + Ziel merken, damit _on_win_configure den
        Resize als gewollt erkennt (kein Selbst-Schrumpfen)."""
        self._shrink_veto_n = 0
        self._prog_geo = (w, h)
        try:
            self.geometry(f"{w}x{h}")
        except Exception:
            pass

    def fit_window_small(self, w=480, h=430):
        """Fenster per Code verkleinern (fuer Tests + Hilfe-Tipp): nutzt
        _set_prog_geo, damit der Shrink-Veto den Resize als gewollt
        erkennt statt ihn zurueckzustellen."""
        self._set_prog_geo(w, h)

    def _on_win_configure(self, ev):
        """Nur echte USER-Groessenaenderungen fitten (Shrink-Wrap-Block).
        Das Fenster schrumpft beim Start von selbst mit dem Inhalt mit
        (511x414 -> 413x309): ECHTE Verkleinerungen ohne User-Resize sind
        keine Verkleinerungsaufforderung, sondern das Symptom. Darum:
        Verkleinerungen werden grundsaetzlich IGNORIERT (Fenster wird auf
        die letzte Groesse zurueckgestellt); nur Vergroesserungen (User
        zieht auf, z.B. 900x700) loesen einen Fit aus (darf schrumpfen,
        weil Ziel groesser ist). User-Verkleinerung: Wer das Fenster per
        Maus laenger gedrueckt kleiner zieht (3 Vetos in Folge an der
        selben Kante), meint es ernst -> Fit geben (einmalig)."""
        if ev.widget is not self:
            return
        if self._startup or self._fitting:
            return  # Startphase / Fit laeuft: nur _startup_fit entscheidet
        wh = (ev.width, ev.height)
        # Maximieren/Ent-Maximieren (Wunsch Patrick): Der WM meldet den
        # Statuswechsel ueber state() == 'zoomed'. Beim Ent-Maximieren
        # schrumpft das Fenster schlagartig -> OHNE Sonderfall wuerde der
        # Shrink-Veto das Fenster per geometry auf Maximiert-Groesse
        # zurueckstellen (Bug: blieb maximiert). Darum: Statuswechsel
        # akzeptieren (Merkstand + Fit), Veto-Zaehler zuruecksetzen.
        # HINWEIS 30.09.2026: state() meldet unter Linux/X11 beim
        # Ent-Maximieren NICHT immer 'zoomed'->'normal' (KDE: bleibt teils
        # 'normal' mit WM-Attribut). Fallback: GROSSER Sprung (>40% einer
        # Achse) in EINEM Configure = WM-Aktion (kein Inhalts-Schrumpfen,
        # das laeuft in kleinen Steps) -> ebenfalls akzeptieren.
        try:
            _zoomed = (self.state() == "zoomed")
        except Exception:
            _zoomed = False
        _state_flip = (_zoomed != getattr(self, "_was_zoomed", False))
        _big_jump = False
        try:
            _lw, _lh = self._last_win_wh
            if _lw > 0 and _lh > 0:
                dw = abs(ev.width - _lw) / float(_lw)
                dh = abs(ev.height - _lh) / float(_lh)
                _big_jump = (dw > 0.40 or dh > 0.40)
        except Exception:
            _big_jump = False
        if _state_flip or _big_jump:
            self._was_zoomed = _zoomed
            self._shrink_veto_n = 0
            self._prog_geo = None
            self._last_win_wh = wh
            self._queue_fit_zoom(allow_shrink=True)
            return
        if wh == self._last_win_wh:
            self._shrink_veto_n = 0
            return  # Echo ohne Groessenaenderung -> ignorieren
        lw, lh = self._last_win_wh
        if ev.width < lw or ev.height < lh:
            # Selbst-Schrumpfen (kein User-Resize): Fenster zurueckstellen,
            # KEIN Fit (wuerde die Spirale naehren). Nur Merkstand halten.
            # Ausnahme: User zieht aktiv kleiner (Veto-Zaehler laeuft voll)
            # ODER Programm-Geometrie (z.B. Test/WM setzt gezielt) -> Fit.
            import time as _t
            now = _t.monotonic()
            prog = getattr(self, "_prog_geo", None)
            if prog is not None and abs(ev.width - prog[0]) <= 2 and abs(ev.height - prog[1]) <= 2:
                self._prog_geo = None  # eigene geometry() angekommen
                self._shrink_veto_n = 0
                self._last_win_wh = wh
                self._queue_fit_zoom(allow_shrink=True)
                return
            if now - self._shrink_veto_t > 1.5:
                self._shrink_veto_n = 0
            self._shrink_veto_t = now
            self._shrink_veto_n += 1
            if self._shrink_veto_n >= 5:
                self._shrink_veto_n = 0
                self._last_win_wh = wh
                self._queue_fit_zoom(allow_shrink=True)
                return
            try:
                self.geometry(f"{lw}x{lh}")
            except Exception:
                pass
            return
        self._shrink_veto_n = 0
        self._prog_geo = None  # Vergroesserung angekommen -> Anker frei
        self._last_win_wh = wh
        self._queue_fit_zoom(allow_shrink=True)  # echte Vergroesserung

    def _startup_fit(self):
        """Genau EIN Start-Fit, sobald das Fenster sichtbar ist. Falls das
        Fenster noch nicht gemappt/vermessbar ist, spaeter erneut versuchen
        (weiterhin in der Start-Sperre, kein Zwischen-Fit von aussen).
        Start-Prinzip 30.09.2026 (Wunsch Patrick): natuerliche Brettgroesse
        (zoom=0.30) – KEIN Vollbild, KEIN
        Fenster-Fit. geometry-Anker + genau 1 _layout_boardbox/draw, damit
        Tk danach nicht mehr von selbst mitschrumpft. User-Resize +
        Maximieren danach normal moeglich (_on_win_configure mit
        _was_zoomed/Big-Jump bleibt unveraendert)."""
        try:
            if not self.winfo_viewable() or self.winfo_width() < 50:
                try:
                    self._startup_after = self.after(100, self._startup_fit)
                except Exception:
                    pass
                return
            self.update_idletasks()
        except Exception:
            try:
                self._startup_after = self.after(100, self._startup_fit)
            except Exception:
                pass
            return
        self._startup = False
        self._prog_geo = None
        try:
            self.update_idletasks()
            # Natuerliche Startgroesse: Brett aus Kachel x 0.30 aufbauen,
            # DANN Fenster per geometry-Anker darauf fixieren (Tk darf
            # danach nicht mehr von selbst mit dem Inhalt mitschrumpfen).
            # User-Resize bleibt moeglich (geometry ist kein minsize/maxsize).
            self.zoom = 0.30
            self.canvas.config(width=COLS * self.cell, height=self.canvas_h())
            self._layout_boardbox()
            self.draw()
            self._scale_chrome()
            self.update_idletasks()
            try:
                req_w = self.winfo_reqwidth()
                req_h = self.winfo_reqheight()
            except Exception:
                req_w, req_h = 0, 0
            try:
                scr_w = self.winfo_screenwidth()
                scr_h = self.winfo_screenheight()
            except Exception:
                scr_w, scr_h = 0, 0
            if req_w > 0 and req_h > 0:
                gw, gh = req_w, req_h
                if scr_w > 0 and scr_h > 0:
                    # Sicherheitskappe: natuerlich, aber nie groesser als
                    # der Bildschirm (minus Taskleisten-Rand).
                    gw = min(gw, max(200, scr_w - 40))
                    gh = min(gh, max(200, scr_h - 80))
                self.geometry(f"{gw}x{gh}")
            else:
                gw, gh = self.winfo_width(), self.winfo_height()
                self.geometry(f"{gw}x{gh}")
            self.update_idletasks()
            self._last_win_wh = (self.winfo_width(), self.winfo_height())
        except Exception:
            pass

    def _queue_fit_zoom(self, allow_shrink=False):
        """Zoom-Neuberechnung debounced anstossen (Fenster-Resize).
        allow_shrink=True nur bei echtem User-Resize; reine Echo-Fits
        duerfen nicht nachschrumpfen."""
        if allow_shrink:
            self._pending_shrink = True
        if self._resize_after is not None:
            try:
                self.after_cancel(self._resize_after)
            except Exception:
                pass
        self._resize_after = self.after(150, self._fire_fit_zoom)

    def _fire_fit_zoom(self):
        allow, self._pending_shrink = self._pending_shrink, False
        self.fit_zoom_to_window(allow_shrink=allow)

    def on_box_resize(self, ev):
        """Boardbox-Resize -> alle Kinder auf Boardbreite zwingen (debounced).
        Der 1. Durchlauf (ev.width != Soll) triggert genau einen 2. Lauf,
        danach ist alles exakt und es kehrt Ruhe ein."""
        want = COLS * self.cell
        if abs((ev.width or 0) - want) <= 1:
            return
        if self._box_after is not None:
            try:
                self.after_cancel(self._box_after)
            except Exception:
                pass
        self._box_after = self.after(30, self._layout_boardbox)

    def _layout_boardbox(self):
        """Alle Kinder der Boardbox auf exakt Boardbreite setzen.
        (Grid-Propagation bleibt AN -> kein Kollaps; die explizite
        Breite gewinnt gegen den Stretch der breiteren Buttons.)"""
        self._box_after = None
        try:
            w = COLS * self.cell
            self.canvas.config(width=w)
            self.canvas.config(height=self.canvas_h())
            for b in self.bar_buttons:
                b.config(width=1)
            self.bar.update_idletasks()
            self.boardbox.update_idletasks()
        except Exception:
            pass

    def score_h(self):
        # Fix: Score-Hoehe NICHT vom Zoom abhaengig machen (sonst Feedback-Loop:
        # groesserer Zoom -> hoehere Leiste -> weniger Platz -> kleinerer Zoom ...).
        return 44

    def board_h(self):
        return ROWS * self.cell

    def canvas_h(self):
        return self.board_h() + self.score_h()

    def fit_zoom_to_window(self, allow_shrink=True):
        """Auto-Zoom: Breite aus der FENSTER-Breite (Fenster - Infobox),
        Hoehe aus der HOLDER-Hoehe (Reihe mit weight=1 = voll verfuegbar).
        NICHT aus der Holder-Breite: Die folgt dem Brett (Spalte weight=0)
        und wuerde eine Schrumpf-Spirale ausloesen (kleines Brett -> kleine
        Holder-Breite -> kleinerer Zoom -> noch kleineres Brett ...).
        Reentrancy-Guard: kein Fit im Fit (Folge-Configures sind Echos und
        werden von _on_win_configure anhand der Fenstergroesse erkannt).
        Shrink-Guard: Nachsetz-Fits aus Inhalts-Echos duerfen den Zoom nicht
        weiter verkleinern (nur echte User-Verkleinerung = kleineres Fenster
        -> _on_win_configure -> neuer Fit darf schrumpfen)."""
        if self._fitting:
            return
        self._fitting = True
        try:
            self._fit_zoom_inner(allow_shrink=allow_shrink)
        finally:
            self._fitting = False

    def _fit_zoom_inner(self, allow_shrink=True):
        """Eigentliche Zoom-Berechnung (wird von fit_zoom_to_window
        mit Reentrancy-Guard aufgerufen)."""
        self._resize_after = None
        # Merkstand SOFORT auf die aktuelle Fenstergroesse: Folge-Configures
        # aus diesem Fit haben dann dieselbe Groesse und werden als Echo
        # erkannt (kein Nach-Fit), egal ob Tk das Fenster minimal anpasst.
        try:
            self._last_win_wh = (self.winfo_width(), self.winfo_height())
        except Exception:
            pass
        try:
            self.main.update_idletasks()
            win_w = self.winfo_width()
            info_w = self.right_panel.winfo_width() if hasattr(self, "right_panel") else 160
            W = max(100, win_w - info_w - 40)  # 40 = Paddings + Menue-Rand
            H = max(150, self.holder.winfo_height() - 4)
        except Exception:
            return
        if W < 100 or H < 150:
            return
        w0, h0 = self.raw[self.set_no]["back"].size
        bar_h = self.bar.winfo_height() or 40
        chrome_h = self.score_h() + 4 + bar_h  # Scores+Buttons+Pads
        z = min(W / (COLS * w0), (H - chrome_h) / (ROWS * h0))
        # gui2 nutzt 256-px-HiRes-Kacheln (statt 50 px): Die alte Untergrenze
        # 0.3 ergab ~538 px Mindestbreite und blockierte kleine Fenster.
        # 0.08 entspricht ~143 px Brettbreite und stellt das alte Verhalten wieder her.
        z = min(4.0, max(0.08, z))
        if not allow_shrink and z < self.zoom - 0.01:
            return  # Echo-Fit nach Start: kein Nachschrumpfen
        if abs(z - self.zoom) > 0.01:
            self.zoom = z
            self.canvas.config(width=COLS * self.cell, height=self.canvas_h())
            self._layout_boardbox()
            self.draw()
            self._scale_chrome()

    def on_canvas_resize(self, ev):
        """Nicht benutzt (Zoom folgt dem Holder). Nur Altlast-Hueter."""
        return

    # ---------- Brett-Darstellung ----------
    # BitBully: to_array()[spalte][zeile], Zeile 0 = unten.
    # 0=leer, 1=Gelb (Anziehender), 2=Rot (Nachziehender).
    def draw(self, falling=None):
        self.canvas.delete("all")
        self.canvas.config(bg=BOARD_BG)
        cell = self.cell
        t_back = self._tile("back")
        arr = self.board.to_array()
        if self.board.is_game_over() and falling is None:
            win = self._win_cells(arr)
        else:
            win = set()
        for c in range(COLS):
            for row in range(ROWS):
                r_top = ROWS - 1 - row
                # Kachel exakt bis zur naechsten Kante ziehen: bei krummen
                # Zoom-Zellen (z.B. 67.4px) bliebe sonst unten ein
                # BOARD_BG-Streifen sichtbar (blaue Linie).
                x0 = round(c * cell)
                x1 = min(round((c + 1) * cell), round(COLS * cell))
                y0 = round(r_top * cell)
                y1 = min(round((r_top + 1) * cell), round(ROWS * cell))
                v = arr[c][row]
                if v == 0:
                    img = t_back
                    if img.width() != x1 - x0 or img.height() != y1 - y0:
                        # Krumme Zoom-Zelle: PIL-Kachel exakt passend rendern
                        # (PhotoImage geht nicht nachtraeglich; _tile_img
                        # baut direkt auf PIL-Ebene). Referenz halten!
                        pil = self._tile_img("back", x1 - x0, y1 - y0)
                        if pil is not None:
                            key = ("crop", self.set_no, self.zoom, x1 - x0, y1 - y0)
                            img = self.tile_cache.get(key)
                            if img is None:
                                img = ImageTk.PhotoImage(pil)
                                self.tile_cache[key] = img
                else:
                    img = self._tile("yellow" if v == 1 else "red")
                self.canvas.create_image(x0, y0, anchor="nw", image=img)
                if (r_top, c) in win:
                    # Sieg-Doppelring (Fix 30.09.2026):
                    # Gruen AUSSen auf dem Brett (2px Abstand zur Scheibe),
                    # Weiss INNEN auf dem Stein (1px innerhalb der Kante).
                    sr = self.raw[self.set_no].get("stone_r", 0.39)
                    wgreen = max(3, cell // 16)
                    pad = cell * (0.5 - sr) - 2 - wgreen // 2
                    self.canvas.create_oval(x0 + pad, y0 + pad, x0 + cell - pad, y0 + cell - pad,
                                            outline="#00ff00", width=wgreen)
                    wwhite = max(1, cell // 40)
                    pad2 = cell * (0.5 - sr) + 1 + wwhite // 2
                    self.canvas.create_oval(x0 + pad2, y0 + pad2, x0 + cell - pad2, y0 + cell - pad2,
                                            outline="#ffffff", width=wwhite)
                elif self.show_last and self.last_move == (r_top, c) and falling is None:
                    # Letztzug-Ring knapp AUSSERHALB der STEINkante
                    # (Fix 30.09.2026): Radius der LIEGENDEN Farbe
                    # (stone_r_y / stone_r_r per Floodfill der Farbscheibe);
                    # der Ring liegt mit 2px Abstand zur Scheibe, damit
                    # kein Stein ueber den Ring lappen kann.
                    sr = self.raw[self.set_no].get(
                        "stone_r_r" if v == 2 else "stone_r_y",
                        self.raw[self.set_no].get("stone_r", 0.39))
                    wlast = max(2, cell // 25)
                    pad = cell * (0.5 - sr) - 2 - wlast // 2
                    self.canvas.create_oval(x0 + pad, y0 + pad, x0 + cell - pad, y0 + cell - pad,
                                            outline="#ffffff", width=wlast)
        # Hover-Vorschau (Ghost-Stein): Stein des Spielers am Zug
        # (gerade Zuege=Gelb/Anziehender, ungerade=Rot)
        if self.ghost and self.hover_col is not None and not self.board.is_game_over() and falling is None:
            hc = self.hover_col
            if self.board.is_legal_move(hc):
                stone = self.stone_for_move_no(len(self.history))
                img = self._tile(stone + "_ghost")
                h = self.board.get_column_height(hc)
                r_top = ROWS - 1 - h
                self.canvas.create_image(hc * cell, r_top * cell, anchor="nw", image=img)
        # fallender Stein
        if falling is not None:
            col, ypix, stone = falling
            img = self._tile(stone)
            self.canvas.create_image(round(col * cell), round(ypix), anchor="nw", image=img)
        self._draw_scores()
        # Pin (Fix 01.10.2026, 2. Review 2.1): gerade gezeichnete Bilder
        # gegen Cache-Eviction schuetzen (Tcl-Name bleibt gueltig).
        try:
            tiles = getattr(self, "tiles", None)
            if tiles is not None and hasattr(tiles, "pinned"):
                tiles.pinned = set(self.tile_cache.keys())
                tiles._evict()
        except Exception:
            pass

    def _win_cells(self, arr):
        """Alle Felder, die zu einer 4er-Reihe (oder laenger) gehoeren.
        arr: BitBully to_array()[spalte][zeile], Rueckgabe {(r_top, c)} (Bildkoord.)."""
        # In (Reihe_unten, Spalte) umrechnen: einfacher pruefen
        grid = [[arr[c][r] for c in range(COLS)] for r in range(ROWS)]
        found = set()
        for r in range(ROWS):
            for c in range(COLS):
                v = grid[r][c]
                if v == 0:
                    continue
                for dc, dr in ((1, 0), (0, 1), (1, 1), (1, -1)):
                    cells = [(r, c)]
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == v:
                        cells.append((nr, nc))
                        nr += dr
                        nc += dc
                    nr, nc = r - dr, c - dc
                    while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == v:
                        cells.append((nr, nc))
                        nr -= dr
                        nc -= dc
                    if len(cells) >= 4:
                        for (rr, cc) in cells:
                            found.add((ROWS - 1 - rr, cc))
        return found

    def on_hover(self, ev):
        self.set_hover(self._col_from_x(ev.x))

    def set_hover(self, col):
        if col != self.hover_col:
            self.hover_col = col
            if self.anim_after is None:
                self.draw()

    def _col_from_x(self, x):
        col = int(x // self.cell)
        return col if 0 <= col < COLS else None

    def click(self, ev):
        if self.thinking or self.anim_after is not None:
            return
        if ev.y < self.board_h() + 4 and ev.y >= self.board_h():
            return  # Luecke zwischen Brett und Scores
        col = self._col_from_x(ev.x)
        if col is not None and (ev.y < self.board_h() or ev.y >= self.board_h() + 4):
            self.human_move(col)

    # ---------- Spiellogik ----------
    def rebuild(self):
        b = bb.Board()
        for m in self.history:
            b.play(m)
        self.board = b

    def current_player_no(self):
        return 1 if len(self.history) % 2 == 0 else 2

    def current_player_name(self):
        # Brettfarbe am Zug (Gelb/Rot) – ungenutzt ausser hier als Referenz;
        # die Anzeige nutzt current_player_label (echte Spieler-Identitaet).
        return cfs_lang.t("color_yellow" if self.current_player_no() == 1
                           else "color_red")

    def current_player_label(self):
        """Wer ist am Zug? Echte Identitaet statt 'Spieler 1/2' (Wunsch
        Patrick 30.09.2026): im Turnier die Seite am Zug (mit
        Farbwechsel-Logik, inkl. User-(p,s,w)-Zusatz); im Normalmodus die
        Seite am Zug (Mensch oder Engine-Stufe, ueber history-Paritaet +
        _human_first); im 2-Spieler-Modus 'Mensch'; beim Ausspielen die
        Engine-Stufe (immer Perfekt)."""
        try:
            if self._match_mode():
                try:
                    return self._stufe_label_for(self._match_side_stufe(),
                                                 mit_psw=True)
                except Exception:
                    pass
        except Exception:
            pass
        try:
            if self.two_player:
                return cfs_lang.t("level_human")
        except Exception:
            pass
        try:
            if self._selfplay_mode():
                return self._stufe_label_for(self._stufe_key(), mit_psw=True)
        except Exception:
            pass
        # Normalmodus Mensch-Computer: WER ist gerade am Zug?
        # _human_first=True -> Mensch zog ungerade Zuege (1,3,5...).
        try:
            n = len(self.history)
            mensch_ungerade = bool(getattr(self, "_human_first", True))
            am_zug_ungerade = (n % 2 == 0)  # naechster Zug ungerade?
            if am_zug_ungerade == mensch_ungerade:
                return cfs_lang.t("level_human")
            return self._stufe_label_for(self._stufe_key(), mit_psw=True)
        except Exception:
            pass
        return cfs_lang.tf("player_n", n=self.current_player_no())

    def _score_font(self):
        return ("TkDefaultFont", max(8, int(round(9 * self.zoom))))

    def _stone_icon(self, stone, size=28):
        """Kleiner Stein (rot/gelb) fuers Am-Zuge-Feld, groessen-cached.
        Referenz zusaetzlich in _turn_icons halten (Fix 01.10.2026,
        2. Review 2.2: reiner Cache + FIFO-Eviction konnte das gerade
        angezeigte Icon aus Tcl loeschen)."""
        key = (self.set_no, stone, size)
        im = self.tile_cache.get(key)
        if im is None:
            raw = self.raw[self.set_no][stone].resize((size, size), Image.LANCZOS)
            im = ImageTk.PhotoImage(raw)
            self.tile_cache[key] = im
        try:
            self._turn_icons[key] = im
        except Exception:
            pass
        return im

    def _update_turn(self):
        stone = "yellow" if self.current_player_no() == 1 else "red"
        size = max(16, min(40, int(round(24 * self.zoom))))
        try:
            self.turn_img.config(image=self._stone_icon(stone, size))
        except Exception:
            pass
        self.turn_var.set(self.current_player_label())

    def _scale_chrome(self):
        """Buttons: feste, kompakte Schrift (NICHT Zoom-skaliert).
        Zoom-skalierte Button-Fonts aendern die Leistenhoehe -> das veraendert
        die Zoom-Berechnung -> Brett springt bei jedem Zug. Deshalb fix."""
        try:
            for b in self.bar_buttons:
                b.config(font=("TkDefaultFont", 9), wraplength=0)
        except Exception:
            pass

    def _draw_scores(self):
        """Score-Zeile direkt im Canvas: pixel-exakt unter jeder Spalte,
        mit 1px-Trennlinien (kein Grid -> kein Rundungsdrift).
        Ohne Analyse: nur Spaltennummern. Mit Analyse: oben gross +,-,=
        (passend zur Farbe), unten klein die Zugzahl bis zum Ende."""
        y0 = self.board_h()
        h = self.score_h()
        cell = self.cell
        fs_big = ("TkDefaultFont", max(9, min(16, int(round(13 * self.zoom)))), "bold")
        fs_val = ("TkDefaultFont", max(8, min(12, int(round(9 * self.zoom)))))
        base = "#d9d9d9"
        for c in range(COLS):
            x0, x1 = c * cell, (c + 1) * cell
            if self.last_scores is None:
                top, sub, bg = str(c + 1), "", base
            else:
                top, sub, bg = self.last_scores[c]
            self.canvas.create_rectangle(x0, y0, x1, y0 + h, fill=bg, outline="#888888")
            cx = (x0 + x1) // 2
            if sub:
                # Analyse: oben NUR das Zeichen, unten NUR die Zahl
                self.canvas.create_text(cx, y0 + int(h * 0.28), text=top,
                                        font=fs_big, fill="black")
                self.canvas.create_text(cx, y0 + int(h * 0.72), text=sub,
                                        font=fs_val, fill="black")
            else:
                self.canvas.create_text(cx, y0 + h // 2, text=top,
                                        font=fs_val, fill="black")

    def _set_scores(self, mapping):
        """mapping: Spalte -> (Text, BG-Farbe). Danach neu zeichnen."""
        self.last_scores = mapping
        self.draw()

    def _clear_scores(self, silent=False):
        """Analyse aus: nur Spaltennummern. Loescht die Wertungs-Info
        (silent=True laesst sie stehen, z.B. Engine-Kennzahlen)."""
        base = "#d9d9d9"
        m = {}
        for c in range(COLS):
            if self.board.is_legal_move(c):
                m[c] = (str(c + 1), "", base)
            else:
                m[c] = ("X", "", "#a0a0a0")
        self._set_scores(m)
        if silent:
            return
        for key in ("Wert", "Tiefe", "Kn", "Zeit", "Kn/s", "Buch"):
            try:
                self.info_vars[key].set("\u2013")
            except Exception:
                pass
        try:
            self.info_vars["Stufe"].set(self._stufe_label())
        except Exception:
            pass

    def stone_for_move_no(self, n):
        # Zugnummer n (0-basiert): Gelb beginnt -> gerade=Gelb
        return "yellow" if n % 2 == 0 else "red"

    def human_move(self, col):
        # Waerend die Engine rechnet: keine Zuege annehmen (sonst Doppelzug
        # mit kaputten Farben; Fix 01.10.2026, 2. Review). Auch Tasten 1-7
        # laufen hierher und werden so abgewiesen.
        if self.thinking:
            self.status.set(cfs_lang.t("status_wait_thinking"))
            return
        # Turnier mit Mensch-Seite: Zuege sind erlaubt, wenn GERADE der
        # Mensch am Zug ist (sonst wuerde man der Engine dazwischenfunken).
        # Ausserhalb des Turniers gilt die alte Sperrlogik.
        if self._match_mode():
            if not self._match_human_turn():
                self.status.set(cfs_lang.t("status_match_running"))
                return
        elif self._selfplay_mode():
            self.status.set(cfs_lang.t("status_selfplay_running"))
            return
        if self.board.is_game_over():
            self.status.set(cfs_lang.t("status_game_over_new"))
            return
        if not self.board.is_legal_move(col):
            self.status.set(cfs_lang.tf("status_column_full", col=col + 1))
            return
        stone = self.stone_for_move_no(len(self.history))
        self.history.append(col)
        self.future.clear()
        self.rebuild()  # last_move berechnet sich live aus history+board
        if self.anim and self._gui_alive():
            self.drop_animation(col, stone, lambda: self.after_human())
        else:
            self.anim_after = None
            self.refresh()
            self.after_human()

    def _gui_alive(self):
        """True, solange das Tk-Fenster existiert (Headless-Tests ausgenommen)."""
        try:
            self.winfo_exists()
            return True
        except Exception:
            return False

    def after_human(self):
        if self.board.is_game_over():
            self.finish_info()
            # Turnier mit Mensch-Seite: Partie werten (ggf. 3 s Pause
            # -> naechste Partie, siehe _match_finish_game).
            if self._match_mode():
                self._match_finish_game()
                return
            # Normales Mensch-vs-Computer-Spiel: Spielstand einbuchen.
            # Regel (Wunsch Patrick): WER den letzten (Sieg-)Zug machte,
            # bekommt den Punkt. Der Zuletzt-Zieher = Gewinner steht per
            # Brett fest (winner 1 <-> Gelb zog zuletzt <-> history ungerade;
            # Ausnahme nur bei inkonsistenten Stellungen wie abgebrochenen
            # Alt-Partien — dann entscheidet die history-Laenge, NICHT der
            # Gewinner). Mensch-Anteil: _human_first=True -> Mensch zog die
            # ungeraden Zuege (1,3,5...), sonst die geraden (2,4,6...).
            # Das deckt ALLE Faelle ab: Mensch Gelb/Rot, Computer beginnt
            # per 'ziehen', Vorgabe-/Zufallsstellungen (3 Steine -> weiter
            # mit Zug 4 = Rot: _random_done setzt _human_first=False).
            if not self.two_player and not self._selfplay_mode():
                try:
                    w = self.board.winner()
                except Exception:
                    w = None
                try:
                    if w in (None, 0):
                        self._stand_book_normal(None)
                    else:
                        n = len(self.history)
                        zuletzt_ungerade = (n % 2 == 1)
                        mensch_ungerade = bool(
                            getattr(self, "_human_first", True))
                        self._stand_book_normal(
                            zuletzt_ungerade == mensch_ungerade)
                except Exception:
                    pass
            return
        if self._selfplay_mode():
            self.engine_move()
            return
        # Turnier: Mensch hat gezogen -> Engine-Seite antwortet (falls die
        # naechste Seite kein Mensch ist; bei Mensch-vs-Mensch warten).
        if self._match_mode():
            try:
                if self._match_side_stufe() != "mensch":
                    self.engine_move(stufe=self._match_side_stufe())
            except Exception:
                pass
            return
        if not self.two_player and self.opp_var.get() == "Computer":
            self.engine_move()

    @property
    def last_move(self):
        """Letzter Zug = oberster Stein der zuletzt gespielten Spalte.
        Wird live aus history+board berechnet (nicht gespeichert) -> immer
        korrekt, egal ob Mensch, Engine, Undo/Redo, Laden oder Zufall."""
        if not self.history:
            return None
        col = self.history[-1]
        try:
            h = self.board.get_column_height(col)
        except Exception:
            return None
        if h <= 0:
            return None
        return (ROWS - h, col)

    def drop_animation(self, col, stone, done, row=0):
        target_h = self.board.get_column_height(col)
        target_top = ROWS - target_h
        cell = self.cell
        if row >= target_top:
            self.anim_after = None
            self.refresh()
            done()
            return
        self.draw(falling=(col, row * cell, stone))
        self.anim_after = self.after(16, lambda: self.drop_animation(col, stone, done, row + 1))

    def _move_stufe(self):
        """Stufe fuer den GERADE zu spielenden Zug (Match > Selbstspiel).
        (Logik in cfs_levels.move_stufe.)"""
        return cfs_levels.move_stufe(self)

    USER_KEYS = cfs_levels.USER_KEYS

    @classmethod
    def _user_psw_for(cls, key):
        """(p,s,w) zur User-Seite (Logik in cfs_levels, Klassenattribute)."""
        return cfs_levels.user_psw_for(cls, key)

    @classmethod
    def _is_user_key(cls, key):
        return cfs_levels.is_user_key(key)

    @classmethod
    def _stufen_werte(cls, key):
        """(key, patzerquote, s, w) zu einem Stufenschluessel (s. cfs_levels)."""
        return cfs_levels.stufen_werte(cls, key)

    def _display_stufe_label(self):
        """Stufen-Name fuer die Infobox (Logik in cfs_levels)."""
        return cfs_levels.display_stufe_label(self)

    def _stufe_key(self):
        """Stufenschluessel thread-sicher lesen (s. cfs_levels)."""
        return cfs_levels.stufe_key(self)

    def _stufe_label_for(self, key, mit_psw=False):
        """Stufen-Anzeigename zu einem Schluessel (s. cfs_levels)."""
        return cfs_levels.stufe_label_for(self, key, mit_psw=mit_psw)

    def _opp_key(self):
        """Gegnermodus thread-sicher lesen (Cache bei Worker-Threads)."""
        try:
            return self.opp_var.get()
        except Exception:
            if getattr(self, "selfplay", False):
                return "Computer-Computer (ausspielen)"
            return "Computer" if not self.two_player else "2-Spieler (beide Mensch)"

    def _selfplay_mode(self):
        """True, wenn Computer-Computer (ausspielen) aktiv ist.
        Radio-Variable ODER Flag (Radio klikt erst beim naechsten
        mainloop-Durchlauf sauber um -> Flag sichert sofort)."""
        if getattr(self, "selfplay", False):
            return True
        try:
            return self.opp_var.get() == "Computer-Computer (ausspielen)"
        except Exception:
            return False

    def _solver_busy(self):
        """True, wenn gerade eine Berechnung laeuft (Engine-Zug/Analyse)."""
        return bool(self.thinking or self._ana_busy)

    def _confirm_no_book(self, what):
        # Altlast: Buch ist fest verdrahtet, keine Bestaetigung mehr noetig.
        return True

    def engine_move(self, stufe=None):
        """Einen Computer-Zug anstossen. stufe (optional): Stufe NUR fuer
        diesen Zug (Match-Modus: Gelb/Rot spielen verschiedene Stufen).
        Wird in _match_stufe zwischengespeichert -> Worker liest pro Zug
        die richtige Stufe, GUI-Variable bleibt unberuehrt.
        Normalmodus: Computer zieht bei LEEREM Brett -> er beginnt
        (_human_first=False, Mensch ist Rot); sonst begann der Mensch."""
        if self.thinking or self.board.is_game_over():
            return
        if (not self._match_mode() and not self.two_player
                and not self._selfplay_mode() and not len(self.history)):
            try:
                self._human_first = False
            except Exception:
                pass
        self.thinking = True
        self.cancel = False
        if stufe == "mensch" or stufe in ("user1", "user2", "verlierer"):
            self._match_stufe = stufe
        else:
            _ok = (stufe in self.STUFEN or stufe in ("user1", "user2", "verlierer")) if stufe else False
            self._match_stufe = stufe if _ok else None
        # Match: Statuszeile bleibt auf dem Stand (kein 'denkt...' pro Zug).
        if not self._match_mode():
            self.status.set(cfs_lang.t("status_thinking"))
        threading.Thread(target=self._engine_thread, daemon=True).start()

    def pick_engine_move(self, board, on_progress=None):
        """Engine-Zugwahl (iterative Vertiefung wie ein Schachprogramm).

        - Sucht Tiefe 4, 6, 8, ... bis Vollsuche (-1); TT bleibt zwischen
          den Stufen erhalten (Wiederverwendung). Nach jeder Stufe meldet
          on_progress(Tiefe, Score, Knoten, Sekunden) -> GUI zeigt live
          Tiefe/kKn/Zeit wie ein Schach-Infofenster. Stop/Neustart prueft
          self.cancel / self._ana_seq -> Abbruch zwischen den Stufen.
        - Analyse: immer volle Staerke (perfekt), damit alle-Zuege ehrlich bleibt.
        - Spielzug: Stufen-Tabelle STUFEN (p, s, w). Patzerquote =
          (100-p)/100: Zufall immer (Sonderfall), Sehr Leicht 75%,
          Leicht 60%, Anfaenger 50%, Fortgeschritten 80%,
          Taktiker immer (p=0, Sonder-Stil: nie perfekt, nur s/w-Filter),
          Mittel 50%, Fordernd 45%, Schwer 35%, Sehr Schwer 30%,
          Experte 20%, Meister 15%, Starker Meister 8%, Perfekt 0%.
          Stufe 0 Verlierer (Spass-Stufe, kein p/s/w): nimmt zufaellig
          einen Verlustzug (Score < 0); Fallback erst '='-Zuege (Remis),
          dann Zufall aus allen (wenn alles gewinnt).
          Verlustschutz s in Gegnerzuegen (tabu, wenn ml <= 2*s):
          0er ohne Filter (Zufall/Sehr Leicht/Leicht/Anfaenger),
          1er nicht im 1. Gegnerzug (Fortgeschritten/Mittel/Fordernd/
          Schwer), 2er nicht in 2 (Sehr Schwer/Experte),
          3er nicht in 3 (Taktiker/Meister), 4er nicht in 4
          (Starker Meister). Siegsschutz w (Variante B): kurzer Gewinn mit
          ml <= 2*w-1 geht IMMER vor (zufaellig aus der Gewinnmenge),
          p-Wurf nur bei leerer Menge. Faellt sonst alles durch, wird
          der am laengsten durchhaltende Verlustzug genommen.
        - Alles verliert (alle Scores < 0, Perfekt/starke Stufen): gewichtete
          Zufallswahl mit Gewicht = Verlustlaenge^LOSS_POWER.
        Gibt (Spalte, Score, Verlustlaenge|None, Knoten) zurueck."""
        md = -1  # Spielzug: volle Tiefe, Schwaeche kommt aus Patzerquote
        depths = self._iter_depths()
        # Engine-Abbruch: NUR cancel-Flag (kein _ana_seq: Analyse-Neustarts
        # duerfen den laufenden Engine-Zug NICHT entwerten, Bug 28.09.2026).
        # Match-Blindmodus: TT ueber Zuege behalten (keep_tt) -> Partie in
        # Sekunden statt Minuten (Messung 28.09.2026: 41 perfekte Zuege in
        # 1,5 s mit weiterverwendeter TT vs. ~1 s pro Zug mit Reset).
        blind = self._match_mode() and self._match_blind()
        scores, nodes = self._iterative_scores(
            board, depths, on_progress, abort=lambda: self.cancel,
            keep_tt=blind)
        if not scores:
            # Abgebrochen BEVOR Stufe 1 fertig: letzter Versuch mit Tiefe 4
            # (Millisekunden), damit immer ein Zug kommt.
            with self._solver_lock:
                self.agent.reset_node_counter()
                scores = dict(self.agent.score_all_moves(board, max_depth=4))
                nodes = self.agent.get_node_counter()
        if not scores:
            raise ValueError(cfs_lang.t("err_no_legal_move"))
        _key, _err, _schutz, _wschutz = self._move_stufe()
        if _key == "verlierer":
            # Stufe 0 Verlierer (Spass-Stufe): zufaellig einen Verlustzug
            # (Score < 0); Fallback erst '=' (Remis), dann Zufall aus allen
            # legalen Zuegen (wenn alles gewinnt). Kein Filter/Schutz.
            legal = list(board.legal_moves())
            verl = [c for c in legal
                    if scores.get(c) is not None and scores.get(c) < 0]
            if verl:
                c = random.choice(verl)
                return c, scores.get(c, max(scores.values())), None, nodes
            rem = [c for c in legal
                   if scores.get(c) is not None and scores.get(c) == 0]
            if rem:
                c = random.choice(rem)
                return c, scores.get(c, max(scores.values())), None, nodes
            c = self._filtered_blunder(board, scores, 0, None)
            return c, scores.get(c, max(scores.values())), None, nodes
        if _key == "zufall":
            # Stufe 1 Zufall: immer uniform zufaellig, ohne Filter/Analyse.
            c = self._filtered_blunder(board, scores, 0, None)
            return c, scores.get(c, max(scores.values())), None, nodes
        # Siegsschutz (Variante B): kurzer Gewinn geht IMMER vor - auch ohne
        # p-Wurf (zufaellig aus der Gewinnmenge, Varianz erhalten).
        _win = self._short_wins(board, scores, _wschutz)
        if _win:
            c = random.choice(_win)
            return c, scores.get(c, max(scores.values())), None, nodes
        if _err > 0.0 and random.random() < _err:
            c = self._filtered_blunder(board, scores, _schutz, _wschutz)
            return c, scores.get(c, max(scores.values())), None, nodes
        best = max(scores.values())
        if best >= 0:
            # KEIN best_move (Vollsuche dauert zu lang): Der beste Zug
            # aus der letzten iterativen Stufe reicht (Mitte bricht Gleichstand
            # nicht exakt wie best_move, dafuer antwortet die Engine in Sekunden).
            # Beide Anzeige-0-6 (Spalte = col+1).
            # Fix 02.10.2026: schnellster Gewinn wird gespielt (nicht
            # gewuerfelt); Gleichstand im ml -> Zufall unter den
            # gleichschnellen. Liegt kein Gewinn innerhalb 10 Halbzuegen,
            # wird aus allen Gewinnzuegen gewuerfelt (Varianz). Remis
            # (best == 0): Zufall unter allen Remis-Zuegen. Vorher nahm
            # max(...) immer denselben Zug -> keine Varianz.
            cands = [c for c, v in scores.items() if v == best]
            try:
                _legal = set(board.legal_moves())
            except Exception:
                _legal = set(cands)
            cands = [c for c in cands if c in _legal] or list(_legal)
            pool = list(cands)
            if best > 0:
                try:
                    _ml = {c: self._moves_left(board, scores.get(c))
                           for c in cands}
                    _fast = [c for c in cands
                             if _ml.get(c) is not None and _ml.get(c) <= 10]
                    if _fast:
                        _min = min(_ml[c] for c in _fast)
                        pool = [c for c in _fast if _ml[c] == _min]
                except Exception:
                    pool = list(cands)
            col = random.choice(pool)
            return col, scores[col], None, nodes
        if _key == "perfekt":
            # Stufe 14 Perfekt in reiner Verluststellung: Verlustzuege mit
            # ml <= 10 (schnelle Niederlage) werden vermieden (Wunsch
            # 02.10.2026, s=5 im Filter). Faellt alles durch (alles verliert
            # schnell), nimmt der Filter-Fallback deterministisch den Zug,
            # der am laengsten durchhaelt. Sind alle Verluste weiter als
            # 10 Halbzuege entfernt, wird aus allen Verlustzuegen gewuerfelt
            # (Abwechslung statt deterministischem Griff).
            try:
                _all_ml = {c: self._moves_left(board, scores.get(c))
                           for c in board.legal_moves()
                           if scores.get(c) is not None}
            except Exception:
                _all_ml = {}
            if (_all_ml and all(ml is not None and ml > 10
                                for ml in _all_ml.values())):
                _pool = list(_all_ml)
                c = random.choice(_pool)
                return c, scores.get(c, max(scores.values())), None, nodes
            c = self._filtered_blunder(board, scores, 5, None)
            return c, scores.get(c, max(scores.values())), None, nodes
        dist = {}
        for col, s in scores.items():
            with self._solver_lock:
                dist[col] = bb.BitBully.score_to_moves_left(s, board)
        if len(set(dist.values())) <= 1:
            # Alle Distanzen identisch: einmal exakt nachrechnen (mit
            # Distanz-Buch Millisekunden), statt uniform zu wuerfeln.
            try:
                with self._solver_lock:
                    exact = dict(self.agent.score_all_moves(board, max_depth=-1))
                if exact and max(exact.values()) < 0:
                    for col, s in exact.items():
                        with self._solver_lock:
                            dist[col] = bb.BitBully.score_to_moves_left(s, board)
                    scores = exact
            except Exception:
                pass
        weights = {c: float(max(1, d)) ** LOSS_POWER for c, d in dist.items()}
        total = sum(weights.values())
        r = random.random() * total
        for c in sorted(weights):
            r -= weights[c]
            if r <= 0:
                return c, scores[c], dist[c], nodes
        c = max(weights, key=weights.get)
        return c, scores[c], dist[c], nodes

    def _moves_left(self, board, score):
        """moves_left (untere Zahl) zu einem Score, thread-sicher.

        score_to_moves_left ist eine reine Funktion (kein Lock noetig),
        hier trotzdem ueber _solver_lock wie im Rest der Datei."""
        try:
            with self._solver_lock:
                return bb.BitBully.score_to_moves_left(score, board)
        except Exception:
            return None

    def _short_wins(self, board, scores, wschutz):
        """Gewinnmenge des Siegsschutzes (Variante B): alle '+'-Zuege mit
        ml <= 2*w-1 (w=1 -> ml 1, w=2 -> ml 3, ...). w=0/None = aus.
        ml = untere Zahl (Gewinn-/Verlustdistanz aus eigener Sicht)."""
        try:
            w = int(wschutz) if wschutz is not None else 0
        except Exception:
            return []
        if w <= 0:
            return []
        limit = 2 * w - 1
        menge = []
        try:
            legal = list(board.legal_moves())
        except Exception:
            return []
        for c in legal:
            s = scores.get(c)
            if s is None or s <= 0:
                continue  # nur echte Gewinne ('+'), kein Remis
            try:
                with self._solver_lock:
                    ml = bb.BitBully.score_to_moves_left(s, board)
            except Exception:
                continue
            if ml <= limit:
                menge.append(c)
        return menge

    def _filtered_blunder(self, board, scores, cutoff, wschutz=None):
        """Gefilterter Patzer: uniform aus legalen Zuegen, aber Zuege, bei
        denen der Gegner in wenigen Zuegen mattet, sind tabu (s = Schutz
        in Gegnerzuegen: tabu, wenn ml <= 2*s).
        Siegsschutz VORAB (Variante B): ist die Gewinnmenge
        ('+'-Zuege mit ml <= 2*w-1) nicht leer, wird zufaellig daraus
        gewaehlt - der kurze Gewinn geht immer vor (kein Patzer-Wurf).
        Gewinn/Unentschieden sind sonst immer erlaubt. Faellt alles durch
        den Filter, wird der am laengsten durchhaltende Verlustzug genommen.
        Schutz s in GEGNERZUEGEN (STUFEN): 0=aus (Zufall/Sehr Leicht/
        Leicht/Anfaenger), 1 (Fortgeschritten/Mittel/Fordernd/
        Schwer), 2 (Sehr Schwer/Experte), 3 (Taktiker/Meister),
        4 (Starker Meister), Perfekt None (kein Patzer).
        Mass: moves_left = untere Zahl (Gewinn-/Verlustdistanz aus eigener
        Sicht, inkl. dem gerade zu spielenden Stein). Gegner mattet in
        seinem N-ten Zug -> moves_left = 2*N (28.09.2026 an echten
        Stellungen verifiziert: matt in 1 Gegnerzug = ml 2 bei Score
        -18/-16/.../-5, unabhaengig von der Brettfuellung; der reine Score
        taugt NICHT: -18 heisst spaet auch nur noch ml 4/6 ohne Sofort-Matt).
        Regel: tabu, wenn ml <= 2*s (ml=2 <-> matt im 1. Gegnerzug).
        WICHTIG: Der Filter prueft die VOLLEN Endscores (Vollsuche -1).
        Fruehe Abbruch-Tiefen liefern zu optimistische Scores (kein Matt
        erkannt) -> Patzer duerfen NUR aus verifizierten Scores waehlen.
        Remis (score 0) wird NICHT bevorzugt (02.10.2026 gestrichen):
        ein einzelnes Remis gegen lauter Verluste zaehlt wie jeder
        andere erlaubte Zug.
        (Mittel 'ging' nur zufaellig: groessere Cutoffs machen
        den Filter strenger, nicht klueger.)
        cutoff None (Perfekt) darf hier nie ankommen (kein Patzerpfad);
        falls doch -> sicherer Fallback auf laengsten Widerstand."""
        # Siegsschutz zuerst (Variante B): kurzer Gewinn geht immer vor.
        win_menge = self._short_wins(board, scores, wschutz)
        if win_menge:
            return random.choice(win_menge)
        legal = list(board.legal_moves())
        if cutoff is None:
            cutoff = 99
        if cutoff <= 0:
            # Patzer ohne Filter (Stufen 1-4, s=0): uniform aus allen
            # legalen Zuegen (Zufall/Sehr Leicht/Leicht/Anfaenger).
            return random.choice(legal)
        # scores + legal_moves: beide 0-6 (Anzeige-Spalte = c+1).
        limit = 2 * cutoff
        ok = []
        for c in legal:
            s = scores.get(c)
            if s is None:
                ok.append(c)  # ohne Wertung: nicht filtern
                continue
            if s >= 0:
                ok.append(c)  # Gewinn/Unentschieden: immer erlaubt
                continue
            try:
                with self._solver_lock:
                    ml = bb.BitBully.score_to_moves_left(s, board)
            except Exception:
                ok.append(c)
                continue
            if ml <= limit:
                continue  # Gegner mattet in <= cutoff Zuegen -> tabu
            ok.append(c)
        if ok:
            return random.choice(ok)
        # Alles tabu: laengster Widerstand statt sofort aufgeben
        # (groesstes ml = Gegner braucht am laengsten).
        best_c, best_ml = legal[0], -1
        for c in legal:
            s = scores.get(c)
            try:
                ml = (bb.BitBully.score_to_moves_left(s, board)
                      if s is not None and s < 0 else 10 ** 9)
            except Exception:
                ml = 10 ** 9
            if ml > best_ml:
                best_c, best_ml = c, ml
        return best_c

    def _iter_depths(self):
        """Iterative Tiefen bis Vollsuche (-1): 4, 6, 8, 10, 12, 14, 16, 18,
        20, Voll. Das 12-ply-dist-Buch liefert bis 12 Steine sofort Werte,
        danach rechnet die iterative Suche. Max. 1 GUI-Callback/200ms."""
        return [4, 6, 8, 10, 12, 14, 16, 18, 20, -1]

    def _iterative_scores(self, board, depths, on_progress=None, abort=None,
                            keep_tt=False):
        """score_all_moves in Stufen; TT bleibt erhalten (kein Reset dazwischen).
        on_progress(depth, scores, nodes, dt) wird DIREKT im Worker-Thread
        gerufen (muss selbst thread-sicher sein, z.B. per _safe_after).
        Abbruch: abort() -> True (Engine: cancel-Flag, Analyse: _ana_seq).
        keep_tt=True (Match-Blindmodus): KEIN TT-Reset pro Zug -> Folgezuege
        nutzen die Tabelle weiter (Sekunden statt Minuten pro Partie).
        WICHTIG: Callbacks ausserhalb des Locks absetzen (Tk-Update + Lock
        aus anderem Thread = Deadlock, GUI scheint eingefroren)."""
        t0 = time.time()
        last_cb = [0.0]
        scores, nodes = {}, 0
        pending_cb = []
        stop = abort if abort is not None else (lambda: self.cancel)
        with self._solver_lock:
            self.agent.reset_node_counter()
            # TT frisch: erste Stufe (Tiefe 4) braucht sonst Altlast und
            # meldet verzoegert; frische TT = reproduzierbare Stufenfolge.
            # Ausnahme: Match-Blindmodus (keep_tt) -> TT weiterverwenden.
            if not keep_tt:
                try:
                    self.agent.reset_transposition_table()
                except Exception:
                    pass
            for depth in depths:
                try:
                    if stop():
                        break
                except Exception:
                    pass
                try:
                    part = self.agent.score_all_moves(board, max_depth=depth)
                except Exception:
                    break
                scores, nodes = dict(part), self.agent.get_node_counter()
                self._last_depth = depth
                dt = time.time() - t0
                # GUI-Throttle: max. 1 Callback/200ms + immer die letzte Stufe.
                # Nur vormerken; abgesetzt wird NACH dem Lock (kein Deadlock).
                if on_progress is not None and (depth == depths[-1] or
                                                 dt - last_cb[0] >= 0.2):
                    last_cb[0] = dt
                    pending_cb.append((depth, dict(scores), nodes, dt))
                if depth == -1:
                    break
                try:
                    if stop():
                        break
                except Exception:
                    pass
        for (depth, s, n, t) in pending_cb:
            # on_progress MUSS thread-sicher sein (Worker-Kontext!).
            # Fehler hier duerfen den Zug NIE killen (Bug 28.09.2026:
            # stiller Thread-Tod nach PICK fertig -> kein _engine_done).
            try:
                on_progress(depth, s, n, t)
            except Exception:
                import traceback as _tb3
                _tb3.print_exc()
        return scores, nodes

    def _engine_thread(self):
        t0 = time.time()
        snap_seq = self._ana_seq
        # Snapshot der Stellung bei Start (Fix 01.10.2026, 2. Review):
        # _engine_done verwirft das Ergebnis, falls sich history seither
        # geaendert hat (Navigation/Laden waehrend des Denkens).
        try:
            snap_hist = list(self.history)
        except Exception:
            snap_hist = None

        def prog(depth, scores, nodes, dt):
            # Live-Info waehrend der Suche (wie Schach-Infofenster).
            # NUR Thread-sicheres: Werte VORHER in reine Python-Typen
            # kopieren (direkte info_vars/status-Sets aus dem Worker werfen
            # RuntimeError, sobald der Mainloop laeuft -> Thread starb
            # still, Bug 28.09.2026). stufe_txt fix pro Zug: _match_stufe
            # wird pro Zug gesetzt (Match: Gelb/Rot-Seite), sonst GUI-Stufe.
            if snap_seq != self._ana_seq:
                return
            try:
                best = max(scores.values())
            except Exception:
                return
            label = cfs_lang.t("depth_full") if depth == -1 else str(depth)
            ms_stufe = getattr(self, "_match_stufe", None)
            try:
                if ms_stufe == "mensch" or ms_stufe in ("user1", "user2", "verlierer"):
                    stufe_txt = self._stufe_label_for(ms_stufe)
                elif ms_stufe in self.STUFEN or ms_stufe == "verlierer":
                    stufe_txt = self._stufe_label_for(ms_stufe)
                else:
                    stufe_txt = self._stufe_label()
            except Exception as e:
                import traceback as _tbp
                _tbp.print_exc()
                stufe_txt = "?"
            try:
                kn_txt = f"{int(nodes):,d}".replace(",", ".")
            except Exception:
                kn_txt = "?"
            try:
                ms = max(1, int(round(dt * 1000)))
            except Exception:
                ms = 1
            try:
                kns_txt = self._kns_text(nodes, dt)
            except Exception as e:
                import traceback as _tbk
                _tbk.print_exc()
                kns_txt = "?"
            try:
                stat_txt = cfs_lang.t("status_thinking")
            except Exception:
                stat_txt = cfs_lang.t("status_thinking")
            # Match: Statuszeile bleibt auf dem Stand stehen (ruhig);
            # Infobox-Stufe zeigt die Seite am Zug (fix pro Partie-Zug).
            # Blindmodus: gar keine Live-Callbacks (sonst Queue-Stau).
            if self._match_mode() and self._match_blind():
                pass
            elif self._match_mode():
                try:
                    self._safe_after(0, lambda st=stufe_txt:
                                     self._match_prog_ui(st))
                except Exception:
                    import traceback as _tbs
                    _tbs.print_exc()
            else:
                try:
                    self._safe_after(0, lambda lb=label, kk=kn_txt, mm=ms, ks=kns_txt,
                                     st=stufe_txt, sa=stat_txt:
                                     self._engine_prog_ui(lb, kk, mm, ks, st, sa))
                except Exception:
                    import traceback as _tbs
                    _tbs.print_exc()

        try:
            col, _score, _dist, _nodes = self.pick_engine_move(self.board, on_progress=prog)
        except Exception as e:
            import traceback as _tb
            _tb.print_exc()
            self._safe_after(0, lambda err=str(e): self._engine_failed(err))
            return
        dt = time.time() - t0
        try:
            self._safe_after(0, lambda c=col, d=dt, nd=_nodes, sc=_score, sh=list(snap_hist) if snap_hist is not None else None: self._engine_done(c, d, nd, sc, sh))
        except Exception:
            import traceback as _tb2
            _tb2.print_exc()

    def _match_prog_ui(self, stufe_txt):
        """Match-Live-Anzeige im GUI-Thread: NUR Infobox-Stufe der Seite am
        Zug (Tiefe/kKn/Zeit bleiben stehen -> ruhige Infobox, keine
        50-ms-Flackerzahlen). Statuszeile wird NICHT angefasst."""
        try:
            self.info_vars["Stufe"].set(stufe_txt)
        except Exception:
            pass

    def _engine_prog_ui(self, label, kn_txt, ms, kns_txt, stufe_txt, stat_txt):
        """Live-Info im GUI-Thread (vom Worker per _safe_after gerufen).
        Die Statuszeile bleibt dabei ruhig: Im Match-Modus wird sie NICHT
        bei jedem Zug neu geschrieben (Wunsch Patrick), sonst nur das
        feste 'Computer denkt...'."""
        try:
            self.info_vars["Tiefe"].set(f"{label}...")
        except Exception:
            pass
        try:
            self.info_vars["Kn"].set(kn_txt)
        except Exception:
            pass
        try:
            self.info_vars["Zeit"].set(f"{ms} ms")
        except Exception:
            pass
        try:
            self.info_vars["Kn/s"].set(kns_txt)
        except Exception:
            pass
        try:
            self.info_vars["Stufe"].set(stufe_txt)
        except Exception:
            pass
        try:
            if self._match_mode():
                return  # Match: Statuszeile bleibt auf dem Stand stehen
            self.status.set(stat_txt)
        except Exception:
            pass

    def _engine_failed(self, err):
        self.thinking = False
        if self._match_mode():
            self._match_cancelled()
            return
        self.status.set(cfs_lang.tf("status_computer_error", err=err))

    def _engine_done(self, col, dt, nodes=0, score=None, snap=None):
        self.thinking = False
        if self.cancel:
            if self._match_mode():
                self._match_cancelled()
            else:
                self.status.set(cfs_lang.t("status_aborted"))
            return
        # Snapshot-Check (Fix 01.10.2026, 2. Review): Wurde waehrend der
        # Berechnung navigiert/geladen (undo/redo/Neu/Laden), ist der Stand
        # fremd -> Ergebnis verwerfen statt anzuhaengen. Mit thinking-Guard
        # in human_move/_nav_blocked + stop() in new_game/load_pos ist das
        # nur noch Sicherheitsnetz (z.B. Match-Sonderwege).
        if snap is not None:
            try:
                if list(self.history) != list(snap):
                    self.status.set(cfs_lang.t("status_discarded"))
                    self.refresh()
                    return
            except Exception:
                pass
        stone = self.stone_for_move_no(len(self.history))
        # Analyse-Wert des gespielten Zugs (Fix 03.10.2026): ml (Steinzahl
        # bis Ende) aus der VOR-Zug-Stellung + Score der Zugberechnung
        # bestimmen, BEVOR history/board fortgeschrieben werden (danach
        # waere score_to_moves_left mit dem Nach-Zug-Brett falsch).
        try:
            _ml_played = self._moves_left(self.board, score)
        except Exception:
            _ml_played = None
        self.history.append(col)
        self.future.clear()
        self.move_times.append(dt)
        self.rebuild()  # last_move berechnet sich live aus history+board
        # Match-Blindmodus ('Nur Ergebnisse'): kein Zeichnen/Animieren pro
        # Zug (nur Rechnen) -> deutlich schneller. Anzeige kommt gebuendelt
        # am Partieende (_match_finish_game -> _new_match_game/refresh).
        if self._match_mode() and self._match_blind():
            self.after_engine(col, dt, nodes, score)
            return
        # NACH dem Zug: erst Basis-Layout (draw/Zug/Stufe), DANN Animation.
        # Die Engine-Info (kKn/Zeit/...) setzt after_engine_anim bzw.
        # _refresh_after_engine als LETZTES (drop_animation->refresh und
        # _clear_scores wuerden sie sonst ueberschreiben).
        # Match-Schnellmodus ('Schnell' oder implizit 'Nur Ergebnisse'):
        # keine Drop-Animation (kostet ~16ms*Zeilen).
        fast = self._match_mode() and self._match_delay_ms() == 0
        if self.anim and not fast and self._gui_alive():
            self.drop_animation(col, stone,
                                lambda: self.after_engine_anim(col, dt, nodes, score, _ml_played))
        else:
            self.anim_after = None
            self._refresh_after_engine(col, nodes, score, _ml_played)
            self.after_engine(col, dt, nodes, score)

    def after_engine_anim(self, col, dt, nodes=0, score=None, ml_played=None):
        """Nach Drop-Animation: Engine-Info erneut setzen (refresh in
        drop_animation hat sie zurueckgesetzt)."""
        try:
            dt0 = self.move_times[-1] if self.move_times else dt
            self._show_engine_info(col, nodes, dt0, score, ml_played)
        except Exception:
            pass
        self.after_engine(col, dt, nodes, score)

    def after_engine(self, col, dt, nodes=0, score=None):
        # Match-Modus: Partie-/Matchstand in die Statuszeile.
        if self._match_mode():
            self._match_after_move(col, dt)
            return
        self.status.set(cfs_lang.tf("status_computer_move", col=col + 1,
                                          sec=f"{dt:.2f}"))
        if self.board.is_game_over():
            self.finish_info()
            # Normales Mensch-vs-Computer-Spiel: Spielstand einbuchen.
            # Regel wie in after_human (Zuletzt-Zieher bekommt den Punkt;
            # history-Laenge entscheidet, winner nur Remis ja/nein).
            if not self.two_player and not self._selfplay_mode():
                try:
                    w = self.board.winner()
                except Exception:
                    w = None
                try:
                    if w in (None, 0):
                        self._stand_book_normal(None)
                    else:
                        n = len(self.history)
                        zuletzt_ungerade = (n % 2 == 1)
                        mensch_ungerade = bool(
                            getattr(self, "_human_first", True))
                        self._stand_book_normal(
                            zuletzt_ungerade == mensch_ungerade)
                except Exception:
                    pass
            # Selbstspiel-Partie ist zu Ende: Modus zuruecksetzen, damit
            # man danach mit erster Zug/zurueck/vor/letzter Zug navigieren
            # kann (kein Dauer-Block durch das Selbstspiel-Radio).
            if self._selfplay_mode():
                self._selfplay_stop()
            return
        # Computer-Computer: naechsten Zug automatisch (Perfekt-Stufe
        # erzwungen, damit die Partie sauber zu Ende spielt).
        if self._selfplay_mode():
            self._safe_after(350, self._selfplay_next)

    def _refresh_after_engine(self, col, nodes, score=None, ml_played=None):
        """Nach Engine-Zug: Info (Zug/Stufe/Wert/Knoten/Zeit/Tempo/Quelle) aus der
        ZUGBERECHNUNG anzeigen, aber KEINE neue Analyse starten. So sieht man
        auch bei ausgeschalteter Dauer-Analyse echte kKn usw."""
        try:
            dt = self.move_times[-1] if self.move_times else 0.0
            self._show_engine_info(col, nodes, dt, score, ml_played)
        except Exception:
            pass
        self.draw()
        self._update_turn()
        self._scale_chrome()
        n = len(self.history)
        try:
            self.info_vars["Zug"].set(str(n + 1))
        except Exception:
            pass
        try:
            self.info_vars["Stufe"].set(self._display_stufe_label())
        except Exception:
            pass
        if self.board.is_game_over():
            self.finish_info()
            return
        # Keine Bewertung anzeigen, keine Analyse starten (aus bleibt aus).
        self.scores_visible = False
        self._clear_scores(silent=True)

    def _show_engine_info(self, col, nodes, dt, score=None, ml_played=None):
        """Engine-Kennzahlen des letzten Zugs: Knoten live gezaehlt, ms-Zeit.
        dt ist die REINE Rechenzeit des Workers (kein Warten/Animieren).
        Wert-Anzeige (Fix 03.10.2026): Analyse-Wert des AUSGESPIELTEN Zugs
        (Klartext + Steinzahl bis Ende, wie _show_scores) statt rohem
        BitBully-Score (undokumentierte Skala, blieb ueber Zuege konstant).
        ml_played = Steinzahl aus der VOR-Zug-Stellung (in _engine_done
        bestimmt); Fallback: live aus aktuellem Brett (kann um +/-1 liegen).
        Hinweis zu '50 ms bei 1-2 Halbzuegen/s': Die 50 ms sind echt, aber
        der getaktete GUI-Turnaround (after-Verzoegerung + Event-Queue)
        bestimmt das Tempo, nicht die Rechnung. Match-Modi 'Schnell'
        (Delay 0) bzw. 'Nur Ergebnisse' (Blindmodus) umgehen genau das."""
        try:
            if score is None:
                self.info_vars["Wert"].set("–")
            else:
                try:
                    _s = int(score)
                except Exception:
                    _s = None
                if _s is None:
                    self.info_vars["Wert"].set("–")
                else:
                    try:
                        _ml = ml_played
                        if _ml is None:
                            _ml = self._moves_left(self.board, _s)
                    except Exception:
                        _ml = None
                    # Gewinner aus Zieher-Sicht: + = Zieher gewinnt,
                    # - = Gegner gewinnt (history enthaelt den Zug bereits:
                    # ungerade = Gelb zog zuletzt, gerade = Rot).
                    try:
                        _n = len(self.history)
                        _last_gelb = (_n % 2 == 1)
                    except Exception:
                        _last_gelb = True
                    _gelb = cfs_lang.t("color_yellow")
                    _rot = cfs_lang.t("color_red")
                    if _s > 0:
                        _w = _gelb if _last_gelb else _rot
                    elif _s < 0:
                        _w = _rot if _last_gelb else _gelb
                    else:
                        _w = cfs_lang.t("value_draw")
                    if _ml is None:
                        self.info_vars["Wert"].set(f"{_w}")
                    else:
                        try:
                            self.info_vars["Wert"].set(
                                f"{_w} ({int(_ml)})")
                        except Exception:
                            self.info_vars["Wert"].set(f"{_w}")
        except Exception:
            pass
        try:
            self.info_vars["Tiefe"].set(self._engine_plies())
        except Exception:
            pass
        try:
            self.info_vars["Kn"].set(cfs_lang.fmt_thousands(nodes))
        except Exception:
            pass
        try:
            ms = max(1, int(round(dt * 1000)))
            self.info_vars["Zeit"].set(f"{ms} ms")
        except Exception:
            pass
        try:
            self.info_vars["Kn/s"].set(self._kns_text(nodes, dt))
        except Exception:
            pass
        try:
            self.info_vars["Buch"].set(self._book_label())
        except Exception:
            pass

    def stop(self):
        """Stop: bricht auch Selbstspiel + Match + laufende Analyse ab
        (inkl. Anzeige-Reset). Der C++-Kern laesst sich nicht unterbrechen:
        ein NOCH laufender Thread rechnet im Hintergrund zu Ende, sein
        Ergebnis wird aber verworfen."""
        self.cancel = True
        self._selfplay_stop()
        self._match_stop(cancelled=True)
        self._ana_seq += 1  # laufende + wartende Analyse entwerten
        self._ana_pending = None
        self._ana_busy = False
        self._ana_running_snap = None
        if self.rand_job:
            self.rand_job["stop"] = True
        self.status.set(cfs_lang.t("status_stopped"))

    def _nav_blocked(self):
        """True + Hinweis, wenn Navigation gerade gesperrt ist (Engine
        rechnet, Selbstspiel oder Match laeuft). Rueckgabe True = Aufrufer
        soll abbrechen. Fix 01.10.2026, 2. Review: thinking fehlte hier,
        undo waehrend des Denkens hing das Engine-Ergebnis an einen
        fremden Stand."""
        if self.thinking:
            self.status.set(cfs_lang.t("status_wait_thinking"))
            return True
        if self._match_mode():
            self.status.set(cfs_lang.t("status_match_running"))
            return True
        if self._selfplay_mode():
            self.status.set(cfs_lang.t("status_selfplay_running_stop"))
            return True
        return False

    def undo(self):
        if self.anim_after is not None:
            return
        if self._nav_blocked():
            return
        if self.history:
            self.future.append(self.history.pop())
            self.rebuild()
            self.refresh()

    def redo(self):
        if self.anim_after is not None:
            return
        if self._nav_blocked():
            return
        if self.future:
            self.history.append(self.future.pop())
            self.rebuild()
            self.refresh()

    def goto_first(self):
        if self._nav_blocked():
            return
        while self.history:
            self.future.append(self.history.pop())
        self.rebuild()
        self.refresh()

    def goto_last(self):
        if self._nav_blocked():
            return
        while self.future:
            self.history.append(self.future.pop())
        self.rebuild()
        self.refresh()

    def new_game(self):
        # Neues Spiel waehrend die Engine rechnet: erst sauber stoppen,
        # damit kein veraltetes Ergebnis an den frischen Stand gehaengt
        # wird (Fix 01.10.2026, 2. Review). stop() entwertet Engine-Zug
        # (cancel) + Analyse (_ana_seq); der Worker verwirft sein Ergebnis.
        try:
            self.stop()
        except Exception:
            pass
        self._selfplay_stop()
        # Neues Spiel: naechste Partie beginnt wieder der Mensch (Gelb).
        try:
            self._human_first = True
        except Exception:
            pass
        # Neues Spiel beendet ein Match-Ergebnis (kein laufendes Match mehr),
        # behält aber den Ergebnis-Text lesbar (kein stilles Loeschen).
        if getattr(self, "_match", None) is not None:
            self._match = None
            self._match_stufe = None
            self._match_refresh_win()
        if self.anim_after is not None:
            try:
                self.after_cancel(self.anim_after)
            except Exception:
                pass
            self.anim_after = None
        self.board = bb.Board()
        self.history.clear()
        self.future.clear()
        self.move_times.clear()
        self.agent.reset_transposition_table()
        self.agent.reset_node_counter()
        self.status.set(cfs_lang.t("status_new_game"))
        self.refresh()

    # ---------- Zufallsstellung mit Wunsch-Ergebnis ----------
    def new_random_dialog(self):
        if self.thinking:
            return
        dlg = RandomDialog(self)
        if not dlg.result:
            return
        n, wunsch = dlg.result
        self.rand_job = {"stop": False}
        self.status.set(cfs_lang.tf("status_search_random", n=n,
                                          wish=self._wish_label(wunsch)))
        threading.Thread(target=self._random_thread, args=(n, wunsch), daemon=True).start()

    def _wish_label(self, wunsch):
        """Anzeigename des Wunsch-Ergebnisses (interner Schluessel
        Egal/Gewinn/Unentschieden/Verlust) in der aktiven Sprache."""
        key = {"Egal": "new_random_any", "Gewinn": "new_random_win",
               "Unentschieden": "new_random_draw",
               "Verlust": "new_random_loss"}.get(wunsch)
        return cfs_lang.t(key) if key else str(wunsch)

    def _random_thread(self, n, wunsch):
        want = {"Gewinn": 1, "Unentschieden": 0, "Verlust": -1}.get(wunsch)
        seq = None
        for _ in range(400):
            if self.rand_job is None or self.rand_job.get("stop"):
                self._safe_after(0, lambda: self.status.set(cfs_lang.t("status_aborted")))
                return
            cand = self._random_legal_seq(n)
            if cand is None:
                continue
            if want is None:
                seq = cand
                break
            try:
                b = bb.Board.from_moves(cand)
                with self._solver_lock:
                    s = self.agent.mtdf(b)
            except Exception:
                continue
            sign = 1 if s > 0 else (-1 if s < 0 else 0)
            if sign == want:
                seq = cand
                break
        if seq is None:
            self._safe_after(0, lambda: self.status.set(cfs_lang.t("status_no_position_found")))
            return
        self._safe_after(0, lambda sq=list(seq), w=wunsch: self._random_done(sq, w))

    def _random_legal_seq(self, n):
        for _ in range(60):
            seq = []
            b = bb.Board()
            ok = True
            for _ in range(n):
                legal = [c for c in b.legal_moves()]
                if not legal:
                    ok = False
                    break
                c = random.choice(legal)
                b2 = b.play_on_copy(c)
                if b2.is_game_over() and len(seq) + 1 < n:
                    # Partie waere frueh entschieden -> verwerfen
                    ok = False
                    break
                b = b2
                seq.append(c)
            if ok and not b.is_game_over():
                return seq
        return None

    def _random_done(self, seq, wunsch):
        self.new_game()
        for m in seq:
            self.history.append(m)
            self.board.play(m)
        # Vorgabe-Steine: naechster Zug = len(seq)+1. Bei UNGERADER Vorgabe
        # (z.B. 3 Steine -> Zug 4 = Rot) waere der Mensch sonst Gelb auf
        # einem Rot-Zug -> Zuletzt-Zieher-Regel im Spielstand kippte.
        # Darum: Mensch bekommt die Farbe des NAECHSTEN Zugs
        # (Bugfix 30.09.2026: Zufallsstellung 3 Steine + Niederlage
        # wurde als 1-0 statt 0-1 gezaehlt).
        try:
            self._human_first = (len(seq) % 2 == 0)
        except Exception:
            pass
        self.rebuild()
        self.rand_job = None
        self.status.set(cfs_lang.tf("status_random_done", n=len(seq),
                                          wish=self._wish_label(wunsch)))
        self.refresh(all_scores=True)

    # ---------- Datei (.4gp = Spalten-Notation) ----------
    def load_pos(self):
        # Laden waehrend die Engine rechnet: erst stoppen (Fix 01.10.2026,
        # 2. Review – sonst landet das Engine-Ergebnis auf fremdem Stand).
        if self.thinking:
            try:
                self.stop()
            except Exception:
                pass
            self.status.set(cfs_lang.t("status_load_stopped_thinking"))
            return
        p = filedialog.askopenfilename(filetypes=[("ConnectFour-Stellung", "*.4gp"), ("Alle", "*.*")])
        if not p:
            return
        try:
            self._load_moves(open(p, encoding="ascii", errors="ignore").read().strip())
            self.status.set(cfs_lang.tf("status_loaded", path=os.path.basename(p)))
        except Exception as e:
            messagebox.showerror(cfs_lang.t("error_title"), str(e))

    def save_pos(self):
        p = filedialog.asksaveasfilename(defaultextension=".4gp",
                                         filetypes=[("ConnectFour-Stellung", "*.4gp")])
        if not p:
            return
        s = "".join(str(m + 1) for m in self.history)
        open(p, "w").write(s)
        self.status.set(cfs_lang.tf("status_saved", path=os.path.basename(p)))

    def _quicksave_path(self):
        return os.path.join(BASE, "quicksave.4gp")

    def quick_save(self):
        """F3: Stellung ohne Dialog in quicksave.4gp sichern."""
        try:
            s = "".join(str(m + 1) for m in self.history)
            open(self._quicksave_path(), "w").write(s)
            self.status.set(cfs_lang.tf("status_quick_saved", n=len(self.history)))
        except Exception as e:
            messagebox.showerror(cfs_lang.t("title_quick_save"), str(e))

    def quick_load(self):
        """F4: quicksave.4gp ohne Dialog laden."""
        # Wie load_pos: erst stoppen, wenn die Engine rechnet.
        if self.thinking:
            try:
                self.stop()
            except Exception:
                pass
            self.status.set(cfs_lang.t("status_load_stopped_thinking"))
            return
        p = self._quicksave_path()
        if not os.path.isfile(p):
            self.status.set(cfs_lang.t("status_no_quicksave"))
            return
        try:
            self._load_moves(open(p, encoding="ascii", errors="ignore").read().strip())
            self.status.set(cfs_lang.tf("status_quick_loaded",
                                          name=os.path.basename(p)))
        except Exception as e:
            messagebox.showerror(cfs_lang.t("title_quick_load"), str(e))

    def _load_moves(self, s):
        moves = [int(c) - 1 for c in s if c in "1234567"]
        self.new_game()
        for m in moves:
            # Fix 04.10.2026: nach Partieende keine weiteren Zuege
            # uebernehmen (sonst Steine ueber eine Viererreihe hinaus).
            if self.board.is_game_over():
                break
            if self.board.is_legal_move(m):
                self.history.append(m)
                self.board.play(m)
        # Wie _random_done: Mensch = Farbe des naechsten Zugs (sonst
        # kippt die Zuletzt-Zieher-Regel bei ungerader Vorgabe).
        try:
            self._human_first = (len(self.history) % 2 == 0)
        except Exception:
            pass
        self.rebuild()
        # Laden schaltet die Analyse NICHT ein: bleibt aus, wenn sie aus war.
        self.refresh(all_scores=self.scores_visible)

    def toggle_scores(self):
        """'Alle'-Button: 1. Klick = sofort bewerten, 2. Klick = Zahlen 1-7 zurueck."""
        if self.scores_visible:
            self.scores_visible = False
            self._ana_seq += 1  # laufende Auto-Analyse entwerten
            self._ana_pending = None
            self._clear_scores()
            self.status.set(cfs_lang.t("status_scores_off"))
        else:
            self.refresh(all_scores=True)

    # ---------- Bewertung / Suche ----------
    def _engine_plies(self):
        """Zuletzt erreichte Iterationstiefe (Halbzuege) oder Buch-Horizont.
        Iteration: _last_depth aus _iterative_scores. Buch: Horizont, danach
        weiter iterativ (Zahl statt 'Suche')."""
        if getattr(self, "_last_depth", None) is not None:
            return cfs_lang.t("depth_full") if self._last_depth == -1 else str(self._last_depth)
        n = len(self.history)
        if not self.agent.is_book_loaded():
            return "\u2013"
        if n <= self.BOOK_HORIZON:
            return f"{cfs_lang.t('depth_book')} {self.BOOK_SHORT}"
        return "\u2013"

    def _book_label(self):
        """Quelle-Anzeige: 'Buch 12d' solange die Stellung im Buch liegt
        (bis 12 Steine), danach 'berechnet'."""
        n = len(self.history)
        if not self.agent.is_book_loaded():
            return "\u2013"
        if n <= self.BOOK_HORIZON:
            return f"{cfs_lang.t('book_from_book')} {self.BOOK_SHORT}"
        return cfs_lang.t("book_computed")

    def refresh(self, all_scores=False):
        self.draw()
        self._update_turn()
        self._scale_chrome()
        n = len(self.history)
        self.info_vars["Zug"].set(str(n + 1))
        try:
            self.info_vars["Stufe"].set(self._display_stufe_label())
        except Exception:
            pass
        if self.board.is_game_over():
            self.finish_info()
            return
        if all_scores and not self.thinking:
            # Manueller Klick: synchron rechnen + anzeigen; Auto-Analyse entwerten.
            # Iterative Stufen statt Vollsuche (GUI bleibt reaktionsfaehig).
            self._ana_seq += 1
            t0 = time.time()
            try:
                scores, nodes = self._iterative_scores(
                    self.board, self._iter_depths())
            except Exception:
                scores, nodes = {}, 0
            dt = time.time() - t0
            if scores:
                self._show_scores(scores, nodes, dt)
            else:
                self.status.set(cfs_lang.t("status_eval_aborted"))
        else:
            self.scores_visible = False
            self._clear_scores()
            try:
                self.info_vars["Stufe"].set(self._display_stufe_label())
            except Exception:
                pass
            self.schedule_auto_analyze()

    def finish_info(self):
        w = self.board.winner()
        if w is None and not self.board.is_game_over():
            return
        # BitBully: 1 = Gelb (Anziehender/Spieler 1), 2 = Rot (Spieler 2)
        if w in (None, 0):
            msg = cfs_lang.t("msg_draw")
        else:
            msg = cfs_lang.tf("msg_wins", who=cfs_lang.t(
                "color_red" if int(w) == 2 else "color_yellow"))
        self.status.set(cfs_lang.tf("status_game_end", msg=msg))
        self.info_vars["Wert"].set(msg)

    # ---------- Dauer-Analyse (ohne Verzoegerung) ----------
    def schedule_auto_analyze(self):
        """Sofortige Hintergrund-Analyse; neueste Stellung gewinnt (kein Delay).
        Iterative Vertiefung: zeigt schon nach Tiefe 4-8 eine Naeherung und
        verfeinert bis zur Vollsuche. Stop/Neuzug bricht zwischen Stufen ab.
        Gleiche Stellung wie laufend -> No-Op (kein Doppelstart, kein Block)."""
        if not self.auto_analyze or self.board.is_game_over():
            return
        snap = list(self.history)
        if self._ana_busy:
            if snap == getattr(self, "_ana_running_snap", None):
                return  # genau diese Stellung wird schon berechnet
            self._ana_seq += 1
            self._ana_pending = (self._ana_seq, snap)
            return
        self._ana_seq += 1
        seq = self._ana_seq
        self._ana_running_snap = list(snap)
        self._ana_busy = True
        # cancel NICHT anfassen: gehoert dem Engine-Zug (Stop setzt es).
        # Die Analyse prueft nur _ana_seq (eigene Abbruchkennung).
        threading.Thread(target=self._auto_analyze_thread, args=(seq, snap), daemon=True).start()

    def _auto_analyze_thread(self, seq, snap):
        t0 = time.time()
        last = [None]  # letzte vollstaendige Stufe (fuer Live-Anzeige)

        def prog(depth, scores, nodes, dt):
            if seq != self._ana_seq:
                return
            last[0] = (dict(scores), nodes, dt)
            # Live-Naeherung anzeigen (Tiefe ... = noch suchend).
            self._safe_after(0, lambda s=dict(scores), n=nodes, t=dt, d=depth:
                             self._show_scores_live(s, n, t, d, seq, snap))

        try:
            b = bb.Board()
            for m in snap:
                b.play(m)
            depths = self._iter_depths()
            # Analyse-Abbruch: NUR eigene _ana_seq (kein cancel: Stop/Neu
            # waehrend eines Engine-Zugs darf die Analyse nicht killen und
            # umgekehrt entwertet Analyse den Engine-Zug nicht, Bug 28.09.2026).
            my = seq
            scores, nodes = self._iterative_scores(
                b, depths, on_progress=prog,
                abort=lambda: my != self._ana_seq)
        except Exception as e:
            self._safe_after(0, lambda s=seq, err=str(e): self._auto_analyze_fail(s, err))
            return
        if not scores and last[0] is not None:
            scores, nodes, _t = last[0]
        dt = time.time() - t0
        self._safe_after(0, lambda s=seq, sn=list(snap), sc=dict(scores), nd=nodes, d=dt: self._auto_analyze_done(s, sn, sc, nd, d))

    def _auto_analyze_fail(self, seq, err):
        self._ana_busy = False
        self._ana_running_snap = None
        if seq != self._ana_seq:
            self._drain_pending()
            return
        self.status.set(cfs_lang.tf("status_analysis_error", err=err))
        self._drain_pending()

    def _auto_analyze_done(self, seq, snap, scores, nodes, dt):
        self._ana_busy = False
        self._ana_running_snap = None
        if seq != self._ana_seq or list(self.history) != snap:
            self._drain_pending()
            return  # veraltet: Ergebnis gehoert zu alter Stellung
        if not self.auto_analyze:
            self._drain_pending()
            return  # Analyse wurde inzwischen ausgeschaltet
        self._show_scores(scores, nodes, dt)
        best = max(scores, key=scores.get)
        self.status.set(cfs_lang.tf("status_analysis_done", col=best + 1,
                                          score=scores[best], sec=f"{dt:.2f}"))
        self._drain_pending()

    def _drain_pending(self):
        if self._ana_pending is None:
            return
        seq, snap = self._ana_pending
        self._ana_pending = None
        if seq != self._ana_seq or list(self.history) != snap:
            return
        if self.board.is_game_over():
            return
        self._ana_running_snap = list(snap)
        self._ana_busy = True
        self.cancel = False
        threading.Thread(target=self._auto_analyze_thread, args=(seq, snap), daemon=True).start()

    def _show_scores_live(self, scores, nodes, dt, depth, seq, snap):
        """Live-Naeherung waehrend iterativer Suche (Tiefe ... = suchend).
        Nur anzeigen, wenn Stellung + Anfrage noch aktuell und Analyse an."""
        if seq != self._ana_seq or list(self.history) != snap:
            return
        if not self.auto_analyze or self.board.is_game_over():
            return
        self._show_scores(scores, nodes, dt, live_depth=depth)
        try:
            label = cfs_lang.t("depth_full") if depth == -1 else str(depth)
            self.info_vars["Tiefe"].set(f"{label}...")
        except Exception:
            pass

    def _show_scores(self, scores, nodes, dt, live_depth=None):
        """Bewertung farbig anzeigen (gruen/gelb/rot), ohne neu zu rechnen.
        Zeile oben: + (Gewinn), = (Unentschieden), - (Verlust). Unten: Zugzahl.
        Info: exakte Knoten (deutsches Format, live vom C++-Kern gezaehlt),
        ms-genaue Zeit, echte Knoten/s. Keine Deko-Zahlen.
        Leere Scores (abgebrochene Suche): nichts anzeigen (Fix 01.10.2026,
        2. Review – vorher ValueError in max())."""
        if not scores:
            return
        self._update_turn()
        self.scores_visible = True
        m = {}
        for c in range(COLS):
            if c in scores:
                s = scores[c]
                ml = bb.BitBully.score_to_moves_left(s, self.board)
                if s > 0:
                    top, bg = "+", C_WIN
                elif s == 0:
                    top, bg = "=", C_DRAW
                else:
                    top, bg = "-", C_LOSS
                m[c] = (top, str(ml), bg)
            else:
                m[c] = ("X", "", "#a0a0a0")
        self._set_scores(m)
        best = max(scores, key=scores.get)
        bs = scores[best]
        # Kompakt (Fix 03.10.2026, Info-Feld width=11): "Gelb (31)" statt
        # "Sp. 4: Gelb gewinnt (31)" – Spalte steht in der Wertungszeile.
        _gelb = cfs_lang.t("color_yellow")
        _rot = cfs_lang.t("color_red")
        if bs > 0:
            _w = _gelb if len(self.history) % 2 == 0 else _rot
        elif bs == 0:
            _w = cfs_lang.t("value_draw")
        elif len(self.history) % 2 == 0:
            _w = _rot
        else:
            _w = _gelb
        try:
            _ml = bb.BitBully.score_to_moves_left(bs, self.board)
            wert_txt = f"{_w} ({int(_ml)})"
        except Exception:
            wert_txt = f"{_w}"
        self.info_vars["Wert"].set(wert_txt)
        self.info_vars["Tiefe"].set(self._engine_plies())
        self.info_vars["Kn"].set(cfs_lang.fmt_thousands(nodes))
        ms = max(1, int(round(dt * 1000)))
        self.info_vars["Zeit"].set(f"{ms} ms")
        self.info_vars["Kn/s"].set(self._kns_text(nodes, dt))
        self.info_vars["Buch"].set(self._book_label())

    def _kns_text(self, nodes, dt):
        """Knoten/s formatiert (Dezimalzeichen je Sprache)."""
        kns = nodes / max(dt, 1e-9)
        if kns >= 1_000_000:
            return cfs_lang.fmt_decimal(f"{kns/1_000_000:.1f} M/s")
        elif kns >= 1_000:
            return f"{kns/1_000:.0f} k/s"
        return f"{kns:.0f} /s"

    # Fest verdrahtet: nur das 12-ply-dist-Buch (Gewinn + Zugzahl bis Ende).
    # Keine Auswahl mehr (8-ply/12-ply ohne Distanz + 'ohne Buch' haben zu
    # viele Sonderfaelle/Probleme verursacht). Buch wird beim Start geladen.
    BOOK_NAME = "12-ply-dist"
    BOOK_SHORT = "12d"
    BOOK_HORIZON = 12

    def _load_book_fixed(self):
        """12-ply-dist-Buch laden (einzige Quelle, beim Start + bei Bedarf)."""
        try:
            self.agent.load_book(self.BOOK_NAME)
        except Exception as e:
            try:
                messagebox.showwarning(cfs_lang.t("title_book"),
                                       cfs_lang.tf("err_book_load", err=e))
            except Exception:
                pass

    # ---------- Einstellungen ----------
    def switch_book(self):
        # Altlast: keine Buchauswahl mehr. Buch erneut laden + anzeigen.
        self._load_book_fixed()
        try:
            self.book_var.set(self.BOOK_NAME)
        except Exception:
            pass
        self.status.set(cfs_lang.tf("status_book_loaded", book=self._book_names.get(
            self.BOOK_NAME, self.BOOK_NAME)))
        # Nur weiter analysieren, wenn vorher auch analysiert wurde
        self.refresh(all_scores=self.scores_visible)

    def _confirm_book_upgrade(self):
        # Altlast: kein Upgrade mehr noetig (nur noch 12-ply-dist).
        return True

    def _stufe_label(self):
        try:
            v = self.depth_var.get()
        except Exception:
            v = getattr(self, "_stufe_cache", "perfekt")
        return self._stufe_label_for(v)

    # Stufen-Tabellen (ausgelagert in cfs_levels, 01.10.2026): als
    # Klassenattribute re-exportiert, damit self.STUFEN & Co. sowie
    # Menue-/Dialog-Code unveraendert funktionieren.
    STUFEN_ORDER = cfs_levels.STUFEN_ORDER
    STUFEN_LABELS = cfs_levels.STUFEN_LABELS
    STUFEN = cfs_levels.STUFEN
    USER_KEYS = cfs_levels.USER_KEYS
    _USER_LABEL_1 = cfs_levels.USER_LABEL_1
    _USER_LABEL_2 = cfs_levels.USER_LABEL_2
    _MATCH_STUFEN = cfs_levels.MATCH_STUFEN

    def _apply_stufe(self):
        """Engine-Staerke anwenden: Perfekt = fehlerfrei + unbegrenzt.
        Stufen = volle Tiefe mit Patzerquote (100-p) + Verlustschutz s
        (Filter schliesst zu schnelle Niederlagen aus) + Siegsschutz w
        (kurzer Gewinn geht immer vor), siehe STUFEN."""
        v = self._stufe_key()
        try:
            self._stufe_cache = v
            self.depth_var.set(v)
        except Exception:
            pass
        _key, err, _s, _w = self._stufen_werte(v)
        self.agent.max_depth = -1
        self.error_rate = err
        try:
            self.info_vars["Stufe"].set(self._stufe_label())
        except Exception:
            pass

    def switch_depth(self):
        """Computer-Stufe (Menue-Unterpunkt).
        Im Selbstspiel-Modus wird die Stufe auf Perfekt zurueckgesetzt
        (Computer-Computer spielt immer perfekt).
        Stufenwechsel -> Spielstand der neuen Stufe auf 0-0
        (Wunsch Patrick: 'Mensch vs <neuer Gegner>' steht sofort da)."""
        if self._selfplay_mode():
            self._stufe_cache = "perfekt"
            try:
                self.depth_var.set("perfekt")
            except Exception:
                pass
        self._apply_stufe()
        try:
            self._stand_reset_to(self._stufe_key())
        except Exception:
            pass
        try:
            self.stand_var.set(bool(getattr(self, "_stand_enabled", False)))
        except Exception:
            pass
        if self._selfplay_mode():
            self.status.set(cfs_lang.t("status_selfplay_fixed"))
        else:
            self.status.set(cfs_lang.tf("status_hc_level", label=self._stufe_label()))
        self.refresh(all_scores=self.scores_visible)

    def _select_engine(self):
        """Computer als Gegner waehlen (Radio): 2-Spieler aus, ggf. Computer-Zug.
        Bricht ein laufendes Selbstspiel ab."""
        self._selfplay_stop()
        self.two_player = False
        try:
            self.opp_var.set("Computer")
        except Exception:
            pass
        self.status.set(cfs_lang.tf("status_hc_mode", label=self._stufe_label()))
        if not self.board.is_game_over() and len(self.history) % 2 == 1:
            self.engine_move()
        else:
            self.refresh(all_scores=self.scores_visible)

    def _select_selfplay(self):
        """Computer-Computer (ausspielen): Computer spielt ab der aktuellen
        Stellung in Stufe Perfekt gegen sich selbst bis zum Partieende.
        Jeder Klick startet neu (Stufe wird auf Perfekt erzwungen)."""
        self.two_player = False
        self.selfplay = True
        try:
            self.opp_var.set("Computer-Computer (ausspielen)")
        except Exception:
            pass
        self._stufe_cache = "perfekt"
        self.depth_var.set("perfekt")
        self._apply_stufe()
        self.status.set(cfs_lang.t("status_selfplay_playing"))
        self.refresh(all_scores=self.scores_visible)
        if not self.board.is_game_over() and not self.thinking:
            self.engine_move()

    def _selfplay_stop(self):
        """Selbstspiel beenden + Modus-Radio auf Computer zuruecksetzen.
        Ohne den Radio-Reset meldet _selfplay_mode() ewig 'laeuft' (nur das
        Flag wurde geloescht) -> Navigation (undo/redo/erster/letzter Zug)
        bleibt nach Partieende/Stop fuer immer gesperrt. Der Reset loest
        KEINEN Engine-Zug aus (nur Variable, kein _select_engine)."""
        self.selfplay = False
        try:
            if self.opp_var.get() == "Computer-Computer (ausspielen)":
                self.opp_var.set("Computer")
        except Exception:
            pass

    def _selfplay_next(self):
        """Naechster Selbstspiel-Zug (nach Animation/Pause)."""
        if not self._selfplay_mode():
            return
        if self.board.is_game_over() or self.thinking:
            if self.board.is_game_over():
                self._selfplay_stop()
            return
        # Stufe waehrend des Selbstspiels auf Perfekt festnageln.
        try:
            if self._stufe_key() != "perfekt":
                self._stufe_cache = "perfekt"
                try:
                    self.depth_var.set("perfekt")
                except Exception:
                    pass
                self._apply_stufe()
        except Exception:
            pass
        self.engine_move()

    # ---------- Turnier (Match) ----------
    # Dialog (wie Hilfe/Info als Toplevel): Gelb-/Rot-Seite je 'Mensch'
    # oder feste Stufe (p,s,w); Partien (1..10000); Farbwechsel-Checkbox;
    # Tempo-Auswahl Normal/Schnell/Nur Ergebnisse (Turbo). Anzeige in der
    # Statuszeile: "Computer-Computer Match 3/20: Gelb (...) – Rot (...) ..." etc.
    # Elo-Differenz (Gelb-Sicht) = -400*log10(1/p - 1), p = Punkte/Partien
    # (0 % / 100 % -> begrenzt auf +/- 2000, wie bei cutechess).
    # Am Turnierende: Endergebnis kopierbar (Text + Kopieren-Button).
    # (Tabellen in cfs_levels; Klassenattribute als Re-Export, damit
    # Dialog-/Match-Code unveraendert funktioniert.)
    # User-Stufen (eigene p,s,w aus dem Turnier-Dialog): Klassenattribute,
    # damit Worker-Threads ohne Tk-Variablen lesen koennen. Getrennt pro
    # Seite (User Gelb / User Rot), damit zwei verschiedene (p,s,w) im
    # selben Turnier spielen koennen.
    _user_psw_1 = (50, 1, 1)
    _user_psw_2 = (50, 1, 1)
    # Altlast-Einzelwert (Bugfix 30.09.2026: als Instanz- statt Klassen-
    # attribut geschrieben -> Ergebnis-Text fiel auf (50,2,2) zurueck).
    # Bleibt als Fallback lesbar, wird aber nicht mehr geschrieben.
    _user_psw = (50, 1, 1)

    def _match_mode(self):
        """True, solange ein Match laeuft (ggf. auch waehrend Pause/Denken)."""
        m = getattr(self, "_match", None)
        return bool(m is not None and not m.get("fertig", False))

    @staticmethod
    def _match_elo(punkte_gelb, partien):
        """Elo-Differenz aus Gelb-Sicht (s. cfs_levels.match_elo)."""
        return cfs_levels.match_elo(punkte_gelb, partien)

    def _match_score_str(self, fixed=False):
        """'Gelb X – Rot Y (+g/=r/-v)' aus Match-Sicht (Seitenpaar).
        Fertige Partien = nr - 1 (nr zeigt waehrend des Laufs schon die
        naechste; nach Matchende bleibt nr auf der letzten Partie).
        fixed=True: kurze Zahlen ohne Nullen (Wunsch Patrick: 1-2 statt
        001.0-0002.0). Halbe Punkte (Remis) werden als ,5 gezeigt."""
        m = self._match
        done = m["nr"] if m.get("fertig") else m["nr"] - 1
        done = max(0, done)
        pg = m["punkte_gelb"] + 0.5 * m["remis"]
        pr = (done - m["punkte_gelb"] - m["remis"]) + 0.5 * m["remis"]
        g = m["punkte_gelb"]
        r = done - m["punkte_gelb"] - m["remis"]
        if fixed:
            def _kurz(x):
                # 12.0 -> '12' (kein 12.0), 12.5 -> '12,5'
                if abs(x - round(x)) < 1e-9:
                    return str(int(round(x)))
                return cfs_lang.fmt_decimal(f"{x:.1f}")
            pg_s, pr_s = _kurz(pg), _kurz(pr)
            # Minus nie doppelt: pr kann rechnerisch negativ werden, wenn
            # der Teststand mehr Punkte zaehlt als Partien fertig sind.
            if pr < 0:
                pr_s = "0"
                r = max(0, r)
            return (f"{pg_s}-{pr_s} "
                    f"(+{g}/={m['remis']}/-{r})")
        return f"{pg:g} – {pr:g} (+{g}/={m['remis']}/-{r})"

    def _match_done(self):
        """Zahl der fertigen Matchpartien (fuer Stand + Elo)."""
        m = self._match
        if m.get("fertig"):
            return max(0, m["nr"])
        return max(0, m["nr"] - 1)

    def _match_status(self):
        """Statuszeilen-Text, ruhig (Wunsch Patrick): feste Struktur und
        Reihenfolge, nur einzelne Woerter/Zahlen wechseln.
        Layout: 'Match 7/20 | Gelb (Mittel) - Rot (Schwer) | 12-8 (+12/=1/-7)
        | Elo +70'. Kurze Zahlen (kein 0007/0020, kein +0070, kein 12.0).
        Wird nur zu Partiebeginn und bei Partie-/Matchende geschrieben,
        NICHT nach jedem Zug (kein 'denkt...'-Flackern).
        Hinweis: Ein Label mit GELB/ROT-Farbcode statt reiner Textnamen waere
        noch ruhiger, ist aber Design -> Rueckfrage."""
        m = self._match
        elo = self._match_elo(m["punkte_gelb"] + 0.5 * m["remis"],
                              self._match_done())
        gn = self._stufe_label_for(m["gelb"])
        rn = self._stufe_label_for(m["rot"])
        elo_txt = "Elo –" if elo is None else f"Elo {elo:+.0f}"
        score = self._match_score_str(fixed=True)
        return cfs_lang.tf("match_status_line", nr=m['nr'], games=m['spiele'],
                           g=gn, r=rn, score=score, elo=elo_txt)

    def _match_refresh_win(self):
        """Match-Fenster (falls offen): Stand live aktualisieren."""
        win = getattr(self, "_match_win", None)
        if win is None:
            return
        try:
            win.winfo_exists()
        except Exception:
            self._match_win = None
            return
        try:
            txtvar = getattr(win, "_stand_var", None)
            if txtvar is not None:
                if self._match is None:
                    txtvar.set(cfs_lang.t("match_none"))
                else:
                    m = self._match
                    elo = self._match_elo(m["punkte_gelb"] + 0.5 * m["remis"],
                                          self._match_done())
                    elo_txt = "–" if elo is None else f"{elo:+.0f}"
                    state = cfs_lang.t(
                        "match_state_done" if m.get("fertig") else
                        ("match_state_aborted" if m.get("abgebrochen")
                         else "match_state_running"))
                    txtvar.set(cfs_lang.tf(
                        "match_live", nr=min(m['nr'], m['spiele']),
                        games=m['spiele'], state=state,
                        g=self._stufe_label_for(m['gelb']),
                        r=self._stufe_label_for(m['rot']),
                        score=self._match_score_str(), elo=elo_txt))
            res = getattr(win, "_result_txt", None)
            if res is not None:
                try:
                    res.config(state="normal")
                    res.delete("1.0", "end")
                    res.insert("end", self._match_result_text())
                    res.config(state="disabled")
                except Exception:
                    pass
        except Exception:
            pass

    def _match_result_text(self):
        """Kopierbarer Endergebnis-Text (wie Patricks Wunschformat).
        Feste Stufen mit (p,s,w)-Zusatz, z.B. '6 Mittel (40,1,1)'.
        Seiten heissen neutral (Mensch/Computer-Namen), nicht 'Match'."""
        m = self._match
        if m is None:
            return cfs_lang.t("match_no_result")
        gn = self._stufe_label_for(m["gelb"], mit_psw=True)
        rn = self._stufe_label_for(m["rot"], mit_psw=True)
        done = self._match_done()
        pg = m["punkte_gelb"] + 0.5 * m["remis"]
        pr = (done - m["punkte_gelb"] - m["remis"]) + 0.5 * m["remis"]
        elo = self._match_elo(m["punkte_gelb"] + 0.5 * m["remis"], done)
        elo_txt = "–" if elo is None else f"{elo:+.0f}"
        state = cfs_lang.t("match_aborted_lc" if m.get("abgebrochen")
                           else "match_finished_lc")

        def _seite(key, label):
            return (cfs_lang.t("level_human") if key == "mensch"
                    else cfs_lang.tf("side_computer", label=label))
        return cfs_lang.tf(
            "match_result_text", a=_seite(m['gelb'], gn), b=_seite(m['rot'], rn),
            pg=f"{pg:g}", pr=f"{pr:g}", w=m['punkte_gelb'], d=m['remis'],
            l=done - m['punkte_gelb'] - m['remis'], elo=elo_txt, done=done,
            games=m['spiele'], state=state,
            swap=cfs_lang.t("onoff_on" if m['wechsel'] else "onoff_off"))

    def match_dialog(self):
        """Turnier-Dialog oeffnen (Toplevel wie Hilfe/Info). Bei laufendem
        Turnier zeigt er den Live-Stand + Stop; sonst die Einstellungen.
        Seiten: je 'Mensch', feste Stufe 0-14, 'User (1)' oder
        'User (2)' — die User-Eintraege aktivieren KEY-basiert je ein
        eigenes (p,s,w)-Feld (Feld (1) <-> Key 'user1', Feld (2) <-> Key
        'user2', egal ob Gelb oder Rot; Fix 30.09.2026, vorher
        seiten-basiert -> falsches Feld aktiv + falscher Name). Zwei ver-
        schiedene (p,s,w) im selben Turnier sind moeglich (user1 vs user2).
        Tempo: Normal / Schnell / Nur Ergebnisse (Turbo) – nur eines.
        Das Endergebnis zeigt das Paar mit (p,s,w)-Zusatz zur Einordnung."""
        if self._selfplay_mode() or self.thinking:
            self.status.set(cfs_lang.t("status_stop_before_match"))
            return
        old = getattr(self, "_match_win", None)
        try:
            if old is not None:
                old.winfo_exists()
                old.lift()
                old.focus_set()
                return
        except Exception:
            self._match_win = None
        win = tk.Toplevel(self)
        win.title(cfs_lang.t("match_title"))
        win.geometry("470x700")
        self._match_win = win
        try:
            win.protocol("WM_DELETE_WINDOW", self._match_win_closed)
        except Exception:
            pass
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text=cfs_lang.t("label_yellow")).grid(row=0, column=0, sticky="w")
        ttk.Label(frm, text=cfs_lang.t("label_red")).grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Label(frm, text=cfs_lang.t("match_games")).grid(row=2, column=0, sticky="w", pady=(6, 0))
        gelb_var = tk.StringVar(value="leicht")
        rot_var = tk.StringVar(value="mittel")
        n_var = tk.StringVar(value="20")
        wechsel_var = tk.BooleanVar(value=True)
        tempo_var = tk.StringVar(value="normal")
        # Vorbelegung aus laufendem Match (Keys direkt; Labels unten).
        _pre_g, _pre_r = "leicht", "mittel"
        if self._match is not None and not self._match.get("fertig", False):
            try:
                _pre_g = self._match["gelb"]
                _pre_r = self._match["rot"]
                n_var.set(str(self._match["spiele"]))
                wechsel_var.set(bool(self._match["wechsel"]))
                if self._match.get("blind"):
                    tempo_var.set("turbo")
                elif self._match.get("schnell"):
                    tempo_var.set("schnell")
                else:
                    tempo_var.set("normal")
            except Exception:
                pass
        # User-(p,s,w) vorbelegen aus den Klassenattributen.
        try:
            _pg, _sg, _wg = type(self)._user_psw_for("user1")
            _pr, _sr, _wr = type(self)._user_psw_for("user2")
        except Exception:
            _pg, _sg, _wg = (50, 1, 1)
            _pr, _sr, _wr = (50, 1, 1)
        namen = [("mensch", cfs_lang.t("level_human"))]
        namen += [(k, self._stufe_label_for(k)) for k in self.STUFEN_ORDER]
        namen += [("user1", self._USER_LABEL_1 + cfs_lang.t("user_own_psw")),
                  ("user2", self._USER_LABEL_2 + cfs_lang.t("user_own_psw"))]
        label_of = {k: n for k, n in namen}
        key_of = {n: k for k, n in namen}
        gelb_var.set(label_of.get(_pre_g, label_of.get("leicht")))
        rot_var.set(label_of.get(_pre_r, label_of.get("mittel")))
        cb_g = ttk.Combobox(frm, textvariable=gelb_var, state="readonly",
                            values=[n for _, n in namen], width=26,
                            height=19)
        cb_r = ttk.Combobox(frm, textvariable=rot_var, state="readonly",
                            values=[n for _, n in namen], width=26,
                            height=19)
        cb_g.grid(row=0, column=1, sticky="w")
        cb_r.grid(row=1, column=1, sticky="w", pady=(6, 0))
        # Zwei User-Felder, je KEY ('User (1)' / 'User (2)'): aktiv SOFORT,
        # sobald die jeweilige AUSWAHL getroffen ist — keine Checkbox mehr.
        # Sonst grau. p = % perfekte Zuege (Patzerquote = 100-p),
        # s = Verlustschutz (Patzer tabu, wenn Gegner in <= s Zuegen mattet),
        # w = Siegsschutz (Gewinn in <= w Zuegen geht immer vor).
        # Naeheres: Hilfe > Userstufen. WICHTIG (Fix 30.09.2026): Die
        # Zuordnung ist KEY-basiert, nicht seiten-basiert: Feld (1) gehoert
        # zu Key 'user1', Feld (2) zu Key 'user2' — egal ob Gelb oder Rot.
        # (Vorher seiten-basiert: Gelb=Zufall/Rot=User 1 machte Feld (2)
        # editierbar und der Ergebnis-Text zeigte den falschen User-Namen.)
        ttk.Label(frm, text="User (1) p,s,w:").grid(row=5, column=0, sticky="w", pady=(8, 0))
        pg_var = tk.StringVar(value=str(_pg))
        sg_var = tk.StringVar(value=str(_sg))
        wg_var = tk.StringVar(value=str(_wg))
        psg_box = ttk.Frame(frm)
        psg_box.grid(row=5, column=1, sticky="w", pady=(8, 0))
        pg_ent = ttk.Entry(psg_box, textvariable=pg_var, width=5)
        pg_ent.pack(side="left", padx=(0, 4))
        sg_ent = ttk.Entry(psg_box, textvariable=sg_var, width=5)
        sg_ent.pack(side="left", padx=(0, 4))
        wg_ent = ttk.Entry(psg_box, textvariable=wg_var, width=5)
        wg_ent.pack(side="left")
        ttk.Label(frm, text="User (2) p,s,w:").grid(row=6, column=0, sticky="w")
        pr_var = tk.StringVar(value=str(_pr))
        sr_var = tk.StringVar(value=str(_sr))
        wr_var = tk.StringVar(value=str(_wr))
        psr_box = ttk.Frame(frm)
        psr_box.grid(row=6, column=1, sticky="w")
        pr_ent = ttk.Entry(psr_box, textvariable=pr_var, width=5)
        pr_ent.pack(side="left", padx=(0, 4))
        sr_ent = ttk.Entry(psr_box, textvariable=sr_var, width=5)
        sr_ent.pack(side="left", padx=(0, 4))
        wr_ent = ttk.Entry(psr_box, textvariable=wr_var, width=5)
        wr_ent.pack(side="left")
        ttk.Label(frm, justify="left", wraplength=440,
                  text=cfs_lang.t("match_hint"))\
            .grid(row=7, column=0, columnspan=2, sticky="w")

        def _umode_flip(*_a):
            """User-Felder je KEY aktivieren (grau sonst). Feld (1) ist
            genau dann editierbar, wenn Gelb ODER Rot 'User (1)' gewaehlt
            hat; Feld (2) analog fuer 'User (2)'. KEY-basiert (Fix
            30.09.2026, vorher seiten-basiert -> falsches Feld aktiv +
            falscher Name im Ergebnis-Text). Wird bei jeder Combo-Aenderung
            + beim Oeffnen gerufen. Bindung an BEIDE Events:
            <<ComboboxSelected>> (Maus) + <KeyRelease>/<FocusOut>
            (Tastatur/programmatisch), plus trace auf die Textvariablen
            (cb.set() aendert nur die Variable, feuert kein Event)."""
            try:
                g = key_of.get(gelb_var.get(), "leicht")
            except Exception:
                g = "leicht"
            try:
                r = key_of.get(rot_var.get(), "mittel")
            except Exception:
                r = "mittel"
            st_1 = "normal" if (g == "user1" or r == "user1") else "disabled"
            st_2 = "normal" if (g == "user2" or r == "user2") else "disabled"
            for _e in (pg_ent, sg_ent, wg_ent):
                try:
                    _e.config(state=st_1)
                except Exception:
                    pass
            for _e in (pr_ent, sr_ent, wr_ent):
                try:
                    _e.config(state=st_2)
                except Exception:
                    pass
        try:
            cb_g.bind("<<ComboboxSelected>>", _umode_flip)
            cb_r.bind("<<ComboboxSelected>>", _umode_flip)
        except Exception:
            pass
        try:
            gelb_var.trace_add("write", _umode_flip)
            rot_var.trace_add("write", _umode_flip)
        except Exception:
            try:
                gelb_var.trace("w", lambda *_a: _umode_flip())
                rot_var.trace("w", lambda *_a: _umode_flip())
            except Exception:
                pass
        _umode_flip()
        ttk.Entry(frm, textvariable=n_var, width=8).grid(row=2, column=1, sticky="w", pady=(6, 0))
        ttk.Checkbutton(frm, text=cfs_lang.t("match_swap"),
                        variable=wechsel_var).grid(row=3, column=0, columnspan=2,
                                                   sticky="w", pady=(6, 0))
        ttk.Label(frm, text=cfs_lang.t("match_tempo")).grid(row=4, column=0, sticky="w", pady=(6, 0))
        tempo_box = ttk.Frame(frm)
        tempo_box.grid(row=4, column=1, sticky="w", pady=(6, 0))
        ttk.Radiobutton(tempo_box, text=cfs_lang.t("tempo_normal"), value="normal",
                        variable=tempo_var).pack(side="left")
        ttk.Radiobutton(tempo_box, text=cfs_lang.t("tempo_fast"), value="schnell",
                        variable=tempo_var).pack(side="left", padx=(8, 0))
        ttk.Radiobutton(tempo_box, text=cfs_lang.t("tempo_turbo"), value="turbo",
                        variable=tempo_var).pack(side="left", padx=(8, 0))
        stand_var = tk.StringVar(value="")
        win._stand_var = stand_var
        stand_lbl = ttk.Label(frm, textvariable=stand_var, justify="left")
        stand_lbl.grid(row=8, column=0, columnspan=2, sticky="w", pady=(8, 0))
        win._stand_lbl = stand_lbl
        ttk.Label(frm, text=cfs_lang.t("match_result_label")).grid(
            row=9, column=0, columnspan=2, sticky="w", pady=(8, 0))
        res_txt = tk.Text(frm, wrap="word", width=52, height=4)
        res_txt.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(2, 0))
        win._result_txt = res_txt
        try:
            res_txt.insert("end", self._match_result_text() if self._match else "")
            res_txt.config(state="disabled")
        except Exception:
            pass
        btn = ttk.Frame(frm)
        btn.grid(row=11, column=0, columnspan=2, pady=(10, 0))

        def _user_psw_triple(var_p, var_s, var_w):
            """(p,s,w) aus drei Eingaben lesen/klammern: p 0-100, s/w 0-9.
            Defaults (50,1,1) = Stufe 'Anfaenger light' (s/w je 1)."""
            try:
                p = max(0, min(100, int(var_p.get())))
            except Exception:
                p = 50
            try:
                s = max(0, min(9, int(var_s.get())))
            except Exception:
                s = 1
            try:
                w = max(0, min(9, int(var_w.get())))
            except Exception:
                w = 1
            return (p, s, w)

        def _start():
            if self._match_mode():
                return
            try:
                g = key_of.get(cb_g.get(), "leicht")
            except Exception:
                g = "leicht"
            try:
                r = key_of.get(cb_r.get(), "mittel")
            except Exception:
                r = "mittel"
            # User-(p,s,w) je KEY uebernehmen (KLASSENattribute, damit
            # Ergebnis-Text + Worker-Threads die Werte sehen — Bugfix
            # 30.09.2026: self._user_psw erzeugte einen Instanz-Schatten,
            # _stufe_label_for las das Klassenattribut -> immer (50,2,2)).
            # KEY-basiert (Fix 30.09.2026): Feld (1) -> Key 'user1',
            # Feld (2) -> Key 'user2', egal auf welcher Seite der Key steht.
            # Beispiel: Gelb=Zufall/Rot=User 1 liest Feld (1); der
            # Ergebnis-Text zeigt dann korrekt 'User (1) (p,s,w)'.
            try:
                if g == "user1" or r == "user1":
                    type(self)._user_psw_1 = _user_psw_triple(
                        pg_var, sg_var, wg_var)
                if g == "user2" or r == "user2":
                    type(self)._user_psw_2 = _user_psw_triple(
                        pr_var, sr_var, wr_var)
            except Exception:
                pass
            try:
                n = max(1, min(10000, int(n_var.get())))
            except Exception:
                n = 20
            tempo = tempo_var.get()
            self._match_start(g, r, n, bool(wechsel_var.get()),
                              schnell=(tempo == "schnell"),
                              blind=(tempo == "turbo"))

        ttk.Button(btn, text=cfs_lang.t("btn_start"), command=_start).pack(side="left", padx=4)
        ttk.Button(btn, text=cfs_lang.t("btn_stop"), command=self.stop).pack(side="left", padx=4)
        ttk.Button(btn, text=cfs_lang.t("btn_copy"),
                   command=lambda: (win.clipboard_clear(),
                                    win.clipboard_append(res_txt.get("1.0", "end-1c")))).pack(side="left", padx=4)
        ttk.Button(btn, text=cfs_lang.t("btn_close"),
                   command=self._match_win_closed).pack(side="left", padx=4)
        # Falls Match laeuft: Stand sofort anzeigen.
        self._match_refresh_win()

    def _match_win_closed(self):
        """Match-Fenster schliessen (Match laeuft im Hintergrund weiter)."""
        win = getattr(self, "_match_win", None)
        self._match_win = None
        try:
            if win is not None:
                win.destroy()
        except Exception:
            pass

    def _match_start(self, gelb, rot, spiele, wechsel,
                       schnell=False, blind=False):
        """Computer-Computer Match starten: Stand zuruecksetzen, Brett leeren, 1. Partie.
        schnell: keine Zugpausen/Animation. blind ('Nur Ergebnisse (Turbo)'):
        zusaetzlich keine Brettanzeige pro Zug (nur Ergebnis) und
        IMPLIZIT immer schnell (Pause 0, keine Animation)."""
        self._selfplay_stop()
        # Fix 04.10.2026: Mit Mensch-Seite kein Turbo (Brett muss sichtbar
        # bleiben, sonst zieht der Mensch blind).
        if "mensch" in (gelb, rot):
            blind = False
        self.two_player = False
        try:
            self.opp_var.set("Computer")
        except Exception:
            pass
        self.cancel = False
        self._ana_seq += 1
        self._ana_pending = None
        self._match = {"gelb": gelb, "rot": rot, "spiele": spiele,
                       "wechsel": wechsel, "nr": 1, "punkte_gelb": 0,
                       "remis": 0, "fertig": False, "abgebrochen": False,
                       "schnell": bool(schnell), "blind": bool(blind)}
        self._match_stufe = None
        self._new_match_game()
        self._match_refresh_win()

    def _match_gelb_beginnt(self):
        """True, wenn in Partie nr Gelb anfaengt (sonst Rot). Ohne Wechsel
        faengt immer Gelb an; mit Wechsel alternierend ab Partie 2."""
        m = self._match
        if not m.get("wechsel", True):
            return True
        return (m["nr"] % 2) == 1

    def _match_human_turn(self):
        """True, wenn im laufenden Turnier gerade die Mensch-Seite am Zug
        ist (Gegner-Engine wartet auf Klick/Taste statt zu rechnen)."""
        try:
            if not self._match_mode():
                return False
            return self._match_side_stufe() == "mensch"
        except Exception:
            return False

    def _new_match_game(self):
        """Brett fuer die naechste Matchpartie leeren (TT bleibt -> schnell).
        Schreibt die (ruhige) Statuszeile einmalig zu Partiebeginn."""
        self.board = bb.Board()
        self.history.clear()
        self.future.clear()
        self.move_times.clear()
        self.refresh()
        self.status.set(self._match_status())
        self._match_refresh_win()
        self._match_trigger_next()

    def _match_side_stufe(self):
        """Stufe des Spielers am Zug: Gelb beginnt normal; bei Wechsel und
        gerader Partie beginnt Rot (Farben getauscht). Die Engine-Namen
        (gelb/rot) bleiben am Brett kleben: Gelb = Anziehender."""
        m = self._match
        if self._match_gelb_beginnt():
            return m["gelb"] if len(self.history) % 2 == 0 else m["rot"]
        return m["rot"] if len(self.history) % 2 == 0 else m["gelb"]

    def _match_delay_ms(self):
        """Pause zwischen Match-Zuegen in ms: normal 350 (ruhig + sichtbar),
        'Schnell' 0 (nur noch Rechenzeit). 'Nur Ergebnisse' ist IMPLIZIT
        immer schnell – auch ohne angekreuztes 'Schnell'."""
        try:
            if self._match is not None and (self._match.get("schnell")
                                            or self._match.get("blind")):
                return 0
        except Exception:
            pass
        return 350

    def _match_blind(self):
        """'Nur Ergebnisse': kein Brett/keine Infobox pro Zug (nur Stand am
        Partieende). Gilt auch fuer die Stufen-Anzeige (bleibt stehen)."""
        try:
            return bool(self._match is not None and self._match.get("blind"))
        except Exception:
            return False

    def _match_trigger_next(self):
        """Naechsten Match-Zug anstossen (debounced, nur wenn Brett lebt).
        Die Statuszeile wird hier NICHT angefasst (Wunsch Patrick: kein
        'denkt...' pro Zug -> ruhige Zeile, nur der Stand zaehlt)."""
        if not self._match_mode():
            return
        if self.board.is_game_over() or self.thinking:
            return
        if self._match_after is not None:
            try:
                self.after_cancel(self._match_after)
            except Exception:
                pass
        self._match_after = self.after(self._match_delay_ms(),
                                       self._match_do_move)

    def _match_do_move(self):
        self._match_after = None
        if not self._match_mode():
            return
        if self.board.is_game_over() or self.thinking:
            return
        # Mensch-Seite: nicht rechnen, sondern auf Klick/Taste warten.
        # Statuszeile bleibt ruhig (Stand steht schon seit Partiebeginn).
        if self._match_side_stufe() == "mensch":
            return
        self.engine_move(stufe=self._match_side_stufe())

    def _match_after_move(self, col, dt):
        """Nach jedem Match-Zug: Brettende? sonst weiter. Die Statuszeile
        bleibt waehrend der Partie ruhig (Wunsch Patrick): Sie wird nur zu
        Partiebeginn geschrieben und bei Partie-/Matchende aktualisiert
        (Stand/Elo), NICHT nach jedem Zug.
        Stufe 1 (28.09.2026): Bei Delay 0 (Schnell/Nur Ergebnisse) direkt
        den naechsten Zug starten statt Umweg ueber _match_trigger_next
        (spart 1 Mainloop-Roundtrip pro Zug). Mit Pause bleibt der alte
        Zwei-Stufen-Weg (ruhig + sichtbar)."""
        m = self._match
        stufe = getattr(self, "_match_stufe", None) or self._match_side_stufe()
        if self.board.is_game_over():
            self.finish_info()
            self._match_finish_game()
            return
        if self._match_mode():
            if self._match_delay_ms() == 0:
                # Direkter naechster Zug (ein Roundtrip gespart).
                if self.board.is_game_over() or self.thinking:
                    return
                # Fix 04.10.2026: Mensch-Seite NICHT vom Computer ziehen
                # lassen (vorher spielte die Engine im Tempo Schnell/Turbo
                # nach dem 1. Klick alle Zuege des Menschen mit).
                if self._match_side_stufe() == "mensch":
                    return
                self.engine_move(stufe=self._match_side_stufe())
                return
            self._safe_after(self._match_delay_ms(),
                             self._match_trigger_next)

    def _match_finish_game(self):
        """Partie werten (Sieg = 1 Punkt fuer Gelb/Rot-Seite), naechste
        Partie oder Matchende. Farben: Gelb gewinnt -> gelb-Seite punktet.
        Zusaetzlich: Mensch-vs-Computer-Sitzungsstand (Spielstand-Feld)
        pro Gegnerstufe (farbwechsel-sicher ueber sieger_key).
        Mensch beteiligt ODER Tempo Normal -> 3 s Pause vor der naechsten
        Partie (User-Wunsch: Ergebnis wirken lassen + pruefen, wer wirklich
        gewinnt); Schnell/Turbo laufen sofort weiter."""
        m = self._match
        w = self.board.winner()
        # Gewinner-Identitaet (Stufenschluessel der siegenden SEITE),
        # None bei Remis. Farbwechsel-sicher ueber _match_gelb_beginnt.
        sieger_key = None
        if w is None or w == 0:
            m["remis"] += 1
        elif int(w) == 1:
            # Anziehender (Gelb am Brett) gewinnt. Punkt fuer die Seite,
            # die in dieser Partie Gelb gespielt hat.
            if self._match_gelb_beginnt():
                m["punkte_gelb"] += 1
                sieger_key = m["gelb"]
            else:
                sieger_key = m["rot"]
        else:
            # Rot (Nachziehender) gewinnt. Punkt fuer die Seite, die in
            # dieser Partie Rot gespielt hat. BUGFIX 29.09.2026: punkte_gelb
            # wurde hier NIE erhoeht - Siege der Gelb-Seite als Rot (jede
            # gerade Partie bei Farbwechsel) wurden der Rot-Seite
            # gutgeschrieben. Ohne Wechsel fiel das nie auf (Gelb-Seite =
            # immer Gelb). Mit Wechsel hat es die Gelb-Seite systematisch
            # bestohlen (Fordernd vs. Mittel: ~50 Punkte auf Rot verbucht).
            if not self._match_gelb_beginnt():
                m["punkte_gelb"] += 1
                sieger_key = m["gelb"]
            else:
                sieger_key = m["rot"]
        # Sitzungsstand Mensch-vs-Computer (nur beendete Partien, kein
        # Abbruch – diese Funktion laeuft nur bei echtem Partieende).
        try:
            self._stand_add_result(m.get("gelb"), m.get("rot"), sieger_key)
        except Exception:
            pass
        # Naechste Partie oder Ende.
        if m["nr"] >= m["spiele"]:
            m["fertig"] = True
            try:
                self._match_stufe = None
            except Exception:
                pass
            try:
                self.status.set(cfs_lang.tf("match_ended_status",
                                              res=self._match_result_text()))
            except Exception:
                pass
            try:
                self.finish_info()
            except Exception:
                pass
            try:
                self._match_refresh_win()
            except Exception:
                pass
            # Matchende: Fenster in den Vordergrund holen (Wunsch Patrick).
            try:
                win = getattr(self, "_match_win", None)
                if win is not None:
                    win.winfo_exists()
                    win.deiconify()
                    win.lift()
                    win.focus_force()
            except Exception:
                pass
            return
        m["nr"] += 1
        # Pause? Mensch beteiligt ODER Tempo Normal (ruhiges Zuschauen;
        # Wunsch Patrick 30.09.2026: auch bei Computer-Turnieren in Normal
        # soll man das Endergebnis 3 s sehen). Schnell/Turbo -> sofort.
        # Stop waehrend der Pause: _match_after loeschen (machen
        # _match_stop/_match_cancelled automatisch).
        try:
            mensch_dabei = (m.get("gelb") == "mensch"
                            or m.get("rot") == "mensch")
        except Exception:
            mensch_dabei = False
        try:
            normal_tempo = not (m.get("schnell") or m.get("blind"))
        except Exception:
            normal_tempo = True
        if mensch_dabei or normal_tempo:
            if getattr(self, "_match_after", None) is not None:
                try:
                    self.after_cancel(self._match_after)
                except Exception:
                    pass
            try:
                self.status.set(self.status.get() + cfs_lang.t("match_next_in"))
            except Exception:
                pass
            self._match_after = self.after(3000, self._match_next_game)
            return
        self._new_match_game()

    def _match_next_game(self):
        """Naechste Matchpartie nach der 3-s-Pause (nur Mensch-Turniere).
        Stop waehrend der Pause -> kein Start (Match ist fertig/abgebrochen
        oder _match_after wurde geloescht)."""
        self._match_after = None
        try:
            if not self._match_mode():
                return
        except Exception:
            return
        self._new_match_game()

    def _match_cancelled(self):
        """Stop waehrend Denken/Rechnen: Match als abgebrochen markieren,
        Ergebnis bleibt kopierbar, Navigation wieder frei."""
        m = self._match
        if m is not None:
            m["fertig"] = True
            m["abgebrochen"] = True
        try:
            self._match_stufe = None
        except Exception:
            pass
        if getattr(self, "_match_after", None) is not None:
            try:
                self.after_cancel(self._match_after)
            except Exception:
                pass
            self._match_after = None
        self.status.set(cfs_lang.tf("match_stopped_status", res=(
            self._match_result_text() if m is not None else "")))
        self._match_refresh_win()

    def _match_stop(self, cancelled=False):
        """Computer-Computer Match beenden (Stop-Menue). cancelled=True: als abgebrochen
        werten; sonst still (z.B. Programmende/Neustart). Navigation wird
        frei, Brett bleibt zur Inspektion stehen."""
        m = getattr(self, "_match", None)
        if m is None or m.get("fertig", False):
            return
        m["fertig"] = True
        if cancelled:
            m["abgebrochen"] = True
        try:
            self._match_stufe = None
        except Exception:
            pass
        if getattr(self, "_match_after", None) is not None:
            try:
                self.after_cancel(self._match_after)
            except Exception:
                pass
            self._match_after = None
        if cancelled:
            self.status.set(cfs_lang.tf("match_stopped_status",
                                          res=self._match_result_text()))
        self._match_refresh_win()

    # ---------- Spielstand (Mensch vs. Computer) ----------
    # Sitzungs-Zaehler unter der Infobox (Wunsch Patrick). Pro Gegnerstufe:
    # self._stand[comp_key] = [siege_mensch, siege_comp, remis]. Anzeige
    # 'Mensch vs <Stufenname>'. Turnier mit Mensch: farbwechsel-sicher
    # ueber Brettgewinner + _match_gelb_beginnt (Siegerseite statt Farbe).
    # Nur beendete Partien (kein Stop/Abbruch): gebucht wird aus
    # _match_finish_game (Turnier mit Mensch) und aus after_engine /
    # after_human (normales Mensch-vs-Computer-Spiel). An/Aus=aus ->
    # NICHTS wird gebucht (Inhalt leer); Reset -> 0-0 (Paar bleibt).
    # STUFENWECHSEL-Reset (Wunsch Patrick): neu gegen eine andere Stufe
    # spielen -> deren Stand wird auf 0-0 gesetzt + angezeigt
    # (_stand_reset_to, gerufen aus switch_depth; dahinter steckt
    # _apply_stufe, das auch Selbstspiel/Selbstwahl bedient).
    def _stand_reset_to(self, comp_key):
        """Spielstand auf 0-0 fuer diese Gegnerstufe setzen + anzeigen.
        Bei An/Aus=aus: Stand trotzdem anlegen, Inhalt leer lassen."""
        try:
            if comp_key == "mensch":
                return
            if comp_key not in self.STUFEN and comp_key not in (
                    "user1", "user2", "verlierer"):
                return
            self._stand[comp_key] = [0, 0, 0]
            if getattr(self, "_stand_enabled", False):
                self._stand_show(comp_key)
            else:
                self._stand_clear_text()
        except Exception:
            pass
    def _stand_pair_key_normal(self, comp_key):
        """Paar-Key fuers normale Spiel: comp_key (Gegnerstufe) oder None.
        User-Keys sind eigene Gegner (eigene Toepfe)."""
        try:
            if comp_key == "mensch":
                return None
            if comp_key in ("user1", "user2"):
                return comp_key
            if comp_key == "verlierer":
                return comp_key
            if comp_key not in self.STUFEN and comp_key != "verlierer":
                return None
            return comp_key
        except Exception:
            return None

    def _stand_book_normal(self, sieger_mensch):
        """Beendete Normal-Partie (Mensch vs. Computer) einbuchen.
        sieger_mensch: True (Mensch gewann), False (Computer), None (Remis).
        Bei An/Aus=aus: nichts buchen. Paare je Gegnerstufe."""
        try:
            if not getattr(self, "_stand_enabled", False):
                return
            comp = self._stufe_key()
            pair = self._stand_pair_key_normal(comp)
            if pair is None:
                return
            z = self._stand.get(pair)
            if z is None:
                z = [0, 0, 0]
                self._stand[pair] = z
            if sieger_mensch is None:
                z[2] += 1
            elif sieger_mensch:
                z[0] += 1
            else:
                z[1] += 1
            self._stand_show(pair)
        except Exception:
            pass

    def _stand_key(self, gelb, rot):
        """Comp-Key fuers Turnier mit Mensch (Gegnerstufe) oder None.
        Reine Computer-Matches -> None (Turnierfenster reicht).
        User-Gegner sind eigene Toepfe ('user1'/'user2')."""
        try:
            if gelb == "mensch" and rot != "mensch":
                if rot in ("user1", "user2"):
                    return rot
                if rot == "verlierer":
                    return rot
                return rot if rot in self.STUFEN else None
            if rot == "mensch" and gelb != "mensch":
                if gelb in ("user1", "user2"):
                    return gelb
                if gelb == "verlierer":
                    return gelb
                return gelb if gelb in self.STUFEN else None
        except Exception:
            pass
        return None

    def _stand_add_result(self, gelb, rot, sieger_key):
        """Eine beendete Turnier-Partie mit Mensch einbuchen.
        sieger_key: Stufenschluessel der Siegerseite oder None (Remis).
        Bei An/Aus=aus wird NICHTS gebucht (Inhalt ist leer)."""
        try:
            if not getattr(self, "_stand_enabled", False):
                return
        except Exception:
            return
        pair = self._stand_key(gelb, rot)
        if pair is None:
            return  # reines Computer-Match -> kein Spielstand-Feld
        try:
            z = self._stand.get(pair)
            if z is None:
                z = [0, 0, 0]
                self._stand[pair] = z
            if sieger_key is None:
                z[2] += 1
            elif sieger_key == "mensch":
                z[0] += 1
            else:
                z[1] += 1
        except Exception:
            return
        try:
            self._stand_show(pair)
        except Exception:
            pass

    def _stand_show(self, pair=None):
        """Spielstand-Feld aktualisieren (Frame bleibt IMMER sichtbar).
        pair: comp_key (Gegnerstufe). Ohne pair: letztes Paar.
        Bei An/Aus=aus: Inhalt leer (nur Titel 'Spielstand' steht)."""
        try:
            if not getattr(self, "_stand_enabled", False):
                self._stand_clear_text()
                return
            if pair is None:
                if not getattr(self, "_stand", None):
                    self._stand_clear_text()
                    return
                pair = next(reversed(self._stand))
            z = self._stand.get(pair)
            if z is None:
                self._stand_clear_text()
                return
            sm, sc, rem = z
            pm = sm + 0.5 * rem
            pc = sc + 0.5 * rem
            partien = sm + sc + rem

            def _kurz(x):
                if abs(x - round(x)) < 1e-9:
                    return str(int(round(x)))
                return cfs_lang.fmt_decimal(f"{x:.1f}")
            try:
                head = cfs_lang.tf("stand_head", x=self._stufe_label_for(pair))
            except Exception:
                head = cfs_lang.t("stand_head_default")
            self._stand_head_var.set(head)
            self._stand_big_var.set(f"{_kurz(pm)}-{_kurz(pc)}")
            self._stand_sub_var.set(cfs_lang.tf("stand_sub", w=sm, d=rem, l=sc,
                                                n=partien))
            # Elo erst, wenn BEIDE Seiten >= 0,5 Punkte haben.
            # (Gleichstand 1,5-1,5 -> 'Elo ±0' statt '-0'.)
            if pm >= 0.5 and pc >= 0.5 and partien > 0:
                try:
                    elo = self._match_elo(pm, partien)
                    if elo is None:
                        elo_txt = "–"
                    elif abs(elo) < 0.5:
                        elo_txt = "±0"
                    else:
                        elo_txt = f"{elo:+.0f}"
                except Exception:
                    elo_txt = "–"
                self._stand_elo_var.set(f"Elo {elo_txt}")
            else:
                self._stand_elo_var.set("")
        except Exception:
            pass

    def _stand_clear_text(self):
        """NUR die Texte loeschen (Frame/Titel 'Spielstand' bleibt)."""
        try:
            self._stand_head_var.set("")
            self._stand_big_var.set("")
            self._stand_sub_var.set("")
            self._stand_elo_var.set("")
        except Exception:
            pass

    def _stand_hide(self):
        """Altlast (Frame bleibt jetzt immer stehen): leert nur den Text,
        damit kein Fremdaufruf das Feld verschwinden laesst."""
        try:
            self._stand_clear_text()
        except Exception:
            pass

    def _stand_toggle(self):
        """An/Aus-Schalter (Wunsch Patrick): NUR der Text geht weg, der
        Frame mit Titel 'Spielstand' bleibt IMMER stehen. Aus = Zaehler
        pausieren (Inhalt leer); An = 0-0 (falls noch nichts gezaehlt)
        bzw. aktueller Stand. Synchronisiert den Ansicht-Menuehaken."""
        try:
            self._stand_enabled = not getattr(self, "_stand_enabled", False)
            try:
                self.stand_var.set(bool(self._stand_enabled))
            except Exception:
                pass
            if self._stand_enabled:
                if getattr(self, "_stand", None):
                    self._stand_show()
                else:
                    # Frisch aktiviert: 0-0 gegen aktuelle Gegnerstufe.
                    try:
                        comp = self._stufe_key()
                    except Exception:
                        comp = "perfekt"
                    try:
                        if comp == "mensch" or (comp not in self.STUFEN and comp != "verlierer"):
                            comp = "perfekt"
                    except Exception:
                        comp = "perfekt"
                    pair = comp
                    try:
                        if pair not in self._stand:
                            self._stand[pair] = [0, 0, 0]
                    except Exception:
                        pass
                    self._stand_show(pair)
            else:
                self._stand_clear_text()
        except Exception:
            pass
        try:
            self.stand_var.set(bool(getattr(self, "_stand_enabled", False)))
        except Exception:
            pass

    def toggle_stand_menu(self):
        """Ansicht > Spielstand ein/aus: Menuehaken -> Anzeige umschalten.
        Der Feld-Button toggelt unbedingt; das Menue setzt den Wunschzustand."""
        try:
            want = bool(self.stand_var.get())
        except Exception:
            want = not getattr(self, "_stand_enabled", False)
        try:
            if want != bool(getattr(self, "_stand_enabled", False)):
                self._stand_toggle()
            else:
                # Bereits im Wunschzustand: nur Haken nachfuehren.
                self.stand_var.set(bool(getattr(self, "_stand_enabled", False)))
        except Exception:
            pass

    def _stand_reset(self):
        """Reset-Button (Wunsch Patrick): Zaehler auf 0-0, Frame bleibt.
        Das Paar (aktuelle Gegnerstufe) bleibt bestehen, damit sofort
        weitergezaehlt werden kann. Bei An/Aus=aus bleibt der Inhalt
        leer (nichts zu zeigen)."""
        try:
            pair = None
            try:
                if getattr(self, "_stand", None):
                    pair = next(reversed(self._stand))
            except Exception:
                pair = None
            if pair is None:
                try:
                    comp = self._stufe_key()
                except Exception:
                    comp = "perfekt"
                try:
                    if comp == "mensch" or comp not in self.STUFEN:
                        comp = "perfekt"
                except Exception:
                    comp = "perfekt"
                pair = comp
            self._stand[pair] = [0, 0, 0]
            if getattr(self, "_stand_enabled", False):
                self._stand_show(pair)
            else:
                self._stand_clear_text()
        except Exception:
            pass

    def clear_hash(self):
        """ENTFERNT (Wunsch Patrick 30.09.2026): Menueeintrag 'Hashtabelle
        loeschen' gestrichen. Methode bleibt als No-Op, falls noch irgendwo
        referenziert (TT wird intern weiter pro Partie/Analyse verwaltet)."""
        try:
            self.status.set(cfs_lang.t("status_removed_hash"))
        except Exception:
            pass

    def switch_set(self):
        try:
            want = int(self.set_var.get())
        except Exception:
            return
        if want not in SET_IDS:
            return
        self.set_no = want
        self.canvas.config(width=COLS * self.cell, height=self.canvas_h(),
                           background=self.raw[self.set_no].get("edge", BOARD_BG))
        self.draw()
        self._layout_boardbox()
        self.fit_zoom_to_window()
        self.status.set(cfs_lang.tf("status_set_changed", no=self.set_no,
                                  name=cfs_sets.set_display_name(self.set_no)))

    def cycle_set(self, direction=+1):
        """Stein-Set wechseln (Mausrad/Bild-rauf/runter): naechstes/
        vorheriges aus den MENUE-Sets (gleiche Reihenfolge wie im Menue:
        _SET_ORDER via set_menu_order). direction +1 = vor, -1 = zurueck;
        Wrap-around. Auch im Menue sichtbar (Radio folgt ueber set_var)."""
        try:
            ids = [s for s in set_menu_order(self.raw) if s in _MENU_SETS]
            if not ids:
                return
            i = ids.index(self.set_no) if self.set_no in ids else 0
            nxt = ids[(i + direction) % len(ids)]
            self.set_var.set(nxt)
            self.switch_set()
        except Exception:
            pass

    def set_gallery(self):
        """ENTFERNT: Galerie gestrichen – zu kleine Bilder. No-Op,
        falls noch referenziert. Sets kommen aus _MENU_SETS."""
        try:
            self.status.set(cfs_lang.t("status_removed_gallery"))
        except Exception:
            pass

    def toggle_show_last(self):
        self.show_last = self.show_var.get()
        self.draw()

    def toggle_ghost(self):
        self.ghost = self.ghost_var.get()
        self.draw()

    def toggle_anim(self):
        self.anim = self.anim_var.get()

    def toggle_two_player(self):
        self._selfplay_stop()
        self.two_player = True
        try:
            self.opp_var.set("2-Spieler (beide Mensch)")
        except Exception:
            pass
        self.status.set(cfs_lang.t("status_two_player"))
        self.schedule_auto_analyze()

    def _set_auto_analyze(self, on, silent=False):
        """Dauer-Analyse umschalten; Menue UND Button bleiben synchron.
        Bei 'aus' wird sofort auf 1-7 zurueckgeblendet (kein Nachstart)."""
        self.auto_analyze = bool(on)
        try:
            self.ana_var.set(bool(on))
        except Exception:
            pass
        if not on:
            self._ana_seq += 1  # laufende Analyse entwerten
            self._ana_pending = None
            self.scores_visible = False
            self._clear_scores()
            if not silent:
                self.status.set(cfs_lang.t("status_autoanalysis_off"))
            return
        if not silent:
            self.status.set(cfs_lang.t("status_autoanalysis_on"))
        self.schedule_auto_analyze()

    def toggle_auto_analyze(self):
        self._set_auto_analyze(self.ana_var.get())

    def toggle_auto_analyze_btn(self):
        """'Analyse'-Button: wie das Menue (Umschalter)."""
        self._set_auto_analyze(not self.ana_var.get())

if __name__ == "__main__":
    app = ConnectFourStudio()
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        try:
            s = open(sys.argv[1], encoding="ascii", errors="ignore").read().strip()
            moves = [int(c) - 1 for c in s if c in "1234567"]
            for m in moves:
                if app.board.is_game_over():
                    break
                if app.board.is_legal_move(m):
                    app.history.append(m)
                    app.board.play(m)
            app.rebuild()
            app.refresh(all_scores=True)
        except Exception as e:
            print(cfs_lang.t("err_start_position"), e)
    app.mainloop()
