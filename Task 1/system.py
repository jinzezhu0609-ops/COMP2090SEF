import json
import os
from seat import StandardSeat, ComputerSeat
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
        # Get the absolute directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, DATA_FILE)
        
        print(f"Looking for user data at: {full_path}")
        
        if not os.path.exists(full_path):
            print("No user data found, starting fresh.")
            return
            
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                user_data_list = json.load(f)
                
            self.users = []     # Clear existing users to avoid duplicates
            
            # Iterate through the JSON data and reconstruct user objects
            for data in user_data_list:
                if data['role'] == "Customer":
                    from user import Customer
                    user = Customer(data['username'], data['password'])
                elif data['role'] == "Admin":
                    from user import Admin
                    user = Admin(data['username'], data['password'])
                else:
                    continue      # Skip unknown roles
                self.users.append(user)
            print(f"Loaded {len(self.users)} users from file successfully!")
        except Exception as e:
            print(f"Error loading user data: {e}")

    def save_user_to_json(self, new_user):
        """Save a new user to the JSON file (overwrite mode to prevent duplicates)"""
        # Get the absolute directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, DATA_FILE)
        
        user_data_list = []  # Read existing data first
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                user_data_list = json.load(f)
        
        # Check if username already exists (prevent duplicate registrations)
        for user in user_data_list:
            if user['username'] == new_user.username:
                print("Username already exists in file!")
                return False # Indicates save failed
        
        # Append new user data
        user_dict = {
            "username": new_user.username,
            "password": new_user.password,
            "role": new_user.role
        }
        user_data_list.append(user_dict)
        
        # Rewrite the entire file with updated data
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(user_data_list, f, ensure_ascii=False, indent=4)
            
        print(f"User saved to {full_path} successfully!")
        return True          # Indicates save succeeded
