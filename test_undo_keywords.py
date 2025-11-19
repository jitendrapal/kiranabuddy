"""
Test script to verify UNDO feature works with new keywords
"""
import os
from ai_service import AIService
from models import CommandAction
from config import Config

# Initialize AI service
ai_service = AIService(api_key=Config.OPENAI_API_KEY)

# Test cases for undo keywords
test_cases = [
    # English
    "undo last entry",
    "undo last action",
    "delete last",
    "remove last",
    "cancel last",
    "wrong entry",
    "mistake",
    "wrong",
    
    # Hinglish
    "galti",
    "galati",
    "galti ho gayi",
    "galati ho gayi",
    "galti ho gai",
    "galati ho gai",
    "undo kar do",
    "undo karo",
    "wapas kar do",
    "wapas karo",
    "hatao",
    "hata do",
    "pichli entry wapas",
    "pichli entry hata do",
    "last wapas",
    "last hatao",
    "galt entry",
    "previous undo",
    "previous wapas",
    
    # Hindi script
    "गलती",
    "गलती हो गई",
    "गलत एंट्री",
    "वापस करो",
    "हटाओ",
    "अंतिम एंट्री वापस लो",
    "आखिरी एंट्री वापस लो",
    "पिछली एंट्री वापस लो",
]

print("🔄 Testing UNDO Feature Keywords\n")
print("=" * 60)

passed = 0
failed = 0
failed_cases = []

for test_message in test_cases:
    parsed = ai_service.parse_command(test_message)
    
    if parsed.action == CommandAction.UNDO_LAST:
        print(f"✅ PASS: '{test_message}'")
        passed += 1
    else:
        print(f"❌ FAIL: '{test_message}' -> {parsed.action.value}")
        failed += 1
        failed_cases.append((test_message, parsed.action.value))

print("\n" + "=" * 60)
print(f"\n📊 Results:")
print(f"   ✅ Passed: {passed}/{len(test_cases)}")
print(f"   ❌ Failed: {failed}/{len(test_cases)}")

if failed > 0:
    print(f"\n❌ Failed cases:")
    for msg, action in failed_cases:
        print(f"   - '{msg}' -> {action}")
else:
    print(f"\n🎉 All tests passed! UNDO feature is working perfectly!")

print("\n" + "=" * 60)

