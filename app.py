from crypt import methods
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def get_or_add_task():
    if request.method == 'POST':
        try:
            task_content = request.form['task']
            new_task = Todo(content=task_content)
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Issue Faced While Adding Task in Todo List"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete_task(id):
    try:
        task = Todo.query.get_or_404(id)

        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Issue Faced While Deleting Task from Todo List"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    print(task)
    if request.method == 'POST':
        try:
            task.content = request.form['update_task_data']
            db.session.commit()
            return redirect('/')
        except:
            return "Issue Faced While Updating Task in Todo List"
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
