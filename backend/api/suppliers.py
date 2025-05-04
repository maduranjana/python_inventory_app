from flask import Blueprint, request, jsonify
from db_config import connect_db  # ✅ Ensure this is correct

bp = Blueprint('suppliers', __name__)  # ✅ Create Blueprint for Suppliers

# ✅ API to Fetch All Suppliers
@bp.route('/get_suppliers', methods=['GET'])
def get_suppliers():
    try:
        db = connect_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM suppliers")
        suppliers = cursor.fetchall()

        db.close()
        return jsonify(suppliers)

    except Exception as e:
        print("Database Error:", str(e))  # ✅ Debugging
        return jsonify({"status": "error", "message": str(e)})

# ✅ API to Add Supplier
@bp.route('/add_supplier', methods=['POST'])
def add_supplier():
    try:
        data = request.json
        print("Received Supplier Data:", data)  # ✅ Debugging

        company_name = data.get("company_name")
        contact_person = data.get("contact_person")
        email = data.get("email")
        phone = data.get("phone")
        status = data.get("status")

        if not all([company_name, contact_person, email, phone, status]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        db = connect_db()
        cursor = db.cursor()

        query = """INSERT INTO suppliers (company_name, contact_person, email, phone, status) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (company_name, contact_person, email, phone, status))
        db.commit()
        db.close()

        print("Supplier successfully added!")  # ✅ Debugging
        return jsonify({"status": "success", "message": "Supplier added successfully!"})

    except Exception as e:
        print("Database Error:", str(e))  # ✅ Debugging
        return jsonify({"status": "error", "message": str(e)})
