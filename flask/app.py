from flask
import pymysql

app = Flask(__name__)

# Replace these with your database credentials
DB_HOST = 'mydbinstance.ciklgdejnsgr.ap-southeast-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'admin123'
DB_NAME = "mydbinstance"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    dob = request.form['dob']

    # Connect to the database
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)

    try:
        with connection.cursor() as cursor:
            # Insert data into the database
            sql = "INSERT INTO user_data (username, dob) VALUES (%s, %s)"
            cursor.execute(sql, (username, dob))
        connection.commit()
        return "Data saved successfully"
    except Exception as e:
        return str(e)
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
    app.run(host='0.0.0.0', port=80, debug=True)
