import customtkinter as ctk
import database
import calculator

class ModuleFrame(ctk.CTkFrame):
    def __init__(self, master, get_font, refresh_callback):
        super().__init__(master, fg_color="#1a1a1a", corner_radius=0)
        self.get_font = get_font
        self.refresh_callback = refresh_callback
        
        self.label = ctk.CTkLabel(self, text="Modules", font=self.get_font("heading"))
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.sem_var = ctk.StringVar()
        self.sem_dropdown = ctk.CTkOptionMenu(self, variable=self.sem_var, command=self.on_sem_change, fg_color="#333", button_color="#444", button_hover_color="#555")
        self.sem_dropdown.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        self.inputs_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.inputs_frame.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        self.mname = ctk.CTkEntry(self.inputs_frame, placeholder_text="Module Name", height=34, corner_radius=2)
        self.mname.pack(side="left", padx=5)
        self.mcred = ctk.CTkEntry(self.inputs_frame, placeholder_text="Credits", height=34, corner_radius=2, width=80)
        self.mcred.pack(side="left", padx=5)
        self.mmark = ctk.CTkEntry(self.inputs_frame, placeholder_text="Mark (0-100)", height=34, corner_radius=2, width=100)
        self.mmark.pack(side="left", padx=5)
        
        self.add_btn = ctk.CTkButton(self.inputs_frame, text="Add", width=60, corner_radius=3, height=32, 
                                     fg_color="#4a90d9", hover_color="#3a7bc8", command=self.add_mod)
        self.add_btn.pack(side="left", padx=5)
        
        headers = ctk.CTkLabel(self, text="MODULE  ·  CREDITS  ·  MARK  ·  GRADE", text_color="#888888", font=("Segoe UI", 11, "bold"))
        headers.grid(row=3, column=0, padx=30, pady=(10, 0), sticky="w")
        
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", height=300)
        self.list_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=5)
        
        self.msg_lbl = ctk.CTkLabel(self, text="", font=self.get_font("main"))
        self.msg_lbl.grid(row=5, column=0, padx=20, sticky="w")
        
        self.semester_map = {}
        self.load_semesters()
        
    def load_semesters(self):
        sems = database.get_all_semesters()
        self.semester_map = {s[1]: s[0] for s in sems}
        if sems:
            self.sem_dropdown.configure(values=[s[1] for s in sems])
            self.sem_var.set(sems[0][1])
            self.load_data()
        else:
            self.sem_dropdown.configure(values=["No Semesters"])
            self.sem_var.set("No Semesters")

    def on_sem_change(self, value):
        self.load_data()

    def load_data(self):
        for widget in self.list_frame.winfo_children(): widget.destroy()
        sem = self.sem_var.get()
        if sem not in self.semester_map: return
        sid = self.semester_map[sem]
        
        mods = database.get_modules_by_semester(sid)
        for i, m in enumerate(mods):
            bg = "#2a2a2a" if i % 2 == 0 else "#262626"
            row = ctk.CTkFrame(self.list_frame, fg_color=bg, height=36, corner_radius=0)
            row.pack(fill="x", pady=1)
            t = f"{m[1]}  ·  {m[2]} cr  ·  {m[3]}  ·  {m[4]} ({m[5]})"
            ctk.CTkLabel(row, text=t, font=self.get_font("main")).pack(side="left", padx=12, pady=5)
            
            del_btn = ctk.CTkButton(row, text="Delete", width=50, fg_color="transparent", text_color="#c0392b",
                                    hover_color="#2a1a1a", border_width=1, border_color="#c0392b", corner_radius=3,
                                    command=lambda m_id=m[0]: self.delete_mod(m_id))
            del_btn.pack(side="right", padx=12, pady=5)

    def add_mod(self):
        try:
            sname = self.sem_var.get()
            sid = self.semester_map[sname]
            cr = int(self.mcred.get())
            mk = float(self.mmark.get())
            if not (0 <= mk <= 100): raise ValueError
            nm = self.mname.get()
            if not nm: raise ValueError
            
            lg = calculator.convert_mark_to_letter_grade(mk)
            gp = calculator.convert_mark_to_grade_point(mk)
            
            database.add_module(sid, nm, cr, mk, lg, gp)
            self.mname.delete(0, 'end'); self.mcred.delete(0, 'end'); self.mmark.delete(0, 'end')
            self.load_data()
            self.refresh_callback()
            self.show_msg("Added.", "#27ae60")
        except:
            self.show_msg("Invalid input.", "#c0392b")

    def delete_mod(self, m_id):
        database.delete_module(m_id)
        self.load_data()
        self.refresh_callback()
        self.show_msg("Deleted.", "#27ae60")

    def show_msg(self, text, color):
        self.msg_lbl.configure(text=text, text_color=color)
        self.after(3000, lambda: self.msg_lbl.configure(text=""))
