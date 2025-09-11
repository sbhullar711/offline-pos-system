#!/usr/bin/env python3
"""
Populate the main POS database with test data for development
This creates test customers and items in your main pos_system.db
"""

import random
from database.models import DatabaseManager

def populate_test_data():
    """Add test customers and items to the main database"""
    
    print("=== Populating Test Data for POS System ===\n")
    
    # Initialize main database
    db = DatabaseManager("database/pos_system.db")
    
    # Test customers
    test_customers = [
        ("555-0101", "John Smith"),
        ("555-0102", "Sarah Johnson"),
        ("555-0103", "Mike Chen"),
        ("555-0104", "Emily Davis"),
        ("555-0105", "David Wilson"),
        ("555-0106", "Lisa Anderson"),
        ("555-0107", "Tom Brown"),
        ("555-0108", "Jessica Miller"),
        ("555-0109", "Chris Garcia"),
        ("555-0110", "Amanda Rodriguez")
    ]
    
    print("Adding test customers...")
    customers_added = 0
    for phone, name in test_customers:
        try:
            existing = db.get_customer_by_phone(phone)
            if not existing:
                db.add_customer(phone, name)
                customers_added += 1
                print(f"  ✅ Added: {name} ({phone})")
            else:
                print(f"  ⚠️  Exists: {name} ({phone})")
        except Exception as e:
            print(f"  ❌ Error adding {name}: {str(e)}")
    
    print(f"Added {customers_added} new customers\n")
    
    # Test items - common store products
    test_items = [
        ("123456789012", "Coca Cola 12oz Can", 1.99),
        ("123456789013", "Pepsi 12oz Can", 1.99),
        ("123456789014", "Sprite 12oz Can", 1.99),
        ("123456789015", "Water Bottle 16oz", 0.99),
        ("123456789016", "Energy Drink", 2.99),
        ("123456789017", "Coffee - Dark Roast", 4.99),
        ("123456789018", "Chocolate Bar", 1.49),
        ("123456789019", "Potato Chips", 2.49),
        ("123456789020", "Candy Bar", 1.29),
        ("123456789021", "Gum Pack", 1.99),
        ("123456789022", "Sandwich - Turkey", 5.99),
        ("123456789023", "Sandwich - Ham", 5.99),
        ("123456789024", "Hot Dog", 3.49),
        ("123456789025", "Pizza Slice", 4.99),
        ("123456789026", "Bagel with Cream Cheese", 2.99),
        ("123456789027", "Muffin - Blueberry", 2.49),
        ("123456789028", "Donut - Glazed", 1.99),
        ("123456789029", "Cookie - Chocolate Chip", 1.79),
        ("123456789030", "Apple", 0.99),
        ("123456789031", "Banana", 0.79),
        ("123456789032", "Orange", 1.19),
        ("123456789033", "Granola Bar", 1.99),
        ("123456789034", "Trail Mix", 3.99),
        ("123456789035", "Yogurt Cup", 1.49),
        ("123456789036", "Milk 16oz", 2.99),
        ("123456789037", "Orange Juice 12oz", 2.49),
        ("123456789038", "Sports Drink", 2.19),
        ("123456789039", "Ice Cream Sandwich", 2.99),
        ("123456789040", "Frozen Burrito", 3.99),
        ("123456789041", "Notebook", 3.99),
        ("123456789042", "Pen - Blue", 1.49),
        ("123456789043", "Pencil", 0.99),
        ("123456789044", "Eraser", 0.79),
        ("123456789045", "Tissues", 2.99),
        ("123456789046", "Hand Sanitizer", 3.49),
        ("123456789047", "Aspirin", 4.99),
        ("123456789048", "Band-Aids", 3.99),
        ("123456789049", "Lip Balm", 2.49),
        ("123456789050", "Sunglasses", 9.99)
    ]
    
    print("Adding test items...")
    items_added = 0
    for upc, name, price in test_items:
        try:
            existing = db.get_item_by_upc(upc)
            if not existing:
                db.add_item(upc, name, price)
                items_added += 1
                print(f"  ✅ Added: {name} (${price}) - UPC: {upc}")
            else:
                print(f"  ⚠️  Exists: {name} - UPC: {upc}")
        except Exception as e:
            print(f"  ❌ Error adding {name}: {str(e)}")
    
    print(f"Added {items_added} new items\n")
    
    # Create some sample sales
    print("Creating sample sales...")
    
    # Get all customers and items
    all_customers = []
    for phone, name in test_customers:
        customer = db.get_customer_by_phone(phone)
        if customer:
            all_customers.append(customer)
    
    all_items = db.get_all_items()
    
    if all_customers and all_items:
        sales_created = 0
        for i in range(5):  # Create 5 sample sales
            customer = random.choice(all_customers)
            payment_status = random.choice(['fully_paid', 'pay_later', 'partial'])
            
            # Select 2-4 random items
            num_items = random.randint(2, 4)
            selected_items = random.sample(all_items, num_items)
            
            # Calculate total
            total_amount = 0
            sale_items_data = []
            
            for item in selected_items:
                quantity = random.randint(1, 2)
                item_total = item['price'] * quantity
                total_amount += item_total
                
                sale_items_data.append({
                    'name': item['name'],
                    'upc_code': item['upc_code'],
                    'quantity': quantity,
                    'unit_price': item['price'],
                    'discounted_price': item['price'],
                    'is_xt_item': False
                })
            
            # Determine paid amount
            if payment_status == 'fully_paid':
                paid_amount = total_amount
            elif payment_status == 'partial':
                paid_amount = round(total_amount * 0.5, 2)  # 50% paid
            else:  # pay_later
                paid_amount = 0.0
            
            # Create sale
            try:
                sale_id = db.create_sale(
                    customer_id=customer['id'],
                    total_amount=total_amount,
                    paid_amount=paid_amount,
                    payment_status=payment_status
                )
                
                # Add sale items
                for item_data in sale_items_data:
                    db.add_sale_item(
                        sale_id=sale_id,
                        item_name=item_data['name'],
                        quantity=item_data['quantity'],
                        unit_price=item_data['unit_price'],
                        upc_code=item_data['upc_code'],
                        discounted_price=item_data['discounted_price'],
                        is_xt_item=item_data['is_xt_item']
                    )
                
                sales_created += 1
                print(f"  ✅ Created sale #{sale_id} for {customer['name']} - ${total_amount:.2f} ({payment_status})")
                
            except Exception as e:
                print(f"  ❌ Error creating sale: {str(e)}")
        
        print(f"Created {sales_created} sample sales\n")
    
    print("=== Test Data Population Complete ===")
    print(f"✅ {customers_added} customers added")
    print(f"✅ {items_added} items added") 
    print(f"✅ Ready to test the POS system!")
    print("\nTo test:")
    print("1. Run: python main.py")
    print("2. Click 'SALE' button")
    print("3. Try phone numbers like: 555-0101, 555-0102, etc.")
    print("4. Scan UPC codes like: 123456789012, 123456789013, etc.")

if __name__ == "__main__":
    populate_test_data()