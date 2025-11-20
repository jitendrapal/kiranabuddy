"""
Find which shop has rice products
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from database import FirestoreDB

def find_rice_shop():
    """Find which shop has rice products"""
    
    print("=" * 80)
    print("Finding Shops with Rice Products")
    print("=" * 80)
    
    db = FirestoreDB()
    
    # Get all shops
    shops_ref = db.db.collection('shops')
    shops = list(shops_ref.stream())
    
    print(f"\n📍 Found {len(shops)} shops\n")
    
    for shop_doc in shops:
        shop_id = shop_doc.id
        shop_data = shop_doc.to_dict()
        shop_name = shop_data.get('name', 'Unknown')
        
        print(f"\n🏪 Shop: {shop_name} (ID: {shop_id})")
        
        # Get products for this shop
        products_ref = db.db.collection('products').where('shop_id', '==', shop_id)
        products = list(products_ref.stream())
        
        print(f"   Total products: {len(products)}")
        
        # Find rice products
        rice_products = []
        for p_doc in products:
            p_data = p_doc.to_dict()
            name = p_data.get('name', '')
            if 'rice' in name.lower():
                rice_products.append({
                    'name': name,
                    'stock': p_data.get('current_stock', 0),
                    'normalized': p_data.get('normalized_name', '')
                })
        
        if rice_products:
            print(f"   ✅ Found {len(rice_products)} rice products:")
            for rp in rice_products:
                print(f"      - {rp['name']} (Stock: {rp['stock']})")
                print(f"        Normalized: {rp['normalized']}")
        else:
            print(f"   ❌ No rice products")
        
        # Show first 5 products as sample
        if products:
            print(f"\n   Sample products:")
            for p_doc in products[:5]:
                p_data = p_doc.to_dict()
                print(f"      - {p_data.get('name', 'Unknown')}")
    
    print("\n" + "=" * 80)
    print("✅ Search Complete!")
    print("=" * 80)


if __name__ == "__main__":
    find_rice_shop()

