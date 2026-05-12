import sqlite3
import os

DB_PATH = "gpa_tracker.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            university TEXT NOT NULL,
            programme TEXT NOT NULL,
            enrolment_year INTEGER NOT NULL
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS semesters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semester_id INTEGER NOT NULL,
            module_name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            mark REAL NOT NULL,
            letter_grade TEXT NOT NULL,
            grade_point REAL NOT NULL,
            FOREIGN KEY (semester_id) REFERENCES semesters(id) ON DELETE CASCADE
        )''')
        conn.commit()

def save_profile(name, university, programme, enrolment_year):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM profile LIMIT 1")
        row = c.fetchone()
        if row:
            c.execute('''UPDATE profile 
                         SET name=?, university=?, programme=?, enrolment_year=? 
                         WHERE id=?''', (name, university, programme, enrolment_year, row[0]))
        else:
            c.execute('''INSERT INTO profile (name, university, programme, enrolment_year) 
                         VALUES (?, ?, ?, ?)''', (name, university, programme, enrolment_year))
        conn.commit()

def load_profile():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT name, university, programme, enrolment_year FROM profile LIMIT 1")
        return c.fetchone()

def add_semester(name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO semesters (name) VALUES (?)", (name,))
        conn.commit()
        return c.lastrowid

def get_all_semesters():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, name FROM semesters ORDER BY id")
        return c.fetchall()

def rename_semester(semester_id, new_name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE semesters SET name=? WHERE id=?", (new_name, semester_id))
        conn.commit()

def delete_semester(semester_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM semesters WHERE id=?", (semester_id,))
        conn.commit()

def add_module(semester_id, module_name, credits, mark, letter_grade, grade_point):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO modules (semester_id, module_name, credits, mark, letter_grade, grade_point) 
                     VALUES (?, ?, ?, ?, ?, ?)''', 
                  (semester_id, module_name, credits, mark, letter_grade, grade_point))
        conn.commit()

def get_modules_by_semester(semester_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, module_name, credits, mark, letter_grade, grade_point FROM modules WHERE semester_id=?", (semester_id,))
        return c.fetchall()

def update_module(module_id, module_name, credits, mark, letter_grade, grade_point):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''UPDATE modules SET module_name=?, credits=?, mark=?, letter_grade=?, grade_point=? 
                     WHERE id=?''', (module_name, credits, mark, letter_grade, grade_point, module_id))
        conn.commit()

def delete_module(module_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM modules WHERE id=?", (module_id,))
        conn.commit()

def get_all_modules():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''SELECT m.id, s.name, m.module_name, m.credits, m.mark, m.letter_grade, m.grade_point 
                     FROM modules m JOIN semesters s ON m.semester_id = s.id
                     ORDER BY s.id, m.id''')
        return c.fetchall()
