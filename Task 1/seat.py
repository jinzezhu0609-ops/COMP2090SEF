class Seat:
    def __init__(self, seat_id):
        self.seat_id = seat_id
        self.is_available = True
        self.reserved_by = None # User who reserved the seat
        self.reservation = None # Reservation object associated with this seat

    @classmethod
    def create_multiple(cls, start_id, end_id): # Create a list of Seat objects in a range of seat IDs
        seats = []
        for seat_id in range(start_id, end_id + 1):
            seats.append(cls(seat_id))
        return seats

    def __str__(self):
        if self.is_available:
            status = "Available"
        else:
            status = f"Reserved by {self.reserved_by.username}"
        return f"Seat {self.seat_id}: {status}"


    def __repr__(self):
        return f"Seat({self.seat_id}, available={self.is_available})"

    def __eq__(self, other):
        return isinstance(other, Seat) and self.seat_id == other.seat_id

    def __lt__(self, other): # Compare seats by seat_id for sorting

        return self.seat_id < other.seat_id
