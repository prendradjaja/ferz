import datetime


class Filter:
    def apply(self, games):
        raise Exception('not implemented')


class AllFilter(Filter):
    def apply(self, games):
        return games

    # TODO is this actually needed?
    def __bool__(self):
        return False


class DateFilter(Filter):
    def __init__(self, days):
        self.days = days

    def apply(self, games):
        recent = (lambda g:
                  datetime.timedelta(self.days)
                  >= datetime.datetime.now() - g.createdAt)
        return list(filter(recent, games))
