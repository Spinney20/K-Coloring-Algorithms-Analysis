# Raport Grafuri Planare (Backtracking ca referință)

**Backtracking** determină numărul de culori (k_ref). Celelalte algoritmii sunt 'corecte' doar dacă au același k_val == k_ref.

## Tabel cu rezultate

| File | N | Backtracking k | Backtracking time | Backtracking ok | Greedy k | Greedy time | Greedy ok | DSATUR k | DSATUR time | DSATUR ok | WelshPowell k | WelshPowell time | WelshPowell ok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `planar_20.in` | 20 | 2 | 0.0000s | YES | 2 | 0.0000s | YES | 2 | 0.0001s | YES | 2 | 0.0000s | YES |
| `planar_100.in` | 100 | 2 | 0.0004s | YES | 4 | 0.0002s | NO | 2 | 0.0002s | YES | 2 | 0.0000s | YES |
| `planar_200.in` | 200 | 2 | 0.0013s | YES | 4 | 0.0003s | NO | 2 | 0.0004s | YES | 2 | 0.0001s | YES |
| `planar_300.in` | 300 | 2 | 0.0030s | YES | 4 | 0.0005s | NO | 2 | 0.0010s | YES | 2 | 0.0001s | YES |
| `planar_400.in` | 400 | 2 | 0.0061s | YES | 4 | 0.0010s | NO | 2 | 0.0012s | YES | 2 | 0.0001s | YES |
| `planar_500.in` | 500 | 2 | 0.0089s | YES | 5 | 0.0010s | NO | 2 | 0.0021s | YES | 2 | 0.0001s | YES |
| `planar_600.in` | 600 | 2 | 0.0128s | YES | 4 | 0.0010s | NO | 2 | 0.0012s | YES | 2 | 0.0002s | YES |
| `planar_700.in` | 700 | 2 | 0.0181s | YES | 4 | 0.0012s | NO | 2 | 0.0013s | YES | 2 | 0.0002s | YES |
| `planar_800.in` | 800 | 2 | 0.0242s | YES | 4 | 0.0014s | NO | 2 | 0.0020s | YES | 2 | 0.0002s | YES |
| `planar_900.in` | 900 | 2 | 0.0340s | YES | 4 | 0.0016s | NO | 2 | 0.0017s | YES | 2 | 0.0002s | YES |

## Statistici globale

| Algo | #Tests | #Correct | %Correct | AvgTime |
|---|---|---|---|---|
| Backtracking | 10 | 10 | 100.0% | 0.0109s |
| Greedy | 10 | 1 | 10.0% | 0.0008s |
| DSATUR | 10 | 10 | 100.0% | 0.0011s |
| WelshPowell | 10 | 10 | 100.0% | 0.0001s |

Observatie: 'Backtracking ok' este mereu 'YES' dacă scriptul îl raportează cu k_val>0 si <= 4, dar mereu e ok oricum
Pentru ceilalti, 'YES' doar daca k_val == k_ref (cel de la Backtracking).
