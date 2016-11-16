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
    #   cmd.type == 'Up'
    # or
    #   cmd.type == Up.name  # need to implement .name
    # instead of
    #   Up.isinstance(cmd)
    def _isinstance(obj):
        return obj.type == name

    def make_obj(*args):
        return _Command(name, CommandType(*args))
    make_obj.isinstance = _isinstance

    return make_obj

### Public

# TODO Can I do any type checking?
# TODO documentation

Repeat = _command_type('Repeat', '')
NoOp = _command_type('NoOp', '')

Help = _command_type('Help', '')

# navigating the tree
Up = _command_type('Up', 'distance')
Move = _command_type('Move', 'move')
Frequent = _command_type('Frequent', 'rank')  # rank starts at 0
Root = _command_type('Root', '')

# filtering
Days = _command_type('Days', 'days')
Months = _command_type('Months', 'months')
Human = _command_type('Human', '')
Rated = _command_type('Rated', '')
TimeControl = _command_type('TimeControl', 'minutes')
