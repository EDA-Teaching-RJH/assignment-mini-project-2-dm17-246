# ==========================================
# 1. IMPORTS & LIBRARIES
# ==========================================

from email.mime import base
from email.mime import base
import re
import csv
import os

# ==========================================
# 2. REGEX VALIDATION FUNCTIONS
# ==========================================

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(pattern, email))

def validate_student_id(student_id):
    pattern = r'^[A-Za-z]\d{5}$'
    return bool(re.match(pattern, student_id))

def validate_name(name):
    pattern = r'^[A-Za-z\s]+$'
    return bool(re.match(pattern, name.strip()))

def validate_score(score_str):
    try:
        score = int(score_str)
        if 0 <= score <= 100:
            return score
        return None
    except ValueError:
        return None

# ==========================================
# 3. FILE I/O FUNCTIONS
# ==========================================

FILE_NAME = "students.csv"
CSV_HEADERS = ["name", "email", "student_id", "score"]

def save_to_file(student_list):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for student in student_list:
            writer.writerow({
                "name":       student.name,
                "email":      student.email,
                "student_id": student.student_id,
                "score":      student.score
            })
    print(f"  Data saved to '{FILE_NAME}'.")

def load_from_file():
    loaded = []
    if not os.path.exists(FILE_NAME):
        print(f"  No file named '{FILE_NAME}' found. Starting with empty records.")
        return loaded

    with open(FILE_NAME, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            score = validate_score(row["score"])
            if score is None:
                print(f"  Warning: skipped row with invalid score: {row}")
                continue
            loaded.append(Student(row["name"], row["email"], row["student_id"], score))

    print(f"  Loaded {len(loaded)} student(s) from '{FILE_NAME}'.")
    return loaded

def export_report(student_list):
    report_file = "report.txt"
    with open(report_file, "w") as f:
        f.write("===== STUDENT PERFORMANCE REPORT =====\n\n")
        if not student_list:
            f.write("No students on record.\n")
        else:
            for s in student_list:
                f.write(f"Name:       {s.name}\n")
                f.write(f"Email:      {s.email}\n")
                f.write(f"Student ID: {s.student_id}\n")
                f.write(f"Score:      {s.score}  |  Grade: {s.get_grade()}\n")
                f.write("-" * 40 + "\n")

            scores = [s.score for s in student_list]
            f.write(f"\nAverage Score: {sum(scores) / len(scores):.1f}\n")
            f.write(f"Highest Score: {max(scores)}\n")
            f.write(f"Lowest Score:  {min(scores)}\n")

    print(f"  Report exported to '{report_file}'.")

# ==========================================
# 4. CLASS DEFINITIONS (OOP)
# ==========================================

class Person:

def __init__(self, name, email):
        self.name  = name
        self.email = email

def get_details(self):
    return f"Name: {self.name} | Email: {self.email}"

class Student(Person):

    def __init__(self, name, email, student_id, score):
        super().__init__(name, email)          # Calls Person.__init__ to set name + email
        self.student_id = student_id
        self.score      = score

def get_grade(self):
    
    if self.score >= 70:
            return "A"
        elif self.score >= 60:
            return "B"
        elif self.score >= 50:
            return "C"
        elif self.score >= 40:
            return "D"
        else:
            return "F"

def get_details(self):
    
    base = super().get_details()
    return f"{base} | ID: {self.student_id} | Score: {self.score} | Grade: {self.get_grade()}"


class StudentManager:
    def __init__(self):
        self.students = []    # The master in-memory list of Student objects

 # ---------- ADD ----------
    def add_student(self, name, email, student_id, score):
        elf.students.append(Student(name, email, student_id, score))
        print(f"  Student '{name}' added successfully.")
