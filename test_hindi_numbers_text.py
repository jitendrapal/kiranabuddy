"""
Test Hindi number word conversion in TEXT commands (not just voice)
"""
from ai_service import AIService
from config import Config

def test_hindi_numbers_in_text_commands():
    """Test that Hindi number words work in text commands"""
    
    print("=" * 80)
    print("Testing Hindi Number Words in Text Commands")
    print("=" * 80)
    
    ai_service = AIService(Config.OPENAI_API_KEY)
    
    test_cases = [
        # Hindi number words
        ("teen rice add kar do", "add_stock", "rice", 3),
        ("panch rice add kar do", "add_stock", "rice", 5),
        ("das oil badha do", "add_stock", "oil", 10),
        ("bees maggi add karo", "add_stock", "maggi", 20),
        
        # English number words
        ("five rice add kar do", "add_stock", "rice", 5),
        ("ten oil badha do", "add_stock", "oil", 10),
        ("twenty maggi add karo", "add_stock", "maggi", 20),
        
        # Mixed formats
        ("rice teen add kar do", "add_stock", "rice", 3),
        ("oil panch badha do", "add_stock", "oil", 5),
        ("maggi das add karo", "add_stock", "maggi", 10),
        
        # Reduce stock
        ("teen rice bech diya", "reduce_stock", "rice", 3),
        ("panch oil sold", "reduce_stock", "oil", 5),
        ("das maggi customer ko diya", "reduce_stock", "maggi", 10),
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
                print(f"✅ '{message}'")
                print(f"   → {result.action.value}, product='{result.product_name}', qty={result.quantity}")
                passed += 1
            else:
                print(f"❌ '{message}'")
                print(f"   Expected: {expected_action}, product='{expected_product}', qty={expected_quantity}")
                print(f"   Got: {result.action.value}, product='{result.product_name}', qty={result.quantity}")
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
    test_hindi_numbers_in_text_commands()

