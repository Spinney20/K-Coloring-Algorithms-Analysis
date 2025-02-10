#!/usr/bin/env python3
"""
run_random_dense_report.py

- Cauta fisiere random_..._p0.8.in => grafuri random dense (p=0.8).
- Restul logicii e identic cu run_random_rare_report.py:
  - Foloseste backtracking ca referinta, skip tot fisierul daca backtracking e Timeout/invalid.
  - Se considera "YES" daca k_val == k_ref.
  - Timp limitat la 40s.
  - Raport final in random_dense_report.md
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
    # Ex: random_30_p0.8.in => caut "random_(\d+)_p0\.8"
    m = re.search(r"random_(\d+)_p0\.8", filename)
    if m:
        return int(m.group(1))
    return 999999

def main():
    if not os.path.isdir(TEST_FOLDER):
        print(f"Folderul {TEST_FOLDER} nu exista.")
        sys.exit(1)

    all_files = os.listdir(TEST_FOLDER)
    dense_files = [f for f in all_files if f.startswith("random_") and "_p0.8.in" in f]
    if not dense_files:
        print("Nu exista fisiere random_..._p0.8.in in folder!")
        sys.exit(0)

    dense_files.sort(key=extract_n)

    results = {}
    stats_tests_total = 0
    stats_tested   = {a[0]:0 for a in ALGOS}
    stats_correct  = {a[0]:0 for a in ALGOS}
    stats_time     = {a[0]:0.0 for a in ALGOS}

    for fname in dense_files:
        path_in = os.path.join(TEST_FOLDER, fname)
        n_val = extract_n(fname)
        stats_tests_total +=1
        results[fname] = {"n": n_val, "algos": {}, "backtracking_k": -1, "skipAll": False}

        print(f"\n=== Fisier: {fname} (n={n_val}) ===")

        # Backtracking
        b_cmd = ["python3", os.path.join(SCRIPT_FOLDER, "backtracking.py"), path_in]
        try:
            st = time.perf_counter()
            proc = subprocess.run(b_cmd, capture_output=True, text=True, timeout=MAX_TIME)
            en = time.perf_counter()
            dur = en - st
            so = proc.stdout
            se = proc.stderr
            bk_val, bt_val = parse_k_time(so)

            if bk_val<1:
                print("  [Backtracking] invalid => skipAll")
                results[fname]["skipAll"] = True
                continue

            print(f"  Backtracking: k={bk_val}, time={dur:.4f}s")
            if se and se.strip():
                print("   [stderr]:", se.strip())

            results[fname]["backtracking_k"] = bk_val
            results[fname]["algos"]["Backtracking"] = {
                "k":bk_val,"time":dur,"correct":True,"skip":False
            }
            stats_tested["Backtracking"]+=1
            stats_correct["Backtracking"]+=1
            stats_time["Backtracking"]+=dur

        except subprocess.TimeoutExpired:
            print("  Backtracking TIMEOUT => skipAll")
            results[fname]["skipAll"] = True
            continue

        if results[fname]["skipAll"]:
            continue

        k_ref = bk_val

        # Ceilalti
        for (algoName,scriptPath) in ALGOS:
            if algoName=="Backtracking":
                continue
            cmd = ["python3", scriptPath, path_in]
            try:
                stt = time.perf_counter()
                prc = subprocess.run(cmd, capture_output=True, text=True, timeout=MAX_TIME)
                enn= time.perf_counter()
                durr = enn-stt
                so2 = prc.stdout
                se2 = prc.stderr
                kk_val, ttt_val = parse_k_time(so2)
                corr = (kk_val==k_ref and kk_val>0)

                results[fname]["algos"][algoName] = {
                    "k":kk_val,"time":durr,"correct":corr,"skip":False
                }
                stats_tested[algoName]+=1
                if corr:
                    stats_correct[algoName]+=1
                stats_time[algoName]+= durr

                print(f"  {algoName}: k={kk_val}, time={durr:.4f}s, correct={corr}")
                if se2 and se2.strip():
                    print("   [stderr]:", se2.strip())

            except subprocess.TimeoutExpired:
                print(f"  {algoName}: TIMEOUT => skip")
                results[fname]["algos"][algoName] = {
                    "k":-1,"time":MAX_TIME,"correct":False,"skip":True
                }
                # no stats

    # generam raport random_dense_report.md
    outfname="random_dense_report.md"
    with open(outfname,"w") as fout:
        fout.write("# Raport Random Dense (p=0.8)\n\n")
        fout.write(f"Total fisiere random p0.8: {stats_tests_total}\n\n")
        fout.write("## Tabel cu rezultate\n\n")

        header = ("| File | N | "
                  "Backtracking k | Backtracking time | Backtracking ok | "
                  "Greedy k | Greedy time | Greedy ok | "
                  "DSATUR k | DSATUR time | DSATUR ok | "
                  "WelshPowell k | WelshPowell time | WelshPowell ok |\n")
        col_count = 2 + 4*3
        sep = "|" + ("---|"*col_count) + "\n"
        fout.write(header)
        fout.write(sep)

        for fname in dense_files:
            info= results[fname]
            n_val= info["n"]
            skipA= info["skipAll"]
            row = f"| `{fname}` | {n_val} "

            if skipA:
                row+="| - | >40s | skip "*4
                row+="|\n"
                fout.write(row)
                continue

            # backtracking
            bdata= info["algos"].get("Backtracking",None)
            if not bdata or bdata["skip"]:
                row+="| - | >40s | skip "
            else:
                k_= bdata["k"]
                t_= bdata["time"]
                row+=f"| {k_} | {t_:.4f}s | YES "

            # greedy
            gdata= info["algos"].get("Greedy",None)
            if not gdata or gdata["skip"]:
                row+="| - | >40s | skip "
            else:
                k_= gdata["k"]
                t_= gdata["time"]
                c_= gdata["correct"]
                cstr="YES" if c_ else "NO"
                row+= f"| {k_} | {t_:.4f}s | {cstr} "

            # dsatur
            ddata= info["algos"].get("DSATUR",None)
            if not ddata or ddata["skip"]:
                row+="| - | >40s | skip "
            else:
                k_= ddata["k"]
                t_= ddata["time"]
                c_= ddata["correct"]
                cstr="YES" if c_ else "NO"
                row+= f"| {k_} | {t_:.4f}s | {cstr} "

            # welsh
            wdata= info["algos"].get("WelshPowell",None)
            if not wdata or wdata["skip"]:
                row+="| - | >40s | skip "
            else:
                k_= wdata["k"]
                t_= wdata["time"]
                c_= wdata["correct"]
                cstr="YES" if c_ else "NO"
                row+= f"| {k_} | {t_:.4f}s | {cstr} "

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

        fout.write("\nObservatie: Daca backtracking a dat skip => tot fisier skip.\n")
        fout.write("Ceilalti => correct daca k_val == k_ref.\nTimeout=40s.\n")

    print(f"\n=== Raport salvat in {outfname}. ===")


if __name__=="__main__":
    main()
