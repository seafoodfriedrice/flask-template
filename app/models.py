from datetime import datetime
from flask.ext.login import UserMixin
from app import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(48), nullable=False)
    last_name = db.Column(db.String(48), nullable=False)
    age = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    hire_date = db.Column(db.Date, default=datetime(2000, 1, 1))
    is_veteran = db.Column(db.Boolean)
    notes = db.Column(db.Text)
    created_date = db.Column(db.DateTime, server_default=db.func.now())
    updated_date = db.Column(db.DateTime, server_default=db.func.now(),
                             onupdate=db.func.now())
    change_notes = db.relationship('ChangeNote', backref='employee')

    def as_dictionary(self):
        employee = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "department": self.department.department_name,
            "hire_date": self.hire_date,
            "is_veteran": self.is_veteran,
            "notes": self.notes
        }
        return employee

    def __repr__(self):
        return "<Employee {!r}>".format(" ".join([self.first_name,
                                                 self.last_name]))


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(32), nullable=False, unique=True)
    employees = db.relationship('Employee', backref='department')

    def as_dictionary(self):
        department = {
            "id": self.id,
            "department_name": self.department_name,
            "employees": self.employees
        }
        return department

    def __repr__(self):
        return "<Department {!r}>".format(self.department_name)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True)
    password = db.Column(db.String(64))

class ChangeNote(db.Model):
    __tablename__ = "change_notes"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, server_default=db.func.now())
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    text = db.Column(db.String(1024))
