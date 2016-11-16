"""
Usage:
  python3    ./wazir.py DB_PATH
  python3 -i ./wazir.py DB_PATH debug
"""


from game import Game
import filters
from command_parser import parse
import commands
from table_display import format_table

import argparse
import json
import os
import sys


def usage():
    print(__doc__[1:][:-1])
    exit(1)


def main(filename):
    all_games = load_games(filename)

    main_loop(all_games)

    # debug code: comment out main_loop to use it
    f = filters.TimeControl(30)
    games = f.apply(all_games)
    print(len(games))
    for g in games:
        print(g)
    print(len(games))


def update_tree(all_games, using_filters, path):
    """
    Filter games, return:
        (node_or_none, num_games)

    A path is a list of moves e.g. ['e4', 'e5']
    """
    games = all_games
    for f in using_filters.values():
        games = f.apply(games)
    num_games = len(games)

    root = make_tree(games)
    node_or_none = find_node(root, path)
    return (node_or_none, num_games)


def find_node(node, path):
    """
    Returns node or none
    """
    for move in path:
        if not node.has_child(move):
            return None
        node = node.child(move)
    return node


def show():
    print(Store.next_message + '\n')

    subtree_size = Store.node.size if Store.node else 0

    header = ('D: {}'.format(len(Store.path)).ljust(7) +
              ' N: {} / {}'.format(subtree_size, Store.num_games) +
              '\n')
    print(header)

    if Store.node:
        Store.node.show()
    else:
        print('  No games found. Try changing filter settings or moving up the tree.')


class Store:
    """
    all state here.
    """

    def __init__(self):
        """
        poor man's singleton.

        maybe refactor to a better singleton later
        """
        raise Exception('do not initialize')

def main_loop(_all_games):
    # TODO there's gotta be a better name.

    Store.all_games = _all_games
    Store.using_filters = {
        filters.Date: filters.All(),
        filters.TimeControl: filters.All(),
        filters.Rated: filters.All(),
    }
    Store.path = []
    Store.node = None
    Store.num_games = None
    Store.next_message = ''

    os.system('clear')
    cmd = None
    while True:
        Store.node, Store.num_games = update_tree(Store.all_games,
                                                  Store.using_filters,
                                                  Store.path)
        show()
        Store.next_message = ''
        try:
            raw_cmd = input('\n> ')
        except (EOFError, KeyboardInterrupt):
            print()
            exit(1)
        os.system('clear')

        # TODO encapsulate state into one object, write eval()
        last_cmd = cmd
        cmd = parse(raw_cmd)

        if commands.Repeat.isinstance(cmd):
            if last_cmd:
                cmd = last_cmd
            else:
                Store.next_message = 'No last command'
                cmd = commands.NoOp()

        if commands.NoOp.isinstance(cmd):
            pass
        elif commands.Root.isinstance(cmd):
            Store.path = []
        elif commands.Up.isinstance(cmd):
            if Store.path == []:
                Store.next_message = 'Already at root'  # TODO better message?
            else:
                Store.path = Store.path[:-cmd.data.distance]
        elif commands.Frequent.isinstance(cmd):
            rank = cmd.data.rank
            try:
                move = Store.node.sorted_children[rank].move
                Store.path.append(move)
            except IndexError:
                Store.next_message = 'IndexError'  # TODO better message?
        elif commands.Days.isinstance(cmd):
            Store.using_filters[filters.Date] = filters.Date(cmd.data.days)
        elif commands.TimeControl.isinstance(cmd):
            Store.using_filters[filters.TimeControl] = \
                    filters.TimeControl(cmd.data.minutes)
        elif commands.Move.isinstance(cmd):
            Store.path.append(cmd.data.move)
        elif commands.Rated.isinstance(cmd):
            if Store.using_filters[filters.Rated]:
                Store.using_filters[filters.Rated] = filters.All()
            else:
                Store.using_filters[filters.Rated] = filters.Rated()
        else:
            Store.next_message = 'Command not implemented: ' + cmd.type


def load_games(filename):
    with open(filename) as f:
        games = [Game(g) for g in json.load(f)]

    # TODO maybe take some of this filtering out

    return [g for g in games if
            g.is_white('prendradjaja') and
            g.variant == 'standard']


def make_tree(games):
    root = Node(0)

    for g in games:
        node = root
        node.add_game(g)
        for move in g.moves:  # TODO should i implement `for move in g`?
            if node.has_child(move):
                node = node.child(move)
            else:
                node = node.add_child(move)
            node.add_game(g)

    return root

class Node:
    def __init__(self, depth, move=None, parent=None):
        self.move = move
        self.games = []
        self.children = []
        self.parent = parent
        self.depth = depth

    def __str__(self):
        return '<{}>'.format(self.move)

    def __repr__(self):
        return str(self)

    def has_child(self, move):
        return move in [child.move for child in self.children]

    def child(self, move):
        assert self.has_child(move)
        matches = [c for c in self.children if c.move == move]
        assert len(matches) == 1
        return matches[0]

    def add_child(self, move):
        assert not self.has_child(move)
        child = Node(self.depth + 1, move, self)
        self.children.append(child)
        return child

    def add_game(self, game):
        self.games.append(game)

    @property
    def size(self):
        return len(self.games)

    @property
    def sorted_children(self):
        return sorted(self.children, key=lambda c: -c.size)

    @property
    def black_to_move(self):
        return self.depth % 2

    def show(self):
        # TODO this method is massive. does everything need to be here?
        table = []
        for i, child in enumerate(self.sorted_children):
            percent = child.size / self.size * 100
            table.append([
                i,
                ('...' if self.black_to_move else '   ') + child.move,
                child.size,
                percent,
                [g.id for g in child.games] if len(child.games) <= 3 else [],
            ])

        identity  = lambda x: x
        ljust     = lambda n: lambda x: x.ljust(n)
        rjust     = lambda n: lambda x: x.rjust(n)
        lpad      = lambda n: lambda x: ' ' * n + x
        rpad      = lambda n: lambda x: x + ' ' * n
        parens    = lambda x: '(' + x + ')'

        LINK_WIDTH = 8
        MAX_NUM_LINKS = 3
        SEPARATOR_WIDTH = 2
        LINKS_COL_WIDTH = (LINK_WIDTH * MAX_NUM_LINKS
                           + SEPARATOR_WIDTH * (MAX_NUM_LINKS - 1))

        MOVE_COL_WIDTH = len('...exd8=Q+') - 3
        PERCENT_COL_WIDTH = len('100.0%')

        my_formatters = [
            [str, parens, rjust(6)],  # width is arbitrary
            [ljust(MOVE_COL_WIDTH)],
            [str, rjust(5)],  # width is arbitrary
            [lambda x: '{:.1f}%'.format(x), rjust(PERCENT_COL_WIDTH)],
            # TODO is that the right formatting for rounding?
            [lambda x: '  '.join(x), ljust(LINKS_COL_WIDTH), lpad(3)],
        ]

        print(format_table(table, my_formatters))

################################################################################


# TODO restore 'debug mode'


parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

main(args.filename)
