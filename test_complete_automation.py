"""
Complete Automation Test Suite for ADD, REDUCE, and CHECK_STOCK Commands

Tests all variations we've implemented:
1. Hindi number words (teen, panch, das)
2. English number words (five, ten, twenty)
3. Different word orders (rice 10 add, 10 rice add, add 10 rice)
4. CHECK_STOCK variations (dikhao, kitna, batao)
5. Multiple product matching
"""
from ai_service import AIService
from config import Config
import time

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_add_stock_commands():
    """Test ADD_STOCK with various formats"""
    print_section("TEST 1: ADD_STOCK Commands")
    
    ai_service = AIService(Config.OPENAI_API_KEY)
    
    test_cases = [
        # Standard format
        ("10 rice add kar do", "add_stock", "rice", 10),
        ("5 oil badha do", "add_stock", "oil", 5),
        ("20 maggi jod do", "add_stock", "maggi", 20),
        
        # Different word orders
        ("rice 10 add kar do", "add_stock", "rice", 10),
        ("oil 5 badha do", "add_stock", "oil", 5),
        ("add 10 rice", "add_stock", "rice", 10),
        ("badha do 5 oil", "add_stock", "oil", 5),
        
        # Hindi number words
        ("teen rice add kar do", "add_stock", "rice", 3),
        ("panch oil badha do", "add_stock", "oil", 5),
        ("das maggi add karo", "add_stock", "maggi", 10),
        ("bees atta jod do", "add_stock", "atta", 20),
        
        # English number words
        ("five rice add kar do", "add_stock", "rice", 5),
        ("ten oil badha do", "add_stock", "oil", 10),
        ("twenty maggi add karo", "add_stock", "maggi", 20),
        
        # Mixed formats with Hindi numbers
        ("rice teen add kar do", "add_stock", "rice", 3),
        ("oil panch badha do", "add_stock", "oil", 5),
        ("maggi das add karo", "add_stock", "maggi", 10),
    ]
    
    passed = 0
    failed = 0
    
    for message, expected_action, expected_product, expected_quantity in test_cases:
        try:
            result = ai_service.parse_command(message)
            
            action_match = result.action.value == expected_action
            product_match = expected_product.lower() in result.product_name.lower()
            quantity_match = result.quantity == expected_quantity
            
            if action_match and product_match and quantity_match:
                print(f"✅ '{message}' → {result.action.value}, {result.product_name}, qty={result.quantity}")
                passed += 1
            else:
                print(f"❌ '{message}'")
                print(f"   Expected: {expected_action}, {expected_product}, qty={expected_quantity}")
                print(f"   Got: {result.action.value}, {result.product_name}, qty={result.quantity}")
                failed += 1
                
        except Exception as e:
            print(f"❌ '{message}' → ERROR: {e}")
            failed += 1
        
        time.sleep(0.1)  # Small delay to avoid rate limits
    
    print(f"\n📊 ADD_STOCK Results: {passed}/{len(test_cases)} passed ({passed*100//len(test_cases)}%)")
    return passed, failed

def test_reduce_stock_commands():
    """Test REDUCE_STOCK with various formats"""
    print_section("TEST 2: REDUCE_STOCK Commands")
    
    ai_service = AIService(Config.OPENAI_API_KEY)
    
    test_cases = [
        # Standard format
        ("10 rice bech diya", "reduce_stock", "rice", 10),
        ("5 oil sold", "reduce_stock", "oil", 5),
        ("3 maggi customer ko diya", "reduce_stock", "maggi", 3),
        
        # Different word orders
        ("rice 10 bech diya", "reduce_stock", "rice", 10),
        ("oil 5 sold", "reduce_stock", "oil", 5),
        ("bik gaya 3 maggi", "reduce_stock", "maggi", 3),
        
        # Hindi number words
        ("teen rice bech diya", "reduce_stock", "rice", 3),
        ("panch oil sold", "reduce_stock", "oil", 5),
        ("das maggi bik gaya", "reduce_stock", "maggi", 10),
        
        # English number words
        ("five rice sold", "reduce_stock", "rice", 5),
        ("ten oil bech diya", "reduce_stock", "oil", 10),
        
        # Mixed formats
        ("rice teen bech diya", "reduce_stock", "rice", 3),
        ("oil panch sold", "reduce_stock", "oil", 5),
    ]
    
    passed = 0
    failed = 0
    
    for message, expected_action, expected_product, expected_quantity in test_cases:
        try:
            result = ai_service.parse_command(message)
            
            action_match = result.action.value == expected_action
            product_match = expected_product.lower() in result.product_name.lower()
            quantity_match = result.quantity == expected_quantity
            
            if action_match and product_match and quantity_match:
                print(f"✅ '{message}' → {result.action.value}, {result.product_name}, qty={result.quantity}")
                passed += 1
            else:
                print(f"❌ '{message}'")
                print(f"   Expected: {expected_action}, {expected_product}, qty={expected_quantity}")
                print(f"   Got: {result.action.value}, {result.product_name}, qty={result.quantity}")
                failed += 1
                
        except Exception as e:
            print(f"❌ '{message}' → ERROR: {e}")
            failed += 1
        
        time.sleep(0.1)  # Small delay to avoid rate limits
    
    print(f"\n📊 REDUCE_STOCK Results: {passed}/{len(test_cases)} passed ({passed*100//len(test_cases)}%)")
    return passed, failed

