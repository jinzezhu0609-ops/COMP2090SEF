# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import datetime
import sys
from typing import List, Optional

# User Module
class User(ABC):
    """Abstract base class for users"""
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.role = None

    @abstractmethod
    def display_menu(self):
        pass

    def __str__(self):
        return f"{self.role}: {self.username}"

    def __repr__(self):
        return f"<{self.role} {self.username}>"


class Customer(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.role = "Customer"

    def display_menu(self):
        print("\n===== Customer Menu =====")
        print("1. View all seats")
        print("2. Reserve a seat")
        print("3. Release my seat")
        print("4. View my reservations")
        print("5. Logout")


class Admin(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.role = "Admin"

    def display_menu(self):
        print("\n===== Admin Menu =====")
        print("1. View all seats")
        print("2. View all reservations")
        print("3. Send reminders (for upcoming reservations)")
        print("4. Add a new seat")
        print("5. Delete a seat")
        print("6. Logout")
        print("7. Demo user sorting (selection sort)")


# Seat Module
class Seat:
    def __init__(self, seat_id: int):
        self.seat_id = seat_id
        self.is_available = True
        self.reserved_by: Optional[Customer] = None
        self.reservation: Optional['Reservation'] = None

    def __str__(self):
        status = "Available" if self.is_available else f"Reserved by {self.reserved_by.username}"
        return f"Seat {self.seat_id}: {status}"

    def __repr__(self):
        return f"Seat({self.seat_id}, available={self.is_available})"

    def __eq__(self, other):
        return isinstance(other, Seat) and self.seat_id == other.seat_id

    def __lt__(self, other):
        return self.seat_id < other.seat_id


# Reservation Module
class Reservation:
    def __init__(self, user: Customer, seat: Seat, start_time: datetime.datetime, duration_minutes: int):
        self.user = user
        self.seat = seat
        self.start_time = start_time
        self.duration_minutes = duration_minutes
        self.end_time = start_time + datetime.timedelta(minutes=duration_minutes)

    def __str__(self):
        return (f"{self.user.username} reserved seat {self.seat.seat_id} "
                f"from {self.start_time.strftime('%Y-%m-%d %H:%M')} "
                f"to {self.end_time.strftime('%Y-%m-%d %H:%M')} "
                f"({self.duration_minutes} min)")

    def __repr__(self):
        return f"Reservation(user={self.user.username}, seat={self.seat.seat_id}, start={self.start_time})"

    def is_active(self):
        return datetime.datetime.now() < self.end_time

    def time_to_start(self):
        diff = self.start_time - datetime.datetime.now()
        return diff.total_seconds() if diff.total_seconds() > 0 else 0

    def time_to_end(self):
        diff = self.end_time - datetime.datetime.now()
        return diff.total_seconds() if diff.total_seconds() > 0 else 0


# Reminder Module ——
class Reminder:
    # 5 minutes reminder
    REMIND_BEFORE_SECONDS = 5 * 60

    @staticmethod
    def check_reminders(reservations: List[Reservation]) -> List[str]:
        msgs = []
        now = datetime.datetime.now()

        for res in reservations:
            if not res.is_active():
                continue

            sec_to_start = res.time_to_start()
            if 0 < sec_to_start <= Reminder.REMIND_BEFORE_SECONDS:
                msgs.append(f"[REMIND] Seat {res.seat.seat_id} will start soon!")

            sec_to_end = res.time_to_end()
            if 0 < sec_to_end <= Reminder.REMIND_BEFORE_SECONDS:
                msgs.append(f"[REMIND] Seat {res.seat.seat_id} will end soon, please prepare to leave.")

        return msgs


# System Management Module
class LibrarySystem:
    def __init__(self):
        self.users: List[User] = []
        self.seats: List[Seat] = []
        self.reservations: List[Reservation] = []
        self.current_user: Optional[User] = None
        self._init_test_data()

    def _init_test_data(self):
        admin = Admin("admin", "123")
        self.users.append(admin)
        cust1 = Customer("alice", "111")
        cust2 = Customer("bob", "222")
        self.users.extend([cust1, cust2])
        for i in range(1, 6):
            self.seats.append(Seat(i))

    @staticmethod
    def bubble_sort_seats(seats: List[Seat]) -> List[Seat]:
        arr = seats.copy()
        n = len(arr)
        for i in range(n-1):
            for j in range(n-i-1):
                if arr[j].seat_id > arr[j+1].seat_id:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    @staticmethod
    def insertion_sort_reservations(reservations: List[Reservation]) -> List[Reservation]:
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
    def selection_sort_users(users: List[User]) -> List[User]:
        arr = users.copy()
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if arr[j].username < arr[min_idx].username:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    def register(self, role: str):
        username = input("Enter username: ").strip()
        if any(u.username == username for u in self.users):
            print("Username already exists!")
            return
        password = input("Enter password: ").strip()
        if role == "customer":
            user = Customer(username, password)
        elif role == "admin":
            user = Admin(username, password)
        else:
            return
        self.users.append(user)
        print(f"{role} registered successfully! Please log in.")

    def login(self) -> bool:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"Welcome back, {user}!")
                return True
        print("Invalid username or password.")
        return False

    def logout(self):
        self.current_user = None
        print("Logged out.")

    def show_all_seats(self):
        sorted_seats = self.bubble_sort_seats(self.seats)
        print("\nCurrent seat status (bubble sort demo):")
        for seat in sorted_seats:
            print(seat)

    def find_available_seats(self) -> List[Seat]:
        return [s for s in self.seats if s.is_available]

    
    def reserve_seat(self, customer: Customer):
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

        # select time 
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

    def release_seat(self, customer: Customer):
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

    def show_my_reservations(self, customer: Customer):
        my_res = [r for r in self.reservations if r.user == customer]
        if not my_res:
            print("You have no reservations.")
            return

        sorted_res = self.insertion_sort_reservations(my_res)
        print("\nYour reservations (sorted by start time):")
        for r in sorted_res:
            status = "Active" if r.is_active() else "Expired"
            print(f"{r} [{status}]")

    def show_all_reservations(self):
        if not self.reservations:
            print("No reservation records.")
            return
        sorted_res = self.insertion_sort_reservations(self.reservations)
        print("\nAll reservation records:")
        for r in sorted_res:
            status = "Active" if r.is_active() else "Expired"
            print(f"{r} [{status}]")

    def admin_send_reminder(self):
        upcoming = [r for r in self.reservations if r.is_active() and 0 < r.time_to_start() <= 1800]
        if not upcoming:
            print("No upcoming reservations.")
            return
        print("Sending reminders:")
        for r in upcoming:
            print(f"  {r.user.username}: seat {r.seat.seat_id} starts at {r.start_time.strftime('%H:%M')}")
        print("Reminders sent.")

    def add_seat(self):
        new_id = max((s.seat_id for s in self.seats), default=0) + 1
        seat = Seat(new_id)
        self.seats.append(seat)
        print(f"New seat {new_id} added.")

    def delete_seat(self):
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

    def run(self):
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
                        print("\n[Demonstration] All users sorted by username (selection sort):")
                        for u in sorted_users:
                            print(f"  {u.username} ({u.role})")
                    else:
                        print("Invalid command.")
                self.check_all_reminders()


if __name__ == "__main__":
    system = LibrarySystem()
    system.run()