"""
Test script to verify Hindi Number Normalization feature
"""
import os
from ai_service import AIService
from config import Config

# Initialize AI service
ai_service = AIService(api_key=Config.OPENAI_API_KEY)

# Test cases for Hindi number conversion
test_cases = [
    # The main problem case
    ("Maggi do add kar do", "Maggi 2 add kar do"),
    ("Maggi do add kardo", "Maggi 2 add kardo"),
    
    # Common Hindi numbers (1-10)
    ("Parle G ek add karo", "Parle G 1 add karo"),
    ("Maggi do bik gaya", "Maggi 2 bik gaya"),
    ("Colgate teen add", "Colgate 3 add"),
    ("Surf Excel char bik gaya", "Surf Excel 4 bik gaya"),
    ("Lays panch add karo", "Lays 5 add karo"),
    ("Kurkure chhe bik gaya", "Kurkure 6 bik gaya"),
    ("Biscuit saat add", "Biscuit 7 add"),
    ("Chips aath bik gaya", "Chips 8 bik gaya"),
    ("Namkeen nau add karo", "Namkeen 9 add karo"),
    ("Toffee das bik gaya", "Toffee 10 bik gaya"),
    
    # Larger numbers
    ("Maggi bees add karo", "Maggi 20 add karo"),
    ("Parle G tees bik gaya", "Parle G 30 bik gaya"),
    ("Colgate pachas add", "Colgate 50 add"),
    ("Surf Excel sau bik gaya", "Surf Excel 100 bik gaya"),
    
    # With filler words
    ("um Maggi do add kar do", "Maggi 2 add kar do"),
    ("uh Parle G teen bik gaya", "Parle G 3 bik gaya"),
    
    # Already digits (should remain unchanged)
    ("Maggi 2 add karo", "Maggi 2 add karo"),
    ("Parle G 5 bik gaya", "Parle G 5 bik gaya"),
    
    # Complex cases
    ("Maggi Maggi do add kar do", "Maggi 2 add kar do"),
    ("um uh Parle G teen teen add karo", "Parle G 3 add karo"),
]

print("🔢 Testing Hindi Number Normalization\n")
print("=" * 80)

passed = 0
failed = 0
failed_cases = []

for raw_text, expected in test_cases:
    print(f"\n📝 Input:    '{raw_text}'")
    
    cleaned = ai_service.clean_voice_text(raw_text)
    
    print(f"✨ Cleaned:  '{cleaned}'")
    print(f"🎯 Expected: '{expected}'")
    
    # Check if cleaned text matches expected
    if cleaned.lower().strip() == expected.lower().strip():
        print("✅ EXACT MATCH")
        passed += 1
    else:
        print("❌ MISMATCH")
        failed += 1
        failed_cases.append((raw_text, expected, cleaned))

print("\n" + "=" * 80)
print(f"\n📊 Results:")
print(f"   ✅ Passed: {passed}/{len(test_cases)}")
print(f"   ❌ Failed: {failed}/{len(test_cases)}")

if failed > 0:
    print(f"\n❌ Failed cases:")
    for raw, expected, cleaned in failed_cases:
        print(f"   Input:    '{raw}'")
        print(f"   Expected: '{expected}'")
        print(f"   Got:      '{cleaned}'")
        print()
else:
    print(f"\n🎉 All tests passed! Hindi number normalization is working perfectly!")

print("\n" + "=" * 80)

# Show some examples of how this helps AI parsing
print("\n🤖 How This Helps AI Parsing:\n")
examples = [
    ("Maggi do add kar do", "Maggi 2 add kar do", "ADD_STOCK, Maggi, 2"),
    ("Parle G teen bik gaya", "Parle G 3 bik gaya", "REDUCE_STOCK, Parle G, 3"),
    ("Colgate panch add karo", "Colgate 5 add karo", "ADD_STOCK, Colgate, 5"),
]

for original, cleaned, parsed in examples:
    print(f"Original:  '{original}'")
    print(f"Cleaned:   '{cleaned}'")
    print(f"AI Parses: {parsed}")
    print()

print("=" * 80)

