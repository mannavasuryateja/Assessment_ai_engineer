from app.booking_flow import (
    initialize_booking_state,
    next_question,
    update_state_from_input,
    booking_summary,
    handle_confirmation
)

if __name__ == "__main__":
    state = initialize_booking_state()

    print(next_question(state))      # name
    state = update_state_from_input(state, "Rahul Sharma")

    print(next_question(state))      # email
    state = update_state_from_input(state, "rahul@gmail.com")

    print(next_question(state))      # phone
    state = update_state_from_input(state, "9876543210")

    print(next_question(state))      # room_type
    state = update_state_from_input(state, "Deluxe")

    print(next_question(state))      # check_in
    state = update_state_from_input(state, "2026-01-22")

    print(next_question(state))      # check_out
    state = update_state_from_input(state, "2026-01-24")

    print(booking_summary(state))

print(handle_confirmation(state, "confirm"))
print(state)
