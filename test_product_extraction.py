"""
Quick test for product name extraction
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from ai_service import AIService
from config import Config

def test_product_extraction():
    """Test that product names are extracted correctly"""
    
    print("=" * 80)
    print("Testing Product Name Extraction")
    print("=" * 80)
    
    ai_service = AIService(Config.OPENAI_API_KEY)
    
    test_cases = [
        # (input, expected_product_name)
        ("10 rice add kar do", "rice"),
        ("rice 10 add kar do", "rice"),
        ("add 10 rice", "rice"),
        ("10 rice badha do", "rice"),
        ("rice badha do 10", "rice"),
        ("5 maggi bik gaya", "maggi"),
        ("maggi 5 bech diya", "maggi"),
        ("10 Parle G add kar do", "Parle G"),
        ("Parle G 10 add kar do", "Parle G"),
        ("5 Basmati Rice add kar do", "Basmati Rice"),
        ("Basmati Rice 5 add kar do", "Basmati Rice"),
    ]
    
    print(f"\n🧪 Running {len(test_cases)} test cases...\n")
    
    passed = 0
    failed = 0
    
    for i, (input_cmd, expected_product) in enumerate(test_cases, 1):
        print(f"\nTest {i}/{len(test_cases)}: '{input_cmd}'")
        
        # Parse the command
        parsed = ai_service.parse_command(input_cmd)
        
        # Check if product name matches
        product_match = expected_product.lower() == (parsed.product_name or "").lower()
        
        print(f"  Expected product: '{expected_product}'")
        print(f"  Got product:      '{parsed.product_name}'")
        print(f"  Action:           {parsed.action.value}")
        print(f"  Quantity:         {parsed.quantity}")
        
        if product_match:
            print(f"  ✅ PASSED")
            passed += 1
        else:
            print(f"  ❌ FAILED - Product name mismatch!")
            failed += 1
    
    # Summary
    print(f"\n{'='*80}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Passed: {passed}/{len(test_cases)} ({passed*100//len(test_cases)}%)")
    print(f"❌ Failed: {failed}/{len(test_cases)} ({failed*100//len(test_cases)}%)")
    print(f"{'='*80}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Product extraction is working correctly! 🎉")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please review the output above.")
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = test_product_extraction()
    exit(0 if failed == 0 else 1)

