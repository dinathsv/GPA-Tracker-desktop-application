import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import database
from calculator import calculate_cgpa

def export_csv(filepath):
    modules = database.get_all_modules()
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Semester', 'Module Name', 'Credits', 'Mark', 'Letter Grade', 'Grade Point'])
        for m in modules:
            writer.writerow([m[1], m[2], m[3], m[4], m[5], m[6]])

def export_pdf(filepath):
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    profile = database.load_profile()
    cgpa = calculate_cgpa()
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Student Transcript & GPA Report")
    
    c.setFont("Helvetica", 12)
    if profile:
        c.drawString(50, height - 80, f"Name: {profile[0]}")
        c.drawString(50, height - 100, f"University: {profile[1]}")
        c.drawString(50, height - 120, f"Programme: {profile[2]}")
        c.drawString(50, height - 140, f"Enrolment Year: {profile[3]}")
    
    cgpa_str = f"{cgpa:.2f}" if cgpa is not None else "N/A"
    c.drawString(50, height - 170, f"Current CGPA: {cgpa_str}")
    
    c.drawString(50, height - 210, "Modules:")
    y = height - 230
    modules = database.get_all_modules()
    
    for m in modules:
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(50, y, f"{m[1]} | {m[2]} | {m[3]} Credits | Mark: {m[4]} | Grade: {m[5]} | GP: {m[6]}")
        y -= 20
        
    c.save()
