import customtkinter as ctk
import database

class SemesterFrame(ctk.CTkFrame):
    def __init__(self, master, get_font, refresh_callback):
        super().__init__(master, fg_color="#1a1a1a", corner_radius=0)
        self.get_font = get_font
        self.refresh_callback = refresh_callback
        
        self.label = ctk.CTkLabel(self, text="Semesters", font=self.get_font("heading"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        self.add_entry = ctk.CTkEntry(self, height=34, corner_radius=2, placeholder_text="New Semester Name")
        self.add_entry.grid(row=1, column=0, padx=20, pady=10, sticky="w", ipadx=50)
        
        self.add_btn = ctk.CTkButton(self, text="Add", width=60, corner_radius=3, height=32, 
                                     fg_color="#4a90d9", hover_color="#3a7bc8", command=self.add_sem)
        self.add_btn.grid(row=1, column=1, pady=10, sticky="w")

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
        
        self.msg_lbl = ctk.CTkLabel(self, text="", font=self.get_font("main"))
        self.msg_lbl.grid(row=3, column=0, padx=20, sticky="w")
        
        self.load_data()

    def load_data(self):
        for widget in self.list_frame.winfo_children(): widget.destroy()
        semesters = database.get_all_semesters()
        for i, s in enumerate(semesters):
            bg = "#2a2a2a" if i % 2 == 0 else "#262626"
            row = ctk.CTkFrame(self.list_frame, fg_color=bg, height=36, corner_radius=0)
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text=s[1], font=self.get_font("main")).pack(side="left", padx=12, pady=5)
            
            del_btn = ctk.CTkButton(row, text="Delete", width=50, fg_color="transparent", text_color="#c0392b",
                                    hover_color="#2a1a1a", border_width=1, border_color="#c0392b", corner_radius=3,
                                    command=lambda s_id=s[0]: self.delete_sem(s_id))
            del_btn.pack(side="right", padx=12, pady=5)

    def add_sem(self):
        try:
            database.add_semester(self.add_entry.get())
            self.add_entry.delete(0, 'end')
            self.load_data()
            self.refresh_callback()
            self.show_msg("Added.", "#27ae60")
        except:
            self.show_msg("Duplicate or invalid name.", "#c0392b")
            
    def delete_sem(self, s_id):
        database.delete_semester(s_id)
        self.load_data()
        self.refresh_callback()
        self.show_msg("Deleted.", "#27ae60")

    def show_msg(self, text, color):
        self.msg_lbl.configure(text=text, text_color=color)
        self.after(3000, lambda: self.msg_lbl.configure(text=""))
