from flask_login import UserMixin
from datetime import time

from .extensions import db, bc, serializer


# Attendee database models
class Attendee(db.Model):  # Abstract parent class
    __tablename__ = "attendee"
    __abstract__ = True

    id = db.Column(db.INTEGER, primary_key=True)
    ticket_num = db.Column(db.INTEGER, nullable=False)
    first_name = db.Column(db.VARCHAR(255))
    last_name = db.Column(db.VARCHAR(255))
    is_cash = db.Column(db.BOOLEAN, nullable=False)
    check_num = db.Column(db.INTEGER)

    def __init__(self, ticket_num: int, first_name: str, last_name: str, is_cash: bool, check_num: int):
        self.ticket_num = ticket_num
        self.first_name = first_name
        self.last_name = last_name
        self.is_cash = is_cash
        self.check_num = check_num


class Student(Attendee):  # PHS Student
    __tablename__ = "student"

    school_id = db.Column(db.INTEGER, nullable=False, unique=True)
    has_guest = db.Column(db.BOOLEAN, nullable=False)

    guests = db.relationship("Guest", backref="host")
    timeEntries = db.relationship("TimeEntryStudent", backref="student")

    def __init__(self, ticket_num: int, school_id: int, first_name: str, last_name: str, is_cash: bool, check_num: int,
                 has_guest: bool):
        super().__init__(ticket_num, first_name, last_name, is_cash, check_num)
        self.school_id = school_id
        self.has_guest = has_guest


class Guest(Attendee):  # Non-PHS Student
    __tablename__ = "guest"

    host_id = db.Column(db.INTEGER, db.ForeignKey("student.school_id"), nullable=False)

    timeEntries = db.relationship("TimeEntryGuest", backref="guest")

    def __init__(self, ticket_num: int, host_id: int, first_name: str, last_name: str, is_cash: bool,
                 check_num: int):
        super().__init__(ticket_num, first_name, last_name, is_cash, check_num)
        self.host_id = host_id


# Time entry database models
class TimeEntryStudent(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    time = db.Column(db.TIME, nullable=False)
    check_in = db.Column(db.BOOLEAN, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)

    def __init__(self, check_in: bool, attendee_id: int):
        self.time = time()
        self.check_in = check_in
        self.attendee_id = attendee_id


class TimeEntryGuest(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    time = db.Column(db.TIME, nullable=False)
    check_in = db.Column(db.BOOLEAN, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guest.id"), nullable=False)

    def __init__(self, check_in: bool, attendee_id: int):
        self.time = time()
        self.check_in = check_in
        self.attendee_id = attendee_id


# Logins database model
class User_(UserMixin, db.Model):  # NOT User due to Postgresql constraints
    id = db.Column(db.INTEGER, primary_key=True)
    session_token = db.Column(db.VARCHAR, nullable=False, unique=True)
    email = db.Column(db.VARCHAR(255), unique=True)
    password = db.Column(db.VARCHAR(255))
    verified = db.Column(db.Boolean, nullable=False)

    def __init__(self, email: str, password: str, verified: bool):
        self.email = email
        self.password = bc.generate_password_hash(password).decode("utf8")
        self.session_token = serializer.dumps([self.email, self.password])
        self.verified = verified

    def changePassword(self, password):
        self.password = bc.generate_password_hash(password).decode("utf8")

    def get_id(self):
        return str(self.session_token)
