from flask import Blueprint, jsonify
from db import get_db_connection

inventory_bp = Blueprint("inventory_service", __name__)

@inventory_bp.route("/inventory", methods=["GET"])
def get_inventory():
    """Retrieve inventory from suppliers."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    conn.close()
    return jsonify(inventory)
