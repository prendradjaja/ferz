from command_parser import parse
from commands import (DaysCommand, FrequentCommand, HumanCommand,
        MonthsCommand, MoveCommand, RatedCommand, RootCommand,
        TimeControlCommand, UpCommand, YearsCommand)
import pytest


@pytest.mark.parametrize('input,expected', [
    ('', FrequentCommand(0)),
    ('0', FrequentCommand(0)),
    ('1', FrequentCommand(1)),
    ('5', FrequentCommand(5)),
    ('9', FrequentCommand(9)),
    # but not multiple digits

    ('h', HumanCommand()),
    ('r', RatedCommand()),
    ('/', RootCommand()),

    ('-', UpCommand(1)),
    ('--', UpCommand(2)),
    ('-----', UpCommand(5)),

    ('2t', TimeControlCommand(2)),
    ('20t', TimeControlCommand(20)),

    ('3d', DaysCommand(3)),
    ('21d', DaysCommand(21)),
    # but not 'd' itself
    ('7m', MonthsCommand(7)),
    ('77777m', MonthsCommand(77777)),
    ('2y', YearsCommand(2)),
    ('100y', YearsCommand(100)),

    # actual algebraic moves
    ('e4', MoveCommand('e4')),
    ('g6', MoveCommand('g6')),
    ('Nf3', MoveCommand('Nf3')),
    ('O-O', MoveCommand('O-O')),
    ('O-O-O', MoveCommand('O-O-O')),
    ('O-O#', MoveCommand('O-O#')),
    ('Bg8+', MoveCommand('Bg8+')),
    # and many more...

    # things that aren't actually algebraic moves but aren't valid commands
    # (currently we just parse all of these as algebraic moves)
    ('d', MoveCommand('d')),
    ('m', MoveCommand('m')),
    ('y', MoveCommand('y')),
    ('13', MoveCommand('13')),
    ('1000', MoveCommand('1000')),
])
def test_parse(input, expected):
    assert parse(input) == expected
