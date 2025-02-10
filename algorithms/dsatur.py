#!/usr/bin/env python3
"""
dsatur_color.py
Versiune imbunatatita DSATUR: 
 - la fiecare pas, aleg nodul necolorat cu sat maxim (tie-break grad + random).
 - actualizez sat in mod inteligent.

Poate folosi parametru "randtie=True" pentru a rezolva egalitatile random.
"""

import time, random, heapq

def read_graph_adjlist(filename):
    with open(filename, "r") as f:
        n,m = map(int, f.readline().split())
        adj = [[] for _ in range(n)]
        deg = [0]*n
        for _ in range(m):
            u,v = map(int, f.readline().split())
            adj[u].append(v)
            adj[v].append(u)
            deg[u]+=1
            deg[v]+=1
    return n, adj, deg

class DSNode:
    __slots__ = ("vertex", "sat", "deg")
    def __init__(self, vertex, sat, deg):
        self.vertex = vertex
        self.sat = sat
        self.deg = deg

def dsatur_coloring(adj, deg, n, randtie=False):
    """
    DSATUR:
    - color[u] = -1 initially
    - sat[u] = 0
    - la fiecare pas, pick nod cu saturatie maxima, tie-break grad, eventual random
    - color[u] = cea mai mica culoare libera
    - update sat la vecini
    Returneaza (color, nr_culori_fol)
    """
    color = [-1]*n
    sat = [0]*n
    # Folosim un heap "negativ" pentru a simula prioritate maxima
    # vom stoca tuple: ( -sat[u], -deg[u], random_key, u )
    # random_key -> un integer random la init
    # astfel, daca e egal saturatia si gradul, random decide ordinea

    heap = []
    for u in range(n):
        rkey = random.randint(0, 999999) if randtie else 0
        heapq.heappush(heap, (-sat[u], -deg[u], rkey, u))

    maxColor = -1

    visited = 0
    while visited < n:
        # extrag top
        # scot tot ce e "outdated"
        ok = False
        while heap and not ok:
            cursat, curdeg, rk, u = heapq.heappop(heap)
            cursat = -cursat
            curdeg = -curdeg
            # verific daca e actual in sat[u] / deg[u]
            if cursat == sat[u] and curdeg == deg[u] and color[u] == -1:
                # e valid
                ok = True
                pick = u
        if not ok:
            # no more
            break

        # coloram pick
        used_colors = set()
        for w in adj[pick]:
            if color[w] != -1:
                used_colors.add(color[w])
        c = 0
        while c in used_colors:
            c+=1
        color[pick] = c
        if c> maxColor:
            maxColor= c

        # update saturatie vecinilor necolorati
        for w in adj[pick]:
            if color[w] == -1:
                # daca c nu era deja in vecinii lui w
                # testam daca c e nou
                # mai simplu: sat[w] += 1 daca c nu e in "veciniColored"
                # fac un set ptr culori in vecini? 
                # => pot menține adjCols[w]
                pass
        visited +=1

        # updatam heap pt toti?
        # e costisitor, dar incercam. 
        # in DSATUR se actualizeaza sat[w] += 1 daca c e nou
        for w in adj[pick]:
            if color[w] == -1:
                # calc sat[w] -> culori distincte la vecini
                neighbor_colors = set()
                for ww in adj[w]:
                    if color[ww] != -1:
                        neighbor_colors.add(color[ww])
                sat[w] = len(neighbor_colors)
                # reinseram in heap
                rkey = random.randint(0,999999) if randtie else 0
                heapq.heappush(heap, (-sat[w], -deg[w], rkey, w))

    return color, maxColor+1

def main():
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} <fisier.in> [randtie=True/False]")
        return
    filename = sys.argv[1]
    randtie = False
    if len(sys.argv)>2:
        randtie = (sys.argv[2].lower()=="true")

    n, adj, deg = read_graph_adjlist(filename)
    start = time.perf_counter()
    color, usedk = dsatur_coloring(adj, deg, n, randtie)
    end = time.perf_counter()
    print(f"[DSATURImpr] n={n}, usedK={usedk}, randTie={randtie}, time={end-start:.4f}s")

if __name__=="__main__":
    main()
