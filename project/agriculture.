from flask import Flask, render_template, request
from termcolor import colored
import pymysql

app = Flask(__name__)

# Replace these with your database credentials
DB_HOST = 'myrdsinstance.cyf3uod2jso1.ap-south-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'admin123'
DB_NAME = 'mmss_mmss2'

def create_database_and_table():
    # Connect to MySQL server
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)

    try:
        with connection.cursor() as cursor:
            # Create the database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            cursor.execute(f"USE {DB_NAME}")

            # Create the user_data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    dob DATE NOT NULL
                )
            """)
        connection.commit()
        print("Database and table created successfully")
    except pymysql.err.OperationalError as e:
        print(f"Error: {e}")
    finally:
        connection.close()

# Create database and table before running the app
create_database_and_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['user_name']
    dob = request.form['date_of_birth']

    # Connect to the database
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)

    try:
        with connection.cursor() as cursor:
            # Insert data into the database
            sql = "INSERT INTO user_data (username, dob) VALUES (%s, %s)"
            cursor.execute(sql, (username, dob))
        connection.commit()
        success_message = "."
        return render_template('message.html', message=success_message)
    except Exception as e:
         error_message = "\033[1;31mError: {}\033[0m".format(str(e))
         centered_error_message = center_message(error_message)
         print(centered_error_message)
    
    finally:
        connection.close()

@app.route('/view')
def view():
    # Connect to the database
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)

    try:
        with connection.cursor() as cursor:
            # Retrieve data from the database
             sql = "SELECT * FROM user_data"
             cursor.execute(sql)
             result = cursor.fetchall()
        return render_template('view.html', data=result)
    except Exception as e:
        return str(e)
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
