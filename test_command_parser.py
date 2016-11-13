from command_parser import parse
import commands
import pytest


@pytest.mark.parametrize('input,expected', [
    ('', commands.Frequent(0)),
    ('0', commands.Frequent(0)),
    ('1', commands.Frequent(1)),
    ('5', commands.Frequent(5)),
    ('9', commands.Frequent(9)),
    # but not multiple digits

    ('h', commands.Human()),
    ('r', commands.Rated()),
    ('/', commands.Root()),

    ('-', commands.Up(1)),
    ('--', commands.Up(2)),
    ('-----', commands.Up(5)),

    ('2t', commands.TimeControl(2)),
    ('20t', commands.TimeControl(20)),
    # but not 't' itself

    ('3d', commands.Days(3)),
    ('21d', commands.Days(21)),
    # but not 'd' itself
    ('7m', commands.Months(7)),
    ('77777m', commands.Months(77777)),
    ('2y', commands.Years(2)),
    ('100y', commands.Years(100)),

    # actual algebraic moves
    ('e4', commands.Move('e4')),
    ('g6', commands.Move('g6')),
    ('Nf3', commands.Move('Nf3')),
    ('O-O', commands.Move('O-O')),
    ('O-O-O', commands.Move('O-O-O')),
    ('O-O#', commands.Move('O-O#')),
    ('Bg8+', commands.Move('Bg8+')),
    # and many more...

    # things that aren't actually algebraic moves but aren't valid commands
    # (currently we just parse all of these as algebraic moves)
    ('t', commands.Move('t')),
    ('d', commands.Move('d')),
    ('m', commands.Move('m')),
    ('y', commands.Move('y')),
    ('13', commands.Move('13')),
    ('1000', commands.Move('1000')),
])
def test_parse(input, expected):
    assert parse(input) == expected
