import sqlite3

db_path = "../db/lesson.db"

def task1_total_price_per_order(cursor):
    print("\n🧾 Task 1: Total price for the first 5 orders")
    cursor.execute("""
        SELECT o.order_id, SUM(li.quantity * p.price) AS total_price
        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"Order ID: {row[0]}, Total Price: ${row[1]:.2f}")

def task2_avg_order_price_per_customer(cursor):
    print("\n👤 Task 2: Average total price per customer")
    cursor.execute("""
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
        GROUP BY c.customer_id
    """)
    for row in cursor.fetchall():
        print(f"Customer: {row[0]}, Avg Order Total: ${row[1]:.2f}" if row[1] else f"Customer: {row[0]}, No orders")

def task3_insert_order_transaction(cursor, conn):
    print("\n🛒 Task 3: Insert new order for 'Perez and Sons'")
    try:
        conn.execute("BEGIN")

        cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'")
        customer_id = cursor.fetchone()[0]

        cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda'")
        employee_id = cursor.fetchone()[0]

        cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
        product_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id)
            VALUES (?, ?)
            RETURNING order_id
        """, (customer_id, employee_id))
        order_id = cursor.fetchone()[0]

        for product_id in product_ids:
            cursor.execute("""
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, 10)
            """, (order_id, product_id))

        conn.commit()

        cursor.execute("""
            SELECT li.line_item_id, li.quantity, p.product_name
            FROM line_items li
            JOIN products p ON li.product_id = p.product_id
            WHERE li.order_id = ?
        """, (order_id,))
        rows = cursor.fetchall()

        print("Line Items do novo pedido:")
        for row in rows:
            print(f"Line Item ID: {row[0]}, Quantidade: {row[1]}, Produto: {row[2]}")

    except Exception as e:
        conn.rollback()
        print("❌ Erro durante a transação:", e)

def task4_employees_with_many_orders(cursor):
    print("\n👷 Task 4: Employees with more than 5 orders")
    try:
        cursor.execute("""
            SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
            FROM employees e
            JOIN orders o ON e.employee_id = o.employee_id
            GROUP BY e.employee_id
            HAVING COUNT(o.order_id) > 5
            ORDER BY order_count DESC
        """)
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(f"Employee ID: {row[0]}, Name: {row[1]} {row[2]}, Orders: {row[3]}")
        else:
            print("Nenhum funcionário com mais de 5 pedidos.")
    except Exception as e:
        print("❌ Erro na Task 4:", e)

def main():
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    task1_total_price_per_order(cursor)
    task2_avg_order_price_per_customer(cursor)
    task3_insert_order_transaction(cursor, conn)
    task4_employees_with_many_orders(cursor)

    conn.close()

if __name__ == "__main__":
    main()
