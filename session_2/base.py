import sqlite3
# you will need to pip install pandas matplotlib
import pandas as pd
import matplotlib as mpl

def get_connection(db_path="orders.db"):
    """
    Establish a connection to the SQLite database.
    Returns a connection object.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def list_product_categories(db):
    # List all **product categories** in the database.
    query = "SELECT name, category FROM products;"
    cursor = db.execute(query)
    for product in cursor:
        print(f"{product['name']}: {product['category']}")


def total_customers(db):
    # Count the **total number of customers**.
    query = "SELECT COUNT(customer_id) as 'total_customer' FROM customers;"
    cursor = db.execute(query)
    data = cursor.fetchone()
    print(f"\nTotal customers: {data['total_customer']}")

def retrieve_customer_orders(db):
    # Show all **orders for a given customer** (ask for a specific email). 
    email = input("Enter customer email: ")
    query = """SELECT c.first_name, c.last_name, od.order_date, p.name FROM customers c
    JOIN orders od ON c.customer_id=od.customer_id
    JOIN order_items oi ON od.order_id=oi.order_id
    JOIN products p ON oi.product_id=p.product_id
    WHERE c.email=?;"""
    cursor = db.execute(query, (email,))
    if cursor:
        for data in cursor:
            print(f"{data['first_name']} {data['last_name']}, order date: {data['order_date']}, product: {data['name']}")
    else:
        print("Not found")

def below_2pounds_product(db):
    # Display **all products priced below £2**.  
    query = "SELECT name, price FROM products WHERE price<2;"
    cursor = db.execute(query)
    for product in cursor:
        print(f"{product['name']}: {product['price']}")
def main():

    db = get_connection()
    # list_product_categories(db)
    # total_customers(db)
    # retrieve_customer_orders(db)
    below_2pounds_product(db)
    db.close()


if __name__=="__main__":
    main()
