import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import platform

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import DatabaseManager

class AddItemWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.db = DatabaseManager()
        
        # Detect platform
        self.is_mac = platform.system() == 'Darwin'
        self.is_windows = platform.system() == 'Windows'
        
        # Create window
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Add Items - CSV Import Only")
        self.window.geometry("700x550")
        self.window.configure(bg='#ffffff')
        
        # Create the interface
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.window.winfo_screenheight() // 2) - (550 // 2)
        self.window.geometry(f"700x550+{x}+{y}")
    
    def create_button(self, parent, text, command, bg_color="#4CAF50", fg_color="white", **kwargs):
        """Create a cross-platform compatible button"""
        if self.is_mac:
            # On Mac, use a Frame with Label to simulate button with background color
            btn_frame = tk.Frame(parent, bg=bg_color, highlightbackground=bg_color, highlightthickness=1)
            btn = tk.Label(btn_frame, text=text, bg=bg_color, fg=fg_color, 
                          cursor="hand2", padx=15, pady=10, **kwargs)
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
        """Create all widgets for the add item window"""
        
        # Title Frame
        title_frame = tk.Frame(self.window, bg='white', relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="ADD ITEMS VIA CSV IMPORT",
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
        
        # CSV Format Instructions
        self.create_format_instructions()
        
        # Import button
        self.create_import_section()
    
    def create_format_instructions(self):
        """Create CSV format instructions"""
        # Container with white background
        instructions_container = tk.Frame(self.window, bg='white')
        instructions_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Title
        title_label = tk.Label(
            instructions_container,
            text="CSV Format Requirements",
            font=("Arial", 14, "bold"),
            bg='white',
            fg='#333333'
        )
        title_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Frame with border
        instructions_frame = tk.Frame(instructions_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        instructions_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Format requirements text
        format_text = """CSV FILE FORMAT REQUIREMENTS:

FILE STRUCTURE:
   • Row 1: Leave BLANK (skip row)
   • Row 2: Headers (UPC, Brand, Product, Description, Cost, Price)
   • Row 3+: Your item data

COLUMN ORDER (must be exact):
   1. UPC/Barcode    - Product barcode (11-12 digits)
   2. Brand          - Product brand name
   3. Product        - Product name
   4. Description    - Product description
   5. Cost           - Your cost price (numbers only)
   6. Price          - Selling price (numbers only)

DATA REQUIREMENTS:
   • UPC: 11-12 digit numbers only (e.g., 51141347042 or 051141347042)
   • Brand: Text (e.g., "Coca-Cola", "Samsung")
   • Product: Text (e.g., "12oz Can", "Galaxy Phone")
   • Description: Text (e.g., "Refreshing cola drink")
   • Cost: Numbers only (e.g., 0.75, 45.50) - NO $ symbol
   • Price: Numbers only (e.g., 1.25, 89.99) - NO $ symbol

IMPORT LIMITS:
   • Maximum: 10,000 items per import
   • File size: Under 50MB recommended
   • Format: CSV files only (.csv extension)

EXAMPLE FORMAT:
   Row 1: [BLANK]
   Row 2: UPC,Brand,Product,Description,Cost,Price
   Row 3: 051141347042,Coca-Cola,12oz Can,Classic Coke,0.75,1.25
   Row 4: 123456789012,Samsung,Galaxy Phone,Smartphone,400.00,599.99"""
        
        # Create scrollable text widget for instructions
        text_frame = tk.Frame(instructions_frame, bg='white')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Text widget with scrollbar
        text_widget = tk.Text(
            text_frame,
            font=("Courier New", 10),
            bg='#f8f9fa',
            fg='#333333',
            relief='flat',
            wrap='word',
            height=20,
            borderwidth=1,
            highlightbackground='#e0e0e0',
            highlightcolor='#007bff',
            highlightthickness=1
        )
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Pack text widget and scrollbar
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Insert instructions
        text_widget.insert('1.0', format_text)
        text_widget.config(state='disabled')
        
        # Style the text with tags for better readability
        text_widget.tag_add("header", "1.0", "1.end")
        text_widget.tag_config("header", font=("Courier New", 11, "bold"), foreground='#007bff')
        
        # Highlight section headers
        for line_num in range(1, 30):
            line_start = f"{line_num}.0"
            line_end = f"{line_num}.end"
            line_text = text_widget.get(line_start, line_end)
            if line_text.strip().endswith(':') and not line_text.startswith('   '):
                text_widget.tag_add("section", line_start, line_end)
                text_widget.tag_config("section", font=("Courier New", 10, "bold"), foreground='#28a745')
    
    def create_import_section(self):
        """Create import button section"""
        # Container frame with white background
        import_container = tk.Frame(self.window, bg='white', relief=tk.RAISED, borderwidth=1)
        import_container.pack(fill='x', padx=10, pady=10)
        
        import_frame = tk.Frame(import_container, bg='white')
        import_frame.pack(padx=20, pady=20)
        
        # Import button - larger and more prominent
        import_btn = self.create_button(
            import_frame,
            text="📂 IMPORT CSV FILE",
            command=self.open_import_window,
            bg_color='#28a745',
            fg_color='white',
            font=("Arial", 16, "bold"),
            width=20,
            height=3
        )
        import_btn.pack()
        
        # Additional info
        info_label = tk.Label(
            import_frame,
            text="Click above to select and import your CSV file",
            font=("Arial", 11),
            bg='white',
            fg='#666666'
        )
        info_label.pack(pady=(10, 0))
        
        # Warning/tips section
        tips_frame = tk.Frame(import_container, bg='#fff3cd', relief=tk.SOLID, borderwidth=1)
        tips_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tips_label = tk.Label(
            tips_frame,
            text="💡 TIP: Save your Excel file as CSV (Comma delimited) before importing",
            font=("Arial", 10),
            bg='#fff3cd',
            fg='#856404',
            pady=8
        )
        tips_label.pack()
    
    def open_import_window(self):
        """Open the CSV import window"""
        try:
            from gui.import_items_window import ImportItemsWindow
            ImportItemsWindow(self.window)
        except ImportError:
            messagebox.showerror("Error", "Import module not found. Please check your installation.")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening import window: {str(e)}")
    
    def close_window(self):
        """Close the add item window"""
        self.window.destroy()

# Main function to test the add item window
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window
    add_item_window = AddItemWindow()
    root.mainloop()