import matplotlib.pyplot as plt

# datele din raport
nodes = [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900]
backtracking_times = [0.0042, 0.0031, 0.0046, 0.0065, 0.0086, 0.0103, 0.0133, 0.0169, 0.0187, 0.0217, 0.0261, 0.0295, 0.0333, 0.0371, 0.0427]
greedy_times = [0.0035, 0.0055, 0.0083, 0.0105, 0.0139, 0.0170, 0.0231, 0.0241, 0.0298, 0.0457, 0.0413, 0.0519, 0.0568, 0.0670, 0.0740]
dsatur_times = [0.0415, 0.0678, 0.1130, 0.1739, 0.2719, 0.3597, 0.4979, 0.6532, 0.8715, 1.1017, 1.3777, 1.7025, 2.0868, 2.6067, 3.2064]
welshpowell_times = [0.0008, 0.0006, 0.0013, 0.0012, 0.0031, 0.0020, 0.0025, 0.0032, 0.0037, 0.0043, 0.0051, 0.0059, 0.0070, 0.0082, 0.0098]

plt.figure(figsize=(10, 6))

plt.plot(nodes, backtracking_times, marker='o', label='Backtracking', color='blue')
plt.plot(nodes, greedy_times, marker='s', label='Greedy', color='orange')
plt.plot(nodes, dsatur_times, marker='^', label='DSATUR', color='green')
plt.plot(nodes, welshpowell_times, marker='d', label='WelshPowell', color='red')

plt.title("Timpul de executie pentru algoritmi pe grafuri bipartite", fontsize=14)
plt.xlabel("Numarul de noduri (N)", fontsize=12)
plt.ylabel("Timpul de executie (secunde)", fontsize=12)
plt.legend(title="Algoritmi")
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()
