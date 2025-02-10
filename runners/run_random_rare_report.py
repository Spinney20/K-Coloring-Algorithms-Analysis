#!/usr/bin/env python3
"""
run_random_rare_report.py

- Cauta DOAR fisiere random_*.in care contin '_p0.3.in' (sau '_p0.2.in',
  modifici regex) in folderul 'generated_tests/' => 'rare' graphs.
- Foloseste Backtracking ca referinta pentru #culori (k_ref).
- Daca Backtracking depaseste 40s => fisier skip complet (nicio statistica).
- Pentru ceilalti algoritmi, "correct" daca k_val == k_ref.
- Genereaza un raport Markdown random_rare_report.md + statistici globale + total time.
"""

import os
import re
import subprocess
import sys
import time

SCRIPT_FOLDER = "pythonsrc"
TEST_FOLDER   = "generated_tests"

MAX_TIME = 40.0

ALGOS = [
    ("Backtracking",  os.path.join(SCRIPT_FOLDER, "backtracking.py")),
    ("Greedy",        os.path.join(SCRIPT_FOLDER, "greedy.py")),
    ("DSATUR",        os.path.join(SCRIPT_FOLDER, "dsatur.py")),
    ("WelshPowell",   os.path.join(SCRIPT_FOLDER, "welsh_powell.py")),
]

def parse_k_time(stdout):
    k_pat = re.search(r"(?:chi=|used_k=|usedK=)(\d+)", stdout)
    t_pat = re.search(r"time=([\d\.]+)", stdout)
    k_val = int(k_pat.group(1)) if k_pat else -1
    t_val = float(t_pat.group(1)) if t_pat else -1.0
    return k_val, t_val

def extract_n(filename):
    # exemplu: random_30_p0.3.in => caut "random_(\d+)_p0.3"
    # daca nu match, pun n=999999
    m = re.search(r"random_(\d+)_p0\.3", filename)
    if m:
        return int(m.group(1))
    return 999999

