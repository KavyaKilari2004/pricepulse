import sqlite3

conn = sqlite3.connect("price_data.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()


if rows:
    print("\nProduct data found in database:\n")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Price: {row[2]}")
        print(f"URL: {row[3]}")
        print(f"Timestamp: {row[4]}")
        print("-" * 50)
else:
    print("No product data found in the database.")

# Close connection
conn.close()
