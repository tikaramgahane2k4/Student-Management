from app import app, db
from models import Admin, Course

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Create default admin
    if not Admin.query.first():
        db.session.add(Admin(username="user123", password="user@123"))
        
    # Create default courses
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
    print("Database reset successfully!")
