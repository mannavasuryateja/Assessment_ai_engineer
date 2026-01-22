#!/usr/bin/env python
"""
Test suite for enhanced booking flow with validation
Tests input validation, dynamic switching, and error handling
"""

from app.booking_flow import (
    initialize_booking_state,
    validate_name,
    validate_email,
    validate_phone,
    validate_room_type,
    validate_date,
    validate_checkout_after_checkin,
    next_question,
    update_state_from_input,
)

def test_validation():
    """Test all validation functions"""
    print("=" * 60)
    print("VALIDATION TESTS")
    print("=" * 60)
    
    # Name validation
    print("\n✓ NAME VALIDATION:")
    assert validate_name("John Smith")[0] == True, "Valid name failed"
    assert validate_name("J")[0] == False, "Short name should fail"
    assert validate_name("John123")[0] == False, "Name with numbers should fail"
    print("  ✅ All name tests passed")
    
    # Email validation
    print("\n✓ EMAIL VALIDATION:")
    assert validate_email("user@example.com")[0] == True, "Valid email failed"
    assert validate_email("invalid@")[0] == False, "Invalid email should fail"
    assert validate_email("user@domain")[0] == False, "Email without TLD should fail"
    print("  ✅ All email tests passed")
    
    # Phone validation
    print("\n✓ PHONE VALIDATION:")
    assert validate_phone("1234567")[0] == True, "7-digit phone should work"
    assert validate_phone("123-456-7890")[0] == True, "Formatted phone should work"
    assert validate_phone("+1 (555) 123-4567")[0] == True, "Complex format should work"
    assert validate_phone("call me")[0] == False, "Non-numeric should fail"
    assert validate_phone("123")[0] == False, "Too few digits should fail"
    print("  ✅ All phone tests passed")
    
    # Room type validation
    print("\n✓ ROOM TYPE VALIDATION:")
    assert validate_room_type("Standard")[0] == True, "Standard should work"
    assert validate_room_type("deluxe")[0] == True, "Case-insensitive should work"
    assert validate_room_type("Suite")[0] == True, "Suite should work"
    assert validate_room_type("Penthouse")[0] == False, "Invalid room should fail"
    print("  ✅ All room type tests passed")
    
    # Date validation
    print("\n✓ DATE VALIDATION:")
    assert validate_date("2026-01-25")[0] == True, "Valid date should work"
    assert validate_date("2026/01/25")[0] == False, "Wrong format should fail"
    assert validate_date("01-25-2026")[0] == False, "Wrong format should fail"
    assert validate_date("2026-13-01")[0] == False, "Invalid month should fail"
    print("  ✅ All date tests passed")
    
    # Checkout after checkin
    print("\n✓ DATE RANGE VALIDATION:")
    state = {
        "check_in": "2026-01-25",
        "check_out": "2026-01-27"
    }
    assert validate_checkout_after_checkin(state)[0] == True, "Valid range should work"
    
    state["check_out"] = "2026-01-25"
    assert validate_checkout_after_checkin(state)[0] == False, "Same date should fail"
    
    state["check_out"] = "2026-01-24"
    assert validate_checkout_after_checkin(state)[0] == False, "Earlier date should fail"
    print("  ✅ All date range tests passed")


def test_booking_flow():
    """Test booking state management"""
    print("\n" + "=" * 60)
    print("BOOKING FLOW TESTS")
    print("=" * 60)
    
    state = initialize_booking_state()
    
    # Test field collection
    print("\n✓ FIELD COLLECTION:")
    q1 = next_question(state)
    assert "name" in q1.lower(), "Should ask for name first"
    print(f"  Q1: {q1}")
    
    # Valid name input
    success, error, _ = update_state_from_input(state, "John Smith")
    assert success == True, "Valid name should succeed"
    assert state["name"] == "John Smith", "Name should be stored"
    print("  ✅ Name accepted")
    
    # Valid email
    q2 = next_question(state)
    assert "email" in q2.lower(), "Should ask for email next"
    success, error, _ = update_state_from_input(state, "john@example.com")
    assert success == True, "Valid email should succeed"
    assert state["email"] == "john@example.com", "Email should be stored"
    print("  ✅ Email accepted")
    
    print("\n✓ FULL BOOKING SEQUENCE:")
    inputs = [
        ("1234567890", "phone"),
        ("Deluxe", "room_type"),
        ("2026-02-01", "check_in"),
        ("2026-02-05", "check_out"),
    ]
    
    for user_input, field_name in inputs:
        # Set current field by calling next_question
        next_question(state)
        success, error, _ = update_state_from_input(state, user_input)
        assert success == True, f"{field_name} should be valid: {error}"
        print(f"  ✅ {field_name.upper()}: {user_input} accepted")
    
    # Verify all fields collected
    assert state["phone"] == "1234567890"
    assert state["room_type"] == "deluxe"
    assert state["check_in"] == "2026-02-01"
    assert state["check_out"] == "2026-02-05"
    print("\n  ✅ All fields collected successfully")


def test_invalid_inputs():
    """Test error handling for invalid inputs"""
    print("\n" + "=" * 60)
    print("INVALID INPUT HANDLING")
    print("=" * 60)
    
    state = initialize_booking_state()
    
    # Test invalid name
    print("\n✓ INVALID NAME:")
    invalid_names = ["A", "John123", "123!@#"]
    for name in invalid_names:
        next_question(state)  # Set current_field
        success, error, _ = update_state_from_input(state, name)
        assert success == False, f"{name} should be rejected"
        print(f"  ✅ Rejected: {name} - {error}")
    
    # Set valid name for next tests
    next_question(state)
    update_state_from_input(state, "John Smith")
    
    # Test invalid email
    print("\n✓ INVALID EMAIL:")
    invalid_emails = ["invalid", "user@", "@example.com"]
    for email in invalid_emails:
        next_question(state)  # Set current_field
        success, error, _ = update_state_from_input(state, email)
        assert success == False, f"{email} should be rejected"
        print(f"  ✅ Rejected: {email}")
    
    # Set valid email
    next_question(state)
    update_state_from_input(state, "john@example.com")
    
    # Test invalid phone
    print("\n✓ INVALID PHONE:")
    invalid_phones = ["123", "call me", "abcdefg"]
    for phone in invalid_phones:
        next_question(state)  # Set current_field
        success, error, _ = update_state_from_input(state, phone)
        assert success == False, f"{phone} should be rejected"
        print(f"  ✅ Rejected: {phone}")
    
    print("\n✅ All validation tests passed!")


if __name__ == "__main__":
    try:
        test_validation()
        test_booking_flow()
        test_invalid_inputs()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        exit(1)
