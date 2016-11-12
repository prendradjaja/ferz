import commands


class TestCommandAccessors:

    def test_type_name(self):
        thing = commands.MoveCommand('e4')
        assert thing.type == 'MoveCommand'

    def test_move(self):
        thing = commands.MoveCommand('e4')
        assert thing.data.move == 'e4'

    def test_days(self):
        thing = commands.DaysCommand(3)
        assert thing.data.days == 3


class TestCommandEquality:

    def test_same_type_same_contents(self):
        thing = commands.MoveCommand('e4')
        other = commands.MoveCommand('e4')
        assert thing == other

    def test_same_type_different_contents(self):
        thing = commands.MoveCommand('e4')
        other = commands.MoveCommand('d4')
        assert thing != other

    def test_different_type(self):
        thing = commands.MoveCommand('e4')

        # TODO e4 is not a number
        other = commands.DaysCommand('e4')
        assert thing != other
