import tkinter as tk
from tkinter import messagebox, simpledialog 
import datetime

# Import your existing system and classes
from system import LibrarySystem
from user import Customer, Admin
from reservation import Reservation
from seat import StandardSeat
from reminder import Reminder

class LibraryGUI:
    def __init__(self, root):
        '''Initialize main window settings'''
        self.root = root
        self.root.title("Library Seat Reservation System GUI")
        self.root.geometry("600x550") 
        self.root.configure(padx=20, pady=20)

        # Initialize system backend logic       
        self.sys = LibrarySystem()
        self.background_loop_id = None 

        # Show login screen on startup    
        self.show_login_screen()

    def start_background_tasks(self):
        '''refresh countdown and reminders every second'''
        if self.sys.current_user is not None:
            self.update_timer_display()  
            self.check_reminders_gui()   
            self.background_loop_id = self.root.after(1000, self.start_background_tasks)

    def stop_background_tasks(self):
        '''Stop background timer tasks'''
        if self.background_loop_id:
            self.root.after_cancel(self.background_loop_id)
            self.background_loop_id = None

    def clear_screen(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()


    def show_login_screen(self):
        '''login and registration screen'''
        self.clear_screen()
        
        tk.Label(self.root, text="Welcome to the Library Seat Reservation System", font=("Arial", 18, "bold")).pack(pady=30)

        # Username input
        tk.Label(self.root, text="Username:").pack()
        self.entry_username = tk.Entry(self.root, width=30)
        self.entry_username.pack(pady=5)

        # Password input
        tk.Label(self.root, text="Password:").pack()
        self.entry_password = tk.Entry(self.root, show="*", width=30)
        self.entry_password.pack(pady=5)

        tk.Button(self.root, text="Login", width=20, command=self.login, bg="#4CAF50", fg="white").pack(pady=10)

        # Registration button area
        frame_register = tk.Frame(self.root)
        frame_register.pack(pady=10)
        tk.Button(frame_register, text="Register as Customer", command=lambda: self.register("Customer")).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_register, text="Register as Admin", command=lambda: self.register("Admin")).pack(side=tk.LEFT, padx=10)

    def login(self):
        '''Handle login logic and redirect based on role'''
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Username and password cannot be empty!")
            return

        # Iterate through users in the underlying system to verify identity
        for user in self.sys.users:
            if user.username == username and user.password == password:
                self.sys.current_user = user
                if isinstance(user, Customer):
                    self.show_customer_dashboard()
                elif isinstance(user, Admin):
                    self.show_admin_dashboard()
                return
        
        messagebox.showerror("Error", "Invalid username or password.")

    def register(self, role):
        '''Handle new user registration logic'''
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please fill in the username and password you want to register in the input boxes above!")
            return

        # Check if username already exists
        for user in self.sys.users:
            if user.username == username:
                messagebox.showerror("Error", "Username already exists!")
                return

        # Create the corresponding user object
        if role == "Customer":
            new_user = Customer(username, password)
        else:
            new_user = Admin(username, password)

        # Add to the system and save to JSON
        self.sys.users.append(new_user)
        self.sys.save_user_to_json(new_user)
        messagebox.showinfo("Success", f"{role} registered successfully! Please log in.")


    def show_customer_dashboard(self):
        '''Customer dashboard'''
        self.clear_screen()
        tk.Label(self.root, text=f"Customer Dashboard - Welcome {self.sys.current_user.username}", font=("Arial", 16, "bold")).pack(pady=10)
        # Feature menu
        tk.Button(self.root, text="View all seats", width=30, command=self.view_all_seats).pack(pady=5)
        tk.Button(self.root, text="Reserve a seat", width=30, command=self.reserve_seat_gui).pack(pady=5)
        tk.Button(self.root, text="Release my seat", width=30, command=self.release_seat_gui).pack(pady=5)
        tk.Button(self.root, text="View my reservations", width=30, command=self.view_my_reservations).pack(pady=5)
        tk.Button(self.root, text="Logout", width=30, command=self.logout, fg="red").pack(pady=10)
        
        # Real-time countdown display area
        tk.Label(self.root, text="Real-time seat status", font=("Arial", 12, "bold")).pack(pady=5)
        self.timer_frame = tk.Frame(self.root)
        self.timer_frame.pack(pady=5)
        
        self.start_background_tasks() 

    def show_admin_dashboard(self):
        '''Admin dashboard'''
        self.clear_screen()
        tk.Label(self.root, text=f"Admin Dashboard - Welcome {self.sys.current_user.username}", font=("Arial", 16, "bold")).pack(pady=10)
        # Feature menu
        tk.Button(self.root, text="View all seats", width=30, command=self.view_all_seats).pack(pady=5)
        tk.Button(self.root, text="View all reservations", width=30, command=self.view_all_reservations).pack(pady=5)
        tk.Button(self.root, text="Add a new seat", width=30, command=self.add_seat_gui).pack(pady=5)
        tk.Button(self.root, text="Delete an available seat", width=30, command=self.delete_seat_gui).pack(pady=5)
        tk.Button(self.root, text="Logout", width=30, command=self.logout, fg="red").pack(pady=10)
        
        # Real-time global status display area
        tk.Label(self.root, text="Real-time global status", font=("Arial", 12, "bold")).pack(pady=5)
        self.timer_frame = tk.Frame(self.root)
        self.timer_frame.pack(pady=5)
        
        self.start_background_tasks() 

    def logout(self):
        '''Log out and return to login screen'''
        self.stop_background_tasks()
        self.sys.current_user = None
        self.show_login_screen()


    def view_all_seats(self):
        '''Show sorted list of all seats in a popup'''
        # Use underlying bubble sort
        sorted_seats = self.sys.bubble_sort_seats(self.sys.seats)
        seat_info = "\n".join([str(seat) for seat in sorted_seats])
        messagebox.showinfo("Seat Status", seat_info if seat_info else "There are currently no seats.")

    def reserve_seat_gui(self):
        '''Handle seat reservation interactive logic'''
        available_seats = self.sys.find_available_seats()
        if not available_seats:
            messagebox.showinfo("Notice", "There are currently no available seats.")
            return

        # Pop-up window for user input
        seat_id_str = simpledialog.askstring("Reservation", f"Available seats: {[s.seat_id for s in available_seats]}\nPlease enter the seat number you want to reserve:")
        if not seat_id_str: 
            return
        
        try:
            seat_id = int(seat_id_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return

        seat = next((s for s in self.sys.seats if s.seat_id == seat_id), None)
        if not seat or not seat.is_available:
            messagebox.showerror("Error", "This seat does not exist or is not available!")
            return

        time_str = simpledialog.askstring("Reservation", "Enter start time (format: 2025-03-04 14:00):")
        if not time_str: return

        try:
            start_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format!")
            return

        if start_time < datetime.datetime.now():
            messagebox.showerror("Error", "The start time cannot be in the past!")
            return

        duration_str = simpledialog.askstring("Reservation", "Enter reservation duration (e.g., 10, 20, 30, 60 minutes):", initialvalue="30")
        
        if duration_str is None: 
            return

        try:
            duration = int(duration_str)
        except ValueError:
            duration = 30 
            
        # Create reservation record
        reservation = Reservation(self.sys.current_user, seat, start_time, duration)
        seat.is_available = False
        seat.reserved_by = self.sys.current_user
        seat.reservation = reservation
        self.sys.reservations.append(reservation)
        
        messagebox.showinfo("Success", f"Reservation successful!\n{reservation}")

    def release_seat_gui(self):
        '''Release seat reserved by current user'''
        my_res = [r for r in self.sys.reservations if r.user == self.sys.current_user]
        if not my_res:
            messagebox.showinfo("Notice", "You currently have no reservations.")
            return

        # List and let user select reservation to release
        res_list = ""
        for i, r in enumerate(my_res, 1):
            status = "Active" if r.is_active() else "Expired"
            res_list += f"{i}. {r} [{status}]\n"

        choice_str = simpledialog.askstring("Release Seat", f"Your reservations:\n{res_list}\nEnter the reservation number to release (1, 2...):")
        if not choice_str: return

        try:
            choice = int(choice_str) - 1
            res = my_res[choice]
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid selection.")
            return
        
        # Update seat and reservation status
        seat = res.seat
        seat.is_available = True
        seat.reserved_by = None
        seat.reservation = None
        if res in self.sys.reservations:
            self.sys.reservations.remove(res)
            
        messagebox.showinfo("Success", f"Seat {seat.seat_id} has been successfully released.")

    def view_my_reservations(self):
        '''View current user's reservations'''
        my_res = [r for r in self.sys.reservations if r.user == self.sys.current_user]
        if not my_res:
            messagebox.showinfo("My Reservations", "You have no reservation records.")
            return
            
        sorted_res = self.sys.insertion_sort_reservations(my_res)
        res_info = "\n".join([f"{r} [{'Active' if r.is_active() else 'Expired'}]" for r in sorted_res])
        messagebox.showinfo("My Reservations", res_info)

    def view_all_reservations(self):
        '''Admin: View all reservations in the system'''
        if not self.sys.reservations:
            messagebox.showinfo("All Reservations", "There are currently no reservation records.")
            return
        sorted_res = self.sys.insertion_sort_reservations(self.sys.reservations)
        res_info = "\n".join([f"{r} [{'Active' if r.is_active() else 'Expired'}]" for r in sorted_res])
        messagebox.showinfo("All Reservations", res_info)

    def add_seat_gui(self):
        '''Admin: Add a new standard seat'''
        new_id = max((s.seat_id for s in self.sys.seats), default=0) + 1
        seat = StandardSeat(new_id) 
        self.sys.seats.append(seat)
        messagebox.showinfo("Success", f"New standard seat {new_id} added successfully.")

    def delete_seat_gui(self):
        '''Admin: Delete an unreserved seat'''
        seat_id_str = simpledialog.askstring("Delete Seat", "Enter the seat number to delete:")
        if not seat_id_str: return
        try:
            seat_id = int(seat_id_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")
            return
            
        seat = next((s for s in self.sys.seats if s.seat_id == seat_id), None)
        if not seat:
            messagebox.showerror("Error", "Seat does not exist.")
            return
        if not seat.is_available:
            messagebox.showerror("Error", "Only available seats can be deleted.")
            return
            
        self.sys.seats.remove(seat)
        messagebox.showinfo("Success", f"Seat {seat_id} deleted.")

    def check_reminders_gui(self):
        '''Call reminder module, check and popup notifications'''
        if not self.sys.current_user:
            return
        if isinstance(self.sys.current_user, Customer):
            target_reservations = [r for r in self.sys.reservations if r.user == self.sys.current_user]
        else:
            target_reservations = self.sys.reservations
        msgs = Reminder.check_reminders(target_reservations)
        if msgs:
            msg_text = "\n".join(msgs)
            messagebox.showinfo("System Reminder", msg_text)
    
    def update_timer_display(self):
        if not self.sys.current_user or not hasattr(self, 'timer_frame'):
            return
        # Clear old text before refreshing 
        for widget in self.timer_frame.winfo_children():
            widget.destroy()
        # Customers only get their own, admins get all
        if isinstance(self.sys.current_user, Customer):
            active_res = [r for r in self.sys.reservations if r.user == self.sys.current_user and r.is_active()]
        else:
            active_res = [r for r in self.sys.reservations if r.is_active()]

        if not active_res:
            tk.Label(self.timer_frame, text="There are no ongoing appointments at present", fg="gray").pack()
            return
        # Iterate active reservations and format HH:MM:SS display
        for res in active_res:
            if res.time_to_start() > 0:
                secs = int(res.time_to_start())
                h, remainder = divmod(secs, 3600)
                m, s = divmod(remainder, 60)
                time_str = f"{h:02d}:{m:02d}:{s:02d}"
                
                msg = f"Seat {res.seat.seat_id} Not start - Distance Start: {time_str}"
                tk.Label(self.timer_frame, text=msg, fg="blue", font=("Arial", 10)).pack()
                
            elif res.time_to_end() > 0:
                secs = int(res.time_to_end())
                h, remainder = divmod(secs, 3600)
                m, s = divmod(remainder, 60)
                time_str = f"{h:02d}:{m:02d}:{s:02d}"
                
                msg = f"Seat {res.seat.seat_id} In use - rest time: {time_str}"
                tk.Label(self.timer_frame, text=msg, fg="green", font=("Arial", 11, "bold")).pack()

if __name__ == "__main__":
    root = tk.Tk()  # Start the GUI application
    app = LibraryGUI(root)
    root.mainloop()