from utils import prettify_moves
import pytest


@pytest.mark.parametrize('input,expected', [
    (['e4'],                          '1.e4'),
    (['e4','d5'],                     '1.e4 d5'),
    (['e4','d5','exd5'],              '1.e4 d5 2.exd5'),
    (['e4','d5','exd5','Qxd5'],       '1.e4 d5 2.exd5 Qxd5'),
    (['e4','d5','exd5','Qxd5','Nc3'], '1.e4 d5 2.exd5 Qxd5 3.Nc3'),
])
def test_prettify_moves(input, expected):
    assert prettify_moves(input) == expected
