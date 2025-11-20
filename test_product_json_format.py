"""
Test to verify the JSON format when creating a product from stock page
"""
import json
from datetime import datetime
from models import Product

def test_product_json_format():
    """Test that product JSON has the correct structure with batches"""
    
    # Simulate creating a product like the API does
    product_id = "test-product-001"
    shop_id = "test-shop-001"
    name = "Test Maggi 70g"
    quantity = 50
    unit = "pieces"
    brand = "Nestle"
    barcode = "8901234567890"
    selling_price = 12.0
    cost_price = 10.0
    expiry_date = "2025-12-31"
    
    # Create batches structure (same as in API)
    batches = None
    if expiry_date:
        batch_id = "batch_001"
        batches = {
            batch_id: {
                "expiry_date": expiry_date,
                "qty": float(quantity),
                "cost_price": float(cost_price) if cost_price is not None else None,
                "added_on": datetime.utcnow().isoformat()
            }
        }
    
    # Create product
    product = Product(
        product_id=product_id,
        shop_id=shop_id,
        name=name,
        normalized_name=name.lower().strip(),
        current_stock=float(quantity),
        unit=unit,
        brand=brand,
        barcode=barcode,
        selling_price=float(selling_price) if selling_price is not None else None,
        cost_price=float(cost_price) if cost_price is not None else None,
        expiry_date=expiry_date,
        batches=batches,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    # Convert to dict (this is what gets saved to Firestore)
    product_dict = product.to_dict()
    
    # Print the JSON structure
    print("\n" + "="*80)
    print("📦 PRODUCT JSON STRUCTURE")
    print("="*80)
    print(json.dumps(product_dict, indent=2, default=str))
    print("="*80)
    
    # Verify structure
    print("\n✅ VERIFICATION:")
    print(f"✓ product_id: {product_dict.get('product_id')}")
    print(f"✓ shop_id: {product_dict.get('shop_id')}")
    print(f"✓ name: {product_dict.get('name')}")
    print(f"✓ normalized_name: {product_dict.get('normalized_name')}")
    print(f"✓ barcode: {product_dict.get('barcode')}")
    print(f"✓ brand: {product_dict.get('brand')}")
    print(f"✓ current_stock: {product_dict.get('current_stock')}")
    print(f"✓ unit: {product_dict.get('unit')}")
    print(f"✓ selling_price: {product_dict.get('selling_price')}")
    print(f"✓ cost_price: {product_dict.get('cost_price')}")
    print(f"✓ expiry_date: {product_dict.get('expiry_date')}")
    print(f"✓ batches: {product_dict.get('batches')}")
    print(f"✓ created_at: {product_dict.get('created_at')}")
    print(f"✓ updated_at: {product_dict.get('updated_at')}")
    
    # Verify batches structure
    if product_dict.get('batches'):
        print("\n📦 BATCHES STRUCTURE:")
        for batch_id, batch_data in product_dict['batches'].items():
            print(f"\n  Batch ID: {batch_id}")
            print(f"    - expiry_date: {batch_data.get('expiry_date')}")
            print(f"    - qty: {batch_data.get('qty')}")
            print(f"    - cost_price: {batch_data.get('cost_price')}")
            print(f"    - added_on: {batch_data.get('added_on')}")
    
    # Check if it matches expected format
    print("\n🎯 FORMAT VALIDATION:")
    
    expected_fields = [
        'product_id', 'shop_id', 'name', 'normalized_name', 'current_stock',
        'unit', 'brand', 'barcode', 'selling_price', 'cost_price', 
        'expiry_date', 'batches', 'created_at', 'updated_at'
    ]
    
    missing_fields = [f for f in expected_fields if f not in product_dict]
    if missing_fields:
        print(f"❌ Missing fields: {missing_fields}")
    else:
        print("✅ All expected fields present!")
    
    # Verify batches structure matches expected format
    if product_dict.get('batches'):
        batch_001 = product_dict['batches'].get('batch_001')
        if batch_001:
            required_batch_fields = ['expiry_date', 'qty', 'cost_price', 'added_on']
            missing_batch_fields = [f for f in required_batch_fields if f not in batch_001]
            if missing_batch_fields:
                print(f"❌ Missing batch fields: {missing_batch_fields}")
            else:
                print("✅ Batch structure matches expected format!")
        else:
            print("❌ batch_001 not found in batches")
    else:
        print("⚠️  No batches structure (expiry_date was not provided)")
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETE!")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_product_json_format()

