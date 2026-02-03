import sqlite3

# ==================================================
# Section 1 – Summaries
# ==================================================

def total_customers(conn):
    query = '''
        SELECT COUNT(*) As 'TotalCustomer' FROM customers;
        '''
    cursor = conn.execute(query)
    data = cursor.fetchone()
    print(f"\nTotal Customer: {data['TotalCustomer']}")

def customer_signup_range(conn):
    # Show the earliest and latest customer signup dates.
    query = '''
        SELECT MIN(signup_date) As 'earliest', MAX(signup_date) As 'latest' FROM customers;
        '''
    cursor = conn.execute(query)
    data = cursor.fetchone()
    print(f"\nEarliest sign up customer: {data['earliest']}, latest signup customer: {data['latest']}")


def order_summary_stats(conn):
    # - total number of orders
    # - average order value
    # - highest and lowest order totals
    query = '''
        SELECT COUNT(order_id) As 'total_order', AVG(order_total) As 'avg_value',
        MAX(order_total) As 'highest_total', MIN(order_total) As 'lowest_total' FROM orders;
        '''
    cursor = conn.execute(query)
    data = cursor.fetchone()
    print(f"\nTotal order: {data['total_order']}, average order value: {data['avg_value']}")
    print(f"Highest order total: {data['highest_total']}, lowest order total: {data['lowest_total']}")

def driver_summary(conn):
    # Display the total number of drivers and their hire dates.
    query = '''
        SELECT COUNT(driver_id) As 'total_driver', MIN(hire_date) as 'earliest_driver',
        MAX(hire_date) As 'newest_driver' FROM drivers;
        '''
    cursor = conn.execute(query)
    data = cursor.fetchone()
    print(f"\nTotal driver: {data['total_driver']}, earliest hire: {data['earliest_driver']}, latest hire: {data['newest_driver']}")


# ==================================================
# Section 2 – Key Statistics
# ==================================================

def orders_per_customer(conn):
    # - Customer name
    # - Number of orders
    # - Total amount spent
    query = '''
        SELECT c.customer_name, COUNT(od.order_id) As 'total_order', SUM(od.order_total) as 'amount_spent'
        FROM customers c
        LEFT JOIN orders od ON c.customer_id=od.customer_id
        GROUP BY c.customer_name;
        '''
    cursor = conn.execute(query)
    
    for cust in cursor:
        print(f"{cust['customer_name']}: total order:{cust['total_order']}, amout spent: {cust['amount_spent']}")

def driver_workload(conn):
    # - Driver name
    # - Number of deliveries completed

    query = '''
        SELECT d.driver_name, COUNT(dl.delivery_id) As 'total_delivery'
        FROM drivers d
        LEFT JOIN deliveries dl ON d.driver_id=dl.driver_id
        GROUP BY d.driver_name;
        '''
    cursor = conn.execute(query)
    print()
    for driver in cursor:
        print(f"{driver['driver_name']} - total deliveries: {driver['total_delivery']}")

def delivery_lookup_by_id(conn, order_id):
    # - search for an order by ID
    # - customer name
    # - order total
    # - delivery date
    # - driver
    query = '''
        SELECT c.customer_name, od.order_total, dl.delivery_date, d.driver_name
        FROM orders od JOIN customers c ON od.customer_id=c.customer_id
        JOIN deliveries dl ON od.order_id=dl.order_id
        JOIN drivers d ON dl.driver_id=d.driver_id;
        '''
    cursor = conn.execute(query)
    data = cursor.fetchone()
    print()
    if data:
        print(f"{data['customer_name']}: order total: {data['order_total']}, delivery date: {data['delivery_date']}, driver:{data['driver_name']} ")
    else:
        print("lookup failed: not found")



# ==================================================
# Section 3 – Time-based Summaries
# ==================================================

def orders_per_date(conn):
    # Count the number of orders per order date.
    pass


def deliveries_per_date(conn):
    # Count the number of deliveries per delivery date.
    pass


def customer_signups_per_month(conn):
    # Count customer signups per month - you may need to do some python processing on this one!
    pass


# ==================================================
# Section 4 – Performance and Rankings
# ==================================================

def top_customers_by_spend(conn, limit=5):
    # List the top 5 customers by total spend.
    pass


def rank_drivers_by_deliveries(conn):
    # Rank drivers by number of deliveries completed.
    pass


def high_value_orders(conn, threshold):
    # Display all orders above a value which should be inputted by the user (e.g. £100)
    pass


# ==================================================
# Menus - You should not need to change any code below this point until the stretch tasks.
# ==================================================

def section_1_menu(conn):
    while True:
        print("\nSection 1 – Summaries")
        print("1. Total number of customers")
        print("2. Customer signup date range")
        print("3. Order summary statistics")
        print("4. Driver summary")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            total_customers(conn)
        elif choice == "2":
            customer_signup_range(conn)
        elif choice == "3":
            order_summary_stats(conn)
        elif choice == "4":
            driver_summary(conn)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_2_menu(conn):
    while True:
        print("\nSection 2 – Key Statistics")
        print("1. Orders per customer")
        print("2. Driver workload")
        print("3. Order delivery overview")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            orders_per_customer(conn)
        elif choice == "2":
            driver_workload(conn)
        elif choice == "3":
            order_id = input("Enter order ID: ").strip()
            if not order_id.isdigit():
                print("Please enter a valid integer order ID.")
                continue
            delivery_lookup_by_id(conn, int(order_id))
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_3_menu(conn):
    while True:
        print("\nSection 3 – Time-based Summaries")
        print("1. Orders per date")
        print("2. Deliveries per date")
        print("3. Customer signups per month")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            orders_per_date(conn)
        elif choice == "2":
            deliveries_per_date(conn)
        elif choice == "3":
            customer_signups_per_month(conn)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_4_menu(conn):
    while True:
        print("\nSection 4 – Performance and Rankings")
        print("1. Top 5 customers by total spend")
        print("2. Rank drivers by deliveries completed")
        print("3. High-value orders")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            top_customers_by_spend(conn)
        elif choice == "2":
            rank_drivers_by_deliveries(conn)
        elif choice == "3":
            try:
                threshold = float(input("Enter order value threshold (£): "))
                high_value_orders(conn, threshold)
            except:
                print("Please enter a valid numerical value.")
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def main_menu(conn):
    while True:
        print("\n=== Delivery Service Management Dashboard ===")
        print("1. Section 1 – Summaries")
        print("2. Section 2 – Key Statistics")
        print("3. Section 3 – Time-based Summaries")
        print("4. Section 4 – Performance and Rankings")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            section_1_menu(conn)
        elif choice == "2":
            section_2_menu(conn)
        elif choice == "3":
            section_3_menu(conn)
        elif choice == "4":
            section_4_menu(conn)
        elif choice == "0":
            print("Exiting dashboard.")
            break
        else:
            print("Invalid option. Please try again.")

def get_connection(db_path="food_delivery.db"):
    """
    Establish a connection to the SQLite database.
    Returns a connection object.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    conn = get_connection()
    main_menu(conn)
    conn.close()