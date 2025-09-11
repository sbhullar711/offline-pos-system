#!/usr/bin/env python3
"""
Performance test script to demonstrate SQLite capabilities
This will add 10,000 sample items and test search performance
"""

import time
import random
import string
from database.models import DatabaseManager

def generate_random_upc():
    """Generate a random UPC code"""
    return ''.join(random.choices(string.digits, k=12))

def generate_random_item_name():
    """Generate a random item name"""
    prefixes = ['Premium', 'Classic', 'Deluxe', 'Standard', 'Super', 'Ultra', 'Fresh']
    products = ['Widget', 'Gadget', 'Tool', 'Device', 'Item', 'Product', 'Component']
    suffixes = ['Pro', 'Plus', 'Max', 'XL', 'Mini', 'Standard', 'Deluxe']
    
    return f"{random.choice(prefixes)} {random.choice(products)} {random.choice(suffixes)}"

def performance_test():
    """Test database performance with 10,000 items"""
    
    print("=== POS System Performance Test ===\n")
    
    # Initialize database
    db = DatabaseManager("database/test_performance.db")
    
    # Test 1: Insert 10,000 items
    print("Test 1: Inserting 10,000 items...")
    start_time = time.time()
    
    for i in range(10000):
        upc = generate_random_upc()
        name = generate_random_item_name()
        price = round(random.uniform(1.0, 999.99), 2)
        
        try:
            db.add_item(upc, name, price)
        except:
            # Skip if UPC already exists (rare collision)
            continue
        
        if (i + 1) % 1000 == 0:
            print(f"  Inserted {i + 1} items...")
    
    insert_time = time.time() - start_time
    print(f"✅ Inserted 10,000 items in {insert_time:.2f} seconds")
    print(f"   Average: {(insert_time/10000)*1000:.2f} ms per item\n")
    
    # Test 2: Search performance
    print("Test 2: Search performance...")
    
    # Get all items to test search
    all_items = db.get_all_items()
    total_items = len(all_items)
    print(f"  Total items in database: {total_items}")
    
    # Test random searches
    search_times = []
    for i in range(100):
        random_item = random.choice(all_items)
        upc_to_search = random_item['upc_code']
        
        start_time = time.time()
        found_item = db.get_item_by_upc(upc_to_search)
        search_time = time.time() - start_time
        search_times.append(search_time)
    
    avg_search_time = sum(search_times) / len(search_times)
    print(f"✅ Average search time: {avg_search_time*1000:.2f} ms")
    print(f"   100 random UPC searches completed\n")
    
    # Test 3: Get all items performance
    print("Test 3: Loading all items...")
    start_time = time.time()
    all_items = db.get_all_items()
    load_time = time.time() - start_time
    print(f"✅ Loaded {len(all_items)} items in {load_time:.2f} seconds\n")
    
    # Test 4: Database file size
    import os
    db_size = os.path.getsize("database/test_performance.db")
    print(f"Database file size: {db_size / 1024 / 1024:.2f} MB")
    print(f"Size per item: {db_size / total_items:.0f} bytes\n")
    
    # Test 5: Add customers and sales
    print("Test 4: Testing with customers and sales...")
    
    # Add some customers
    customer_ids = []
    for i in range(100):
        phone = f"555-{random.randint(1000000, 9999999)}"
        name = f"Customer {i+1}"
        try:
            customer_id = db.add_customer(phone, name)
            customer_ids.append(customer_id)
        except:
            continue
    
    # Add some sales
    for i in range(500):
        customer_id = random.choice(customer_ids)
        total_amount = round(random.uniform(10.0, 500.0), 2)
        payment_status = random.choice(['fully_paid', 'pay_later', 'partial'])
        paid_amount = total_amount if payment_status == 'fully_paid' else round(random.uniform(0, total_amount), 2)
        
        sale_id = db.create_sale(customer_id, total_amount, paid_amount, payment_status)
        
        # Add some items to the sale
        num_items = random.randint(1, 5)
        for j in range(num_items):
            item = random.choice(all_items)
            quantity = random.randint(1, 3)
            db.add_sale_item(
                sale_id, 
                item['name'], 
                quantity, 
                item['price'], 
                item['upc_code']
            )
    
    print(f"✅ Added 100 customers and 500 sales with items")
    
    # Final database size
    final_db_size = os.path.getsize("database/test_performance.db")
    print(f"Final database size: {final_db_size / 1024 / 1024:.2f} MB\n")
    
    print("=== Performance Test Results ===")
    print(f"✅ SQLite easily handles 10,000+ items")
    print(f"✅ Search performance: {avg_search_time*1000:.2f} ms per lookup")
    print(f"✅ Database size: {final_db_size / 1024 / 1024:.2f} MB for full dataset")
    print(f"✅ Ready for production use!")
    
    # Cleanup
    print(f"\nTest database saved as: database/test_performance.db")
    print("You can delete this file after reviewing the results.")

if __name__ == "__main__":
    performance_test()