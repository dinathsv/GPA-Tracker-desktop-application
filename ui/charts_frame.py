import customtkinter as ctk
import database
import calculator
from utils.export import export_pdf, export_csv
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter.filedialog as fd

class ChartsFrame(ctk.CTkFrame):
    def __init__(self, master, get_font):
        super().__init__(master, fg_color="#1a1a1a", corner_radius=0)
        self.get_font = get_font
        
        self.label = ctk.CTkLabel(self, text="Charts & Export", font=self.get_font("heading"))
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.fig = Figure(figsize=(7, 4), dpi=100)
        self.fig.patch.set_facecolor('#1a1a1a')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#222222')
        self.ax.tick_params(colors='#888888')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        
        ctk.CTkButton(self.btn_frame, text="Export CSV", width=100, corner_radius=3, fg_color="#333333", hover_color="#3d3d3d", command=self.do_csv).pack(side="left", padx=5)
        ctk.CTkButton(self.btn_frame, text="Export PDF", width=100, corner_radius=3, fg_color="#4a90d9", hover_color="#3a7bc8", command=self.do_pdf).pack(side="left", padx=5)
        
    def load_data(self):
        sems = database.get_all_semesters()
        sgpas = []
        names = []
        for s in sems:
            sgpa = calculator.calculate_sgpa(s[0])
            if sgpa is not None:
                names.append(s[1][:10])
                sgpas.append(sgpa)
                
        self.ax.clear()
        self.ax.set_facecolor('#222222')
        if names:
            self.ax.bar(names, sgpas, color='#4a90d9')
            self.ax.set_ylim(0, 4.0)
            self.ax.spines['bottom'].set_color('#333333')
            self.ax.spines['top'].set_color('none')
            self.ax.spines['left'].set_color('#333333')
            self.ax.spines['right'].set_color('none')
            for i, v in enumerate(sgpas):
                self.ax.text(i, v + 0.1, f"{v:.2f}", color='#e0e0e0', ha='center')
        
        self.canvas.draw()
        
    def do_csv(self):
        p = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if p: export_csv(p)

    def do_pdf(self):
        p = fd.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if p: export_pdf(p)
