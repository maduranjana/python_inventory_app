from flask import Blueprint, request, jsonify
from db_config import connect_db  # ✅ Ensure `db_config.py` exists

bp = Blueprint('orders', __name__)  # ✅ Create Blueprint for Orders

@bp.route('/order', methods=['GET'])
def get_orders():
    try:
        db = connect_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()

        db.close()
        return jsonify(orders)

    except Exception as e:
        print("Database Error:", str(e))  # ✅ Debugging
        return jsonify({"status": "error", "message": str(e)})


@bp.route('/order', methods=['POST'])
def create_order():
    try:
        data = request.json
        print("Received Data:", data)  # ✅ Debugging

        order_id = data.get("orderID")
        ordered_by = data.get("orderedBy")
        items = data.get("items")
        order_date = data.get("orderDate")
        supplier = data.get("supplier")
        order_status = data.get("orderStatus")

        if not all([order_id, ordered_by, items, order_date, supplier, order_status]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        db = connect_db()
        cursor = db.cursor()

        query = """INSERT INTO orders (order_id, ordered_by, items, order_date, supplier, order_status) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (order_id, ordered_by, items, order_date, supplier, order_status)

        cursor.execute(query, values)
        db.commit()
        db.close()

        print("Order successfully saved!")  # ✅ Debugging
        return jsonify({"status": "success", "message": "Order created successfully!"})

    except Exception as e:
        print("Database Error:", str(e))  # ✅ Debugging
        return jsonify({"status": "error", "message": str(e)})
