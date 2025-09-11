import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "database/pos_system.db"):
        self.db_path = db_path
        self.ensure_db_directory()
        self.init_database()
    
    def ensure_db_directory(self):
        """Ensure the database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone VARCHAR(20) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                upc_code VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(200) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                paid_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
                payment_status VARCHAR(20) NOT NULL DEFAULT 'pay_later',
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Sale items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                item_name VARCHAR(200) NOT NULL,
                upc_code VARCHAR(50),
                quantity INTEGER NOT NULL DEFAULT 1,
                unit_price DECIMAL(10,2) NOT NULL,
                discounted_price DECIMAL(10,2),
                is_xt_item BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (sale_id) REFERENCES sales(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Customer operations
    def add_customer(self, phone: str, name: str) -> int:
        """Add a new customer and return customer ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customers (phone, name) VALUES (?, ?)",
            (phone, name)
        )
        customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return customer_id
    
    def get_customer_by_phone(self, phone: str) -> Optional[Dict]:
        """Get customer by phone number"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, phone, name, created_at FROM customers WHERE phone = ?",
            (phone,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'phone': row[1],
                'name': row[2],
                'created_at': row[3]
            }
        return None
    
    def get_customer_balance(self, customer_id: int) -> float:
        """Get customer's outstanding balance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(total_amount - paid_amount) 
            FROM sales 
            WHERE customer_id = ? AND payment_status != 'fully_paid'
        ''', (customer_id,))
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0.0
    
    # Item operations
    def add_item(self, upc_code: str, name: str, price: float) -> int:
        """Add a new item and return item ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (upc_code, name, price) VALUES (?, ?, ?)",
            (upc_code, name, price)
        )
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id
    
    def get_item_by_upc(self, upc_code: str) -> Optional[Dict]:
        """Get item by UPC code"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, upc_code, name, price FROM items WHERE upc_code = ?",
            (upc_code,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'upc_code': row[1],
                'name': row[2],
                'price': row[3]
            }
        return None
    
    def update_item_price(self, upc_code: str, new_price: float) -> bool:
        """Update item price"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE items SET price = ? WHERE upc_code = ?",
            (new_price, upc_code)
        )
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def get_all_items(self) -> List[Dict]:
        """Get all items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, upc_code, name, price FROM items ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'upc_code': row[1],
                'name': row[2],
                'price': row[3]
            }
            for row in rows
        ]
    
    # Sale operations
    def create_sale(self, customer_id: int, total_amount: float, 
                   paid_amount: float = 0, payment_status: str = 'pay_later') -> int:
        """Create a new sale and return sale ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sales (customer_id, total_amount, paid_amount, payment_status)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, total_amount, paid_amount, payment_status))
        sale_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return sale_id
    
    def add_sale_item(self, sale_id: int, item_name: str, quantity: int, 
                     unit_price: float, upc_code: str = None, 
                     discounted_price: float = None, is_xt_item: bool = False) -> int:
        """Add item to sale"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sale_items (sale_id, item_name, upc_code, quantity, 
                                  unit_price, discounted_price, is_xt_item)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (sale_id, item_name, upc_code, quantity, unit_price, discounted_price, is_xt_item))
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id
    
    def get_customer_sales(self, customer_id: int) -> List[Dict]:
        """Get all sales for a customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, total_amount, paid_amount, payment_status, sale_date
            FROM sales 
            WHERE customer_id = ? 
            ORDER BY sale_date DESC
        ''', (customer_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'total_amount': row[1],
                'paid_amount': row[2],
                'payment_status': row[3],
                'sale_date': row[4],
                'balance': row[1] - row[2]
            }
            for row in rows
        ]
    
    def get_sale_items(self, sale_id: int) -> List[Dict]:
        """Get all items for a specific sale"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_name, upc_code, quantity, unit_price, discounted_price, is_xt_item
            FROM sale_items 
            WHERE sale_id = ?
        ''', (sale_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'name': row[0],
                'upc_code': row[1],
                'quantity': row[2],
                'unit_price': row[3],
                'discounted_price': row[4] or row[3],
                'is_xt_item': row[5],
                'total': row[2] * (row[4] or row[3])
            }
            for row in rows
        ]