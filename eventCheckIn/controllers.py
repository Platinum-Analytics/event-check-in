from flask import render_template, redirect, url_for

from .extensions import db
from .forms import CSVUpload
from .models import Student, Guest
from .scripts import checkString, checkInt, checkBool, checkCash


def index():
    return redirect(url_for("main.login"))


def login():
    return "<h1>My Login Page</h1>"


def upload():
    form = CSVUpload()
    if not form.validate_on_submit():
        return render_template("upload.html", form=form, success=False)

    # Read and parse CSV Data
    rawData = form.csvData.data.read().decode().split('\n')

    parsedData = [i.strip('\r').split(',') for i in rawData]
    del parsedData[0]

    # Clear the database
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

    # Store Students and Guests in database
    guest_ids = {}
    guests = []
    for user in parsedData:
        if user[7] == "Y":
            guest_ids[user[8]] = user[1]  # [guest_id : host_school_id]

    for user in parsedData:
        user_id = user[0]
        if user_id in guest_ids.keys():
            guests.append([user, guest_ids[user_id]])
        else:
            is_cash, check_num = checkCash(user[6])

            student = Student(checkInt(user[0]), checkInt(user[1]), checkString(user[4]), checkString(user[2]), is_cash,
                              check_num, checkBool(user[7]))

            db.session.add(student)

    for user, host_school_id in guests:
        is_cash, check_num = checkCash(user[6])
        guest = Guest(checkInt(user[0]), host_school_id, checkString(user[4]), checkString(user[2]), is_cash, check_num)

        db.session.add(guest)

    db.session.commit()
    return render_template("upload.html", success=True)
