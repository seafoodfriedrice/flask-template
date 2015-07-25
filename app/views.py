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
from app.models import Employee
from app.models import Department
from app.models import User


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<employee>")
def employee():
    pass


@app.route("/<department_name>")
def department_name():
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
