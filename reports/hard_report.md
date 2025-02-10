# Raport SHC/HC (Hard to Color) – Stil Chordal

Total fisiere: 5

## Tabel cu rezultate

| File | n | chi | Backtracking k | B.time | B.ok | Greedy k | G.time | G.ok | DSATUR k | D.time | D.ok | WelshPowell k | W.time | W.ok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `hc_dsatur.in` | 8 | 3 | 4 | 0.0431s | YES | 4 | 0.0565s | NO | 4 | 0.0504s | NO | 4 | 0.0492s | NO |
| `shc_1.in` | 5 | 3 | 3 | 0.0402s | YES | 3 | 0.0521s | YES | 3 | 0.0642s | YES | 3 | 0.0495s | YES |
| `shc_2.in` | 6 | 3 | 3 | 0.0435s | YES | 3 | 0.0487s | NO | 3 | 0.0507s | YES | 4 | 0.0465s | NO |
| `shc_3.in` | 5 | 3 | 3 | 0.0497s | YES | 3 | 0.0486s | NO | 3 | 0.0501s | YES | 3 | 0.0547s | YES |
| `shc_dsatur.in` | 6 | 3 | 3 | 0.0464s | YES | 3 | 0.0576s | NO | 3 | 0.0489s | NO | 3 | 0.0454s | NO |

## Statistici globale

| Algo | #Tested | #Correct | %Correct | AvgTime |
|---|---|---|---|---|
| Backtracking | 5 | 5 | 80.0% | 0.0446 |
| Greedy | 5 | 1 | 20.0% | 0.0527 |
| DSATUR | 5 | 3 | 60.0% | 0.0529 |
| WelshPowell | 5 | 2 | 40.0% | 0.0491 |

Observatie:
- Timeout=40s => skip.
- 'k' e corect daca k==chi, stabilit manual in CHI_MAP.
