from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'instance', 'test.db')

db = SQLAlchemy(app)


class ToDo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):         #repr method is used to define how to represent the object when it is printed
        return '<Task %r>' % self.id
@app.route('/',methods=['POST','GET'])  #route for home page
def index():
    if request.method =='POST':
        task_content=request.form['content']    #this creates a new task by taking the inputs and commits it to the database
        new_task=ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding ur task'
    else:
        tasks= ToDo.query.order_by(ToDo.date_created).all()   # this creates the queries of the database in the order they have been created
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=ToDo.query.get_or_404(id)  #queries to get the task and if not found returns 404 error

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem deleting it'
    
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task=ToDo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']    #task.content is used  to get the content from the database and update it with the new content from the form

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue while updating'
    else:
         return render_template('update.html',task=task)
if __name__ == "__main__":
    # Create database tables before starting the dev server (safe for local/dev use)
    with app.app_context():
        db.create_all()

    app.run(debug=True)