import commands


class TestAccessors:

    def test_move(self):
        thing = commands.Move('e4')
        assert thing.data.move == 'e4'

    def test_days(self):
        thing = commands.Days(3)
        assert thing.data.days == 3


class TestIsInstance:

    def test_true(self):
        thing = commands.Move('e4')
        assert commands.Move.isinstance(thing)

    def test_false(self):
        thing = commands.Move('e4')
        assert not commands.Days.isinstance(thing)



class TestEquality:

    def test_same_type_same_contents(self):
        thing = commands.Move('e4')
        other = commands.Move('e4')
        assert thing == other

    def test_same_type_different_contents(self):
        thing = commands.Move('e4')
        other = commands.Move('d4')
        assert thing != other

    def test_different_type(self):
        thing = commands.Move('e4')

        # TODO e4 is not a number
        other = commands.Days('e4')
        assert thing != other
