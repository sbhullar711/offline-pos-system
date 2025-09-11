import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import DatabaseManager

class ChangePriceWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.db = DatabaseManager()
        
        # Create window
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Change Item Price - POS System")
        self.window.geometry("600x400")
        self.window.configure(bg='#f0f0f0')
        
        # Create the interface
        self.create_widgets()
        
        # Center window
        self.center_window()
        
        # Focus on UPC entry
        self.upc_entry.focus()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"600x400+{x}+{y}")
    
    def create_widgets(self):
        """Create all widgets for the change price window"""
        
        # Title
        title_frame = tk.Frame(self.window, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="CHANGE ITEM PRICE",
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
        
        # UPC lookup section
        self.create_lookup_section()
        
        # Item details section
        self.create_item_details_section()
        
        # Price change section
        self.create_price_change_section()
    
    def create_lookup_section(self):
        """Create UPC lookup section"""
        lookup_frame = tk.LabelFrame(
            self.window,
            text="Find Item",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        lookup_frame.pack(fill='x', padx=10, pady=10)
        
        # UPC entry
        upc_frame = tk.Frame(lookup_frame, bg='#f0f0f0')
        upc_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            upc_frame,
            text="UPC/Barcode:",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.upc_entry = tk.Entry(
            upc_frame,
            font=("Arial", 14),
            width=25
        )
        self.upc_entry.pack(side='left', padx=(10, 5))
        self.upc_entry.bind('<Return>', self.lookup_item)
        
        lookup_btn = tk.Button(
            upc_frame,
            text="Lookup Item",
            command=self.lookup_item,
            bg='#2196F3',
            fg='white',
            font=("Arial", 12, "bold"),
            width=12
        )
        lookup_btn.pack(side='left', padx=5)
        
        # Instructions
        instructions = tk.Label(
            lookup_frame,
            text="Scan or enter UPC code to find item",
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        instructions.pack(pady=(0, 10))
    
    def create_item_details_section(self):
        """Create item details display section"""
        details_frame = tk.LabelFrame(
            self.window,
            text="Item Details",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        details_frame.pack(fill='x', padx=10, pady=10)
        
        # Item info display
        self.item_info_frame = tk.Frame(details_frame, bg='#f0f0f0')
        self.item_info_frame.pack(fill='x', padx=10, pady=10)
        
        # Initially hidden, will be shown when item is found
        self.item_name_label = tk.Label(
            self.item_info_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        
        self.item_upc_label = tk.Label(
            self.item_info_frame,
            text="",
            font=("Arial", 11),
            bg='#f0f0f0',
            fg='#666666'
        )
        
        self.current_price_label = tk.Label(
            self.item_info_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2196F3'
        )
        
        # No item found message
        self.no_item_label = tk.Label(
            self.item_info_frame,
            text="Enter UPC code to view item details",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#999999'
        )
        self.no_item_label.pack(pady=20)
        
        # Store current item
        self.current_item = None
    
    def create_price_change_section(self):
        """Create price change section"""
        self.price_frame = tk.LabelFrame(
            self.window,
            text="Change Price",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.price_frame.pack(fill='x', padx=10, pady=10)
        
        # Price entry
        price_input_frame = tk.Frame(self.price_frame, bg='#f0f0f0')
        price_input_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            price_input_frame,
            text="New Price: $",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.new_price_entry = tk.Entry(
            price_input_frame,
            font=("Arial", 14),
            width=15
        )
        self.new_price_entry.pack(side='left', padx=(5, 10))
        self.new_price_entry.bind('<Return>', self.update_price)
        
        self.update_btn = tk.Button(
            price_input_frame,
            text="Update Price",
            command=self.update_price,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 12, "bold"),
            width=12,
            state='disabled'
        )
        self.update_btn.pack(side='left', padx=5)
        
        # Initially hide the price frame
        self.price_frame.pack_forget()
    
    def lookup_item(self, event=None):
        """Look up item by UPC code"""
        upc = self.upc_entry.get().strip()
        if not upc:
            messagebox.showwarning("Warning", "Please enter a UPC code")
            return
        
        # Look up item in database
        item = self.db.get_item_by_upc(upc)
        
        if item:
            self.show_item_details(item)
        else:
            self.show_item_not_found(upc)
    
    def show_item_details(self, item):
        """Display item details"""
        self.current_item = item
        
        # Hide no item message
        self.no_item_label.pack_forget()
        
        # Show item details
        self.item_name_label.config(text=item['name'])
        self.item_name_label.pack(anchor='w', pady=(0, 5))
        
        self.item_upc_label.config(text=f"UPC: {item['upc_code']}")
        self.item_upc_label.pack(anchor='w', pady=(0, 5))
        
        self.current_price_label.config(text=f"Current Price: ${item['price']:.2f}")
        self.current_price_label.pack(anchor='w', pady=(0, 10))
        
        # Show price change section
        self.price_frame.pack(fill='x', padx=10, pady=10)
        
        # Pre-fill new price with current price
        self.new_price_entry.delete(0, tk.END)
        self.new_price_entry.insert(0, f"{item['price']:.2f}")
        self.new_price_entry.select_range(0, tk.END)
        
        # Enable update button
        self.update_btn.config(state='normal')
        
        # Focus on price entry
        self.new_price_entry.focus()
    
    def show_item_not_found(self, upc):
        """Show item not found message"""
        self.current_item = None
        
        # Hide item details
        self.item_name_label.pack_forget()
        self.item_upc_label.pack_forget()
        self.current_price_label.pack_forget()
        
        # Hide price change section
        self.price_frame.pack_forget()
        
        # Show not found message
        self.no_item_label.config(
            text=f"Item with UPC '{upc}' not found",
            fg='#f44336'
        )
        self.no_item_label.pack(pady=20)
        
        # Disable update button
        self.update_btn.config(state='disabled')
        
        # Show error message
        messagebox.showerror("Item Not Found", f"No item found with UPC code: {upc}")
    
    def update_price(self, event=None):
        """Update the item price"""
        if not self.current_item:
            messagebox.showwarning("Warning", "No item selected")
            return
        
        new_price_str = self.new_price_entry.get().strip()
        
        # Validate price
        try:
            new_price = float(new_price_str)
            if new_price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid positive price")
            self.new_price_entry.focus()
            return
        
        # Confirm price change
        old_price = self.current_item['price']
        if new_price == old_price:
            messagebox.showinfo("Info", "Price is the same as current price")
            return
        
        result = messagebox.askyesno(
            "Confirm Price Change",
            f"Change price for '{self.current_item['name']}'?\n\n"
            f"From: ${old_price:.2f}\n"
            f"To: ${new_price:.2f}"
        )
        
        if not result:
            return
        
        # Update price in database
        try:
            success = self.db.update_item_price(self.current_item['upc_code'], new_price)
            
            if success:
                # Update current item data
                self.current_item['price'] = new_price
                
                # Update display
                self.current_price_label.config(text=f"Current Price: ${new_price:.2f}")
                
                # Show success message
                messagebox.showinfo("Success", f"Price updated successfully!\n\n"
                                              f"Item: {self.current_item['name']}\n"
                                              f"New Price: ${new_price:.2f}")
                
                # Clear UPC entry for next item
                self.upc_entry.delete(0, tk.END)
                self.upc_entry.focus()
                
            else:
                messagebox.showerror("Error", "Failed to update price. Item may not exist.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error updating price: {str(e)}")
    
    def close_window(self):
        """Close the change price window"""
        self.window.destroy()

# Main function to test the change price window
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window
    change_price_window = ChangePriceWindow()
    root.mainloop()