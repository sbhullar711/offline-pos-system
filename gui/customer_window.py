import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import DatabaseManager

class CustomerWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.db = DatabaseManager()
        
        # Create window
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Customer Management - POS System")
        self.window.geometry("900x600")
        self.window.configure(bg='#f0f0f0')
        
        # Create the interface
        self.create_widgets()
        
        # Center window
        self.center_window()
        
        # Load customers
        self.load_customers()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"900x600+{x}+{y}")
    
    def create_widgets(self):
        """Create all widgets for the customer window"""
        
        # Title
        title_frame = tk.Frame(self.window, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="CUSTOMER MANAGEMENT",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(side='left')
        
        # Close button
        close_btn = tk.Button(
            title_frame,
            text="✕ Close",
            command=self.close_window,
            bg='#f44336',
            fg='white',
            font=("Arial", 10, "bold")
        )
        close_btn.pack(side='right')
        
        # Search section
        self.create_search_section()
        
        # Customer list
        self.create_customer_list()
        
        # Customer details and receipts
        self.create_details_section()
    
    def create_search_section(self):
        """Create customer search section"""
        search_frame = tk.LabelFrame(
            self.window,
            text="Search Customers",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        search_frame.pack(fill='x', padx=10, pady=5)
        
        # Search controls
        controls_frame = tk.Frame(search_frame, bg='#f0f0f0')
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            controls_frame,
            text="Search:",
            font=("Arial", 10),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.search_entry = tk.Entry(
            controls_frame,
            font=("Arial", 12),
            width=25
        )
        self.search_entry.pack(side='left', padx=(10, 5))
        self.search_entry.bind('<KeyRelease>', self.search_customers)
        
        refresh_btn = tk.Button(
            controls_frame,
            text="Refresh",
            command=self.load_customers,
            bg='#2196F3',
            fg='white',
            font=("Arial", 10, "bold")
        )
        refresh_btn.pack(side='left', padx=5)
    
    def create_customer_list(self):
        """Create customer list display"""
        list_frame = tk.LabelFrame(
            self.window,
            text="Customers",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create treeview for customers
        columns = ('Name', 'Phone', 'Total Sales', 'Balance Due', 'Last Sale')
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        self.customer_tree.heading('Name', text='Customer Name')
        self.customer_tree.heading('Phone', text='Phone Number')
        self.customer_tree.heading('Total Sales', text='Total Sales')
        self.customer_tree.heading('Balance Due', text='Balance Due')
        self.customer_tree.heading('Last Sale', text='Last Sale Date')
        
        # Column widths
        self.customer_tree.column('Name', width=200)
        self.customer_tree.column('Phone', width=120)
        self.customer_tree.column('Total Sales', width=100)
        self.customer_tree.column('Balance Due', width=100)
        self.customer_tree.column('Last Sale', width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.customer_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.customer_tree.xview)
        self.customer_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.customer_tree.grid(row=0, column=0, sticky='nsew', padx=(10, 0), pady=10)
        v_scrollbar.grid(row=0, column=1, sticky='ns', pady=10)
        h_scrollbar.grid(row=1, column=0, sticky='ew', padx=(10, 0))
        
        # Configure grid weights
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection event
        self.customer_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
        self.customer_tree.bind('<Double-1>', self.pay_balance)
    
    def create_details_section(self):
        """Create customer details and receipt section"""
        details_frame = tk.LabelFrame(
            self.window,
            text="Customer Details & Receipts",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        details_frame.pack(fill='x', padx=10, pady=5)
        
        # Customer info
        info_frame = tk.Frame(details_frame, bg='#f0f0f0')
        info_frame.pack(fill='x', padx=10, pady=5)
        
        self.customer_info_label = tk.Label(
            info_frame,
            text="Select a customer to view details",
            font=("Arial", 11),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.customer_info_label.pack(side='left')
        
        # Pay Balance button
        self.pay_balance_btn = tk.Button(
            info_frame,
            text="Pay Balance",
            command=self.pay_balance,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 11, "bold"),
            state='disabled'
        )
        self.pay_balance_btn.pack(side='right')
        
        # Receipt list (small preview)
        receipt_frame = tk.Frame(details_frame, bg='#f0f0f0')
        receipt_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            receipt_frame,
            text="Recent Receipts:",
            font=("Arial", 10, "bold"),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        # Small receipt treeview
        receipt_columns = ('Sale ID', 'Date', 'Total', 'Paid', 'Balance', 'Status')
        self.receipt_tree = ttk.Treeview(receipt_frame, columns=receipt_columns, show='headings', height=4)
        
        for col in receipt_columns:
            self.receipt_tree.heading(col, text=col)
            self.receipt_tree.column(col, width=80)
        
        self.receipt_tree.pack(fill='x', pady=5)
        self.receipt_tree.bind('<Double-1>', self.view_receipt_details)
    
    def load_customers(self):
        """Load all customers into the tree"""
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Get all customers with their sales data
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                c.id,
                c.name,
                c.phone,
                COALESCE(SUM(s.total_amount), 0) as total_sales,
                COALESCE(SUM(s.total_amount - s.paid_amount), 0) as balance_due,
                MAX(s.sale_date) as last_sale
            FROM customers c
            LEFT JOIN sales s ON c.id = s.customer_id
            GROUP BY c.id, c.name, c.phone
            ORDER BY c.name
        ''')
        
        customers = cursor.fetchall()
        conn.close()
        
        # Add customers to tree
        for customer in customers:
            customer_id, name, phone, total_sales, balance_due, last_sale = customer
            last_sale_date = last_sale[:10] if last_sale else 'Never'
            
            # Color code based on balance
            tags = []
            if balance_due > 0:
                tags = ['has_balance']
            
            self.customer_tree.insert('', 'end', values=(
                name,
                phone,
                f"${total_sales:.2f}",
                f"${balance_due:.2f}",
                last_sale_date
            ), tags=tags)
        
        # Configure tag colors
        self.customer_tree.tag_configure('has_balance', background='#ffebee')
    
    def search_customers(self, event=None):
        """Search customers by name or phone"""
        search_term = self.search_entry.get().strip().lower()
        
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        if not search_term:
            self.load_customers()
            return
        
        # Get filtered customers
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                c.id,
                c.name,
                c.phone,
                COALESCE(SUM(s.total_amount), 0) as total_sales,
                COALESCE(SUM(s.total_amount - s.paid_amount), 0) as balance_due,
                MAX(s.sale_date) as last_sale
            FROM customers c
            LEFT JOIN sales s ON c.id = s.customer_id
            WHERE LOWER(c.name) LIKE ? OR c.phone LIKE ?
            GROUP BY c.id, c.name, c.phone
            ORDER BY c.name
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        customers = cursor.fetchall()
        conn.close()
        
        # Add filtered customers to tree
        for customer in customers:
            customer_id, name, phone, total_sales, balance_due, last_sale = customer
            last_sale_date = last_sale[:10] if last_sale else 'Never'
            
            tags = []
            if balance_due > 0:
                tags = ['has_balance']
            
            self.customer_tree.insert('', 'end', values=(
                name,
                phone,
                f"${total_sales:.2f}",
                f"${balance_due:.2f}",
                last_sale_date
            ), tags=tags)
    
    def on_customer_select(self, event=None):
        """Handle customer selection"""
        selection = self.customer_tree.selection()
        if not selection:
            return
        
        # Get selected customer data
        item = self.customer_tree.item(selection[0])
        values = item['values']
        
        if not values:
            return
        
        customer_name = values[0]
        customer_phone = values[1]
        balance_due = values[3]
        
        # Update customer info display
        self.customer_info_label.config(
            text=f"Customer: {customer_name} ({customer_phone}) | Balance: {balance_due}"
        )
        
        # Enable/disable pay balance button
        balance_amount = float(balance_due.replace('$', ''))
        if balance_amount > 0:
            self.pay_balance_btn.config(state='normal')
        else:
            self.pay_balance_btn.config(state='disabled')
        
        # Load customer receipts
        self.load_customer_receipts(customer_phone)
    
    def load_customer_receipts(self, phone):
        """Load receipts for selected customer"""
        # Clear existing receipts
        for item in self.receipt_tree.get_children():
            self.receipt_tree.delete(item)
        
        # Get customer
        customer = self.db.get_customer_by_phone(phone)
        if not customer:
            return
        
        # Get customer sales
        sales = self.db.get_customer_sales(customer['id'])
        
        # Add sales to receipt tree
        for sale in sales:
            status = sale['payment_status'].replace('_', ' ').title()
            
            self.receipt_tree.insert('', 'end', values=(
                sale['id'],
                sale['sale_date'][:10] if sale['sale_date'] else 'N/A',
                f"${sale['total_amount']:.2f}",
                f"${sale['paid_amount']:.2f}",
                f"${sale['balance']:.2f}",
                status
            ))
    
    def pay_balance(self, event=None):
        """Handle balance payment"""
        selection = self.customer_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer first")
            return
        
        # Get selected customer
        item = self.customer_tree.item(selection[0])
        values = item['values']
        customer_phone = values[1]
        balance_str = values[3]
        balance_amount = float(balance_str.replace('$', ''))
        
        if balance_amount <= 0:
            messagebox.showinfo("Info", "This customer has no outstanding balance")
            return
        
        # Ask for payment amount
        payment = simpledialog.askfloat(
            "Pay Balance",
            f"Outstanding balance: {balance_str}\nEnter payment amount:",
            minvalue=0.01,
            maxvalue=balance_amount
        )
        
        if payment is None:
            return
        
        # Get customer and update payments
        customer = self.db.get_customer_by_phone(customer_phone)
        if not customer:
            return
        
        # Get unpaid sales and apply payment
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, total_amount, paid_amount 
            FROM sales 
            WHERE customer_id = ? AND payment_status != 'fully_paid'
            ORDER BY sale_date ASC
        ''', (customer['id'],))
        
        unpaid_sales = cursor.fetchall()
        remaining_payment = payment
        
        for sale_id, total_amount, paid_amount in unpaid_sales:
            if remaining_payment <= 0:
                break
            
            outstanding = total_amount - paid_amount
            payment_for_this_sale = min(remaining_payment, outstanding)
            new_paid_amount = paid_amount + payment_for_this_sale
            
            # Update payment status
            if new_paid_amount >= total_amount:
                status = 'fully_paid'
            else:
                status = 'partial'
            
            cursor.execute('''
                UPDATE sales 
                SET paid_amount = ?, payment_status = ?
                WHERE id = ?
            ''', (new_paid_amount, status, sale_id))
            
            remaining_payment -= payment_for_this_sale
        
        conn.commit()
        conn.close()
        
        # Refresh displays
        self.load_customers()
        messagebox.showinfo("Success", f"Payment of ${payment:.2f} applied successfully!")
    
    def view_receipt_details(self, event=None):
        """View detailed receipt"""
        selection = self.receipt_tree.selection()
        if not selection:
            return
        
        item = self.receipt_tree.item(selection[0])
        sale_id = item['values'][0]
        
        # Import and show receipt window
        from gui.sale_window import ReceiptWindow
        receipt_window = ReceiptWindow(self.window, self.db, sale_id)
    
    def close_window(self):
        """Close the customer window"""
        self.window.destroy()

# Main function to test the customer window
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window
    customer_window = CustomerWindow()
    root.mainloop()