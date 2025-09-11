#!/usr/bin/env python3
"""
POS System - Main Entry Point
Offline Point of Sale System for Windows/Mac

Author: Your Name
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from gui.main_window import MainWindow
    from database.models import DatabaseManager
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_modules = ['PIL', 'barcode', 'qrcode', 'reportlab']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        messagebox.showerror(
            "Missing Dependencies",
            f"The following modules are required but not installed:\n\n" +
            "\n".join(missing_modules) +
            f"\n\nPlease run: pip install -r requirements.txt"
        )
        return False
    return True

def main():
    """Main application entry point"""
    try:
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Test database connection
        db = DatabaseManager()
        print("Database initialized successfully")
        
        # Create and run main window
        app = MainWindow()
        print("Starting POS System...")
        app.run()
        
    except Exception as e:
        # Show error dialog if GUI is available
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror(
                "Application Error",
                f"An error occurred while starting the POS system:\n\n{str(e)}"
            )
        except:
            # Fallback to console output
            print(f"Error starting application: {e}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()