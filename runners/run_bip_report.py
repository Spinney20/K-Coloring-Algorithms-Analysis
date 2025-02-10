#!/usr/bin/env python3
"""
run_bip_report.py

- Cauta DOAR fisiere bip_*.in din folderul 'generated_tests/'.
- Sorteaza fisierele dupa n, extras din numele 'bip_(\d+)_...'.
- Ruleaza 4 algoritmi (Backtracking, Greedy, DSATUR, WelshPowell) pe fiecare fisier.
- Parsea numarul de culori (k) si timpul (time=...) din output.
- Considera "corect" daca k==2 (pentru bipartite complete cu partite nenule).
- Afiseaza un tabel Markdownsi un rezumat statistic, in fisierul bip_report.md.
"""

import os
import re
import subprocess
import sys

SCRIPT_FOLDER = "pythonsrc"

# Unde se afla fisierele bip_*.in
TEST_FOLDER = "generated_tests"

# Definim cele 4 algoritmi: (NumeDeAfisat, caleSpreScript)
ALGOS = [
    ("Backtracking",  os.path.join(SCRIPT_FOLDER, "backtracking.py")),
    ("Greedy",        os.path.join(SCRIPT_FOLDER, "greedy.py")),
    ("DSATUR",        os.path.join(SCRIPT_FOLDER, "dsatur.py")),
    ("WelshPowell",   os.path.join(SCRIPT_FOLDER, "welsh_powell.py")),
]

def parse_k_time(stdout):
    """
    Cautceva de forma:
       (chi=|used_k=|usedK=)(\d+)
       time=([\d\.]+)
    Returnez (k_val, time_val).
    Daca nu gasesc, pun k_val=-1, time_val=-1.0
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

def extract_n_from_filename(fname):
    """
    Daca fname e gen 'bip_30_15_15.in', extrag n=30 prin 'bip_(\d+)_'.
    Daca nu match, intorc 999999 pt sortare la coada.
    """
    m = re.match(r"bip_(\d+)_", fname)
    if m:
        return int(m.group(1))
    return 999999

def main():
    # Verificam daca folderul TEST_FOLDER exista
    if not os.path.isdir(TEST_FOLDER):
        print(f"Eroare: folderul '{TEST_FOLDER}' nu exista!")
        sys.exit(1)

    # Selectam fisiere bip_*.in
    bip_files = [f for f in os.listdir(TEST_FOLDER)
                 if f.startswith("bip_") and f.endswith(".in")]
    if not bip_files:
        print(f"Nu am gasit fisiere bip_*.in in '{TEST_FOLDER}'!")
        sys.exit(0)

    # Sortam dupa n (extras din bip_(\d+)_)
    bip_files.sort(key=extract_n_from_filename)

    # Rezultate: results[testFile][algoName] = (k, time, correct)
    results = {}
    # Statistici globale
    stats_count = {}
    stats_correct= {}
    stats_time = {}
    for (algoName, _) in ALGOS:
        stats_count[algoName] = 0
        stats_correct[algoName] = 0
        stats_time[algoName] = 0.0

    # Rulare
    for fname in bip_files:
        path_in = os.path.join(TEST_FOLDER, fname)
        n_val = extract_n_from_filename(fname)
        print(f"\n=== Fisier: {fname} (n={n_val}) ===")
        results[fname] = {}

        for (algoName, scriptPath) in ALGOS:
            cmd = ["python3", scriptPath, path_in]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            stdout = proc.stdout
            stderr = proc.stderr

            k_val, t_val = parse_k_time(stdout)
            correct = (k_val == 2)  # bip complet => chi=2

            results[fname][algoName] = (k_val, t_val, correct)

            stats_count[algoName]+=1
            if correct:
                stats_correct[algoName]+=1
            if t_val>0:
                stats_time[algoName]+= t_val

            # Afisare scurta
            print(f"  {algoName}: k={k_val}, time={t_val:.4f}s, correct={correct}")
            if stderr and stderr.strip():
                print("  [stderr]", stderr.strip())

    # Generam un raport Markdown
    outfname = "bip_report.md"
    with open(outfname, "w") as fout:
        fout.write("# Raport Grafuri Bipartite\n\n")

        fout.write("## Tabel cu rezultate (tip matrice)\n\n")
        # Antet de coloane grupate
        header = "| File | N | Backtracking k | Backtracking time | Backtracking correct | Greedy k | Greedy time | Greedy correct | DSATUR k | DSATUR time | DSATUR correct | WelshPowell k | WelshPowell time | WelshPowell correct |\n"
        sep = "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        fout.write(header)
        fout.write(sep)

        for fname in bip_files:
            n_val = extract_n_from_filename(fname)
            row = f"| {fname} | {n_val} "
            for (algoName, _) in ALGOS:
                k_val, t_val, correct = results[fname][algoName]
                correct_str = "YES" if correct else "NO"
                row += f"| {k_val} | {t_val:.4f}s | {correct_str} "
            row += "|\n"
            fout.write(row)

        fout.write("\n## Statistici globale\n\n")
        # AM ADUGAT MAI JOS COLOANA TOTAL TIME DUPA AVG TIME
        fout.write("| Algo | #Tests | #Correct | %Correct | AvgTime | TotalTime |\n")
        fout.write("|---|---|---|---|---|---|\n")
        for (algoName, _) in ALGOS:
            tot = stats_count[algoName]
            corr= stats_correct[algoName]
            ratio = 100.0*corr/tot if tot>0 else 0.0
            avgT  = stats_time[algoName]/tot if tot>0 else 0.0
            totalT = stats_time[algoName]
            fout.write(f"| {algoName} | {tot} | {corr} | {ratio:.1f}% | {avgT:.4f}s | {totalT:.4f}s |\n")

        fout.write("\n*Observatie*: Consideram \"corect\" daca nr de culori = 2.\n")

    print(f"\n=== Raport generat in '{outfname}'. Vezi tabelul Markdown. ===")


if __name__=="__main__":
    main()
