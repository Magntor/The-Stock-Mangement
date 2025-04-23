import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'stock'
}


def get_connection():
    """Establish and return a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def initialize_db():
    """Create necessary tables if they don't exist."""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    # Use AUTO_INCREMENT for orders and sales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            pcode INT(4) PRIMARY KEY,
            pname VARCHAR(50) NOT NULL,
            pprice DECIMAL(10,2) NOT NULL,
            pqty INT NOT NULL,
            pcat VARCHAR(30)
        ) ENGINE=InnoDB;
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            orderid INT AUTO_INCREMENT PRIMARY KEY,
            orderdate DATETIME NOT NULL,
            pcode INT(4) NOT NULL,
            pprice DECIMAL(10,2) NOT NULL,
            pqty INT NOT NULL,
            supplier VARCHAR(50),
            pcat VARCHAR(30),
            FOREIGN KEY (pcode) REFERENCES product(pcode) ON DELETE CASCADE
        ) ENGINE=InnoDB;
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            salesid INT AUTO_INCREMENT PRIMARY KEY,
            salesdate DATETIME NOT NULL,
            pcode INT(4) NOT NULL,
            pprice DECIMAL(10,2) NOT NULL,
            pqty INT NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (pcode) REFERENCES product(pcode) ON DELETE CASCADE
        ) ENGINE=InnoDB;
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            uid VARCHAR(50) PRIMARY KEY,
            uname VARCHAR(50) NOT NULL,
            upwd VARCHAR(50) NOT NULL
        ) ENGINE=InnoDB;
    """)
    conn.commit()
    cursor.close()
    conn.close()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def product_menu():
    while True:
        clear_screen()
        print("\nPRODUCT MANAGEMENT\n")
        print("1. Add New Product")
        print("2. List Products")
        print("3. Update Stock Quantity")
        print("4. Delete Product")
        print("5. Back to Main Menu")
        choice = input("Enter choice: ")
        if choice == '1':
            add_product()
        elif choice == '2':
            list_products()
        elif choice == '3':
            update_stock()
        elif choice == '4':
            delete_product()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.")
        input("Press Enter to continue...")


def add_product():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        pcode = int(input("Enter product code: "))
        # Check if exists
        cursor.execute("SELECT 1 FROM product WHERE pcode=%s", (pcode,))
        if cursor.fetchone():
            print("Product code already exists.")
        else:
            pname = input("Enter product name: ")
            pqty = int(input("Enter quantity: "))
            pprice = float(input("Enter unit price: "))
            pcat = input("Enter category: ")
            cursor.execute(
                "INSERT INTO product (pcode,pname,pprice,pqty,pcat) VALUES (%s,%s,%s,%s,%s)",
                (pcode, pname, pprice, pqty, pcat)
            )
            conn.commit()
            print("Product added successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def list_products():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT pcode, pname, pprice, pqty, pcat FROM product")
    rows = cursor.fetchall()
    print("\nPRODUCT LIST")
    print(f"{'Code':<6} {'Name':<20} {'Price':<10} {'Qty':<6} {'Category'}")
    print('-'*60)
    for r in rows:
        print(f"{r[0]:<6} {r[1]:<20} {r[2]:<10.2f} {r[3]:<6} {r[4]}")
    cursor.close()
    conn.close()


def update_stock():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        pcode = int(input("Enter product code: "))
        qty = int(input("Enter quantity to add: "))
        cursor.execute("UPDATE product SET pqty = pqty + %s WHERE pcode = %s", (qty, pcode))
        conn.commit()
        print("Stock updated.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def delete_product():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        pcode = int(input("Enter product code to delete: "))
        cursor.execute("DELETE FROM product WHERE pcode = %s", (pcode,))
        conn.commit()
        print(f"{cursor.rowcount} record(s) deleted.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def purchase_menu():
    while True:
        clear_screen()
        print("\nPURCHASE MANAGEMENT\n")
        print("1. Add Purchase Order")
        print("2. List Orders")
        print("3. Back to Main Menu")
        choice = input("Enter choice: ")
        if choice == '1':
            add_order()
        elif choice == '2':
            list_orders()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")
        input("Press Enter to continue...")


def add_order():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        pcode = int(input("Enter product code: "))
        cursor.execute("SELECT pprice, pcat FROM product WHERE pcode=%s", (pcode,))
        product = cursor.fetchone()
        if not product:
            print("Product not found.")
            return
        unit_price, category = product
        qty = int(input("Enter quantity: "))
        supplier = input("Enter supplier name: ")
        now = datetime.now()
        cursor.execute(
            "INSERT INTO orders (orderdate,pcode,pprice,pqty,supplier,pcat) VALUES (%s,%s,%s,%s,%s,%s)",
            (now, pcode, unit_price, qty, supplier, category)
        )
        # Update stock
        cursor.execute("UPDATE product SET pqty = pqty + %s WHERE pcode = %s", (qty, pcode))
        conn.commit()
        print("Order placed successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def list_orders():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT orderid, orderdate, pcode, pprice, pqty, supplier, pcat FROM orders")
    rows = cursor.fetchall()
    print("\nORDER LIST")
    print(f"{'ID':<5} {'Date':<20} {'Code':<6} {'Price':<10} {'Qty':<5} {'Supplier':<15} {'Category'}")
    print('-'*80)
    for r in rows:
        print(f"{r[0]:<5} {r[1]:<20} {r[2]:<6} {r[3]:<10.2f} {r[4]:<5} {r[5]:<15} {r[6]}")
    cursor.close()
    conn.close()


def sales_menu():
    while True:
        clear_screen()
        print("\nSALES MANAGEMENT\n")
        print("1. Sell Product")
        print("2. List Sales")
        print("3. Back to Main Menu")
        choice = input("Enter choice: ")
        if choice == '1':
            sell_product()
        elif choice == '2':
            list_sales()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")
        input("Press Enter to continue...")


def sell_product():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        pcode = int(input("Enter product code: "))
        cursor.execute("SELECT pprice, pqty FROM product WHERE pcode=%s", (pcode,))
        product = cursor.fetchone()
        if not product:
            print("Product not found.")
            return
        unit_price, stock_qty = product
        qty = int(input("Enter quantity to sell: "))
        if qty > stock_qty:
            print("Insufficient stock.")
            return
        total = qty * unit_price
        now = datetime.now()
        cursor.execute(
            "INSERT INTO sales (salesdate,pcode,pprice,pqty,total) VALUES (%s,%s,%s,%s,%s)",
            (now, pcode, unit_price, qty, total)
        )
        cursor.execute("UPDATE product SET pqty = pqty - %s WHERE pcode = %s", (qty, pcode))
        conn.commit()
        print(f"Sale recorded. Total: Rs. {total:.2f}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def list_sales():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT salesid, salesdate, pcode, pprice, pqty, total FROM sales")
    rows = cursor.fetchall()
    print("\nSALES LIST")
    print(f"{'ID':<5} {'Date':<20} {'Code':<6} {'Price':<10} {'Qty':<5} {'Total'}")
    print('-'*70)
    for r in rows:
        print(f"{r[0]:<5} {r[1]:<20} {r[2]:<6} {r[3]:<10.2f} {r[4]:<5} {r[5]:.2f}")
    cursor.close()
    conn.close()


def user_menu():
    while True:
        clear_screen()
        print("\nUSER MANAGEMENT\n")
        print("1. Add User")
        print("2. List Users")
        print("3. Back to Main Menu")
        choice = input("Enter choice: ")
        if choice == '1':
            add_user()
        elif choice == '2':
            list_users()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")
        input("Press Enter to continue...")


def add_user():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        uid = input("Enter user ID (email): ")
        cursor.execute("SELECT 1 FROM user WHERE uid=%s", (uid,))
        if cursor.fetchone():
            print("User already exists.")
            return
        uname = input("Enter name: ")
        upwd = input("Enter password: ")
        cursor.execute(
            "INSERT INTO user (uid,uname,upwd) VALUES (%s,%s,%s)",
            (uid, uname, upwd)
        )
        conn.commit()
        print("User added.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def list_users():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT uid, uname FROM user")
    rows = cursor.fetchall()
    print("\nUSER LIST")
    print(f"{'UID':<25} {'Name'}")
    print('-'*40)
    for r in rows:
        print(f"{r[0]:<25} {r[1]}")
    cursor.close()
    conn.close()


def main_menu():
    initialize_db()
    while True:
        clear_screen()
        print("\nSTOCK MANAGEMENT SYSTEM\n")
        print("1. Product Management")
        print("2. Purchase Management")
        print("3. Sales Management")
        print("4. User Management")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            product_menu()
        elif choice == '2':
            purchase_menu()
        elif choice == '3':
            sales_menu()
        elif choice == '4':
            user_menu()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option.")
        input("Press Enter to continue...")


if __name__ == '__main__':
    main_menu()
