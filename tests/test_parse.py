"""
Tests for Kirana Shop Management App
"""
import pytest
from models import CommandAction, ParsedCommand


def test_parsed_command_validation():
    """Test ParsedCommand validation"""
    # Valid add_stock command
    cmd = ParsedCommand(
        action=CommandAction.ADD_STOCK,
        product_name="Maggi",
        quantity=10
    )
    assert cmd.is_valid() == True

    # Valid reduce_stock command
    cmd = ParsedCommand(
        action=CommandAction.REDUCE_STOCK,
        product_name="Oil",
        quantity=2
    )
    assert cmd.is_valid() == True

    # Valid check_stock command
    cmd = ParsedCommand(
        action=CommandAction.CHECK_STOCK,
        product_name="Atta"
    )
    assert cmd.is_valid() == True

    # Invalid - missing product name
    cmd = ParsedCommand(
        action=CommandAction.ADD_STOCK,
        quantity=10
    )
    assert cmd.is_valid() == False

    # Invalid - missing quantity for add_stock
    cmd = ParsedCommand(
        action=CommandAction.ADD_STOCK,
        product_name="Maggi"
    )
    assert cmd.is_valid() == False

    # Invalid - zero quantity
    cmd = ParsedCommand(
        action=CommandAction.ADD_STOCK,
        product_name="Maggi",
        quantity=0
    )
    assert cmd.is_valid() == False


def test_command_action_enum():
    """Test CommandAction enum"""
    assert CommandAction.ADD_STOCK.value == "add_stock"
    assert CommandAction.REDUCE_STOCK.value == "reduce_stock"
    assert CommandAction.CHECK_STOCK.value == "check_stock"
    assert CommandAction.UNKNOWN.value == "unknown"


# Note: To test AI parsing, you need to set OPENAI_API_KEY in environment
# Uncomment and run these tests only when you have API access

# def test_ai_parse_add_stock():
#     """Test AI parsing for add stock command"""
#     from ai_service import AIService
#     import os
#
#     ai = AIService(api_key=os.getenv('OPENAI_API_KEY'))
#     result = ai.parse_command("Add 10 Maggi")
#
#     assert result.action == CommandAction.ADD_STOCK
#     assert result.product_name.lower() == "maggi"
#     assert result.quantity == 10
#     assert result.is_valid() == True

# def test_ai_parse_reduce_stock():
#     """Test AI parsing for reduce stock command"""
#     from ai_service import AIService
#     import os
#
#     ai = AIService(api_key=os.getenv('OPENAI_API_KEY'))
#     result = ai.parse_command("2 oil sold")
#
#     assert result.action == CommandAction.REDUCE_STOCK
#     assert result.product_name.lower() == "oil"
#     assert result.quantity == 2
#     assert result.is_valid() == True

# def test_ai_parse_check_stock():
#     """Test AI parsing for check stock command"""
#     from ai_service import AIService
#     import os
#
#     ai = AIService(api_key=os.getenv('OPENAI_API_KEY'))
#     result = ai.parse_command("Kitna stock hai atta?")
#
#     assert result.action == CommandAction.CHECK_STOCK
#     assert result.product_name.lower() == "atta"
#     assert result.is_valid() == True
