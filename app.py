import os 
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")

CR_USERS = {
    "VANSH ARORA",
    "HARSIMRAT SUMMAN"
}



# ================= STUDENTS =================
students = {
    "28152500001": "ADITI SHARMA",
    "28152500002": "HARDILPREET KAUR",
    "28152500003": "RISHIKA SINGH",
    "28152500004": "VAIBHAV MEHRA",
    "28152500005": "HARJOT SINGH",
    "28152500006": "KHUSHI TALWAR",
    "28152500007": "EKAMJOT KAUR",
    "28152500008": "VEEBHUTI MAHAJAN",
    "28152500009": "BNEET KAUR",
    "28152500010": "SIFATJOT SINGH",
    "28152500011": "SEEYA SHARMA",
    "28152500012": "MUSKAAN KAUR",
    "28152500013": "SAKSHAM MANGOTRA",
    "28152500014": "KHUSHBOO",
    "28152500015": "ARSHNOOR KAUR",
    "28152500016": "KRISHNA SHARMA",
    "28152500017": "MUNISHWAR",
    "28152500018": "BALDEEP SINGH",
    "128152500019": "KARAN CHOUDHARY",
    "28152500020": "MOHITESHWAR SHARMA",
    "28152500021": "MEHTAAB PURI",
    "28152500022": "PARMEET SINGH",
    "28152500023": "LAVANYA JOSHI",
    "28152500024": "LOVENEET",
    "28152500025": "DAISY SHARMA",
    "28152500026": "KASHISH",
    "28152500027": "JASMINE KAUR",
    "28152500028": "HITAKSHI",
    "28152500029": "KHUSHI MAHAJAN",
    "28152500030": "ZORAVAR SINGH",
    "28152500031": "PRATHAM",
    "28152500032": "KASHVI TANEJA",
    "28152500033": "KRITIKA SINGLA",
    "28152500034": "HARSIMRAT SUMMAN",
    "28152500035": "SAMRIDHI",
    "28152500036": "VANSH ARORA",
    "28152500037": "USTATDEEP SINGH",
    "28152500038": "AAMANA",
    "28152500039": "SUMIT KUMAR"
}

# ================= DATABASE INIT =================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cur.execute("SELECT COUNT(*) FROM students")
    if cur.fetchone()[0] == 0:
        for roll, name in students.items():
            cur.execute(
                "INSERT INTO students (roll_no, name) VALUES (?, ?)",
                (roll, name)
            )

    conn.commit()
    conn.close()

init_db()

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("home.html")

# ===== STUDENT LOGIN =====
@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        roll_no = request.form.get("roll_no").strip()
        name = request.form.get("name", "").strip().upper()  # remove extra spaces and upper

        # convert stored name to upper before comparing
        if roll_no in students and students[roll_no].upper() == name:
            session["student_roll"] = roll_no
            session["student_name"] = students[roll_no]  # store original name
            return redirect("/student/dashboard")
        else:
            flash("Invalid Roll No or Name")

    return render_template("student_login.html")


