import matplotlib.pyplot as plt

#Data
nodes_planar = [20, 100, 200, 300, 400, 500, 600, 700, 800, 900]
backtracking_times_planar = [0.0000, 0.0004, 0.0013, 0.0030, 0.0061, 0.0089, 0.0128, 0.0181, 0.0242, 0.0340]
greedy_times_planar = [0.0000, 0.0002, 0.0003, 0.0005, 0.0010, 0.0010, 0.0010, 0.0012, 0.0014, 0.0016]
dsatur_times_planar = [0.0001, 0.0002, 0.0004, 0.0010, 0.0012, 0.0021, 0.0012, 0.0013, 0.0020, 0.0017]
welshpowell_times_planar = [0.0000, 0.0000, 0.0001, 0.0001, 0.0001, 0.0001, 0.0002, 0.0002, 0.0002, 0.0002]

plt.figure(figsize=(10, 6))

plt.plot(nodes_planar, backtracking_times_planar, marker='o', label='Backtracking', color='blue')
plt.plot(nodes_planar, greedy_times_planar, marker='s', label='Greedy', color='green')
plt.plot(nodes_planar, dsatur_times_planar, marker='^', label='DSATUR', color='orange')
plt.plot(nodes_planar, welshpowell_times_planar, marker='d', label='WelshPowell', color='red')

plt.title("Timpul de executie al algoritmilor pe grafuri planare", fontsize=14)
plt.xlabel("Numarul de noduri (N)", fontsize=12)
plt.ylabel("Timpul de executie (secunde)", fontsize=12)
plt.legend(title="Algoritmi")
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()
