
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime

# ---------------- APP SETTINGS ----------------

BG = "#F1F5F9"
NAVY = "#172554"
BLUE = "#2563EB"
WHITE = "#FFFFFF"
GREEN = "#15803D"
ORANGE = "#C2410C"
RED = "#B91C1C"

students = []
next_id = 1


# ---------------- PERFORMANCE ANALYZER ----------------

def predict_performance(marks, attendance):
    # Transparent scoring formula, not trained machine learning
    score = (marks * 0.70) + (attendance * 0.30)

    if score >= 75:
        status = "Excellent"
        suggestion = "Maintain consistency and try advanced learning."
    elif score >= 60:
        status = "Good"
        suggestion = "Keep practising and revise difficult topics."
    elif score >= 40:
        status = "Needs Improvement"
        suggestion = "Follow a study timetable and practise regularly."
    else:
        status = "At Risk"
        suggestion = "Seek teacher support and make a study plan."

    return round(score, 2), status, suggestion


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("AI Student Performance Predictor")
root.geometry("1120x760")
root.minsize(900, 650)
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=NAVY,
    rowheight=30,
    fieldbackground=WHITE,
    font=("Arial", 10)
)
style.configure(
    "Treeview.Heading",
    background=NAVY,
    foreground=WHITE,
    font=("Arial", 10, "bold")
)
style.map(
    "Treeview",
    background=[("selected", "#BFDBFE")],
    foreground=[("selected", NAVY)]
)

# ---------------- HEADER ----------------

header = tk.Frame(root, bg=NAVY, padx=20, pady=17)
header.pack(fill="x")

