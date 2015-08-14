from os import environ
from datetime import datetime
from getpass import getpass
from werkzeug.security import generate_password_hash
from werkzeug.serving import run_simple
from flask.ext.script import Manager
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand
from app import app
from app import db
from app.models import Employee
from app.models import Department


manager = Manager(app)

@manager.command
def run():
    port = int(environ.get('PORT', 8080))
    # Normal method to run application without SSL
    #app.run(host='0.0.0.0', port=port)

    '''
        Run application with SSL context, see more information at
        http://werkzeug.pocoo.org/docs/0.10/serving/#quickstart
    '''
    run_simple('localhost', port, app, ssl_context=('app.crt', 'app.key'))


@manager.command
def add_user():
    username = raw_input("Username: ")
    if User.query.filter_by(username=username).first():
        print "Username already exists."
        return
    password = ""
    password2 = ""
    while not (password and password2 or get_pass != password2):
        password = getpass("Password: ")
        password2 = getpass("Re-enter password: ")
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()


@manager.command
def seed():
    alice = Employee(first_name="Alice", last_name="Wonderland",
                     hire_date=datetime.now(), is_veteran=False,
                     notes="We're not in Kansas anymore.")
    bob = Employee(first_name="Bob", last_name="Builder",
                   hire_date=datetime.now(), is_veteran=True,
                   notes="Yes we can!")
    hr = Department(department_name="Information Technology")
    hr.employees.append(alice)
    hr.employees.append(bob)
    db.session.add_all([alice, bob, hr])
    db.session.commit()

    # Create login accounts
    alice_password = "garland"
    alice_user = User(username="alicew", password=alice_password)
    bob_password = "robert"
    bob_user = User(username="bobb", password=bob_password)
    db.session.add_all([alice_user, bob_user])
    db_session.commit()


# For database migrations
class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(db.metadata))
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
