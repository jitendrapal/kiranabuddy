"""
Test CHECK_STOCK heuristic detection (no API calls)
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from ai_service import AIService
from config import Config

def test_check_stock_heuristic():
    """Test that CHECK_STOCK commands are detected by heuristic (not API)"""
    
    print("=" * 80)
    print("Testing CHECK_STOCK Heuristic Detection")
    print("=" * 80)
    
    ai_service = AIService(Config.OPENAI_API_KEY)
    
    # Test cases - all should be detected as CHECK_STOCK
    test_cases = [
        ("maggi ka stock dikhao", "maggi"),
        ("maggi ke kitne packet hai", "maggi"),
        ("maggi kitni bachi hai", "maggi"),
        ("maggi kitni hai", "maggi"),
        ("maggi ki quantity batao", "maggi"),
        ("oil ka stock dikhao", "oil"),
        ("rice kitna hai", "rice"),
        ("atta kitna bacha hai", "atta"),
        ("biscuit ki quantity batao", "biscuit"),
        ("oil dikhao", "oil"),
        ("rice stock check karo", "rice"),
        ("maggi", "maggi"),  # Just product name
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} commands...\n")
    
    passed = 0
    failed = 0
    
    for i, (command, expected_product) in enumerate(test_cases, 1):
        print(f"Test {i}/{len(test_cases)}: '{command}'")
        
        # Parse the command
        parsed = ai_service.parse_command(command)
        
        # Check if action is CHECK_STOCK
        is_check_stock = parsed.action.value == 'check_stock'
        product_match = expected_product.lower() in (parsed.product_name or "").lower()
        
        print(f"  Action: {parsed.action.value}")
        print(f"  Product: '{parsed.product_name}'")
        print(f"  Expected: '{expected_product}'")
        print(f"  Confidence: {parsed.confidence:.2f}")
        
        if is_check_stock and product_match:
            print(f"  ✅ PASSED")
            passed += 1
        else:
            if not is_check_stock:
                print(f"  ❌ FAILED - Expected CHECK_STOCK, got {parsed.action.value}")
            else:
                print(f"  ❌ FAILED - Product mismatch")
            failed += 1
        print()
    
    # Summary
    print(f"{'='*80}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Passed: {passed}/{len(test_cases)} ({passed*100//len(test_cases)}%)")
    print(f"❌ Failed: {failed}/{len(test_cases)} ({failed*100//len(test_cases)}%)")
    print(f"{'='*80}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! CHECK_STOCK heuristic detection works!")
    else:
        print(f"\n⚠️ {failed} test(s) failed.")
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = test_check_stock_heuristic()
    exit(0 if failed == 0 else 1)

