"""
Test CHECK_STOCK detection for ghee and other products
"""
from ai_service import AIService
from config import Config

def test_ghee_stock_detection():
    """Test that 'ghee ka stock dikhao' is correctly parsed as CHECK_STOCK"""
    
    print("=" * 80)
    print("Testing CHECK_STOCK Detection for Ghee and Other Products")
    print("=" * 80)
    
    ai_service = AIService(Config.OPENAI_API_KEY)
    
    test_cases = [
        # Ghee variations
        ("ghee ka stock dikhao", "ghee"),
        ("ghee kitna hai", "ghee"),
        ("ghee batao", "ghee"),
        ("ghee dikhao", "ghee"),
        ("gheee ka stock dikhao", "gheee"),  # Typo
        
        # Rice variations
        ("rice ka stock dikhao", "rice"),
        ("rice kitna hai", "rice"),
        ("riceee dikhao", "riceee"),  # Typo
        
        # Oil variations
        ("oil ka stock dikhao", "oil"),
        ("oil kitna hai", "oil"),
        ("oill batao", "oill"),  # Typo
        
        # Atta variations
        ("atta ka stock dikhao", "atta"),
        ("atta kitna hai", "atta"),
        
        # Maggi variations
        ("maggi ka stock dikhao", "maggi"),
        ("maggi kitna hai", "maggi"),
    ]
    
    passed = 0
    failed = 0
    
    for message, expected_product in test_cases:
        try:
            result = ai_service.parse_command(message)
            
            if result.action.value == "check_stock":
                if result.product_name.lower() == expected_product.lower():
                    print(f"✅ '{message}' → CHECK_STOCK, product='{result.product_name}'")
                    passed += 1
                else:
                    print(f"❌ '{message}' → CHECK_STOCK, but product='{result.product_name}' (expected '{expected_product}')")
                    failed += 1
            else:
                print(f"❌ '{message}' → {result.action.value} (expected CHECK_STOCK)")
                failed += 1
                
        except Exception as e:
            print(f"❌ '{message}' → ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"Results: {passed}/{len(test_cases)} passed ({passed*100//len(test_cases)}%)")
    print("=" * 80)
    
    if failed > 0:
        print(f"\n⚠️ {failed} tests failed!")
    else:
        print("\n🎉 All tests passed!")

if __name__ == "__main__":
    test_ghee_stock_detection()

