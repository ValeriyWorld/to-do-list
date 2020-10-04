import os

from flask import Flask, render_template, request
from flask_script import Manager, Shell
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand


def make_shell_context():
    return dict(app = app, db = db, Task = Task)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                        'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '< Content: {}>'.format(self.content)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_task = request.form.get('add_task')

        if new_task:
            new_task_obj = Task(content=new_task)
            db.session.add(new_task_obj)
            db.session.commit()

    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


if __name__ == '__main__':
    manager.run()
