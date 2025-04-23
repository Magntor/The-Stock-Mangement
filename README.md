# Stock Management System

A lightweight, console-based application written in Python for managing products, purchase orders, sales, and users—all backed by a MySQL database.

**Key Features:**
- **Product Management:** Add, list, update, and delete products.
- **Purchase Orders:** Record incoming stock with supplier details, auto‑updating inventory.
- **Sales Tracking:** Process sales, calculate totals, and adjust stock in real time.
- **User Accounts:** Create and list system users.
- **Automatic Database Setup:** Tables are created on first run with proper foreign keys and constraints.

**Requirements:**
- Python 3.6+
- `mysql-connector-python` library
- MySQL server with a database named `stock`

**Getting Started:**
1. Clone or download the repository.
2. Install dependencies:
   ```bash
   pip install mysql-connector-python
   ```
3. Configure your database credentials in `stock_management.py`.
4. Run the application:
   ```bash
   python stock_management.py
   ```

**Usage:**
Navigate through the intuitive menu to manage products, orders, sales, and users. Press `Enter` to return to menus and follow on-screen prompts.

_Designed for small businesses or personal projects looking for a simple, extensible stock-control solution._

