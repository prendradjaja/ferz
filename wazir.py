"""
Usage:
  python3    ./explorer.py DB_PATH
  python3 -i ./explorer.py DB_PATH debug
"""

import os
import sys

def usage():
    print(__doc__[1:][:-1])
    exit(1)

def main_loop(root):
    node = root

    os.system('clear')
    print('\n')
    while True:
        node.show()
        cmd = input('\n> ')
        os.system('clear')

        output = ''

        if cmd == '/':
            node = root
        elif cmd == '-':
            if node.parent:
                node = node.parent
            else:
                output = 'already at top of tree'
        elif len(cmd) == 1 and cmd in '0123456789':
            try:
                node = node.sorted_children[int(cmd)]
            except IndexError:
                output = 'IndexError'
        elif cmd == '':
            if node.children:
                node = node.sorted_children[0]
            else:
                output = 'already at bottom of tree'
        elif node.has_child(cmd):
            node = node.child(cmd)
        else:
            output = 'no such child ' + cmd

        print(output + '\n')

def make_tree(filename):
    games = []
    with open(filename) as f:
        for line in f:
            id, *moves = line.split()
            games.append(Game(id, moves))

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

# TODO: reconcile this with the other Game class
class Game:
    def __init__(self, id, moves):
        self.id = id
        self.moves = moves

    def __str__(self):
        return '{}: {}'.format(self.id, self.moves)

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


if len(sys.argv) not in (2, 3):
    usage()
filename = sys.argv[1]

root = make_tree(filename)

if len(sys.argv) == 3:
    if sys.argv[2] == 'debug':
        print('DEBUG MODE.')
        print('Inspecting database:', filename)
        print()

        r = root
        n = node = root
        n.show()

        print('\nAvailable local variables: n (node), r (root)')
    else:
        usage()
elif len(sys.argv) == 2:
    if filename == 'debug':
        print('Whoops. You gave me the filename "debug"!')
        exit(1)
    main_loop(root)
else:
    assert False, 'Impossible!'
    # Should've already exited if invalid number of arguments.
