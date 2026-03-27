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
        super().__init__(name, email)          
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
        self.students = []    

    # ---------- ADD ----------
    def add_student(self, name, email, student_id, score):
        self.students.append(Student(name, email, student_id, score))
        print(f"  Student '{name}' added successfully.")

    # ---------- VIEW ----------
    def view_all(self):
        if not self.students:
            print("  No students on record.")
            return
        print("\n  --- All Students ---")
        for i, s in enumerate(self.students, start=1):
            print(f"  {i}. {s.get_details()}")

    # ---------- SEARCH ----------
    def search_students(self, field, pattern):
            
        results = []
        for s in self.students:
            target = getattr(s, field)       
            if re.search(pattern, target, re.IGNORECASE):
                results.append(s)
        return results
    
    # ---------- EDIT ----------
    def edit_student(self, student_id, field, new_value):
         
        for s in self.students:
            if s.student_id == student_id:
                setattr(s, field, new_value)
                return True
        return False

    # ---------- DELETE ----------
    def delete_student(self, student_id):
         
         for s in self.students:
            if s.student_id == student_id:
                self.students.remove(s)
                return True
         return False

    # ---------- ANALYSE ----------
    def analyse(self):
         
        if not self.students:
            print("  No data to analyse.")
            return

        scores = [s.score for s in self.students]
        avg    = sum(scores) / len(scores)
        high   = max(scores)
        low    = min(scores)
    
        grades = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for s in self.students:
            grades[s.get_grade()] += 1

        failing = [s for s in self.students if s.get_grade() == "F"]

        print("\n  --- Analysis ---")
        print(f"  Total Students : {len(self.students)}")
        print(f"  Average Score  : {avg:.1f}")
        print(f"  Highest Score  : {high}")
        print(f"  Lowest Score   : {low}")
        print(f"  Grade Breakdown: {grades}")
        if failing:
            print("  Failing Students:")
            for s in failing:
                print(f"    - {s.name} (ID: {s.student_id}, Score: {s.score})")

    # ---------- SORT ----------
    def sort_by_score(self, descending=True):

        self.students.sort(key=lambda s: s.score, reverse=descending)

     # ---------- DUPLICATE CHECK ----------
    def id_exists(self, student_id):
        return any(s.student_id == student_id for s in self.students)
    
# ==========================================
# 5. TESTING FUNCTIONS
# ==========================================

def run_tests():
    print("\n========== RUNNING TESTS ==========")
    passed = 0
    failed= 0

    def check(description, condition):
        nonlocal passed, failed
        if condition:
            print(f"  [PASS]{description}")
            passed += 1
        else:
            print(f"  [FAIL]{description}")
            failed += 1

    # --- Email validation tests ---
    check("Valid email accepted",             validate_email("john@example.com"))
    check("Email without @ rejected",         not validate_email("johnexample.com"))
    check("Email without domain rejected",    not validate_email("john@"))

    # --- Student ID validation tests ---
    check("Valid student ID accepted",        validate_student_id("S12345"))
    check("ID with no letter rejected",       not validate_student_id("123456"))
    check("ID that is too short rejected",    not validate_student_id("S1234"))
    check("ID with two letters rejected",     not validate_student_id("SA1234"))

    # --- Score validation tests ---
    check("Score 0 accepted",                 validate_score("0") == 0)
    check("Score 100 accepted",               validate_score("100") == 100)
    check("Score 101 rejected",               validate_score("101") is None)
    check("Non-numeric score rejected",       validate_score("abc") is None)

    # --- Name validation tests ---
    check("Valid name accepted",              validate_name("Alice Smith"))
    check("Name with numbers rejected",       not validate_name("Alice123"))

    # --- Grade classification tests ---
    s = Student("Test", "test@test.com", "T00001", 75)
    check("Score 75 gives grade A",           s.get_grade() == "A")
    s.score = 55
    check("Score 55 gives grade C",           s.get_grade() == "C")
    s.score = 30
    check("Score 30 gives grade F",           s.get_grade() == "F")

     # --- StudentManager tests ---
    mgr = StudentManager()
    mgr.add_student("Alice", "alice@test.com", "A00001", 85)
    mgr.add_student("Bob",   "bob@test.com",   "B00002", 45)
    check("Add student works",                len(mgr.students) == 2)
    check("Duplicate ID detected",            mgr.id_exists("A00001"))
    check("Delete student works",             mgr.delete_student("B00002"))
    check("Student count after delete",       len(mgr.students) == 1)
    check("Edit student score works",         mgr.edit_student("A00001", "score", 90) and mgr.students[0].score == 90)

     # --- Regex search tests ---
    mgr2 = StudentManager()
    mgr2.add_student("Alice",   "alice@gmail.com",   "A11111", 70)
    mgr2.add_student("Bob",     "bob@outlook.com",   "B22222", 60)
    mgr2.add_student("Charlie", "charlie@gmail.com", "C33333", 50)
    results = mgr2.search_students("name", r"^A")
    check("Search by name starting with A returns 1 result",  len(results) == 1)
    results = mgr2.search_students("email", r"@gmail\.com$")
    check("Search emails ending in @gmail.com returns 2",     len(results) == 2)

    print(f"\n  Results: {passed} passed, {failed} failed.")
    print("====================================\n")

# ==========================================
# 6. HELPER: COLLECT INPUT WITH VALIDATION
# ==========================================

