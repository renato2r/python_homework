import sqlite3

def connect_db():
    conn = sqlite3.connect("../db/magazines.db")
    conn.execute("PRAGMA foreign_keys = 1")  # Enforce foreign key constraints
    return conn

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            PRIMARY KEY (subscriber_id, magazine_id),
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        );
    """)

    conn.commit()

def add_publisher(conn, name):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO publishers (name) VALUES (?)", (name,))
    except sqlite3.Error as e:
        print(f"Publisher error: {e}")

def add_magazine(conn, name, publisher_name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM publishers WHERE name = ?", (publisher_name,))
        publisher = cursor.fetchone()
        if publisher:
            cursor.execute("INSERT OR IGNORE INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher[0]))
    except sqlite3.Error as e:
        print(f"Magazine error: {e}")

def add_subscriber(conn, name, address):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", (name, address))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address))
    except sqlite3.Error as e:
        print(f"Subscriber error: {e}")

def add_subscription(conn, subscriber_name, subscriber_address, magazine_name, expiration_date):
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", (subscriber_name, subscriber_address))
        sub = cursor.fetchone()
        cursor.execute("SELECT id FROM magazines WHERE name = ?", (magazine_name,))
        mag = cursor.fetchone()

        if sub and mag:
            cursor.execute("""
                INSERT OR IGNORE INTO subscriptions (subscriber_id, magazine_id, expiration_date)
                VALUES (?, ?, ?)""", (sub[0], mag[0], expiration_date))
    except sqlite3.Error as e:
        print(f"Subscription error: {e}")

def populate_data(conn):
    # Add publishers
    add_publisher(conn, "Penguin Media")
    add_publisher(conn, "Globe Publications")
    add_publisher(conn, "Sunshine Press")

    # Add magazines
    add_magazine(conn, "Tech Today", "Penguin Media")
    add_magazine(conn, "Health Weekly", "Globe Publications")
    add_magazine(conn, "Travel Life", "Sunshine Press")

    # Add subscribers
    add_subscriber(conn, "Alice Smith", "123 Maple St")
    add_subscriber(conn, "Bob Jones", "456 Oak St")
    add_subscriber(conn, "Charlie Davis", "789 Pine St")

    # Add subscriptions
    add_subscription(conn, "Alice Smith", "123 Maple St", "Tech Today", "2025-12-31")
    add_subscription(conn, "Bob Jones", "456 Oak St", "Health Weekly", "2025-11-30")
    add_subscription(conn, "Charlie Davis", "789 Pine St", "Travel Life", "2025-10-15")

def query_all_subscribers(conn):
    print("\nAll subscribers:")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subscribers")
    for row in cursor.fetchall():
        print(row)

def query_all_magazines_sorted(conn):
    print("\nAll magazines (sorted by name):")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM magazines ORDER BY name ASC")
    for row in cursor.fetchall():
        print(row)

def query_magazines_by_publisher(conn, publisher_name):
    print(f"\nMagazines published by '{publisher_name}':")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT magazines.id, magazines.name
        FROM magazines
        JOIN publishers ON magazines.publisher_id = publishers.id
        WHERE publishers.name = ?
        ORDER BY magazines.name
    """, (publisher_name,))
    for row in cursor.fetchall():
        print(row)


if __name__ == "__main__":
    try:
        conn = connect_db()
        create_tables(conn)
        populate_data(conn)
        conn.commit()
        print("Database populated successfully.")
        query_all_subscribers(conn)
        query_all_magazines_sorted(conn)
        query_magazines_by_publisher(conn, "Penguin Media")  # You can change the name as needed

    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection closed.")
