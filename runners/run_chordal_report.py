#!/usr/bin/env python3
"""
run_chordal_report.py

- Cauta DOAR fisiere chordal_*.in din folderul 'generated_tests/'.
- Foloseste formula chordal: chi(G)=omega(G) => calcul polinomial (MCS).
- Avem 4 algoritmi: Backtracking, Greedy, DSATUR, WelshPowell, cu timeout=MAX_TIME.
- DACA un algoritm (ex. Backtracking) da Timeout la un anumit n,
  NU mai incercam deloc acel algoritm la n mai mari => skip,
  DAR incercam in continuare ceilalti algoritmi pt testele ulterioare.
- Tabel tip matrice + statistici, la fel ca in versiunile anterioare.
"""

import os
import sys
import re
import subprocess
import time

SCRIPT_FOLDER = "pythonsrc"
TEST_FOLDER   = "generated_tests"
MAX_TIME      = 15.0  # secunde

ALGOS = [
    ("Backtracking",  os.path.join(SCRIPT_FOLDER, "backtracking.py")),
    ("Greedy",        os.path.join(SCRIPT_FOLDER, "greedy.py")),
    ("DSATUR",        os.path.join(SCRIPT_FOLDER, "dsatur.py")),
    ("WelshPowell",   os.path.join(SCRIPT_FOLDER, "welsh_powell.py")),
]


# -------------------------------------------------------------------
# Functii de citire + MCS
# -------------------------------------------------------------------
def read_chordal_infile(path):
    with open(path, "r") as f:
        n,m = map(int, f.readline().split())
        adj = [[] for _ in range(n)]
        for _ in range(m):
            line = f.readline().strip()
            u,v = map(int, line.split())
            adj[u].append(v)
            adj[v].append(u)
    return n, adj

def compute_omega_chordal(adj, n):
    return mcs_omega(adj,n)

def mcs_omega(adj,n):
    label   = [0]*n
    visited = [False]*n
    omega   = 1
    for _ in range(n):
        best = -1
        bestLab= -1
        for v in range(n):
            if not visited[v] and label[v]> bestLab:
                bestLab= label[v]
                best= v
        visited[best]= True
        # clique size
        csize=1
        for w in adj[best]:
            if visited[w]:
                csize+=1
        if csize>omega:
            omega=csize
        # update
        for w in adj[best]:
            if not visited[w]:
                label[w]+=1
    return omega

def parse_k_time(stdout):
    k_pat = re.search(r"(?:chi=|used_k=|usedK=)(\d+)", stdout)
    t_pat = re.search(r"time=([\d\.]+)", stdout)
    if k_pat:
        k_val= int(k_pat.group(1))
    else:
        k_val= -1
    if t_pat:
        t_val= float(t_pat.group(1))
    else:
        t_val= -1.0
    return k_val, t_val


