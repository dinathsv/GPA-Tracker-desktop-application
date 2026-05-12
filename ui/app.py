import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GPA Tracker")
        self.geometry("960x620")
        self.resizable(False, False)
        
        # Determine standard font
        self.font_main = ("Segoe UI", 13)
        self.font_heading = ("Segoe UI", 15, "bold")
        self.font_large = ("Segoe UI", 48, "bold")
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Navigation Frame
        self.nav_frame = ctk.CTkFrame(self, width=180, corner_radius=0, fg_color="#222222")
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_propagate(False)
        
        self.logo_label = ctk.CTkLabel(self.nav_frame, text="GPA Tracker", font=self.font_heading)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.separator = ctk.CTkFrame(self.nav_frame, height=1, fg_color="#333333")
        self.separator.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Placeholder for dynamic frames, easily added in main module
        self.frames = {}
        self.active_btn = None
        
    def get_font(self, name):
        if name == "heading":
            return self.font_heading
        elif name == "large":
            return self.font_large
        return self.font_main
        
        self.separator = ctk.CTkFrame(self.nav_frame, height=1, fg_color="#333333")
        self.separator.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Placeholder for dynamic frames, easily added in main module
        self.frames = {}
        self.active_btn = None
