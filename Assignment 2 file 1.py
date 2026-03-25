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