import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import DatabaseManager

class SaleWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.db = DatabaseManager()
        
        # Current sale data
        self.current_customer = None
        self.sale_items = []  # List of sale items
        self.total_amount = 0.0
        
        # Create window
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Sale - POS System")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f0f0f0')
        
        # Create the interface
        self.create_widgets()
        
        # Center window
        self.center_window()
        
        # Focus on phone entry
        self.phone_entry.focus()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"1000x700+{x}+{y}")
    
    def create_widgets(self):
        """Create all widgets for the sale window"""
        
        # Title
        title_frame = tk.Frame(self.window, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="NEW SALE",
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
        customer_frame = tk.LabelFrame(
            self.window,
            text="Customer",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        customer_frame.pack(fill='x', padx=10, pady=5)
        
        # Phone entry
        phone_frame = tk.Frame(customer_frame, bg='#f0f0f0')
        phone_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            phone_frame,
            text="Phone Number:",
            font=("Arial", 10),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.phone_entry = tk.Entry(
            phone_frame,
            font=("Arial", 12),
            width=20
        )
        self.phone_entry.pack(side='left', padx=(10, 5))
        self.phone_entry.bind('<Return>', self.lookup_customer)
        
        lookup_btn = tk.Button(
            phone_frame,
            text="Lookup",
            command=self.lookup_customer,
            bg='#2196F3',
            fg='white',
            font=("Arial", 10, "bold")
        )
        lookup_btn.pack(side='left', padx=5)
        
        # Customer info display
        self.customer_info_label = tk.Label(
            customer_frame,
            text="Enter phone number to start sale",
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.customer_info_label.pack(padx=10, pady=5)
    
    def create_scanning_section(self):
        """Create barcode scanning and item entry section"""
        scan_frame = tk.LabelFrame(
            self.window,
            text="Add Items",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        scan_frame.pack(fill='x', padx=10, pady=5)
        
        # UPC entry
        upc_frame = tk.Frame(scan_frame, bg='#f0f0f0')
        upc_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            upc_frame,
            text="UPC/Barcode:",
            font=("Arial", 10),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.upc_entry = tk.Entry(
            upc_frame,
            font=("Arial", 12),
            width=25
        )
        self.upc_entry.pack(side='left', padx=(10, 5))
        self.upc_entry.bind('<Return>', self.add_item_by_upc)
        
        add_item_btn = tk.Button(
            upc_frame,
            text="Add Item",
            command=self.add_item_by_upc,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 10, "bold")
        )
        add_item_btn.pack(side='left', padx=5)
        
        # XT Item button
        xt_btn = tk.Button(
            upc_frame,
            text="XT Item",
            command=self.add_xt_item,
            bg='#FF9800',
            fg='white',
            font=("Arial", 10, "bold")
        )
        xt_btn.pack(side='left', padx=5)
    
    def create_items_list(self):
        """Create the sale items list"""
        list_frame = tk.LabelFrame(
            self.window,
            text="Sale Items",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create treeview for items
        columns = ('Item', 'UPC', 'Qty', 'Unit Price', 'Disc. Price', 'Total')
        self.items_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.items_tree.heading('Item', text='Item Name')
        self.items_tree.heading('UPC', text='UPC')
        self.items_tree.heading('Qty', text='Qty')
        self.items_tree.heading('Unit Price', text='Unit Price')
        self.items_tree.heading('Disc. Price', text='Disc. Price')
        self.items_tree.heading('Total', text='Total')
        
        # Column widths
        self.items_tree.column('Item', width=250)
        self.items_tree.column('UPC', width=120)
        self.items_tree.column('Qty', width=60)
        self.items_tree.column('Unit Price', width=100)
        self.items_tree.column('Disc. Price', width=100)
        self.items_tree.column('Total', width=100)
        
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
        total_frame = tk.Frame(self.window, bg='#f0f0f0')
        total_frame.pack(fill='x', padx=10, pady=10)
        
        # Total display
        total_display_frame = tk.Frame(total_frame, bg='#f0f0f0')
        total_display_frame.pack(side='right')
        
        self.total_label = tk.Label(
            total_display_frame,
            text="TOTAL: $0.00",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.total_label.pack()
        
        # Payment buttons
        button_frame = tk.Frame(total_frame, bg='#f0f0f0')
        button_frame.pack(side='left')
        
        btn_style = {
            'font': ('Arial', 12, 'bold'),
            'width': 12,
            'height': 2
        }
        
        fully_paid_btn = tk.Button(
            button_frame,
            text="FULLY PAID",
            bg='#4CAF50',
            fg='white',
            command=lambda: self.process_payment('fully_paid'),
            **btn_style
        )
        fully_paid_btn.pack(side='left', padx=5)
        
        pay_later_btn = tk.Button(
            button_frame,
            text="PAY LATER",
            bg='#FF9800',
            fg='white',
            command=lambda: self.process_payment('pay_later'),
            **btn_style
        )
        pay_later_btn.pack(side='left', padx=5)
        
        partial_btn = tk.Button(
            button_frame,
            text="PARTIAL PAY",
            bg='#2196F3',
            fg='white',
            command=lambda: self.process_payment('partial'),
            **btn_style
        )
        partial_btn.pack(side='left', padx=5)
        
        # Clear sale button
        clear_btn = tk.Button(
            button_frame,
            text="CLEAR SALE",
            bg='#f44336',
            fg='white',
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
                fg='#4CAF50'
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
                    fg='#4CAF50'
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
        xt_dialog = XTItemDialog(self.window)
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
            upc_display = item['upc_code'] if item['upc_code'] else 'XT'
            self.items_tree.insert('', 'end', values=(
                item['name'],
                upc_display,
                item['quantity'],
                f"${item['unit_price']:.2f}",
                f"${item['discounted_price']:.2f}",
                f"${item['total']:.2f}"
            ))
    
    def update_total(self):
        """Update the total amount"""
        self.total_amount = sum(item['total'] for item in self.sale_items)
        self.total_label.config(text=f"TOTAL: ${self.total_amount:.2f}")
    
    def edit_item_price(self, event=None):
        """Edit item price (for discounts)"""
        selection = self.items_tree.selection()
        if not selection:
            return
        
        item_index = self.items_tree.index(selection[0])
        current_item = self.sale_items[item_index]
        
        # Ask for new price
        new_price = simpledialog.askfloat(
            "Adjust Price",
            f"Enter new price for {current_item['name']}:",
            initialvalue=current_item['discounted_price'],
            minvalue=0.01
        )
        
        if new_price is not None:
            current_item['discounted_price'] = new_price
            current_item['total'] = current_item['quantity'] * new_price
            self.update_items_display()
            self.update_total()
    
    def show_item_context_menu(self, event):
        """Show context menu for items"""
        selection = self.items_tree.selection()
        if not selection:
            return
        
        context_menu = tk.Menu(self.main_window.root if hasattr(self, 'main_window') else self.window, tearoff=0)
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
    def edit_item_details(self, event=None):
        """Edit item price and quantity"""
        selection = self.items_tree.selection()
        if not selection:
            return
        
        item_index = self.items_tree.index(selection[0])
        current_item = self.sale_items[item_index]
        
        # Create custom dialog for editing price and quantity
        dialog = tk.Toplevel(self.main_window.root if hasattr(self, 'main_window') else self.window)
        dialog.title("Edit Item")
        dialog.geometry("400x250")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.main_window.root if hasattr(self, 'main_window') else self.window)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        parent = self.main_window.root if hasattr(self, 'main_window') else self.window
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 125
        dialog.geometry(f"400x250+{x}+{y}")
        
        result = None
        
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
        
        # Dialog content
        tk.Label(dialog, text=f"Edit: {current_item['name']}", bg='#f0f0f0', font=("Arial", 12, "bold")).pack(pady=10)
        
        # Quantity
        qty_frame = tk.Frame(dialog, bg='#f0f0f0')
        qty_frame.pack(pady=10)
        tk.Label(qty_frame, text="Quantity:", bg='#f0f0f0', font=("Arial", 11)).pack(side='left')
        qty_entry = tk.Entry(qty_frame, font=("Arial", 11), width=10)
        qty_entry.pack(side='left', padx=(10, 0))
        qty_entry.insert(0, str(current_item['quantity']))
        qty_entry.select_range(0, tk.END)
        
        # Price
        price_frame = tk.Frame(dialog, bg='#f0f0f0')
        price_frame.pack(pady=10)
        tk.Label(price_frame, text="Price ($):", bg='#f0f0f0', font=("Arial", 11)).pack(side='left')
        price_entry = tk.Entry(price_frame, font=("Arial", 11), width=10)
        price_entry.pack(side='left', padx=(10, 0))
        price_entry.insert(0, str(current_item['discounted_price']))
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="OK", command=on_ok, bg='#4CAF50', fg='white', width=8).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=on_cancel, bg='#f44336', fg='white', width=8).pack(side='left', padx=5)
        
        dialog.bind('<Return>', lambda e: on_ok())
        dialog.bind('<Escape>', lambda e: on_cancel())
        
        qty_entry.focus()
        
        parent.wait_window(dialog)
        
        if result:
            current_item['quantity'] = result['quantity']
            current_item['discounted_price'] = result['price']
            current_item['total'] = current_item['quantity'] * current_item['discounted_price']
            self.update_items_display()
            self.update_total()    
        
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

class XTItemDialog:
    """Dialog for adding XT items"""
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add XT Item")
        self.dialog.geometry("400x250")
        self.dialog.configure(bg='#f0f0f0')
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
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Title
        title_label = tk.Label(
            self.dialog,
            text="Add XT Item",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0'
        )
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        input_frame.pack(padx=20, pady=10, fill='x')
        
        # Name
        tk.Label(input_frame, text="Item Name:", bg='#f0f0f0').grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Quantity
        tk.Label(input_frame, text="Quantity:", bg='#f0f0f0').grid(row=1, column=0, sticky='w', pady=5)
        self.quantity_entry = tk.Entry(input_frame, width=30)
        self.quantity_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        self.quantity_entry.insert(0, "1")
        
        # Price
        tk.Label(input_frame, text="Price:", bg='#f0f0f0').grid(row=2, column=0, sticky='w', pady=5)
        self.price_entry = tk.Entry(input_frame, width=30)
        self.price_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        add_btn = tk.Button(
            button_frame,
            text="Add Item",
            command=self.add_item,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 11, "bold"),
            width=10
        )
        add_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            bg='#f44336',
            fg='white',
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
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Receipt - Sale #{sale_id}")
        self.window.geometry("500x700")
        self.window.configure(bg='white')
        
        self.create_receipt()
    
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
        from config import RECEIPT_TAX_RATE, RECEIPT_COMPANY_NAME, RECEIPT_ADDRESS
        
        subtotal = sale_info[0]  # Total amount includes everything
        tax_amount = round(subtotal * RECEIPT_TAX_RATE, 2)  # Round to 2 decimal places
        total_with_tax = subtotal + tax_amount
        
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
        
        for item in sale_items:
            item_line1 = item['name']
            if len(item_line1) > 48:
                item_line1 = item_line1[:45] + "..."
            
            upc_text = f"UPC: {item['upc_code']}" if item['upc_code'] else "XT ITEM"
            
            qty_price = f"{item['quantity']} x ${item['discounted_price']:.2f}"
            total_price = f"${item['total']:.2f}"
            
            # Format the price line with right alignment
            price_line = f"{qty_price}".ljust(48 - len(total_price)) + total_price
            
            receipt_text += f"""
{item_line1}
{upc_text}
{price_line}
"""
        
        receipt_text += f"""
{'=' * 48}
{'Subtotal:'.ljust(40)}${subtotal:.2f}
{'Tax (8.875%):'.ljust(40)}${tax_amount:.2f}
{'=' * 48}
{'TOTAL:'.ljust(40)}${total_with_tax:.2f}
{'PAID:'.ljust(40)}${tax_amount+sale_info[1]:.2f}
{'BALANCE:'.ljust(40)}${subtotal - sale_info[1]:.2f}

Payment: {sale_info[2].replace('_', ' ').title()}

{'=' * 48}
Thank you for your business!
{'=' * 48}
        """
        
        # Store receipt text for printing
        self.receipt_text = receipt_text
        
        # Create text widget
        text_widget = tk.Text(
            self.window,
            font=("Courier New", 9),
            bg='white',
            fg='black',
            relief='flat',
            wrap='none'
        )
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Insert receipt text
        text_widget.insert('1.0', receipt_text)
        text_widget.config(state='disabled')
        
        # Button frame
        button_frame = tk.Frame(self.window, bg='white')
        button_frame.pack(pady=10)
        
        # Print button
        print_btn = tk.Button(
            button_frame,
            text="🖨️ Print Receipt",
            command=self.print_receipt,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        )
        print_btn.pack(side='left', padx=5)
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=self.window.destroy,
            bg='#607D8B',
            fg='white',
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