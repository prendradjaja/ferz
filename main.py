import requests
import time

from game import Game
from utils import readable

LICHESS_URL = 'https://en.lichess.org'
PAGE_SIZE = 10
NUM_PAGES = 1

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

        page = [Game(g) for g in response.json()['currentPageResults']]
        games.extend(page)
        print('Got {n} games from {latest} to {earliest}'
                .format(n = len(page),
                        latest = readable(page[0].createdAt),
                        earliest = readable(page[-1].createdAt)))

        if i != NUM_PAGES:
            time.sleep(1)

        if not response.json()['nextPage']:
            break

    return games

###############################################################################

username = 'thibault'
games = get_games(username)

for g in games:
    s = ''

    # id
    s += '{}. '.format(g.id)

    # username
    s += '{} vs {}. '.format(g.white, g.black).ljust(35)

    # speed
    s += '{}. '.format(g.speed).ljust(20)

    # createdAt
    s += '{}. '.format(readable(g.createdAt))

    # moves
    s += ' --  {} ...'.format(g.moves[:20])

    print(s)
