
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# File to store student records
FILE_NAME = "students.json"

SUBJECTS = ["Python", "DBMS", "Java", "C++", "Computer Networks"]

students = []


# Load students from file
def load_students():
    global students

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                students = json.load(file)
        except (json.JSONDecodeError, OSError):
            students = []
    else:
        students = []


# Save students to file
def save_students():
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


# Calculate percentage
def calculate_percentage(marks):
    return sum(marks) / len(marks)


# Calculate grade
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


# Clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)

    for entry in marks_entries:
        entry.delete(0, tk.END)

    search_entry.delete(0, tk.END)
    student_table.selection_remove(student_table.selection())


# Get marks from input fields
def get_marks():
    marks = []

    for entry in marks_entries:
        value = entry.get().strip()

        if value == "":
            raise ValueError("Please enter marks for all subjects.")

        mark = float(value)

        if mark < 0 or mark > 100:
            raise ValueError("Marks must be between 0 and 100.")

        marks.append(mark)

    return marks


# Add student
def add_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()

    if not name or not roll:
        messagebox.showwarning(
            "Missing Information",
            "Please enter student name and roll number."
        )
        return

    if any(s["roll"].lower() == roll.lower() for s in students):
        messagebox.showerror(
            "Duplicate Roll Number",
            "This roll number already exists."
        )
        return

    try:
        marks = get_marks()

    except ValueError as error:
        messagebox.showerror("Invalid Marks", str(error))
        return

    student = {
        "name": name,
        "roll": roll,
        "marks": marks
    }

    students.append(student)
    save_students()
    refresh_table()
    clear_fields()

    messagebox.showinfo("Success", "Student added successfully!")


# Refresh student table
def refresh_table():
    for item in student_table.get_children():
        student_table.delete(item)

    for student in students:
        marks = student["marks"]
        total = sum(marks)
        percentage = calculate_percentage(marks)
        grade = calculate_grade(percentage)

        student_table.insert(
            "",
            tk.END,
            values=(
                student["roll"],
                student["name"],
                f"{total:g}/500",
                f"{percentage:.2f}%",
                grade
            )
        )


# Search student
def search_student():
    query = search_entry.get().strip().lower()

    if not query:
        messagebox.showwarning(
            "Search",
            "Please enter a name or roll number."
        )
        return

    for item in student_table.get_children():
        student_table.delete(item)

    found = False

    for student in students:
        if (
            query in student["name"].lower()
            or query == student["roll"].lower()
        ):
            marks = student["marks"]
            total = sum(marks)
            percentage = calculate_percentage(marks)
            grade = calculate_grade(percentage)

            student_table.insert(
                "",
                tk.END,
                values=(
                    student["roll"],
                    student["name"],
                    f"{total:g}/500",
                    f"{percentage:.2f}%",
                    grade
                )
            )

            found = True

    if not found:
        messagebox.showinfo("Search Result", "No student found.")


# Show all students
def show_all_students():
    refresh_table()


# Select student from table
def select_student(event=None):
    selected = student_table.selection()

    if not selected:
        return

    values = student_table.item(selected[0], "values")
    roll = str(values[0])

    for student in students:
        if student["roll"].lower() == roll.lower():
            clear_fields()

            name_entry.insert(0, student["name"])
            roll_entry.insert(0, student["roll"])

            for entry, mark in zip(marks_entries, student["marks"]):
                entry.insert(0, str(mark))

            break


# Update student
def update_student():
    roll = roll_entry.get().strip()

    if not roll:
        messagebox.showwarning(
            "Update Student",
            "Select a student or enter their roll number."
        )
        return

    student = next(
        (s for s in students if s["roll"].lower() == roll.lower()),
        None
    )

    if student is None:
        messagebox.showerror("Error", "Student not found.")
        return

    name = name_entry.get().strip()

    if not name:
        messagebox.showwarning("Error", "Please enter student name.")
        return

    try:
        marks = get_marks()

    except ValueError as error:
        messagebox.showerror("Invalid Marks", str(error))
        return

    student["name"] = name
    student["marks"] = marks

    save_students()
    refresh_table()
    clear_fields()

    messagebox.showinfo("Success", "Student updated successfully!")


# Delete student
def delete_student():
    selected = student_table.selection()

    if selected:
        roll = str(student_table.item(selected[0], "values")[0])
    else:
        roll = roll_entry.get().strip()

    if not roll:
        messagebox.showwarning(
            "Delete Student",
            "Select a student or enter their roll number."
        )
        return

    student = next(
        (s for s in students if s["roll"].lower() == roll.lower()),
        None
    )

    if student is None:
        messagebox.showerror("Error", "Student not found.")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete student {student['name']}?"
    )

    if confirm:
        students.remove(student)
        save_students()
        refresh_table()
        clear_fields()

        messagebox.showinfo("Success", "Student deleted successfully!")