def main():
    if not os.path.isdir(TEST_FOLDER):
        print(f"Eroare: folderul '{TEST_FOLDER}' nu exista.")
        sys.exit(1)

    # colectam chordal_*.in
    all_files = os.listdir(TEST_FOLDER)
    chordal_files = [f for f in all_files if f.startswith("chordal_") and f.endswith(".in")]
    if not chordal_files:
        print("Nu exista fisiere chordal_*.in!")
        sys.exit(0)

    # sort
    def extract_n(fname):
        m = re.match(r"chordal_(\d+)", fname)
        return int(m.group(1)) if m else 999999
    chordal_files.sort(key=extract_n)

    # results[fname][algoName] = {k, time, correct, skip}
    results={}
    stats_tests_total=0
    stats_tested   = {a[0]:0 for a in ALGOS}
    stats_correct  = {a[0]:0 for a in ALGOS}
    stats_time     = {a[0]:0.0 for a in ALGOS}

    # NE introducem un dict "stop_for_algo" care devine True
    # daca un algo a dat Timeout la un n => nu-l mai rulam la n mai mari.
    stop_for_algo = {a[0]: False for a in ALGOS}

    for fname in chordal_files:
        path_in= os.path.join(TEST_FOLDER, fname)
        # calc n, adj
        n, adj= read_chordal_infile(path_in)
        w= compute_omega_chordal(adj,n)
        stats_tests_total+=1

        results[fname]= {
            "n": n,
            "omega": w,
            "algos": {}
        }

        print(f"\n=== {fname} => n={n}, omega={w} ===")

        for (algoName, scriptPath) in ALGOS:
            # daca deja a crapat la un n mai mic => skip direct
            if stop_for_algo[algoName]:
                results[fname]["algos"][algoName] = {
                    "k":-1,"time":-1,"correct":False,"skip":True
                }
                print(f"  {algoName}: skip (deja a dat timeout la un n mai mic)")
                continue

            # altfel incercam
            try:
                st= time.perf_counter()
                proc= subprocess.run(
                    ["python3", scriptPath, path_in],
                    capture_output=True,
                    text=True,
                    timeout=MAX_TIME
                )
                en= time.perf_counter()
                dur= en-st

                so= proc.stdout
                se= proc.stderr
                k_val, t_val= parse_k_time(so)
                correct= (k_val==w)

                results[fname]["algos"][algoName]={
                    "k":k_val,"time":dur,"correct":correct,"skip":False
                }
                stats_tests_total
                stats_tested[algoName]+=1
                if correct:
                    stats_correct[algoName]+=1
                stats_time[algoName]+=dur

                print(f"  {algoName}: k={k_val}, time={dur:.4f}s => correct={correct}")
                if se and se.strip():
                    print("    [stderr]:", se.strip())

            except subprocess.TimeoutExpired:
                # Timeout => de acum incolo => skip
                print(f"  {algoName}: TIMEOUT => nu-l mai rulam la n mai mari")
                results[fname]["algos"][algoName]={
                    "k":-1,"time":MAX_TIME,"correct":False,"skip":True
                }
                # nu-l pun in stats
                stop_for_algo[algoName]= True

    # generam chordal_report.md
    outfname= "chordal_report.md"
    with open(outfname,"w") as fout:
        fout.write("# Raport Grafuri Chordale (stop partial pt. Timeout)\n\n")
        fout.write(f"Total fisiere chordal: {stats_tests_total}\n\n")
        fout.write(f"Daca un algoritm timeouteaza, nu-l mai rulam la testele ulterioare.\n\n")
        fout.write("## Tabel cu rezultate\n\n")

        # Tabel
        header="| File | n | ω |"
        for (algoName,_) in ALGOS:
            header+= f" {algoName} k | {algoName} time | {algoName} ok |"
        header+="\n"
        col_count=3+3*len(ALGOS)
        sep= "|" + ("---|"*col_count) + "\n"

        fout.write(header)
        fout.write(sep)

        for fname in chordal_files:
            if fname not in results:
                # poate ceva ciudat
                continue
            n_ = results[fname]["n"]
            w_ = results[fname]["omega"]
            row= f"| {fname} | {n_} | {w_} "
            for (algoName,_) in ALGOS:
                ad= results[fname]["algos"].get(algoName,None)
                if not ad:
                    row+="| - | - | skip "
                    continue
                if ad["skip"]:
                    if ad["time"]==MAX_TIME:
                        row+= f"| - | >{MAX_TIME}s | skip "
                    else:
                        row+= f"| - | - | skip "
                else:
                    k_= ad["k"]
                    tm_= ad["time"]
                    c_= ad["correct"]
                    cstr= "YES" if c_ else "NO"
                    row+= f"| {k_} | {tm_:.4f}s | {cstr} "
            row+="|\n"
            fout.write(row)

        # statistici
        fout.write("\n## Statistici globale\n\n")
        fout.write("| Algo | #Tested | #Correct | %Correct | AvgTime(s) | TotalTime(s) |\n")
        fout.write("|---|---|---|---|---|---|\n")

        for (algoName,_) in ALGOS:
            tested= stats_tested[algoName]
            corr= stats_correct[algoName]
            ratio= 100.0*corr/tested if tested>0 else 0.0
            totalT= stats_time[algoName]
            avgT= totalT/tested if tested>0 else 0.0
            fout.write(f"| {algoName} | {tested} | {corr} | {ratio:.1f}% | {avgT:.4f} | {totalT:.4f} |\n")

        fout.write("\nObservatie: Daca un algoritm a dat Timeout la un test => nu-l mai incercam la testele cu n mai mare.\n")
        fout.write("In rest, logica e identica cu run_chordal_report.py.\n")

    print(f"\n=== Raport generat in '{outfname}' ===")


if __name__=="__main__":
    main()
