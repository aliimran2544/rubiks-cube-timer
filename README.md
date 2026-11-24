# Rubik's Cube Timer

A desktop speedcubing timer built with Python and tkinter. Time 5 solves and it calculates the stats speedcubers actually use.

<!-- Add a screenshot here -->
<!-- ![Screenshot](screenshot.png) -->

## Features

- Live timer in `MM:SS.hh` format
- Turns **green** if the solve beat your previous one, **red** if it was slower
- Table of all 5 solve times
- Statistics after 5 solves:
  - **Best single** solve
  - **Mean of 3 (MO3)** for solves 1–3, 2–4 and 3–5, plus the best MO3
  - **Average of 5 (AO5)** using the official WCA method: drop the best and worst solve, then average the middle 3
- **Reset** to start a new session

## How to run

Requires Python 3 (tkinter comes with most Python installs).

```
python3 rubiks_cube_timer.py
```

## Ideas for future improvements

- Start and stop with the spacebar, like real cube timers
- Generate a random scramble for each solve
- Save sessions to a file to track progress over time

## Author

**Ali Imran**, CS & Math student at the University of Toronto Scarborough
