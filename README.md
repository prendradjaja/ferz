# Ferz and Wazir

## Setup

```
./make-venv.sh &&
. activate-venv &&
pip3 install -r requirements.txt
```

## Run

Activate the venv:

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

All of these are todos unless crossed out.

- ~~Bulk-downloads PGNs for a given user~~
- Filter by:
  - Recent (within the last X days)?
  - Chess games only
- Games labeled with which color the user was
- Games labeled with the following for further interactive filtering in Wazir:
  - Date
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

- color
- date
- time\_control
- rated
- human\_opponent
- move\_list
- game\_id

## Implementation todos

- ~~Pagination~~
- Determine if pagination breaks if new games are played. Possible consequences?
- Any bad behavior with 0-move games?
