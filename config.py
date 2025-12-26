import os

SQLALCHEMY_DATABASE_URI = os.environ.get("postgresql://postgres:user%40123@localhost:5432/student_ms_db")
SQLALCHEMY_TRACK_MODIFICATION = False
SECRET_KEY = os.environ.get("SECRET_KEY", "student@123")