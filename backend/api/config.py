import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",  # ✅ Default MySQL username
    password="",  # ✅ If no password, leave it empty
    database="techfix"
)

cursor = db.cursor()

