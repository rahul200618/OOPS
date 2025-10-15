class Bookings:
        def __init__(self, passengerName, flight, category, ticketCost, seatNumber):
                self.passengerName = passengerName
                self.flight = flight
                self.category = category
                self.ticketCost = ticketCost
                self.seatNumber = seatNumber

        def displayBookingDetails(self):
                print(f"Passenger Name : {self.passengerName}")
                print(f"Flight : {self.flight}")
                print(f"Category : {self.category}")
                print(f"Ticket Cost  : ₹{self.ticketCost}")
                print(f"Seat Number : {self.seatNumber}")
