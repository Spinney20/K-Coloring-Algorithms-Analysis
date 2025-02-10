import matplotlib.pyplot as plt

# Data
nodes_complete = [6, 7, 8, 9, 10, 11, 12, 20, 30, 40, 50, 60, 70, 80, 90, 100]
backtracking_times_complete = [0.0425, 0.0577, 0.0758, 0.3139, 3.0206, 34.5786]
greedy_times_complete = [0.0585, 0.0542, 0.0538, 0.0522, 0.0553, 0.0530, 0.0622, 0.0650, 0.0675, 0.0664, 0.0590, 0.0779, 0.0658, 0.0752, 0.0693, 0.0791]
dsatur_times_complete = [0.0686, 0.0549, 0.0529, 0.0532, 0.0538, 0.0563, 0.0610, 0.0544, 0.0505, 0.0567, 0.0552, 0.0745, 0.0708, 0.0911, 0.0951, 0.0926]
welshpowell_times_complete = [0.0617, 0.0590, 0.0517, 0.0520, 0.0658, 0.0571, 0.0553, 0.0612, 0.0534, 0.0517, 0.0562, 0.0720, 0.0754, 0.0757, 0.0817, 0.0740]

# Backtracking sepa
plt.figure(figsize=(10, 6))
plt.plot(nodes_complete[:len(backtracking_times_complete)], backtracking_times_complete, 
         marker='o', color='blue', label='Backtracking')


plt.title("Timpul de executie - Backtracking pe grafuri complete", fontsize=14)
plt.xlabel("Numarul de noduri (N)", fontsize=12)
plt.ylabel("Timpul de executie (secunde)", fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# other algorithms
plt.figure(figsize=(10, 6))
plt.plot(nodes_complete, greedy_times_complete, marker='s', color='green', label='Greedy')
plt.plot(nodes_complete, dsatur_times_complete, marker='^', color='orange', label='DSATUR')
plt.plot(nodes_complete, welshpowell_times_complete, marker='d', color='red', label='WelshPowell')

plt.title("Timpul de executie - Algoritmi euristici pe grafuri complete", fontsize=14)
plt.xlabel("Numarul de noduri (N)", fontsize=12)
plt.ylabel("Timpul de executie (secunde)", fontsize=12)
plt.legend(title="Algoritmi")
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
