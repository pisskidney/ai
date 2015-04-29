#!/usr/bin/python


xi = (-1, -1, 1, 1, 2, -2, 2, -2)
xj = (2, -2, 2, -2, -1, -1, 1, 1)


def all_covered(board, n, m):
    for i in xrange(n):
        for j in xrange(m):
            ok = False
            for k in xrange(8):
                if (i + xi[k] >= 0 and i + xi[k] < n and
                    j + xj[k] >= 0 and j + xj[k] < m and
                    board[i+xi[k]][j+xj[k]] is True):
                    ok = True
                    break
            if not ok:
                return False
    return True


def min_knights(n, m):
    board = [[True for _ in xrange(m)] for _ in xrange(n)]
    for i in xrange(n):
        for j in xrange(m):
            if board[i][j] is True:
                board[i][j] = False
                if not all_covered(board, n, m):
                    board[i][j] = True
    print board
    return sum([sum(x) for x in board])


def back(board, n, m, i, j):
    if i >= n:
        return sum([sum(x) for x in board]) if all_covered(board, n, m) else n*m
    if j >= m - 1:
        newi = i + 1
        newj = 0
    else:
        newi = i
        newj = j + 1
    board[i][j] = False
    x = back(board, n, m, newi, newj)
    board[i][j] = True
    y = back(board, n, m, newi, newj)
    return min(x, y)


def main():
    n = int(raw_input('n= '))
    m = int(raw_input('m= '))
    print min_knights(n, m)

    board = [[False for _ in xrange(m)] for _ in xrange(n)]
    print back(board, n, m, 0, 0)


if __name__ == "__main__":
    main()
