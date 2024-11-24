from flask import Flask
from flask import render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# initialize app
app = Flask(__name__)

# initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    completed = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello_world')
def hello_world():
    return render_template('hello_world.html')

@app.route('/todo', methods=['POST', 'GET'])
def todo():
    if (request.method == 'POST'):
        # return 'POST'
        # update data to database
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('todo.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete (id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')
    except:
        return 'There was a problem deleting that task'
    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit (id):
    task = Todo.query.get_or_404(id)

    if (request.method == 'POST'):
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue editing your task'
    else:
        return render_template('edit.html', task=task)
    
@app.route('/complete/<int:id>', methods=['GET', 'POST'])
def complete (id):
    task = Todo.query.get_or_404(id)
    task.completed = 1
    try:
        db.session.commit()
        return redirect('/todo')
    except:
        return 'There was a problem completing that task'

if __name__ == '__main__':
    app.run(debug=True)