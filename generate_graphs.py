#!/usr/bin/env python3

import os
import math
import random
import argparse
import networkx as nx

def parse_single_range(arg: str):
    """
    Paraseaza un string de forma "start:end:step" in range(start, end+1, step).
    - Ex: "10:20:2" -> range(10,21,2)
          "30:40"   -> range(30,41,1)
          "15"      -> range(15,16,1)
    """
    parts = arg.split(":")
    if len(parts) == 1:
        start = int(parts[0])
        return range(start, start+1, 1)
    elif len(parts) == 2:
        start = int(parts[0])
        end   = int(parts[1])
        return range(start, end+1, 1)
    elif len(parts) == 3:
        start = int(parts[0])
        end   = int(parts[1])
        step  = int(parts[2])
        return range(start, end+1, step)
    else:
        raise ValueError(f"Format invalid pentru range: '{arg}' (foloseste start:end:step)")

def parse_intervals(arg: str):
    """
    Paraseaza un string cu una sau mai multe intervale separate prin virgule,
    ex: "10:20:2,30:100:10"
    Returneaza o lista de range-uri, ex: [range(10,21,2), range(30,101,10)].
    Daca `arg` e gol, returneaza lista goala => nu generam nimic.
    """
    arg = arg.strip()
    if not arg:
        return []
    segments = arg.split(",")
    ranges = []
    for seg in segments:
        seg = seg.strip()
        if seg:
            r = parse_single_range(seg)
            ranges.append(r)
    return ranges

def save_graph_nx(G: nx.Graph, filename: str):
    """
    Salvam graful G in fisier, format:
       n m
       u1 v1
       ...
       um vm
    cu noduri 0-based.
    """
    mapping = {node: i for i, node in enumerate(G.nodes())}
    G = nx.relabel_nodes(G, mapping)
    n = G.number_of_nodes()
    m = G.number_of_edges()

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(f"{n} {m}\n")
        for (u,v) in G.edges():
            if u>v:
                u,v = v,u
            f.write(f"{u} {v}\n")

def generate_bipartite(n: int):
    """
    Bipartit complet (n1, n2) unde n1 = n//2, n2 = n - n1
    """
    if n <= 0:
        return
    n1 = n//2
    n2 = n - n1
    G = nx.complete_bipartite_graph(n1, n2)
    fname = f"generated_tests/bip_{n}_{n1}_{n2}.in"
    save_graph_nx(G, fname)
    print(f"[OK] Bipartite {n} -> {fname}")

def generate_chordal_interval(n: int):
    """
    Graph chordal: creeaza un interval graph cu n intervale random.
    """
    if n <= 0:
        return
    intervals = []
    for i in range(n):
        start = random.uniform(0,100)
        length= random.uniform(1,10)
        intervals.append((start, start+length))

    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i+1,n):
            s1,e1 = intervals[i]
            s2,e2 = intervals[j]
            if not (e1 < s2 or e2 < s1):
                G.add_edge(i,j)

    fname = f"generated_tests/chordal_{n}.in"
    save_graph_nx(G, fname)
    print(f"[OK] Chordal {n} -> {fname}")

def generate_random_erdos(n: int, pvals: list):
    """
    Genereaza random Erdos-Renyi G(n, p) pentru fiecare p din pvals
    Ex: pvals = [0.3, 0.8]
    """
    if n <= 0:
        return
    for p in pvals:
        G = nx.erdos_renyi_graph(n, p)
        fname = f"generated_tests/random_{n}_p{p}.in"
        save_graph_nx(G, fname)
        print(f"[OK] Random n={n}, p={p} -> {fname}")

def generate_complete(n: int):
    """
    Graf complet K_n => n*(n-1)/2 muchii
    """
    if n <= 0:
        return
    G = nx.complete_graph(n)
    fname = f"generated_tests/complete_{n}.in"
    save_graph_nx(G, fname)
    print(f"[OK] Complete {n} -> {fname}")

def generate_planar_grid(n: int):
    """
    Grid 2D (side x side), apoi tai nodurile in plus daca side^2 > n
    => Aproximare graf planabil (bipartit).
    """
    if n <= 0:
        return
    side = int(math.sqrt(n))
    if side*side < n:
        side+=1
    G = nx.grid_2d_graph(side, side)
    G = nx.convert_node_labels_to_integers(G)
    # daca e > n, sterg un surplus
    alln = list(G.nodes())
    if len(alln)>n:
        for nod in alln[n:]:
            G.remove_node(nod)
    fname = f"generated_tests/planar_{n}.in"
    save_graph_nx(G, fname)
    print(f"[OK] Planar(aprox) {n} -> {fname}")

