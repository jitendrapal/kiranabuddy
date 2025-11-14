"""
Test natural language understanding
"""
from ai_service import AIService
from config import Config
from dotenv import load_dotenv

load_dotenv()

def test_natural_commands():
    """Test various natural language commands"""
    
    print("="*60)
    print("  TESTING NATURAL LANGUAGE UNDERSTANDING")
    print("="*60)
    print()
    
    ai = AIService(api_key=Config.OPENAI_API_KEY)
    
    # Test commands in various natural formats
    test_commands = [
        # Add stock - natural variations
        "I bought 10 Maggi packets today",
        "Got 5 oil bottles from supplier",
        "20 kg atta ka stock aaya",
        "Received 15 biscuit packets",
        "New stock: 30 cold drinks",
        "Aaj 100 sabun aaye hain",
        
        # Reduce stock - natural variations
        "Sold 2 oil bottles to customer",
        "Customer ne 3 Maggi liya",
        "Bech diya 7 biscuit",
        "5 cold drink nikala",
        "Customer ko 10 atta diya",
        
        # Check stock - natural variations
        "How much atta stock do we have?",
        "Maggi kitna bacha hai?",
        "Oil ka stock batao",
        "What's the biscuit count?",
        "Cold drink inventory check karo",
        
        # Mixed/complex
        "Today I sold 5 Maggi and 3 oil",
        "Kitna Maggi hai? Check karo",
        "Customer ne bola 10 atta chahiye, kitna hai?",
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"{i}. Testing: '{command}'")
        
        try:
            result = ai.parse_command(command)
            
            if result.is_valid():
                print(f"   ✅ Understood!")
                print(f"      Action: {result.action.value}")
                print(f"      Product: {result.product_name}")
                if result.quantity:
                    print(f"      Quantity: {result.quantity}")
                print(f"      Confidence: {result.confidence:.2f}")
            else:
                print(f"   ❌ Could not understand")
                print(f"      Action: {result.action.value}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("="*60)
    print("  TEST COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    test_natural_commands()

