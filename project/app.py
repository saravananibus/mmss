from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Replace these values with your RDS credentials
db_config = {
    'host': 'myrdsinstance.cyf3uod2jso1.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'admin123',
}

# Connect to MySQL server (not to a specific database)
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

def create_database():
    cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
    conn.commit()

def create_user_table():
    create_database()  # Call the create_database function before creating the table
    cursor.execute("""
        USE mydatabase;
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
    # Fetch existing users from the database
    select_query = "SELECT username, dob FROM users"
    cursor.execute(select_query)
    users = [{'username': username, 'dob': dob.strftime('%Y-%m-%d')} for username, dob in cursor.fetchall()]

    return render_template('index.html', users=users)

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

    # Redirect to the 'show_data' route
    return redirect(url_for('show_data'))

@app.route('/show_data')
def show_data():
    # Fetch all users from the database
    select_query = "SELECT username, dob FROM users"
    cursor.execute(select_query)
    users = [{'username': username, 'dob': dob.strftime('%Y-%m-%d')} for username, dob in cursor.fetchall()]

    return render_template('show_data.html', users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
