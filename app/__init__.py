from os import environ
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
config_path = environ.get("CONFIG_PATH", "app.config.DevelopmentConfig")
app.config.from_object(config_path)

db = SQLAlchemy(app)
db.create_all()


from . import views
from . import login
