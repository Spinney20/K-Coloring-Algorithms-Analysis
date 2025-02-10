#!/usr/bin/env python3
"""
welsh_powell_color.py
Implementare avansata WP:
 - sorteaza nodurile descrescator dupa grad
 - optional tie-break random
 - coloram nodurile in "valuri" cu aceeasi culoare
"""

import time, random

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

def welsh_powell_coloring(adj, deg, n, randtie=False):
    # creez o lista [ (node, deg[node], randomKey) ]
    # sort desc dupa deg, apoi randomKey
    nodes = list(range(n))
    if randtie:
        # random key
        labeled = [(u, deg[u], random.random()) for u in nodes]
        # sort => desc deg => asc random
        labeled.sort(key=lambda x:(x[1], -x[2]), reverse=True)
        # re-extrag ordinea
        order = [x[0] for x in labeled]
    else:
        order = sorted(nodes, key=lambda x: deg[x], reverse=True)

    color = [-1]*n
    usedColors = 0

    for u in order:
        if color[u] == -1:
            # culoare noua
            c = usedColors
            usedColors +=1
            color[u] = c

            # incerc sa colorez cu c toate nodurile necolorate neadiacente
            for v in order:
                if color[v]==-1:
                    # check daca v e neadiacent cu oricine care are color c
                    can_color = True
                    for w in adj[v]:
                        if color[w] == c:
                            can_color=False
                            break
                    if can_color:
                        color[v] = c

    return color, usedColors


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
    color, usedK = welsh_powell_coloring(adj, deg, n, randtie)
    end = time.perf_counter()
    print(f"[WelshPowellImpr] n={n}, usedK={usedK}, randTie={randtie}, time={end-start:.4f}s")

if __name__=="__main__":
    main()
