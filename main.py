import os
import database
from ui.app import App
from ui.profile_frame import ProfileFrame
from ui.semester_frame import SemesterFrame
from ui.module_frame import ModuleFrame
from ui.dashboard_frame import DashboardFrame
from ui.charts_frame import ChartsFrame
import customtkinter as ctk

def main():
    database.init_db()
    
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")
    
    app = App()
    
    # Store frames
    app.frames["Profile"] = ProfileFrame(app, app.get_font)
    app.frames["Semesters"] = SemesterFrame(app, app.get_font, lambda: app.frames["Modules"].load_semesters())
    app.frames["Modules"] = ModuleFrame(app, app.get_font, lambda: [app.frames["Dashboard"].load_data(), app.frames["Charts"].load_data()])
    app.frames["Dashboard"] = DashboardFrame(app, app.get_font)
    app.frames["Charts"] = ChartsFrame(app, app.get_font)
    
    active_frame = None
    nav_buttons = {}

    def show_frame(name):
        nonlocal active_frame
        if active_frame:
            active_frame.grid_forget()
            nav_buttons[app.active_btn].configure(font=app.font_main, border_width=0)
            
        active_frame = app.frames[name]
        app.active_btn = name
        active_frame.grid(row=0, column=1, sticky="nsew")
        if hasattr(active_frame, "load_data"):
            active_frame.load_data()
            
        nav_buttons[name].configure(font=("Segoe UI", 13, "bold"), border_width=2, border_spacing=0, border_color="#4a90d9")
        # Hack to emulate left border: just make text bold and standard button look active. The requirement is minimalist.
    
    for i, f_name in enumerate(["Dashboard", "Semesters", "Modules", "Profile", "Charts"]):
        btn = ctk.CTkButton(app.nav_frame, text=f_name, fg_color="transparent", text_color="#e0e0e0",
                            hover_color="#333333", anchor="w", corner_radius=0, command=lambda n=f_name: show_frame(n))
        btn.grid(row=i+2, column=0, sticky="ew", pady=2)
        nav_buttons[f_name] = btn

    # Initial view
    if database.load_profile() is None:
        show_frame("Profile")
    else:
        show_frame("Dashboard")
        
    app.mainloop()

if __name__ == "__main__":
    main()
