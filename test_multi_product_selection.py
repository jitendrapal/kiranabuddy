"""
Test script for multi-product selection feature
"""
from database import FirestoreDB
from config import Config

def test_multi_product_selection():
    """Test the multi-product selection feature"""
    
    print("=" * 60)
    print("Testing Multi-Product Selection Feature")
    print("=" * 60)
    
    # Initialize database
    db = FirestoreDB(Config.GOOGLE_APPLICATION_CREDENTIALS)
    
    # Get shop by phone
    shop_phone = "9876543210"
    shop = db.get_shop_by_phone(shop_phone)
    
    if not shop:
        print(f"❌ No shop found for phone: {shop_phone}")
        return
    
    print(f"\n✅ Found shop: {shop.name} (ID: {shop.shop_id})")
    
    # Test 1: Add some rice products with different brands
    print("\n" + "=" * 60)
    print("Test 1: Creating multiple rice products")
    print("=" * 60)
    
    rice_products = [
        {"name": "Basmati Rice India Gate 1kg", "brand": "India Gate", "price": 120.0},
        {"name": "Basmati Rice Daawat 1kg", "brand": "Daawat", "price": 130.0},
        {"name": "Basmati Rice Kohinoor 1kg", "brand": "Kohinoor", "price": 125.0},
        {"name": "Sona Masoori Rice 1kg", "brand": "Fortune", "price": 80.0},
    ]
    
    created_products = []
    for rice in rice_products:
        product = db.get_or_create_product(
            shop_id=shop.shop_id,
            product_name=rice["name"],
            unit="kg"
        )
        # Update price and brand
        db.update_product_fields(product.product_id, {
            "selling_price": rice["price"],
            "brand": rice["brand"],
        })
        created_products.append(product)
        print(f"✅ Created: {rice['name']} - ₹{rice['price']}")
    
    # Test 2: Search for "rice" - should find multiple matches
    print("\n" + "=" * 60)
    print("Test 2: Searching for 'rice' (should find multiple)")
    print("=" * 60)
    
    matches = db.find_all_matching_products(shop.shop_id, "rice")
    print(f"\n🔍 Found {len(matches)} matching products:")
    for i, p in enumerate(matches, 1):
        print(f"  {i}. {p.name} ({p.brand}) - ₹{p.selling_price}")
    
    if len(matches) >= 2:
        print("\n✅ Test 2 PASSED: Multiple matches found")
    else:
        print("\n❌ Test 2 FAILED: Expected multiple matches")
    
    # Test 3: Search for "basmati" - should find 3 matches
    print("\n" + "=" * 60)
    print("Test 3: Searching for 'basmati' (should find 3)")
    print("=" * 60)
    
    matches = db.find_all_matching_products(shop.shop_id, "basmati")
    print(f"\n🔍 Found {len(matches)} matching products:")
    for i, p in enumerate(matches, 1):
        print(f"  {i}. {p.name} ({p.brand}) - ₹{p.selling_price}")
    
    if len(matches) == 3:
        print("\n✅ Test 3 PASSED: Found 3 basmati rice products")
    else:
        print(f"\n⚠️ Test 3: Expected 3 matches, found {len(matches)}")
    
    # Test 4: Test pending selection save and retrieve
    print("\n" + "=" * 60)
    print("Test 4: Testing pending selection save/retrieve")
    print("=" * 60)
    
    user_phone = "9876543210"
    
    # Save a pending selection
    if matches:
        product_ids = [p.product_id for p in matches]
        product_names = [p.name for p in matches]
        
        pending = db.save_pending_selection(
            shop_id=shop.shop_id,
            user_phone=user_phone,
            action="ADD_STOCK",
            quantity=10.0,
            product_ids=product_ids,
            product_names=product_names,
        )
        print(f"✅ Saved pending selection: {pending.selection_id}")
        print(f"   Action: {pending.action}")
        print(f"   Quantity: {pending.quantity}")
        print(f"   Products: {len(pending.product_ids)}")
        
        # Retrieve the pending selection
        retrieved = db.get_pending_selection(user_phone)
        if retrieved:
            print(f"\n✅ Retrieved pending selection:")
            print(f"   Selection ID: {retrieved.selection_id}")
            print(f"   Action: {retrieved.action}")
            print(f"   Quantity: {retrieved.quantity}")
            print(f"   Expired: {retrieved.is_expired()}")
            print(f"   Products:")
            for i, name in enumerate(retrieved.product_names, 1):
                print(f"     {i}. {name}")
            print("\n✅ Test 4 PASSED: Pending selection saved and retrieved")
        else:
            print("\n❌ Test 4 FAILED: Could not retrieve pending selection")
        
        # Delete the pending selection
        db.delete_pending_selection(user_phone)
        print(f"\n🗑️ Deleted pending selection")
        
        # Verify it's deleted
        retrieved_after_delete = db.get_pending_selection(user_phone)
        if not retrieved_after_delete:
            print("✅ Verified: Pending selection deleted successfully")
        else:
            print("❌ Error: Pending selection still exists after delete")
    
    # Test 5: Search for specific product - should return empty (single match)
    print("\n" + "=" * 60)
    print("Test 5: Searching for specific product (should return empty)")
    print("=" * 60)
    
    matches = db.find_all_matching_products(shop.shop_id, "India Gate")
    print(f"\n🔍 Found {len(matches)} matching products for 'India Gate'")
    
    if len(matches) == 0:
        print("✅ Test 5 PASSED: Single match returns empty (use find_existing_product_by_name instead)")
    else:
        print(f"⚠️ Test 5: Expected 0 matches (single match), found {len(matches)}")
    
    print("\n" + "=" * 60)
    print("✅ All Tests Completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_multi_product_selection()

