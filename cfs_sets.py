"""Stein-Sets für ConnectFour Studio (ausgelagert 01.10.2026).

Enthält alles rund um Brett-/Steinoptik:
- Konstanten SET_NAMES, _SET_ORDER, _MENU_SETS, SET_IDS (beim Import
  aus data/images erkannt), START_SET
- set_menu_order(raw): Menü-Reihenfolge
- SetArt: Laden der Rohgrafiken (HiRes-PNG bevorzugt, BMP-Fallback),
  Kantenfarbe + Stein-Radien (Floodfill + Differenz-Deckel + Ring-Test)
- SetTiles: Zoom-Cache für Tk-PhotoImages (back/red/yellow + Ghost)

Anbindung an die App: die Klasse ConnectFourStudio hält nur noch
  self.set_no, self.set_var, self.raw (= {nr: {...}}), self.tile_cache
und delegiert Laden/Cachen an dieses Modul. So bleibt die Hauptdatei
schlank; neue Sets = neuer Ordner data/images/set<N> + Eintrag unten.
"""

import os

from PIL import Image, ImageTk

# Basis-Ordner: <projekt>/data (neben diesem Modul: <projekt>/cfs_sets.py).
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
IMAGE_DIR = os.path.join(DATA_DIR, "images")

# --- Start-Set (frisch, keine Alt-INI): ConnectFour Studio startet mit Set 1. ---
START_SET = 1


def available_sets():
    """Alle vorhandenen set<N>-Ordner unter data/images (mit back.bmp)."""
    found = []
    try:
        base = IMAGE_DIR
        for name in os.listdir(base):
            if not name.startswith("set"):
                continue
            if not name[3:].isdigit():
                continue
            if not os.path.isdir(os.path.join(base, name)):
                continue
            back = os.path.join(base, name, "back.bmp")
            if os.path.isfile(back):
                found.append(int(name[3:]))
        found.sort()
    except Exception:
        pass
    return found or [1, 2, 3, 4, 5]


SET_IDS = available_sets()

# Stein-Sets + Anzeigereihenfolge (ConnectFour Studio, 04.10.2026):
# 20 Sets, durchnummeriert 1-20 (Set 11 Blau-Matt geloescht;
# alte 12-21 je -1).
# _SET_ORDER ist die Master-Reihenfolge fuer Menue +
# cycle_set (Mausrad/Bild-rauf/runter, gleiche Reihenfolge, Wrap-around).
_SET_ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
              13, 14, 15, 16, 17, 18, 19, 20]
_MENU_SETS = set(_SET_ORDER)

# Anzeige-Namen der Sets (ConnectFour Studio, 04.10.2026).
# Vortex (vorher 20) steht jetzt auf 8; die alten 8-19 rutschen je +1.
# 03.10.2026: Blau-Gelb-Rot (11) geloescht, Rest 12-15 je -1;
# Hellblau (15) + Dunkelblau (16) neu, Rest 16-20 je +1 (jetzt 17-21).
# 04.10.2026: Blau-Matt (11) geloescht, Rest 12-21 je -1 (jetzt 11-20).
SET_NAMES = {1: "Blau-Hochglanz", 2: "Sandstein",
             3: "Silbergrau", 4: "Creme",
             5: "Schiefer-Blau",
             6: "Walnuss-Bernstein-Rubin",
             7: "Jade-Perlmutt-Lapis", 8: "Vortex",
             9: "Königsblau", 10: "Flat-Blau",
             11: "Petrol", 12: "Schoko",
             13: "Ocker", 14: "Hellblau",
             15: "Dunkelblau", 16: "Mint",
             17: "Mitternacht", 18: "Schiefer",
             19: "Schwarz-Gelb-Rot", 20: "Malachit"}


def set_menu_order(raw):
    """Menue-Reihenfolge der Sets: exakt _SET_ORDER (1-20).
    Neue Ordner ausserhalb von _MENU_SETS erscheinen NICHT im Menue."""

    try:
        have = set(raw) if raw is not None else set()
    except Exception:
        have = set()
    return [s for s in _SET_ORDER if s in have]


SET_NAMES_EN = {1: "Glossy Blue", 2: "Sandstone",
                3: "Silver Gray", 4: "Cream",
                5: "Slate Blue",
                6: "Walnut-Amber-Ruby",
                7: "Jade-Pearl-Lapis", 8: "Vortex",
                9: "Royal Blue", 10: "Flat Blue",
                11: "Petrol", 12: "Chocolate",
                13: "Ochre", 14: "Light Blue",
                15: "Dark Blue", 16: "Mint",
                17: "Midnight", 18: "Slate",
                19: "Black-Yellow-Red", 20: "Malachite"}


