import commands

import re


# TODO
# - do i want to attach raw command text?

_REGEX_UP   = re.compile('-+')
_REGEX_DAYS = re.compile('(\d+)d')
_REGEX_MONTHS = re.compile('(\d+)m')
_REGEX_YEARS = re.compile('(\d+)y')
_REGEX_TIME_CONTROL = re.compile('(\d+)t')


def parse(cmd):
    if cmd == '':
        return commands.Repeat()

    elif len(cmd) == 1 and cmd.isdigit():
        rank = int(cmd)
        return commands.Frequent(rank)

    elif cmd == 'h':
        return commands.Human()

    elif cmd == 'r':
        return commands.Rated()

    elif cmd == '/':
        return commands.Root()

    elif cmd == '?':
        return commands.Help()

    elif _REGEX_UP.fullmatch(cmd):
        return commands.Up(len(cmd))

    elif _REGEX_DAYS.fullmatch(cmd):
        # TODO is there a good way to avoid duplicating the .fullmatch() call?
        days_str = _REGEX_DAYS.fullmatch(cmd).group(1)
        days = int(days_str)
        return commands.Days(days)

    elif _REGEX_MONTHS.fullmatch(cmd):
        months_str = _REGEX_MONTHS.fullmatch(cmd).group(1)
        months = int(months_str)
        return commands.Months(months)

    elif _REGEX_YEARS.fullmatch(cmd):
        years_str = _REGEX_YEARS.fullmatch(cmd).group(1)
        years = int(years_str)
        return commands.Years(years)

    elif _REGEX_TIME_CONTROL.fullmatch(cmd):
        minutes_str = _REGEX_TIME_CONTROL.fullmatch(cmd).group(1)
        minutes = int(minutes_str)
        return commands.TimeControl(minutes)

    else:  # TODO maybe want a regex for moves?
        return commands.Move(cmd)
