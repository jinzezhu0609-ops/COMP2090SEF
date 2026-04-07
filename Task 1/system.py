import json
from seat import StandardSeat, ComputerSeat
from user import Customer, Admin
DATA_FILE = "user_data.json"

class LibrarySystem: # Main library seat reservation system
    
    def __init__(self):
        self.users = [] # List of all registered users
        self.seats = [] # List of all seats in the library 
        self.reservations = []
        self.current_user = None
        self._init_test_data()
        self.load_users_from_json()

    def _init_test_data(self): # Create seats 1 to 5 for testing 
        self.seats = StandardSeat.create_multiple(1, 3)
        self.seats.extend(ComputerSeat.create_multiple(4, 5))
    
    @staticmethod
    def bubble_sort_seats(seats): # Sort seats by seat_id using bubble sort
        arr = seats.copy()
        n = len(arr)
        for i in range(n-1):
            for j in range(n-i-1):
                if arr[j].seat_id > arr[j+1].seat_id:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    @staticmethod
    def insertion_sort_reservations(reservations): # Sort reservations by start time using insertion sort
        arr = reservations.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i-1
            while j >= 0 and arr[j].start_time > key.start_time:
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key
        return arr

    def logout(self): # Log out current user
        self.current_user = None
        print("Logged out.")

    def find_available_seats(self): # Return list of available seats
        return [s for s in self.seats if s.is_available]
    
    def load_users_from_json(self):
        """Load all user data from the JSON file into system memory"""
        self.users = []     # Clear existing users to avoid duplicates
            
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Reconstruct user objects based on their roles
            for item in data:
                if item.get("role") == "Customer":
                    self.users.append(Customer(item.get("username"), item.get("password")))
                elif item.get("role") == "Admin":
                    self.users.append(Admin(item.get("username"), item.get("password")))
        except Exception:
            pass        # Skip if file doesn't exist or is corrupted

    def save_user_to_json(self, new_user=None):
        """Save a new user to the JSON file (overwrite mode to prevent duplicates)"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            # Convert user objects to dictionaries and save
            data = [u.to_dict() for u in self.users]
            json.dump(data, f, ensure_ascii=False, indent=4)