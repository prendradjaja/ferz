# Ferz

## Setup

```
./make-venv.sh &&
. activate-venv &&
pip3 install -r requirements.txt
```

## Run

```
. activate-venv &&
python3 main.py
```

## Overview:

This tool:

(all of this is todos unless crossed out)

- ~~gets games~~
- that are:
  - recent (within the last X days)
  - chess games
- bucketed into time controls
- bucketed into color
- labeled with the following for further filtering:
  - rated?
  - against human opponent?
- and also with these additional properties:
  - move list
  - game id
- Might also want to have some features for figuring out what X ("last X days") should be.
- "Download manager" behavior: continue partial download
- Dump raw API data

That is, it returns a list of games, with the following properties:

- rated
- human_opponent
- recent
- move_list
- game_id

All this stuff is to be consumed by another program, Wazir, which will be able to:

- filter by:
  - recency
  - whether or not the game was rated
  - whether or not the opponent was human
- given a game-prefix, show:
  - number of games
  - responses (with percentages and counts)
  - link to games

## Other to-do:

- ~~Pagination~~
- Determine if pagination breaks if new games are played. Possible consequences?
- Any bad behavior with 0-move games?
