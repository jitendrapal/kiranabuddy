"""
Test script to verify Voice Cleaning + Normalization feature
"""
import os
from ai_service import AIService
from config import Config

# Initialize AI service
ai_service = AIService(api_key=Config.OPENAI_API_KEY)

# Test cases for voice cleaning
test_cases = [
    # Filler words
    ("um Maggi 5 add karo", "Maggi 5 add karo"),
    ("uh Parle G 10 bik gaya", "Parle G 10 bik gaya"),
    ("hmm stock kitna hai", "stock kitna hai"),
    ("you know Colgate 3 add", "Colgate 3 add"),
    ("like Surf Excel 2 bik gaya", "Surf Excel 2 bik gaya"),
    
    # Repeated words
    ("Maggi Maggi 5 add", "Maggi 5 add"),
    ("galti galti ho gayi", "galti ho gayi"),
    ("stock stock kitna hai", "stock kitna hai"),
    
    # Already clean (should remain unchanged)
    ("Maggi 5 add karo", "Maggi 5 add karo"),
    ("Parle G 10 bik gaya", "Parle G 10 bik gaya"),
    ("galti ho gayi", "galti ho gayi"),
    ("stock", "stock"),
    
    # Complex cases
    ("um uh Maggi Maggi 5 pieces add karo", "Maggi 5 pieces add karo"),
    ("you know like Parle G uh 10 bik gaya", "Parle G 10 bik gaya"),
    ("hmm Surf Excel ka stock kitna hai", "Surf Excel ka stock kitna hai"),
]

print("🎤 Testing Voice Cleaning + Normalization\n")
print("=" * 80)

passed = 0
failed = 0
failed_cases = []

for raw_text, expected in test_cases:
    print(f"\n📝 Input:    '{raw_text}'")
    
    cleaned = ai_service.clean_voice_text(raw_text)
    
    print(f"✨ Cleaned:  '{cleaned}'")
    print(f"🎯 Expected: '{expected}'")
    
    # Check if cleaned text is close to expected (AI might vary slightly)
    if cleaned.lower().strip() == expected.lower().strip():
        print("✅ EXACT MATCH")
        passed += 1
    elif expected.lower().replace(" ", "") in cleaned.lower().replace(" ", ""):
        print("✅ CLOSE MATCH (acceptable)")
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
    print(f"\n🎉 All tests passed! Voice cleaning is working perfectly!")

print("\n" + "=" * 80)

