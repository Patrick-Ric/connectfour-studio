"""Mini-Eroeffnungsbuch "Buch 2d" (cfs_minibook).

Exakte Bewertungen aller 7 Zuege fuer die 57 Stellungen mit 0-2 Steinen
(Grundstellung, 7 nach dem ersten, 49 nach dem zweiten Halbzug), erzeugt mit
bitbully 0.0.79 (Vollsuche mit 12-ply-dist-Buch). Dort entfaellt die Suche:
Computer-Eroeffnung, Antwort auf den ersten Zug und Analyse sind sofort fertig.
Anzeige: Tiefe/Quelle "Buch 2d", 0 Knoten. Gleiche Daten in allen drei
Versionen (Tk, Qt, Android).
"""

import bitbully as bb

SHORT = "2d"
MAX_STONES = 2

# Schluessel: .4gp-Ziffernkette der Zuege ("" = Grundstellung),
# Wert: Scores der Spalten 1-7 aus Sicht der Seite am Zug.
_ROWS = {
    "": (-2, -1, 0, 1, 0, -1, -2),
    "1": (-1, 2, 1, 2, -1, 1, -2),
    "2": (-2, 0, 1, 0, -2, -2, -3),
    "3": (-2, -2, 0, 0, 0, 0, -3),
    "4": (-4, -2, -2, -1, -2, -2, -4),
    "5": (-3, 0, 0, 0, 0, -2, -2),
    "6": (-3, -2, -2, 0, 1, 0, -2),
    "7": (-2, 1, -1, 2, 1, 2, -1),
    "11": (-2, 0, 0, 1, -1, 1, -1),
    "12": (-2, -2, -3, -2, -2, -2, -2),
    "13": (-3, -3, -1, -3, -3, -2, -4),
    "14": (-5, -5, -5, -2, -5, -4, -4),
    "15": (-5, -4, -1, 1, -2, -2, -4),
    "16": (-3, -3, -2, -2, -2, -1, -2),
    "17": (-2, -1, -1, 2, -2, -1, -2),
    "21": (0, 2, 0, -2, 2, -2, -1),
    "22": (-3, -2, -2, -1, 0, -1, -2),
    "23": (-3, -1, -1, -3, -2, -2, -2),
    "24": (-5, 0, -4, 0, -3, -5, -4),
    "25": (-4, -2, -1, 2, -1, -2, -2),
    "26": (-3, 2, 0, 2, 2, 0, -2),
    "27": (-1, 3, 0, 3, 0, -2, -1),
    "31": (0, 0, 0, 2, 0, 0, -2),
    "32": (-3, 0, -1, -2, 0, 2, -2),
    "33": (-4, 0, -1, 0, -3, -2, -3),
    "34": (-5, -4, 0, 0, -3, -3, -5),
    "35": (-1, -1, 0, -2, 0, -2, -3),
    "36": (-2, 0, 0, 0, 0, 0, -2),
    "37": (-1, 0, 3, 3, 0, 2, -1),
    "41": (0, -2, 2, 4, 3, 3, 2),
    "42": (-2, 2, -2, 0, 0, 2, -2),
    "43": (-3, -3, 0, 0, -2, 2, 1),
    "44": (-3, -3, -2, 1, -2, -3, -3),
    "45": (1, 2, -2, 0, 0, -3, -3),
    "46": (-2, 2, 0, 0, -2, 2, -2),
    "47": (2, 3, 3, 4, 2, -2, 0),
    "51": (-1, 2, 0, 3, 3, 0, -1),
    "52": (-2, 0, 0, 0, 0, 0, -2),
    "53": (-3, -2, 0, -2, 0, -1, -1),
    "54": (-5, -3, -3, 0, 0, -4, -5),
    "55": (-3, -2, -3, 0, -1, 0, -4),
    "56": (-2, 2, 0, -2, -1, 0, -3),
    "57": (-2, 0, 0, 2, 0, 0, 0),
    "61": (-1, -2, 0, 3, 0, 3, -1),
    "62": (-2, 0, 2, 2, 0, 2, -3),
    "63": (-2, -2, -1, 2, -1, -2, -4),
    "64": (-4, -5, -3, 0, -4, 0, -5),
    "65": (-2, -2, -2, -3, -1, -1, -3),
    "66": (-2, -1, 0, -1, -2, -2, -3),
    "67": (-1, -2, 2, -2, 0, 2, 0),
    "71": (-2, -1, -2, 2, -1, -1, -2),
    "72": (-2, -1, -2, -2, -2, -3, -3),
    "73": (-4, -2, -2, 1, -1, -4, -5),
    "74": (-4, -4, -5, -2, -5, -5, -5),
    "75": (-4, -2, -3, -3, -1, -3, -3),
    "76": (-2, -2, -2, -2, -3, -2, -2),
    "77": (-1, 1, -1, 1, 0, 0, -2),
}

_TABLE = None


def _key(board):
    return tuple(tuple(col) for col in board.to_array())


def _table():
    global _TABLE
    if _TABLE is None:
        table = {}
        for moves, row in _ROWS.items():
            b = bb.Board()
            for ch in moves:
                b.play(int(ch) - 1)
            table[_key(b)] = row
        _TABLE = table
    return _TABLE


def scores(board):
    """Scores wie score_all_moves (dict, absteigend nach Wert, stabil) oder
    None, wenn die Stellung mehr als 2 Steine hat."""
    try:
        if 42 - board.moves_left() > MAX_STONES:
            return None
    except Exception:
        return None
    row = _table().get(_key(board))
    if row is None:
        return None
    return dict(sorted(enumerate(row), key=lambda kv: kv[1], reverse=True))
