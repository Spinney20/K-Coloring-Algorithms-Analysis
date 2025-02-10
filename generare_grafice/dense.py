import matplotlib.pyplot as plt

# Data
nodes_dense = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
backtracking_times_dense = [0.0730, 0.0553, 0.0592, 0.0607, 0.0997, 0.0587, 0.0612, 0.2420, 0.1558, 3.2121, 1.6993]
greedy_times_dense = [0.0491, 0.0591, 0.0564, 0.0566, 0.0565, 0.0577, 0.0517, 0.0587, 0.0543, 0.0518, 0.0557]
dsatur_times_dense = [0.0528, 0.0515, 0.0508, 0.0556, 0.0529, 0.0499, 0.0537, 0.0527, 0.0522, 0.0507, 0.0542]
welshpowell_times_dense = [0.0546, 0.0521, 0.0488, 0.0526, 0.0493, 0.0481, 0.0529, 0.0519, 0.0534, 0.0520, 0.0512]

plt.figure(figsize=(10, 6))

plt.plot(nodes_dense, backtracking_times_dense, marker='o', label='Backtracking')
plt.plot(nodes_dense, greedy_times_dense, marker='s', label='Greedy')
plt.plot(nodes_dense, dsatur_times_dense, marker='^', label='DSATUR')
plt.plot(nodes_dense, welshpowell_times_dense, marker='d', label='WelshPowell')

plt.title("Timpul de execuție pentru grafuri dense random", fontsize=14)
plt.xlabel("Numărul de noduri (N)", fontsize=12)
plt.ylabel("Timpul de execuție (secunde)", fontsize=12)
plt.legend(title="Algoritmi")
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()
