from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask.ext.login import current_user
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from werkzeug.security import check_password_hash
from app import app
from app import db
from app.models import Employee
from app.models import Department
from app.models import User
from app.models import ChangeNote
from app.forms import EmployeeForm
from app.forms import ChangeForm


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
        messages = []
        for attr in ['first_name', 'last_name', 'age']:
            employee_attr = getattr(employee, attr)
            form_attr = getattr(form, attr).data
            if employee_attr != form_attr:
                setattr(employee, attr, getattr(form,attr).data)
                m = "{}: '{}' -> '{}'".format(getattr(form, attr).label.text,
                    employee_attr, form_attr)
                messages.append(m)
        if messages:
            flash(", ".join(messages), "success")
            flash("Edited {}".format(employee.first_name), "success")
            text = "{} {}".format(", ".join(messages),change_form.text.data)
            change_note = ChangeNote(text=text)
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
