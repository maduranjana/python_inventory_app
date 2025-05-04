from flask import Blueprint, request, jsonify
import bcrypt
from db_config import connect_db  # ✅ Import database connection

bp = Blueprint('register', __name__)  # ✅ Create Blueprint for Registration

@bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        print("Received Data from Frontend:", data)  # ✅ Debugging: Print received data in terminal

        full_name = data.get("full_name")
        email = data.get("email")
        username = data.get("username")
        phone = data.get("phone")
        location = data.get("location")
        password = data.get("password")
        user_type = data.get("user_type")

        if not all([full_name, email, username, phone, location, password, user_type]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        # Hash password securely
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # ✅ Fixed Password Hashing

        db = connect_db()
        cursor = db.cursor()

        # SQL query to insert user, with current timestamp for 'joined_date' handled by MySQL
        query = """INSERT INTO users (full_name, email, username, phone, location, password, user_type) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (full_name, email, username, phone, location, hashed_password, user_type)

        cursor.execute(query, values)
        db.commit()

        print("User successfully inserted into database!")  # ✅ Debugging
        return jsonify({"status": "success", "message": "User registered successfully!"})

    except Exception as e:
        print("Database Error:", str(e))  # ✅ Debugging: Print error in terminal
        return jsonify({"status": "error", "message": str(e)})

    finally:
        if db.is_connected():
            db.close()  # Ensure the DB connection is always closed