tk.Label(
    header,
    text="AI STUDENT PERFORMANCE PREDICTOR",
    font=("Arial", 19, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(anchor="w")

tk.Label(
    header,
    text="Academic Analytics | Student Management | Reports",
    font=("Arial", 10),
    bg=NAVY,
    fg="#BFDBFE"
).pack(anchor="w", pady=(5, 0))


# ---------------- DASHBOARD CARDS ----------------

cards = tk.Frame(root, bg=BG, padx=15, pady=12)
cards.pack(fill="x")


def make_card(parent, title, color):
    frame = tk.Frame(parent, bg=WHITE, padx=14, pady=10,
                     highlightbackground="#CBD5E1",
                     highlightthickness=1)

    tk.Label(
        frame, text=title, bg=WHITE, fg="#64748B",
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    value = tk.Label(
        frame, text="0", bg=WHITE, fg=color,
        font=("Arial", 21, "bold")
    )
    value.pack(anchor="w", pady=(6, 0))

    return frame, value


card1, total_value = make_card(cards, "TOTAL STUDENTS", BLUE)
card2, marks_value = make_card(cards, "AVERAGE MARKS", GREEN)
card3, attendance_value = make_card(cards, "AVG ATTENDANCE", ORANGE)
card4, risk_value = make_card(cards, "NEED SUPPORT", RED)

for card in (card1, card2, card3, card4):
    card.pack(side="left", fill="x", expand=True, padx=5)


# ---------------- MAIN CONTENT ----------------

content = tk.Frame(root, bg=BG, padx=15)
content.pack(fill="both", expand=True)

left = tk.Frame(content, bg=WHITE, padx=15, pady=15,
                highlightbackground="#CBD5E1",
                highlightthickness=1)
left.pack(side="left", fill="y", padx=(0, 12))

tk.Label(
    left, text="STUDENT DETAILS",
    bg=WHITE, fg=NAVY,
    font=("Arial", 12, "bold")
).pack(anchor="w", pady=(0, 12))


def create_field(label_text):
    tk.Label(
        left, text=label_text, bg=WHITE,
        fg="#334155", font=("Arial", 10, "bold")
    ).pack(anchor="w", pady=(7, 3))

    entry = tk.Entry(
        left, font=("Arial", 11), width=27,
        relief="solid", bd=1
    )
    entry.pack(fill="x", ipady=5)
    return entry


name_entry = create_field("Student Name")
roll_entry = create_field("Roll Number")
marks_entry = create_field("Average Marks (0-100)")
attendance_entry = create_field("Attendance Percentage (0-100)")


# ---------------- RESULTS AREA ----------------

right = tk.Frame(content, bg=BG)
right.pack(side="left", fill="both", expand=True)

result_box = tk.Frame(right, bg=WHITE, padx=12, pady=10,
                      highlightbackground="#CBD5E1",
                      highlightthickness=1)
result_box.pack(fill="x", pady=(0, 10))

tk.Label(
    result_box, text="PERFORMANCE ANALYSIS",
    bg=WHITE, fg=NAVY, font=("Arial", 11, "bold")
).pack(anchor="w")

result_label = tk.Label(
    result_box,
    text="Add a student to view performance analysis.",
    bg=WHITE, fg="#475569",
    font=("Arial", 10), justify="left",
    wraplength=520
)
result_label.pack(anchor="w", pady=(7, 0))


# ---------------- STUDENT TABLE ----------------

table_frame = tk.Frame(right, bg=WHITE)
table_frame.pack(fill="both", expand=True)

columns = (
    "id", "name", "roll", "marks",
    "attendance", "score", "status"
)

tree = ttk.Treeview(
    table_frame, columns=columns,
    show="headings", height=10
)

headings = {
    "id": "ID",
    "name": "Student Name",
    "roll": "Roll No.",
    "marks": "Marks",
    "attendance": "Attendance",
    "score": "Score",
    "status": "Prediction"
}

widths = {
    "id": 42, "name": 125, "roll": 75,
    "marks": 65, "attendance": 85,
    "score": 65, "status": 135
}

for col in columns:
    tree.heading(col, text=headings[col])
    tree.column(col, width=widths[col], anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame, orient="vertical", command=tree.yview
)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# ---------------- DASHBOARD UPDATE ----------------

def update_dashboard():
    count = len(students)
    total_value.config(text=str(count))

    if count == 0:
        marks_value.config(text="0.0")
        attendance_value.config(text="0.0%")
        risk_value.config(text="0")
    else:
        avg_marks = sum(s["marks"] for s in students) / count
        avg_attendance = sum(s["attendance"] for s in students) / count
        support = sum(
            1 for s in students
            if s["status"] in ("Needs Improvement", "At Risk")
        )

        marks_value.config(text=f"{avg_marks:.1f}")
        attendance_value.config(text=f"{avg_attendance:.1f}%")
        risk_value.config(text=str(support))


def refresh_table():
    for item in tree.get_children():
        tree.delete(item)

    for s in students:
        tree.insert(
            "", "end",
            values=(
                s["id"], s["name"], s["roll"],
                f'{s["marks"]:.1f}',
                f'{s["attendance"]:.1f}%',
                f'{s["score"]:.1f}',
                s["status"]
            )
        )

    update_dashboard()


# ---------------- ADD STUDENT ----------------

def add_student():
    global next_id

    name = name_entry.get().strip()
    roll = roll_entry.get().strip()

    if not name or not roll:
        messagebox.showwarning(
            "Missing Details",
            "Please enter both student name and roll number."
        )
        return

    try:
        marks = float(marks_entry.get())
        attendance = float(attendance_entry.get())
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Marks and attendance must be numbers."
        )
        return

    if not (0 <= marks <= 100 and 0 <= attendance <= 100):
        messagebox.showerror(
            "Invalid Range",
            "Marks and attendance must be between 0 and 100."
        )
        return

    if any(s["roll"].lower() == roll.lower() for s in students):
        messagebox.showerror(
            "Duplicate Roll Number",
            "This roll number already exists."
        )
        return

    score, status, suggestion = predict_performance(
        marks, attendance
    )

    student = {
        "id": next_id,
        "name": name,
        "roll": roll,
        "marks": marks,
        "attendance": attendance,
        "score": score,
        "status": status,
        "suggestion": suggestion
    }

    students.append(student)
    next_id += 1

    refresh_table()
    clear_fields()

    result_label.config(
        text=f"Student: {name}\n"
             f"Estimated score: {score}/100\n"
             f"Status: {status}\n"
             f"Suggestion: {suggestion}"
    )


# ---------------- CLEAR FORM ----------------

def clear_fields():
    for entry in (
        name_entry, roll_entry,
        marks_entry, attendance_entry
    ):
        entry.delete(0, tk.END)


def clear_form():
    clear_fields()
    result_label.config(
        text="Enter student details and click Add Student."
    )


# ---------------- DELETE STUDENT ----------------

def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showinfo(
            "Select Student",
            "Please select a student from the table first."
        )
        return

    item = tree.item(selected[0])
    student_id = int(item["values"][0])

    if messagebox.askyesno(
        "Confirm Delete",
        "Delete the selected student record?"
    ):
        students[:] = [
            s for s in students if s["id"] != student_id
        ]
        refresh_table()
        result_label.config(text="Selected record deleted.")


# ---------------- ANALYZE SELECTED STUDENT ----------------

def analyze_selected(event=None):
    selected = tree.selection()

    if not selected:
        return

    values = tree.item(selected[0])["values"]
    student_id = int(values[0])

    student = next(
        (s for s in students if s["id"] == student_id),
        None
    )

    if student:
        result_label.config(
            text=f"Student: {student['name']}\n"
                 f"Marks: {student['marks']:.1f}/100\n"
                 f"Attendance: {student['attendance']:.1f}%\n"
                 f"Estimated score: {student['score']:.1f}/100\n"
                 f"Status: {student['status']}\n"
                 f"Suggestion: {student['suggestion']}"
        )


tree.bind("<<TreeviewSelect>>", analyze_selected)


# ---------------- CSV EXPORT ----------------

def export_csv():
    if not students:
        messagebox.showinfo(
            "No Data", "Add student records before exporting."
        )
        return

    filename = filedialog.asksaveasfilename(
        title="Save Student Report",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="student_performance_report.csv"
    )

    if not filename:
        return

    try:
        with open(
            filename, "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.writer(file)

            writer.writerow([
                "ID", "Student Name", "Roll Number",
                "Marks", "Attendance", "Estimated Score",
                "Status", "Suggestion"
            ])

            for s in students:
                writer.writerow([
                    s["id"], s["name"], s["roll"],
                    s["marks"], s["attendance"], s["score"],
                    s["status"], s["suggestion"]
                ])

        messagebox.showinfo(
            "Export Successful",
            "Student report saved successfully!"
        )

    except OSError as error:
        messagebox.showerror(
            "Save Error", str(error)
        )


# ---------------- PERFORMANCE CHART ----------------

def show_chart():
    if not students:
        messagebox.showinfo(
            "No Data", "Add students before viewing the chart."
        )
        return

    window = tk.Toplevel(root)
    window.title("Performance Analytics")
    window.geometry("620x440")
    window.configure(bg=BG)

    tk.Label(
        window, text="STUDENT PERFORMANCE CHART",
        font=("Arial", 15, "bold"),
        bg=BG, fg=NAVY
    ).pack(pady=15)

    canvas = tk.Canvas(
        window, width=570, height=310,
        bg=WHITE, highlightthickness=1,
        highlightbackground="#CBD5E1"
    )
    canvas.pack(padx=15, pady=5, fill="both", expand=True)

    canvas.create_text(
        285, 20, text="Estimated Performance Score (0-100)",
        fill=NAVY, font=("Arial", 10, "bold")
    )

    chart_students = students[-8:]
    chart_width = 520
    start_x = 35
    base_y = 250
    bar_width = min(42, chart_width // len(chart_students) - 8)
    gap = (chart_width - len(chart_students) * bar_width) / (
        len(chart_students) + 1
    )

    for mark in (0, 25, 50, 75, 100):
        y = base_y - mark * 2
        canvas.create_line(
            35, y, 550, y, fill="#E2E8F0"
        )
        canvas.create_text(
            20, y, text=str(mark),
            fill="#475569", font=("Arial", 8)
        )

    for i, student in enumerate(chart_students):
        x = start_x + gap + i * (bar_width + gap)
        height = student["score"] * 2
        y = base_y - height

        color = (
            GREEN if student["score"] >= 75
            else BLUE if student["score"] >= 60
            else ORANGE if student["score"] >= 40
            else RED
        )

        canvas.create_rectangle(
            x, y, x + bar_width, base_y,
            fill=color, outline=""
        )
        canvas.create_text(
            x + bar_width / 2, y - 10,
            text=f'{student["score"]:.0f}',
            fill=NAVY, font=("Arial", 8, "bold")
        )
        canvas.create_text(
            x + bar_width / 2, base_y + 17,
            text=student["roll"][:7],
            fill=NAVY, font=("Arial", 8)
        )

    tk.Label(
        window,
        text="Showing up to the latest 8 students. Labels show roll numbers.",
        bg=BG, fg="#475569", font=("Arial", 9)
    ).pack(pady=8)


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(root, bg=BG, padx=15, pady=12)
button_frame.pack(fill="x")

def make_button(parent, text, command, color):
    return tk.Button(
        parent, text=text, command=command,
        bg=color, fg=WHITE, activebackground=color,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat", cursor="hand2",
        padx=12, pady=9
    )

make_button(
    button_frame, "Add Student", add_student, BLUE
).pack(side="left", padx=4)

make_button(
    button_frame, "Clear Form", clear_form, "#475569"
).pack(side="left", padx=4)

make_button(
    button_frame, "Delete Selected", delete_student, RED
).pack(side="left", padx=4)

make_button(
    button_frame, "View Chart", show_chart, GREEN
).pack(side="left", padx=4)

make_button(
    button_frame, "Export CSV", export_csv, "#6D28D9"
).pack(side="left", padx=4)

footer = tk.Label(
    root,
    text="Academic support tool | Predictions are estimates, not guarantees.",
    bg=BG, fg="#64748B", font=("Arial", 9)
)
footer.pack(pady=(0, 8))

root.mainloop()
