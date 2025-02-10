import matplotlib.pyplot as plt
# Data
nodes_sparse = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
backtracking_times_sparse = [0.0602, 0.0571, 0.0500, 0.0584, 0.0499, 0.0588, 0.0684, 0.0588, 0.0716, 0.0703, 0.0687]
greedy_times_sparse = [0.0570, 0.0541, 0.0518, 0.0882, 0.0579, 0.0547, 0.0581, 0.0570, 0.0520, 0.0511, 0.0572]
dsatur_times_sparse = [0.0484, 0.0460, 0.0511, 0.0484, 0.0539, 0.0537, 0.0502, 0.0515, 0.0509, 0.0481, 0.0530]
welshpowell_times_sparse = [0.0516, 0.0505, 0.0584, 0.0515, 0.0552, 0.0567, 0.0499, 0.0507, 0.0556, 0.0645, 0.0538]

plt.figure(figsize=(10, 6))

plt.plot(nodes_sparse, backtracking_times_sparse, marker='o', label='Backtracking')
plt.plot(nodes_sparse, greedy_times_sparse, marker='s', label='Greedy')
plt.plot(nodes_sparse, dsatur_times_sparse, marker='^', label='DSATUR')
plt.plot(nodes_sparse, welshpowell_times_sparse, marker='d', label='WelshPowell')

plt.title("Timpul de execuție pentru grafuri sparse (rare)")
plt.xlabel("Numărul de noduri (N)")
plt.ylabel("Timpul de execuție (secunde)")
plt.legend(title="Algoritmi")
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()
