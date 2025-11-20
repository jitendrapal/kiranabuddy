"""
Test all variations of CHECK_STOCK commands
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from ai_service import AIService
from config import Config

def test_check_stock_variations():
    """Test all ways to ask for stock"""
    
    print("=" * 80)
    print("Testing CHECK_STOCK Command Variations")
    print("=" * 80)
    
    ai_service = AIService(Config.OPENAI_API_KEY)
    
    # All the variations user mentioned
    test_cases = [
        "maggi ka stock dikhao",
        "maggi ke kitne packet hai",
        "maggi kitni bachi hai",
        "maggi kitni hai",
        "maggi ki quantity batao",
        # Additional variations
        "oil ka stock dikhao",
        "rice kitna hai",
        "atta kitna bacha hai",
        "biscuit ki quantity batao",
        "maggi",  # Just product name
        "oil dikhao",
        "rice stock check karo",
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} variations...\n")
    
    passed = 0
    failed = 0
    
    for i, command in enumerate(test_cases, 1):
        print(f"\nTest {i}/{len(test_cases)}: '{command}'")
        
        # Parse the command
        parsed = ai_service.parse_command(command)
        
        # Check if action is CHECK_STOCK
        is_check_stock = parsed.action.value == 'check_stock'
        
        print(f"  Action: {parsed.action.value}")
        print(f"  Product: '{parsed.product_name}'")
        print(f"  Confidence: {parsed.confidence:.2f}")
        
        if is_check_stock:
            print(f"  ✅ PASSED - Correctly identified as CHECK_STOCK")
            passed += 1
        else:
            print(f"  ❌ FAILED - Expected CHECK_STOCK, got {parsed.action.value}")
            failed += 1
    
    # Summary
    print(f"\n{'='*80}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Passed: {passed}/{len(test_cases)} ({passed*100//len(test_cases)}%)")
    print(f"❌ Failed: {failed}/{len(test_cases)} ({failed*100//len(test_cases)}%)")
    print(f"{'='*80}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! All CHECK_STOCK variations work!")
    else:
        print(f"\n⚠️ {failed} test(s) failed.")
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = test_check_stock_variations()
    exit(0 if failed == 0 else 1)