SET_NAMES_ES = {1: "Azul brillante", 2: "Arenisca",
                3: "Gris plata", 4: "Crema",
                5: "Azul pizarra",
                6: "Nogal-Ámbar-Rubí",
                7: "Jade-Nácar-Lapislázuli", 8: "Vórtice",
                9: "Azul real", 10: "Azul plano",
                11: "Petróleo", 12: "Chocolate",
                13: "Ocre", 14: "Azul claro",
                15: "Azul oscuro", 16: "Menta",
                17: "Medianoche", 18: "Pizarra",
                19: "Negro-Amarillo-Rojo", 20: "Malaquita"}


SET_NAMES_FR = {1: "Bleu brillant", 2: "Grès",
                3: "Gris argent", 4: "Crème",
                5: "Bleu ardoise",
                6: "Noyer-Ambre-Rubis",
                7: "Jade-Nacre-Lapis", 8: "Vortex",
                9: "Bleu roi", 10: "Bleu uni",
                11: "Pétrole", 12: "Chocolat",
                13: "Ocre", 14: "Bleu clair",
                15: "Bleu foncé", 16: "Menthe",
                17: "Minuit", 18: "Ardoise",
                19: "Noir-Jaune-Rouge", 20: "Malachite"}


SET_NAMES_IT = {1: "Blu lucido", 2: "Arenaria",
                3: "Grigio argento", 4: "Crema",
                5: "Blu ardesia",
                6: "Noce-Ambra-Rubino",
                7: "Giada-Perla-Lapislazzuli", 8: "Vortice",
                9: "Blu reale", 10: "Blu piatto",
                11: "Petrolio", 12: "Cioccolato",
                13: "Ocra", 14: "Azzurro",
                15: "Blu scuro", 16: "Menta",
                17: "Mezzanotte", 18: "Ardesia",
                19: "Nero-Giallo-Rosso", 20: "Malachite"}


SET_NAMES_NL = {1: "Glanzend blauw", 2: "Zandsteen",
                3: "Zilvergrijs", 4: "Crème",
                5: "Leisteenblauw",
                6: "Walnoot-Amber-Robijn",
                7: "Jade-Parel-Lapis", 8: "Vortex",
                9: "Koningsblauw", 10: "Effen blauw",
                11: "Petrol", 12: "Chocolade",
                13: "Oker", 14: "Lichtblauw",
                15: "Donkerblauw", 16: "Munt",
                17: "Middernacht", 18: "Leisteen",
                19: "Zwart-Geel-Rood", 20: "Malachiet"}


def set_display_name(no, lang=None):
    """Anzeigename für Statuszeile/Menü ('?' bei unbekannt), in der
    aktiven Sprache (lang=None) bzw. in `lang`; Fallback Deutsch."""
    if lang is None:
        try:
            import cfs_lang
            lang = cfs_lang.LANG
        except Exception:
            lang = "de"
    if lang == "en":
        return SET_NAMES_EN.get(no, SET_NAMES.get(no, "?"))
    if lang == "es":
        return SET_NAMES_ES.get(no, SET_NAMES.get(no, "?"))
    if lang == "fr":
        return SET_NAMES_FR.get(no, SET_NAMES.get(no, "?"))
    if lang == "nl":
        return SET_NAMES_NL.get(no, SET_NAMES.get(no, "?"))
    if lang == "it":
        return SET_NAMES_IT.get(no, SET_NAMES.get(no, "?"))
    return SET_NAMES.get(no, "?")


