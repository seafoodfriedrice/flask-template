class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/flask-template"
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "hunter2"
