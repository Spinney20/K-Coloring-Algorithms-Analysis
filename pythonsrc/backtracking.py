#!/usr/bin/env python3
"""
backtracking_color.py
Backtracking (Brute Force) pentru determinarea exacta a chi(G).
Metoda: loop k=1..n, prima colorare reusita -> chi(G).
"""

import time

def read_graph_adjmatrix(filename):
    with open(filename, "r") as f:
        n, m = map(int, f.readline().split())
        graph = [[0]*n for _ in range(n)]
        for _ in range(m):
            u, v = map(int, f.readline().split())
            graph[u][v] = 1
            graph[v][u] = 1
    return n, graph

def is_safe(v, graph, color, c, n):
    for i in range(n):
        if graph[v][i] == 1 and color[i] == c:
            return False
    return True

def backtracking_util(graph, k, color, v, n):
    if v == n:
        return True
    for c in range(1, k+1):
        if is_safe(v, graph, color, c, n):
            color[v] = c
            if backtracking_util(graph, k, color, v+1, n):
                return True
            color[v] = 0
    return False

def backtracking_min_color(graph, n):
    color = [0]*n
    for k in range(1, n+1):
        for i in range(n):
            color[i] = 0
        if backtracking_util(graph, k, color, 0, n):
            return k, color
    return n, color

def main():
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} <fisier.in>")
        return
    filename = sys.argv[1]
    n, graph = read_graph_adjmatrix(filename)
    start = time.perf_counter()
    chi, coloring = backtracking_min_color(graph, n)
    end = time.perf_counter()
    print(f"[Backtracking] n={n}, chi={chi}, time={end-start:.4f}s")

if __name__ == "__main__":
    main()