# ===== STUDENT DASHBOARD =====
# ===== STUDENT DASHBOARD =====
# ===== STUDENT DASHBOARD =====
@app.route("/student/dashboard")
def student_dashboard():
    # ===== AUTH =====
    if "student_roll" not in session:
        return redirect("/student")
    



    roll_no = session.get("student_roll")
    name = session.get("student_name")

    # ===== PAGINATION =====
    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ===== TOTAL RECORD COUNT =====
    cur.execute(
        "SELECT COUNT(*) FROM attendance WHERE roll_no = ?",
        (roll_no,)
    )
    total_records = cur.fetchone()[0]
    total_pages = max((total_records + per_page - 1) // per_page, 1)
    #PAGINATION SETUP 
    page = request.args.get("page" , 1 , type = int )
    per_page = 10 
    offest = ( page - 1 ) * per_page


    # ===== FETCH PAGINATED RECORDS =====
    cur.execute("""
        SELECT subject, date, status
        FROM attendance
        WHERE roll_no = ?
        ORDER BY date DESC
        LIMIT ? OFFSET ?
    """, (roll_no, per_page, offset))
    records = cur.fetchall()
    

    # ===== FETCH ALL RECORDS FOR STATS =====
    cur.execute("""
        SELECT subject, date, status
        FROM attendance
        WHERE roll_no = ?
    """, (roll_no,))
    all_records = cur.fetchall()

    # ===== SUBJECT-WISE =====
    subject_totals = {}
    subject_present = {}
    present_count = 0
    absent_count = 0

    for subject, date, status in all_records:
        subject_totals[subject] = subject_totals.get(subject, 0) + 1
        if status == "Present":
            subject_present[subject] = subject_present.get(subject, 0) + 1
            present_count += 1
        else:
            absent_count += 1

    subject_labels = []
    subject_values = []

    for sub in subject_totals:
        total = subject_totals[sub]
        present = subject_present.get(sub, 0)
        percent = round((present / total) * 100, 2) if total else 0
        subject_labels.append(sub)
        subject_values.append(percent)

    if not subject_labels:
        subject_labels = ["No Data"]
        subject_values = [0]

    # ===== MONTHLY TREND =====
    monthly_totals = {}
    monthly_present = {}

    for subject, date, status in all_records:
        month = date[:7]
        monthly_totals[month] = monthly_totals.get(month, 0) + 1
        if status == "Present":
            monthly_present[month] = monthly_present.get(month, 0) + 1

    monthly_labels = []
    monthly_values = []

    for m in monthly_totals:
        total = monthly_totals[m]
        present = monthly_present.get(m, 0)
        percent = round((present / total) * 100, 2) if total else 0
        monthly_labels.append(m)
        monthly_values.append(percent)

    if not monthly_labels:
        monthly_labels = ["No Data"]
        monthly_values = [0]

    # ===== OVERALL =====
    total_classes = present_count + absent_count
    overall_percentage = round(
        (present_count / total_classes) * 100, 2
    ) if total_classes else 0

    conn.close()

    # ===== RENDER =====
    return render_template(
        
        "student_dashboard.html",
        roll_no=roll_no,
        name=name,

        records=records,
        page=page,
        total_pages=total_pages,

        subject_labels=subject_labels,
        subject_values=subject_values,

        monthly_labels=monthly_labels,
        monthly_values=monthly_values,

        present_count=present_count,
        absent_count=absent_count,
        overall_percentage=overall_percentage
    )

    # ================= FETCH ATTENDANCE =================
    cur.execute("""
        SELECT subject, date, status
        FROM attendance
        WHERE roll_no = ?
        ORDER BY date ASC
    """, (roll_no,))
    records = cur.fetchall() or []

    # ================= SUBJECT-WISE CALCULATION =================
    subject_totals = {}
    subject_present = {}

    present_count = 0
    absent_count = 0

    for subject, date, status in records:
        subject_totals[subject] = subject_totals.get(subject, 0) + 1

        if status == "Present":
            subject_present[subject] = subject_present.get(subject, 0) + 1
            present_count += 1
        else:
            absent_count += 1

    subject_labels = list(subject_totals.keys())
    subject_values = []

    for sub in subject_labels:
        total = subject_totals[sub]
        present = subject_present.get(sub, 0)
        percent = round((present / total) * 100, 2) if total else 0
        subject_values.append(percent)

    # ===== SAFETY DEFAULTS (NO DATA CASE) =====
    if not subject_labels:
        subject_labels = ["No Data"]
        subject_values = [0]



    # ================= FETCH ATTENDANCE =================
    cur.execute("""
        SELECT subject, date, status
        FROM attendance
        WHERE roll_no = ?
        ORDER BY date ASC
    """, (roll_no,))
    records = cur.fetchall()

    # ================= SUBJECT-WISE CALCULATION =================
    subject_totals = {}
    subject_present = {}

    present_count = 0
    absent_count = 0

    for subject, date, status in records:
        subject_totals[subject] = subject_totals.get(subject, 0) + 1
        if status == "Present":
            subject_present[subject] = subject_present.get(subject, 0) + 1
            present_count += 1
        else:
            absent_count += 1

    subject_labels = list(subject_totals.keys())
    subject_values = [
        round((subject_present.get(sub, 0) / subject_totals[sub]) * 100, 2)
        for sub in subject_labels
    ]

    # ================= MONTHLY TREND =================
    monthly_totals = {}
    monthly_present = {}

    for subject, date, status in records:
        month = date[:7]  # YYYY-MM
        monthly_totals[month] = monthly_totals.get(month, 0) + 1
        if status == "Present":
            monthly_present[month] = monthly_present.get(month, 0) + 1

    monthly_labels = list(monthly_totals.keys())
    monthly_values = [
        round((monthly_present.get(m, 0) / monthly_totals[m]) * 100, 2)
        for m in monthly_labels
    ]

    # ================= OVERALL PERCENTAGE =================
    total_classes = present_count + absent_count
    overall_percentage = round((present_count / total_classes) * 100, 2) if total_classes else 0

    conn.close()

    # ================= RENDER =================
    return render_template(
        "student_dashboard.html",
        roll_no=roll_no,
        name=name,
        records=records,

        subject_labels=subject_labels,
        subject_values=subject_values,

        monthly_labels=monthly_labels,
        monthly_values=monthly_values,

        present_count=present_count,
        absent_count=absent_count,
        overall_percentage=overall_percentage
    )


@app.route("/cr", methods=["GET", "POST"])
def cr():
    if request.method == "POST":
        name = request.form.get("name", "").upper().strip()
        password = request.form.get("password")

        if name not in CR_USERS:
            flash("You are not authorized as CR")
            return redirect(url_for("cr"))

        if password != "HARSIMRAT@985":
            flash("Invalid CR password")
            return redirect(url_for("cr"))

        # ✅ SUCCESS → SET SESSION
        session.clear()
        session["role"] = "CR"
        session["cr_name"] = name

        return redirect(url_for("cr_dashboard"))

    return render_template("cr_login.html")


# ================= CR DASHBOARD =================
@app.route("/cr/dashboard", methods=["GET","POST"])
def cr_dashboard():

    # 🚫 BLOCK STUDENTS
    if session.get("role") != "CR":
        flash("Access denied: CR only")
        return redirect(url_for("home"))

    # ---- existing code below stays untouched ----


    if request.method == "POST":
        date = request.form.get("attendance_date")
        subject = request.form.get("subject")

        if not date or not subject:
            flash("Select date and subject before submitting!")
            return redirect(url_for("cr_dashboard"))

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        for roll in students.keys():
            status = request.form.get(f"status_{roll}")
            if status:
                cur.execute(
                    "SELECT id FROM attendance WHERE roll_no=? AND subject=? AND date=?",
                    (roll, subject, date)
                )
                existing = cur.fetchone()

                if existing:
                    cur.execute(
                        "UPDATE attendance SET status=? WHERE id=?",
                        (status, existing[0])
                    )
                else:
                    cur.execute(
                        "INSERT INTO attendance (roll_no, subject, date, status) VALUES (?, ?, ?, ?)",
                        (roll, subject, date, status)
                    )

        conn.commit()
        conn.close()
        flash("Attendance submitted successfully!")
        return redirect(url_for("cr_dashboard"))

    return render_template("cr_dashboard.html", students=students)

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



