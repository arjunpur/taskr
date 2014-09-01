# db_create.py
from views import db
from models import Tasks
from datetime import date

db.create_all()

db.session.add(Tasks("Finish Tutorial", date(2014,3,13),10,1))
db.session.add(Tasks("Finish Pizza", date(2014,3,13),10,1))

db.session.commit()