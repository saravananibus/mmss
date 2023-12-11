import mysql.connector

def connect_to_rds():
    # Replace these values with your RDS details
    db_config = {
        'host':'mydbinstance.ciklgdejnsgr.ap-southeast-1.rds.amazonaws.com',
        'user':'admin',
        'password':'admin123',
        'database':'mydbinstance',
    }

    try:
        connection = mysql.connector.connect(**db_config)
        print("Connected to RDS")
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

def insert_mmss(connection, username, dob):
    cursor = connection.cursor()
    insert_query = "INSERT INTO user_data (username, dob) VALUES (%s, %s)"
    data = (username, dob)

    try:
        cursor.execute(insert_query, data)
        connection.commit()
        print("User data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

def retrieve_mmss(connection):
    cursor = connection.cursor()
    select_query = "SELECT * FROM user_data"

    try:
        cursor.execute(select_query)
        result = cursor.fetchall()
        for row in result:
            print(f"Username: {row[0]}, Date of Birth: {row[1]}")
    except Exception as e:
        print(f"Error retrieving data: {e}")
    finally:
        cursor.close()

def main():
    connection = connect_to_rds()
    if connection:
        # Sample data
        username = "JohnDoe"
        dob = "1990-01-01"

        # Insert user data
        insert_mmss(connection, username, dob)

        # Retrieve and print user data
        retrieve_mmss(connection)

        # Close the connection
        connection.close()

if __name__ == "__main__":
    main()
