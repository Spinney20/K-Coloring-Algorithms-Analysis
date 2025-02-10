#!/usr/bin/env python3
"""
run_planar_report.py

- Cauta DOAR fisiere planar_*.in din folderul 'generated_tests/'.
- Sorteaza fisierele dupa n, extras din numele 'planar_(\\d+)'.
- Ruleaza 4 algoritmi (Backtracking, Greedy, DSATUR, WelshPowell) pe fiecare fisier.
- Parseaza numarul de culori (k) si timpul (time=...) din output.
- Backtracking este considerat referinta (k_ref).
- "Corect" pentru ceilalti => k_val == k_ref.
- Afiseaza un tabel Markdown cu (File, N) si, pentru fiecare algoritm, (k, time, correct).
- Salveaza raportul in 'planar_report.md'.
"""

import os
import re
import subprocess
import sys

# Unde se afla scripturile Python cu algoritmii
SCRIPT_FOLDER = "pythonsrc"

# Unde se afla fisierele planar_*.in
TEST_FOLDER = "generated_tests"

# Patru algoritmi
ALGOS = [
    ("Backtracking",  os.path.join(SCRIPT_FOLDER, "backtracking.py")),
    ("Greedy",        os.path.join(SCRIPT_FOLDER, "greedy.py")),
    ("DSATUR",        os.path.join(SCRIPT_FOLDER, "dsatur.py")),
    ("WelshPowell",   os.path.join(SCRIPT_FOLDER, "welsh_powell.py")),
]

def parse_k_time(stdout):
    """
    Caut in stdout ceva de forma:
       (chi=|used_k=|usedK=)(\\d+)
       time=([\\d\\.]+)
    Returnez (k_val, t_val).
    Daca nu gasesc, pun k_val=-1, t_val=-1.0
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
    Daca fname e gen 'planar_30.in', extrag n=30 prin 'planar_(\\d+)'.
    Daca nu match, intorc 999999 pt sortare la coada.
    """
    m = re.match(r"planar_(\d+)", fname)
    if m:
        return int(m.group(1))
    return 999999

def main():
    # 1) Verific folder
    if not os.path.isdir(TEST_FOLDER):
        print(f"Eroare: folderul '{TEST_FOLDER}' nu exista!")
        sys.exit(1)

    # 2) Adun fisiere planar_*.in
    planar_files = [f for f in os.listdir(TEST_FOLDER)
                    if f.startswith("planar_") and f.endswith(".in")]
    if not planar_files:
        print(f"Nu am gasit fisiere planar_*.in in '{TEST_FOLDER}'!")
        sys.exit(0)

    # sortez dupa n
    planar_files.sort(key=extract_n_from_filename)

    # results[testFile][algoName] = (k, time, correct?)
    results = {}

    # statistici globale
    stats_count   = {a[0]:0 for a in ALGOS}
    stats_correct = {a[0]:0 for a in ALGOS}
    stats_time    = {a[0]:0.0 for a in ALGOS}

    for fname in planar_files:
        path_in = os.path.join(TEST_FOLDER, fname)
        n_val = extract_n_from_filename(fname)
        print(f"\n=== Fisier: {fname} (n={n_val}) ===")

        # Rulam toate algoritmii; dar avem nevoie de backtracking k_ref
        # => rulam in ordinea definita, stocam info
        algo_outputs = {}
        for (algoName, scriptPath) in ALGOS:
            cmd = ["python3", scriptPath, path_in]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            stdout = proc.stdout
            stderr = proc.stderr
            k_val, t_val = parse_k_time(stdout)

            # Afisare scurt
            print(f"  {algoName}: k={k_val}, time={t_val:.4f}s")
            if stderr and stderr.strip():
                print("    [stderr]", stderr.strip())

            algo_outputs[algoName] = (k_val, t_val)

        # Acum preiau k_ref = kVal de la Backtracking
        k_ref, _ = algo_outputs["Backtracking"]

        # Construiesc results dict, calculez correct
        results[fname] = {}
        for (algoName, _) in ALGOS:
            (k_val, t_val) = algo_outputs[algoName]
            # if backtracking are -1 => invalid, dar teoretic backtracking e mereu corect
            # "correct" = (k_val == k_ref)
            correct = (k_val == k_ref and k_val>0)
            results[fname][algoName] = (k_val, t_val, correct)

            # statistici
            stats_count[algoName]+=1
            if correct:
                stats_correct[algoName]+=1
            if t_val>0:
                stats_time[algoName]+= t_val

    # generam planar_report.md
    outfname = "planar_report.md"
    with open(outfname, "w") as fout:
        fout.write("# Raport Grafuri Planare (Backtracking ca referinta)\n\n")
        fout.write("**Backtracking** determina numarul de culori (k_ref). "
                   "Celelalte algoritmii sunt 'corecte' doar daca au acelasi k_val == k_ref.\n\n")

        fout.write("## Tabel cu rezultate\n\n")
        # 2 + (4*3) = 14 coloane
        header = ("| File | N | "
                  "Backtracking k | Backtracking time | Backtracking ok | "
                  "Greedy k | Greedy time | Greedy ok | "
                  "DSATUR k | DSATUR time | DSATUR ok | "
                  "WelshPowell k | WelshPowell time | WelshPowell ok |\n")
        sep = "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        fout.write(header)
        fout.write(sep)

        for fname in planar_files:
            n_val = extract_n_from_filename(fname)
            row = f"| `{fname}` | {n_val} "
            for (algoName, _) in ALGOS:
                (k_val, t_val, correct) = results[fname][algoName]
                c_str = "YES" if correct else "NO"
                row += f"| {k_val} | {t_val:.4f}s | {c_str} "
            row+="|\n"
            fout.write(row)

        # statistici globale
        fout.write("\n## Statistici globale\n\n")
        fout.write("| Algo | #Tests | #Correct | %Correct | AvgTime |\n")
        fout.write("|---|---|---|---|---|\n")

        total_tests = len(planar_files)
        for (algoName, _) in ALGOS:
            tot = stats_count[algoName]
            corr= stats_correct[algoName]
            ratio = 100.0*corr/tot if tot>0 else 0.0
            avgT  = stats_time[algoName]/tot if tot>0 else 0.0
            fout.write(f"| {algoName} | {tot} | {corr} | {ratio:.1f}% | {avgT:.4f}s |\n")

        fout.write("\nObservatie: 'Backtracking ok' este mereu 'YES' daca scriptul il raporteaza cu k_val>0.\n")
        fout.write("Pentru ceilalti, 'YES' doar daca k_val == k_ref (cel de la Backtracking).\n")

    print(f"\n=== Raport generat in '{outfname}'. Vezi tabelul Markdown. ===")


if __name__=="__main__":
    main()
