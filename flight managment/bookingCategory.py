class BookingCategory:
    def __init__(self, name, priceMultiplier):
        self.name = name
        self.priceMultiplier = priceMultiplier

    def calculateprice(self, base_fare):
        return base_fare * self.priceMultiplier


class Economy(BookingCategory):
    def __init__(self):
        super().__init__("Economy", 1)

    def display(self):
        print("Economy benefits: Standard seating, no extras")


class Business(BookingCategory):
    def __init__(self):
        super().__init__("Business", 2)

    def display(self):
        print("Business benefits: Extra legroom, meals, lounge access.")


class Firstclass(BookingCategory):
    def __init__(self):
        super().__init__("Firstclass", 3)

    def display(self):
        print("First class :has luxury seating")

    


    




                        