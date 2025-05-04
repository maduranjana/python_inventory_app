from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from config import db, cursor

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/register', methods=['POST'])  # Only accepts POST requests
def register():
    try:
        data = request.json  # Ensure frontend sends JSON data
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if not name or not email or not password or not role:
            return jsonify({"error": "All fields are required!"}), 400

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"error": "Email already registered!"}), 409

        # Hash password for security
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert user into database
        cursor.execute(
            "INSERT INTO users (name, email, role, password_hash) VALUES (%s, %s, %s, %s)",
            (name, email, role, hashed_password)
        )
        db.commit()

        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        print("Error:", str(e))  # Debugging in Flask console
        return jsonify({"error": "Internal Server Error"}), 500
