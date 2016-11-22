import datetime

from game import Game
from typing import List


# TODO how do i make sure you actually subclass Filter?
# TODO maybe rename to _Filter?
class Filter:
    def apply(self, games: List[Game]) -> List[Game]:
        raise Exception('not implemented')


class All(Filter):
    def apply(self, games: List[Game]) -> List[Game]:
        return games

    def __bool__(self):
        return False

    def __repr__(self):
        return 'AllFilter()'


class Date(Filter):
    def __init__(self, days: int) -> None:
        self.days = days

    def apply(self, games: List[Game]) -> List[Game]:
        recent = (lambda g:
                  datetime.timedelta(self.days)
                  >= datetime.datetime.now() - g.createdAt)
        return list(filter(recent, games))

    def __str__(self):
        return 'Last {} days'.format(self.days)

    def __repr__(self):
        return 'DateFilter({})'.format(self.days)


# TODO "less than" -- this only does "greater than"
class TimeControl(Filter):
    def __init__(self, minutes: int) -> None:
        self.minutes = minutes

    def apply(self, games: List[Game]) -> List[Game]:
        # + 0.0001 because floating point.
        return list(filter(lambda g: g.time + 0.0001 >= self.minutes,
                           games))

    def __repr__(self):
        return 'TimeControlFilter({})'.format(self.minutes)


class Rated(Filter):
    def apply(self, games: List[Game]) -> List[Game]:
        return list(filter(lambda g: g.rated, games))

    def __str__(self):
        return 'Only rated games'

    def __repr__(self):
        return 'RatedFilter()'
