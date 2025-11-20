"""
Test to see how "do" is being converted in different contexts
"""
from ai_service import AIService
from config import Config

ai_service = AIService(api_key=Config.OPENAI_API_KEY)

# Test cases showing what Whisper might return
test_cases = [
    # What Whisper might transcribe when you say "Maggi do add kar do"
    ("Maggi do add kar do", "Maggi 2 add kar do"),  # Expected: convert first "do" only
    ("Maggi do add", "Maggi 2 add"),  # Expected: convert "do"
    ("add kar do", "add kar do"),  # Expected: don't convert "do" at end
    ("Maggi do bik gaya", "Maggi 2 bik gaya"),  # Expected: convert "do"
    ("do Maggi add", "do Maggi add"),  # Expected: don't convert "do" at start
    ("Maggi 2 add kar do", "Maggi 2 add kar do"),  # Already has number
    
    # Edge cases
    ("do add", "2 add"),  # "do" followed by "add"
    ("do bik", "2 bik"),  # "do" followed by "bik"
    ("kar do", "kar do"),  # "do" at end (command suffix)
    ("karo do", "karo do"),  # "do" at end
]

print("=" * 80)
print("Testing 'do' → '2' conversion")
print("=" * 80)

passed = 0
failed = 0

for i, (input_text, expected_output) in enumerate(test_cases, 1):
    cleaned = ai_service.clean_voice_text(input_text)
    
    status = "✅ PASS" if cleaned == expected_output else "❌ FAIL"
    if cleaned == expected_output:
        passed += 1
    else:
        failed += 1
    
    print(f"\nTest {i}: {status}")
    print(f"  Input:    '{input_text}'")
    print(f"  Expected: '{expected_output}'")
    print(f"  Got:      '{cleaned}'")
    
    if cleaned != expected_output:
        print(f"  ⚠️ MISMATCH!")

print("\n" + "=" * 80)
print(f"Results: {passed}/{len(test_cases)} passed, {failed}/{len(test_cases)} failed")
print("=" * 80)

# Now test the actual parsing
print("\n" + "=" * 80)
print("Testing full command parsing")
print("=" * 80)

test_commands = [
    "Maggi do add kar do",
    "Maggi do add",
    "Maggi do bik gaya",
]

for cmd in test_commands:
    print(f"\n📝 Command: '{cmd}'")
    cleaned = ai_service.clean_voice_text(cmd)
    print(f"   Cleaned: '{cleaned}'")
    
    parsed = ai_service.parse_command(cleaned)
    print(f"   Parsed: {parsed.action.name}, '{parsed.product_name}', {parsed.quantity}")