def get_validated_input(prompt, validator, error_message):
    while True:
        value = input(prompt).strip()
        result = validator(value)
        if result or result == 0:     # Allow 0 as a valid score
            return result if not isinstance(result, bool) else value
        print(f"  Error: {error_message}")

# ==========================================
# 7. MAIN PROGRAM (USER INTERFACE)
# ==========================================

def main():
    print("=" * 45)
    print("  Student Coursework Management System")
    print("=" * 45)

    manager = StudentManager()

    while True:
        print("\n  Main Menu")
        print("  ---------")
        print("  1. Add Student")
        print("  2. View All Students")
        print("  3. Search Students")
        print("  4. Edit Student")
        print("  5. Delete Student")
        print("  6. Analyse Data")
        print("  7. Sort by Score")
        print("  8. Save Data")
        print("  9. Load Data")
        print(" 10. Export Report")
        print(" 11. Run Tests")
        print("  0. Exit")

        choice = input("\n  Enter choice: ").strip()

        # ---- 1. ADD STUDENT ----
        if choice == "1":
            print("\n  -- Add Student --")

            name = get_validated_input(
                "  Name: ",
                validate_name,
                "Name must only contain letters and spaces."
            )

            email = get_validated_input(
                "  Email: ",
                validate_name,
                "Please enter a valid eamil (e.g. jphn@example.com)"
            )

            while True:
                sid = input("  Student ID (e.g. S98765): ").strip() 
                if not validate_student_id(sid):
                    print("  Error: ID must be one letter followed by 5 digits (e.g. S98765).")
                elif manager.id_exists(sid):
                    print("  Error: That Student ID already exists. IDs must be unique.")
                else:
                    break

            score = get_validated_input(
                "  Score (0-100): ",
                validate_score,
                "Score must be a whole number between 0 and 100."
            )

            manager.add_student(name, email, sid, score)

        # ---- 2. VIEW ALL STUDENTS ----
        elif choice == "2":
            manager.view_all()

        # ---- 3. SEARCH ----
        elif choice == "3":
            print("\n  -- Search Students --")    
            print("  Search by: (1) Name  (2) Email  (3) Student ID")
            field_choice = input("  Choose field: ").strip()
            field_map = {"1": "name", "2": "email", "3": "student_id"}

            if field_choice not in field_map:
                print("  Invalid choice.")
            else:
                field   = field_map[field_choice]
                pattern = input("  Enter search pattern: ").strip()
                results = manager.search_students(field, pattern)

                if results:
                    print(f"\n  Found {len(results)} result(s):")
                    for s in results:
                        print(f"    {s.get_details()}")
                else:
                    print("   No matches found.")

        # ---- 4. EDIT ----
        elif choice == "4":
            print("\n -- Edit Student --")
            sid = input("  Enter Student ID to edit: ").strip
            
            if not manager.id_exists(sid):
                print("  Error: Student ID not found.")
            else:
                print("  Edit: (1) Name  (2) Email  (3) Score")
                edit_choice = input("  Choose field to edit;").strip

                if edit_choice == "1":
                    new_val = get_validated_input(
                        "New name: ", validate_name,
                        "Name must only contain letters and spaces."
                    )
                    manager.edit_student(sid, "name", new_val)
                    print("  Name updated.")

                elif edit_choice == "2":
                    new_val = get_validated_input(
                        "  New email: ", validate_email,
                        "Please enter a valid email."
                    )
                    manager.edit_student(sid, "email", new_val)
                    print("  Email updated.")
                    
                elif edit_choice == "3":
                    new_val = get_validated_input(
                        "  New score (0-100): ", validate_score,
                        "Score must be a whole number between 0 and 100."
                    )
                    manager.edit_student(sid, "score", new_val)
                    print("  Score updated.")

                else:
                    print("  Invalid choice.")

        # ---- 5. DELETE ----
        elif choice == "5":
            print("\n  -- Delete Student -- ")
            sid = input("  Enter Student ID to delete: ").strip()
            confirm = input(f"  Are you sure you want to delete '{sid}'? (y/n): ").strip().lower()
            if confirm == "y":
                if manager.delete_student(sid):
                    print("  Student deleted.")
                else:
                    print("  Error: Student ID not found.")

            else: 
                print("  Delete cancelled.")

        # ---- 6. ANALYSE ----
        elif choice == "6":
            manager.analyse()
        
        # ---- 7. SORT ----
        elif choice == "7":
            print("\n  Sort order: (1) Highest first  (2) Lowest first")
            sort_choice = input("  Choose: ").strip()
            if sort_choice == "1":
                manager.sort_by_score(descending=True)
                print("  Sorted highest to lowest.")
            elif sort_choice == "2":
                manager.sort_by_score(descending=False)
                print("  Sorted lowest to highest.")
            else:
                print("  Invalid choice.")

        # ---- 8. SAVE ----
        elif choice == "8":
            save_to_file(manager.students)

        # ---- 9. LOAD ----
        elif choice == "9":
            confirm = input("  Loading will replace current data. Continue? (y/n): ").strip().lower()
            if confirm == "y":
                manager.students = load_from_file()

        # ---- 10. EXPORT REPORT ----
        elif choice == "10":
            export_report(manager.students)

        # ---- 11. RUN TESTS ----
        elif choice == "11":
            run_tests()

        # ---- 0. EXIT ----
        elif choice == "0":
            print("\n  Goodbye!")
            break

        else:
            print("  Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    main()       