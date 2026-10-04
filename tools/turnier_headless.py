"""Headless-Turnier: GUI-exakte Stufenlogik, ohne Tkinter.
Stand: 03.10.2026 — portiert aus connectfour_studio.py (kein Copy-Paste der
GUI-Klasse moeglich: pick_engine_move/_filtered_blunder/_short_wins sind
Methoden der Tk-App mit self._solver_lock/self.agent/self._move_stufe()).

GUI-Quellstand: Remis-Regeln gestrichen (02.10.2026), Gleichstand =
schnellster Gewinn / gleichschnelle wuerfeln / kein Gewinn <=10 -> alle
wuerfeln (02.10.2026), Perfekt-Verlust mit ml>10-Pool (02.10.2026).

Jeder Prozess hat eine EIGENE BitBully-Instanz (nicht threadsicher!).
Nutzung: worker-Funktion spielt 1 Partie; main verteilt per ProcessPool.
"""

import math
import os
import random
import sys

import bitbully as bb

LOSS_POWER = 8
BOOK = "12-ply-dist"

# (label, p, s, w) = cfs_levels.STUFEN (Stand 03.10.2026, finale 14er-Leiter).
# 'verlierer' = Stufe 0 (Spass-Stufe, eigene Logik in pick_move, kein p/s/w).
STUFEN = {
    "verlierer": ("0 Verlierer", 0, 0, 0),
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
    # Testkandidaten 03.10.2026 (nur headless, NICHT in GUI/Help):
    "takt_a": ("Taktiker (0,1,1)", 0, 1, 1),
    "takt_b": ("Taktiker (0,2,2)", 0, 2, 2),
    "takt_c": ("Taktiker (0,3,3)", 0, 3, 3),
    # Screening-Kandidaten (nur headless, NICHT in GUI/Help).
    # Stand 03.10.2026: auf finale 14er-Leiter umgebogen (alte Keys bleiben
    # als Aliase, damit alte Specs/Logs lesbar bleiben).
    "zw60": ("5 Fortgeschritten-Alias", 20, 1, 1),
    "zw30": ("Screen (30,1,1)", 30, 1, 1),
    "zw50": ("7 Mittel-Alias", 50, 1, 1),
    "zw62": ("Screen (62,2,2)", 62, 2, 2),
    "exp80": ("11 Experte-Alias", 80, 2, 2),
    "strat_a": ("Stratege (84,1,1)", 84, 1, 1),
    "strat_b": ("Stratege (92,1,1)", 92, 1, 1),
}
DEPTHS = [4, 6, 8, 10, 12, 14, 16, 18, 20, -1]

_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = bb.BitBully()
        _agent.max_depth = -1
        _agent.load_book(BOOK)
    return _agent


def moves_left(board, score):
    """GUI: ConnectFourStudio._moves_left (reine Funktion, headless ohne Lock)."""
    try:
        return bb.BitBully.score_to_moves_left(score, board)
    except Exception:
        return None


def short_wins(board, scores, w):
    """Gewinnmenge des Siegsschutzes: alle '+'-Zuege mit ml <= 2*w-1."""
    try:
        w = int(w) if w is not None else 0
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
            continue
        try:
            ml = bb.BitBully.score_to_moves_left(s, board)
        except Exception:
            continue
        if ml <= limit:
            menge.append(c)
    return menge


def filtered_blunder(board, scores, cutoff, w=None):
    """GUI: ConnectFourStudio._filtered_blunder (Stand 03.10.2026).

    Siegsschutz zuerst (Variante B), dann s-Filter. Remis (score 0) wird
    NICHT bevorzugt (02.10.2026 gestrichen): ein einzelnes Remis gegen
    lauter Verluste zaehlt wie jeder andere erlaubte Zug.
    """
    win_menge = short_wins(board, scores, w)
    if win_menge:
        return random.choice(win_menge)
    legal = list(board.legal_moves())
    if cutoff is None:
        cutoff = 99
    if cutoff <= 0:
        # Patzer ohne Filter (Stufen 1-4, s=0): uniform aus allen legalen.
        return random.choice(legal)
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
            ml = bb.BitBully.score_to_moves_left(s, board)
        except Exception:
            ok.append(c)
            continue
        if ml <= limit:
            continue
        ok.append(c)
    if ok:
        return random.choice(ok)
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


