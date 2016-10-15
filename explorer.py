def make_tree(filename):
    games = []
    with open(filename) as f:
        for line in f:
            id, *moves = line.split()
            games.append(Game(id, moves))

    root = Node()

    for g in games:
        node = root
        for move in g.moves:  # TODO move in g?
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
    def __init__(self, move=None, parent=None):
        self.move = move
        self.games = []
        self.children = []
        self.parent = parent

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
        child = Node(move, self)
        self.children.append(child)
        return child

    def add_game(self, game):
        self.games.append(game)


# filename = './tiny-db'
# filename = './small-db'
filename = './medium-db'

tree = make_tree(filename)
