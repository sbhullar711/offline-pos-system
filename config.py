"""
Configuration file for POS System
"""

import os

# Database configuration
DATABASE_PATH = "database/pos_system.db"

# Application settings
APP_NAME = "POS System"
APP_VERSION = "1.0.0"
APP_WINDOW_SIZE = "1000x800"

# Receipt settings
RECEIPT_COMPANY_NAME = "Hardware store"
RECEIPT_ADDRESS = "QUOTE"
RECEIPT_TAX_RATE = 0.0  # 0 because it is being used for quote 

# Barcode scanner settings
BARCODE_SCANNER_ENABLED = True
BARCODE_PREFIX = ""  # Some scanners add prefix/suffix characters
BARCODE_SUFFIX = ""

# Printer settings
PRINTER_NAME = "default"  # Use "default" for default printer
RECEIPT_WIDTH = 48  # Receipt width in characters (80 for thermal printers)

# UI Colors
COLORS = {
    'primary': '#2196F3',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336',
    'info': '#00BCD4',
    'light': "#c8daec",
    'dark': "#a2bcd7"
}

# File paths
BACKUP_PATH = "backups/"
LOG_PATH = "logs/"
TEMP_PATH = "temp/"

# Ensure directories exist
for path in [BACKUP_PATH, LOG_PATH, TEMP_PATH, os.path.dirname(DATABASE_PATH)]:
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)