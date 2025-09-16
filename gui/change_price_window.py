import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os
import platform

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import DatabaseManager

class ChangePriceWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.db = DatabaseManager()
        
        # Detect platform
        self.is_mac = platform.system() == 'Darwin'
        self.is_windows = platform.system() == 'Windows'
        
        # Create window
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Change Item Price - POS System")
        self.window.geometry("600x400")
        self.window.configure(bg='#ffffff')
        
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
    
    def create_button(self, parent, text, command, bg_color="#4CAF50", fg_color="white", **kwargs):
        """Create a cross-platform compatible button"""
        if self.is_mac:
            # On Mac, use a Frame with Label to simulate button with background color
            btn_frame = tk.Frame(parent, bg=bg_color, highlightbackground=bg_color, highlightthickness=1)
            btn = tk.Label(btn_frame, text=text, bg=bg_color, fg=fg_color, 
                          cursor="hand2", padx=10, pady=5, **kwargs)
            btn.pack()
            
            # Store reference for state changes
            btn_frame.label = btn
            btn_frame.original_bg = bg_color
            btn_frame.original_fg = fg_color
            
            # Bind click events
            def handle_click(e):
                if not hasattr(btn_frame, 'disabled') or not btn_frame.disabled:
                    command()
            
            btn.bind("<Button-1>", handle_click)
            btn_frame.bind("<Button-1>", handle_click)
            
            # Hover effects
            def on_enter(e):
                if not hasattr(btn_frame, 'disabled') or not btn_frame.disabled:
                    btn.configure(bg=self.darken_color(bg_color))
                    btn_frame.configure(bg=self.darken_color(bg_color))
            
            def on_leave(e):
                if not hasattr(btn_frame, 'disabled') or not btn_frame.disabled:
                    btn.configure(bg=bg_color)
                    btn_frame.configure(bg=bg_color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
            # Add method to handle state changes
            def config_state(state='normal'):
                if state == 'disabled':
                    btn_frame.disabled = True
                    btn.configure(bg='#e0e0e0', fg='#999999')
                    btn_frame.configure(bg='#e0e0e0')
                else:
                    btn_frame.disabled = False
                    btn.configure(bg=btn_frame.original_bg, fg=btn_frame.original_fg)
                    btn_frame.configure(bg=btn_frame.original_bg)
            
            btn_frame.config = lambda **kw: config_state(kw.get('state', 'normal'))
            
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
        """Create all widgets for the change price window"""
        
        # Title Frame
        title_frame = tk.Frame(self.window, bg='white', relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="CHANGE ITEM PRICE",
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
        
        # UPC lookup section
        self.create_lookup_section()
        
        # Item details section
        self.create_item_details_section()
        
        # Price change section
        self.create_price_change_section()
    
    def create_lookup_section(self):
        """Create UPC lookup section"""
        # Container with white background
        lookup_container = tk.Frame(self.window, bg='white')
        lookup_container.pack(fill='x', padx=10, pady=5)
        
        # Title
        title_label = tk.Label(
            lookup_container,
            text="Find Item",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Frame with border
        lookup_frame = tk.Frame(lookup_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        lookup_frame.pack(fill='x', padx=5, pady=5)
        
        # UPC entry
        upc_frame = tk.Frame(lookup_frame, bg='white')
        upc_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            upc_frame,
            text="UPC/Barcode:",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        ).pack(side='left')
        
        self.upc_entry = tk.Entry(
            upc_frame,
            font=("Arial", 14),
            width=25,
            bg="white",
            fg="black",
            insertbackground="black"
        )
        self.upc_entry.pack(side='left', padx=(10, 5))
        self.upc_entry.bind('<Return>', self.lookup_item)
        
        lookup_btn = self.create_button(
            upc_frame,
            text="Lookup Item",
            command=self.lookup_item,
            bg_color='#007bff',
            fg_color='white',
            font=("Arial", 12, "bold"),
            width=12
        )
        lookup_btn.pack(side='left', padx=5)
        
        # Instructions
        instructions = tk.Label(
            lookup_frame,
            text="Scan or enter UPC code to find item",
            font=("Arial", 10),
            bg='white',
            fg='#666666'
        )
        instructions.pack(pady=(0, 10))
    
    def create_item_details_section(self):
        """Create item details display section"""
        # Container with white background
        details_container = tk.Frame(self.window, bg='white')
        details_container.pack(fill='x', padx=10, pady=5)
        
        # Title
        title_label = tk.Label(
            details_container,
            text="Item Details",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Frame with border
        details_frame = tk.Frame(details_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        details_frame.pack(fill='x', padx=5, pady=5)
        
        # Item info display
        self.item_info_frame = tk.Frame(details_frame, bg='white')
        self.item_info_frame.pack(fill='x', padx=10, pady=10)
        
        # Initially hidden, will be shown when item is found
        self.item_name_label = tk.Label(
            self.item_info_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg='white',
            fg='#333333'
        )
        
        self.item_upc_label = tk.Label(
            self.item_info_frame,
            text="",
            font=("Arial", 11),
            bg='white',
            fg='#666666'
        )
        
        self.current_price_label = tk.Label(
            self.item_info_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg='white',
            fg='#007bff'
        )
        
        # No item found message
        self.no_item_label = tk.Label(
            self.item_info_frame,
            text="Enter UPC code to view item details",
            font=("Arial", 12),
            bg='white',
            fg='#999999'
        )
        self.no_item_label.pack(pady=20)
        
        # Store current item
        self.current_item = None
    
    def create_price_change_section(self):
        """Create price change section"""
        # Container (initially hidden)
        self.price_container = tk.Frame(self.window, bg='white')
        
        # Title
        title_label = tk.Label(
            self.price_container,
            text="Change Price",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(anchor='w', padx=15, pady=(5, 0))
        
        # Frame with border
        self.price_frame = tk.Frame(self.price_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        self.price_frame.pack(fill='x', padx=15, pady=5)
        
        # Price entry
        price_input_frame = tk.Frame(self.price_frame, bg='white')
        price_input_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            price_input_frame,
            text="New Price: $",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        ).pack(side='left')
        
        self.new_price_entry = tk.Entry(
            price_input_frame,
            font=("Arial", 14),
            width=15,
            bg="white",
            fg="black",
            insertbackground="black"
        )
        self.new_price_entry.pack(side='left', padx=(5, 10))
        self.new_price_entry.bind('<Return>', self.update_price)
        
        self.update_btn = self.create_button(
            price_input_frame,
            text="Update Price",
            command=self.update_price,
            bg_color='#28a745',
            fg_color='white',
            font=("Arial", 12, "bold"),
            width=12
        )
        self.update_btn.pack(side='left', padx=5)
        self.update_btn.config(state='disabled')
        
        # Initially hide the price container
        # Don't pack it yet
    
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
        self.price_container.pack(fill='x', padx=10, pady=10)
        
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
        self.price_container.pack_forget()
        
        # Show not found message
        self.no_item_label.config(
            text=f"Item with UPC '{upc}' not found",
            fg='#dc3545'
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
                
                # Clear and hide price change section
                self.item_name_label.pack_forget()
                self.item_upc_label.pack_forget()
                self.current_price_label.pack_forget()
                self.price_container.pack_forget()
                
                # Reset no item label
                self.no_item_label.config(
                    text="Enter UPC code to view item details",
                    fg='#999999'
                )
                self.no_item_label.pack(pady=20)
                
                # Clear current item
                self.current_item = None
                
                # Disable update button
                self.update_btn.config(state='disabled')
                
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