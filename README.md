# ConnectFour Studio

![ConnectFour Studio](screenshot-1.png)

A free, offline desktop program for Connect Four — play against the computer,
analyze positions, and run engine-vs-engine matches.

- **Engine:** BitBully by Markus Thill (Python module `bitbully`, C++ core)
- **GUI:** Python + Tkinter (+ Pillow)
- **License:** GNU AGPL v3 — source code freely available

## Features

- 14 computer levels (1 Zufall … 14 Perfekt) + 0 Loser joke level + 2 custom user levels with own (p, s, w)
- Live evaluation: winner + stones to the end, nodes, time, book/computed source
- Modes: Human-Computer, 2 players, Computer-Computer playout, Computer-Computer match
- 20 stone sets (mouse wheel / PageUp-PageDown to browse)
- Session score vs. the engine, quicksave, random positions, help in 6 languages (German, English, French, Spanish, Dutch, Italian)

## Install & Start

```bash
python3 -m venv .venv
.venv/bin/pip install bitbully bitbully-databases pillow
.venv/bin/python connectfour_studio.py
```

Requirements: Python 3.10+, Tkinter 8.6+ (usually included with Python).

## Keyboard

- `1-7` play column, `Arrow Left/Right` undo/redo, `Arrow Up/Down` first/last move
- `PageUp/PageDown` or mouse wheel over the board browse stone sets
- `F1` help, `F3/F4` quick save/load, `F5` engine move, `F6` evaluate all moves, `F7` permanent analysis

## Project layout

- `connectfour_studio.py` — main window, board, menus, threads
- `cfs_help.py` — help + info dialogs (`HELP_CONTENT`, DE/EN/FR/ES/NL/IT)
- `cfs_sets.py` — stone sets (`data/images/set1..set20`)
- `cfs_levels.py` — levels, match, score, random dialog
- `cfs_lang.py` — UI strings (`STRINGS`, DE/EN/FR/ES/NL/IT)

## Credits

- Engine: **BitBully by Markus Thill** — https://markusthill.github.io/projects/0_bitbully/
- Opening book: `bitbully-databases` (`12-ply-dist`)
