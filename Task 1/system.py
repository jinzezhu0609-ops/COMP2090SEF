import datetime
import sys
import json
import os
from user import User, Customer, Admin
from seat import Seat
from reservation import Reservation
from reminder import Reminder
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
        self.seats = Seat.create_multiple(1, 5)
    
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
                
            self.users = [] # Clear existing users to avoid duplicates
            
            for data in user_data_list:
                if data['role'] == "Customer":
                    from user import Customer
                    user = Customer(data['username'], data['password'])
                elif data['role'] == "Admin":
                    from user import Admin
                    user = Admin(data['username'], data['password'])
                else:
                    continue # Skip unknown roles
                self.users.append(user)
            print(f"Loaded {len(self.users)} users from file successfully!")
        except Exception as e:
            print(f"Error loading user data: {e}")

    def save_user_to_json(self, new_user):
        """Save a new user to the JSON file (overwrite mode to prevent duplicates)"""
        # Get the absolute directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, DATA_FILE)
        
        # Read existing data first
        user_data_list = []
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
        return True # Indicates save succeeded

    def update_user_in_json(self, user):
        """Update an existing user in the JSON file (for password changes, etc.)"""
        # Get the absolute directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, DATA_FILE)
        
        # Read existing data
        user_data_list = []
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                user_data_list = json.load(f)
        
        # Find and update the user
        for i, user_data in enumerate(user_data_list):
            if user_data['username'] == user.username:
                user_data['password'] = user.password
                user_data['role'] = user.role
                break
        
        # Rewrite the entire file with updated data
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(user_data_list, f, ensure_ascii=False, indent=4)
        
        print(f"User {user.username} updated in {full_path} successfully!")
        return True

    def delete_user_from_json(self, user):
        """Delete a user from the JSON file"""
        # Get the absolute directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, DATA_FILE)
        
        # Read existing data
        user_data_list = []
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                user_data_list = json.load(f)
        
        # Find and remove the user
        user_data_list = [u for u in user_data_list if u['username'] != user.username]
        
        # Rewrite the entire file with updated data
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(user_data_list, f, ensure_ascii=False, indent=4)
        
        print(f"User {user.username} deleted from {full_path} successfully!")
        return True

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

    @staticmethod
    def selection_sort_users(users): # Sort users by username using selection sort
        arr = users.copy()
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if arr[j].username < arr[min_idx].username:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    def register(self, role): # Register a new user (Customer or Admin)
        username = input("Enter username: ").strip()
        if not username:
            print("Please input valid name")
            return
        for user in self.users:
            if user.username == username:
                print("Username already exists!")
                return
        password = input("Enter password: ").strip()
        if not password:
            print("Please input valid password")
            return
        if role == "customer":
            user = Customer(username, password)
        elif role == "admin":
            user = Admin(username, password)
        else:
            return
        self.users.append(user)
        self.save_user_to_json(user)
        print(f"{role} registered successfully! Please log in.")

    def login(self): # User login with username and password
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        if not username or not password:
            print("Username and Password must not be null")
            return False
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"Welcome back, {user}!")
                return True
        print("Invalid username or password.")
        return False

    def logout(self): # Log out current user
        self.current_user = None
        print("Logged out.")

    def show_all_seats(self): # Display all seats sorted by seat_id
        sorted_seats = self.bubble_sort_seats(self.seats)
        print("\nCurrent seat status :")
        for seat in sorted_seats:
            print(seat)

    def find_available_seats(self): # Return list of available seats
        return [s for s in self.seats if s.is_available]

    def reserve_seat(self, customer): # Allow customer to reserve an available seat
        available = self.find_available_seats()
        if not available:
            print("No available seats at the moment.")
            return

        print("Available seats:")
        for s in available:
            print(s)

        try:
            seat_id = int(input("Enter seat number to reserve: "))
        except ValueError:
            print("Invalid input.")
            return

        seat = next((s for s in self.seats if s.seat_id == seat_id), None)
        if not seat or not seat.is_available:
            print("Seat not available.")
            return

        time_str = input("Enter start time (format 2025-03-04 14:00): ").strip()
        try:
            start_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid time format.")
            return
        if start_time < datetime.datetime.now():
            print("The start time is in the past! Please choose time in the future")
            return

        print("\nChoose reservation duration:")
        print("1. 10 minutes")
        print("2. 20 minutes")
        print("3. 30 minutes")
        print("4. 60 minutes")
        dur_choice = input("Your choice: ").strip()

        duration_map = {
            "1": 10,
            "2": 20,
            "3": 30,
            "4": 60
        }
        duration_minutes = duration_map.get(dur_choice, 30)

        reservation = Reservation(customer, seat, start_time, duration_minutes)
        seat.is_available = False
        seat.reserved_by = customer
        seat.reservation = reservation
        self.reservations.append(reservation)
        print(f"Reservation successful! \n{reservation}")

    def release_seat(self, customer): # Release a reverved seat
        my_res = [r for r in self.reservations if r.user == customer]
        if not my_res:
            print("You have no reservations.")
            return

        print("Your reservations:")
        for i, r in enumerate(my_res, 1):
            status = "Active" if r.is_active() else "Expired"
            print(f"{i}. {r} [{status}]")

        try:
            choice = int(input("Select reservation number to release: ")) - 1
            res = my_res[choice]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return

        seat = res.seat
        seat.is_available = True
        seat.reserved_by = None
        seat.reservation = None
        if res in self.reservations:
            self.reservations.remove(res)
        print(f"Seat {seat.seat_id} released.")

    def show_my_reservations(self, customer): # Show reservations for the current customer
        my_res = [r for r in self.reservations if r.user == customer]
        if not my_res:
            print("You have no reservations.")
            return

        sorted_res = self.insertion_sort_reservations(my_res)
        print("\nYour reservations :")
        for r in sorted_res:
            status = "Active" if r.is_active() else "Expired"
            print(f"{r} [{status}]")

    def show_all_reservations(self): # Admin: show all reservations
        if not self.reservations:
            print("No reservation records.")
            return
        sorted_res = self.insertion_sort_reservations(self.reservations)
        print("\nAll reservation records:")
        for r in sorted_res:
            status = "Active" if r.is_active() else "Expired"
            print(f"{r} [{status}]")

    def admin_send_reminder(self): # Send reminders for upcoming reservations 
        upcoming = [r for r in self.reservations if r.is_active() and 0 < r.time_to_start() <= 600]
        if not upcoming:
            print("No upcoming reservations.")
            return
        print("Sending reminders:")
        for r in upcoming:
            print(f"  {r.user.username}: seat {r.seat.seat_id} starts at {r.start_time.strftime('%H:%M')}")
        print("Reminders sent.")

    def add_seat(self): # Add a new seat 
        new_id = max((s.seat_id for s in self.seats), default=0) + 1
        seat = Seat(new_id)
        self.seats.append(seat)
        print(f"New seat {new_id} added.")

    def delete_seat(self): # Delete an available seat
        self.show_all_seats()
        try:
            seat_id = int(input("Enter seat number to delete: "))
        except ValueError:
            print("Invalid input.")
            return
        seat = next((s for s in self.seats if s.seat_id == seat_id), None)
        if not seat:
            print("Seat does not exist.")
            return
        if not seat.is_available:
            print("Only available seats can be deleted.")
            return
        self.seats.remove(seat)
        print(f"Seat {seat_id} deleted.")

    def check_all_reminders(self):
        msgs = Reminder.check_reminders(self.reservations)
        for msg in msgs:
            print(msg)

    def run(self): # Main program loop
        while True:
            if self.current_user is None:
                print("\n===== Library Seat Reservation System =====")
                print("1. Login")
                print("2. Register as Customer")
                print("3. Register as Admin")
                print("4. Exit")
                choice = input("Choose an option: ").strip()
                if choice == "1":
                    self.login()
                elif choice == "2":
                    self.register("customer")
                elif choice == "3":
                    self.register("admin")
                elif choice == "4":
                    print("Goodbye!")
                    sys.exit(0)
                else:
                    print("Invalid choice.")
            else:
                self.current_user.display_menu()
                cmd = input("Select an action: ").strip()
                if isinstance(self.current_user, Customer):
                    if cmd == "1":
                        self.show_all_seats()
                    elif cmd == "2":
                        self.reserve_seat(self.current_user)
                    elif cmd == "3":
                        self.release_seat(self.current_user)
                    elif cmd == "4":
                        self.show_my_reservations(self.current_user)
                    elif cmd == "5":
                        self.logout()
                    else:
                        print("Invalid command.")
                elif isinstance(self.current_user, Admin):
                    if cmd == "1":
                        self.show_all_seats()
                    elif cmd == "2":
                        self.show_all_reservations()
                    elif cmd == "3":
                        self.admin_send_reminder()
                    elif cmd == "4":
                        self.add_seat()
                    elif cmd == "5":
                        self.delete_seat()
                    elif cmd == "6":
                        self.logout()
                    elif cmd == "7":
                        sorted_users = self.selection_sort_users(self.users)
                        print("\nAll users sorted by username (selection sort):")
                        for u in sorted_users:
                            print(f"  {u.username} ({u.role})")
                    else:
                        print("Invalid command.")

            self.check_all_reminders()
    