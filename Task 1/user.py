from abc import ABC, abstractmethod  # Import abstract 

class User(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = None

    @abstractmethod # Abstract method: must be implemented by subclasses
    def display_menu(self):
        pass

    def __str__(self):
        return f"{self.role}: {self.username}"

    def __repr__(self):
        return f"{self.role}: {self.username}"


class Customer(User): # Customer class inherits from User 
    def __init__(self, username, password):
        super().__init__(username, password) # Call parent class constructor
        self.role = "Customer"

    def display_menu(self): # Display menu for customer operations
        print("\n===== Customer Menu =====")
        print("1. View all seats")
        print("2. Reserve a seat")
        print("3. Release my seat")
        print("4. View my reservations")
        print("5. Logout")


class Admin(User): # Admin class inherits from User
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = "Admin"

    def display_menu(self): # Display menu for admin operations
        print("\n===== Admin Menu =====")
        print("1. View all seats")
        print("2. View all reservations")
        print("3. Send reminders (for upcoming reservations)")
        print("4. Add a new seat")
        print("5. Delete a seat")
        print("6. Logout")
        print("7. Demo user sorting (selection sort)")
    
