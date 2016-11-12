import collections

### Private

_Command = collections.namedtuple('Command', 'type data')

# TODO Would using inheritance be cleaner?
def _command_type(name, fields):
    CommandType = collections.namedtuple(name, fields)
    return lambda *args: _Command(name, CommandType(*args))

### Public

# TODO Can I do any type checking?

# navigating the tree
UpCommand = _command_type('UpCommand', 'distance')
MoveCommand = _command_type('MoveCommand', 'move')
FrequentCommand = _command_type('FrequentCommand', 'rank')  # rank starts at 0
RootCommand = _command_type('RootCommand', '')

# filtering
DaysCommand = _command_type('DaysCommand', 'days')
MonthsCommand = _command_type('MonthsCommand', 'months')
YearsCommand = _command_type('YearsCommand', 'years')
HumanCommand = _command_type('HumanCommand', '')
RatedCommand = _command_type('RatedCommand', '')
