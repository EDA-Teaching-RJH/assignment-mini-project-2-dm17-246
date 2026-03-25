# ==========================================
# 1. IMPORTS & LIBRARIES
# ==========================================

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
