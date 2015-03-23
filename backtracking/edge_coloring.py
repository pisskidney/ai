#!/usr/bin/python

'''
Horvath Peter
Artificial Intelligence
Lab 1, Problem 16
'''


def read(filename):
    f = open(filename, mode='r')
    out = [int(x) for x in f.readline().strip().split(' ')]
    inn = [int(x) for x in f.readline().strip().split(' ')]
    v = set(out + inn)
    edges = [(out[i], inn[i]) for i in xrange(len(inn))]
    return v, edges


def generate(res, edges, pos, best):
    if pos == len(res):
        if len(set(res)) < len(set(best)):
            best[:] = res
        print res
        return
    candidates = range(len(edges))
    no_good = []
    for i in xrange(pos):
        curr_vertices = list(edges[pos])
        if edges[i][0] in curr_vertices or edges[i][1] in curr_vertices:
            no_good.append(res[i])
    good_candidates = [x for x in candidates if x not in no_good]

    for gc in good_candidates:
        res[pos] = gc
        generate(res, edges, pos + 1, best)


def main():
    v, edges = read('adj.txt')
    res = [0 for _ in xrange(len(edges))]
    best = range(len(edges))
    generate(res, edges, 0, best)
    print 'best: ', best


if __name__ == "__main__":
    main()
