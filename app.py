from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# First step - init
app = Flask(__name__)

# Database initialization
# in case you call it sqllite instead of sqlite you will have - https://github.com/miguelgrinberg/Flask-Migrate/issues/197
# If the program is changed the python shell has to be quite and reopened.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goda.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name = db.Column(db.DateTime, default=datetime.utcnow)

    # Called whenever some data is inserted
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/')
def index():
    # You dont have to mention the templates folder here as the name is predefined name.
    return render_template('index.html')


# Why this condition is written without directly calling app.run is something i am not sure.
if __name__ == "__main__":
    app.run(debug=True)
