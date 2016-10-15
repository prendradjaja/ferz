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

## Goal:

This tool:

- [x] gets games
- that are:
  - [ ] recent (within the last X days)
  - [ ] chess games
- [ ] bucketed into time controls
- [ ] bucketed into color
- labeled with the following for further filtering:
  - [ ] rated?
  - [ ] against human opponent?
- and also with these additional properties:
  - [ ] move list
  - [ ] game id
- [ ] Might also want to have some features for figuring out what X ("last X days") should be.
- [ ] "Download manager" behavior: continue partial download
- [ ] Dump raw API data

That is, it returns a list of games, with the following properties:

- rated
- human_opponent
- recent
- move_list
- game_id

To be used in another tool:

- filter by:
  - recency
  - whether or not the game was rated
  - whether or not the opponent was human
- given a game-prefix, show:
  - number of games
  - responses (with percentages and counts)
  - link to games

The terminal version of this tool should support these commands:

    (algebraic move) = go down
    (nothing)        = go down to most common move
    0                = go down to most common move
    1                = go down to most second common move
    .                = go up one
    ...              = go up three
    /                = go to root
    h                = toggle human
    r                = toggle rated
    3d               = recency filter at 3 days
    7m
    2y
    g                = show games (paginated)
    n                = next page of games
    4n

## Other to-do:

- [ ] Determine if pagination breaks if new games are played. Possible consequences?
- [ ] Any bad behavior with 0-move games?
