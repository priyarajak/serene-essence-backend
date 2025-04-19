from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import mysql.connector
from db_config import get_db_connection

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return '🕯️ Serene Essence Backend Running!'

@app.route('/products')
def get_products():
    import sys
    print("🔍 /products endpoint hit", file=sys.stderr)  # log even when stdout is suppressed

    cursor = None
    conn = None
    try:
        conn = get_db_connection()
        print("✅ DB Connection successful", file=sys.stderr)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        print(f"📦 Products fetched: {len(products)} items", file=sys.stderr)
        return jsonify(products)
    except Exception as e:
        print("❌ PRODUCTS ERROR:", e, file=sys.stderr)  # log errors even when hidden
        return jsonify({'error': 'Failed to fetch products'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/test')
def test():
    print("🧪 Test route hit!", file=sys.stderr)
    return "Test successful"


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()

        if product:
            return jsonify(product)
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        print("GET PRODUCT ERROR:", e)
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        return jsonify([
            {"id": 1, "total": 599, "status": "Delivered"},
            {"id": 2, "total": 849, "status": "Processing"},
        ])
    except Exception as e:
        print("ORDER ERROR:", e)
        return jsonify({'error': 'Could not fetch orders'}), 500


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_pw))
        conn.commit()
        return jsonify({'message': 'User registered successfully', 'user': {
        'name': name,
        'email': email,
        'id': cursor.lastrowid
    }}), 201
    except mysql.connector.errors.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409
    except Exception as e:
        print("REGISTER ERROR:", e)
        return jsonify({'error': 'Registration failed'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'User not found'}), 404

        user_id, name, hashed_pw = result

        if bcrypt.check_password_hash(hashed_pw, password):
            return jsonify({'message': 'Login successful', 'user': {'id': user_id, 'name': name, 'email': email}}), 200
        else:
            return jsonify({'error': 'Incorrect password'}), 401

    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({'error': 'Login failed'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/save-address', methods=['POST'])
def save_address():
    data = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO addresses (user_id, full_name, address_line, city, state, zip_code, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['user_id'], data['full_name'], data['address_line'],
            data['city'], data['state'], data['zip_code'], data['phone_number']
        ))
        conn.commit()
        return jsonify({'message': 'Address saved successfully'}), 200
    except Exception as e:
        print("ADDRESS SAVE ERROR:", e)
        return jsonify({'error': 'Address save failed'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/place-order', methods=['POST'])
def place_order():
    data = request.get_json()
    try:
        user_id = data['user_id']
        address_id = data['address_id']
        cart_items = data['items']
        total = data['total']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO orders (user_id, address_id, total_price) VALUES (%s, %s, %s)",
                       (user_id, address_id, total))
        order_id = cursor.lastrowid

        for item in cart_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, item['id'], item['quantity'], item['price'])
            )

        conn.commit()
        return jsonify({'message': 'Order placed successfully'}), 200
    except Exception as e:
        print("ORDER ERROR:", e)
        return jsonify({'error': 'Order failed'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/get-addresses/<int:user_id>', methods=['GET'])
def get_addresses(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM addresses WHERE user_id = %s", (user_id,))
        addresses = cursor.fetchall()
        return jsonify(addresses)
    except Exception as e:
        print("GET ADDRESSES ERROR:", e)
        return jsonify({'error': 'Could not fetch addresses'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))  # Render provides PORT env
    app.run(host="0.0.0.0", port=port)
