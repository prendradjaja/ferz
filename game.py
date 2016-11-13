import datetime

from constants import STOCKFISH, WHITE, BLACK
from utils import readable

class Game:
    """
    Wrapper for the lichess API representation of one single game, extracted from the results of the
    following endpoint:

        /api/user/<USERNAME>/games
    """

    # These attributes can be used with dot notation, e.g. game.speed == game['speed']
    ALLOWED_ATTRS = ['id', 'speed', 'rated', 'variant']

    def __init__(self, game_dict):
        """
        game_dict: lichess API representation of a single game, parsed from JSON into a Python dict
        """
        self._game_dict = game_dict

    def __str__(self):
        return (

            # id
            '{}. '.format(self.id) +

            # black
            'vs {}. '.format(self.black[:8]) +
            '\t' +

            # date
            readable(self.createdAt) +
            ' ' +

            # moves
            '-- ' +
            str(self.moves[:4]) +

        '')

    @property
    def time(self):
        """
        (in minutes) initial time + 40sec * increment

        I think this is equal to self['clock']['totalTime'] / 60, but lichess
        API documentation suggests that the multiplier is 30, not 40. Not sure
        if that's a bug, so I'll just reimplement the totalTime calculation
        here.
        """
        return ((self['clock']['initial'] + 40 * self['clock']['increment'])
                / 60)

    def color(self, username):
        return WHITE if self.is_white(username) else BLACK

    def is_white(self, username):
        return self.white.lower() == username.lower()

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

    # TODO capitalization
    @property
    def createdAt(self):
        return datetime.datetime.fromtimestamp(self['createdAt']/1000)

    @property
    def moves(self):
        return self['moves'].split()

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
