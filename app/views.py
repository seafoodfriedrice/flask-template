import json

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import (login_required, login_user, logout_user,
                             current_user)
from werkzeug.security import check_password_hash

from app import app, db
from app.models import Employee, Department, User, ChangeNote
from app.forms import EmployeeForm, ChangeForm


@app.route("/")
def index():
    employees = Employee.query.all()
    departments = Department.query.all()
    return render_template("index.html", employees=employees,
                           departments=departments)

def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error), "danger")

@app.route("/employee/add", methods=["GET", "POST"])
def employee_add():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee()
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.age = form.age.data
        db.session.add(employee)
        db.session.commit()
        flash("Added {}".format(employee.first_name), "success")
        return render_template("index.html")
    else:
        flash_form_errors(form)
    return render_template("employee.html", form=form, action="add")


@app.route("/employee/<int:id>", methods=["GET", "POST"])
def employee_edit(id):
    employee = Employee.query.get(id)
    form = EmployeeForm(obj=employee)
    change_form = ChangeForm()
    if (form.validate_on_submit() and request.form["submit"] == "Save" and
            request.method == "POST"):
        old_value = {}
        new_value = {}
        changes = False
        for attr in ['first_name', 'last_name', 'age']:
            employee_attr = getattr(employee, attr)
            form_attr = getattr(form, attr).data
            if employee_attr != form_attr:
                # Set new value from form on Employee attribute
                setattr(employee, attr, getattr(form,attr).data)

                label = getattr(form, attr).label.text
                old_value[label] = employee_attr
                new_value[label] = form_attr
                changes = True

        if changes:
            flash("{} to {}".format(old_value, new_value), "success")
            flash("Edited {}".format(employee.first_name), "success")
            change_note = ChangeNote(
                old_value=json.dumps(old_value),
                new_value=json.dumps(new_value),
                description=change_form.description.data
            )
            employee.change_notes.append(change_note)
            db.session.add(employee)
            db.session.commit()
        else:
            flash("No changes were made", "info")
        return redirect(url_for("employee_edit", id=employee.id))
    else:
        flash_form_errors(form)
    return render_template("employee.html", form=form, change_form=change_form,
                           employee=employee, action="edit")


'''
@app.route("/<department_name>")
def department_name(department_name):
    pass


@app.route("/portal")
@login_required
def portal():
    pass


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        user = User.query.filter_by(username == username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Incorrect username or password", "danger")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(request.args.get("next") or url_for("index"))
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    if current_user.is_authenticated():
        logout_user()
        return render_template("logout.html")
    else:
        return render_template("login.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
'''
