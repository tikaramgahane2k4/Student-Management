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
        query = query.filter(
            (Student.name.ilike(f"%{search}%")) | 
            (Student.email.ilike(f"%{search}%"))
        )

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
        email = request.form["email"]
        age = request.form["age"]
        course_id = request.form["course"]

        # Validate required fields
        if not name or not email or not age or not course_id:
            flash("All fields are required!", "error")
            return render_template("add_student.html", courses=courses, form=request.form)

        # Validate email format (simple regex or check)
        if "@" not in email or "." not in email:
            flash("Invalid email format!", "error")
            return render_template("add_student.html", courses=courses, form=request.form)

        # Check for duplicates
        existing_email = Student.query.filter_by(email=email).first()
        if existing_email:
            flash("Student with this email already exists!", "error")
            return render_template("add_student.html", courses=courses, form=request.form)

        existing_in_course = Student.query.filter_by(name=name, course_id=course_id).first()
        if existing_in_course:
             flash("Student already exists in this course!", "error")
             return render_template("add_student.html", courses=courses, form=request.form)

        try:
            db.session.add(Student(name=name, email=email, age=age, course_id=course_id))
            db.session.commit()
            flash("Student added successfully ✅", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding student: {str(e)}", "error")
            return render_template("add_student.html", courses=courses, form=request.form)

    return render_template("add_student.html", courses=courses)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    courses = Course.query.all()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]
        course_id = request.form["course"]

        if not name or not email or not age or not course_id:
            flash("All fields are required!", "error")
            return render_template("edit_student.html", student=student, courses=courses)

        # Check unique email (exclude current student)
        existing_email = Student.query.filter(Student.email == email, Student.id != id).first()
        if existing_email:
            flash("Email already taken by another student!", "error")
            return render_template("edit_student.html", student=student, courses=courses)

        try:
            student.name = name
            student.email = email
            student.age = age
            student.course_id = course_id
            db.session.commit()
            flash("Student updated successfully ✅", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating student: {str(e)}", "error")
            return render_template("edit_student.html", student=student, courses=courses)

    return render_template("edit_student.html", student=student, courses=courses)

@app.route("/delete/<int:id>")
@login_required
def delete_student(id):
    try:
        db.session.delete(Student.query.get_or_404(id))
        db.session.commit()
        flash("Student deleted successfully 🗑️", "success")
    except Exception as e:
        flash(f"Error deleting student: {str(e)}", "error")
    return redirect(url_for("dashboard"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run()
