# Elo measurements of the 14 levels (as of 2026-10-03, final ladder)

Engine vs. engine, 200 games per pairing with color swapping.
LS fit over 58 measurements (95/5 threshold), Random = 1000 as anchor.
Relative numbers, not FIDE Elo – they shift against human opponents.
NoRemis rule (forced draw removed 2026-10-02).

0 Loser is a fun level without rating and is not included.

## ELO-LS (Random = 1000 fixed)

Games = per level 13 opponents × 200 = 2600 (all 91 pairs played,
33 pairs outside 10..190 display only, not in fit).
Diff-1 = Elo difference to the direct predecessor from the LS fit
(smoothed level gaps from all measurements).

| Level            | (p,s,w)   | Elo  | Games | Diff-1 |
|------------------|-----------|------|-------|--------|
| 1 Random         | (0,0,0)   | 1000 | 2600  | --     |
| 2 Very Easy      | (25,0,0)  | 1204 | 2600  | +204   |
| 3 Easy           | (40,0,0)  | 1340 | 2600  | +136   |
| 4 Beginner       | (50,0,0)  | 1431 | 2600  | +91    |
| 5 Advanced       | (20,1,1)  | 1498 | 2600  | +67    |
| 6 Tactician      | (0,3,3)   | 1614 | 2600  | +116   |
| 7 Intermediate   | (50,1,1)  | 1702 | 2600  | +88    |
| 8 Demanding      | (55,1,1)  | 1752 | 2600  | +50    |
| 9 Hard           | (65,1,1)  | 1817 | 2600  | +65    |
| 10 Very Hard     | (70,2,2)  | 1929 | 2600  | +112   |
| 11 Expert        | (80,2,2)  | 2010 | 2600  | +81    |
| 12 Master        | (85,3,3)  | 2080 | 2600  | +70    |
| 13 Strong Master | (92,4,4)  | 2132 | 2600  | +52    |
| 14 Perfect       | (100,-,-) | 2174 | 2600  | +42    |

## CROSS TABLE (points of the ROW level vs. the COLUMN level, out of 200)

All 91 pairs with 200 games each (as of 2026-10-03, NoRemis, color swap on).
Full table: `elo_run/kreuztabelle_14final_95.txt` (threshold 95.0/5.0,
Fit = 58, SAT = 33 display only).

```
Row\Column          1      2      3      4      5      6      7      8      9     10     11     12     13     14
 1 Random          X   55.0   20.0   16.0    6.5    1.0    2.0    0.0    1.0    0.0    0.0    0.0    0.0    0.0
 2 Very Easy   145.0      X   69.5   51.0   35.5   10.5   10.5   10.0    6.5    4.0    0.5    1.5    0.0    0.0
 3 Easy        180.0  130.5      X   75.5   53.5   29.5   25.0   15.5   13.5    5.5    3.0    2.5    4.5    2.0
 4 Beginner    184.0  149.0  124.5      X   63.0   50.5   33.0   37.0   28.5    7.0    6.5    9.5    5.0    2.0
 5 Advanced    193.5  164.5  146.5  137.0      X   72.5   37.0   33.0   28.0    7.5   10.0    6.0    3.0    0.5
 6 Tactician   199.0  189.5  170.5  149.5  127.5      X   75.0   65.0   50.5   21.0   12.5    5.5    0.5    0.0
 7 Intermedia  198.0  189.5  175.0  167.0  163.0  125.0      X   85.0   70.5   49.5   29.0   21.0   10.5   11.0
 8 Demanding   200.0  190.0  184.5  163.0  167.0  135.0  115.0      X   80.0   52.5   39.5   23.5   22.0   22.0
 9 Hard        199.0  193.5  186.5  171.5  172.0  149.5  129.5  120.0      X   67.0   54.0   37.0   33.0   31.5
10 Very Hard   200.0  196.0  194.5  193.0  192.5  179.0  150.5  147.5  133.0      X   83.5   51.5   46.0   36.5
11 Expert      200.0  199.5  197.0  193.5  190.0  187.5  171.0  160.5  146.0  116.5      X   79.0   68.5   51.5
12 Master      200.0  198.5  197.5  190.5  194.0  194.5  179.0  176.5  163.0  148.5  121.0      X   85.0   62.0
13 Strong Ma   200.0  200.0  195.5  195.0  197.0  199.5  189.5  178.0  167.0  154.0  131.5  115.0      X   81.0
14 Perfect     200.0  200.0  198.0  198.0  199.5  200.0  189.0  178.0  168.5  163.5  148.5  138.0  119.0      X
```

## Methodology

- 200 games per pairing, color swap on (seeds 90000–162400).
- 95/5 threshold (CCRL/CEGT standard, truncation instead of capping):
  fit only over pairs with 10..190 points (58 measurements),
  33 pairs outside display only.
- LS fit: 1000/1204/1340/1431/1498/1614/1702/1752/1817/1929/2010/2080/2132/2174.
- History 2026-10-03: old 14-level ladder (68-fit) -> NoRemis re-measurement
  (probe12+rest72) -> screening of 24 candidates -> final 14-level ladder
  (Tactician new, Expert (80,2,2), Intermediate (50,1,1), Ansteiger removed,
  World Class renamed to Strong Master).
- Fit script: `elo_run/make_neu.py`, threshold comparison:
  `elo_run/kreuz14final/schwelle_*.txt` (+ `UEBERSICHT*.txt`).
- Raw data: `elo_run/log/probe12_*.jsonl`, `rest72_*.jsonl`,
  `testkand_*.jsonl`, `taktc_*.jsonl`, `final56_*.jsonl`,
  `screen24_*.jsonl`, `gap9_*.jsonl`, `gap9b_*.jsonl`.
