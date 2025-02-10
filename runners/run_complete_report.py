#!/usr/bin/env python3
"""
run_complete_report.py

- Cauta DOAR fisiere complete_*.in din folderul 'generated_tests/'.
- Pentru un graf complet K_n, chi(G) = n. Deci "k_corect" = n.
- Ruleaza 4 algoritmi (Backtracking, Greedy, DSATUR, WelshPowell) cu timeout=MAX_TIME sec.
  Daca depaseste MAX_TIME => skip (nu e inclus in statistici).
- Compara k_val cu n => correct/not.
- Genereaza un raport Markdown (tabel + statistici) in complete_report.md.
- Afiseaza timpul cu 4 zecimale si adauga la statistici finale si "TotalTime(s)" (timpul cumulat).
"""

import os
import sys
import re
import subprocess
import time

SCRIPT_FOLDER = "pythonsrc"      # folderul cu fisierele .py (backtracking, etc.)
TEST_FOLDER   = "generated_tests" # folderul cu fisiere complete_*.in

MAX_TIME = 35.0  # secunde, daca se depaseste => skip

ALGOS = [
    ("Backtracking",  os.path.join(SCRIPT_FOLDER, "backtracking.py")),
    ("Greedy",        os.path.join(SCRIPT_FOLDER, "greedy.py")),
    ("DSATUR",        os.path.join(SCRIPT_FOLDER, "dsatur.py")),
    ("WelshPowell",   os.path.join(SCRIPT_FOLDER, "welsh_powell.py")),
]

def parse_k_time(stdout):
    """
    In stdout cautam:
       (chi=|used_k=|usedK=)(\\d+)
       time=([\\d\\.]+)
    Return (k_val, t_val), sau (-1, -1.0) daca nu gasim.
    """
    k_pat = re.search(r"(?:chi=|used_k=|usedK=)(\d+)", stdout)
    t_pat = re.search(r"time=([\d\.]+)", stdout)
    if k_pat:
        k_val = int(k_pat.group(1))
    else:
        k_val = -1
    if t_pat:
        t_val = float(t_pat.group(1))
    else:
        t_val = -1.0
    return k_val, t_val

def extract_n(fname):
    """
    Pt. un fisier complete_30.in, extrag n=30 prin regex 'complete_(\\d+)'.
    Daca nu match, return 999999 => sort la coada.
    """
    m = re.match(r"complete_(\d+)", fname)
    if m:
        return int(m.group(1))
    return 999999

def read_complete_infile(path):
    """
    Citeste fisier:
      n m
      u1 v1
      ...
    Returneaza (n, adj) - desi pt. complet e clar m = n*(n-1)/2
    """
    with open(path, "r") as f:
        n, m = map(int, f.readline().split())
        adj = [[] for _ in range(n)]
        for _ in range(m):
            line = f.readline().strip()
            u, v = map(int, line.split())
            adj[u].append(v)
            adj[v].append(u)
    return n, adj

