from abc import ABC, abstractmethod

class Seat(ABC):
    '''Abstract base class for seats'''
    def __init__(self, seat_id):
        self.seat_id = seat_id     # Seat ID
        self.is_available = True   # Availability status
        self.reserved_by = None    # User who reserved the seat
        self.reservation = None    # Associated reservation record

    @abstractmethod
    def get_seat_type(self):
        '''Abstract method: Returns seat type'''
        pass

    @classmethod
    def create_multiple(cls, start_id, end_id): 
        seats = []
        for seat_id in range(start_id, end_id + 1):
            seats.append(cls(seat_id)) 
        return seats

    def __str__(self):
        '''Returns the current status of the seat'''
        if self.is_available:
            status = "Available"
        else:
            status = f"Reserved by {self.reserved_by.username}"
        return f"[{self.get_seat_type()}] Seat {self.seat_id}: {status}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.seat_id}, available={self.is_available})"

    def __eq__(self, other):
        '''Equal if it is a Seat object with the same seat ID'''
        return isinstance(other, Seat) and self.seat_id == other.seat_id

    def __lt__(self, other): 
        return self.seat_id < other.seat_id

class StandardSeat(Seat):
    '''Standard desk seat'''
    def get_seat_type(self):
        return "Standard Desk" 

class ComputerSeat(Seat):
    '''Seat with a computer'''
    def get_seat_type(self):
        return "Computer Seat" 
