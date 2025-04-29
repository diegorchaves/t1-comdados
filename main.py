import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def nrz_l(binary_seq):
    signal, time = [], []
    t = 0
    for bit in binary_seq:
        val = 1 if bit == '1' else 0
        signal += [val, val]
        time += [t, t + 1]
        t += 1
    return time, signal

def nrz_i(binary_seq):
    signal, time = [], []
    t, level = 0, 0
    for bit in binary_seq:
        if bit == '1':
            level = 1 - level
        signal += [level, level]
        time += [t, t + 1]
        t += 1
    return time, signal

def ami(binary_seq):
    signal, time = [], []
    t, level = 0, 1
    for bit in binary_seq:
        if bit == '1':
            signal += [level, level]
            level = -level
        else:
            signal += [0, 0]
        time += [t, t + 1]
        t += 1
    return time, signal

def pseudoternary(binary_seq):
    signal, time = [], []
    t, level = 1, 1
    for bit in binary_seq:
        if bit == '0':
            signal += [level, level]
            level = -level
        else:
            signal += [0, 0]
        time += [t, t + 1]
        t += 1
    return time, signal

def manchester(binary_seq):
    signal, time = [], []
    t = 0
    for bit in binary_seq:
        if bit == '1':
            signal += [1, 0]
        else:
            signal += [0, 1]
        time += [t, t + 0.5]
        t += 1
    return time, signal

def differential_manchester(binary_seq):
    signal, time = [], []
    t, level = 0, 1
    for bit in binary_seq:
        if bit == '0':
            level = 1 - level
        signal += [level, 1 - level]
        time += [t, t + 0.5]
        t += 1
    return time, signal

def rz(binary_seq):
    signal, time = [], []
    t = 0
    for bit in binary_seq:
        if bit == '1':
            signal += [1, 0]
        else:
            signal += [0, 0]
        time += [t, t + 0.5]
        t += 1
    return time, signal

def mlt_3(binary_seq):
    signal, time = [], []
    t = 0
    current_level = 0
    levels = [0, 1, 0, -1]
    state = 0 

    for bit in binary_seq:
        if bit == '1':
            state = (state + 1) % 4
        current_level = levels[state]
        signal += [current_level, current_level]
        time += [t, t + 1]
        t += 1

    return time, signal


def hdb3(binary_seq):
    signal, time = [], []
    t = 0
    level = 1  # Primeiro pulso é +1
    pulse_count = 0  # Conta quantos pulsos '1' já houve
    zero_count = 0

    i = 0
    while i < len(binary_seq):
        bit = binary_seq[i]
        if bit == '1':
            zero_count = 0
            level = -level
            signal += [level, level]
            pulse_count += 1
            time += [t, t + 1]
            t += 1
            i += 1
        else:
            # Conta zeros consecutivos
            zero_count = 1
            j = i + 1
            while j < len(binary_seq) and binary_seq[j] == '0' and zero_count < 4:
                zero_count += 1
                j += 1

            if zero_count == 4:
                if pulse_count % 2 == 0:
                    # Substitui por B00V
                    signal += [level, level] + [0, 0] + [0, 0] + [level, level]
                else:
                    # Substitui por 000V
                    signal += [0, 0] + [0, 0] + [0, 0]
                    level = -level
                    signal += [level, level]
                pulse_count = 0
                time += [t + i2 for i2 in range(4) for _ in (0, 1)]
                t += 4
                i += 4
            else:
                # Menos de 4 zeros → insere normalmente
                for _ in range(zero_count):
                    signal += [0, 0]
                    time += [t, t + 1]
                    t += 1
                i += zero_count
    return time, signal


class LineCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Códigos de Linha")

        # Frame lateral
        sidebar = ttk.Frame(root, padding=10)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(sidebar, text="Tipo de Codificação:").pack(anchor=tk.W)
        self.code_type = tk.StringVar(value="NRZ-L")

        self.options = [
            "NRZ-L", "NRZ-I", "AMI", "Pseudoternário",
            "Manchester", "Manchester Diferencial",
            "HDB3", "MLT-3", "RZ"
        ]
        for opt in self.options:
            ttk.Radiobutton(sidebar, text=opt, variable=self.code_type, value=opt).pack(anchor=tk.W)

        ttk.Label(sidebar, text="Sequência binária:").pack(anchor=tk.W, pady=(10, 0))
        self.binary_entry = ttk.Entry(sidebar)
        self.binary_entry.pack(fill=tk.X)

        ttk.Button(sidebar, text="Gerar Gráfico", command=self.generate_plot).pack(pady=10)

        # Área do gráfico
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def generate_plot(self):
        binary_seq = self.binary_entry.get()
        if not all(c in '01' for c in binary_seq):
            messagebox.showerror("Erro", "A sequência deve conter apenas 0s e 1s.")
            return

        self.ax.clear()

        code_type = self.code_type.get()
        if code_type == "NRZ-L":
            t, s = nrz_l(binary_seq)
        elif code_type == "NRZ-I":
            t, s = nrz_i(binary_seq)
        elif code_type == "AMI":
            t, s = ami(binary_seq)
        elif code_type == "Pseudoternário":
            t, s = pseudoternary(binary_seq)
        elif code_type == "Manchester":
            t, s = manchester(binary_seq)
        elif code_type == "Manchester Diferencial":
            t, s = differential_manchester(binary_seq)
        elif code_type == "HDB3":
            t, s = hdb3(binary_seq)
        elif code_type == "MLT-3":
            t, s = mlt_3(binary_seq)
        elif code_type == "RZ":
            t, s = rz(binary_seq)
        else:
            t, s = []

        self.ax.step(t, s, where='post')
        self.ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
        self.ax.set_title(f"Codificação: {code_type}")
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_yticks([0])
        self.ax.set_yticklabels(['0'])
        self.ax.set_xticks(np.arange(0, len(binary_seq) + 1, 1))
        self.ax.set_xticklabels([])
        self.ax.grid(True, which='major', axis='x', linestyle='--', linewidth=0.5)
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = LineCodeApp(root)
    root.mainloop()
