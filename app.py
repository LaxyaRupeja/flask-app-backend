from flask import Flask, jsonify, request
import sqlite3
app = Flask(__name__)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

@app.route('/menu', methods=['GET'])
def get_menu():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu_items')
    menu_items = cursor.fetchall()
    conn.close()
    return jsonify({'menu_items': menu_items}), 200

@app.route('/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu_items WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()
    if item:
        return jsonify({'menu_item': item}), 200
    else:
        return jsonify({'error': 'Menu item not found'}), 404

@app.route('/menu', methods=['POST'])
def add_menu_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    availability = data.get('availability')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO menu_items (name, description, price, availability) VALUES (?, ?, ?, ?)',
                   (name, description, price, availability))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Menu item added successfully'}), 201
    

@app.route('/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    availability = data.get('availability')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE menu_items SET name=?, description=?, price=?, availability=? WHERE id=?',
                   (name, description, price, availability, item_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Menu item updated successfully'}), 200

@app.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM menu_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Menu item deleted successfully'}), 200

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    conn.close()
    return jsonify({'orders': orders}), 200

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    customer_name = data.get('customer_name')
    item_ids = data.get('item_ids')
    status = 'received'

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (customer_name, item_ids, status) VALUES (?, ?, ?)',
                   (customer_name, item_ids, status))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Order placed successfully'}), 201
    

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    status = data.get('status')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET status=? WHERE id=?', (status, order_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Order status updated successfully'}), 200

if __name__ == '__main__':
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        availability BOOLEAN NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        item_ids TEXT NOT NULL,
        status TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
    app.run(debug=True)
