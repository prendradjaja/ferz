import datetime
from constants import STOCKFISH

class Game:
    """
    Wrapper for the lichess API representation of one single game, extracted from the results of the
    following endpoint:

        /api/user/<USERNAME>/games
    """

    # These attributes can be used with dot notation, e.g. game.speed == game['speed']
    ALLOWED_ATTRS = ['id', 'speed', 'moves']

    def __init__(self, game_dict):
        """
        game_dict: lichess API representation of a single game, parsed from JSON into a Python dict
        """
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
