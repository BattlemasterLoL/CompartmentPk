import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox


def is_square(mat):
    return mat.shape[0] == mat.shape[1]


def get_user_input():
    n = int(input_compartments.get())
    m = np.zeros((n, n))
    y0 = np.zeros(n)

    for i in range(n):
        for j in range(n):
            m[i, j] = float(input_m_matrix[i][j].get())
        y0[i] = float(input_y0_vector[i].get())

    return m, y0


def run_simulation():
    try:
        m, y0 = get_user_input()
        if is_square(m) and is_square(m.T):
            pass
        else:
            messagebox.showerror(
                "Error", "Please enter a square matrix for m.")
            return

        def model(y, t):
            dydt = -np.dot(m, y)  # ODE
            return dydt

        t = np.linspace(0, 20)
        y = odeint(model, y0, t)

        for i in range(len(m)):
            plt.plot(t, y[:, i], label="Compartment " + str(i + 1))
        print(type(y))

        plt.xlabel("Time (hrs)")
        plt.ylabel("Concentration (nM)")
        plt.legend()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("ODE Solver")

frame_main = ttk.Frame(root, padding="10")
frame_main.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame_compartments = ttk.LabelFrame(
    frame_main, padding="10", text="Compartments")
frame_compartments.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

input_compartments = ttk.Entry(frame_compartments, width=10)
input_compartments.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
ttk.Label(frame_compartments, text="Enter the number of compartments: ").grid(
    row=0, column=1, padx=5, pady=5, sticky=tk.W
)

frame_m_matrix = ttk.LabelFrame(frame_main, padding="10", text="m Matrix")
frame_m_matrix.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

input_m_matrix = []
for i in range(4):
    input_row = []
    for j in range(4):
        entry = ttk.Entry(frame_m_matrix, width=10)
        entry.grid(row=i, column=j, padx=5, pady=5, sticky=tk.W)
        input_row.append(entry)
    input_m_matrix.append(input_row)

frame_y0_vector = ttk.LabelFrame(
    frame_main, padding="10", text="Initial Conditions")
frame_y0_vector.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

input_y0_vector = []
for i in range(4):
    entry = ttk.Entry(frame_y0_vector, width=10)
    entry.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
    input_y0_vector.append(entry)

ttk.Button(frame_main, text="Run Simulation", command=run_simulation).grid(
    row=3, column=0, columnspan=4, padx=5, pady=5
)

root.mainloop()
