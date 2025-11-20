"""
Debug test for oil product matching
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from database import FirestoreDB

def test_oil_matching():
    """Test why only 2 out of 3 oil products are matched"""
    
    print("=" * 80)
    print("Debug Test - Oil Product Matching")
    print("=" * 80)
    
    # Initialize database
    db = FirestoreDB()
    
    # Get test shop
    shop = db.get_shop_by_phone("9876543210")
    if not shop:
        print("❌ Test shop not found!")
        return
    
    shop_id = shop.shop_id
    print(f"\n✅ Found shop: {shop.name} (ID: {shop_id})")
    
    # Get all products
    all_products = db.get_products_by_shop(shop_id)
    
    # Filter oil products manually
    oil_products = [p for p in all_products if 'oil' in p.name.lower()]
    
    print(f"\n📦 All Oil Products in Database ({len(oil_products)}):")
    for i, p in enumerate(oil_products, 1):
        print(f"{i}. {p.name}")
        print(f"   Normalized: {p.normalized_name}")
        print(f"   Stock: {p.current_stock}")
        print()
    
    # Test the matching function
    print("=" * 80)
    print("Testing find_all_matching_products('oil')")
    print("=" * 80)
    
    matching = db.find_all_matching_products(shop_id, "oil")
    
    print(f"\n✅ Matched Products ({len(matching)}):")
    for i, p in enumerate(matching, 1):
        print(f"{i}. {p.name}")
    
    print(f"\n❌ Missing Products ({len(oil_products) - len(matching)}):")
    matched_names = {p.name for p in matching}
    for p in oil_products:
        if p.name not in matched_names:
            print(f"   - {p.name}")
            print(f"     Normalized: {p.normalized_name}")
    
    # Debug tokenization
    print("\n" + "=" * 80)
    print("Debug Tokenization")
    print("=" * 80)
    
    from database import canonical_product_key
    
    def _tokenize_for_match(text: str) -> set:
        if not text:
            return set()
        s = text.lower().replace("-", " ")
        cleaned_chars = []
        for ch in s:
            if ch.isdigit() or ch in "+-":
                cleaned_chars.append(" ")
            else:
                cleaned_chars.append(ch)
        s = "".join(cleaned_chars)
        stopwords = {
            "add", "added", "sold", "sale", "bought", "purchase", "customer",
            "new", "stock", "ne", "ko", "hai", "pieces", "piece", "packet",
            "packets", "kg", "g", "gm", "ml", "ltr", "l",
        }
        tokens = [t for t in s.split() if t and t not in stopwords]
        return set(tokens)
    
    search_term = "oil"
    normalized_search = canonical_product_key(search_term)
    target_tokens = _tokenize_for_match(normalized_search)
    
    print(f"\nSearch term: '{search_term}'")
    print(f"Normalized: '{normalized_search}'")
    print(f"Tokens: {target_tokens}")
    print()
    
    for p in oil_products:
        name_norm = (p.normalized_name or "").strip().lower()
        product_tokens = _tokenize_for_match(name_norm)
        common = target_tokens & product_tokens
        score = len(common)
        coverage = score / max(1, len(product_tokens))
        min_coverage = 0.3 if len(target_tokens) == 1 else 0.5
        
        print(f"Product: {p.name}")
        print(f"  Normalized: '{name_norm}'")
        print(f"  Tokens: {product_tokens}")
        print(f"  Common tokens: {common}")
        print(f"  Score: {score}")
        print(f"  Coverage: {coverage:.2f} (min: {min_coverage})")
        print(f"  Match: {'✅ YES' if coverage >= min_coverage else '❌ NO'}")
        print()


if __name__ == "__main__":
    test_oil_matching()

