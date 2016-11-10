from datetime import datetime
import requests
import time
import json

LICHESS_URL = 'https://en.lichess.org'
PAGE_SIZE = 2
NUM_PAGES = 2

def readable_date(unix_time_ms):
    return datetime.fromtimestamp(unix_time_ms/1000).strftime('%b %d %Y at %H:%M')

def get_games(username):
    games = []

    # TODO is it bad to use my own page enumeration despite the API having a 'nextPage'?
    for i in range(1, 1 + NUM_PAGES):
        # API seems to exclude aborted games
        response = requests.get('{}/api/user/{}/games'.format(LICHESS_URL, username),
                                params={'with_moves': 1,
                                        'nb': PAGE_SIZE,
                                        'page': i})
        assert response.status_code == 200, 'Response code was {}'.format(response.status_code)

        page = [g for g in response.json()['currentPageResults']]
        games.extend(page)
        print('Got {n} games from {latest} to {earliest}'
                .format(n = len(page),
                        latest = readable_date(page[0]['createdAt']),
                        earliest = readable_date(page[-1]['createdAt'])))

        if i != NUM_PAGES:
            time.sleep(1)

        if not response.json()['nextPage']:
            break

    return games

###############################################################################

username = 'thibault'
games = get_games(username)

print(json.dumps(games))
