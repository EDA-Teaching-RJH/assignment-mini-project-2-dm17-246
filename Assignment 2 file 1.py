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

