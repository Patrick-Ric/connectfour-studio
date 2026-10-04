# Elo-Messungen der 14 Spielstufen (Stand 03.10.2026, finale Leiter)

Engine-gegen-Engine, je Paarung 200 Partien mit Farbwechsel.
LS-Fit über 58 Messungen (95/5-Schwelle), Zufall = 1000 als Anker.
Relativ, kein FIDE-Elo – gegen Menschen verschiebt sich das.
NoRemis-Regel (Pflicht-Remis gestrichen 02.10.2026).

0 Verlierer ist eine Spaß-Stufe ohne Wertung und nicht enthalten.

## ELO-LS (Zufall = 1000 fix)

Part. = je Stufe 13 Gegner × 200 = 2600 (alle 91 Paare gespielt,
33 Paare außerhalb 10..190 nur Anzeige, nicht Fit).
Diff-1 = Elo-Differenz zum direkten Vorgänger aus dem LS-Fit
(geglättete Stufenabstände aus allen Messungen).

| Stufe            | (p,s,w)   | Elo  | Part. | Diff-1 |
|------------------|-----------|------|-------|--------|
| 1 Zufall         | (0,0,0)   | 1000 | 2600  | --     |
| 2 Sehr Leicht    | (25,0,0)  | 1204 | 2600  | +204   |
| 3 Leicht         | (40,0,0)  | 1340 | 2600  | +136   |
| 4 Anfänger       | (50,0,0)  | 1431 | 2600  | +91    |
| 5 Fortgeschritten| (20,1,1)  | 1498 | 2600  | +67    |
| 6 Taktiker       | (0,3,3)   | 1614 | 2600  | +116   |
| 7 Mittel         | (50,1,1)  | 1702 | 2600  | +88    |
| 8 Fordernd       | (55,1,1)  | 1752 | 2600  | +50    |
| 9 Schwer         | (65,1,1)  | 1817 | 2600  | +65    |
| 10 Sehr Schwer   | (70,2,2)  | 1929 | 2600  | +112   |
| 11 Experte       | (80,2,2)  | 2010 | 2600  | +81    |
| 12 Meister       | (85,3,3)  | 2080 | 2600  | +70    |
| 13 Starker Meister| (92,4,4) | 2132 | 2600  | +52    |
| 14 Perfekt       | (100,-,-) | 2174 | 2600  | +42    |

## KREUZTABELLE (Punkte der ZEILEN-Stufe gegen die SPALTEN-Stufe, aus 200)

Alle 91 Paare je 200 (Stand 03.10.2026, NoRemis, Farbwechsel an).
Volltabelle: `elo_run/kreuztabelle_14final_95.txt` (Schwelle 95.0/5.0,
Fit = 58, SAT = 33 nur Anzeige).

```
Zeile\Spalte        1      2      3      4      5      6      7      8      9     10     11     12     13     14
 1 Zufall          X   55.0   20.0   16.0    6.5    1.0    2.0    0.0    1.0    0.0    0.0    0.0    0.0    0.0
 2 Sehr Leich  145.0      X   69.5   51.0   35.5   10.5   10.5   10.0    6.5    4.0    0.5    1.5    0.0    0.0
 3 Leicht      180.0  130.5      X   75.5   53.5   29.5   25.0   15.5   13.5    5.5    3.0    2.5    4.5    2.0
 4 Anfaenger   184.0  149.0  124.5      X   63.0   50.5   33.0   37.0   28.5    7.0    6.5    9.5    5.0    2.0
 5 Fortgeschr  193.5  164.5  146.5  137.0      X   72.5   37.0   33.0   28.0    7.5   10.0    6.0    3.0    0.5
 6 Taktiker    199.0  189.5  170.5  149.5  127.5      X   75.0   65.0   50.5   21.0   12.5    5.5    0.5    0.0
 7 Mittel      198.0  189.5  175.0  167.0  163.0  125.0      X   85.0   70.5   49.5   29.0   21.0   10.5   11.0
 8 Fordernd    200.0  190.0  184.5  163.0  167.0  135.0  115.0      X   80.0   52.5   39.5   23.5   22.0   22.0
 9 Schwer      199.0  193.5  186.5  171.5  172.0  149.5  129.5  120.0      X   67.0   54.0   37.0   33.0   31.5
10 Sehr Schwe  200.0  196.0  194.5  193.0  192.5  179.0  150.5  147.5  133.0      X   83.5   51.5   46.0   36.5
11 Experte     200.0  199.5  197.0  193.5  190.0  187.5  171.0  160.5  146.0  116.5      X   79.0   68.5   51.5
12 Meister     200.0  198.5  197.5  190.5  194.0  194.5  179.0  176.5  163.0  148.5  121.0      X   85.0   62.0
13 Starker Me  200.0  200.0  195.5  195.0  197.0  199.5  189.5  178.0  167.0  154.0  131.5  115.0      X   81.0
14 Perfekt     200.0  200.0  198.0  198.0  199.5  200.0  189.0  178.0  168.5  163.5  148.5  138.0  119.0      X
```

## Methodik

- Je Paarung 200 Partien, Farbwechsel an (Seeds 90000-162400).
- 95/5-Schwelle (CCRL/CEGT-üblich, Truncation statt Capping):
  Fit nur über Paare mit 10..190 Punkten (58 Messungen),
  33 Paare außerhalb nur Anzeige.
- LS-Fit: 1000/1204/1340/1431/1498/1614/1702/1752/1817/1929/2010/2080/2132/2174.
- History 03.10.2026: alte 14er-Leiter (68er-Fit) -> NoRemis-Neumessung
  (probe12+rest72) -> Screening 24 Kandidaten -> finale 14er-Leiter
  (Taktiker neu, Experte (80,2,2), Mittel (50,1,1), Ansteiger gestrichen,
  Weltklasse heisst Starker Meister).
- Fit-Skript: `elo_run/make_neu.py`, Schwellenvergleich:
  `elo_run/kreuz14final/schwelle_*.txt` (+ `UEBERSICHT*.txt`).
- Rohdaten: `elo_run/log/probe12_*.jsonl`, `rest72_*.jsonl`,
  `testkand_*.jsonl`, `taktc_*.jsonl`, `final56_*.jsonl`,
  `screen24_*.jsonl`, `gap9_*.jsonl`, `gap9b_*.jsonl`.
