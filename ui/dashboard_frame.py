import customtkinter as ctk
import database
import calculator

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, get_font):
        super().__init__(master, fg_color="#1a1a1a", corner_radius=0)
        self.get_font = get_font
        
        self.label = ctk.CTkLabel(self, text="Dashboard", font=self.get_font("heading"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        self.cgpa_val = ctk.CTkLabel(self, text="N/A", font=("Segoe UI", 48, "bold"))
        self.cgpa_val.grid(row=1, column=0, padx=20, sticky="w")
        
        self.stats_lbl = ctk.CTkLabel(self, text="Total Credits: 0  |  Total Modules: 0", text_color="#888888", font=self.get_font("main"))
        self.stats_lbl.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")
        
        self.best_lbl = ctk.CTkLabel(self, text="Best Module: N/A", font=self.get_font("main"))
        self.best_lbl.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        
        self.worst_lbl = ctk.CTkLabel(self, text="Needs Attention: N/A", font=self.get_font("main"))
        self.worst_lbl.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        
        self.warn_title = ctk.CTkLabel(self, text="Warnings:", text_color="#e67e22", font=self.get_font("heading"))
        self.warn_title.grid(row=5, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.warn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.warn_frame.grid(row=6, column=0, padx=20, sticky="w")
        
    def load_data(self):
        cgpa = calculator.calculate_cgpa()
        mods = database.get_all_modules()
        
        if cgpa is None:
            self.cgpa_val.configure(text="N/A", text_color="#e0e0e0")
            self.stats_lbl.configure(text="Total Credits: 0  |  Total Modules: 0")
            self.best_lbl.configure(text="Best Module: N/A")
            self.worst_lbl.configure(text="Needs Attention: N/A")
            for w in self.warn_frame.winfo_children(): w.destroy()
            return
            
        color = "#27ae60" if cgpa >= 3.0 else ("#e67e22" if cgpa >= 2.0 else "#c0392b")
        self.cgpa_val.configure(text=f"{cgpa:.2f}", text_color=color)
        
        cc = sum(m[3] for m in mods)
        self.stats_lbl.configure(text=f"Total Credits: {cc}  |  Total Modules: {len(mods)}")
        
        best = max(mods, key=lambda x: x[6])
        worst = min(mods, key=lambda x: x[6])
        
        self.best_lbl.configure(text=f"Best Module: {best[2]} ({best[5]})")
        self.worst_lbl.configure(text=f"Needs Attention: {worst[2]} ({worst[5]})")
        
        for w in self.warn_frame.winfo_children(): w.destroy()
        
        warnings = [m for m in mods if m[6] < 2.0]
        if not warnings:
            ctk.CTkLabel(self.warn_frame, text="All good!", text_color="#27ae60").pack(anchor="w")
        else:
            for w in warnings:
                ctk.CTkLabel(self.warn_frame, text=f"⚠ {w[2]} ({w[5]})", text_color="#c0392b").pack(anchor="w")