def main():
    # 1) Verificam folderul cu teste
    if not os.path.isdir(TEST_FOLDER):
        print(f"Folderul '{TEST_FOLDER}' nu exista.")
        sys.exit(1)

    # 2) Gasim complete_*.in
    all_files = os.listdir(TEST_FOLDER)
    complete_files = [f for f in all_files if f.startswith("complete_") and f.endswith(".in")]
    if not complete_files:
        print(f"Nu exista fisiere complete_*.in in '{TEST_FOLDER}'!")
        sys.exit(0)

    # sortam dupa n
    complete_files.sort(key=extract_n)

    # results[testFile][algoName] = {k, time, correct, skip}
    results = {}

    # statistici
    stats_tests_total = 0
    stats_tested   = {a[0]: 0 for a in ALGOS}
    stats_correct  = {a[0]: 0 for a in ALGOS}
    stats_time     = {a[0]: 0.0 for a in ALGOS}   # totalTime

    for fname in complete_files:
        path_in = os.path.join(TEST_FOLDER, fname)
        n, adj = read_complete_infile(path_in)
        # Pt. K_n => chi(G) = n
        chi_correct = n
        stats_tests_total += 1

        results[fname] = {"n": n, "chi": chi_correct, "algos": {}}

        print(f"\n=== {fname} => n={n}, chi(G)={chi_correct} ===")

        # Rulam 4 algoritmi cu timeout
        for (algoName, scriptPath) in ALGOS:
            cmd = ["python3", scriptPath, path_in]
            try:
                start_t = time.perf_counter()
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=MAX_TIME)
                end_t   = time.perf_counter()
                dur = end_t - start_t

                stdout = proc.stdout
                stderr = proc.stderr
                k_val, t_val = parse_k_time(stdout)
                correct = (k_val == chi_correct)

                results[fname]["algos"][algoName] = {
                    "k": k_val,
                    "time": dur,
                    "correct": correct,
                    "skip": False
                }
                # statistici
                stats_tested[algoName] += 1
                if correct:
                    stats_correct[algoName] += 1
                stats_time[algoName] += dur

                # log scurt cu 4 zecimale
                print(f"  {algoName}: k={k_val}, time={dur:.4f}s, correct={correct}")
                if stderr and stderr.strip():
                    print("   [stderr]:", stderr.strip())

            except subprocess.TimeoutExpired:
                # skip
                print(f"  {algoName}: TIMEOUT > {MAX_TIME}s => skip from stats")
                results[fname]["algos"][algoName] = {
                    "k": -1,
                    "time": MAX_TIME,
                    "correct": False,
                    "skip": True
                }
                # nu incrementam stats_tested => e ca si cum n-am testat

    # generam complete_report.md
    outfname = "complete_report.md"
    with open(outfname, "w") as fout:
        fout.write("# Raport Grafuri Complete\n\n")
        fout.write(f"Total fisiere complete: {stats_tests_total}\n\n")
        fout.write("## Tabel cu rezultate\n\n")

        # 1 col File, 1 col n, 1 col (chi?), 4*3 = 12, deci total 1+1+1 + 12 = 15
        header = "| File | n | chi |"
        for (algoName, _) in ALGOS:
            header += f" {algoName} k | {algoName} time | {algoName} ok |"
        header += "\n"
        col_count = 3 + 3 * len(ALGOS)
        sep = "|" + ("---|" * col_count) + "\n"

        fout.write(header)
        fout.write(sep)

        for fname in complete_files:
            n_val = results[fname]["n"]
            chi   = results[fname]["chi"]
            row = f"| `{fname}` | {n_val} | {chi} "
            for (algoName, _) in ALGOS:
                adata = results[fname]["algos"][algoName]
                if adata["skip"]:
                    row += f"| - | >{MAX_TIME}s | skip "
                else:
                    k    = adata["k"]
                    dur  = adata["time"]
                    corr = adata["correct"]
                    cstr = "YES" if corr else "NO"
                    # afisam dur cu 4 zecimale
                    row += f"| {k} | {dur:.4f}s | {cstr} "
            row += "|\n"
            fout.write(row)

        # statistici globale
        fout.write("\n## Statistici globale\n\n")
        fout.write("| Algo | #Tested | #Correct | %Correct | AvgTime(s) | TotalTime(s) |\n")
        fout.write("|---|---|---|---|---|---|\n")

        for (algoName, _) in ALGOS:
            tested  = stats_tested[algoName]
            correct = stats_correct[algoName]
            ratio   = 100.0 * correct / tested if tested > 0 else 0.0
            totalT  = stats_time[algoName]  # timp cumulat
            avgT    = totalT / tested if tested > 0 else 0.0
            # afisam totalT si avgT cu 4 zecimale
            fout.write(f"| {algoName} | {tested} | {correct} | {ratio:.1f}% | {avgT:.4f} | {totalT:.4f} |\n")

        fout.write("\nObservatie: Daca un algoritm a depasit 10s, e skip si nu apare in statistici (#Tested).\n")
        fout.write("De asemenea, 'k' e corect daca k == n (chi(K_n)=n).\n")

    print(f"\n=== Raport generat in '{outfname}'. Vizualizeaza-l in Markdown. ===")


if __name__ == "__main__":
    main()
