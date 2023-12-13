from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_rds_database_uri'  # Replace with your RDS database URI
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    dob = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        dob = request.form['dob']

        new_user = User(username=username, dob=dob)
        db.session.add(new_user)
        db.session.commit()

        return f'Data saved for user: {username}, Date of Birth: {dob}'

if __name__ == '__main__':
    app.run(debug=True)
