"""
Usage:
  python3    ./wazir.py DB_PATH
  python3 -i ./wazir.py DB_PATH debug
"""


from game import Game
from filters import DateFilter, AllFilter, TimeControlFilter, RatedFilter
from command_parser import parse
from commands import (DaysCommand, FrequentCommand, HumanCommand,
        MonthsCommand, MoveCommand, RatedCommand, RootCommand,
        TimeControlCommand, UpCommand, YearsCommand)

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
    f = TimeControlFilter(30)
    games = f.apply(all_games)
    print(len(games))
    for g in games:
        print(g)
    print(len(games))


def update_tree(all_games, filters, path):
    """
    Filter games, return:
        (node_or_none, num_games)

    A path is a list of moves e.g. ['e4', 'e5']
    """
    games = all_games
    for f in filters.values():
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


def show(node):
    # TODO it's silly to have this and node.show()...
    if node:
        node.show()
    else:
        print('nothing')


def main_loop(all_games):
    filters = {
        DateFilter: AllFilter(),
        TimeControlFilter: AllFilter(),
        RatedFilter: AllFilter(),
    }
    path = []

    os.system('clear')
    print('\n')
    while True:
        node, num_games = update_tree(all_games, filters, path)
        show(node)
        try:
            raw_cmd = input('\n> ')
        except (EOFError, KeyboardInterrupt):
            print()
            exit(1)
        os.system('clear')

        output = ''

        # TODO encapsulate state into one object, write eval()
        cmd = parse(raw_cmd)
        if RootCommand.isinstance(cmd):
            path = []
        elif UpCommand.isinstance(cmd):
            # TODO "already at top"
            path = path[:-cmd.data.distance]
        elif FrequentCommand.isinstance(cmd):
            # TODO handle index error
            rank = cmd.data.rank
            move = node.sorted_children[rank].move
            path.append(move)
        elif DaysCommand.isinstance(cmd):
            filters[DateFilter] = DateFilter(cmd.data.days)
        elif TimeControlCommand.isinstance(cmd):
            filters[TimeControlFilter] = TimeControlFilter(cmd.data.minutes)
        elif MoveCommand.isinstance(cmd):
            path.append(cmd.data.move)
        elif RatedCommand.isinstance(cmd):
            if filters[RatedFilter]:
                filters[RatedFilter] = AllFilter()
            else:
                filters[RatedFilter] = RatedFilter()
        else:
            raise Exception('not implemented: ' + cmd.type)

        print(output + '\n')


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
        header = ('Depth: {}'.format(self.depth).ljust(11) +
                  ' Size: {}'.format(self.size) +
                  '\n')
        print(header)
        for i, child in enumerate(self.sorted_children):
            move = ('...' if self.black_to_move else '   ') + child.move
            percent = child.size / self.size * 100
            s = '  ({}) {}\t{}\t{:.1f}%'.format(i, move, child.size, percent)
            if child.size <= 3:
                s += '\t   ' + '  '.join(game.id for game in child.games)
            print(s)
            # TODO is that the right formatting for rounding?
            # TODO need real table formatting. also, moves can be up to
            #      seven characters long, e.g. exd8=Q+

################################################################################


# TODO restore 'debug mode'


parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

main(args.filename)
