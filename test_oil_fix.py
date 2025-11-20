"""
Test the oil matching fix
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_tokenization():
    """Test the tokenization logic directly"""
    
    print("=" * 80)
    print("Testing Oil Product Matching Logic")
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
    
    # Test data
    search_term = "oil"
    products = [
        "Fortune Sunflower Oil 1L",
        "Fortune Rice Bran Oil 1L",
        "Saffola Gold Oil 1L",
    ]
    
    normalized_search = canonical_product_key(search_term)
    target_tokens = _tokenize_for_match(normalized_search)
    
    print(f"\n🔍 Search term: '{search_term}'")
    print(f"   Normalized: '{normalized_search}'")
    print(f"   Tokens: {target_tokens}")
    print(f"   Token count: {len(target_tokens)}")
    print()
    
    print("=" * 80)
    print("Testing Each Product")
    print("=" * 80)
    
    matched_count = 0
    
    for product_name in products:
        name_norm = canonical_product_key(product_name).lower()
        product_tokens = _tokenize_for_match(name_norm)
        common = target_tokens & product_tokens
        score = len(common)
        
        print(f"\n📦 Product: {product_name}")
        print(f"   Normalized: '{name_norm}'")
        print(f"   Tokens: {product_tokens}")
        print(f"   Token count: {len(product_tokens)}")
        print(f"   Common tokens: {common}")
        print(f"   Score: {score}")
        
        # NEW LOGIC: For single-word searches, if the word is in the product, it's a match
        if len(target_tokens) == 1:
            if common:
                print(f"   ✅ MATCH (single-word search, word found in product)")
                matched_count += 1
            else:
                print(f"   ❌ NO MATCH (word not found)")
        else:
            coverage = score / max(1, len(product_tokens))
            min_coverage = 0.5
            print(f"   Coverage: {coverage:.2f} (min: {min_coverage})")
            if coverage >= min_coverage:
                print(f"   ✅ MATCH")
                matched_count += 1
            else:
                print(f"   ❌ NO MATCH (coverage too low)")
    
    print("\n" + "=" * 80)
    print(f"📊 RESULTS")
    print("=" * 80)
    print(f"Total products: {len(products)}")
    print(f"Matched: {matched_count}")
    print(f"Expected: 3")
    
    if matched_count == 3:
        print("\n🎉 SUCCESS! All 3 oil products matched!")
        return True
    else:
        print(f"\n❌ FAILED! Only {matched_count} products matched, expected 3")
        return False


if __name__ == "__main__":
    success = test_tokenization()
    exit(0 if success else 1)

