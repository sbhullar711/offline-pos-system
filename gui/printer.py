import os
import platform
import subprocess
import tempfile
from config import RECEIPT_WIDTH, PRINTER_NAME

class ZStarPrinter:
    """Z-Star thermal printer utility"""
    
    def __init__(self):
        self.width = RECEIPT_WIDTH
        self.printer_name = PRINTER_NAME
    
    def format_line(self, text, align='left'):
        """Format a line for the receipt width"""
        if len(text) > self.width:
            # If text is too long, truncate it
            return text[:self.width]
        
        if align == 'center':
            return text.center(self.width)
        elif align == 'right':
            return text.rjust(self.width)
        else:
            return text.ljust(self.width)
    
    def format_two_column(self, left_text, right_text):
        """Format two columns on one line"""
        available_width = self.width - len(right_text)
        if len(left_text) > available_width - 1:
            left_text = left_text[:available_width - 4] + "..."
        
        spaces_needed = self.width - len(left_text) - len(right_text)
        return left_text + " " * spaces_needed + right_text
    
    def create_separator(self, char='-'):
        """Create a separator line"""
        return char * self.width
    
    def print_receipt(self, receipt_text):
        """Print receipt to Z-Star printer"""
        try:
            system = platform.system()
            
            if system == "Windows":
                self._print_windows(receipt_text)
            elif system == "Darwin":  # macOS
                self._print_macos(receipt_text)
            else:  # Linux
                self._print_linux(receipt_text)
                
            return True
        except Exception as e:
            print(f"Printing error: {e}")
            return False
    
    def _print_windows(self, receipt_text):
        """Print on Windows"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(receipt_text)
            temp_file_path = temp_file.name
        
        try:
            # Print using Windows print command
            if self.printer_name == "default":
                subprocess.run(['print', temp_file_path], check=True, shell=True)
            else:
                subprocess.run(['print', f'/D:{self.printer_name}', temp_file_path], check=True, shell=True)
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)
    
    def _print_macos(self, receipt_text):
        """Print on macOS"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(receipt_text)
            temp_file_path = temp_file.name
        
        try:
            # Print using lpr command
            if self.printer_name == "default":
                subprocess.run(['lpr', temp_file_path], check=True)
            else:
                subprocess.run(['lpr', '-P', self.printer_name, temp_file_path], check=True)
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)
    
    def _print_linux(self, receipt_text):
        """Print on Linux"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(receipt_text)
            temp_file_path = temp_file.name
        
        try:
            # Print using lp command
            if self.printer_name == "default":
                subprocess.run(['lp', temp_file_path], check=True)
            else:
                subprocess.run(['lp', '-d', self.printer_name, temp_file_path], check=True)
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)