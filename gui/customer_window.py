import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os
import platform

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import DatabaseManager

class CustomerWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.db = DatabaseManager()
        
        # Detect platform
        self.is_mac = platform.system() == 'Darwin'
        self.is_windows = platform.system() == 'Windows'
        
        # Create window
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Customer Management - POS System")
        self.window.geometry("1000x800")
        self.window.configure(bg="#ffffff")
        
        # Configure ttk styles for cross-platform consistency
        self.setup_styles()
        
        # Create the interface
        self.create_widgets()
        
        # Center window
        self.center_window()
        
        # Load customers
        self.load_customers()
    
    def setup_styles(self):
        """Setup ttk styles for cross-platform consistency"""
        style = ttk.Style()
        
        # Configure Treeview style with white background
        style.configure("Treeview",
                       background="white",
                       foreground="black",
                       fieldbackground="white",
                       borderwidth=1)
        style.map('Treeview',
                 background=[('selected', '#0078d7')],
                 foreground=[('selected', 'white')])
        
        # Configure Treeview heading
        style.configure("Treeview.Heading",
                       background="#f0f0f0",
                       foreground="black",
                       borderwidth=1)
        style.map("Treeview.Heading",
                 background=[('active', '#e0e0e0')])
        
        # Configure scrollbar for white theme
        style.configure("Vertical.TScrollbar",
                       background="white",
                       bordercolor="white",
                       arrowcolor="gray",
                       darkcolor="white",
                       lightcolor="white")
        
        style.configure("Horizontal.TScrollbar",
                       background="white",
                       bordercolor="white",
                       arrowcolor="gray",
                       darkcolor="white",
                       lightcolor="white")
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"900x600+{x}+{y}")
    
    def create_button(self, parent, text, command, bg_color="#4CAF50", fg_color="white", **kwargs):
        """Create a cross-platform compatible button"""
        if self.is_mac:
            # On Mac, use a Frame with Label to simulate button with background color
            btn_frame = tk.Frame(parent, bg=bg_color, highlightbackground=bg_color, highlightthickness=1)
            btn = tk.Label(btn_frame, text=text, bg=bg_color, fg=fg_color, 
                          cursor="hand2", padx=10, pady=5, **kwargs)
            btn.pack()
            
            # Bind click events
            btn.bind("<Button-1>", lambda e: command())
            btn_frame.bind("<Button-1>", lambda e: command())
            
            # Hover effects
            def on_enter(e):
                btn.configure(bg=self.darken_color(bg_color))
                btn_frame.configure(bg=self.darken_color(bg_color))
            
            def on_leave(e):
                btn.configure(bg=bg_color)
                btn_frame.configure(bg=bg_color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
            return btn_frame
        else:
            # On Windows/Linux, regular button works fine
            return tk.Button(parent, text=text, command=command, 
                           bg=bg_color, fg=fg_color, 
                           activebackground=self.darken_color(bg_color),
                           activeforeground=fg_color, **kwargs)
    
    def darken_color(self, color):
        """Darken a color for hover effect"""
        if color.startswith('#'):
            # Convert hex to RGB, darken, then back to hex
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Darken by 20%
            r = int(r * 0.8)
            g = int(g * 0.8)
            b = int(b * 0.8)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def create_widgets(self):
        """Create all widgets for the customer window"""
        
        # Title Frame
        title_frame = tk.Frame(self.window, bg='white', relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="CUSTOMER MANAGEMENT",
            font=("Arial", 18, "bold"),
            bg='white',
            fg="#333333"
        )
        title_label.pack(side='left', padx=10, pady=5)
        
        # Close button
        close_btn = self.create_button(
            title_frame,
            text="✕ Close",
            command=self.close_window,
            bg_color="#dc3545",
            fg_color="white",
            font=("Arial", 10, "bold")
        )
        close_btn.pack(side='right', padx=10, pady=5)
        
        # Search section
        self.create_search_section()
        
        # Customer list
        self.create_customer_list()
        
        # Customer details and receipts
        self.create_details_section()
    
    def create_search_section(self):
        """Create customer search section"""
        # Use Frame instead of LabelFrame for consistent white background
        search_container = tk.Frame(self.window, bg='white')
        search_container.pack(fill='x', padx=10, pady=5)
        
        # Title for the section
        title_label = tk.Label(
            search_container,
            text="Search Customers",
            font=("Arial", 12, "bold"),
            bg='white',
            fg="#333333"
        )
        title_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Search frame with border
        search_frame = tk.Frame(search_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        search_frame.pack(fill='x', padx=5, pady=5)
        
        # Search controls
        controls_frame = tk.Frame(search_frame, bg="white")
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            controls_frame,
            text="Search:",
            font=("Arial", 10),
            fg="#333333",
            bg="white"
        ).pack(side='left')
        
        self.search_entry = tk.Entry(
            controls_frame,
            font=("Arial", 12),
            width=25,
            bg="white",
            fg="black",
            insertbackground="black"
        )
        self.search_entry.pack(side='left', padx=(10, 5))
        self.search_entry.bind('<KeyRelease>', self.search_customers)
        
        refresh_btn = self.create_button(
            controls_frame,
            text="Refresh",
            command=self.load_customers,
            bg_color="#007bff",
            fg_color='white',
            font=("Arial", 10, "bold")
        )
        refresh_btn.pack(side='left', padx=5)
    
    def create_customer_list(self):
        """Create customer list display"""
        # Container with white background
        list_container = tk.Frame(self.window, bg='white')
        list_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Title
        title_label = tk.Label(
            list_container,
            text="Customers",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Frame with border for the list
        list_frame = tk.Frame(list_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview for customers
        columns = ('Name', 'Phone', 'Total Sales', 'Balance Due', 'Last Sale')
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12,
                                         style="Treeview")
        
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
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.customer_tree.yview,
                                   style="Vertical.TScrollbar")
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.customer_tree.xview,
                                   style="Horizontal.TScrollbar")
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
        # Container with white background
        details_container = tk.Frame(self.window, bg='white')
        details_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Title
        title_label = tk.Label(
            details_container,
            text="Customer Details & Receipts",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Frame with border
        details_frame = tk.Frame(details_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        details_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Customer info
        info_frame = tk.Frame(details_frame, bg='white')
        info_frame.pack(fill='x', padx=10, pady=10)
        
        self.customer_info_label = tk.Label(
            info_frame,
            text="Select a customer to view details",
            font=("Arial", 11),
            bg='white',
            fg='#666666'
        )
        self.customer_info_label.pack(side='left')
        
        # Pay Balance button
        self.pay_balance_btn = self.create_button(
            info_frame,
            text="Pay Balance",
            command=self.pay_balance,
            bg_color='#28a745',
            fg_color='white',
            font=("Arial", 11, "bold")
        )
        self.pay_balance_btn.pack(side='right')
        
        # Initially disable the button
        if self.is_mac:
            self.pay_balance_btn.pack_forget()
        else:
            self.pay_balance_btn.config(state='disabled')
        
        # Receipt list
        receipt_frame = tk.Frame(details_frame, bg='white')
        receipt_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        tk.Label(
            receipt_frame,
            text="Recent Receipts:",
            font=("Arial", 10, "bold"),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', pady=(0, 5))
        
        # Receipt treeview
        receipt_columns = ('Sale ID', 'Date', 'Total', 'Paid', 'Balance', 'Status')
        self.receipt_tree = ttk.Treeview(receipt_frame, columns=receipt_columns, show='headings', height=4,
                                        style="Treeview")
        
        for col in receipt_columns:
            self.receipt_tree.heading(col, text=col)
            self.receipt_tree.column(col, width=80)
        
        self.receipt_tree.pack(fill='both', expand=True)
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
            
            # Color code based on balance (using light pink for balance due)
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
        
        # Configure tag colors (light pink background for customers with balance)
        self.customer_tree.tag_configure('has_balance', background="#cd8181")
    
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
            if self.is_mac:
                # Re-create button if needed on Mac
                if not self.pay_balance_btn.winfo_viewable():
                    self.pay_balance_btn.pack(side='right')
            else:
                self.pay_balance_btn.config(state='normal')
        else:
            if self.is_mac:
                self.pay_balance_btn.pack_forget()
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