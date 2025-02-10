import matplotlib.pyplot as plt

nodes_chordal = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
backtracking_times_chordal = [0.0424, 0.0382, 0.0445, 0.0455, 0.0403, 0.0463, 0.0380, 0.0428, 0.1274, 0.6766, 10.4985]
greedy_times_chordal = [0.0474, 0.0461, 0.0537, 0.0489, 0.0615, 0.0484, 0.0478, 0.0498, 0.0512, 0.0597, 0.0564, 0.0615, 0.0547, 0.0501, 0.0506, 0.0517, 0.0502, 0.0553, 0.0520, 0.0482, 0.0494, 0.0484, 0.0536, 0.0598, 0.0508, 0.0531, 0.0495, 0.0515, 0.0747, 0.0529, 0.0487]
dsatur_times_chordal = [0.0505, 0.0473, 0.0481, 0.0514, 0.0604, 0.0562, 0.0519, 0.0470, 0.0579, 0.0608, 0.0475, 0.0503, 0.0490, 0.0566, 0.0515, 0.0576, 0.0500, 0.0539, 0.0631, 0.0538, 0.0677, 0.0538, 0.0499, 0.0591, 0.0553, 0.0647, 0.0604, 0.0539, 0.0502, 0.0538, 0.0511]
welshpowell_times_chordal = [0.0466, 0.0495, 0.0499, 0.0481, 0.0480, 0.0498, 0.0471, 0.0498, 0.0485, 0.0547, 0.0580, 0.0508, 0.0462, 0.0489, 0.0550, 0.0513, 0.0494, 0.0532, 0.0520, 0.0612, 0.0541, 0.0542, 0.0634, 0.0471, 0.0535, 0.0490, 0.0530, 0.0519, 0.0520, 0.0508, 0.0521]

plt.figure(figsize=(10, 6))

# Backtracking
plt.plot(nodes_chordal[:len(backtracking_times_chordal)], backtracking_times_chordal, 
         marker='o', color='blue', label='Backtracking')

plt.title("Timpul de executie - Backtracking pe grafuri chordale", fontsize=14)
plt.xlabel("Numarul de noduri (N)", fontsize=12)
plt.ylabel("Timpul de executie (secunde)", fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

# Greedy, DSATUR, WelshPowell
plt.plot(nodes_chordal, greedy_times_chordal[:len(nodes_chordal)], marker='s', color='green', label='Greedy')
plt.plot(nodes_chordal, dsatur_times_chordal[:len(nodes_chordal)], marker='^', color='orange', label='DSATUR')
plt.plot(nodes_chordal, welshpowell_times_chordal[:len(nodes_chordal)], marker='d', color='red', label='WelshPowell')

plt.title("Timpul de executie - Algoritmi euristici pe grafuri chordale", fontsize=14)
plt.xlabel("Numarul de noduri (N)", fontsize=12)
plt.ylabel("Timpul de executie (secunde)", fontsize=12)
plt.legend(title="Algoritmi")
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
