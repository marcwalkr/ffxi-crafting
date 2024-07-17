from tkinter import ttk


class SimulatePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent.notebook)
        self.parent = parent
        self.create_simulate_page()

    def create_simulate_page(self):
        self.parent.notebook.add(self, text="Simulate Synth")
        label = ttk.Label(self, text="Simulate Synth Page", font=("Helvetica", 16))
        label.pack(pady=20)
