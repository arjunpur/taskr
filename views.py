from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Tasks



def login_required(test):
	@wraps(test)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return test(*args,**kwargs)
		else:
			flash('You need to login')
			return redirect(url_for('login'))
	return wrap
 
@app.route('/logout/')
def logout():
	session.pop('logged_in')
	flash('You were logged out')
	return redirect(url_for('login'))


@app.route('/',methods = ['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if (request.form['username'] != app.config['USERNAME']) or (request.form['password'] != 
		app.config['PASSWORD']):
			error = 'Invalid Credentials'
		else:
			session['logged_in'] = True
			return redirect(url_for('tasks'))
	return render_template('login.html',error = error)

@app.route('/tasks/')
@login_required
def tasks():
	open_tasks = db.session.query(Tasks).filter_by(status = '1').order_by(Tasks.due_date.asc())
	closed_tasks = db.session.query(Tasks).filter_by(status = "0").order_by(Tasks.due_date.asc())
	return render_template('tasks.html',form = AddTask(request.form),open_tasks = open_tasks, closed_tasks = closed_tasks)

@app.route('/add/',methods= ['POST'])
@login_required
def new_task():
	form = AddTask(request.form, csrf_enabled = False)
	if form.validate_on_submit():
		task = Tasks(form.name.data,form.due_date.data,form.priority.data,'1')
		db.session.add(task)
		db.session.commit()
		flash('Entry was successful')
	return redirect_url(url_for('tasks'))

@app.route('/complete/<int:task_id>/')
@login_required
def complete_task(task_id):
	temp = task_id
	db.session.query(Tasks).filter_by(task_id = temp).update({"status":"0"})
	db.session.commit()
	flash('Task has been changed to Complete')
	return redirect_url(url_for('tasks'))

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
	temp = task_id
	db.session.query(Tasks).filter_by(task_id = temp).delete()
	db.session.commit()
	flash('Task has been deleted')
	return redirect_url(url_for('tasks'))