def _flood_r(tex, tol=70):
    """Stein-Radius (relativ): Floodfill ab Kachelmitte, 128er-Raster."""
    him = tex.resize((128, 128)).convert("RGB")
    pp = him.load()
    size = 128
    cc = size // 2
    mr, mg, mb = pp[cc, cc]
    t2 = tol * tol
    seen = bytearray(size * size)
    stack = [(cc, cc)]
    x0 = x1 = y0 = y1 = None
    while stack:
        xx_, yy_ = stack.pop()
        if not (0 <= xx_ < size and 0 <= yy_ < size):
            continue
        ii = yy_ * size + xx_
        if seen[ii]:
            continue
        rr_, gg_, bb_ = pp[xx_, yy_]
        dr_ = rr_ - mr
        dg_ = gg_ - mg
        db_ = bb_ - mb
        if dr_ * dr_ + dg_ * dg_ + db_ * db_ >= t2:
            continue
        seen[ii] = 1
        if x0 is None:
            x0 = x1 = xx_
            y0 = y1 = yy_
        else:
            if xx_ < x0:
                x0 = xx_
            if xx_ > x1:
                x1 = xx_
            if yy_ < y0:
                y0 = yy_
            if yy_ > y1:
                y1 = yy_
        stack.append((xx_ + 1, yy_))
        stack.append((xx_ - 1, yy_))
        stack.append((xx_, yy_ + 1))
        stack.append((xx_, yy_ - 1))
    if x0 is None or (x1 - x0) < 10 or (y1 - y0) < 10:
        return 0.39
    return ((x1 - x0) + (y1 - y0)) / 4 / size


def _gap_sat(tex, r_in, r_out):
    """Ring-Test: Sättigung mittig in der Lücke (Metall vs. Verlauf)."""
    import math as _math
    him = tex.resize((256, 256)).convert("RGB")
    pp = him.load()
    mid = (r_in + r_out) / 2 * 256
    sats = []
    for k in range(8):
        a = _math.pi / 4 * k
        x = min(255, max(0, int(round(
            128 + _math.cos(a) * mid))))
        y = min(255, max(0, int(round(
            128 + _math.sin(a) * mid))))
        rr_, gg_, bb_ = pp[x, y]
        mx_ = max(rr_, gg_, bb_)
        mn_ = min(rr_, gg_, bb_)
        sats.append((mx_ - mn_) / (mx_ + 1) * 255)
    sats.sort()
    return (sats[3] + sats[4]) / 2


class SetArt:
    """Rohgrafiken laden + vermessen. Ergebnis: dict {nr: {...}}.

    Eintrag je Set: back/red/yellow (PIL-RGBA), edge (Hex-Farbe),
    stone_r_y/stone_r_r/stone_r (relativ zur Kachel).
    Reines PIL, kein numpy.
    """

    @staticmethod
    def load_all(numbers=None):
        raw = {}
        if numbers is None:
            try:
                numbers = sorted(int(n[3:]) for n in os.listdir(IMAGE_DIR)
                                 if n.startswith("set") and n[3:].isdigit()
                                 and os.path.isdir(os.path.join(IMAGE_DIR, n)))
            except Exception:
                numbers = list(SET_IDS)
        for s in numbers:
            try:
                d = {}
                for name in ("back", "red", "yellow"):
                    # HiRes-Master (256x256) bevorzugen, falls vorhanden.
                    hi = os.path.join(IMAGE_DIR, f"set{s}",
                                      f"{name}_hires.png")
                    if os.path.exists(hi):
                        lo = hi
                    else:
                        lo = os.path.join(IMAGE_DIR, f"set{s}",
                                          f"{name}.bmp")
                    d[name] = Image.open(lo).convert("RGBA")
                # Ecken-Farbe (Median der 4 Kachel-Ecken von back): dient
                # als Canvas-Hintergrund, damit keine sichtbaren Nähte
                # zwischen den Kacheln entstehen.
                bg = d["back"].convert("RGB")
                w0, h0 = bg.size
                if w0 >= 7 and h0 >= 7:
                    corners = [bg.getpixel((2, 2)), bg.getpixel((w0 - 3, 2)),
                               bg.getpixel((2, h0 - 3)), bg.getpixel((w0 - 3, h0 - 3))]
                else:
                    corners = [bg.getpixel((0, 0))]
                d["edge"] = "#%02x%02x%02x" % tuple(
                    int(sum(c[i] for c in corners) / len(corners)) for i in range(3))
                # Differenz-Deckel (Union gelb/red vs. back, Schwelle 30).
                y256 = d["yellow"].resize((256, 256)).convert("RGB")
                r256 = d["red"].resize((256, 256)).convert("RGB")
                b256 = d["back"].resize((256, 256)).convert("RGB")
                py_, pr_, pb_ = y256.load(), r256.load(), b256.load()
                col_any = [False] * 256
                row_any = [False] * 256
                for yy_ in range(256):
                    for xx_ in range(256):
                        r1_, g1_, b1_ = py_[xx_, yy_]
                        r2_, g2_, b2_ = pb_[xx_, yy_]
                        if (abs(r1_ - r2_) + abs(g1_ - g2_)
                                + abs(b1_ - b2_) > 30):
                            col_any[xx_] = True
                            row_any[yy_] = True
                            continue
                        r1_, g1_, b1_ = pr_[xx_, yy_]
                        if (abs(r1_ - r2_) + abs(g1_ - g2_)
                                + abs(b1_ - b2_) > 30):
                            col_any[xx_] = True
                            row_any[yy_] = True
                try:
                    dx0 = col_any.index(True)
                    dx1 = 255 - col_any[::-1].index(True)
                    dy0 = row_any.index(True)
                    dy1 = 255 - row_any[::-1].index(True)
                    cap = ((dx1 - dx0) + (dy1 - dy0)) / 4 / 256 - 1 / 256
                except ValueError:
                    cap = 0.40
                fry = _flood_r(d["yellow"])
                frr = _flood_r(d["red"])
                # Deckel + Ring-Test.
                if fry > cap:
                    fry = cap
                elif cap - fry > 0.012 and _gap_sat(
                        d["yellow"], fry, cap) < 40:
                    pass  # Metall-Luecke: Farbe umschliessen
                elif cap - fry > 0.012:
                    fry = cap  # Verlauf: Scheibe geht weiter
                if frr > cap:
                    frr = cap
                elif cap - frr > 0.012 and _gap_sat(
                        d["red"], frr, cap) < 40:
                    pass
                elif cap - frr > 0.012:
                    frr = cap
                d["stone_r_y"] = fry
                d["stone_r_r"] = frr
                d["stone_r"] = max(d["stone_r_y"], d["stone_r_r"])
                raw[s] = d
            except Exception:
                continue
        return raw