def main():
    if not os.path.isdir(TEST_FOLDER):
        print(f"Folderul {TEST_FOLDER} nu exista.")
        sys.exit(1)

    # Colectam random_*.in cu "_p0.3.in"
    all_files = os.listdir(TEST_FOLDER)
    rare_files = [f for f in all_files if f.startswith("random_") and "_p0.3.in" in f]
    if not rare_files:
        print("Nu exista fisiere random_..._p0.3.in in folder!")
        sys.exit(0)

    # sortam dupa n
    rare_files.sort(key=extract_n)

    # results[f][algo] = {k, time, correct, skip}
    results = {}
    stats_tests_total = 0
    stats_tested   = {a[0]:0 for a in ALGOS}
    stats_correct  = {a[0]:0 for a in ALGOS}
    stats_time     = {a[0]:0.0 for a in ALGOS}

    for fname in rare_files:
        path_in = os.path.join(TEST_FOLDER, fname)
        # incerc extrag n
        n_val = extract_n(fname)
        stats_tests_total +=1
        results[fname] = {"n": n_val, "algos": {}, "backtracking_k": -1, "skipAll": False}

        print(f"\n=== Fisier: {fname} (n={n_val}) ===")

        # 1) rulez backtracking
        b_cmd = ["python3", os.path.join(SCRIPT_FOLDER, "backtracking.py"), path_in]
        try:
            start_t = time.perf_counter()
            proc = subprocess.run(b_cmd, capture_output=True, text=True, timeout=MAX_TIME)
            end_t   = time.perf_counter()
            dur = end_t - start_t
            b_stdout = proc.stdout
            b_stderr = proc.stderr
            bk_val, bt_val = parse_k_time(b_stdout)
            # daca bk_val<0 => ceva eroare => skip
            if bk_val<1:
                print("  [Backtracking] invalid k => skip complet")
                results[fname]["skipAll"] = True
                continue  # merg la urm fisier
            # altfel
            print(f"  Backtracking: k={bk_val}, time={dur:.2f}s")
            if b_stderr and b_stderr.strip():
                print("   [stderr]:", b_stderr.strip())

            # setez in results
            results[fname]["backtracking_k"] = bk_val
            # retin in struct
            results[fname]["algos"]["Backtracking"] = {
                "k":bk_val,"time":dur,"correct":True,"skip":False
            }
            # stats backtracking
            stats_tested["Backtracking"]+=1
            stats_correct["Backtracking"]+=1  # consideram backtracking mereu "correct"
            stats_time["Backtracking"] += dur

        except subprocess.TimeoutExpired:
            print(f"  Backtracking TIMEOUT > {MAX_TIME}s => skip complet.")
            results[fname]["skipAll"] = True
            continue  # la urm fisier

        # 2) rulez ceilalti 3 daca skipAll e False
        if results[fname]["skipAll"]:
            continue

        k_ref = results[fname]["backtracking_k"]
        for algoName, scriptPath in ALGOS:
            if algoName=="Backtracking":
                continue  # deja rulat
            cmd = ["python3", scriptPath, path_in]
            try:
                stt = time.perf_counter()
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=MAX_TIME)
                endt= time.perf_counter()
                durr = endt - stt
                so = proc.stdout
                se = proc.stderr
                kk_val, ttt_val = parse_k_time(so)
                corr = (kk_val==k_ref and kk_val>0)
                # salvam
                results[fname]["algos"][algoName] = {
                    "k":kk_val,"time":durr,"correct":corr,"skip":False
                }
                stats_tested[algoName]+=1
                if corr:
                    stats_correct[algoName]+=1
                stats_time[algoName]+= durr

                print(f"  {algoName}: k={kk_val}, time={durr:.2f}s, correct={corr}")
                if se and se.strip():
                    print("   [stderr]:", se.strip())

            except subprocess.TimeoutExpired:
                print(f"  {algoName}: TIMEOUT => skip")
                results[fname]["algos"][algoName] = {
                    "k":-1,"time":MAX_TIME,"correct":False,"skip":True
                }
                # nu-l pun la stats

    # 3) generam raport => random_rare_report.md
    outfname = "random_rare_report.md"
    with open(outfname,"w") as fout:
        fout.write("# Raport Random Rare (p=0.3) \n\n")
        fout.write(f"Total fisiere random p0.3: {stats_tests_total}\n\n")

        fout.write("## Tabel cu rezultate\n\n")
        # 2 col (File,n) + 4*(k,time,ok)=12 => total 14 coloane
        header = ("| File | N | "
                  "Backtracking k | Backtracking time | Backtracking ok | "
                  "Greedy k | Greedy time | Greedy ok | "
                  "DSATUR k | DSATUR time | DSATUR ok | "
                  "WelshPowell k | WelshPowell time | WelshPowell ok |\n")
        col_count = 2 + 4*3
        sep = "|" + ("---|"*col_count) + "\n"
        fout.write(header)
        fout.write(sep)

        for fname in rare_files:
            info = results[fname]
            n_val= info["n"]
            skipAll= info["skipAll"]
            row = f"| `{fname}` | {n_val} "

            if skipAll:
                # backtracking a dat skip, pun un row "skip" pt. tot
                row += " | - | >40s | skip " * 4
                row += "|\n"
                fout.write(row)
                continue

            # altfel
            # backtracking
            bdata = info["algos"].get("Backtracking",None)
            if bdata is None or bdata["skip"]:
                row+="| - | >40s | skip "
            else:
                bk=bdata["k"]
                bt=bdata["time"]
                row+=f"| {bk} | {bt:.4f}s | YES "  # backtracking e mereu "YES"

            # greedy
            gdata = info["algos"].get("Greedy",None)
            if (not gdata) or gdata["skip"]:
                row+="| - | >40s | skip "
            else:
                kk=gdata["k"]
                dd=gdata["time"]
                cc=gdata["correct"]
                cstr = "YES" if cc else "NO"
                row+= f"| {kk} | {dd:.4f}s | {cstr} "

            # dsatur
            ddata = info["algos"].get("DSATUR",None)
            if (not ddata) or ddata["skip"]:
                row+="| - | >40s | skip "
            else:
                kk=ddata["k"]
                dd=ddata["time"]
                cc=ddata["correct"]
                cstr = "YES" if cc else "NO"
                row+= f"| {kk} | {dd:.4f}s | {cstr} "

            # welsh
            wdata = info["algos"].get("WelshPowell",None)
            if (not wdata) or wdata["skip"]:
                row+="| - | >40s | skip "
            else:
                kk=wdata["k"]
                dd=wdata["time"]
                cc=wdata["correct"]
                cstr = "YES" if cc else "NO"
                row+= f"| {kk} | {dd:.4f}s | {cstr} "

            row+="|\n"
            fout.write(row)

        fout.write("\n## Statistici globale\n\n")
        fout.write("| Algo | #Tested | #Correct | %Correct | AvgTime | TotalTime |\n")
        fout.write("|---|---|---|---|---|---|\n")

        for (algoName,_) in ALGOS:
            tested = stats_tested[algoName]
            corr   = stats_correct[algoName]
            ratio  = 100.0*corr/tested if tested>0 else 0.0
            totalT = stats_time[algoName]
            avgT   = totalT/tested if tested>0 else 0.0
            fout.write(f"| {algoName} | {tested} | {corr} | {ratio:.1f}% | {avgT:.4f} | {totalT:.4f} |\n")

        fout.write("\nObservatie: Daca backtracking a dat skip => fisier skip pt toti.\n")
        fout.write("Algoritm=YES daca k == k_ref (cel gasit de backtracking).\n")
        fout.write("Timeout=40s.\n")

    print(f"\n=== Raport generat in '{outfname}'. ===")


if __name__=="__main__":
    main()
