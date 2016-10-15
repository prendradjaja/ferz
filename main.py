import requests

from game import Game
from utils import readable

API_URL = 'https://en.lichess.org/api'

def get_games(username):
    response = requests.get('{}/user/{}/games'.format(API_URL, username),
                            params={'with_moves': 1,
                                    'nb': 10})
    assert response.status_code == 200

    j = response.json()
    return j

###############################################################################

username = 'thibault'
games = [Game(each) for each in get_games(username)['currentPageResults']]

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
