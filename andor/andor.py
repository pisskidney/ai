#!/usr/bin/python


''' Given a Tic-Tac-Toe position, decide whether or not the player
to move has a guaranteed win or not.
'''


import copy


switch = {
    'X': 'O',
    'O': 'X'
}


class Node(object):
    def __init__(self, children=None, val=None, data=None):
        if children is None:
            self.children = []
        else:
            self.children = children
        self.val = val
        self.data = data

    @classmethod
    def from_node(cls, node):
        new = cls()
        new.data = copy.deepcopy(node.data)
        return new

    def __repr__(self):
        return '%s\n%s\n%s\n%s\n' % (
            self.val, self.data[0], self.data[1], self.data[2]
        )


class TicTacTree(object):
    def __init__(self, root, tomove='X'):
        self.root = root
        self.levels = 0
        self.nodes = 1
        self.tomove = tomove
        self.expand(root, tomove)

    def finished(self, node):
        for line in node.data:
            for c in line:
                if c == '_':
                    return False
        return True

    def winner(self, node, player):
        if [player, player, player] in node.data:
            return True
        elif (player, player, player) in zip(*node.data):
            return True
        elif (node.data[0][0] == node.data[1][1] and
              node.data[1][1] == node.data[2][2] and
              node.data[2][2] == player):
            return True
        elif (node.data[2][0] == node.data[1][1] and
              node.data[1][1] == node.data[0][2] and
              node.data[0][2] == player):
            return True
        return False

    def expand(self, node, tomove):
        if self.winner(node, self.tomove):
            node.val = True
        elif self.winner(node, switch[self.tomove]):
            node.val = False
        elif self.finished(node):
            node.val = False
        else:
            for i in xrange(len(node.data)):
                for j in xrange(len(node.data[i])):
                    if node.data[i][j] == '_':
                        new = Node.from_node(node)
                        new.data[i][j] = tomove
                        node.children.append(new)
                        self.nodes += 1
                        self.expand(new, switch[tomove])

    def is_winner(self):
        return self.andor(self.root, self.tomove)

    def andor(self, node, tomove):
        if not node.children:
            return
        if self.tomove == tomove:
            result = False
            for child in node.children:
                if child.val is not None:
                    result = result or child.val
                else:
                    result = result or self.andor(child, switch[tomove])
        else:
            result = True
            for child in node.children:
                if child.val is not None:
                    result = result and child.val
                else:
                    result = result and self.andor(child, switch[tomove])
        return result

    def show(self, node):
        print node
        for n in node.children:
            self.show(n)


def main():
    root = Node(data=[['O', 'X', 'O'], ['_', '_', 'X'], ['_', '_', '_']])
    tree = TicTacTree(root, tomove='X')
    print tree.nodes
    print tree.is_winner()


if __name__ == "__main__":
    main()
