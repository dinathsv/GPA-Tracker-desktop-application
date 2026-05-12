import customtkinter as ctk
import database

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master, get_font):
        super().__init__(master, fg_color="#1a1a1a", corner_radius=0)
        self.get_font = get_font
        
        self.label = ctk.CTkLabel(self, text="Profile Settings", font=self.get_font("heading"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        self.name_lbl = ctk.CTkLabel(self, text="Name", text_color="#888888", font=self.get_font("main"))
        self.name_lbl.grid(row=1, column=0, padx=20, pady=(10,4), sticky="w")
        self.name_entry = ctk.CTkEntry(self, height=34, corner_radius=2)
        self.name_entry.grid(row=2, column=0, padx=20, pady=(0, 16), sticky="w", ipadx=100)
        
        self.uni_lbl = ctk.CTkLabel(self, text="University", text_color="#888888", font=self.get_font("main"))
        self.uni_lbl.grid(row=3, column=0, padx=20, pady=(10,4), sticky="w")
        self.uni_entry = ctk.CTkEntry(self, height=34, corner_radius=2)
        self.uni_entry.grid(row=4, column=0, padx=20, pady=(0, 16), sticky="w", ipadx=100)
        
        self.prog_lbl = ctk.CTkLabel(self, text="Programme", text_color="#888888", font=self.get_font("main"))
        self.prog_lbl.grid(row=5, column=0, padx=20, pady=(10,4), sticky="w")
        self.prog_entry = ctk.CTkEntry(self, height=34, corner_radius=2)
        self.prog_entry.grid(row=6, column=0, padx=20, pady=(0, 16), sticky="w", ipadx=100)
        
        self.year_lbl = ctk.CTkLabel(self, text="Enrolment Year", text_color="#888888", font=self.get_font("main"))
        self.year_lbl.grid(row=7, column=0, padx=20, pady=(10,4), sticky="w")
        self.year_entry = ctk.CTkEntry(self, height=34, corner_radius=2)
        self.year_entry.grid(row=8, column=0, padx=20, pady=(0, 16), sticky="w", ipadx=100)
        
        self.save_btn = ctk.CTkButton(self, text="Save Profile", corner_radius=3, height=32, 
                                      fg_color="#4a90d9", hover_color="#3a7bc8", command=self.save_profile)
        self.save_btn.grid(row=9, column=0, padx=20, pady=24, sticky="w")
        
        self.msg_lbl = ctk.CTkLabel(self, text="", text_color="#27ae60", font=self.get_font("main"))
        self.msg_lbl.grid(row=10, column=0, padx=20, sticky="w")

        self.load_data()

    def load_data(self):
        data = database.load_profile()
        if data:
            self.name_entry.insert(0, data[0])
            self.uni_entry.insert(0, data[1])
            self.prog_entry.insert(0, data[2])
            self.year_entry.insert(0, str(data[3]))

    def save_profile(self):
        n = self.name_entry.get()
        u = self.uni_entry.get()
        p = self.prog_entry.get()
        try:
            y = int(self.year_entry.get())
            if not n or not u or not p: raise ValueError()
            database.save_profile(n, u, p, y)
            self.msg_lbl.configure(text="Saved.", text_color="#27ae60")
            self.after(3000, lambda: self.msg_lbl.configure(text=""))
        except:
            self.msg_lbl.configure(text="Please fill all fields correctly.", text_color="#c0392b")
