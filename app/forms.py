from datetime import datetime
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import DateTimeField
from wtforms import TextAreaField
from wtforms.validators import Required
from wtforms.validators import Length
from wtforms.validators import Optional
from app import db
from app.models import Department

def department_names():
    return Department.query.order_by(Department.department_name)

class EmployeeForm(Form):
    first_name = StringField(u'First Name', validators=[Required(),
                                                        Length(max=48)])
    last_name = StringField(u'Last Name', validators=[Required(),
                                                      Length(max=48)])
    age = IntegerField(u'Age', validators=[Optional()])
    department = QuerySelectField(get_label='department_name',
                                  query_factory=department_names,
                                  validators=[Optional()])
    hire_date = DateTimeField(u'Hire Date', default=datetime(2000, 1, 1),
                              validators=[Optional()])
    is_veteran = BooleanField(u'Veteran', default=False,
                              validators=[Optional()])
    notes = TextAreaField(u'Notes', validators=[Optional()])
