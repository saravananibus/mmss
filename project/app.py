from flask import Flask, render_template, request
import boto3
from sqlalchemy import create_engine

app = Flask(__name__)

# Replace the following placeholders with your RDS details
RDS_HOST = 'your-rds-host'
RDS_PORT = 'your-rds-port'
RDS_DB_NAME = 'your-db-name'
RDS_USERNAME = 'your-db-username'
RDS_PASSWORD = 'your-db-password'

# Create an SQL Alchemy engine for database connection
db_url = f'mysql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DB_NAME}'
engine = create_engine(db_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_data():
    username = request.form['username']
    dob = request.form['dob']

    try:
        # Use the SQL Alchemy engine to execute an INSERT query
        with engine.connect() as connection:
            connection.execute("INSERT INTO your_table (username, dob) VALUES (%s, %s)", (username, dob))
        
        return f'Data saved for {username} with DOB {dob}'
    except Exception as e:
        return f'Error saving data: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