def generate_fullrandom(n: int, p=0.5):
    """
    "Full random" = Erdos-Renyi cu p=0.5 by default (sau alt p fix).
    """
    if n <= 0:
        return
    G = nx.erdos_renyi_graph(n, p)
    fname = f"generated_tests/fullrandom_{n}_p{p}.in"
    save_graph_nx(G, fname)
    print(f"[OK] FullRandom n={n}, p={p} -> {fname}")

def generate_shc(n: int):
    """
    Generam un exemplu de "Slightly Hard to Color".
    - 30% noduri intr-o clique mare
    - restul nodurilor conectate partial la clique si intre ele cu prob=0.2
    -> Nu exista garantii formale, dar poate fi o instanta "SHC-like".
    """
    if n <= 0:
        return
    G = nx.Graph()
    G.add_nodes_from(range(n))

    # calculez clique_size ~30% din n, minim 2
    clique_size = max(2, int(0.3*n))
    clique_nodes = list(range(clique_size))
    # Adaug muchii complete in clique
    for i in range(clique_size):
        for j in range(i+1, clique_size):
            G.add_edge(i, j)

    # restul nodurilor [clique_size..n-1]
    # conectare partiala
    for node in range(clique_size, n):
        # conectez random ~ jumatate la clique
        # ex: half
        half = clique_size//2
        # extrag aleator half noduri din clique
        chosen = random.sample(clique_nodes, min(half, clique_size))
        for c in chosen:
            G.add_edge(node, c)

        # plus un 0.2 prob la oricare alt node in [clique_size..node-1]
        for other in range(clique_size, node):
            if random.random() < 0.2:
                G.add_edge(node, other)

    fname = f"generated_tests/shc_{n}.in"
    save_graph_nx(G, fname)
    print(f"[OK] SHC n={n} -> {fname}")

# ---------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Genereaza grafuri de tipuri diferite, inclusiv fullrandom si shc. Daca nimic pt un tip, nu-l genereaza."
    )
    # deja existente
    parser.add_argument("--bip",
                        help="Intervale pt bipartite: '20:30:2,40:60:10'")
    parser.add_argument("--chordal",
                        help="Intervale pt chordal: '10:20:2,30:50:10'")
    parser.add_argument("--random",
                        help="Intervale pt random Erdos-Renyi: '30:50:10,60:80:20'")
    parser.add_argument("--pvalues",
                        default="0.3,0.8",
                        help="Lista p pt random, ex '0.3,0.8'")
    parser.add_argument("--complete",
                        help="Intervale pt complete: '10:40:10,50:60:5'")
    parser.add_argument("--planar",
                        help="Intervale pt planare(grid): '10:30:10,50:100:25'")
    # noi
    parser.add_argument("--fullrandom",
                        help="Intervale pt fullrandom cu p=0.5 (sau alt p fix). Ex: '10:20:1'")
    parser.add_argument("--shc",
                        help="Intervale pt SHC-like. Ex: '20:40:10'")

    args = parser.parse_args()

    # parse pvalues
    pvals = [float(x) for x in args.pvalues.split(",")] if args.pvalues else []

    os.makedirs("generated_tests", exist_ok=True)

    # bip
    if args.bip:
        intervals = parse_intervals(args.bip)
        for r in intervals:
            for n in r:
                generate_bipartite(n)

    # chordal
    if args.chordal:
        intervals = parse_intervals(args.chordal)
        for r in intervals:
            for n in r:
                generate_chordal_interval(n)

    # random
    if args.random:
        intervals = parse_intervals(args.random)
        for r in intervals:
            for n in r:
                generate_random_erdos(n, pvals)

    # complete
    if args.complete:
        intervals = parse_intervals(args.complete)
        for r in intervals:
            for n in r:
                generate_complete(n)

    # planar
    if args.planar:
        intervals = parse_intervals(args.planar)
        for r in intervals:
            for n in r:
                generate_planar_grid(n)

    #PE ASGEA NU LE AM MAI FOLOSIT, DAR LE AM LASAT AICI FOR THE PLOT
    # fullrandom
    if args.fullrandom:
        intervals = parse_intervals(args.fullrandom)
        for r in intervals:
            for n in r:
                generate_fullrandom(n, p=0.5)  # p fix 0.5, ex.

    # shc
    if args.shc:
        intervals = parse_intervals(args.shc)
        for r in intervals:
            for n in r:
                generate_shc(n)

    print("\n=== Gata! Am generat testele in folderul 'generated_tests'. ===")

if __name__=="__main__":
    main()
