from flask import Flask, render_template, request
import boto3
from sqlalchemy import create_engine

app = Flask(__name__)

# Replace the following placeholders with your RDS details
RDS_HOST = 'myrdsinstance.cyf3uod2jso1.ap-south-1.rds.amazonaws.com'
RDS_PORT = '3306'
RDS_DB_NAME = 'MyRDSInstance'
RDS_USERNAME = 'admin'
RDS_PASSWORD = 'admin123'

# Create an SQL Alchemy engine for database connection
db_url = f'mysql://admin:admin123@myrdsinstance.cyf3uod2jso1.ap-south-1.rds.amazonaws.com:3306/MyRDSInstance'
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
