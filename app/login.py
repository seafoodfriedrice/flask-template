from flask.ext.login import LoginManager
from app import app
from app import db
from app.models import User


login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
