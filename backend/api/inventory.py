from flask import Blueprint, request, jsonify
from db_config import connect_db  # ✅ Import database connection

bp = Blueprint('inventory', __name__)  # ✅ Create Blueprint for Inventory

# ✅ API to Retrieve All Inventory Items
@bp.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        db = connect_db()
        if db is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inventory")
        inventory_items = cursor.fetchall()

        cursor.close()
        db.close()

        if not inventory_items:
            return jsonify({"status": "error", "message": "No inventory items found"}), 404

        print("✅ Inventory Data Retrieved Successfully")
        return jsonify(inventory_items)

    except Exception as e:
        print("Database Error:", str(e))
        return jsonify({"status": "error", "message": str(e)})


# ✅ API to Add Inventory Item
@bp.route('/inventory', methods=['POST'])
def add_inventory():
    try:
        data = request.json
        print("✅ Received Inventory Data:", data)  # Debugging

        part_number = data.get("item_part")
        item_name = data.get("item_name")
        reorder_level = data.get("reorder_level")
        item_quantity = data.get("item_quantity")
        stock_status = data.get("stock_status")

        if not all([part_number, item_name, reorder_level, item_quantity]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        db = connect_db()
        if db is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        try:
            cursor = db.cursor()

            query = """INSERT INTO inventory (part_number, item_name, reorder_level,item_quantity,stock_status) 
                       VALUES (%s, %s, %s,%s,%s)"""
            values = (part_number, item_name, reorder_level,item_quantity,stock_status)

            cursor.execute(query, values)
            db.commit()

            new_item_id = cursor.lastrowid
            print(f"✅ New inventory item added with ID: {new_item_id}")  # Debugging

            return jsonify({"status": "success", "message": "Item added successfully!", "id": new_item_id})

        except Exception as db_error:
            db.rollback()  # Rollback in case of error
            print("❌ Database Error:", str(db_error))
            return jsonify({"status": "error", "message": str(db_error)})

        finally:
            cursor.close()
            db.close()

    except Exception as e:
        print("❌ Server Error:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500

# ✅ API to Update Inventory Item
@bp.route('/inventory', methods=['PUT'])
def update_inventory():
    try:
        data = request.json
        print("✅ Update Inventory Data:", data)  # ✅ Debugging

        item_id = data.get("id")
        part_number = data.get("part_number")
        brand = data.get("brand")
        stock_level = data.get("stock_level")
        unit_price = data.get("unit_price")

        if not all([item_id, part_number, brand, stock_level, unit_price]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        db = connect_db()
        if db is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = db.cursor()

        query = """UPDATE inventory SET part_number=%s, brand=%s, stock_level=%s, unit_price=%s WHERE id=%s"""
        values = (part_number, brand, stock_level, unit_price, item_id)

        cursor.execute(query, values)
        db.commit()

        # ✅ Confirm update was successful
        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "Item not found or no changes made"}), 404

        print(f"✅ Inventory item ID {item_id} updated successfully")  # ✅ Debugging

        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Item updated successfully!", "id": item_id})

    except Exception as e:
        print("Database Error:", str(e))
        return jsonify({"status": "error", "message": str(e)})
