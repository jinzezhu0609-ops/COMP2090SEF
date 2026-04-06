class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = None   # User role, specified by subclasses

class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password) 
        self.role = "Customer"  # Explicitly set role to customer

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password) 
        self.role = "Admin"    # Explicitly set role to admin
       