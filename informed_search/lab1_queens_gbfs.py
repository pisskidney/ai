#!/usr/bin/python
from collections import deque


def main():
    n = raw_input('How many rows? n= ')
    m = raw_input('How many columns? m= ')
    GBFS(int(n), int(m))


def GBFS(n, m):
    q = deque()
    root = Board(n, m)
    q.append(root)
    while(q):
        #Use the dequeue as a queue
        current_board = q.popleft()
        if current_board.is_done():
            print current_board
            return
        else:
            #Generate new states
            for i in range(m):
                new_board = Board.from_board(current_board)
                new_board.add(i)
                if new_board.no_attacks:
                    if new_board.is_done():
                        print new_board
                        return
                    else:
                        q.append(new_board)
            #Sort states based on some heuristics. GBFS!!!
            sort(q)


#The GBFS heuristics function
def sort(queue):
    #cant think of any atm
    pass


class Board():
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.board = [[0 for i in range(m)] for i in range(n)]
        self.queens = []

    @classmethod
    def from_board(cls, board):
        import copy
        new = cls(board.n, board.m)
        new.board = copy.deepcopy(board.board)
        new.queens = list(board.queens)
        return new

    def add(self, m):
        self.board[len(self.queens)][m] = 1
        self.queens.append(m)

    def pop(self):
        self.queens.pop()

    def is_done(self):
        return len(self.queens) == min(self.n, self.m)

    @property
    def no_attacks(self):
        for i in range(self.n):
            if self.board[i].count(1) > 1:
                return False
        rotated = zip(*self.board)
        for i in range(self.m):
            if rotated[i].count(1) > 1:
                return False
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] != 0:
                    for k in range(self.n):
                        for l in range(self.m):
                            if (self.board[k][l] != 0 and
                                    (i != k and j != l) and
                                    abs(i-k) == abs(j-l)):
                                return False
        return True

    def __str__(self):
        str = ''
        for i in range(self.n):
            str += ' '.join(['-' if x == 0 else 'Q' for x in self.board[i]])
            str += '\n'
        return str


if __name__ == "__main__":
    main()
