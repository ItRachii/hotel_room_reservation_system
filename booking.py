import random
import streamlit as st
import pandas as pd
import time

def generate_occupancy():
    """Generate random occupancy for all rooms in the hotel."""
    occupancy = {}
    # Floors 1-9: 10 rooms each
    for floor in range(1, 10):
        for room in range(1, 11):
            room_number = floor * 100 + room
            occupancy[room_number] = random.choice([True, False])
    # Floor 10: 7 rooms
    for room in range(1, 8):
        room_number = 1000 + room
        occupancy[room_number] = random.choice([True, False])
    return occupancy

def get_available_rooms_by_floor(occupancy):
    """Get dictionary of available rooms grouped by floor."""
    available_rooms = {}
    for room, is_occupied in occupancy.items():
        if not is_occupied:
            floor = room // 100
            room_pos = room % 100
            if floor not in available_rooms:
                available_rooms[floor] = []
            available_rooms[floor].append(room_pos)
    # Sort rooms on each floor
    for floor in available_rooms:
        available_rooms[floor].sort()
    return available_rooms

def calculate_travel_time(rooms):
    """Calculate horizontal travel time between rooms on the same floor."""
    if not rooms:
        return 0
    # Horizontal travel time is the difference between first and last room
    return max(rooms) - min(rooms)

def calculate_total_travel_time(room_combination):
    """Calculate total travel time including vertical and horizontal components."""
    if not room_combination:
        return float('inf')
    
    # Extract floors and positions
    floors = [room[0] for room in room_combination]
    positions = [room[1] for room in room_combination]
    
    # Calculate vertical travel time (2 minutes per floor)
    vertical_time = (max(floors) - min(floors)) * 2
    
    # Calculate horizontal travel on each floor
    horizontal_times = {}
    for floor, pos in room_combination:
        if floor not in horizontal_times:
            horizontal_times[floor] = []
        horizontal_times[floor].append(pos)
    
    # Sum the max horizontal distance on each floor
    horizontal_time = 0
    for floor, positions in horizontal_times.items():
        if positions:
            horizontal_time += max(positions) - min(positions)
    
    # Return combined travel time
    return vertical_time + horizontal_time

def find_best_room_combination(available_rooms, num_rooms):
    """Find the best combination of rooms based on travel time."""
    # First try booking on the same floor
    best_same_floor = None
    min_same_floor_time = float('inf')
    
    for floor, positions in available_rooms.items():
        if len(positions) >= num_rooms:
            # Try different consecutive combinations of num_rooms from positions
            for i in range(len(positions) - num_rooms + 1):
                selected_positions = positions[i:i+num_rooms]
                travel_time = calculate_travel_time(selected_positions)
                
                if travel_time < min_same_floor_time:
                    min_same_floor_time = travel_time
                    best_same_floor = [(floor, pos) for pos in selected_positions]
    
    # If found on same floor, return this combination
    if best_same_floor:
        return best_same_floor, min_same_floor_time
    
    # If not found on same floor, try combinations across floors
    all_room_options = []
    for floor, positions in available_rooms.items():
        for pos in positions:
            all_room_options.append((floor, pos))
    
    # Try all possible combinations of num_rooms
    from itertools import combinations
    best_combination = None
    min_travel_time = float('inf')
    
    for combo in combinations(all_room_options, num_rooms):
        travel_time = calculate_total_travel_time(combo)
        if travel_time < min_travel_time:
            min_travel_time = travel_time
            best_combination = combo
    
    return best_combination, min_travel_time

def book_rooms(available_rooms, num_rooms):
    """Book the best combination of rooms."""
    best_combination, travel_time = find_best_room_combination(available_rooms, num_rooms)
    
    # Book the selected rooms (remove them from available rooms)
    if best_combination:
        for floor, pos in best_combination:
            available_rooms[floor].remove(pos)
            # If a floor has no more available rooms, remove it
            if not available_rooms[floor]:
                available_rooms.pop(floor)
                
        # Convert position to full room numbers
        booked_room_numbers = [(floor, floor * 100 + pos) for floor, pos in best_combination]
        return booked_room_numbers, travel_time
    
    return None, float('inf')

