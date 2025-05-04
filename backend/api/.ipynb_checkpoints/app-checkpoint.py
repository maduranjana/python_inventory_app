from flask import Flask, request, jsonify
import mysql.connector
import hashlib

app = Flask(__name__)

# ✅ Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="techfix_db"
    )

# ✅ POST API to Register Users (Includes Phone, Location, and Joined Date)
@app.route('/api/register_user', methods=['POST'])
def register_user():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    username = data.get('username')
    phone = data.get('phone')
    location = data.get('location')
    password = data.get('password')
    user_type = "Supplier"  # Default user type

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (full_name, email, username, phone, location, password, user_type, joined_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())
        """, (full_name, email, username, phone, location, hashed_password, user_type))

        conn.commit()
        return jsonify({"status": "success", "message": "User registered successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)}), 500
    finally:
        conn.close()

# ✅ GET API to Fetch Quotations
@app.route('/quotations', methods=['GET'])
def get_quotations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quotations")
    quotations = cursor.fetchall()
    conn.close()
    return jsonify(quotations)

# ✅ POST API to Add a Quotation
@app.route('/quotations', methods=['POST'])
def add_quotation():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quotations (part_number, brand, quantity, specification, status) VALUES (%s, %s, %s, %s, 'Pending')",
                   (data['part_number'], data['brand'], data['quantity'], data['specification']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Quotation added successfully!"})

# ✅ PUT API to Update a Quotation
@app.route('/quotations/<int:id>', methods=['PUT'])
def update_quotation(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE quotations SET part_number=%s, brand=%s, quantity=%s, specification=%s WHERE id=%s",
                   (data['part_number'], data['brand'], data['quantity'], data['specification'], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Quotation updated successfully!"})

# ✅ GET API to Fetch Inventory
@app.route('/inventory', methods=['GET'])
def get_inventory():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    conn.close()
    return jsonify(inventory)

# ✅ POST API to Add an Inventory Item
@app.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (part_number, product_name, brand, stock_level, unit_price) VALUES (%s, %s, %s, %s, %s)",
                   (data['part_number'], data['product_name'], data['brand'], data['stock_level'], data['unit_price']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Inventory item added successfully!"})

# ✅ PUT API to Update an Inventory Item
@app.route('/inventory/<int:id>', methods=['PUT'])
def update_inventory(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET part_number=%s, product_name=%s, brand=%s, stock_level=%s, unit_price=%s WHERE id=%s",
                   (data['part_number'], data['product_name'], data['brand'], data['stock_level'], data['unit_price'], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Inventory updated successfully!"})

# ✅ GET API to Fetch Orders
@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return jsonify(orders)

# ✅ POST API to Place an Order
@app.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (part_number, supplier, quantity, delivery_date, status) VALUES (%s, %s, %s, %s, 'Pending')",
                   (data['part_number'], data['supplier'], data['quantity'], data['delivery_date']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order placed successfully!"})

# ✅ PUT API to Update an Order
@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET part_number=%s, supplier=%s, quantity=%s, delivery_date=%s, status=%s WHERE id=%s",
                   (data['part_number'], data['supplier'], data['quantity'], data['delivery_date'], data['status'], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order updated successfully!"})

# ✅ API to Verify Supplier Login
@app.route('/api/verify_supplier', methods=['GET'])
def verify_supplier():
    email = request.args.get('email')
    password = request.args.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s AND user_type = 'Supplier'", (email, hashed_password))
    supplier = cursor.fetchone()
    conn.close()

    if supplier:
        return jsonify({"status": "success", "supplier_id": supplier["id"]})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"})

# ✅ API to Log Supplier Login Attempts
@app.route('/api/log_supplier_login', methods=['POST'])
def log_supplier_login():
    data = request.json
    email = data.get("email")
    status = data.get("status")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO supplier_logins (email, status, login_time) VALUES (%s, %s, NOW())", (email, status))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Login attempt logged"})

# ✅ Run Flask Application
if __name__ == '__main__':
    app.run(debug=True)
