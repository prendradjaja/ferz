import collections

### Private

_Command = collections.namedtuple('Command', 'type data')

# TODO Would using inheritance be cleaner?
# TODO How can I avoid using cmd.data.field and just use cmd.field?
# TODO Any way to "hide" the type field? Ideally it should only be used by
# isinstance... unfortunately namedtuple doesn't allow underscored names

def _command_type(name, fields):
    CommandType = collections.namedtuple(name, fields)

    # TODO isinstance feels hacky. maybe better to just use
    #   cmd.type == 'UpCommand'
    # or
    #   cmd.type == UpCommand.name  # need to implement .name
    # instead of
    #   UpCommand.isinstance(cmd)
    def _isinstance(obj):
        return obj.type == name

    def make_obj(*args):
        return _Command(name, CommandType(*args))
    make_obj.isinstance = _isinstance

    return make_obj

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
TimeControlCommand = _command_type('TimeControlCommand', 'minutes')
