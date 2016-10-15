# Ferz

## Setup

```
./make-venv.sh &&
. activate-venv &&
pip3 install -r requirements.txt
```

## Run

Make sure you've got the venv activated! Then run:

```
python3 main.py
```

## Features and purpose

All of these are todos unless crossed out.

- ~~Bulk-downloads PGNs for a given user~~
- Filter by:
  - Recent (within the last X days)?
  - Chess games only
- Games labeled with which color the user was
- Games labeled with the following for further filtering:
  - Time control
  - Rated?
  - Human opponent?
- Games also have these properties:
  - move list
  - game id
- Might also want to have some features for figuring out what X ("last X days") should be.
- "Download manager" behavior? (continue partial download)
- Dump raw API data

That is, it returns a list of games, with the following properties:

- rated
- human\_opponent
- recent
- move\_list
- game\_id

All this stuff is to be consumed by another program, Wazir, whose purpose is to
explore a player's opening tree and games.

## Implementation todos

- ~~Pagination~~
- Determine if pagination breaks if new games are played. Possible consequences?
- Any bad behavior with 0-move games?
