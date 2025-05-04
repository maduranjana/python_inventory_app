from flask import Blueprint, request, jsonify
import bcrypt
from db_config import connect_db  # ✅ Import database connection

bp = Blueprint('login', __name__)  # ✅ Create Blueprint for Login

@bp.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        print("Login Request Data:", data)  # ✅ Debugging

        username = data.get("username")
        password = data.get("password")
        user_type = data.get("userType")

        if not all([username, password, user_type]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        db = connect_db()
        cursor = db.cursor(dictionary=True)

        # ✅ Query user from database
        query = "SELECT * FROM users WHERE username = %s AND user_type = %s"
        cursor.execute(query, (username, user_type))
        user = cursor.fetchone()

        db.close()

        if user:
            stored_password = user["password"]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):  # ✅ Check hashed password
                # ✅ Redirect user to correct dashboard
                redirect_url = "admindashboard.html" if user_type == "Admin" else "supplierdashboard.html"
                return jsonify({"status": "success", "message": "Login successful!", "redirect": redirect_url})
            else:
                return jsonify({"status": "error", "message": "Invalid password!"})
        else:
            return jsonify({"status": "error", "message": "User not found or incorrect user type!"})

    except Exception as e:
        print("Login Error:", str(e))  # ✅ Debugging
        return jsonify({"status": "error", "message": str(e)})