def pick_move(board, key):
    """GUI: ConnectFourStudio.pick_engine_move (Stand 03.10.2026, ohne GUI/Threads)."""
    agent = get_agent()
    _label, p, s, w = STUFEN[key]
    agent.reset_node_counter()
    agent.reset_transposition_table()
    scores = {}
    for depth in DEPTHS:
        try:
            part = agent.score_all_moves(board, max_depth=depth)
        except Exception:
            break
        scores = dict(part)
        if depth == -1:
            break
    if not scores:
        agent.reset_node_counter()
        scores = dict(agent.score_all_moves(board, max_depth=4))
    if not scores:
        raise ValueError("kein legaler Zug")
    if key == "verlierer":
        legal = list(board.legal_moves())
        verl = [c for c in legal
                if scores.get(c) is not None and scores.get(c) < 0]
        if verl:
            return random.choice(verl)
        rem = [c for c in legal
               if scores.get(c) is not None and scores.get(c) == 0]
        if rem:
            return random.choice(rem)
        return filtered_blunder(board, scores, 0, None)
    if key == "zufall":
        # GUI-exakt: durch _filtered_blunder(0, None) = echter Zufall aus
        # allen legalen (kein Remis-Zwang mehr seit 02.10.2026).
        return filtered_blunder(board, scores, 0, None)
    # Siegsschutz (Variante B): kurzer Gewinn geht IMMER vor.
    win_menge = short_wins(board, scores, w)
    if win_menge:
        return random.choice(win_menge)
    err = (100 - p) / 100.0
    if err > 0.0 and random.random() < err:
        return filtered_blunder(board, scores, s, w)
    best = max(scores.values())
    if best >= 0:
        # GUI-exakt (Fix 02.10.2026): schnellster Gewinn wird gespielt
        # (nicht gewuerfelt); Gleichstand im ml -> Zufall unter den
        # gleichschnellen. Liegt kein Gewinn innerhalb 10 Halbzuegen,
        # wird aus allen Gewinnzuegen gewuerfelt. Remis (best == 0):
        # Zufall unter allen Remis-Zuegen.
        cands = [c for c, v in scores.items() if v == best]
        try:
            _legal = set(board.legal_moves())
        except Exception:
            _legal = set(cands)
        cands = [c for c in cands if c in _legal] or list(_legal)
        pool = list(cands)
        if best > 0:
            try:
                _ml = {c: moves_left(board, scores.get(c)) for c in cands}
                _fast = [c for c in cands
                         if _ml.get(c) is not None and _ml.get(c) <= 10]
                if _fast:
                    _min = min(_ml[c] for c in _fast)
                    pool = [c for c in _fast if _ml[c] == _min]
            except Exception:
                pool = list(cands)
        return random.choice(pool)
    if key == "perfekt":
        # GUI-exakt (02.10.2026): Verluste mit ml <= 10 meiden (s=5);
        # alles schnell verloren -> laengster Widerstand; alle Verluste
        # weiter als 10 -> aus allen wuerfeln (Abwechslung).
        try:
            _all_ml = {c: moves_left(board, scores.get(c))
                       for c in board.legal_moves()
                       if scores.get(c) is not None}
        except Exception:
            _all_ml = {}
        if (_all_ml and all(ml is not None and ml > 10
                            for ml in _all_ml.values())):
            _pool = list(_all_ml)
            return random.choice(_pool)
        return filtered_blunder(board, scores, 5, None)
    dist = {}
    for col, s in scores.items():
        dist[col] = bb.BitBully.score_to_moves_left(s, board)
    if len(set(dist.values())) <= 1:
        try:
            exact = dict(agent.score_all_moves(board, max_depth=-1))
            if exact and max(exact.values()) < 0:
                for col, s in exact.items():
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
            return c
    return max(weights, key=weights.get)


def play_game(key_gelb, key_rot, seed):
    """Eine Partie. seed steuert den Zufall (reproduzierbar).
    Return: 1 (Gelb gewinnt), 2 (Rot gewinnt), 0 (Remis)."""
    random.seed(seed)
    get_agent()  # Instanz je Prozess
    board = bb.Board()
    while not board.is_game_over():
        n = len(board_to_moves(board))
        key = key_gelb if n % 2 == 0 else key_rot
        col = pick_move(board, key)
        board.play(col)
    return board.winner() or 0


