from flask import redirect, url_for, session, flash, request, Response, stream_with_context
from flask_login import logout_user, login_required, current_user

from .extensions import db
from .models import Student, Guest, TimeEntryStudent, TimeEntryGuest


@login_required
def resetDB():
    db.session.execute(TimeEntryStudent.__table__.delete())
    db.session.execute(TimeEntryGuest.__table__.delete())
    db.session.execute(Guest.__table__.delete())
    db.session.execute(Student.__table__.delete())

    db.session.commit()

    flash("Database reset", "success")
    return redirect(url_for("main.settings"))


@login_required
def logout():
    logout_user()
    flash("Successfully logged out!", "success")
    return redirect(url_for("main.login"))


@login_required
def log(id_):
    group = request.args.get("group")

    if group == "student":
        student = db.session.get(Student, id_)
        student.checked_in = not student.checked_in
        db.session.add(TimeEntryStudent(student.checked_in, id_, current_user.email))
    elif group == "guest":
        guest = db.session.get(Guest, id_)
        guest.checked_in = not guest.checked_in
        db.session.add(TimeEntryGuest(guest.checked_in, id_, current_user.email))
    else:
        return redirect(url_for("main.home"))

    db.session.commit()
    session["returnLog"] = True
    return redirect(url_for("main.search"))


@login_required
def removeLog(entry_id):
    group = request.args.get("group")

    if group == "student":
        entry = db.session.get(TimeEntryStudent, entry_id)
        db.session.delete(entry)
        db.session.commit()

        student = db.session.get(Student, entry.student_id)

        flag = True
        for i in student.timeEntries:
            if i.is_check_in != flag:
                i.is_check_in = flag
            flag = not flag

        student.checked_in = not flag
    elif group == "guest":
        entry = db.session.get(TimeEntryGuest, entry_id)
        db.session.delete(entry)
        db.session.commit()

        guest = db.session.get(Guest, entry.guest_id)

        flag = True
        for i in guest.timeEntries:
            if i.is_check_in != flag:
                i.is_check_in = flag
            flag = not flag

        guest.checked_in = not flag

    db.session.commit()
    session["returnLog"] = True
    return redirect(url_for("main.search"))


# noinspection PyCallingNonCallable
@login_required
def download(group):
    def parse_times(entry_list):
        str_list = ""
        for j in entry_list:
            str_list += j.time.strftime("%b-%d-%Y %I:%M:%S %p") + f"|{j.staff.split('@')[0]};"
        str_list = str_list.strip(";")

        return str_list

    @stream_with_context
    def generate(studentList, guestList):
        yield "Ticket,ID,LAST,MI,FIRST,GR,Payment Method,Guest YN,Guest Ticket Number,Check In,Check Out\n"

        if studentList:
            students = db.session.query(Student).all()
            for i in students:
                g_ids = ""
                for j in i.guests:
                    g_ids += str(j.ticket_num) + ";"
                g_ids = g_ids.strip(";")

                check_in = parse_times(
                    db.session.query(TimeEntryStudent).filter_by(student_id=i.id).filter_by(is_check_in=True).all())

                check_out = parse_times(
                    db.session.query(TimeEntryStudent).filter_by(student_id=i.id).filter_by(is_check_in=False).all())

                yield f"{i.ticket_num},{i.school_id},{i.last_name},,{i.first_name},,{'cash' if i.is_cash else i.check_num},{'Y' if i.guests else 'N'},{g_ids},{check_in},{check_out}\n"
        if guestList:
            guests = db.session.query(Guest).all()
            for i in guests:
                check_in = parse_times(
                    db.session.query(TimeEntryGuest).filter_by(guest_id=i.id).filter_by(is_check_in=True).all())

                check_out = parse_times(
                    db.session.query(TimeEntryGuest).filter_by(guest_id=i.id).filter_by(is_check_in=False).all())

                yield f"{i.ticket_num},,{i.last_name},,{i.first_name},,{'cash' if i.is_cash else i.check_num},N,,{check_in},{check_out}\n"

    if group == "students":
        content = generate(True, False)
        filename = "students"
    elif group == "guests":
        content = generate(False, True)
        filename = "guests"
    else:
        content = generate(True, True)
        filename = "attendees"

    response = Response(content, mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename=f"{filename}.csv")
    return response


@login_required
def downloadLog():
    @stream_with_context
    def generate():
        student_log = db.session.query(TimeEntryStudent).all()
        guest_log = db.session.query(TimeEntryGuest).all()

        data = [
            [i.student.ticket_num, i.student.school_id, i.student.last_name, i.student.first_name,
             "Check In" if i.is_check_in else "Check Out",
             i.time.strftime("%r"), i.staff.split("@")[0]] for i in student_log]
        temp_data = [
            [i.guest.ticket_num, "", i.guest.last_name, i.guest.first_name,
             "Check In" if i.is_check_in else "Check Out",
             i.time.strftime("%r"), i.staff.split("@")[0]] for i in guest_log]

        data.extend(temp_data)
        data.sort(key=lambda e: e[5], reverse=True)

        yield "Ticket,ID,Last,First,Action,Time,Logged By\n"
        for j in data:
            row = ""
            for k in j:
                row += str(k) + ","
            row = row.strip(",")
            row += "\n"
            yield row

    response = Response(generate(), mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response.headers.set("Content-Disposition", "attachment", filename=f"activity_log.xlsx")
    return response


@login_required
def deleteUser():
    db.session.delete(current_user)
    db.session.commit()

    flash("Account Deleted", "success")
    return redirect(url_for("main.login"))
