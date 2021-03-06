from command_parser import parse
import commands
import pytest


@pytest.mark.parametrize('input,expected', [
    ('', commands.Repeat()),

    ('0', commands.Frequent(0)),
    ('1', commands.Frequent(1)),
    ('5', commands.Frequent(5)),
    ('9', commands.Frequent(9)),
    # but not multiple digits

    ('h', commands.Human()),
    ('r', commands.Rated()),
    ('/', commands.Root()),
    ('?', commands.Help()),
    ('??', commands.MoreHelp()),

    ('-', commands.Up(1)),
    ('--', commands.Up(2)),
    ('-----', commands.Up(5)),

    ('t', commands.HelpTopic('t')),
    ('2t', commands.TimeControl(2)),
    ('20t', commands.TimeControl(20)),

    ('d', commands.HelpTopic('d')),
    ('m', commands.HelpTopic('m')),
    ('3d', commands.Days(3)),
    ('21d', commands.Days(21)),
    ('7m', commands.Months(7)),
    ('77777m', commands.Months(77777)),

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
    ('13', commands.Move('13')),
    ('1000', commands.Move('1000')),
])
def test_parse(input, expected):
    assert parse(input) == expected
