from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Replace these values with your RDS credentials
db_config = {
    'host': 'dbinstance.cyf3uod2jso1.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'admin123',
    'database': 'mysql'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

def create_user_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            dob DATE NOT NULL
        )
    """)
    conn.commit()

create_user_table()

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

    insert_query = "INSERT INTO users (username, dob) VALUES (%s, %s)"
    cursor.execute(insert_query, (username, dob))
    conn.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