def visualize_hotel(occupancy, booked_rooms=None, selected_rooms=None):
    """Create visualization of hotel with room status."""
    if booked_rooms is None:
        booked_rooms = []
    if selected_rooms is None:
        selected_rooms = []
    
    # Mark booked rooms as occupied in the occupancy dictionary
    for _, room_number in booked_rooms:
        occupancy[room_number] = True

    # Extract just the room numbers from booked_rooms list of tuples
    booked_room_numbers = [room[1] for room in booked_rooms]
    selected_room_numbers = [room[1] for room in selected_rooms]
    
    # Add a legend
    legend_html = """
    <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background-color: #ffffff; border: 3px solid #4CAF50; margin-right: 5px;"></div>
            <span style="color: white;">Available</span>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background-color: #d3d3d3; margin-right: 5px;"></div>
            <span style="color: white;">Occupied</span>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background-color: #4CAF50; color: black; font-weight: bold; margin-right: 5px;"></div>
            <span style="color: white;">Currently Selected</span>
        </div>
    </div>
    """
    st.markdown(legend_html, unsafe_allow_html=True)
    
    # Set up CSS for the grid
    st.markdown("""
    <style>
    .hotel-grid {
        display: grid;
        grid-template-columns: 80px repeat(10, 1fr);
        grid-gap: 5px;
        margin-bottom: 20px;
    }
    .hotel-cell {
        padding: 10px 5px;
        text-align: center;
        background-color: #f0f0f0;
        border-radius: 5px;
        font-weight: normal; /* Change from bold to normal */
    }
    .floor-label {
        background-color: #333;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .diagonal-header {
        background-color: #333;
        color: white;
        position: relative;
        overflow: hidden;
        padding: 5px;  /* Add padding for better spacing */
    }
    .diagonal-header:after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(to bottom left, transparent calc(50% - 1px), white, transparent calc(50% + 1px));
        z-index: 1;
    }
    .diagonal-header .bottom-left {
        position: absolute;
        bottom: 5px;  /* Adjust spacing */
        left: 5px;    /* Adjust spacing */
        font-size: 12px;  /* Reduce font size */
        z-index: 2;
    }
    .diagonal-header .top-right {
        position: absolute;
        top: 5px;     /* Adjust spacing */
        right: 5px;   /* Adjust spacing */
        font-size: 12px;  /* Reduce font size */
        z-index: 2;
    }
    .room-header {
        background-color: #333;
        color: white;
    }
    .room-available {
        background-color: #ffffff; /* White background */
        color: #4CAF50; /* Green font */
        border: 3px solid #4CAF50; /* Green border */
    }
    .room-occupied {
        background-color: #d3d3d3; /* Light grey background */
        color: white; /* White font */
    }
    .room-booked {
        background-color: #d3d3d3;
        color: white;
    }
    .room-selected {
        background-color: #4CAF50;
        color: black;
        font-weight: bold; /* Make selected room text bold */
    }
    .room-empty {
        background-color: transparent;
        color: transparent;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the grid as HTML
    html = '<div class="hotel-grid">'
    
    # Header row with room numbers
    html += '<div class="hotel-cell diagonal-header"><span class="bottom-left">Floor</span><span class="top-right">Room</span></div>'
    for i in range(1, 11):
        html += f'<div class="hotel-cell room-header">{i}</div>'
    
    # Create rows for floors (top to bottom: 10 down to 1)
    for floor in range(10, 0, -1):
        # Floor label
        html += f'<div class="hotel-cell floor-label">{floor}</div>'
        
        # Determine number of rooms for this floor (7 for floor 10, 10 for others)
        num_rooms = 7 if floor == 10 else 10
        
        # Rooms for this floor
        for room_pos in range(1, 11):
            room_number = floor * 100 + room_pos
            
            if room_pos <= num_rooms:  # Only show cells for rooms that exist
                # Determine room status and CSS class
                if room_number in selected_room_numbers:
                    status_class = "room-selected"
                elif room_number in booked_room_numbers:
                    status_class = "room-booked"
                elif occupancy.get(room_number, False):
                    status_class = "room-occupied"
                else:
                    status_class = "room-available"
                
                html += f'<div class="hotel-cell {status_class}">{room_number}</div>'
            else:
                # Empty cell for non-existent rooms on floor 10
                html += '<div class="hotel-cell room-empty">-</div>'
    
    html += '</div>'
    
    # Display the grid
    st.markdown(html, unsafe_allow_html=True)

# Streamlit UI
def main():
    st.title("Hotel Room Reservation System")
    st.markdown("""
    <style>
    .stTextInput > div {
        margin-top: -20px;
    }
    .stTextInput > div > div > input, .stButton > button {
        height: 50px;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "occupancy" not in st.session_state:
        st.session_state.occupancy = None
        st.session_state.available_rooms = None
        st.session_state.booked_rooms = []
        st.session_state.last_selected_rooms = []
        st.session_state.booking_history = []
    
    # Layout for input and buttons
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        num_rooms = st.text_input("Number of Rooms", placeholder="Enter number of rooms", label_visibility="hidden")
    
    with col2:
        if st.button("Book Room"):
            if not num_rooms.isdigit() or int(num_rooms) < 1 or int(num_rooms) > 5:
                st.toast("Please enter a valid number between 1 and 5.", icon="❌")
            elif st.session_state.available_rooms:
                selected_rooms, travel_time = book_rooms(st.session_state.available_rooms, int(num_rooms))
                if selected_rooms:
                    # Generate a booking ID
                    booking_id = len(st.session_state.booking_history) + 1
                    
                    # Store this booking
                    st.session_state.booking_history.append({
                        "id": booking_id,
                        "rooms": selected_rooms,
                        "travel_time": travel_time
                    })
                    
                    st.session_state.last_selected_rooms = selected_rooms
                    st.session_state.booked_rooms.extend(selected_rooms)
                    room_numbers = [room[1] for room in selected_rooms]
                    st.toast(f"Successfully booked {len(selected_rooms)} room(s): {room_numbers}", icon="✅")
                    st.toast(f"Total travel time between rooms: {travel_time} minutes", icon="ℹ️")
                else:
                    st.toast("Not enough rooms available to fulfill your request.", icon="❌")
            else:
                st.toast("Please generate room occupancy first.", icon="❌")
    
    with col3:
        if st.button("Reset Booking"):
            # Reset the occupancy for booked and selected rooms
            for _, room_number in st.session_state.booked_rooms:
                st.session_state.occupancy[room_number] = False
            for _, room_number in st.session_state.last_selected_rooms:
                st.session_state.occupancy[room_number] = False
            
            # Clear the session state for booked and selected rooms
            st.session_state.booked_rooms = []
            st.session_state.last_selected_rooms = []
            st.session_state.booking_history = []
            st.session_state.text_input_value = ""
            
            st.toast("Booking reset successfully.", icon="✅")
    
    with col4:
        if st.button("Generate Random Occupancy"):
            st.session_state.occupancy = generate_occupancy()
            st.session_state.available_rooms = get_available_rooms_by_floor(st.session_state.occupancy)
            st.session_state.booked_rooms = []
            st.session_state.last_selected_rooms = []
            st.session_state.booking_history = []
            st.session_state.text_input_value = ""
            st.toast("Random occupancy generated successfully.", icon="✅")
    
    # Display hotel visualization
    if st.session_state.occupancy:
        st.subheader("Hotel Layout & Room Status")
        visualize_hotel(
            st.session_state.occupancy, 
            st.session_state.booked_rooms, 
            st.session_state.last_selected_rooms
        )
        
        # Display booking history
        if st.session_state.booking_history:
            st.subheader("Booking History")
            
            for booking in st.session_state.booking_history:
                with st.expander(f"Booking #{booking['id']} - {len(booking['rooms'])} rooms - Travel Time: {booking['travel_time']} min"):
                    # Create a table of the booked rooms
                    rooms_data = []
                    for floor, room in booking['rooms']:
                        rooms_data.append({
                            "Floor": floor,
                            "Room": room
                        })
                    
                    if rooms_data:
                        # Convert to DataFrame and adjust index
                        df = pd.DataFrame(rooms_data)
                        df.index += 1  # Start index from 1
                        df.index.name = "S.No"  # Rename index column
                        st.table(df) 

if __name__ == "__main__":
    main()