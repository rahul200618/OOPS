# from flight import *
# from booking import *
# from bookingCategory import *

# flights = [
#     NormalFlight("AI101", "Mumbai", 720, 6),
#     NormalFlight("BA202", "Delhi", 1150, 5),
#     RedEyeFlight("UA303", "Dubai", 2000, 8),
#     NormalFlight("AF404", "Bangalore", 950, 7),
#     RedEyeFlight("SQ505", "Singapore", 3900, 10),
#     NormalFlight("LH606", "Frankfurt", 6800, 12),
#     RedEyeFlight("QF707", "Sydney", 10400, 15),
#     NormalFlight("EK808", "Abu Dhabi", 2300, 9),
#     RedEyeFlight("CX909", "Hong Kong", 4200, 11),
#     NormalFlight("JL010", "Tokyo", 6000, 13),
#     RedEyeFlight("AA111", "New York", 12500, 16),
#     NormalFlight("QR212", "Doha", 3200, 10),
#     RedEyeFlight("BA313", "London", 7200, 14),
#     NormalFlight("AI414", "Chennai", 700, 6),
#     RedEyeFlight("SQ515", "Kuala Lumpur", 3600, 10)
# ]

# while True:
#     print("""✈️ Airline Ticket Booking System

# 1. View All Flights
# 2. View Flight Details
# 3. Make a New Booking
# 4. View My Bookings
# 5. Cancel a Booking
# 6. Exit
# """)
    
#     user_input = int(input("Enter the number : "))

#     if user_input == 1:
#         for i in flights:
#             i.displayDetails()

#     elif user_input == 2:
#         flightno = input("Flight ID : ")
#         for i in flights:
#             if i.flightNumber == flightno:
#                 i.displayDetails()
#                 break
    
#     elif user_input == 3:
#         passenger_name = input("Passenger Name : ")
#         flight_id = input("Flight : ")
#         category = input("Category (Economy/Business/Firstclass) : ")
        
from flight import *
from booking import *
from bookingCategory import *

flights = [
    NormalFlight("AI101", "Mumbai", 720, 6),
    NormalFlight("BA202", "Delhi", 1150, 5),
    RedEyeFlight("UA303", "Dubai", 2000, 8),
    NormalFlight("AF404", "Bangalore", 950, 7),
    RedEyeFlight("SQ505", "Singapore", 3900, 10),
]

bookings = []
seatCounter = 1

while True:
    print("""\n✈️ Airline Ticket Booking System

1. View All Flights
2. View Flight Details
3. Make a New Booking
4. View My Bookings
5. Cancel a Booking
6. Exit
""")
    
    user_input = int(input("Enter the number : "))

    if user_input == 1:
        print("\nAll Flights:")
        for i in flights:
            print(f"{i.flightNumber} → {i.destination}")

    elif user_input == 2:
        flightno = input("Enter Flight ID : ")
        found = False
        for i in flights:
            if i.flightNumber == flightno:
                i.displayDetails()
                found = True
                break
        if not found:
            print("❌ Flight not found.")

    elif user_input == 3:
        passenger_name = input("Passenger Name : ")
        flight_id = input("Flight Number : ")
        
        flight = next((f for f in flights if f.flightNumber == flight_id), None)
        if not flight:
            print("❌ Flight not found.")
            continue

        category = input("Category (Economy/Business/Firstclass) : ").strip().lower()

        if category == "economy":
            categoryObj = Economy()
        elif category == "business":
            categoryObj = Business()
        elif category == "firstclass":
            categoryObj = Firstclass()
        else:
            print("❌ Invalid category.")
            continue

        fare = flight.calculateFare(categoryObj)

        # ✅ FIX: use Bookings class
        booking = Bookings(passenger_name, flight, categoryObj, fare, seatCounter)
        bookings.append(booking)

        print(f"✅ Booking successful! Seat Number: {seatCounter}")
        seatCounter += 1

    elif user_input == 4:
        if not bookings:
            print("\n❌ No bookings yet.")
        else:
            print("\n--- My Bookings ---")
            for b in bookings:
                b.displayBookingDetails()

    elif user_input == 5:
        if not bookings:
            print("\n❌ No bookings to cancel.")
            continue

        seat = int(input("Enter Seat Number to cancel: "))
        found = False
        for b in bookings:
            if b.seatNumber == seat:
                bookings.remove(b)
                print(f"✅ Booking with Seat {seat} cancelled.")
                found = True
                break
        if not found:
            print("❌ Booking not found.")

    elif user_input == 6:
        print("Exiting... Thank you for using the system ✈️")
        break

    else:
        print("❌ Invalid option. Try again.")
