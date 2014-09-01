import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'taskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
CSRF_ENABLED = True
SECRET_KEY = 'precious'

DATABASE_PATH = os.path.join(basedir,DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH