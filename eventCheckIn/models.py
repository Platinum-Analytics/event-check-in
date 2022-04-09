from .extensions import db


class Guest(db.Model):
    ticket_num = db.Column(db.VARCHAR(8), primary_key=True, nullable=False)
    first_name = db.Column(db.VARCHAR(255))
    last_name = db.Column(db.VARCHAR(255))
    is_cash = db.Column(db.BOOLEAN, nullable=False)
    check_num = db.Column(db.VARCHAR(4))


class Student(Guest):
    school_id = db.Column(db.VARCHAR(8), nullable=False)
    has_guest = db.Column(db.BOOLEAN, nullable=False)
    has_oblg = db.Column(db.BOOLEAN, nullable=False)


class Visitor(Guest):
    host_id = db.Column(db.VARCHAR(8), db.ForeignKey(Student.ticket_num))

