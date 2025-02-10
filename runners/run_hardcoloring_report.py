#!/usr/bin/env python3
"""
run_hard_report.py

- Caută DOAR fiierele SHC/HC (create manual) in 'generated_tests/':
    shc_1.in, shc_2.in, shc_3.in, shc_dsatur.in, hc_dsatur.in
- Pentru fiecare, avem deja un numar cromatic "corect" (chi) predefinit.
- Ruleaza 4 algoritmi (Backtracking, Greedy, DSATUR, WelshPowell) cu timeout=40s:
   daca un algoritm sare de 40s => skip => nu-l includ in statistici.
- Comparam k_val cu chi => correct / not.
- Tabel tip matrice + un rezumat final, EXACT ca la chordal_report.
"""

import os
import sys
import re
import subprocess
import time

SCRIPT_FOLDER = "pythonsrc"
TEST_FOLDER   = "generated_tests"
MAX_TIME      = 40.0

ALGOS = [
    ("Backtracking",  os.path.join(SCRIPT_FOLDER, "backtracking.py")),
    ("Greedy",        os.path.join(SCRIPT_FOLDER, "greedy.py")),
    ("DSATUR",        os.path.join(SCRIPT_FOLDER, "dsatur.py")),
    ("WelshPowell",   os.path.join(SCRIPT_FOLDER, "welsh_powell.py")),
]

# Harta cu fișiere (nume) -> chi real
#   - conform exemplului manual:
#      shc_1.in => chi=3
#      shc_2.in => chi=3
#      shc_3.in => chi=3
#      shc_dsatur.in => chi=3
#      hc_dsatur.in => chi=3
CHI_MAP = {
    "shc_1.in": 3,
    "shc_2.in": 3,
    "shc_3.in": 3,
    "shc_dsatur.in": 3,
    "hc_dsatur.in": 3,
}

def parse_k_time(stdout):
    """
    Caut in stdout ceva de forma:
       (chi=|used_k=|usedK=)(\d+)
       time=([\d\.]+)
    Return (k_val, t_val), altfel (-1, -1).
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

def read_infile_n(path):
    """
    Pentru a n, extragem primele linii (n, m).
    SHC/HC :
      n m
      ...
    Returnez n.
    """
    with open(path,"r") as f:
        line= f.readline().strip()
        n,m = map(int,line.split())
    return n

def main():
    if not os.path.isdir(TEST_FOLDER):
        print(f"Folder '{TEST_FOLDER}' nu exista.")
        sys.exit(1)

    all_files = os.listdir(TEST_FOLDER)
    # DOAR fisierele din CHI_MAP
    # adica "shc_1.in", "shc_2.in", "shc_3.in", "shc_dsatur.in", "hc_dsatur.in"
    hard_files = [f for f in all_files if f in CHI_MAP.keys()]

    if not hard_files:
        print("Nu am  SHC/HC in CHI_MAP in folder!")
        sys.exit(0)

    hard_files.sort()  # sort lexic, sau cum vrei

    # results[fname][algoName] = {k, time, correct, skip}
    results = {}
    stats_tests_total=0
    stats_tested   = {a[0]:0 for a in ALGOS}
    stats_correct  = {a[0]:0 for a in ALGOS}
    stats_time     = {a[0]:0.0 for a in ALGOS}

    for fname in hard_files:
        path_in= os.path.join(TEST_FOLDER, fname)
        n_val= read_infile_n(path_in)
        chi_ref= CHI_MAP[fname]

        stats_tests_total+=1
        print(f"\n=== Fisier: {fname} => n={n_val}, chi_ref={chi_ref} ===")

        results[fname]={
            "n": n_val,
            "chi": chi_ref,
            "algos": {}
        }

        for (algoName, scriptPath) in ALGOS:
            cmd= ["python3", scriptPath, path_in]
            try:
                st= time.perf_counter()
                proc= subprocess.run(cmd, capture_output=True, text=True, timeout=MAX_TIME)
                en= time.perf_counter()
                dur= en-st

                k_val, t_val= parse_k_time(proc.stdout)
                skip_= False
                correct_= (k_val==chi_ref)

                results[fname]["algos"][algoName]={
                    "k":k_val, "time":dur, "correct":correct_, "skip":False
                }
                # statistici
                stats_tested[algoName]+=1
                if correct_:
                    stats_correct[algoName]+=1
                stats_time[algoName]+= dur

                print(f"  {algoName}: k={k_val}, time={dur:.4f}s => correct={correct_}")
                se= proc.stderr
                if se and se.strip():
                    print("   [stderr]:", se.strip())

            except subprocess.TimeoutExpired:
                print(f"  {algoName}: TIMEOUT => skip")
                results[fname]["algos"][algoName]={
                    "k":-1, "time":MAX_TIME, "correct":False, "skip":True
                }
                # nu incrementam stats

    # generam hard_report.md
    outfname="hard_report.md"
    with open(outfname,"w") as fout:
        fout.write("# Raport SHC/HC (Hard to Color) – Stil Chordal\n\n")
        fout.write(f"Total fisiere: {stats_tests_total}\n\n")
        fout.write("## Tabel cu rezultate\n\n")

        # 3 col => File, n, chi => plus 4*(k,time,ok)=12 => total 15
        header=("| File | n | chi | "
                "Backtracking k | B.time | B.ok | "
                "Greedy k | G.time | G.ok | "
                "DSATUR k | D.time | D.ok | "
                "WelshPowell k | W.time | W.ok |\n")
        col_count=3 + 4*3
        sep= "|" + ("---|"*col_count)+"\n"
        fout.write(header)
        fout.write(sep)

        for fname in hard_files:
            n_ = results[fname]["n"]
            c_ = results[fname]["chi"]
            row= f"| `{fname}` | {n_} | {c_} "

            for (algoName,_) in ALGOS:
                ad= results[fname]["algos"][algoName]
                if ad["skip"]:
                    row+= f"| - | >{MAX_TIME}s | skip "
                else:
                    kk= ad["k"]
                    tm= ad["time"]
                    corr= ad["correct"]
                    cstr= "YES" if corr else "NO"
                    row+= f"| {kk} | {tm:.4f}s | {cstr} "
            row+="|\n"
            fout.write(row)

        # statistici
        fout.write("\n## Statistici globale\n\n")
        fout.write("| Algo | #Tested | #Correct | %Correct | AvgTime |\n")
        fout.write("|---|---|---|---|---|\n")

        for (algoName,_) in ALGOS:
            tested= stats_tested[algoName]
            corr= stats_correct[algoName]
            ratio= 100.0*corr/tested if tested>0 else 0.0
            avgT= stats_time[algoName]/tested if tested>0 else 0.0
            fout.write(f"| {algoName} | {tested} | {corr} | {ratio:.1f}% | {avgT:.4f} |\n")

        fout.write("\nObservatie:\n")
        fout.write("- Timeout=40s => skip.\n")
        fout.write("- 'k' e corect daca k==chi, stabilit manual in CHI_MAP.\n")

    print(f"\n=== Raport salvat in '{outfname}'. ===")

if __name__=="__main__":
    main()
