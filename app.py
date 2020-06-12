from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


# First step - init
app = Flask(__name__)

# Database initialization
# in case you call it sqllite instead of sqlite you will have - https://github.com/miguelgrinberg/Flask-Migrate/issues/197
# If the program is changed the python shell has to be quite and reopened.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goda.db'
db = SQLAlchemy(app)


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Called whenever some data is inserted
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # pass
        task_content = request.form['name']
        new_insert = Friends(name=task_content)
        try:
            db.session.add(new_insert)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(str(e))
            return "There was a database issue and the data could not be inserted"
    if request.method == 'GET':
        # You can also do a query.get_or_404(<id>) and then use the id to do a db.session.delete(id) which I am not going to do now in the interest of time
        data = Friends.query.order_by(Friends.date).all()

        # You dont have to mention the templates folder here as the name is predefined name.
        return render_template('index.html', data=data)


@app.route('/friend/', methods=['GET'])
@app.route('/friend', methods=['GET'])
def friend():
    data = Friends.query.order_by(Friends.date).all()
    data_lst = []
    for item in data:
        data_lst.append(
            {
                'id': item.id,
                'name': item.name,
                'date': item.date.date()
            }
        )
    # It can be named anything not essentially response.
    response = jsonify(data_lst)
    response.status_code = 200
    return response


@app.route('/friend/<int:id>', methods=['GET'])
def friend_by_id(id):
    data_lst = []
    status = 200

    if(id is None):
        data_lst.append(
            {
                'msg': 'No data found with id ' + str(id)
            }
        )
        status = 404
    else:
        data = Friends.query.get(id)
        print(data)

        if(data is None):
            data_lst.append(
                {
                    'msg': 'No data found with id ' + str(id)
                }
            )
            status = 404
        else:
            data_lst.append(
                {
                    'id': data.id,
                    'name': data.name,
                    'date': data.date.date()
                }
            )

    # It can be named anything not essentially response.
    response = jsonify(data_lst)
    response.status_code = status
    return response


def toJSON(data):
    return json.dumps(data, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)


# Why this condition is written without directly calling app.run is something i am not sure.
if __name__ == "__main__":
    app.run(debug=True)
