class Flight:
    def __init__(self, flightNumber, destination, distanceKm, baseFarePerKm):
        self.flightNumber = flightNumber
        self.destination = destination
        self.distanceKm = distanceKm
        self.baseFarePerKm = baseFarePerKm

    def calculateFare(self, bookingCategory):
        return self.distanceKm * self.baseFarePerKm * bookingCategory.priceMultiplier

    def displayDetails(self):
        print()
        print(f"Flight Number : {self.flightNumber}")
        print(f"Destination   : {self.destination}")
        print(f"Distance (km) : {self.distanceKm}")
        print(f"Base Fare (per Km)  : ₹{self.baseFarePerKm}")
        print()


class NormalFlight(Flight):
    def calculateFare(self, bookingCategory):
        return super().calculateFare(bookingCategory)

    def displayDetails(self):
        print("Normal Flight")
        super().displayDetails()


class RedEyeFlight(Flight):
    discountRate = 0.10

    def calculateFare(self, bookingCategory):
        fare = super().calculateFare(bookingCategory)
        return fare * (1 - self.discountRate)

    def displayDetails(self):
        print("Red-Eye Flight (10% discount applied)")
        super().displayDetails()
