#!/usr/bin/python


''' Given a Tic-Tac-Toe position, decide whether or not the player
to move has a guaranteed win or not.
'''


import copy


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



class TicTacTree(object):
    def __init__(self, root):
        self.root = root
        self.levels = 0
        self.expand(root, 'X')

    def expand(self, node, tomove):
        if self.winner(node, 'X'):
            node.val = True
        elif self.winner(node, 'O'):
            node.val = False
        elif self.finished(node):
            node.val = False
        else:
            nextmove = 'X' if tomove == 'O' else 'O'
            for i in xrange(len(node.data)):
                for j in xrange(len(node.data[i]))
                    if node.data[i][j] == '_':
                        new = Node.from_node(node)
                        new.data[i][j] = tomove
                        self.children.append(new)
                        self.expand(new, nextmove)


def main():
    root = Node(data=[['O', 'X', 'O'], ['_', '_', 'X'], ['_', '_', '_']])
    tree = TicTacTree(root)


if __name__ == "__main__":
    main()


    