def test_check_stock_commands():
    """Test CHECK_STOCK with various formats"""
    print_section("TEST 3: CHECK_STOCK Commands")

    ai_service = AIService(Config.OPENAI_API_KEY)

    test_cases = [
        # Standard variations
        ("maggi ka stock dikhao", "check_stock", "maggi"),
        ("rice kitna hai", "check_stock", "rice"),
        ("oil batao", "check_stock", "oil"),
        ("ghee dikhao", "check_stock", "ghee"),
        ("atta ka stock batao", "check_stock", "atta"),

        # Different keywords
        ("maggi kitna bachi hai", "check_stock", "maggi"),
        ("rice ke packet kitne hai", "check_stock", "rice"),
        ("oil ki quantity batao", "check_stock", "oil"),
        ("ghee ka stock check karo", "check_stock", "ghee"),

        # With typos (should still work)
        ("gheee ka stock dikhao", "check_stock", "ghee"),
        ("riceee kitna hai", "check_stock", "rice"),
        ("oill dikhao", "check_stock", "oil"),

        # Short forms
        ("maggi dikhao", "check_stock", "maggi"),
        ("rice kitna", "check_stock", "rice"),
        ("oil batao", "check_stock", "oil"),
    ]

    passed = 0
    failed = 0

    for message, expected_action, expected_product in test_cases:
        try:
            result = ai_service.parse_command(message)

            action_match = result.action.value == expected_action
            product_match = expected_product.lower() in result.product_name.lower()

            if action_match and product_match:
                print(f"✅ '{message}' → {result.action.value}, product='{result.product_name}'")
                passed += 1
            else:
                print(f"❌ '{message}'")
                print(f"   Expected: {expected_action}, product='{expected_product}'")
                print(f"   Got: {result.action.value}, product='{result.product_name}'")
                failed += 1

        except Exception as e:
            print(f"❌ '{message}' → ERROR: {e}")
            failed += 1

        time.sleep(0.1)  # Small delay to avoid rate limits

    print(f"\n📊 CHECK_STOCK Results: {passed}/{len(test_cases)} passed ({passed*100//len(test_cases)}%)")
    return passed, failed

def test_undo_commands():
    """Test UNDO commands"""
    print_section("TEST 4: UNDO Commands")

    ai_service = AIService(Config.OPENAI_API_KEY)

    test_cases = [
        ("undo", "undo_last"),
        ("undo kar do", "undo_last"),
        ("galti ho gayi", "undo_last"),
        ("wapas kar do", "undo_last"),
        ("hatao", "undo_last"),
        ("wrong entry", "undo_last"),
        ("mistake ho gaya", "undo_last"),
    ]

    passed = 0
    failed = 0

    for message, expected_action in test_cases:
        try:
            result = ai_service.parse_command(message)

            if result.action.value == expected_action:
                print(f"✅ '{message}' → {result.action.value}")
                passed += 1
            else:
                print(f"❌ '{message}' → Expected: {expected_action}, Got: {result.action.value}")
                failed += 1

        except Exception as e:
            print(f"❌ '{message}' → ERROR: {e}")
            failed += 1

        time.sleep(0.1)

    print(f"\n📊 UNDO Results: {passed}/{len(test_cases)} passed ({passed*100//len(test_cases)}%)")
    return passed, failed

def run_all_tests():
    """Run all test suites and show summary"""
    print("\n" + "🚀" * 40)
    print("  COMPLETE AUTOMATION TEST SUITE")
    print("  Testing ADD, REDUCE, CHECK_STOCK, and UNDO Commands")
    print("🚀" * 40)

    total_passed = 0
    total_failed = 0

    # Test 1: ADD_STOCK
    passed, failed = test_add_stock_commands()
    total_passed += passed
    total_failed += failed

    # Test 2: REDUCE_STOCK
    passed, failed = test_reduce_stock_commands()
    total_passed += passed
    total_failed += failed

    # Test 3: CHECK_STOCK
    passed, failed = test_check_stock_commands()
    total_passed += passed
    total_failed += failed

    # Test 4: UNDO
    passed, failed = test_undo_commands()
    total_passed += passed
    total_failed += failed

    # Final Summary
    print("\n" + "=" * 80)
    print("  FINAL SUMMARY")
    print("=" * 80)
    total_tests = total_passed + total_failed
    success_rate = (total_passed * 100 // total_tests) if total_tests > 0 else 0

    print(f"\n📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"📈 Success Rate: {success_rate}%")

    if total_failed == 0:
        print("\n🎉 ALL TESTS PASSED! Everything is working perfectly! 🎉")
    elif success_rate >= 90:
        print(f"\n✅ Great! {success_rate}% tests passed. Minor issues detected.")
    elif success_rate >= 70:
        print(f"\n⚠️ {success_rate}% tests passed. Some issues need attention.")
    else:
        print(f"\n❌ Only {success_rate}% tests passed. Major issues detected.")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    run_all_tests()


