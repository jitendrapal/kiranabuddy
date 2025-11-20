"""
Test script for Unrecognized Command Tracking Feature

This script tests:
1. Saving unrecognized commands to database
2. Retrieving unrecognized commands
3. Marking commands as resolved
4. Deleting commands
"""

from database import FirestoreDB
from config import Config
from datetime import datetime

def test_unrecognized_commands():
    """Test the unrecognized command tracking feature"""

    print("=" * 60)
    print("🧪 Testing Unrecognized Command Tracking Feature")
    print("=" * 60)

    # Initialize database
    db = FirestoreDB(Config.GOOGLE_APPLICATION_CREDENTIALS)
    
    # Get test shop
    test_phone = "9876543210"
    shop = db.get_shop_by_phone(test_phone)
    
    if not shop:
        print(f"❌ No shop found for phone: {test_phone}")
        print("Please create a shop first using the login page")
        return
    
    print(f"\n✅ Found shop: {shop.name} (ID: {shop.shop_id})")
    
    # Test 1: Save unrecognized voice command
    print("\n" + "=" * 60)
    print("Test 1: Save Unrecognized Voice Command")
    print("=" * 60)
    
    try:
        cmd1 = db.save_unrecognized_command(
            shop_id=shop.shop_id,
            user_phone=test_phone,
            message_type="voice",
            raw_text="Maggi do add kar do",
            transcribed_text="Maggi do add kar do",
            cleaned_text="Maggi 2 add kar do",
            parsed_action="ADD_STOCK",
            confidence=0.45,  # Low confidence
        )
        print(f"✅ Saved voice command: {cmd1.command_id}")
        print(f"   Raw: {cmd1.raw_text}")
        print(f"   Transcribed: {cmd1.transcribed_text}")
        print(f"   Cleaned: {cmd1.cleaned_text}")
        print(f"   Confidence: {cmd1.confidence * 100}%")
    except Exception as e:
        print(f"❌ Error saving voice command: {e}")
        return
    
    # Test 2: Save unrecognized text command
    print("\n" + "=" * 60)
    print("Test 2: Save Unrecognized Text Command")
    print("=" * 60)
    
    try:
        cmd2 = db.save_unrecognized_command(
            shop_id=shop.shop_id,
            user_phone=test_phone,
            message_type="text",
            raw_text="xyz abc random gibberish",
            parsed_action="UNKNOWN",
            confidence=0.1,
        )
        print(f"✅ Saved text command: {cmd2.command_id}")
        print(f"   Raw: {cmd2.raw_text}")
        print(f"   Action: {cmd2.parsed_action}")
        print(f"   Confidence: {cmd2.confidence * 100}%")
    except Exception as e:
        print(f"❌ Error saving text command: {e}")
        return
    
    # Test 3: Retrieve unrecognized commands
    print("\n" + "=" * 60)
    print("Test 3: Retrieve Unrecognized Commands")
    print("=" * 60)
    
    try:
        commands = db.get_unrecognized_commands(shop_id=shop.shop_id, include_resolved=False)
        print(f"✅ Retrieved {len(commands)} unrecognized commands")
        
        for i, cmd in enumerate(commands[:5], 1):  # Show first 5
            print(f"\n   Command {i}:")
            print(f"   - ID: {cmd.command_id}")
            print(f"   - Type: {cmd.message_type}")
            print(f"   - Text: {cmd.raw_text}")
            print(f"   - Action: {cmd.parsed_action}")
            print(f"   - Confidence: {cmd.confidence * 100:.0f}%")
            print(f"   - Resolved: {cmd.resolved}")
            print(f"   - Time: {cmd.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"❌ Error retrieving commands: {e}")
        return
    
    # Test 4: Mark command as resolved
    print("\n" + "=" * 60)
    print("Test 4: Mark Command as Resolved")
    print("=" * 60)
    
    try:
        success = db.mark_command_resolved(
            command_id=cmd1.command_id,
            resolution_notes="Fixed by improving Hindi number conversion"
        )
        if success:
            print(f"✅ Marked command {cmd1.command_id} as resolved")
        else:
            print(f"❌ Failed to mark command as resolved")
    except Exception as e:
        print(f"❌ Error marking command as resolved: {e}")
    
    # Test 5: Retrieve including resolved
    print("\n" + "=" * 60)
    print("Test 5: Retrieve Including Resolved Commands")
    print("=" * 60)
    
    try:
        all_commands = db.get_unrecognized_commands(shop_id=shop.shop_id, include_resolved=True)
        resolved_count = sum(1 for cmd in all_commands if cmd.resolved)
        unresolved_count = len(all_commands) - resolved_count
        
        print(f"✅ Total commands: {len(all_commands)}")
        print(f"   - Resolved: {resolved_count}")
        print(f"   - Unresolved: {unresolved_count}")
    except Exception as e:
        print(f"❌ Error retrieving all commands: {e}")
    
    # Test 6: Delete command
    print("\n" + "=" * 60)
    print("Test 6: Delete Command")
    print("=" * 60)
    
    try:
        success = db.delete_unrecognized_command(cmd2.command_id)
        if success:
            print(f"✅ Deleted command {cmd2.command_id}")
        else:
            print(f"❌ Failed to delete command")
    except Exception as e:
        print(f"❌ Error deleting command: {e}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("✅ All Tests Completed!")
    print("=" * 60)
    print("\n📊 Next Steps:")
    print("1. Start the Flask app: python app.py")
    print("2. Open browser: http://127.0.0.1:5000/unrecognized_commands")
    print(f"3. Enter shop phone: {test_phone}")
    print("4. Click 'Load' to see unrecognized commands")
    print("\n💡 Try sending some invalid commands via the test chat to see them appear!")


if __name__ == "__main__":
    test_unrecognized_commands()

