import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import sys
import os
import platform

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import DatabaseManager

class SaleWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.db = DatabaseManager()
        
        # Detect platform
        self.is_mac = platform.system() == 'Darwin'
        self.is_windows = platform.system() == 'Windows'
        
        # Current sale data
        self.current_customer = None
        self.sale_items = []  # List of sale items
        self.total_amount = 0.0
        
        # Create window
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Sale - POS System")
        self.window.geometry("1000x700")
        self.window.configure(bg='#ffffff')
        
        # Configure ttk styles for cross-platform consistency
        self.setup_styles()
        
        # Create the interface
        self.create_widgets()
        
        # Center window
        self.center_window()
        
        # Focus on phone entry
        self.phone_entry.focus()
    
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
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"1000x700+{x}+{y}")
    
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
        """Create all widgets for the sale window"""
        
        # Title Frame
        title_frame = tk.Frame(self.window, bg='white', relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="NEW SALE",
            font=("Arial", 18, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(side='left', padx=10, pady=5)
        
        # Close button
        close_btn = self.create_button(
            title_frame,
            text="✕ Close",
            command=self.close_window,
            bg_color='#dc3545',
            fg_color='white',
            font=("Arial", 10, "bold")
        )
        close_btn.pack(side='right', padx=10, pady=5)
        
        # Customer section
        self.create_customer_section()
        
        # Item scanning section
        self.create_scanning_section()
        
        # Sale items list
        self.create_items_list()
        
        # Total and payment section
        self.create_total_section()
    
    def create_customer_section(self):
        """Create customer lookup section"""
        # Container with white background
        customer_container = tk.Frame(self.window, bg='white')
        customer_container.pack(fill='x', padx=10, pady=5)
        
        # Title
        title_label = tk.Label(
            customer_container,
            text="Customer",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Frame with border
        customer_frame = tk.Frame(customer_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        customer_frame.pack(fill='x', padx=5, pady=5)
        
        # Phone entry
        phone_frame = tk.Frame(customer_frame, bg='white')
        phone_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            phone_frame,
            text="Phone Number:",
            font=("Arial", 10),
            bg='white',
            fg='#333333'
        ).pack(side='left')
        
        self.phone_entry = tk.Entry(
            phone_frame,
            font=("Arial", 12),
            width=20,
            bg="white",
            fg="black",
            insertbackground="black"
        )
        self.phone_entry.pack(side='left', padx=(10, 5))
        self.phone_entry.bind('<Return>', self.lookup_customer)
        
        lookup_btn = self.create_button(
            phone_frame,
            text="Lookup",
            command=self.lookup_customer,
            bg_color='#007bff',
            fg_color='white',
            font=("Arial", 10, "bold")
        )
        lookup_btn.pack(side='left', padx=5)
        
        # Customer info display
        self.customer_info_label = tk.Label(
            customer_frame,
            text="Enter phone number to start sale",
            font=("Arial", 10),
            bg='white',
            fg='#666666'
        )
        self.customer_info_label.pack(padx=10, pady=(0, 10))
    
    def create_scanning_section(self):
        """Create barcode scanning and item entry section"""
        # Container with white background
        scan_container = tk.Frame(self.window, bg='white')
        scan_container.pack(fill='x', padx=10, pady=5)
        
        # Title
        title_label = tk.Label(
            scan_container,
            text="Add Items",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Frame with border
        scan_frame = tk.Frame(scan_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        scan_frame.pack(fill='x', padx=5, pady=5)
        
        # UPC entry
        upc_frame = tk.Frame(scan_frame, bg='white')
        upc_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            upc_frame,
            text="UPC/Barcode:",
            font=("Arial", 10),
            bg='white',
            fg='#333333'
        ).pack(side='left')
        
        self.upc_entry = tk.Entry(
            upc_frame,
            font=("Arial", 12),
            width=25,
            bg="white",
            fg="black",
            insertbackground="black"
        )
        self.upc_entry.pack(side='left', padx=(10, 5))
        self.upc_entry.bind('<Return>', self.add_item_by_upc)
        
        add_item_btn = self.create_button(
            upc_frame,
            text="Add Item",
            command=self.add_item_by_upc,
            bg_color='#28a745',
            fg_color='white',
            font=("Arial", 10, "bold")
        )
        add_item_btn.pack(side='left', padx=5)
        
        # XT Item button
        xt_btn = self.create_button(
            upc_frame,
            text="XT Item",
            command=self.add_xt_item,
            bg_color='#ffc107',
            fg_color='#333333',
            font=("Arial", 10, "bold")
        )
        xt_btn.pack(side='left', padx=5)
    
    def create_items_list(self):
        """Create the sale items list"""
        # Container with white background
        list_container = tk.Frame(self.window, bg='white')
        list_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Title
        title_label = tk.Label(
            list_container,
            text="Sale Items",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Frame with border
        list_frame = tk.Frame(list_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview for items - UPDATED columns
        columns = ('Item', 'Description', 'UPC', 'Qty', 'Cost', 'Unit Price', 'Disc. Price', 'Total')
        self.items_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # Configure columns - UPDATED headers
        self.items_tree.heading('Item', text='Item Name')
        self.items_tree.heading('Description', text='Description')
        self.items_tree.heading('UPC', text='UPC')
        self.items_tree.heading('Qty', text='Qty')
        self.items_tree.heading('Cost', text='Cost')
        self.items_tree.heading('Unit Price', text='Unit Price')
        self.items_tree.heading('Disc. Price', text='Disc. Price')
        self.items_tree.heading('Total', text='Total')
        
        # Column widths - UPDATED to accommodate new columns
        self.items_tree.column('Item', width=180)
        self.items_tree.column('Description', width=200)
        self.items_tree.column('UPC', width=100)
        self.items_tree.column('Qty', width=50)
        self.items_tree.column('Cost', width=70)
        self.items_tree.column('Unit Price', width=80)
        self.items_tree.column('Disc. Price', width=80)
        self.items_tree.column('Total', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.items_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)
        
        # Context menu for items
        self.items_tree.bind('<Double-1>', self.edit_item_details)
        self.items_tree.bind('<Button-3>', self.show_item_context_menu)  # Right click
    def create_total_section(self):
        """Create total and payment section"""
        total_frame = tk.Frame(self.window, bg='white', relief=tk.RAISED, borderwidth=1)
        total_frame.pack(fill='x', padx=10, pady=10)
        
        # Total display
        total_display_frame = tk.Frame(total_frame, bg='white')
        total_display_frame.pack(side='right', padx=20, pady=10)
        
        self.total_label = tk.Label(
            total_display_frame,
            text="TOTAL: $0.00",
            font=("Arial", 16, "bold"),
            bg='white',
            fg='#333333'
        )
        self.total_label.pack()
        
        # Payment buttons
        button_frame = tk.Frame(total_frame, bg='white')
        button_frame.pack(side='left', padx=10, pady=10)
        
        btn_style = {
            'font': ('Arial', 11, 'bold'),
            'width': 12,
            'height': 2
        }
        
        # Create styled buttons for each payment type
        fully_paid_btn = self.create_button(
            button_frame,
            text="FULLY PAID",
            bg_color='#28a745',
            fg_color='white',
            command=lambda: self.process_payment('fully_paid'),
            **btn_style
        )
        fully_paid_btn.pack(side='left', padx=5)
        
        pay_later_btn = self.create_button(
            button_frame,
            text="PAY LATER",
            bg_color='#ffc107',
            fg_color='#333333',
            command=lambda: self.process_payment('pay_later'),
            **btn_style
        )
        pay_later_btn.pack(side='left', padx=5)
        
        partial_btn = self.create_button(
            button_frame,
            text="PARTIAL PAY",
            bg_color='#007bff',
            fg_color='white',
            command=lambda: self.process_payment('partial'),
            **btn_style
        )
        partial_btn.pack(side='left', padx=5)
        
        # Clear sale button
        clear_btn = self.create_button(
            button_frame,
            text="CLEAR SALE",
            bg_color='#dc3545',
            fg_color='white',
            command=self.clear_sale,
            **btn_style
        )
        clear_btn.pack(side='left', padx=5)
    
    def lookup_customer(self, event=None):
        """Look up customer by phone number"""
        phone = self.phone_entry.get().strip()
        if not phone:
            messagebox.showwarning("Warning", "Please enter a phone number")
            return
        
        # Look up customer
        customer = self.db.get_customer_by_phone(phone)
        
        if customer:
            self.current_customer = customer
            balance = self.db.get_customer_balance(customer['id'])
            self.customer_info_label.config(
                text=f"Customer: {customer['name']} | Balance: ${balance:.2f}",
                fg='#28a745'
            )
            self.upc_entry.focus()  # Move focus to UPC entry
        else:
            # Ask to add new customer
            result = messagebox.askyesno(
                "Customer Not Found",
                f"Customer with phone {phone} not found.\nWould you like to add a new customer?"
            )
            if result:
                self.add_new_customer(phone)
    
    def add_new_customer(self, phone):
        """Add a new customer"""
        name = simpledialog.askstring("New Customer", "Enter customer name:")
        if name:
            try:
                customer_id = self.db.add_customer(phone, name.strip())
                self.current_customer = {
                    'id': customer_id,
                    'phone': phone,
                    'name': name.strip()
                }
                self.customer_info_label.config(
                    text=f"Customer: {name.strip()} | Balance: $0.00",
                    fg='#28a745'
                )
                self.upc_entry.focus()
                messagebox.showinfo("Success", f"Customer {name} added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding customer: {str(e)}")
    
    def add_item_by_upc(self, event=None):
        """Add item to sale by UPC code"""
        if not self.current_customer:
            messagebox.showwarning("Warning", "Please select a customer first")
            self.phone_entry.focus()
            return
        
        upc = self.upc_entry.get().strip()
        if not upc:
            messagebox.showwarning("Warning", "Please enter a UPC code")
            return
        
        # Look up item
        item = self.db.get_item_by_upc(upc)
        if item:
            self.add_item_to_sale(
                name=item['name'],
                upc_code=item['upc_code'],
                unit_price=item['price'],
                is_xt_item=False
            )
            self.upc_entry.delete(0, tk.END)  # Clear UPC entry
        else:
            messagebox.showerror("Error", f"Item with UPC {upc} not found")
    
    def add_xt_item(self):
        """Add XT item (manual entry)"""
        if not self.current_customer:
            messagebox.showwarning("Warning", "Please select a customer first")
            self.phone_entry.focus()
            return
        
        # Get XT item details
        xt_dialog = XTItemDialog(self.window, self.is_mac)
        self.window.wait_window(xt_dialog.dialog)  # Wait for dialog to close
        
        if xt_dialog.result:
            self.add_item_to_sale(
                name=xt_dialog.result['name'],
                upc_code=None,
                unit_price=xt_dialog.result['price'],
                quantity=xt_dialog.result['quantity'],
                is_xt_item=True
            )
    
    def add_item_to_sale(self, name, upc_code, unit_price, quantity=1, is_xt_item=False):
        """Add item to current sale"""
        # Check if item already exists in sale (only for non-XT items with UPC)
        if not is_xt_item and upc_code:
            for existing_item in self.sale_items:
                if existing_item['upc_code'] == upc_code and not existing_item['is_xt_item']:
                    # Item already exists, increase quantity
                    existing_item['quantity'] += quantity
                    existing_item['total'] = existing_item['quantity'] * existing_item['discounted_price']
                    self.update_items_display()
                    self.update_total()
                    return
        
        # Item doesn't exist yet, add new item
        sale_item = {
            'name': name,
            'upc_code': upc_code,
            'quantity': quantity,
            'unit_price': unit_price,
            'discounted_price': unit_price,  # Initially same as unit price
            'is_xt_item': is_xt_item,
            'total': quantity * unit_price
        }
        
        self.sale_items.append(sale_item)
        self.update_items_display()
        self.update_total()
        
    def update_items_display(self):
        """Update the items treeview display"""
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Add sale items
        for item in self.sale_items:
            # Get full item details if available
            if item['upc_code'] and not item['is_xt_item']:
                full_item = self.db.get_item_by_upc(item['upc_code'])
                if full_item:
                    item_name = full_item.get('product', item['name'])
                    description = full_item.get('description', '')[:30] + "..." if len(full_item.get('description', '')) > 30 else full_item.get('description', '')
                    cost = full_item.get('cost', 0)
                else:
                    item_name = item['name']
                    description = ''
                    cost = 0
            else:
                # XT item
                item_name = item['name']
                description = 'XT ITEM'
                cost = 0
            
            upc_display = item['upc_code'] if item['upc_code'] else 'XT'
            
            self.items_tree.insert('', 'end', values=(
                item_name,
                description,
                upc_display,
                item['quantity'],
                f"${cost:.2f}",
                f"${item['unit_price']:.2f}",
                f"${item['discounted_price']:.2f}",
                f"${item['total']:.2f}"
            ))
    def update_total(self):
        """Update the total amount"""
        self.total_amount = sum(item['total'] for item in self.sale_items)
        self.total_label.config(text=f"TOTAL: ${self.total_amount:.2f}")
    


    def edit_item_details(self, event=None):
        """Edit item price and quantity with cross-platform compatibility"""
        selection = self.items_tree.selection()
        if not selection:
            return
        
        item_index = self.items_tree.index(selection[0])
        current_item = self.sale_items[item_index]
        
        # Get cost information if available
        cost_info = ""
        full_item = None
        if current_item['upc_code'] and not current_item['is_xt_item']:
            full_item = self.db.get_item_by_upc(current_item['upc_code'])
            if full_item and 'cost' in full_item:
                cost_info = f"Cost: ${full_item['cost']:.2f}"
        
        # Detect platform
        is_mac = platform.system() == 'Darwin'
        
        # Create custom dialog for editing price and quantity
        dialog = tk.Toplevel(self.main_window.root if hasattr(self, 'main_window') else self.window)
        dialog.title("Edit Item")
        dialog.geometry("450x350")
        dialog.configure(bg='white')
        dialog.transient(self.main_window.root if hasattr(self, 'main_window') else self.window)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        parent = self.main_window.root if hasattr(self, 'main_window') else self.window
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 225
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 175
        dialog.geometry(f"450x350+{x}+{y}")
        
        result = None
        
        def create_button(parent_widget, text, command, bg_color, fg_color, **kwargs):
            """Create cross-platform button"""
            if is_mac:
                btn_frame = tk.Frame(parent_widget, bg=bg_color, highlightbackground=bg_color, highlightthickness=1)
                btn = tk.Label(btn_frame, text=text, bg=bg_color, fg=fg_color, 
                            cursor="hand2", padx=15, pady=8, **kwargs)
                btn.pack()
                btn.bind("<Button-1>", lambda e: command())
                
                # Hover effects
                def on_enter(e):
                    # Darken color on hover
                    if bg_color.startswith('#'):
                        r = int(bg_color[1:3], 16)
                        g = int(bg_color[3:5], 16)
                        b = int(bg_color[5:7], 16)
                        r = int(r * 0.8)
                        g = int(g * 0.8)
                        b = int(b * 0.8)
                        darker = f"#{r:02x}{g:02x}{b:02x}"
                        btn.configure(bg=darker)
                        btn_frame.configure(bg=darker)
                
                def on_leave(e):
                    btn.configure(bg=bg_color)
                    btn_frame.configure(bg=bg_color)
                
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
                
                return btn_frame
            else:
                return tk.Button(parent_widget, text=text, command=command, 
                            bg=bg_color, fg=fg_color, **kwargs)
        
        def on_ok():
            nonlocal result
            try:
                new_qty = int(qty_entry.get())
                new_price = float(price_entry.get())
                if new_qty <= 0 or new_price <= 0:
                    raise ValueError()
                result = {'quantity': new_qty, 'price': new_price}
                dialog.destroy()
            except ValueError:
                messagebox.showwarning("Warning", "Please enter valid positive numbers")
        
        def on_cancel():
            dialog.destroy()
        
        # Main container with white background
        main_container = tk.Frame(dialog, bg='white')
        main_container.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Item name header
        item_label = tk.Label(
            main_container, 
            text=f"Edit: {current_item['name']}", 
            bg='white', 
            fg='#333333',
            font=("Arial", 14, "bold")
        )
        item_label.pack(pady=(0, 10))
        
        # Show cost if available
        if cost_info:
            cost_label = tk.Label(
                main_container, 
                text=cost_info, 
                bg='white', 
                font=("Arial", 11), 
                fg='#666666'
            )
            cost_label.pack(pady=(0, 10))
        
        # Current price info
        current_price_label = tk.Label(
            main_container, 
            text=f"Current Price: ${current_item['discounted_price']:.2f}", 
            bg='white', 
            font=("Arial", 11), 
            fg='#007bff'
        )
        current_price_label.pack(pady=(0, 20))
        
        # Divider line
        divider = tk.Frame(main_container, bg='#e0e0e0', height=1)
        divider.pack(fill='x', pady=(0, 20))
        
        # Quantity frame
        qty_frame = tk.Frame(main_container, bg='white')
        qty_frame.pack(pady=10)
        
        qty_label = tk.Label(
            qty_frame, 
            text="Quantity:", 
            bg='white', 
            fg='#333333',
            font=("Arial", 11, "bold"),
            width=12,
            anchor='e'
        )
        qty_label.pack(side='left')
        
        qty_entry = tk.Entry(
            qty_frame, 
            font=("Arial", 11), 
            width=15,
            bg='white',
            fg='black',
            insertbackground='black',
            relief=tk.SOLID,
            borderwidth=1
        )
        qty_entry.pack(side='left', padx=(10, 0))
        qty_entry.insert(0, str(current_item['quantity']))
        qty_entry.select_range(0, tk.END)
        
        # Price frame
        price_frame = tk.Frame(main_container, bg='white')
        price_frame.pack(pady=10)
        
        price_label = tk.Label(
            price_frame, 
            text="New Price ($):", 
            bg='white', 
            fg='#333333',
            font=("Arial", 11, "bold"),
            width=12,
            anchor='e'
        )
        price_label.pack(side='left')
        
        price_entry = tk.Entry(
            price_frame, 
            font=("Arial", 11), 
            width=15,
            bg='white',
            fg='black',
            insertbackground='black',
            relief=tk.SOLID,
            borderwidth=1
        )
        price_entry.pack(side='left', padx=(10, 0))
        price_entry.insert(0, str(current_item['discounted_price']))
        
        # Profit/Loss calculation if cost is available
        profit_label = None
        if cost_info and full_item and 'cost' in full_item:
            def update_profit_loss():
                try:
                    new_price = float(price_entry.get())
                    cost = full_item['cost']
                    profit_loss = new_price - cost
                    profit_percentage = ((profit_loss / cost) * 100) if cost > 0 else 0
                    
                    if profit_loss >= 0:
                        profit_label.config(
                            text=f"Profit: ${profit_loss:.2f} ({profit_percentage:.1f}%)", 
                            fg='#28a745'
                        )
                    else:
                        profit_label.config(
                            text=f"Loss: ${abs(profit_loss):.2f} ({profit_percentage:.1f}%)", 
                            fg='#dc3545'
                        )
                except ValueError:
                    profit_label.config(
                        text="Enter valid price to see profit/loss", 
                        fg='#999999'
                    )
            
            # Profit/Loss display frame with background
            profit_frame = tk.Frame(main_container, bg='#f8f9fa', relief=tk.SOLID, borderwidth=1)
            profit_frame.pack(pady=(15, 0), padx=20, fill='x')
            
            profit_label = tk.Label(
                profit_frame, 
                text="", 
                bg='#f8f9fa', 
                font=("Arial", 11, "bold"),
                pady=8
            )
            profit_label.pack()
            
            # Update profit/loss when price changes
            price_entry.bind('<KeyRelease>', lambda e: update_profit_loss())
            update_profit_loss()  # Initial calculation
        
        # Buttons frame
        button_frame = tk.Frame(main_container, bg='white')
        button_frame.pack(pady=(25, 10))
        
        # Update button
        update_btn = create_button(
            button_frame, 
            text="Update", 
            command=on_ok, 
            bg_color='#28a745', 
            fg_color='white',
            font=("Arial", 11, "bold"),
            width=10
        )
        update_btn.pack(side='left', padx=10)
        
        # Cancel button
        cancel_btn = create_button(
            button_frame, 
            text="Cancel", 
            command=on_cancel, 
            bg_color='#dc3545', 
            fg_color='white',
            font=("Arial", 11, "bold"),
            width=10
        )
        cancel_btn.pack(side='left', padx=10)
        
        # Bind keyboard shortcuts
        dialog.bind('<Return>', lambda e: on_ok())
        dialog.bind('<Escape>', lambda e: on_cancel())
        
        # Focus on quantity entry
        qty_entry.focus()
        
        # Wait for dialog to close
        parent.wait_window(dialog)
        
        # Apply changes if user clicked OK
        if result:
            current_item['quantity'] = result['quantity']
            current_item['discounted_price'] = result['price']
            current_item['total'] = current_item['quantity'] * current_item['discounted_price']
            self.update_items_display()
            self.update_total()
    def show_item_context_menu(self, event):
        """Show context menu for items"""
        selection = self.items_tree.selection()
        if not selection:
            return
        
        context_menu = tk.Menu(self.window, tearoff=0)
        context_menu.add_command(label="Edit Price & Quantity", command=self.edit_item_details)
        context_menu.add_command(label="Remove Item", command=self.remove_selected_item)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
        
    def remove_selected_item(self):
        """Remove selected item from sale"""
        selection = self.items_tree.selection()
        if not selection:
            return
        
        item_index = self.items_tree.index(selection[0])
        removed_item = self.sale_items.pop(item_index)
        
        self.update_items_display()
        self.update_total()
        
        messagebox.showinfo("Item Removed", f"Removed {removed_item['name']} from sale")
    
    def process_payment(self, payment_type):
        """Process the payment and complete the sale"""
        if not self.current_customer:
            messagebox.showwarning("Warning", "Please select a customer first")
            return
        
        if not self.sale_items:
            messagebox.showwarning("Warning", "Please add items to the sale")
            return
        
        paid_amount = 0.0
        
        if payment_type == 'fully_paid':
            paid_amount = self.total_amount
        elif payment_type == 'partial':
            paid_amount = simpledialog.askfloat(
                "Partial Payment",
                f"Total: ${self.total_amount:.2f}\nEnter amount paid:",
                minvalue=0.0,
                maxvalue=self.total_amount
            )
            if paid_amount is None:
                return
        # For 'pay_later', paid_amount remains 0.0
        
        try:
            # Create sale record
            sale_id = self.db.create_sale(
                customer_id=self.current_customer['id'],
                total_amount=self.total_amount,
                paid_amount=paid_amount,
                payment_status=payment_type
            )
            
            # Add sale items
            for item in self.sale_items:
                self.db.add_sale_item(
                    sale_id=sale_id,
                    item_name=item['name'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    upc_code=item['upc_code'],
                    discounted_price=item['discounted_price'],
                    is_xt_item=item['is_xt_item']
                )
            
            # Show receipt
            self.show_receipt(sale_id)
            
            # Clear sale for next transaction
            self.clear_sale()
            
            messagebox.showinfo("Success", f"Sale completed! Sale ID: {sale_id}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing sale: {str(e)}")
        
    def show_receipt(self, sale_id):
        """Show receipt for the completed sale"""
        receipt_window = ReceiptWindow(self.window, self.db, sale_id)
    
    def clear_sale(self):
        """Clear current sale"""
        self.sale_items = []
        self.total_amount = 0.0
        self.current_customer = None
        
        self.phone_entry.delete(0, tk.END)
        self.upc_entry.delete(0, tk.END)
        self.customer_info_label.config(
            text="Enter phone number to start sale",
            fg='#666666'
        )
        
        self.update_items_display()
        self.update_total()
        
        self.phone_entry.focus()
    
    def close_window(self):
        """Close the sale window"""
        if self.sale_items:
            result = messagebox.askyesno(
                "Confirm Close",
                "You have items in the current sale. Are you sure you want to close?"
            )
            if not result:
                return
        
        self.window.destroy()

class EditItemDialog:
    """Dialog for editing item price and quantity"""
    def __init__(self, parent, current_item, is_mac):
        self.result = None
        self.is_mac = is_mac
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Item")
        self.dialog.geometry("400x250")
        self.dialog.configure(bg='white')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 125
        self.dialog.geometry(f"400x250+{x}+{y}")
        
        self.create_widgets(current_item)
        
        # Focus on quantity entry
        self.qty_entry.focus()
        self.qty_entry.select_range(0, tk.END)
    
    def create_button(self, parent, text, command, bg_color, fg_color, **kwargs):
        """Create cross-platform button"""
        if self.is_mac:
            btn_frame = tk.Frame(parent, bg=bg_color, highlightbackground=bg_color, highlightthickness=1)
            btn = tk.Label(btn_frame, text=text, bg=bg_color, fg=fg_color, 
                          cursor="hand2", padx=10, pady=5, **kwargs)
            btn.pack()
            btn.bind("<Button-1>", lambda e: command())
            return btn_frame
        else:
            return tk.Button(parent, text=text, command=command, 
                           bg=bg_color, fg=fg_color, **kwargs)
    
    def create_widgets(self, current_item):
        """Create dialog widgets"""
        # Title
        tk.Label(
            self.dialog, 
            text=f"Edit: {current_item['name']}", 
            bg='white', 
            fg='#333333',
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Quantity
        qty_frame = tk.Frame(self.dialog, bg='white')
        qty_frame.pack(pady=10)
        tk.Label(qty_frame, text="Quantity:", bg='white', fg='#333333', font=("Arial", 11)).pack(side='left')
        self.qty_entry = tk.Entry(qty_frame, font=("Arial", 11), width=10, bg='white', fg='black')
        self.qty_entry.pack(side='left', padx=(10, 0))
        self.qty_entry.insert(0, str(current_item['quantity']))
        
        # Price
        price_frame = tk.Frame(self.dialog, bg='white')
        price_frame.pack(pady=10)
        tk.Label(price_frame, text="Price ($):", bg='white', fg='#333333', font=("Arial", 11)).pack(side='left')
        self.price_entry = tk.Entry(price_frame, font=("Arial", 11), width=10, bg='white', fg='black')
        self.price_entry.pack(side='left', padx=(10, 0))
        self.price_entry.insert(0, str(current_item['discounted_price']))
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg='white')
        button_frame.pack(pady=20)
        
        ok_btn = self.create_button(button_frame, text="OK", command=self.on_ok, 
                                   bg_color='#28a745', fg_color='white', width=8)
        ok_btn.pack(side='left', padx=5)
        
        cancel_btn = self.create_button(button_frame, text="Cancel", command=self.on_cancel,
                                       bg_color='#dc3545', fg_color='white', width=8)
        cancel_btn.pack(side='left', padx=5)
        
        self.dialog.bind('<Return>', lambda e: self.on_ok())
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def on_ok(self):
        """Handle OK button"""
        try:
            new_qty = int(self.qty_entry.get())
            new_price = float(self.price_entry.get())
            if new_qty <= 0 or new_price <= 0:
                raise ValueError()
            self.result = {'quantity': new_qty, 'price': new_price}
            self.dialog.destroy()
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid positive numbers")
    
    def on_cancel(self):
        """Handle Cancel button"""
        self.dialog.destroy()

class XTItemDialog:
    """Dialog for adding XT items"""
    def __init__(self, parent, is_mac):
        self.result = None
        self.is_mac = is_mac
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add XT Item")
        self.dialog.geometry("400x250")
        self.dialog.configure(bg='white')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 125
        self.dialog.geometry(f"400x250+{x}+{y}")
        
        self.create_widgets()
        
        # Focus on name entry
        self.name_entry.focus()
    
    def create_button(self, parent, text, command, bg_color, fg_color, **kwargs):
        """Create cross-platform button"""
        if self.is_mac:
            btn_frame = tk.Frame(parent, bg=bg_color, highlightbackground=bg_color, highlightthickness=1)
            btn = tk.Label(btn_frame, text=text, bg=bg_color, fg=fg_color, 
                          cursor="hand2", padx=10, pady=5, **kwargs)
            btn.pack()
            btn.bind("<Button-1>", lambda e: command())
            return btn_frame
        else:
            return tk.Button(parent, text=text, command=command, 
                           bg=bg_color, fg=fg_color, **kwargs)
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Title
        title_label = tk.Label(
            self.dialog,
            text="Add XT Item",
            font=("Arial", 14, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.dialog, bg='white')
        input_frame.pack(padx=20, pady=10, fill='x')
        
        # Name
        tk.Label(input_frame, text="Item Name:", bg='white', fg='#333333').grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(input_frame, width=30, bg='white', fg='black')
        self.name_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Quantity
        tk.Label(input_frame, text="Quantity:", bg='white', fg='#333333').grid(row=1, column=0, sticky='w', pady=5)
        self.quantity_entry = tk.Entry(input_frame, width=30, bg='white', fg='black')
        self.quantity_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        self.quantity_entry.insert(0, "1")
        
        # Price
        tk.Label(input_frame, text="Price:", bg='white', fg='#333333').grid(row=2, column=0, sticky='w', pady=5)
        self.price_entry = tk.Entry(input_frame, width=30, bg='white', fg='black')
        self.price_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg='white')
        button_frame.pack(pady=20)
        
        add_btn = self.create_button(
            button_frame,
            text="Add Item",
            command=self.add_item,
            bg_color='#28a745',
            fg_color='white',
            font=("Arial", 11, "bold"),
            width=10
        )
        add_btn.pack(side='left', padx=5)
        
        cancel_btn = self.create_button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            bg_color='#dc3545',
            fg_color='white',
            font=("Arial", 11, "bold"),
            width=10
        )
        cancel_btn.pack(side='left', padx=5)
        
        # Bind Enter key to add item
        self.dialog.bind('<Return>', lambda e: self.add_item())
    
    def add_item(self):
        """Add the XT item"""
        name = self.name_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()
        price_str = self.price_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter item name")
            return
        
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid quantity")
            return
        
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid price")
            return
        
        self.result = {
            'name': name,
            'quantity': quantity,
            'price': price
        }
        
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()

class ReceiptWindow:
    """Receipt display and printing window"""
    def __init__(self, parent, db, sale_id):
        self.db = db
        self.sale_id = sale_id
        
        # Detect platform
        self.is_mac = platform.system() == 'Darwin'
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Receipt - Sale #{sale_id}")
        self.window.geometry("500x700")
        self.window.configure(bg='white')
        
        self.create_receipt()
    
    def create_button(self, parent, text, command, bg_color, fg_color, **kwargs):
        """Create cross-platform button"""
        if self.is_mac:
            btn_frame = tk.Frame(parent, bg=bg_color, highlightbackground=bg_color, highlightthickness=1)
            btn = tk.Label(btn_frame, text=text, bg=bg_color, fg=fg_color, 
                          cursor="hand2", padx=15, pady=10, **kwargs)
            btn.pack()
            btn.bind("<Button-1>", lambda e: command())
            return btn_frame
        else:
            return tk.Button(parent, text=text, command=command, 
                           bg=bg_color, fg=fg_color, **kwargs)
    
    def create_receipt(self):
        """Create receipt display"""
        # Get sale data
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get sale info
        cursor.execute('''
            SELECT s.total_amount, s.paid_amount, s.payment_status, s.sale_date, c.name, c.phone
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            WHERE s.id = ?
        ''', (self.sale_id,))
        sale_info = cursor.fetchone()
        
        # Get sale items
        sale_items = self.db.get_sale_items(self.sale_id)
        
        conn.close()
        
        # Calculate tax details
        from config import RECEIPT_COMPANY_NAME, RECEIPT_ADDRESS
        
        subtotal = sale_info[0]  # Total amount includes everything
        
        # Create receipt text
        receipt_text = f"""
{RECEIPT_COMPANY_NAME.center(48)}
{RECEIPT_ADDRESS.replace(chr(10), chr(10)).center(48)}
{'=' * 48}

Sale #: {self.sale_id}
Date: {sale_info[3][:19] if sale_info[3] else 'N/A'}
Customer: {sale_info[4]}
Phone: {sale_info[5]}

{'=' * 48}
ITEMS:
{'=' * 48}
"""
# In ReceiptWindow.create_receipt(), replace the items section:
        for item in sale_items:
            # Get full item details from database
            full_item = self.db.get_item_by_upc(item['upc_code']) if item['upc_code'] else None
            
            if full_item:
                # Show: UPC, Brand, Product, Description, Price
                receipt_text += f"""
        {full_item['upc_code']}
        {full_item['brand']} {full_item['product']}
        {full_item['description'][:45]}
        {item['quantity']} x ${item['discounted_price']:.2f} = ${item['total']:.2f}
        """
            else:
                # XT item or item not found
                receipt_text += f"""
        {item['name']}
        XT ITEM
        {item['quantity']} x ${item['discounted_price']:.2f} = ${item['total']:.2f}
        """



        
        receipt_text += f"""
{'=' * 48}
{'TOTAL:'.ljust(40)}${subtotal:.2f}
{'PAID:'.ljust(40)}${sale_info[1]:.2f}
{'BALANCE:'.ljust(40)}${subtotal - sale_info[1]:.2f} 
Payment: {sale_info[2].replace('_', ' ').title()}

{'=' * 48}
Thank you for your business!
{'=' * 48}
        """
        
        # Store receipt text for printing
        self.receipt_text = receipt_text
        
        # Create frame for receipt
        receipt_frame = tk.Frame(self.window, bg='white')
        receipt_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create text widget
        text_widget = tk.Text(
            receipt_frame,
            font=("Courier New", 9),
            bg='white',
            fg='black',
            relief='flat',
            wrap='none'
        )
        text_widget.pack(fill='both', expand=True)
        
        # Insert receipt text
        text_widget.insert('1.0', receipt_text)
        text_widget.config(state='disabled')
        
        # Button frame
        button_frame = tk.Frame(self.window, bg='white')
        button_frame.pack(pady=10)
        
        # Print button
        print_btn = self.create_button(
            button_frame,
            text="🖨️ Print Receipt",
            command=self.print_receipt,
            bg_color='#28a745',
            fg_color='white',
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        )
        print_btn.pack(side='left', padx=5)
        
        # Close button
        close_btn = self.create_button(
            button_frame,
            text="Close",
            command=self.window.destroy,
            bg_color='#6c757d',
            fg_color='white',
            font=("Arial", 12, "bold"),
            width=10,
            height=2
        )
        close_btn.pack(side='left', padx=5)
    
    def print_receipt(self):
        """Print receipt to Z-Star printer"""
        try:
            from utils.printer import ZStarPrinter
            printer = ZStarPrinter()
            
            success = printer.print_receipt(self.receipt_text)
            
            if success:
                messagebox.showinfo("Print Success", "Receipt sent to printer successfully!")
            else:
                messagebox.showerror("Print Error", "Failed to print receipt. Please check your printer connection.")
                
        except ImportError:
            messagebox.showerror("Print Error", "Printer module not found. Please check printer setup.")
        except Exception as e:
            messagebox.showerror("Print Error", f"Error printing receipt: {str(e)}")

# Main function to test the sale window
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window
    sale_window = SaleWindow()
    root.mainloop()