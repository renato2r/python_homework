import sqlite3   # For SQL command execution
import sys
conn = sqlite3.connect("./db/lesson.db", isolation_level='IMMEDIATE')
conn.execute("PRAGMA foreign_keys = 1")

cursor = conn.cursor()

# -----------------------------
# Task 1: Total price for the first 5 orders
print("\n🧾 Task 1: Total price for the first 5 orders")
cursor.execute('''
    SELECT o.order_id, SUM(li.quantity * p.price) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
''')
for row in cursor.fetchall():
    print(row)

# -----------------------------
# Task 2: Average total price per customer
print("\n👤 Task 2: Average total price per customer")
cursor.execute('''
    SELECT c.customer_name, AVG(sub.total_price) AS average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT o.customer_id AS customer_id_b, SUM(li.quantity * p.price) AS total_price
        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id
    ) AS sub
    ON c.customer_id = sub.customer_id_b
    GROUP BY c.customer_id;
''')
for row in cursor.fetchall():
    print(row)

# -----------------------------
# Task 3: Insert transaction for Perez and Sons
print("\n🛒 Task 3: Insert transaction for 'Perez and Sons'")
try:
    conn.execute("BEGIN;")
    
    cursor.execute('''
        INSERT INTO orders (customer_id, employee_id)
        VALUES (
            (SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'),
            (SELECT employee_id FROM employees WHERE first_name = 'Miranda')
        )
        RETURNING order_id;
    ''')
    order_id = cursor.fetchone()[0]

    cursor.execute('''
        INSERT INTO line_items (order_id, product_id, quantity)
        SELECT ?, product_id, 10
        FROM products
        ORDER BY price ASC
        LIMIT 5;
    ''', (order_id,))

    conn.commit()
    
    cursor.execute('''
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
        WHERE li.order_id = ?;
    ''', (order_id,))
    for row in cursor.fetchall():
        print(row)
except Exception as e:
    conn.rollback()
    print("❌ Erro durante a transação:", e)

# -----------------------------
# Task 4: Employees with more than 5 orders
print("\n👨‍💼 Task 4: Employees with more than 5 orders")
cursor.execute('''
    SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    GROUP BY e.employee_id
    HAVING COUNT(o.order_id) > 5;
''')
for row in cursor.fetchall():
    print(row)

conn.close()
