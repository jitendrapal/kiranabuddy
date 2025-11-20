"""
Simple test for CHECK_STOCK keyword detection (no API calls)
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_check_keywords():
    """Test that CHECK keywords are detected"""
    
    print("=" * 80)
    print("Testing CHECK_STOCK Keyword Detection")
    print("=" * 80)
    
    # CHECK keywords from ai_service.py
    check_keywords = [
        # Hindi/Hinglish
        'kitna', 'kitne', 'kitni', 'कितना', 'कितने', 'कितनी',
        'dikhao', 'dikha', 'दिखाओ', 'दिखा',
        'batao', 'bata', 'बताओ', 'बता',
        'bachi', 'bacha', 'बची', 'बचा', 'बचे',
        'quantity', 'stock',
        # English
        'check', 'show', 'how much', 'how many',
        'stock check', 'check stock',
        # Phrases
        'ka stock', 'ke packet', 'ki quantity',
    ]
    
    # Test cases
    test_cases = [
        "maggi ka stock dikhao",
        "maggi ke kitne packet hai",
        "maggi kitni bachi hai",
        "maggi kitni hai",
        "maggi ki quantity batao",
        "oil ka stock dikhao",
        "rice kitna hai",
        "atta kitna bacha hai",
        "biscuit ki quantity batao",
        "oil dikhao",
        "rice stock check karo",
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} commands...\n")
    
    passed = 0
    failed = 0
    
    for i, command in enumerate(test_cases, 1):
        command_lower = command.lower()
        
        # Check if any keyword is in the command
        found_keywords = [kw for kw in check_keywords if kw in command_lower]
        
        print(f"Test {i}/{len(test_cases)}: '{command}'")
        
        if found_keywords:
            print(f"  ✅ PASSED - Found keywords: {found_keywords}")
            passed += 1
        else:
            print(f"  ❌ FAILED - No CHECK keywords found")
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
        print("\n🎉 ALL TESTS PASSED! All commands contain CHECK keywords!")
    else:
        print(f"\n⚠️ {failed} test(s) failed.")
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = test_check_keywords()
    exit(0 if failed == 0 else 1)

