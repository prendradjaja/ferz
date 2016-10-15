import datetime

from constants import STOCKFISH
from utils import readable

class Game:
    """
    Wrapper for the lichess API representation of one single game, extracted from the results of the
    following endpoint:

        /api/user/<USERNAME>/games
    """

    # These attributes can be used with dot notation, e.g. game.speed == game['speed']
    ALLOWED_ATTRS = ['id', 'speed']

    def __init__(self, game_dict):
        """
        game_dict: lichess API representation of a single game, parsed from JSON into a Python dict
        """
        self._game_dict = game_dict

    def __str__(self):
        return '{}. {} vs {}. {} -- {}'.format(self.id, self.white, self.black, readable(self.createdAt), self.moves[:10])

    def is_white(self, username):
        return self.white == username

    def is_black(self, username):
        return not self.is_white(username)

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

    @property
    def moves(self):
        # TODO create unit tests for these test cases:
        #
        # cases = [
        #     {'moves': 'e4'},
        #     {'moves': 'e4 d5'},
        #     {'moves': 'e4 d5 exd5'},
        #     {'moves': 'e4 d5 exd5 Qxd5'},
        #     {'moves': 'e4 d5 exd5 Qxd5 Nc3'},
        # ]
        moves = self['moves'].split(' ')

        result = []
        for n, i in enumerate(range(0, len(moves), 2), start=1):
            result.append('{}.'.format(n))
            result.append(moves[i])
            try:
                result.append(moves[i + 1])
            except IndexError:
                pass

        return ' '.join(result)

    @property
    def raw_moves(self):
        return self['moves']

    def __getattr__(self, attr):
        """
        Implement dot notation.
        """
        if attr in Game.ALLOWED_ATTRS:
            return self[attr]
        else:
            raise AttributeError

    def __getitem__(self, key):
        """
        Allow indexing to call through to the internal game dict.
        """
        return self._game_dict[key]
