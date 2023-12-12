from flask import Flask, render_template, request
import boto3
from datetime import datetime

app = Flask(__name__)

# Replace these with your AWS credentials and DynamoDB table name
AWS_ACCESS_KEY = 'AKIAWCVXQWV2MPRZ55GG'
AWS_SECRET_KEY = 'KCzHbWTZ2RHmlYTMUK5b6mMTPXPgTTfaAJwSyoTz'
AWS_REGION = 'ap-southeast-1'
DYNAMODB_TABLE_NAME = 'sarandb'

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

# Get reference to your DynamoDB table
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    dob_str = request.form['dob']

    # Convert dob_str to datetime
    dob = datetime.strptime(dob_str, '%Y-%m-%d')

    # Save data to DynamoDB
    response = table.put_item(
        Item={
            'Username': username,
            'DOB': dob.strftime('%Y-%m-%d')
        }
    )

    return "Data saved successfully"

@app.route('/view')
def view():
    # Retrieve data from DynamoDB
    response = table.scan()
    data = response.get('Items', [])

    return render_template('view.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
