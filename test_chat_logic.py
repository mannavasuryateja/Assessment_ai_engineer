from app.chat_logic import initialize_chat_state, handle_user_message

def test_booking_flow():
    """Test complete booking flow through chat logic"""
    state = initialize_chat_state()

    # Test booking initiation
    result = handle_user_message(state, "I want to book a room")
    assert result is not None
    
    # Test name input
    result = handle_user_message(state, "Rahul Sharma")
    assert result is not None
    
    # Test email input
    result = handle_user_message(state, "rahul@gmail.com")
    assert result is not None
    
    # Test phone input
    result = handle_user_message(state, "9876543210")
    assert result is not None
    
    # Test room type
    result = handle_user_message(state, "Deluxe")
    assert result is not None
    
    # Test check-in
    result = handle_user_message(state, "2026-01-22")
    assert result is not None
    
    # Test check-out
    result = handle_user_message(state, "2026-01-24")
    assert result is not None
    
    # Test confirmation
    result = handle_user_message(state, "confirm")
    assert result is not None

def test_greeting_detection():
    """Test greeting detection and response"""
    state = initialize_chat_state()
    
    # Test various greetings
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    
    for greeting in greetings:
        state = initialize_chat_state()  # Reset state
        result = handle_user_message(state, greeting)
        assert result is not None, f"Failed for greeting: {greeting}"
        # Check for presence of hotel/service-related keywords
        response_lower = result.lower()
        assert any(word in response_lower for word in ["welcome", "greetings", "pleasure", "hospitality", "delighted", "assist", "service"]), \
            f"Response doesn't contain hotel greeting keywords for: {greeting}. Got: {result[:50]}..."

def test_exit_command():
    """Test exit command during booking"""
    state = initialize_chat_state()
    handle_user_message(state, "I want to book a room")
    
    # Test exit command
    result = handle_user_message(state, "back")
    assert result is not None
    assert "exited" in result.lower() or "exit" in result.lower()

if __name__ == "__main__":
    test_booking_flow()
    test_greeting_detection()
    test_exit_command()
    print("All tests passed!")

