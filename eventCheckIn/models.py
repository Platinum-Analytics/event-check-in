from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, Integer, Boolean, Text

from .extensions import db, bc, serializer


# Attendee database models
class Attendee(db.Model):  # Abstract parent class
    __tablename__ = "attendee"
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)
    checked_in = Column(Boolean)

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
        self.checked_in = False


class Student(Attendee):  # PHS Student
    __tablename__ = "student"

    school_id = Column(Integer, nullable=False, unique=True)
    has_guest = Column(Boolean, nullable=False)

    guests = db.relationship("Guest", backref="host")
    timeEntries = db.relationship("TimeEntryStudent", backref="student", order_by="TimeEntryStudent.time")

    def __init__(self, school_id: int, first_name: str, last_name: str, has_guest: bool):
        super().__init__(first_name, last_name)
        self.school_id = school_id
        self.has_guest = has_guest


class Guest(Attendee):  # Non-PHS Student
    __tablename__ = "guest"

    host_id = Column(Integer, db.ForeignKey("student.school_id"), nullable=False)

    timeEntries = db.relationship("TimeEntryGuest", backref="guest", order_by="TimeEntryGuest.time")

    def __init__(self, host_id: int, first_name: str, last_name: str):
        super().__init__(first_name, last_name)
        self.host_id = host_id


# Time entry database models
class TimeEntryStudent(db.Model):
    id = Column(Integer, primary_key=True)
    time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    is_check_in = Column(Boolean, nullable=False)
    student_id = Column(Integer, db.ForeignKey("student.id"), nullable=False)
    staff = Column(Text, nullable=False)

    def __init__(self, check_in: bool, student_id: int, staff: str, time=func.now()):
        self.time = time
        self.is_check_in = check_in
        self.student_id = student_id
        self.staff = staff


class TimeEntryGuest(db.Model):
    id = Column(Integer, primary_key=True)
    time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    is_check_in = Column(Boolean, nullable=False)
    guest_id = Column(Integer, db.ForeignKey("guest.id"), nullable=False)
    staff = Column(Text, nullable=False)

    def __init__(self, check_in: bool, guest_id: int, staff: str, time=func.now()):
        self.time = time
        self.is_check_in = check_in
        self.guest_id = guest_id
        self.staff = staff


# Logins database model
class User_(UserMixin, db.Model):  # NOT User due to Postgresql constraints
    id = Column(Integer, primary_key=True)
    session_token = Column(Text, nullable=False, unique=True)
    email = Column(Text, unique=True)
    password = Column(Text)
    verified = Column(Boolean, nullable=False)

    def __init__(self, email: str, password: str, verified: bool):
        self.email = email
        self.password = bc.generate_password_hash(password).decode("utf8")
        self.session_token = serializer.dumps([self.email, self.password])
        self.verified = verified

    def changePassword(self, password):
        self.password = bc.generate_password_hash(password).decode("utf8")

    def get_id(self):
        return str(self.session_token)
