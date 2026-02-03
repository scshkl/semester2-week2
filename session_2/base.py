import sqlite3
# you will need to pip install pandas matplotlib
import pandas as pd
import matplotlib.pyplot as plt

def get_connection(db_path="orders.db"):
    """
    Establish a connection to the SQLite database.
    Returns a connection object.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ==================================== Level 1 =======================================
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

# ==================================== Level 2 =======================================

def top_five_customers(db):
    # Compute **total spent per customer**. Display the top 5 spenders
    query = """SELECT c.first_name, c.last_name, SUM(od.total_amount) As 'total_amount' FROM orders od
            JOIN customers c ON od.customer_id=c.customer_id
            GROUP BY c.first_name, c.last_name
            ORDER BY total_amount DESC
            LIMIT 5;"""
    cursor = db.execute(query)
    for cust in cursor:
        print(f"{cust['first_name']} {cust['last_name']}: total amount: {cust['total_amount']}")
    
def total_order_per_product_category(db):
    # Count **orders per product category** and show these in descending order. Challenge: Plot a bar chart to show this.
    query = """SELECT p.category, COUNT(oi.quantity) As 'quantity' FROM products p
            LEFT JOIN order_items oi ON p.product_id=oi.product_id
            GROUP BY p.category
            ORDER BY quantity DESC;"""
    cursor = db.execute(query)
    for product in cursor:
        print(f"{product['category']} - total order:{product['quantity']}")
    
    # todo - plot bar chart


def average_product_per_order(db):
    # Calculate **average number of products per order**
    query = """ SELECT AVG(total_item) as 'average' FROM 
            (SELECT oi.order_id, SUM(oi.quantity) As 'total_item' FROM order_items oi
            JOIN orders od ON oi.order_id=od.order_id
            GROUP BY oi.order_id);"""
    cursor = db.execute(query)
    data = cursor.fetchone()
    print(f"average product per order {data['average']}")

    # checking the total product per order
    # for data in cursor:
    #     print(f"{data['order_id']}:{data['average']}")

def delivery_status(db):
    # Summarize **deliveries by status** (`scheduled`, `delivered`, `failed`) and plot a pie chart.  
    query = """SELECT delivery_status, COUNT(delivery_id) as 'total' FROM deliveries
            GROUP BY delivery_status;"""
    cursor = db.execute(query)
    data = dict(cursor)
    for idx, item in data.items():
        print(f"{idx}:{item}")

    # todo - check why it does not work if run the whole file
    # error to do with deliveries table?
    plot_delivery_status(data)

def plot_delivery_status(data):
    data = {'delivered': 60, 'failed': 56, 'scheduled': 4}
    df = pd.DataFrame.from_dict(data.items())
    plt.pie(df[1], labels=df[0], autopct='%1.1f%%', startangle=90)
    plt.show()



# ==================================== Level 3 =======================================


def main():

    db = get_connection()
    # level 1
    # list_product_categories(db)
    # total_customers(db)
    # retrieve_customer_orders(db)
    # below_2pounds_product(db)

    # level 2
    # top_five_customers(db)
    # total_order_per_product_category(db)
    average_product_per_order(db)
    # delivery_status(db)

    # level 3
    db.close()


if __name__=="__main__":
    main()
