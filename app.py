from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from models import db, Admin, Student, Course
from config import *
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

with app.app_context():
    db.create_all()

    if not Admin.query.first():
        db.session.add(Admin(username="user123", password="user@123"))

    course_names = [
        "Python", "Web Development", "Data Science", "AI Engineer",
        "Computer Science", "Bachlor of Science", "Civil Engineering",
        "Electrical Engineering", "Mechanical Engineering", "Software Engineering",
        "Cyber Security", "Information Technology", "Business Administration",
        "Graphic Design", "Marketing", "Finance", "AI/ML Engineer"
    ]

    for name in course_names:
        if not Course.query.filter_by(name=name).first():
            db.session.add(Course(name=name))
    
    db.session.commit()

# ---------- AUTH ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Admin.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ---------- STUDENTS ----------
@app.route("/dashboard")
@login_required
def dashboard():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")

    query = Student.query
    if search:
        query = query.filter(Student.name.ilike(f"%{search}%"))

    students = query.paginate(page=page, per_page=5)

    total_students = Student.query.count()
    total_courses = Course.query.count()

    return render_template(
        "dashboard.html",
        students=students,
        total_students=total_students,
        total_courses=total_courses,
        search=search
    )

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_student():
    courses = Course.query.all()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        course_id = request.form["course"]

        existing_student = Student.query.filter_by(
            name=name,
            course_id=course_id
        ).first()

        if existing_student:
            flash("Student already exists in this course ❌")
            return redirect(url_for("add_student"))

        db.session.add(Student(name=name, age=age, course_id=course_id))
        db.session.commit()
        flash("Student added successfully ✅")
        return redirect(url_for("dashboard"))

    return render_template("add_student.html", courses=courses)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    courses = Course.query.all()

    if request.method == "POST":
        student.name = request.form["name"]
        student.age = request.form["age"]
        student.course_id = request.form["course"]
        db.session.commit()
        flash("Student updated successfully")
        return redirect(url_for("dashboard"))

    return render_template("edit_student.html", student=student, courses=courses)

@app.route("/delete/<int:id>")
@login_required
def delete_student(id):
    db.session.delete(Student.query.get(id))
    db.session.commit()
    flash("Student deleted")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run()
