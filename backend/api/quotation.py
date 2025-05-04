from flask import Blueprint, request, jsonify
from db_config import connect_db  # ✅ Import database connection

bp = Blueprint('quotation', __name__)  # ✅ Create Blueprint for Quotations

# ✅ API to Retrieve All Quotations
@bp.route('/get_quotations', methods=['GET'])
def get_quotations():
    try:
        db = connect_db()
        if db is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM quotations")
        quotations = cursor.fetchall()

        cursor.close()
        db.close()

        if not quotations:
            return jsonify({"status": "error", "message": "No quotations found"}), 404

        print("✅ Quotation Data Retrieved Successfully")
        return jsonify({"status": "success", "data": quotations})

    except Exception as e:
        print("Database Error:", str(e))
        return jsonify({"status": "error", "message": str(e)})


# ✅ API to Retrieve a Single Quotation by ID
@bp.route('/get_quotation/<int:quotation_id>', methods=['GET'])
def get_quotation(quotation_id):
    try:
        db = connect_db()
        if db is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM quotations WHERE id = %s", (quotation_id,))
        quotation = cursor.fetchone()

        cursor.close()
        db.close()

        if not quotation:
            return jsonify({"status": "error", "message": "Quotation not found"}), 404

        print(f"✅ Quotation ID {quotation_id} Retrieved Successfully")
        return jsonify({"status": "success", "data": quotation})

    except Exception as e:
        print("Database Error:", str(e))
        return jsonify({"status": "error", "message": str(e)})


# ✅ API to Add a New Quotation
@bp.route('/add_quotation', methods=['POST'])
def add_quotation():
    try:
        data = request.json
        print("✅ Received Quotation Data:", data)


        quotation_id = data.get("newQuotationID")
        requested_by = data.get("requestedBy")
        items_needed = data.get("itemsNeeded")
        request_date = data.get("requestDate")

        if not all([quotation_id, requested_by, items_needed, request_date]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        db = connect_db()
        if db is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = db.cursor()

        query = """INSERT INTO quotations (quotation_id, requested_by, items_needed, request_date, status) 
                   VALUES (%s, %s, %s, %s, 'Pending')"""
        values = (quotation_id, requested_by, items_needed, request_date)

        cursor.execute(query, values)
        db.commit()

        new_quotation_id = cursor.lastrowid
        print(f"✅ New quotation added with ID: {new_quotation_id}")

        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Quotation added successfully!", "id": new_quotation_id})

    except Exception as e:
        print("Database Error:", str(e))
        return jsonify({"status": "error", "message": str(e)})


# ✅ API to Update a Quotation
@bp.route('/update_quotation', methods=['PUT'])
def update_quotation():
    try:
        data = request.json
        print("✅ Update Quotation Data:", data)

        quotation_id = data.get("id")
        requested_by = data.get("requested_by")
        items_needed = data.get("items_needed")
        request_date = data.get("request_date")
        status = data.get("status")

        if not all([quotation_id, requested_by, items_needed, request_date, status]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        db = connect_db()
        if db is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = db.cursor()

        query = """UPDATE quotations SET requested_by=%s, items_needed=%s, request_date=%s, status=%s WHERE id=%s"""
        values = (requested_by, items_needed, request_date, status, quotation_id)

        cursor.execute(query, values)
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "Quotation not found or no changes made"}), 404

        print(f"✅ Quotation ID {quotation_id} updated successfully")

        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Quotation updated successfully!", "id": quotation_id})

    except Exception as e:
        print("Database Error:", str(e))
        return jsonify({"status": "error", "message": str(e)})


# ✅ API to Delete a Quotation
@bp.route('/delete_quotation/<int:quotation_id>', methods=['DELETE'])
def delete_quotation(quotation_id):
    try:
        db = connect_db()
        if db is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = db.cursor()

        query = "DELETE FROM quotations WHERE id=%s"
        cursor.execute(query, (quotation_id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "Quotation not found"}), 404

        print(f"✅ Quotation ID {quotation_id} deleted successfully")

        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Quotation deleted successfully!"})

    except Exception as e:
        print("Database Error:", str(e))
        return jsonify({"status": "error", "message": str(e)})