def board_to_moves(board):
    # Steinzahl = Summe der Spaltenhöhen
    return [None] * sum(board.get_column_height(c) for c in range(7))


def play_match(args):
    """(keyA, keyB, n_spiele, wechsel, seed0) -> dict mit Zaehler aus A-Sicht."""
    keyA, keyB, n, wechsel, seed0 = args
    wA = wB = rem = 0
    for i in range(n):
        nr = i + 1
        gelb_beginnt = True if not wechsel else (nr % 2 == 1)
        key_gelb = keyA if gelb_beginnt else keyB
        key_rot = keyB if gelb_beginnt else keyA
        w = play_game(key_gelb, key_rot, seed0 + i)
        if w == 0:
            rem += 1
        elif w == 1:
            if gelb_beginnt:
                wA += 1
            else:
                wB += 1
        else:
            if gelb_beginnt:
                wB += 1
            else:
                wA += 1
    return {"A": keyA, "B": keyB, "wA": wA, "wB": wB, "rem": rem, "n": n,
            "wechsel": wechsel}


def elo(punkte, partien):
    if partien <= 0:
        return None
    p = punkte / partien
    if p <= 0.0:
        return -2000.0
    if p >= 1.0:
        return 2000.0
    import decimal as d
    raw = -400.0 * math.log10((1.0 - p) / p)
    return float(d.Decimal(str(raw)).quantize(d.Decimal("1"),
                                              rounding=d.ROUND_HALF_UP))


def fmt(res):
    A, B = res["A"], res["B"]
    la, lb = STUFEN[A][0], STUFEN[B][0]
    pa = res["wA"] + 0.5 * res["rem"]
    pb = res["wB"] + 0.5 * res["rem"]
    e = elo(pa, res["n"])
    et = "–" if e is None else f"{e:+.0f}"
    w = "an" if res["wechsel"] else "aus"
    return (f"Computer ({la}) - Computer ({lb}) = {pa:g}-{pb:g} "
            f"(+{res['wA']}/={res['rem']}/-{res['wB']})  Elo-Differenz = {et}\n"
            f"Partien: {res['n']}/{res['n']} (beendet), Farbwechsel: {w}")


if __name__ == "__main__":
    import json
    import time
    from concurrent.futures import ProcessPoolExecutor

    t0 = time.time()
    # Modus: "probe" (2 Partien zum Timing) oder Vollturnier via --jobs JSON
    if len(sys.argv) > 1 and sys.argv[1] == "probe":
        ka, kb = sys.argv[2], sys.argv[3]
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 2
        r = play_match((ka, kb, n, True, 12345))
        print(fmt(r))
        print(f"DAUER: {time.time()-t0:.1f}s fuer {n} Partien "
              f"(= {(time.time()-t0)/n:.1f}s/Partie, 1 Kern)")
    else:
        spec = json.loads(sys.argv[1])  # [{"A":..,"B":..,"n":..,"wechsel":..,"seed":..}, ...]
        jobs = [(j["A"], j["B"], j["n"], j["wechsel"], j.get("seed", 1000))
                for j in spec]
        import fcntl
        workers = min(len(jobs), int(sys.argv[2]) if len(sys.argv) > 2 else 5)
        # Stromausfall-sicher: Teilergebnis SOFORT in Datei (ungepuffert).
        # teil_log (optional, 3. Argument): jede fertige Partie wird als
        # JSON-Zeile angehaengt (fsync) -> nach Reboot auswertbar.
        teil_log = sys.argv[3] if len(sys.argv) > 3 else None
        tf = None
        if teil_log:
            tf = open(teil_log, "a", buffering=1)
        out = []
        with ProcessPoolExecutor(max_workers=workers) as ex:
            for r in ex.map(play_match, jobs):
                out.append(r)
                print(fmt(r), flush=True)
                print(f"  [nach {time.time()-t0:.0f}s]", flush=True)
                if tf is not None:
                    import json as _j
                    tf.write(_j.dumps(r) + "\n")
                    tf.flush()
                    try:
                        os.fsync(tf.fileno())
                    except Exception:
                        pass
        print(f"GESAMT: {time.time()-t0:.0f}s")
