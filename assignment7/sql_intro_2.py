import sqlite3
import pandas as pd

def main():
    # Connect to the database
    conn = sqlite3.connect("../db/lesson.db")

    # SQL JOIN query to retrieve data from line_items and products
    query = """
    SELECT 
        line_items.line_item_id,
        line_items.quantity,
        line_items.product_id,
        products.product_name,
        products.price
    FROM line_items
    JOIN products ON line_items.product_id = products.product_id
    """

    # Read query into DataFrame
    df = pd.read_sql_query(query, conn)

    print("First 5 rows of raw data:")
    print(df.head())

    # Add a 'total' column: quantity * price
    df['total'] = df['quantity'] * df['price']
    print("\nFirst 5 rows with total column:")
    print(df.head())

    # Group by product_id and summarize
    summary = df.groupby('product_id').agg({
        'line_item_id': 'count',
        'total': 'sum',
        'product_name': 'first'
    }).reset_index()

    # Rename columns for clarity
    summary = summary.rename(columns={
        'line_item_id': 'order_count',
        'total': 'total_paid'
    })

    # Sort by product_name
    summary = summary.sort_values(by='product_name')

    print("\nSummary (first 5 rows):")
    print(summary.head())

    # Save to CSV
    summary.to_csv("order_summary.csv", index=False)
    print("\nSummary written to order_summary.csv")

    # Close DB connection
    conn.close()

if __name__ == "__main__":
    main()
