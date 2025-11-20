"""
Test script for command normalization feature
Tests various word orders and action keywords
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from ai_service import AIService
from config import Config

def test_command_normalization():
    """Test command normalization with various word orders"""
    
    print("=" * 80)
    print("Testing Command Normalization Feature")
    print("=" * 80)
    
    # Initialize AI service
    ai_service = AIService(Config.OPENAI_API_KEY)
    
    # Test cases: (input_command, expected_action, expected_product, expected_quantity)
    test_cases = [
        # Standard format (already good)
        ("10 rice add kar do", "ADD_STOCK", "rice", 10.0),
        ("5 maggi bik gaya", "REDUCE_STOCK", "maggi", 5.0),
        ("rice kitna hai", "CHECK_STOCK", "rice", None),
        
        # Reversed order: product first, then quantity
        ("rice 10 add kar do", "ADD_STOCK", "rice", 10.0),
        ("maggi 5 bik gaya", "REDUCE_STOCK", "maggi", 5.0),
        
        # Action first
        ("add 10 rice", "ADD_STOCK", "rice", 10.0),
        ("add rice 10", "ADD_STOCK", "rice", 10.0),
        
        # Different action keywords - ADD variants
        ("10 rice jod do", "ADD_STOCK", "rice", 10.0),
        ("10 rice badha do", "ADD_STOCK", "rice", 10.0),
        ("10 rice dal do", "ADD_STOCK", "rice", 10.0),
        ("10 rice update kar do", "ADD_STOCK", "rice", 10.0),
        ("10 rice ka stock update kar do", "ADD_STOCK", "rice", 10.0),
        ("10 rice aur add kar do", "ADD_STOCK", "rice", 10.0),
        
        # Different action keywords - REDUCE variants
        ("5 maggi bech diya", "REDUCE_STOCK", "maggi", 5.0),
        ("5 maggi sold", "REDUCE_STOCK", "maggi", 5.0),
        ("5 maggi kam kar do", "REDUCE_STOCK", "maggi", 5.0),
        
        # Complex product names
        ("10 Parle G add kar do", "ADD_STOCK", "Parle G", 10.0),
        ("Parle G 10 add kar do", "ADD_STOCK", "Parle G", 10.0),
        ("add 10 Parle G", "ADD_STOCK", "Parle G", 10.0),
        
        # Multi-word products
        ("5 Basmati Rice add kar do", "ADD_STOCK", "Basmati Rice", 5.0),
        ("Basmati Rice 5 add kar do", "ADD_STOCK", "Basmati Rice", 5.0),
        ("add 5 Basmati Rice", "ADD_STOCK", "Basmati Rice", 5.0),
        
        # Quantity at the end
        ("rice badha do 10", "ADD_STOCK", "rice", 10.0),
        ("maggi bech diya 5", "REDUCE_STOCK", "maggi", 5.0),
    ]
    
    print(f"\n🧪 Running {len(test_cases)} test cases...\n")
    
    passed = 0
    failed = 0
    
    for i, (input_cmd, expected_action, expected_product, expected_qty) in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}/{len(test_cases)}: '{input_cmd}'")
        print(f"{'='*80}")
        
        # Parse the command
        parsed = ai_service.parse_command(input_cmd)
        
        # Check results (case-insensitive comparison for action)
        action_match = parsed.action.value.upper() == expected_action.upper()
        product_match = expected_product.lower() in (parsed.product_name or "").lower()
        qty_match = (parsed.quantity == expected_qty) if expected_qty else (parsed.quantity is None)
        
        all_match = action_match and product_match and qty_match
        
        # Print results
        print(f"📝 Input:    '{input_cmd}'")
        print(f"🎯 Expected: Action={expected_action}, Product='{expected_product}', Qty={expected_qty}")
        print(f"✨ Got:      Action={parsed.action.value}, Product='{parsed.product_name}', Qty={parsed.quantity}")
        print(f"📊 Confidence: {parsed.confidence:.2f}")
        
        if all_match:
            print(f"✅ PASSED")
            passed += 1
        else:
            print(f"❌ FAILED")
            if not action_match:
                print(f"   ❌ Action mismatch: expected {expected_action}, got {parsed.action.value}")
            if not product_match:
                print(f"   ❌ Product mismatch: expected '{expected_product}', got '{parsed.product_name}'")
            if not qty_match:
                print(f"   ❌ Quantity mismatch: expected {expected_qty}, got {parsed.quantity}")
            failed += 1
    
    # Summary
    print(f"\n{'='*80}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Passed: {passed}/{len(test_cases)} ({passed*100//len(test_cases)}%)")
    print(f"❌ Failed: {failed}/{len(test_cases)} ({failed*100//len(test_cases)}%)")
    print(f"{'='*80}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please review the output above.")
    
    return passed, failed


def test_normalization_only():
    """Test just the normalization function"""
    
    print("\n" + "=" * 80)
    print("Testing Normalization Function Only")
    print("=" * 80)
    
    ai_service = AIService(Config.OPENAI_API_KEY)
    
    test_inputs = [
        "10 rice add kar do",
        "rice 10 add kar do",
        "add 10 rice",
        "10 rice jod do",
        "10 rice badha do",
        "rice badha do 10",
        "10 rice ka stock update kar do",
        "5 maggi bik gaya",
        "maggi 5 bech diya",
        "rice kitna hai",
        "kitna hai rice",
    ]
    
    print("\n🔄 Normalization Results:\n")
    for input_text in test_inputs:
        normalized = ai_service.normalize_command_structure(input_text)
        print(f"📝 '{input_text}'")
        print(f"   → '{normalized}'")
        print()


if __name__ == "__main__":
    # Test normalization function first
    test_normalization_only()
    
    # Then test full command parsing
    print("\n\n")
    passed, failed = test_command_normalization()
    
    # Exit with appropriate code
    exit(0 if failed == 0 else 1)

