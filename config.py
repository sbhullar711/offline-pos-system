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
RECEIPT_COMPANY_NAME = "Bellerose Tiles And Building Materials"
RECEIPT_ADDRESS = "248-27 Jericho Tpke\nJamaica, NY 11803\nPhone: (516) 344-1708"
RECEIPT_TAX_RATE = 0.08875  # 8% tax rate (set to 0 for no tax)

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
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# File paths
BACKUP_PATH = "backups/"
LOG_PATH = "logs/"
TEMP_PATH = "temp/"

# Ensure directories exist
for path in [BACKUP_PATH, LOG_PATH, TEMP_PATH, os.path.dirname(DATABASE_PATH)]:
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)