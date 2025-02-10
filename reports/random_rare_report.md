# Raport Random Rare (p=0.3) 

Total fisiere random p0.3: 11

## Tabel cu rezultate

| File | N | Backtracking k | Backtracking time | Backtracking ok | Greedy k | Greedy time | Greedy ok | DSATUR k | DSATUR time | DSATUR ok | WelshPowell k | WelshPowell time | WelshPowell ok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `random_6_p0.3.in` | 6 | 3 | 0.0602s | YES | 3 | 0.0570s | YES | 3 | 0.0484s | YES | 3 | 0.0516s | YES |
| `random_7_p0.3.in` | 7 | 3 | 0.0571s | YES | 3 | 0.0541s | YES | 3 | 0.0460s | YES | 3 | 0.0505s | YES |
| `random_8_p0.3.in` | 8 | 3 | 0.0500s | YES | 3 | 0.0518s | YES | 3 | 0.0511s | YES | 3 | 0.0584s | YES |
| `random_9_p0.3.in` | 9 | 4 | 0.0584s | YES | 4 | 0.0882s | YES | 4 | 0.0484s | YES | 4 | 0.0515s | YES |
| `random_10_p0.3.in` | 10 | 4 | 0.0499s | YES | 4 | 0.0579s | YES | 4 | 0.0539s | YES | 4 | 0.0552s | YES |
| `random_11_p0.3.in` | 11 | 3 | 0.0588s | YES | 3 | 0.0547s | YES | 3 | 0.0537s | YES | 3 | 0.0567s | YES |
| `random_12_p0.3.in` | 12 | 4 | 0.0684s | YES | 4 | 0.0581s | YES | 4 | 0.0502s | YES | 4 | 0.0499s | YES |
| `random_13_p0.3.in` | 13 | 4 | 0.0588s | YES | 4 | 0.0570s | YES | 4 | 0.0515s | YES | 4 | 0.0507s | YES |
| `random_14_p0.3.in` | 14 | 3 | 0.0716s | YES | 4 | 0.0520s | NO | 3 | 0.0509s | YES | 4 | 0.0556s | NO |
| `random_15_p0.3.in` | 15 | 4 | 0.0703s | YES | 4 | 0.0511s | YES | 4 | 0.0481s | YES | 5 | 0.0645s | NO |
| `random_16_p0.3.in` | 16 | 3 | 0.0687s | YES | 3 | 0.0572s | YES | 3 | 0.0530s | YES | 3 | 0.0538s | YES |

## Statistici globale

| Algo | #Tested | #Correct | %Correct | AvgTime | TotalTime |
|---|---|---|---|---|---|
| Backtracking | 11 | 11 | 100.0% | 0.0611 | 0.6721 |
| Greedy | 11 | 10 | 90.9% | 0.0581 | 0.6391 |
| DSATUR | 11 | 11 | 100.0% | 0.0505 | 0.5554 |
| WelshPowell | 11 | 9 | 81.8% | 0.0544 | 0.5985 |

Observatie: Daca backtracking a dat skip => fisier skip pt toti.
Algoritm=YES daca k == k_ref (cel gasit de backtracking).
Timeout=40s.
