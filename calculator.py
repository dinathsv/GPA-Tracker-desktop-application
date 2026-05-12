import database

def convert_mark_to_grade_point(mark: float) -> float:
    if mark >= 85: return 4.0
    if mark >= 70: return 4.0
    if mark >= 65: return 3.7
    if mark >= 60: return 3.3
    if mark >= 55: return 3.0
    if mark >= 50: return 2.7
    if mark >= 45: return 2.3
    if mark >= 40: return 2.0
    return 0.0

def convert_mark_to_letter_grade(mark: float) -> str:
    if mark >= 85: return "A+"
    if mark >= 70: return "A"
    if mark >= 65: return "A-"
    if mark >= 60: return "B+"
    if mark >= 55: return "B"
    if mark >= 50: return "B-"
    if mark >= 45: return "C+"
    if mark >= 40: return "C"
    return "F"

def calculate_sgpa(semester_id: int) -> float | None:
    modules = database.get_modules_by_semester(semester_id)
    if not modules:
        return None
    
    total_credits = sum(m[2] for m in modules)
    if total_credits == 0:
        return None
    
    total_points = sum(m[5] * m[2] for m in modules)
    return total_points / total_credits

def calculate_cgpa() -> float | None:
    modules = database.get_all_modules()
    if not modules:
        return None
    
    total_credits = sum(m[3] for m in modules)
    if total_credits == 0:
        return None
    
    total_points = sum(m[6] * m[3] for m in modules)
    return total_points / total_credits