class SetTiles:
    """Zoom-Cache für Tk-PhotoImages. Braucht raw-Dict + set_no/zoom
    der App (als referenziertes Objekt mit .raw/.set_no/.zoom)."""

    def __init__(self, app):
        self.app = app
        self.cache = {}
        # Pinned Keys (Fix 01.10.2026, 2. Review 2.1/2.2): gerade auf dem
        # Brett / im Am-Zuge-Feld angezeigte Bilder duerfen NICHT per
        # FIFO verdrängt werden (sonst räumt PIL den Tcl-Namen auf und
        # das Icon bleibt leer). draw() pinnt nach jedem Zeichnen.
        self.pinned = set()

    def _evict(self):
        """Nur NICHT-gepinnte Eintraege verdrängen (Fix 01.10.2026)."""
        LIMIT = 500
        if len(self.cache) <= LIMIT:
            return
        for key in list(self.cache):
            if key not in self.pinned:
                try:
                    del self.cache[key]
                except Exception:
                    pass
                if len(self.cache) <= LIMIT:
                    return

    def tile(self, kind):
        """Skalierte Kachel ('back'/'red'/'yellow', '*_ghost' = Vorschau
        mit halbiertem Alpha), Zoom-cached."""
        app = self.app
        key = (app.set_no, app.zoom, kind)
        im = self.cache.get(key)
        if im is None:
            raw = app.raw[app.set_no]
            bg = raw["back"]
            w0, h0 = bg.size
            w = max(8, int(round(w0 * app.zoom)))
            h = max(8, int(round(h0 * app.zoom)))
            cell = bg.resize((w, h), Image.LANCZOS).copy()
            if kind in ("red", "yellow"):
                cell.alpha_composite(raw[kind].resize((w, h), Image.LANCZOS))
            elif kind in ("red_ghost", "yellow_ghost"):
                fg = raw[kind[:-6]].resize((w, h), Image.LANCZOS).copy()
                a = fg.getchannel("A").point(lambda v: v // 2)  # halbtransparent
                fg.putalpha(a)
                cell.alpha_composite(fg)
            im = ImageTk.PhotoImage(cell)
            self.cache[key] = im
            self._evict()
        return im

    def tile_img(self, kind, w, h):
        """PIL-Kachel (kein PhotoImage) exakt auf w x h skaliert."""
        try:
            w, h = max(1, int(round(w))), max(1, int(round(h)))
            raw = self.app.raw[self.app.set_no]
            bg = raw["back"]
            cell = bg.resize((w, h), Image.LANCZOS).copy()
            if kind in ("red", "yellow"):
                cell.alpha_composite(raw[kind].resize((w, h), Image.LANCZOS))
            return cell
        except Exception:
            return None

    def clear(self):
        self.cache.clear()
