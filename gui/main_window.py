import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import DatabaseManager

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("POS System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        self.db = DatabaseManager()
        
        # Create main interface
        self.create_widgets()
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
    
    def create_widgets(self):
        """Create the main interface widgets"""
        # Main title
        title_label = tk.Label(
            self.root,
            text="POS System",
            font=("Arial", 24, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=30)
        
        # Create button frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        # Configure grid weights for centering
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # Button style configuration
        button_style = {
            'font': ('Arial', 16, 'bold'),
            'width': 15,
            'height': 3,
            'relief': 'raised',
            'bd': 3
        }
        
        # Sale button (top-left)
        sale_btn = tk.Button(
            button_frame,
            text="SALE",
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            command=self.open_sale_window,
            **button_style
        )
        sale_btn.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        
        # Add Item button (top-right)
        add_item_btn = tk.Button(
            button_frame,
            text="ADD ITEM",
            bg='#2196F3',
            fg='white',
            activebackground='#1976D2',
            command=self.open_add_item_window,
            **button_style
        )
        add_item_btn.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')
        
        # Change Item Price button (bottom-left)
        change_price_btn = tk.Button(
            button_frame,
            text="CHANGE ITEM\nPRICE",
            bg='#FF9800',
            fg='white',
            activebackground='#F57C00',
            command=self.open_change_price_window,
            **button_style
        )
        change_price_btn.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')
        
        # Customer button (bottom-right)
        customer_btn = tk.Button(
            button_frame,
            text="CUSTOMER",
            bg='#9C27B0',
            fg='white',
            activebackground='#7B1FA2',
            command=self.open_customer_window,
            **button_style
        )
        customer_btn.grid(row=1, column=1, padx=20, pady=20, sticky='nsew')
        
        # Configure grid weights for buttons
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bg='#e0e0e0',
            relief='sunken',
            anchor='w',
            font=('Arial', 10)
        )
        self.status_bar.pack(side='bottom', fill='x')
        
        # Menu bar
        self.create_menu()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def show_about(self):
        """Show about dialog"""
        from tkinter import messagebox
        messagebox.showinfo(
            "About",
            "POS System v1.0\nOffline Point of Sale System\n\nBuilt with Python & Tkinter"
        )
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    # Button click handlers (placeholders for now)
    def open_sale_window(self):
        """Open sale window"""
        self.update_status("Opening Sale window...")
        try:
            from gui.sale_window import SaleWindow
            sale_window = SaleWindow(self.root)
            self.update_status("Sale window opened")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error opening sale window: {str(e)}")
    
    def open_add_item_window(self):
        """Open add item window"""
        self.update_status("Opening Add Item window...")
        try:
            from gui.add_item_window import AddItemWindow
            add_item_window = AddItemWindow(self.root)
            self.update_status("Add Item window opened")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error opening add item window: {str(e)}")
    
    def open_change_price_window(self):
        """Open change price window"""
        self.update_status("Opening Change Price window...")
        try:
            from gui.change_price_window import ChangePriceWindow
            change_price_window = ChangePriceWindow(self.root)
            self.update_status("Change Price window opened")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error opening change price window: {str(e)}")
    
    def open_customer_window(self):
        """Open customer window"""
        self.update_status("Opening Customer window...")
        try:
            from gui.customer_window import CustomerWindow
            customer_window = CustomerWindow(self.root)
            self.update_status("Customer window opened")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error opening customer window: {str(e)}")
                
    def run(self):
        """Start the application"""
        self.update_status("POS System Ready")
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()