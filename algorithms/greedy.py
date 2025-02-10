#!/usr/bin/env python3
"""
greedy_color.py
Greedy "imbunatatit": incercam un numar de permutari random (default=3),
pastram colorarea cu nr minim de culori. Tot nu garanteaza minim, dar e mai bun
decât un singur greedy fix 0..n-1.
"""

import time, random

def read_graph_adjlist(filename):
    with open(filename, "r") as f:
        n, m = map(int, f.readline().split())
        adj = [[] for _ in range(n)]
        for _ in range(m):
            u,v = map(int, f.readline().split())
            adj[u].append(v)
            adj[v].append(u)
    return n, adj

def greedy_one_order(adj, order):
    """
    Aplica Greedy in ordinea "order" (list of nodes),
    returneaza vector color[], si nr culori folosite.
    color[node] = culoare (incepand de la 0).
    """
    n = len(adj)
    color = [-1]*n
    used = [False]*n
    # primul nod in order -> color=0
    first = order[0]
    color[first] = 0

    for idx in range(1, n):
        u = order[idx]
        # marchez culorile vecinilor
        for w in adj[u]:
            if color[w] != -1:
                used[color[w]] = True
        # gasesc prima culoare libera
        c = 0
        while c < n and used[c]:
            c+=1
        color[u] = c
        # reset used
        for w in adj[u]:
            if color[w] != -1:
                used[color[w]] = False
    return color, max(color)+1

def greedy_improved(adj, n, retries=3):
    """
    Incearca 'retries' permutari random ale [0..n-1].
    Pastreaza colorarea cu nr minimal de culori.
    """
    best_colors = None
    best_k = n+1
    nodes = list(range(n))
    for _ in range(retries):
        random.shuffle(nodes)
        c, k = greedy_one_order(adj, nodes)
        if k < best_k:
            best_k = k
            best_colors = c[:]
    return best_colors, best_k

def main():
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} <fisier.in> [retries]")
        return
    filename = sys.argv[1]
    retries = 3
    if len(sys.argv)>2:
        retries = int(sys.argv[2])
    n, adj = read_graph_adjlist(filename)
    start = time.perf_counter()
    color, used_k = greedy_improved(adj, n, retries)
    end = time.perf_counter()
    durata = end - start
    print(f"[GreedyImpr] n={n}, used_k={used_k}, retries={retries}, time={durata:.4f}s")

if __name__=="__main__":
    main()