# Display student result
def show_result():
    roll = roll_entry.get().strip()

    selected = student_table.selection()

    if selected:
        roll = str(student_table.item(selected[0], "values")[0])

    if not roll:
        messagebox.showwarning(
            "Student Result",
            "Select a student or enter their roll number."
        )
        return

    student = next(
        (s for s in students if s["roll"].lower() == roll.lower()),
        None
    )

    if student is None:
        messagebox.showerror("Error", "Student not found.")
        return

    marks = student["marks"]
    total = sum(marks)
    percentage = calculate_percentage(marks)
    grade = calculate_grade(percentage)

    result = (
        f"Student Name: {student['name']}\n"
        f"Roll Number: {student['roll']}\n\n"
    )

    for subject, mark in zip(SUBJECTS, marks):
        result += f"{subject}: {mark:g}/100\n"

    result += (
        f"\nTotal Marks: {total:g}/500"
        f"\nPercentage: {percentage:.2f}%"
        f"\nGrade: {grade}"
    )

    messagebox.showinfo("Student Result", result)


# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("1050x720")
root.minsize(900, 650)
root.configure(bg="#f0f4f8")


# Styles
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    rowheight=28,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)

style.configure(
    "TButton",
    font=("Arial", 10),
    padding=6
)


# Heading
title_label = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#1f3a5f",
    fg="white",
    pady=15
)
title_label.pack(fill="x")


# Input form
form_frame = tk.LabelFrame(
    root,
    text="Student Information",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=10,
    bg="#f0f4f8"
)
form_frame.pack(fill="x", padx=20, pady=15)


tk.Label(
    form_frame, text="Student Name:",
    bg="#f0f4f8"
).grid(row=0, column=0, padx=8, pady=8, sticky="w")

name_entry = ttk.Entry(form_frame, width=25)
name_entry.grid(row=0, column=1, padx=8, pady=8)


tk.Label(
    form_frame, text="Roll Number:",
    bg="#f0f4f8"
).grid(row=0, column=2, padx=8, pady=8, sticky="w")

roll_entry = ttk.Entry(form_frame, width=25)
roll_entry.grid(row=0, column=3, padx=8, pady=8)


marks_entries = []

for index, subject in enumerate(SUBJECTS):
    row = 1 + index // 3
    column = (index % 3) * 2

    tk.Label(
        form_frame,
        text=subject + " Marks:",
        bg="#f0f4f8"
    ).grid(row=row, column=column, padx=8, pady=8, sticky="w")

    entry = ttk.Entry(form_frame, width=12)
    entry.grid(row=row, column=column + 1, padx=8, pady=8)

    marks_entries.append(entry)


# Buttons
button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=5)

ttk.Button(
    button_frame, text="Add Student",
    command=add_student
).grid(row=0, column=0, padx=5, pady=5)

ttk.Button(
    button_frame, text="Update Student",
    command=update_student
).grid(row=0, column=1, padx=5, pady=5)

ttk.Button(
    button_frame, text="Delete Student",
    command=delete_student
).grid(row=0, column=2, padx=5, pady=5)

ttk.Button(
    button_frame, text="Show Result",
    command=show_result
).grid(row=0, column=3, padx=5, pady=5)

ttk.Button(
    button_frame, text="Clear Fields",
    command=clear_fields
).grid(row=0, column=4, padx=5, pady=5)


# Search area
search_frame = tk.LabelFrame(
    root,
    text="Search Student by Name or Roll Number",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10,
    bg="#f0f4f8"
)
search_frame.pack(fill="x", padx=20, pady=10)

search_entry = ttk.Entry(search_frame, width=35)
search_entry.pack(side="left", padx=10)

ttk.Button(
    search_frame, text="Search",
    command=search_student
).pack(side="left", padx=5)

ttk.Button(
    search_frame, text="Show All Students",
    command=show_all_students
).pack(side="left", padx=5)


# Student table
table_frame = tk.LabelFrame(
    root,
    text="Student Records",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=10,
    bg="#f0f4f8"
)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("Roll", "Name", "Total", "Percentage", "Grade")

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

student_table.heading("Roll", text="Roll Number")
student_table.heading("Name", text="Student Name")
student_table.heading("Total", text="Total Marks")
student_table.heading("Percentage", text="Percentage")
student_table.heading("Grade", text="Grade")

student_table.column("Roll", width=120, anchor="center")
student_table.column("Name", width=250, anchor="center")
student_table.column("Total", width=150, anchor="center")
student_table.column("Percentage", width=150, anchor="center")
student_table.column("Grade", width=100, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=student_table.yview
)

student_table.configure(yscrollcommand=scrollbar.set)

student_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

student_table.bind("<<TreeviewSelect>>", select_student)


# Load saved data and show records
load_students()
refresh_table()


# Start application
root.mainloop()

