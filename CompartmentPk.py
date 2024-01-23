import numpy as np
from scipy.integrate import odeint
import sympy as sym
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

# Compile macOS: pyinstaller --collect-all matplotlib --onefile --windowed CompartmentPk.py

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


def find_eigenvalues_and_eigenvectors(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    return eigenvalues, eigenvectors


def find_coeff(eigenvectors, initial_values):
    if len(initial_values) == 2:
        # Equations below are determined by the compartment placement
        a1, a2 = sym.symbols("a1, a2")
        eq1 = sym.Eq(
            (a1 * eigenvectors[0][1] + a2 * eigenvectors[0][0]), initial_values[0])
        eq2 = sym.Eq(
            (a1 * eigenvectors[1][1] + a2 * eigenvectors[1][0]), initial_values[1])
        result = sym.solve([eq1, eq2], (a1, a2))
        result = [result[a1], result[a2]]
    elif len(initial_values) == 3:
        # Equations below are determined by the compartment placement
        a1, a2, a3 = sym.symbols("a1, a2, a3")
        eq1 = sym.Eq((a1 * eigenvectors[0][2] + a2 * eigenvectors[0]
                     [1] + a3 * eigenvectors[0][0]), initial_values[0])
        eq2 = sym.Eq((a1 * eigenvectors[1][2] + a2 * eigenvectors[1]
                     [1] + a3 * eigenvectors[1][0]), initial_values[1])
        eq3 = sym.Eq((a1 * eigenvectors[2][2] + a2 * eigenvectors[2]
                     [1] + a3 * eigenvectors[2][0]), initial_values[2])
        result = sym.solve([eq1, eq2, eq3], (a1, a2, a3))
        result = [result[a1], result[a2], result[a3]]
    elif len(initial_values) == 4:
        # Equations below are determined by the compartment placement
        a1, a2, a3, a4 = sym.symbols("a1, a2, a3, a4")
        eq1 = sym.Eq((a1 * eigenvectors[0][3] + a2 * eigenvectors[0][2] + a3 *
                     eigenvectors[0][1] + a4 * eigenvectors[0][0]), initial_values[0])
        eq2 = sym.Eq((a1 * eigenvectors[1][3] + a2 * eigenvectors[1][2] + a3 *
                     eigenvectors[1][1] + a4 * eigenvectors[1][0]), initial_values[1])
        eq3 = sym.Eq((a1 * eigenvectors[2][3] + a2 * eigenvectors[2][2] + a3 *
                     eigenvectors[2][1] + a4 * eigenvectors[2][0]), initial_values[2])
        eq4 = sym.Eq((a1 * eigenvectors[3][3] + a2 * eigenvectors[3][2] + a3 *
                     eigenvectors[3][1] + a4 * eigenvectors[3][0]), initial_values[3])
        result = sym.solve([eq1, eq2, eq3, eq4], (a1, a2, a3, a4))
        result = [result[a1], result[a2], result[a3], result[a4]]
    return result


def const_eigen_window():
    m, y0 = get_user_input()
    eigvalues, eigvectors = find_eigenvalues_and_eigenvectors(m)
    a_coeff = find_coeff(eigvectors, y0)
    prefix = "a{}: "

    window2 = tk.Toplevel()
    window2.title('Extra Data')
    window2.geometry('+700+75')
    

    # Creating a frame for each label
    evecf = ttk.LabelFrame(window2, padding="10", text="Eigenvector")
    evalf = ttk.LabelFrame(window2, padding="10", text="Eigenvalue")
    cvalf = ttk.LabelFrame(window2, padding="10", text="a Coefficents")

    # Gridding the frames
    evecf.grid(row=0, column=0, padx=5, pady=5)
    evalf.grid(row=1, column=0, padx=5, pady=5)
    cvalf.grid(row=2, column=0, padx=5, pady=5)

    # Packing the labels within each frame
    ttk.Label(evecf, text=eigvectors).pack(padx=5, pady=5)
    ttk.Label(evalf, text=eigvalues).pack(padx=5, pady=5)
    for i, coeff in enumerate(a_coeff, start=1):
        ttk.Label(cvalf, text=prefix.format(
            i) + str(coeff)).pack(padx=5, pady=5)


def run_simulation():
    const_eigen_window()
    try:
        m, y0 = get_user_input()
        if is_square(m) and is_square(m.T):
            pass
        else:
            messagebox.showerror(
                "Error", "Please enter a square matrix for m.")
            return

        def model(y, t):
            dydt = -np.dot(m, y)          # ODE
            return dydt

        def model_cont(y, t):
            dydt = -np.dot(m, y) + y0     # ODE
            return dydt

        t = np.linspace(float(time_0.get()), float(time_f.get()), 100)
        if cont_value.get() == 0:
            y = odeint(model, y0, t)
        else:
            # for continuous injection
            yin = np.zeros(len(y0))
            y = odeint(model_cont, yin, t)

        if time_skip.get() == '':
            for i in range(len(m)):
                plt.plot(t, y[:, i], label="Compartment " + str(i + 1))
        else:
            y_new = y.copy()
            tskip = float(time_skip.get())
            time_index = int(np.where(t >= tskip)[0][0])
            idx = time_index
            # for repeated injection
            while idx < len(t):
                ypad = np.pad(y, ((int(idx), 0), (0, 0)),
                              mode='constant', constant_values=0)
                ypad = ypad[0:len(y), :]
                y_new = y_new + ypad
                idx = idx + time_index
            for i in range(len(m)):
                plt.plot(t, y_new[:, i], label="Compartment " + str(i + 1))

        plt.xlabel("Time (hrs)")
        plt.ylabel("Concentration (nM)")
        plt.legend()
        plt.show()


    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Compartment Pk Solver")

frame_main = ttk.Frame(root, padding="10")
frame_main.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame_compartments = ttk.LabelFrame(
    frame_main, padding="10", text="Compartments")
frame_compartments.grid(row=0, column=0, columnspan=2,
                        sticky=(tk.W, tk.E, tk.N, tk.S))

input_compartments = ttk.Entry(frame_compartments, width=10)
input_compartments.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
ttk.Label(frame_compartments, text="Enter the number of compartments: ").grid(
    row=0, column=1, padx=5, pady=5, sticky=tk.W
)

frame_m_matrix = ttk.LabelFrame(frame_main, padding="10", text="m Matrix")
frame_m_matrix.grid(row=1, column=0, columnspan=2,
                    sticky=(tk.W, tk.E, tk.N, tk.S))

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

frame_t_values = ttk.LabelFrame(frame_main, padding="10", text="Time Values")
frame_t_values.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame_t_values, text='Initial: ').grid(
    row=0, column=0, padx=5, pady=5)
ttk.Label(frame_t_values, text='Final: ').grid(row=1, column=0, padx=5, pady=5)
ttk.Label(frame_t_values, text='Skip: ').grid(row=2, column=0, padx=5, pady=5)

time_0 = ttk.Entry(frame_t_values, width=10)
time_0.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
time_f = ttk.Entry(frame_t_values, width=10)
time_f.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
time_skip = ttk.Entry(frame_t_values, width=10)
time_skip.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

ttk.Button(frame_main, text="Run Simulation", command=run_simulation).grid(
    row=3, column=0, padx=5, pady=5
)

cont_value = tk.IntVar(value=0)
continuous_check = ttk.Checkbutton(frame_main, text="Continuous Input", onvalue=1, offvalue=0, variable=cont_value).grid(
    row=3, column=1, padx=5, pady=5
)


root.mainloop()
