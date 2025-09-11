import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import DatabaseManager

class AddItemWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.db = DatabaseManager()
        
        # Create window
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Add New Item - POS System")
        self.window.geometry("500x400")
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
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"500x400+{x}+{y}")
    
    def create_widgets(self):
        """Create all widgets for the add item window"""
        
        # Title
        title_frame = tk.Frame(self.window, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="ADD NEW ITEM",
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
        
        # Main form
        self.create_form()
        
        # Buttons
        self.create_buttons()
    
    def create_form(self):
        """Create the item input form"""
        form_frame = tk.LabelFrame(
            self.window,
            text="Item Information",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Configure grid
        form_frame.grid_columnconfigure(1, weight=1)
        
        # UPC Code
        tk.Label(
            form_frame,
            text="UPC/Barcode:",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0'
        ).grid(row=0, column=0, sticky='w', padx=10, pady=15)
        
        self.upc_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=25
        )
        self.upc_entry.grid(row=0, column=1, sticky='ew', padx=(10, 20), pady=15)
        self.upc_entry.bind('<KeyRelease>', self.check_upc_exists)
        
        # UPC status label
        self.upc_status_label = tk.Label(
            form_frame,
            text="",
            font=("Arial", 9),
            bg='#f0f0f0'
        )
        self.upc_status_label.grid(row=1, column=1, sticky='w', padx=10, pady=(0, 10))
        
        # Item Name
        tk.Label(
            form_frame,
            text="Item Name:",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0'
        ).grid(row=2, column=0, sticky='w', padx=10, pady=15)
        
        self.name_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=25
        )
        self.name_entry.grid(row=2, column=1, sticky='ew', padx=(10, 20), pady=15)
        
        # Price
        tk.Label(
            form_frame,
            text="Price ($):",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0'
        ).grid(row=3, column=0, sticky='w', padx=10, pady=15)
        
        price_frame = tk.Frame(form_frame, bg='#f0f0f0')
        price_frame.grid(row=3, column=1, sticky='ew', padx=(10, 20), pady=15)
        
        tk.Label(
            price_frame,
            text="$",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.price_entry = tk.Entry(
            price_frame,
            font=("Arial", 12),
            width=20
        )
        self.price_entry.pack(side='left', padx=(5, 0))
        
        # Instructions
        instructions_frame = tk.Frame(form_frame, bg='#f0f0f0')
        instructions_frame.grid(row=4, column=0, columnspan=2, sticky='ew', padx=10, pady=20)
        
        instructions_text = """Instructions:
- UPC/Barcode: Enter the unique product code (numbers only)
- Item Name: Enter a descriptive name for the product
- Price: Enter the selling price (numbers only, no $ sign needed)"""
        
        tk.Label(
            instructions_frame,
            text=instructions_text,
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#666666',
            justify='left'
        ).pack(anchor='w')
    
    def create_buttons(self):
        """Create action buttons"""
        button_frame = tk.Frame(self.window, bg='#f0f0f0')
        button_frame.pack(fill='x', padx=20, pady=10)
        
        # Add Item button
        self.add_btn = tk.Button(
            button_frame,
            text="Add Item",
            command=self.add_item,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 14, "bold"),
            width=12,
            height=2
        )
        self.add_btn.pack(side='left', padx=(0, 10))
        
        # Clear Form button
        clear_btn = tk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            bg='#FF9800',
            fg='white',
            font=("Arial", 14, "bold"),
            width=12,
            height=2
        )
        clear_btn.pack(side='left', padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.close_window,
            bg='#607D8B',
            fg='white',
            font=("Arial", 14, "bold"),
            width=12,
            height=2
        )
        cancel_btn.pack(side='right')
        
        # Bind Enter key to add item
        self.window.bind('<Return>', lambda e: self.add_item())
    
    def check_upc_exists(self, event=None):
        """Check if UPC already exists as user types"""
        upc = self.upc_entry.get().strip()
        
        if len(upc) < 3:  # Don't check very short inputs
            self.upc_status_label.config(text="", fg='black')
            return
        
        # Check if item exists
        existing_item = self.db.get_item_by_upc(upc)
        
        if existing_item:
            self.upc_status_label.config(
                text=f"⚠️ UPC already exists: {existing_item['name']}",
                fg='#f44336'
            )
        else:
            self.upc_status_label.config(
                text="✓ UPC available",
                fg='#4CAF50'
            )
    
    def validate_input(self):
        """Validate all input fields"""
        upc = self.upc_entry.get().strip()
        name = self.name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        
        # Validate UPC
        if not upc:
            messagebox.showwarning("Validation Error", "Please enter a UPC/Barcode")
            self.upc_entry.focus()
            return False
        
        if not upc.isdigit():
            messagebox.showwarning("Validation Error", "UPC/Barcode should contain only numbers")
            self.upc_entry.focus()
            return False
        
        if len(upc) < 8:
            messagebox.showwarning("Validation Error", "UPC/Barcode should be at least 8 digits")
            self.upc_entry.focus()
            return False
        
        # Check if UPC already exists
        existing_item = self.db.get_item_by_upc(upc)
        if existing_item:
            messagebox.showwarning(
                "Duplicate UPC", 
                f"UPC '{upc}' already exists for item:\n{existing_item['name']}\n\nPlease use a different UPC code."
            )
            self.upc_entry.focus()
            return False
        
        # Validate name
        if not name:
            messagebox.showwarning("Validation Error", "Please enter an item name")
            self.name_entry.focus()
            return False
        
        if len(name) < 2:
            messagebox.showwarning("Validation Error", "Item name should be at least 2 characters")
            self.name_entry.focus()
            return False
        
        # Validate price
        if not price_str:
            messagebox.showwarning("Validation Error", "Please enter a price")
            self.price_entry.focus()
            return False
        
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showwarning("Validation Error", "Please enter a valid positive price")
            self.price_entry.focus()
            return False
        
        return True
    
    def add_item(self):
        """Add the new item to database"""
        if not self.validate_input():
            return
        
        upc = self.upc_entry.get().strip()
        name = self.name_entry.get().strip()
        price = float(self.price_entry.get().strip())
        
        # Confirm addition
        result = messagebox.askyesno(
            "Confirm Add Item",
            f"Add this item to inventory?\n\n"
            f"UPC: {upc}\n"
            f"Name: {name}\n"
            f"Price: ${price:.2f}"
        )
        
        if not result:
            return
        
        try:
            # Add item to database
            item_id = self.db.add_item(upc, name, price)
            
            # Show success message
            messagebox.showinfo(
                "Item Added Successfully",
                f"Item added to inventory!\n\n"
                f"Item ID: {item_id}\n"
                f"UPC: {upc}\n"
                f"Name: {name}\n"
                f"Price: ${price:.2f}"
            )
            
            # Clear form for next item
            self.clear_form()
            
            # Focus back to UPC entry
            self.upc_entry.focus()
            
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror(
                    "Duplicate UPC",
                    f"UPC '{upc}' already exists in the database.\nPlease use a different UPC code."
                )
            else:
                messagebox.showerror("Error", f"Error adding item: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.upc_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.upc_status_label.config(text="")
        self.upc_entry.focus()
    
    def close_window(self):
        """Close the add item window"""
        self.window.destroy()

# Main function to test the add item window
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window
    add_item_window = AddItemWindow()
    root.mainloop()