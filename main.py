import requests
import datetime

API_URL = 'https://en.lichess.org/api'

def get_games(username):
    response = requests.get('{}/user/{}/games'.format(API_URL, username),
                            params={'with_moves': 1,
                                    'nb': 10})
    assert response.status_code == 200

    j = response.json()
    return j


STOCKFISH = '[Stockfish]'  # Invalid username, so this should be fine.

def readable(dt):
    return dt.strftime('%b %d %Y. %H:%M')

class Game:
    ALLOWED_ATTRS = ['id', 'speed', 'moves']

    def __init__(self, game_dict):
        self._game_dict = game_dict

    @property
    def white(self):
        # TODO: run through Stockfish as white codepath
        white_dict = self['players']['white']
        try:
            return white_dict['userId']
        except KeyError:
            return STOCKFISH

    @property
    def black(self):
        black_dict = self['players']['black']
        try:
            return black_dict['userId']
        except KeyError:
            return STOCKFISH

    @property
    def createdAt(self):
        return datetime.datetime.fromtimestamp(self['createdAt']/1000)

    def __getattr__(self, attr):
        if attr in Game.ALLOWED_ATTRS:
            return self[attr]
        else:
            raise AttributeError

    def __getitem__(self, key):
        return self._game_dict[key]

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
