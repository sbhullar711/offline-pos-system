import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import sys
import os
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.models import DatabaseManager

class ImportItemsWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.db = DatabaseManager()
        self.csv_data = []
        
        # Detect platform
        self.is_mac = platform.system() == 'Darwin'
        self.is_windows = platform.system() == 'Windows'
        
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Import Items from CSV")
        self.window.geometry("700x500")
        self.window.configure(bg='#ffffff')
        
        # Configure ttk styles for cross-platform consistency
        self.setup_styles()
        
        self.create_widgets()
        self.center_window()
    
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
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"700x500+{x}+{y}")
    
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
        # Title and close button
        title_frame = tk.Frame(self.window, bg='white', relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            title_frame, 
            text="IMPORT ITEMS FROM CSV", 
            font=("Arial", 16, "bold"), 
            bg='white',
            fg='#333333'
        ).pack(side='left', padx=10, pady=5)
        
        close_btn = self.create_button(
            title_frame, 
            text="✕ Close", 
            command=self.window.destroy, 
            bg_color='#dc3545', 
            fg_color='white',
            font=("Arial", 10, "bold")
        )
        close_btn.pack(side='right', padx=10, pady=5)
        
        # File selection
        file_container = tk.Frame(self.window, bg='white')
        file_container.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            file_container,
            text="Select CSV File",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', padx=5, pady=(5, 0))
        
        file_frame = tk.Frame(file_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        file_frame.pack(fill='x', padx=5, pady=5)
        
        file_inner = tk.Frame(file_frame, bg='white')
        file_inner.pack(fill='x', padx=10, pady=10)
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(
            file_inner, 
            textvariable=self.file_path_var, 
            state='readonly', 
            width=60,
            bg='white',
            fg='black'
        )
        file_entry.pack(side='left', padx=(0, 10))
        
        browse_btn = self.create_button(
            file_inner, 
            text="Browse", 
            command=self.browse_file, 
            bg_color='#007bff', 
            fg_color='white',
            font=("Arial", 10, "bold")
        )
        browse_btn.pack(side='right')
        
        # Import options
        options_container = tk.Frame(self.window, bg='white')
        options_container.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            options_container,
            text="Import Options",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', padx=5, pady=(5, 0))
        
        options_frame = tk.Frame(options_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        options_frame.pack(fill='x', padx=5, pady=5)
        
        options_inner = tk.Frame(options_frame, bg='white')
        options_inner.pack(fill='x', padx=10, pady=10)
        
        self.import_mode = tk.StringVar(value="insert")
        
        radio1 = tk.Radiobutton(
            options_inner, 
            text="Insert New Items Only (Skip existing)", 
            variable=self.import_mode, 
            value="insert", 
            bg='white',
            fg='#333333',
            font=("Arial", 10),
            activebackground='white',
            selectcolor='white'
        )
        radio1.pack(anchor='w', padx=10, pady=2)
        
        radio2 = tk.Radiobutton(
            options_inner, 
            text="Update All Items (Update existing, add new)", 
            variable=self.import_mode, 
            value="update", 
            bg='white',
            fg='#333333',
            font=("Arial", 10),
            activebackground='white',
            selectcolor='white'
        )
        radio2.pack(anchor='w', padx=10, pady=2)
        
        # Preview
        preview_container = tk.Frame(self.window, bg='white')
        preview_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        tk.Label(
            preview_container,
            text="Preview (First 20 items)",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', padx=5, pady=(5, 0))
        
        preview_frame = tk.Frame(preview_container, bg='white', relief=tk.GROOVE, borderwidth=1)
        preview_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Treeview for preview
        columns = ('UPC', 'Brand', 'Product', 'Description', 'Cost', 'Price')
        self.preview_tree = ttk.Treeview(preview_frame, columns=columns, show='headings', height=10,
                                        style="Treeview")
        
        for col in columns:
            self.preview_tree.heading(col, text=col, anchor='w')
            if col in ['Cost', 'Price']:
                self.preview_tree.column(col, width=80, anchor='e')
            elif col == 'Description':
                self.preview_tree.column(col, width=150, anchor='w')
            else:
                self.preview_tree.column(col, width=100, anchor='w')
        
        scrollbar = ttk.Scrollbar(preview_frame, orient='vertical', command=self.preview_tree.yview,
                                 style="Vertical.TScrollbar")
        self.preview_tree.configure(yscrollcommand=scrollbar.set)
        
        self.preview_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)
        
        # Status label
        self.status_label = tk.Label(
            self.window,
            text="No file selected",
            font=("Arial", 10),
            bg='white',
            fg='#666666'
        )
        self.status_label.pack(pady=5)
        
        # Import button
        self.import_btn = self.create_button(
            self.window, 
            text="IMPORT ITEMS", 
            command=self.import_items,
            bg_color='#28a745', 
            fg_color='white', 
            font=("Arial", 12, "bold"), 
            height=2
        )
        self.import_btn.pack(pady=10)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.load_csv_preview(file_path)
    
    def load_csv_preview(self, file_path):
        try:
            self.csv_data = []
            
            # Clear preview
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                rows = list(csv_reader)
                
                # Skip first row (blank), use second row as headers, start from third row
                if len(rows) < 3:
                    messagebox.showerror("Error", "CSV file must have at least 3 rows (blank row, headers, and data)")
                    self.status_label.config(text="Invalid CSV format", fg='#dc3545')
                    return
                
                headers = rows[1]  # Row 2 is headers
                data_rows = rows[2:]  # Row 3 onwards is data
                
                for row in data_rows:
                    if len(row) >= 6:  # Ensure we have all required columns
                        # Normalize UPC - pad with 0 if 11 digits
                        upc = row[0].strip()
                        if len(upc) == 11:
                            upc = '0' + upc
                        
                        try:
                            item_data = {
                                'upc': upc,
                                'brand': row[1].strip(),
                                'product': row[2].strip(),
                                'description': row[3].strip(),
                                'cost': float(row[4].strip()),
                                'price': float(row[5].strip())
                            }
                            self.csv_data.append(item_data)
                            
                            # Add to preview (first 20 items)
                            if len(self.preview_tree.get_children()) < 20:
                                desc_display = item_data['description']
                                if len(desc_display) > 30:
                                    desc_display = desc_display[:30] + "..."
                                
                                self.preview_tree.insert('', 'end', values=(
                                    item_data['upc'],
                                    item_data['brand'],
                                    item_data['product'],
                                    desc_display,
                                    f"${item_data['cost']:.2f}",
                                    f"${item_data['price']:.2f}"
                                ))
                        except ValueError as e:
                            print(f"Skipping invalid row: {row} - Error: {e}")
                            continue
                
                # Update status
                self.status_label.config(
                    text=f"Loaded {len(self.csv_data)} valid items", 
                    fg='#28a745'
                )
                
                if len(self.csv_data) == 0:
                    messagebox.showwarning("Warning", "No valid items found in CSV file")
                else:
                    messagebox.showinfo("Success", f"Loaded {len(self.csv_data)} items for import")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error reading CSV file: {str(e)}")
            self.status_label.config(text="Error loading file", fg='#dc3545')
    
    def import_items(self):
        if not self.csv_data:
            messagebox.showwarning("Warning", "Please select and load a CSV file first")
            return
        
        mode = self.import_mode.get()
        
        # Confirm import
        confirm = messagebox.askyesno(
            "Confirm Import",
            f"Import {len(self.csv_data)} items?\nMode: {'Insert new only' if mode == 'insert' else 'Update all'}"
        )
        
        if not confirm:
            return
        
        try:
            success_count = 0
            error_count = 0
            duplicate_count = 0
            
            # Progress tracking
            total_items = len(self.csv_data)
            
            for idx, item_data in enumerate(self.csv_data):
                try:
                    if mode == "insert":
                        # Check if item already exists
                        existing_item = self.db.get_item_by_upc(item_data['upc'])
                        if existing_item:
                            duplicate_count += 1
                            continue  # Skip duplicates in insert mode
                        
                        self.db.add_item_full(
                            item_data['upc'], 
                            item_data['brand'], 
                            item_data['product'],
                            item_data['description'], 
                            item_data['cost'], 
                            item_data['price']
                        )
                        success_count += 1
                    else:  # update mode
                        success = self.db.update_item_full(
                            item_data['upc'], 
                            item_data['brand'], 
                            item_data['product'],
                            item_data['description'], 
                            item_data['cost'], 
                            item_data['price']
                        )
                        if success:
                            success_count += 1
                        else:
                            # Item doesn't exist, insert it
                            self.db.add_item_full(
                                item_data['upc'], 
                                item_data['brand'], 
                                item_data['product'],
                                item_data['description'], 
                                item_data['cost'], 
                                item_data['price']
                            )
                            success_count += 1
                            
                except Exception as e:
                    error_count += 1
                    print(f"Error with item {item_data['upc']}: {e}")
                
                # Update status every 100 items
                if (idx + 1) % 100 == 0:
                    self.status_label.config(
                        text=f"Processing... {idx + 1}/{total_items} items",
                        fg='#007bff'
                    )
                    self.window.update()
            
            # Final result message
            result_msg = f"Import Complete!\n\n"
            result_msg += f"✅ Successfully imported: {success_count}\n"
            if error_count > 0:
                result_msg += f"❌ Errors: {error_count}\n"
            if duplicate_count > 0:
                result_msg += f"⏭️ Duplicates skipped: {duplicate_count}\n"
            
            messagebox.showinfo("Import Complete", result_msg)
            
            # Update final status
            self.status_label.config(
                text=f"Import complete: {success_count} items imported",
                fg='#28a745'
            )
            
            # Clear data after successful import
            self.csv_data = []
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
            self.file_path_var.set("")
            
        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {str(e)}")
            self.status_label.config(text="Import failed", fg='#dc3545')

# Main function to test
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    import_window = ImportItemsWindow()
    root.mainloop()