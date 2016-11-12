# Ferz and Wazir

## Setup

```
./make-venv.sh &&
. activate-venv &&
pip3 install -r requirements.txt
```

## Run

Activate the venv if you haven't already:

```
. activate-venv
```

Download a user's games with Ferz:

```
python3 ferz.py prendradjaja -o prendradjaja.json
```

Explore their openings with Wazir:

```
python3 wazir.py prendradjaja.json
```

## Features

    x Bulk-download PGNs for a given user
    _ Download in human-readable format
    _ Filter by:
      x Date
      x Chess games only
        _ Configurable
      _ Time control
      _ Rated?
      _ Human opponent?
    _ Games labeled with which color the user was
    _ Might also want to have some features for figuring out what X ("last X days") should be.
      _ Activity graph? (Histogram of games by date)

    - Interactively explore a game database by walking up and down the "game tree."
      x Basic "walking"
      - At any node, show:
        x Responses (with percentages and counts)
        x Which player is to move
        x Links to games

## Implementation todos

    x Pagination
    _ Determine if pagination breaks if new games are played. Possible consequences?
    _ Any bad behavior with 0-move games?
