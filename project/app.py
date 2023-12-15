from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Replace 'your_rds_connection_string' with your actual RDS connection string
# Format: 'mysql://username:password@hostname:port/database'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin123@dbinstance.cyf3uod2jso1.ap-south-1.rds.amazonaws.com:3306/mysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Use 'mysqlclient' instead of 'MySQLdb'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'charset': 'utf8mb4'},
    'client_flag': 3306,
}

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    dob_str = request.form['dob']

    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."

    user = User(username=username, dob=dob)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
