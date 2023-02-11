# pip install psycopg2-binary
# pip install sqlalchemy
# pip install flask
# pip install Flask-SQLalchemy
# pushed to git
from flask import Flask,render_template,request,flash,url_for,redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost:5432/projectnou'
app.config['SECRET_KEY']='secret'

db=SQLAlchemy(app)

class Project(db.Model):
    __tablename__='projects'
    project_id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(length=50))

    task=db.relationship("Task",cascade="all,delete-orphan")

class Task(db.Model):
    __tablename__='tasks'
    task_id=db.Column(db.Integer,primary_key=True)
    project_id=db.Column(db.Integer,db.ForeignKey('projects.project_id'))
    description=db.Column(db.String(length=200))

    project=db.relationship("Project",backref='project')

@app.route("/")
def show_projects():
    return render_template("index.html",projects=Project.query.all())

@app.route("/project/<project_id>")
def show_tasks(project_id):
    return render_template("project-tasks.html",
    project=Project.query.filter_by(project_id=project_id).first(),
    tasks=Task.query.filter_by(project_id=project_id).all())

@app.route("/add/project",methods=['POST'])
def add_project():
    #Add Project
    if not request.form['project-title']:
        flash("Enter a title for the new project","red")
    else:
        pp=Project(title=request.form['project-title'])
        db.session.add(pp)
        db.session.commit()
        flash("Project added succesufully","green")
    #
    return redirect(url_for('show_projects'))

@app.route("/add/task/<project_id>",methods=['POST'])
def add_task(project_id):
    #ADd task
    if not request.form['task-description']:
        flash("Enter a description for new task","red")
    else:
        tt=Task(description=request.form['task-description'],project_id=project_id)
        db.session.add(tt)
        db.session.commit()
        flash("Task added succesufully","green")
    return redirect(url_for('show_tasks',project_id=project_id))

#delete func.

@app.route("/delete/task/<task_id>",methods=['POST'])
def delete_task(task_id):
    pending_delete=Task.query.filter_by(task_id=task_id).first()
    original_project=pending_delete.project.project_id
    db.session.delete(pending_delete)
    db.session.commit()
    return redirect(url_for('show_tasks',project_id=original_project))

@app.route("/delete/project/<project_id>",methods=['POST'])
def delete_project(project_id):
    pd=Project.query.filter_by(project_id=project_id).first()
    #op=pd.project.project_id
    db.session.delete(pd)
    db.session.commit()
    return redirect(url_for('show_projects'))

app.run(debug=True,host="127.0.0.1",port=3000)