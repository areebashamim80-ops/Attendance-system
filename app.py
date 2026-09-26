from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =======================
# Database Model
# =======================

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    student_class = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    present = db.Column(db.Integer, default=0)
    absent = db.Column(db.Integer, default=0)

# =======================
# Login
# =======================

@app.route("/")
def login():
    return render_template("login.html")

# =======================
# Dashboard
# =======================

@app.route("/dashboard")
def dashboard():

    students = Student.query.all()

    total_students = len(students)

    total_present = sum(student.present for student in students)

    total_absent = sum(student.absent for student in students)

    return render_template(
        "dashboard.html",
        students=students,
        total_students=total_students,
        total_present=total_present,
        total_absent=total_absent
    )

# =======================
# Add Student
# =======================

@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        student = Student(
            roll=request.form["roll"],
            name=request.form["name"],
            department=request.form["department"],
            student_class=request.form["student_class"],
            email=request.form["email"],
            phone=request.form["phone"]
        )

        db.session.add(student)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("add_student.html")

# =======================
# Student List
# =======================

@app.route("/students")
def students():

    students = Student.query.all()

    return render_template(
        "student_list.html",
        students=students
    )

# =======================
# Attendance
# =======================

@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    students = Student.query.all()

    if request.method == "POST":

        for student in students:

            status = request.form.get(f"attendance_{student.id}")

            if status == "present":
                student.present += 1

            elif status == "absent":
                student.absent += 1

        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template(
        "attendance.html",
        students=students
    )
    # =======================
# Report
# =======================

@app.route("/report")
def report():

    students = Student.query.all()

    return render_template(
        "report.html",
        students=students
    )


# =======================
# Mark Present
# =======================

@app.route("/present/<int:id>")
def present(id):

    student = Student.query.get_or_404(id)

    student.present += 1

    db.session.commit()

    return redirect(url_for("dashboard"))


# =======================
# Mark Absent
# =======================

@app.route("/absent/<int:id>")
def absent(id):

    student = Student.query.get_or_404(id)

    student.absent += 1

    db.session.commit()

    return redirect(url_for("dashboard"))


# =======================
# Delete Student
# =======================

@app.route("/delete/<int:id>")
def delete(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    return redirect(url_for("students"))


# =======================
# Edit Student
# =======================

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        student.roll = request.form["roll"]
        student.name = request.form["name"]
        student.department = request.form["department"]
        student.student_class = request.form["student_class"]
        student.email = request.form["email"]
        student.phone = request.form["phone"]

        db.session.commit()

        return redirect(url_for("students"))

    return render_template(
        "add_student.html",
        student=student
    )


# =======================
# Create Database & Run App
# =======================
# =======================
# Logout
# =======================

@app.route("/logout")
def logout():
    return redirect(url_for("login"))
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)