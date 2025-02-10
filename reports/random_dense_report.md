# Raport Random Dense (p=0.8)

Total fisiere random p0.8: 11

## Tabel cu rezultate

| File | N | Backtracking k | Backtracking time | Backtracking ok | Greedy k | Greedy time | Greedy ok | DSATUR k | DSATUR time | DSATUR ok | WelshPowell k | WelshPowell time | WelshPowell ok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `random_6_p0.8.in` | 6 | 5 | 0.0730s | YES | 5 | 0.0491s | YES | 5 | 0.0528s | YES | 5 | 0.0546s | YES |
| `random_7_p0.8.in` | 7 | 5 | 0.0553s | YES | 5 | 0.0591s | YES | 5 | 0.0515s | YES | 5 | 0.0521s | YES |
| `random_8_p0.8.in` | 8 | 5 | 0.0592s | YES | 5 | 0.0564s | YES | 5 | 0.0508s | YES | 5 | 0.0488s | YES |
| `random_9_p0.8.in` | 9 | 5 | 0.0607s | YES | 5 | 0.0566s | YES | 5 | 0.0556s | YES | 5 | 0.0526s | YES |
| `random_10_p0.8.in` | 10 | 7 | 0.0997s | YES | 7 | 0.0565s | YES | 7 | 0.0529s | YES | 7 | 0.0493s | YES |
| `random_11_p0.8.in` | 11 | 6 | 0.0587s | YES | 6 | 0.0577s | YES | 6 | 0.0499s | YES | 6 | 0.0481s | YES |
| `random_12_p0.8.in` | 12 | 6 | 0.0612s | YES | 7 | 0.0517s | NO | 6 | 0.0537s | YES | 6 | 0.0529s | YES |
| `random_13_p0.8.in` | 13 | 7 | 0.2420s | YES | 7 | 0.0587s | YES | 7 | 0.0527s | YES | 7 | 0.0519s | YES |
| `random_14_p0.8.in` | 14 | 7 | 0.1558s | YES | 7 | 0.0543s | YES | 7 | 0.0522s | YES | 7 | 0.0534s | YES |
| `random_15_p0.8.in` | 15 | 8 | 3.2121s | YES | 8 | 0.0518s | YES | 8 | 0.0507s | YES | 8 | 0.0520s | YES |
| `random_16_p0.8.in` | 16 | 8 | 1.6993s | YES | 9 | 0.0557s | NO | 8 | 0.0542s | YES | 8 | 0.0512s | YES |

## Statistici globale

| Algo | #Tested | #Correct | %Correct | AvgTime | TotalTime |
|---|---|---|---|---|---|
| Backtracking | 11 | 11 | 100.0% | 0.5252 | 5.7769 |
| Greedy | 11 | 9 | 81.8% | 0.0552 | 0.6076 |
| DSATUR | 11 | 11 | 100.0% | 0.0525 | 0.5770 |
| WelshPowell | 11 | 11 | 100.0% | 0.0515 | 0.5668 |

Observatie: Daca backtracking a dat skip => tot fisier skip pt ca gen n avem cum sa stim daca e corect aici daca n avem backtracking
Ceilalti => correct daca k_val == k_ref.
Timeout=40s.
