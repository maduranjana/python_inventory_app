import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Change this to your MySQL username 
            password="1234",  # Change this to your MySQL password
            database="techfix_db"  # Change this to your database name
        )
        print("Database connected successfully!")  # ✅ Debugging
        return connection
    except mysql.connector.Error as err:
        print("Database Connection Error:", err)
        return None  # ✅ Return None if connection fails
