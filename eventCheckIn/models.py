from .extensions import db


# Abstract parent class
class Attendee(db.Model):
    __abstract__ = True

    _id = db.Column(db.INTEGER, primary_key=True)
    ticket_num = db.Column(db.VARCHAR(8), nullable=False)
    first_name = db.Column(db.VARCHAR(255))
    last_name = db.Column(db.VARCHAR(255))
    is_cash = db.Column(db.BOOLEAN, nullable=False)
    check_num = db.Column(db.VARCHAR(4))

    def __init__(self, ticket_num: int, first_name: str, last_name: str, is_cash: bool, check_num: int):
        self.ticket_num = ticket_num
        self.first_name = first_name
        self.last_name = last_name
        self.is_cash = is_cash
        self.check_num = check_num


class Student(Attendee):
    __tablename__ = "student"

    school_id = db.Column(db.VARCHAR(8), nullable=False)
    has_guest = db.Column(db.BOOLEAN, nullable=False)

    guests = db.relationship("Guest", backref="host")

    def __init__(self, ticket_num: int, school_id: int, first_name: str, last_name: str, is_cash: bool, check_num: int,
                 has_guest: bool):
        super().__init__(ticket_num, first_name, last_name, is_cash, check_num)
        self.school_id = school_id
        self.has_guest = has_guest


class Guest(Attendee):
    __tablename__ = "guest"

    host_id = db.Column(db.VARCHAR(8), db.ForeignKey("student.ticket_num"), nullable=False)

    def __init__(self, ticket_num: int, host_id: int, first_name: str, last_name: str, is_cash: bool,
                 check_num: int):
        super().__init__(ticket_num, first_name, last_name, is_cash, check_num)
        self.host_id = host_id
