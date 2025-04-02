# Hotel Room Reservation System

This project implements a room reservation system for a hotel that optimally assigns rooms to guests based on minimizing the travel time between booked rooms. The system dynamically calculates travel times and uses an intelligent algorithm to determine the best possible assignment based on the hotel's layout and booking rules.

---

## Table of Contents

- [Problem Overview](#problem-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Algorithm Details](#algorithm-details)
- [Contributing](#contributing)
- [License](#license)

---

## Problem Overview

The hotel has a total of 97 rooms spread over 10 floors with the following details:

- **Floors 1-9:** Each floor has 10 rooms, sequentially numbered (e.g., Floor 1: 101–110, Floor 2: 201–210, etc.).
- **Floor 10:** Contains 7 rooms, numbered 1001–1007.

### Building Layout

- **Staircase & Lift:**  
  Located on the left side of the building.
  
- **Room Arrangement:**  
  Rooms are arranged sequentially from left to right on each floor, with the first room being closest to the stairs/lift.

### Travel Time Metrics

- **Horizontal Movement:**  
  Moving between adjacent rooms on the same floor takes 1 minute per room.
  
- **Vertical Movement:**  
  Moving between floors using the stairs/lift takes 2 minutes per floor.

### Booking Rules

- **Room Booking Limit:**  
  A guest can book up to 5 rooms at a time.

- **Primary Booking Strategy:**  
  The system first attempts to assign all requested rooms on the same floor to minimize travel time.

- **Secondary Booking Strategy:**  
  If sufficient rooms are not available on a single floor, the system selects rooms across different floors while minimizing the combined vertical and horizontal travel times between the first and last booked room.

#### Example Scenarios

1. **Single-Floor Booking:**  
   - **Available Rooms on Floor 1:** 101, 102, 105, 106  
   - **Guest Request:** 4 rooms  
   - **Result:** All four rooms on Floor 1 are selected, as they minimize the overall travel time.

2. **Multi-Floor Booking:**  
   - **Available Rooms on Floor 1:** Only 101 and 102  
   - **Guest Request:** 4 rooms  
   - **Result:** The system selects 101, 102 from Floor 1 and chooses additional rooms from another floor (e.g., 201, 202 from Floor 2) to minimize vertical (2 minutes per floor) and horizontal travel times.

---

## Features

- **Dynamic Travel Time Calculation:**  
  Computes travel time by considering both horizontal (room-to-room) and vertical (floor-to-floor) movement.

- **Optimal Room Assignment:**  
  Prioritizes booking rooms on the same floor; if not available, selects the combination of rooms that minimizes total travel time.

- **Full Stack Implementation:**  
  - **Backend:** Implements the room assignment and booking logic (e.g., using Flask or Django).
  - **Frontend:** Provides a user-friendly interface (e.g., using React) for checking room availability and making bookings.
  - **Database:** Maintains the status of room availability and updates booking records.

---

## Getting Started

### Prerequisites

- Python 3.x
- Node.js & npm (for frontend development)
- Virtual Environment (optional but recommended)
- Flask or Django (if using a specific web framework for the backend)
