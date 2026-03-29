import sys
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QGridLayout, QDateEdit, QScrollArea, QCheckBox)
from PyQt5.QtCore import QTimer, Qt, QDate
from PyQt5.QtGui import QFont, QColor
from system import LibrarySystem
from reservation import Reservation
from seat import Seat


# ===== UTILITY FUNCTIONS FOR CODE SIMPLIFICATION =====

def create_title_label(text, size=14):
    """Create a formatted title label with consistent styling"""
    title = QLabel(text)
    font = QFont()
    font.setPointSize(size)
    font.setBold(True)
    title.setFont(font)
    title.setAlignment(Qt.AlignCenter)
    return title


def create_button(text, min_width=100, min_height=40, tooltip=None):
    """Create a button with consistent styling"""
    btn = QPushButton(text)
    btn.setMinimumWidth(min_width)
    btn.setMinimumHeight(min_height)
    if tooltip:
        btn.setToolTip(tooltip)
    return btn


def init_window(window, title, width=500, height=500):
    """Initialize window with title and size"""
    window.setWindowTitle(title)
    window.setGeometry(100, 100, width, height)
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout()
    return central_widget, main_layout


# ===== GUI WINDOW CLASSES =====

class ReservationWindow(QMainWindow):
    def __init__(self, system, user, replace_mode=False):
        super().__init__()
        self.system = system
        self.user = user
        self.replace_mode = replace_mode  # If True, replaces existing reservation
        self.admin_mode = False  # If True, window closes automatically after reservation
        self.select_user_window = None  # Reference to parent SelectUserWindow
        self.selected_seat = None
        self.selected_seat_button = None
        self.seat_buttons = {}  # Dictionary to store seat buttons for easy access
        self.init_ui()
        
    def init_ui(self):
        """Initialize the reservation interface"""
        self.setWindowTitle(f"Reservation System - Reserve a Table ({self.user.username})")
        self.setGeometry(100, 100, 600, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Title
        title_label = create_title_label("Reserve a Table")
        main_layout.addWidget(title_label)
        
        # Date input
        date_layout = QHBoxLayout()
        date_label = QLabel("Select Date:")
        self.date_input = QDateEdit()
        # Set default date to one day after current date
        tomorrow = QDate.currentDate().addDays(1)
        self.date_input.setDate(tomorrow)
        # Disable all dates before tomorrow
        self.date_input.setMinimumDate(tomorrow)
        self.date_input.setCalendarPopup(True)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        date_layout.addStretch()
        main_layout.addLayout(date_layout)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Existing reservation warning label
        self.reservation_warning_label = QLabel("")
        self.reservation_warning_label.setAlignment(Qt.AlignCenter)
        self.reservation_warning_label.setStyleSheet("color: red; background-color: rgb(255, 240, 240); padding: 10px; border: 1px solid red; border-radius: 5px;")
        self.reservation_warning_label.setVisible(False)
        main_layout.addWidget(self.reservation_warning_label)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Check if user already has a reservation
        if self.user.reservations:
            reservation = self.user.reservations[0]
            date_str = reservation.start_time.strftime("%Y-%m-%d")
            self.reservation_warning_label.setText(f"You have made a reservation on {date_str} at seat {reservation.seat.seat_id}")
            self.reservation_warning_label.setVisible(True)
        
        # Seat matrix (4x3)
        seats_layout = QGridLayout()
        seats_layout.setSpacing(10)
        
        # Create seat buttons - 4 rows, 3 columns
        # Rows: A, B, C, D; Columns: 1, 2, 3
        row_labels = ['A', 'B', 'C', 'D']
        for row in range(4):
            for col in range(3):
                seat_name = f"{row_labels[row]}{col + 1}"
                btn = QPushButton(seat_name)
                btn.setMinimumHeight(60)
                btn.setMinimumWidth(80)
                btn.clicked.connect(lambda checked, name=seat_name: self.on_seat_selected(name))
                self.seat_buttons[seat_name] = btn
                seats_layout.addWidget(btn, row, col)
        
        main_layout.addLayout(seats_layout)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Selected seat message
        self.selected_seat_label = QLabel("No seat selected")
        self.selected_seat_label.setAlignment(Qt.AlignCenter)
        self.selected_seat_label.setStyleSheet("color: blue; font-size: 12px;")
        main_layout.addWidget(self.selected_seat_label)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Button layout - Cancel and Reserve buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumWidth(100)
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.clicked.connect(self.on_cancel)
        button_layout.addWidget(self.cancel_button)
        
        # Reserve button
        self.reserve_button = QPushButton("Reserve")
        self.reserve_button.setMinimumWidth(100)
        self.reserve_button.setMinimumHeight(40)
        self.reserve_button.setEnabled(False)  # Disabled initially
        self.reserve_button.clicked.connect(self.on_reserve)
        button_layout.addWidget(self.reserve_button)
        main_layout.addLayout(button_layout)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Return button layout
        return_layout = QHBoxLayout()
        return_layout.addStretch()
        self.return_button = QPushButton("Return")
        self.return_button.setMinimumWidth(100)
        self.return_button.setMinimumHeight(40)
        self.return_button.clicked.connect(self.on_return)
        return_layout.addWidget(self.return_button)
        main_layout.addLayout(return_layout)
        
        main_layout.addStretch()
        central_widget.setLayout(main_layout)
    
    def on_seat_selected(self, seat_name):
        """Handle seat button click"""
        # If the same seat is clicked again, ignore it
        if self.selected_seat == seat_name:
            return
        
        # Reset all buttons to normal state first
        for name, btn in self.seat_buttons.items():
            btn.setStyleSheet("")
            btn.setEnabled(True)
        
        # Now disable all buttons except the selected one and update styles
        for name, btn in self.seat_buttons.items():
            if name != seat_name:
                btn.setStyleSheet("background-color: rgb(200, 200, 200);")
                btn.setEnabled(False)
            else:
                # Highlight selected button
                btn.setStyleSheet("background-color: rgb(0, 150, 0); color: white;")
                btn.setEnabled(True)
        
        # Update selected seat
        self.selected_seat = seat_name
        self.selected_seat_button = self.seat_buttons[seat_name]
        self.selected_seat_label.setText(f"Selected Seat: {seat_name}")
        
        # Check if user already has a reservation - disable reserve button if so
        if self.user.reservations and not self.replace_mode:
            self.reserve_button.setEnabled(False)
        else:
            self.reserve_button.setEnabled(True)
    
    def on_cancel(self):
        """Handle cancel button click - unselect the seat"""
        # Reset all buttons to normal state
        for name, btn in self.seat_buttons.items():
            btn.setStyleSheet("")
            btn.setEnabled(True)
        
        # Reset selected seat
        self.selected_seat = None
        self.selected_seat_button = None
        self.selected_seat_label.setText("No seat selected")
        
        # Disable reserve button
        self.reserve_button.setEnabled(False)
    
    def on_reserve(self):
        """Handle reserve button click"""
        if not self.selected_seat:
            QMessageBox.warning(self, "Error", "Please select a seat first.")
            return
        
        selected_date = self.date_input.date().toPyDate()
        start_time = datetime.combine(selected_date, datetime.min.time())
        
        # If in replace mode, remove the old reservation
        if self.replace_mode and self.user.reservations:
            old_reservation = self.user.reservations[0]
            self.user.reservations.clear()
            if old_reservation in self.system.reservations:
                self.system.reservations.remove(old_reservation)
        
        # Create a Seat object for the reservation
        # In a real app, you'd find the actual seat from the system
        seat = Seat(self.selected_seat)
        
        # Create reservation
        reservation = Reservation(self.user, seat, start_time, duration_minutes=60)
        
        # Add reservation to user's reservations
        self.user.reservations.append(reservation)
        
        # Add reservation to system
        self.system.reservations.append(reservation)
        
        # In admin mode, refresh the manage window and close
        if self.admin_mode:
            if hasattr(self, 'manage_window') and self.manage_window:
                self.manage_window.refresh_list()
            self.close()
        else:
            QMessageBox.information(self, "Success", f"Reservation confirmed for seat {self.selected_seat} on {selected_date}")
            self.close()
    
    def on_return(self):
        """Handle return button click - close the window"""
        self.close()


class ViewReservationWindow(QMainWindow):
    def __init__(self, system, user):
        super().__init__()
        self.system = system
        self.user = user
        self.init_ui()
        
    def init_ui(self):
        """Initialize the view reservation interface"""
        self.setWindowTitle(f"Reservation System - View My Reservation ({self.user.username})")
        self.setGeometry(100, 100, 500, 500)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Title
        title_label = create_title_label("View My Reservations")
        main_layout.addWidget(title_label)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Reservation info label
        if self.user.reservations:
            reservations_text = "Your Current Reservations:\n\n"
            for res in self.user.reservations:
                date_str = res.start_time.strftime("%Y-%m-%d")
                reservations_text += f"Seat {res.seat.seat_id} on {date_str}"
            
            warning_label = QLabel(reservations_text)
            warning_font = QFont()
            warning_font.setPointSize(11)
            warning_label.setFont(warning_font)
            warning_label.setAlignment(Qt.AlignCenter)
            warning_label.setStyleSheet("color: red; background-color: rgb(255, 240, 240); padding: 10px; border: 1px solid red; border-radius: 5px;")
        else:
            warning_label = QLabel("No reservations made")
            warning_font = QFont()
            warning_font.setPointSize(11)
            warning_label.setFont(warning_font)
            warning_label.setAlignment(Qt.AlignCenter)
            warning_label.setStyleSheet("color: blue; padding: 10px;")
        
        main_layout.addWidget(warning_label)
        
        # Add spacing
        main_layout.addSpacing(30)
        
        # Buttons layout - vertical spacing
        button_layout = QVBoxLayout()
        
        # Cancel previous reservation button
        self.cancel_previous_btn = QPushButton("Cancel Previous Reservation")
        self.cancel_previous_btn.setMinimumHeight(40)
        self.cancel_previous_btn.clicked.connect(self.on_cancel_previous)
        if not self.user.reservations:
            self.cancel_previous_btn.setEnabled(False)
        button_layout.addWidget(self.cancel_previous_btn)
        
        # Change reservation button
        self.change_btn = QPushButton("Change My Reservation")
        self.change_btn.setMinimumHeight(40)
        self.change_btn.clicked.connect(self.on_change)
        if not self.user.reservations:
            self.change_btn.setEnabled(False)
        button_layout.addWidget(self.change_btn)
        
        # Return button
        self.return_btn = QPushButton("Return")
        self.return_btn.setMinimumHeight(40)
        self.return_btn.clicked.connect(self.on_return)
        button_layout.addWidget(self.return_btn)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
    
    def on_cancel_previous(self):
        """Cancel the user's previous reservation"""
        if not self.user.reservations:
            QMessageBox.warning(self, "Error", "No reservation to cancel.")
            return
        
        reservation = self.user.reservations[0]
        seat_id = reservation.seat.seat_id
        date_str = reservation.start_time.strftime("%Y-%m-%d")
        
        # Remove from user's reservations
        self.user.reservations.clear()
        
        # Remove from system's reservations
        if reservation in self.system.reservations:
            self.system.reservations.remove(reservation)
        
        QMessageBox.information(self, "Success", f"Reservation for seat {seat_id} on {date_str} has been cancelled.")
        
        # Disable buttons
        self.cancel_previous_btn.setEnabled(False)
        self.change_btn.setEnabled(False)
        
        # Update warning label to show no reservations
        warning_label = self.findChild(QLabel, "warning_label") if hasattr(self, 'warning_label') else None
        self.close()  # Close the window after cancellation
    
    def on_change(self):
        """Open reservation window to change the reservation"""
        if not self.user.reservations:
            QMessageBox.warning(self, "Error", "No reservation to change.")
            return
        
        self.reservation_window = ReservationWindow(self.system, self.user, replace_mode=True)
        self.reservation_window.show()
        self.close()  # Close this window
    
    def on_return(self):
        """Return to main menu"""
        self.close()


class ChangeInfoWindow(QMainWindow):
    def __init__(self, system, user, manage_account_window=None):
        super().__init__()
        self.system = system
        self.user = user
        self.manage_account_window = manage_account_window
        self.init_ui()
        
    def init_ui(self):
        """Initialize the change info interface"""
        self.setWindowTitle(f"Reservation System - Change My Info ({self.user.username})")
        self.setGeometry(100, 100, 500, 420)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Title
        title_label = create_title_label("Change My Info")
        main_layout.addWidget(title_label)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # New password input
        password_layout = QHBoxLayout()
        password_label = QLabel("New Password:")
        password_label.setMinimumWidth(150)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter new password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.check_passwords)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Confirm password input
        confirm_layout = QHBoxLayout()
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setMinimumWidth(150)
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm new password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.textChanged.connect(self.check_passwords)
        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.confirm_input)
        main_layout.addLayout(confirm_layout)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Warning label
        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red; font-size: 11px;")
        self.warning_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.warning_label)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Button layout - Reset and Enter buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.setMinimumWidth(100)
        self.reset_button.setMinimumHeight(40)
        self.reset_button.clicked.connect(self.on_reset)
        button_layout.addWidget(self.reset_button)
        
        # Enter button
        self.enter_button = QPushButton("Enter")
        self.enter_button.setMinimumWidth(100)
        self.enter_button.setMinimumHeight(40)
        self.enter_button.setEnabled(False)
        self.enter_button.clicked.connect(self.on_change_password)
        button_layout.addWidget(self.enter_button)
        
        main_layout.addLayout(button_layout)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Return button layout
        return_layout = QHBoxLayout()
        return_layout.addStretch()
        self.return_button = QPushButton("Return")
        self.return_button.setMinimumWidth(100)
        self.return_button.setMinimumHeight(40)
        self.return_button.clicked.connect(self.on_return)
        return_layout.addWidget(self.return_button)
        main_layout.addLayout(return_layout)
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
    
    def check_passwords(self):
        """Check if passwords match and update warning"""
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not password or not confirm:
            self.warning_label.setText("")
            self.enter_button.setEnabled(False)
        elif password != confirm:
            self.warning_label.setText("Passwords do not match")
            self.enter_button.setEnabled(False)
        else:
            self.warning_label.setText("")
            self.enter_button.setEnabled(True)
    
    def on_change_password(self):
        """Change the user's password"""
        new_password = self.password_input.text()
        
        # Update password in user object
        self.user.password = new_password
        
        # Save updated password to JSON file
        self.system.update_user_in_json(self.user)
        
        QMessageBox.information(self, "Success", "Password changed successfully!")
        
        # Close manage account window if called from there
        if self.manage_account_window:
            self.manage_account_window.close()
        
        self.close()
    
    def on_reset(self):
        """Reset all input fields"""
        self.password_input.clear()
        self.confirm_input.clear()
        self.warning_label.setText("")
        self.enter_button.setEnabled(False)
        self.password_input.setFocus()
    
    def on_return(self):
        """Return to main menu"""
        self.close()


class ManageAccountWindow(QMainWindow):
    def __init__(self, system, admin_user):
        super().__init__()
        self.system = system
        self.admin_user = admin_user
        self.change_info_window = None
        self.user_checks = {}  # Dictionary to track checkbox states
        self.init_ui()
        
    def init_ui(self):
        """Initialize the manage account interface"""
        self.setWindowTitle("Reservation System - Manage Accounts")
        self.setGeometry(100, 100, 400, 550)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Title
        title_label = create_title_label("Manage User Accounts")
        main_layout.addWidget(title_label)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Scroll area for user list
        scroll_area = QWidget()
        self.scroll_layout = QVBoxLayout()
        
        # Get all users except admin
        non_admin_users = [user for user in self.system.users if user.role != 'Admin']
        
        # Create user entries with checkboxes
        if non_admin_users:
            for user in non_admin_users:
                user_layout = QHBoxLayout()
                
                # Username label (clickable to change password)
                user_label = QLabel(f'<a href="#">{user.username}</a>')
                user_label.setOpenExternalLinks(False)
                user_label.setCursor(Qt.PointingHandCursor)
                user_label.linkActivated.connect(lambda checked, u=user: self.on_user_clicked(u))
                user_layout.addWidget(user_label)
                
                user_layout.addStretch()
                
                # Checkbox
                checkbox = QCheckBox()
                checkbox.stateChanged.connect(self.update_delete_button)
                self.user_checks[user] = checkbox
                user_layout.addWidget(checkbox)
                
                self.scroll_layout.addLayout(user_layout)
        else:
            no_users_label = QLabel("No user accounts to manage")
            self.scroll_layout.addWidget(no_users_label)
        
        self.scroll_layout.addStretch()
        scroll_area.setLayout(self.scroll_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(scroll_area)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Button layout - Delete on left, Return on right
        button_layout = QHBoxLayout()
        
        # Delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.setMinimumWidth(100)
        self.delete_button.setMinimumHeight(40)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.on_delete)
        button_layout.addWidget(self.delete_button)
        
        button_layout.addStretch()
        
        # Return button
        self.return_button = QPushButton("Return")
        self.return_button.setMinimumWidth(100)
        self.return_button.setMinimumHeight(40)
        self.return_button.clicked.connect(self.on_return)
        button_layout.addWidget(self.return_button)
        
        main_layout.addLayout(button_layout)
        
        central_widget.setLayout(main_layout)
    
    def update_delete_button(self):
        """Update delete button state based on checkbox selections"""
        any_checked = any(cb.isChecked() for cb in self.user_checks.values())
        self.delete_button.setEnabled(any_checked)
    
    def on_user_clicked(self, user):
        """Handle user selection - login and open change info window"""
        self.system.current_user = user
        self.change_info_window = ChangeInfoWindow(self.system, user, manage_account_window=self)
        self.change_info_window.show()
    
    def on_delete(self):
        """Show confirmation dialog and delete selected accounts"""
        # Create confirmation dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirm Delete")
        dialog.setGeometry(200, 200, 400, 150)
        
        layout = QVBoxLayout()
        
        # Warning label
        warning_label = QLabel("Confirm deleting the selected account")
        warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning_label)
        
        layout.addSpacing(20)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Confirm button
        confirm_btn = QPushButton("Confirm")
        confirm_btn.setMinimumWidth(80)
        confirm_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(confirm_btn)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(80)
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        # Show dialog and check result
        if dialog.exec() == QDialog.Accepted:
            self.on_confirm_delete()
    
    def on_confirm_delete(self):
        """Delete selected user accounts"""
        users_to_delete = [user for user, checkbox in self.user_checks.items() if checkbox.isChecked()]
        
        for user in users_to_delete:
            # Remove from system users list
            if user in self.system.users:
                self.system.users.remove(user)
            # Delete from JSON file
            self.system.delete_user_from_json(user)
        
        # Refresh the list by closing and reopening the window
        self.close()
    
    def on_return(self):
        """Return to admin menu"""
        self.close()


class AdminWindow(QMainWindow):
    def __init__(self, system, user, login_window=None):
        super().__init__()
        self.system = system
        self.user = user
        self.login_window = login_window
        self.init_ui()
        
    def init_ui(self):
        """Initialize the admin menu interface"""
        self.setWindowTitle(f"Reservation System - Admin Menu ({self.user.username})")
        self.setGeometry(100, 100, 500, 500)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Welcome label
        welcome_label = QLabel("Welcome to the Admin Panel!")
        welcome_font = QFont()
        welcome_font.setPointSize(16)
        welcome_font.setBold(True)
        welcome_label.setFont(welcome_font)
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)
        
        # Add spacing
        main_layout.addSpacing(30)
        
        # Admin info
        admin_info_label = QLabel(f"Logged in as: {self.user.username} (Admin)")
        admin_font = QFont()
        admin_font.setPointSize(12)
        admin_info_label.setFont(admin_font)
        admin_info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(admin_info_label)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Menu buttons layout - vertical
        buttons_layout = QVBoxLayout()
        
        # Button 1: Manage Reservation
        self.manage_reservation_btn = QPushButton("1. Manage Reservation")
        self.manage_reservation_btn.setMinimumHeight(50)
        self.manage_reservation_btn.clicked.connect(self.on_manage_reservation)
        buttons_layout.addWidget(self.manage_reservation_btn)
        
        # Button 2: Manage Accounts
        self.manage_accounts_btn = QPushButton("2. Manage Accounts")
        self.manage_accounts_btn.setMinimumHeight(50)
        self.manage_accounts_btn.clicked.connect(self.on_manage_accounts)
        buttons_layout.addWidget(self.manage_accounts_btn)
        
        # Button 3: Change My Info
        self.change_info_btn = QPushButton("3. Change My Info")
        self.change_info_btn.setMinimumHeight(50)
        self.change_info_btn.clicked.connect(self.on_change_info)
        buttons_layout.addWidget(self.change_info_btn)
        
        # Button 4: Return
        self.return_btn = QPushButton("4. Return")
        self.return_btn.setMinimumHeight(50)
        self.return_btn.clicked.connect(self.on_return)
        buttons_layout.addWidget(self.return_btn)
        
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
    
    def on_manage_reservation(self):
        """Open Manage Reservation window"""
        self.manage_reservation_window = ManageReservationWindow(self.system, self.user)
        self.manage_reservation_window.show()
    
    def on_manage_accounts(self):
        """Open Manage Accounts window"""
        self.manage_account_window = ManageAccountWindow(self.system, self.user)
        self.manage_account_window.show()
    
    def on_change_info(self):
        """Handle Change My Info button"""
        self.change_info_window = ChangeInfoWindow(self.system, self.user)
        self.change_info_window.show()
    
    def on_return(self):
        """Handle Return button - logout"""
        if self.login_window:
            self.login_window.reset_for_login()
        self.close()


class ManageReservationWindow(QMainWindow):
    def __init__(self, system, admin_user):
        super().__init__()
        self.system = system
        self.admin_user = admin_user
        self.reservation_checks = {}  # Dictionary to track checkbox states
        self.scroll_area = None
        self.scroll_layout = None
        self.main_layout = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the manage reservation interface"""
        self.setWindowTitle("Reservation System - Manage Reservations")
        self.setGeometry(100, 100, 700, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Title
        title_label = create_title_label("Manage Reservations")
        main_layout.addWidget(title_label)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Reservations list area
        self.scroll_area = QWidget()
        self.scroll_layout = QVBoxLayout()
        
        # Get all reservations and sort by date
        all_reservations = []
        for user in self.system.users:
            for res in user.reservations:
                all_reservations.append((user, res))
        
        # Sort by date
        all_reservations.sort(key=lambda x: x[1].start_time)
        
        # Display reservations with checkboxes
        if all_reservations:
            for user, reservation in all_reservations:
                res_layout = QHBoxLayout()
                
                # Reservation info
                date_str = reservation.start_time.strftime("%Y-%m-%d")
                seat_str = str(reservation.seat.seat_id)
                username = user.username
                info_text = f"{date_str} | Seat {seat_str} | User: {username}"
                
                info_label = QLabel(info_text)
                res_layout.addWidget(info_label)
                res_layout.addStretch()
                
                # Checkbox
                checkbox = QCheckBox()
                self.reservation_checks[(user, reservation)] = checkbox
                res_layout.addWidget(checkbox)
                
                self.scroll_layout.addLayout(res_layout)
            
            self.scroll_area.setLayout(self.scroll_layout)
        else:
            no_res_label = QLabel("No reservations found")
            self.scroll_layout.addWidget(no_res_label)
            self.scroll_area.setLayout(self.scroll_layout)
        
        self.scroll_layout.addStretch()
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(self.scroll_area)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)
        
        # Store main_layout for use in refresh method
        self.main_layout = main_layout
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Add button
        self.add_button = QPushButton("Add")
        self.add_button.setMinimumWidth(100)
        self.add_button.setMinimumHeight(40)
        self.add_button.clicked.connect(self.on_add)
        button_layout.addWidget(self.add_button)
        
        button_layout.addStretch()
        
        # Delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.setMinimumWidth(100)
        self.delete_button.setMinimumHeight(40)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.on_delete)
        button_layout.addWidget(self.delete_button)
        
        main_layout.addLayout(button_layout)
        
        # Return button
        return_layout = QHBoxLayout()
        return_layout.addStretch()
        self.return_button = QPushButton("Return")
        self.return_button.setMinimumWidth(100)
        self.return_button.setMinimumHeight(40)
        self.return_button.clicked.connect(self.on_return)
        return_layout.addWidget(self.return_button)
        main_layout.addLayout(return_layout)
        
        central_widget.setLayout(main_layout)
        
        # Connect checkbox changes to update delete button state
        for checkbox in self.reservation_checks.values():
            checkbox.stateChanged.connect(self.update_delete_button)
    
    def update_delete_button(self):
        """Update delete button state based on checkbox selections"""
        any_checked = any(cb.isChecked() for cb in self.reservation_checks.values())
        self.delete_button.setEnabled(any_checked)
    
    def refresh_list(self):
        """Refresh the reservation list display"""
        # Clear old layout
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._clear_layout(child.layout())
        
        self.reservation_checks.clear()
        
        # Get all reservations and sort by date
        all_reservations = []
        for user in self.system.users:
            for res in user.reservations:
                all_reservations.append((user, res))
        
        # Sort by date
        all_reservations.sort(key=lambda x: x[1].start_time)
        
        # Display reservations with checkboxes
        if all_reservations:
            for user, reservation in all_reservations:
                res_layout = QHBoxLayout()
                
                # Reservation info
                date_str = reservation.start_time.strftime("%Y-%m-%d")
                seat_str = str(reservation.seat.seat_id)
                username = user.username
                info_text = f"{date_str} | Seat {seat_str} | User: {username}"
                
                info_label = QLabel(info_text)
                res_layout.addWidget(info_label)
                res_layout.addStretch()
                
                # Checkbox
                checkbox = QCheckBox()
                checkbox.stateChanged.connect(self.update_delete_button)
                self.reservation_checks[(user, reservation)] = checkbox
                res_layout.addWidget(checkbox)
                
                self.scroll_layout.addLayout(res_layout)
        else:
            no_res_label = QLabel("No reservations found")
            self.scroll_layout.addWidget(no_res_label)
        
        self.scroll_layout.addStretch()
    
    def _clear_layout(self, layout):
        """Helper method to clear a layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._clear_layout(child.layout())
    
    def on_add(self):
        """Open window to select user for reservation"""
        self.select_user_window = SelectUserWindow(self.system, self.admin_user, self)
        self.select_user_window.show()
    
    def on_delete(self):
        """Delete checked reservations"""
        deleted_count = 0
        for (user, reservation), checkbox in self.reservation_checks.items():
            if checkbox.isChecked():
                if reservation in user.reservations:
                    user.reservations.remove(reservation)
                    deleted_count += 1
                if reservation in self.system.reservations:
                    self.system.reservations.remove(reservation)
        
        if deleted_count > 0:
            QMessageBox.information(self, "Success", f"{deleted_count} reservation(s) deleted successfully!")
            self.close()
    
    def on_return(self):
        """Return to admin menu"""
        self.close()


class SelectUserWindow(QMainWindow):
    def __init__(self, system, admin_user, manage_window=None):
        super().__init__()
        self.system = system
        self.admin_user = admin_user
        self.selected_user = None
        self.auto_login_timer = None
        self.manage_window = manage_window
        self.init_ui()
        
    def init_ui(self):
        """Initialize the select user interface"""
        self.setWindowTitle("Reservation System - Select User")
        self.setGeometry(100, 100, 400, 500)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Title
        title_label = create_title_label("Select a User for Reservation", size=12)
        main_layout.addWidget(title_label)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # User list
        for user in self.system.users:
            if user.role == "Customer":  # Only show customers
                user_link = QLabel(f"<a href='#'>{user.username}</a>")
                user_link.setOpenExternalLinks(False)
                user_data = user
                user_link.linkActivated.connect(lambda checked, u=user_data: self.on_user_selected(u))
                user_link.setCursor(Qt.PointingHandCursor)
                main_layout.addWidget(user_link)
        
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
    
    def on_user_selected(self, user):
        """Handle user selection - open reservation immediately without waiting"""
        self.selected_user = user
        self.user_to_login = user
        # Open reservation window immediately
        self.open_reservation()
    
    def open_reservation(self):
        """Login user and open reservation window"""
        self.system.current_user = self.user_to_login
        
        # Open reservation window
        self.reservation_window = ReservationWindow(self.system, self.user_to_login, replace_mode=False)
        
        # Store reference to auto-close when done
        self.reservation_window.admin_mode = True
        self.reservation_window.select_user_window = self
        self.reservation_window.manage_window = self.manage_window
        
        self.reservation_window.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self, system, user, login_window=None):
        super().__init__()
        self.system = system
        self.user = user
        self.login_window = login_window
        self.init_ui()
        
    def init_ui(self):
        """Initialize the main menu interface"""
        self.setWindowTitle(f"Reservation System - Main Menu ({self.user.username})")
        self.setGeometry(100, 100, 500, 500)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Welcome label
        welcome_label = QLabel("Welcome to the Reservation system!")
        welcome_font = QFont()
        welcome_font.setPointSize(16)
        welcome_font.setBold(True)
        welcome_label.setFont(welcome_font)
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)
        
        # Clock and date label
        self.clock_label = QLabel()
        clock_font = QFont()
        clock_font.setPointSize(14)
        self.clock_label.setFont(clock_font)
        self.clock_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.clock_label)
        
        # Update clock initially
        self.update_clock()
        
        # Timer to update clock every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        
        # Add spacing
        main_layout.addSpacing(30)
        
        # User info label
        user_info_label = QLabel(f"Logged in as: {self.user.username}")
        user_font = QFont()
        user_font.setPointSize(12)
        user_info_label.setFont(user_font)
        user_info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(user_info_label)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Menu buttons layout
        buttons_layout = QVBoxLayout()
        
        # Button 1: Reserve a table
        self.reserve_btn = QPushButton("1. Reserve a Table")
        self.reserve_btn.setMinimumHeight(50)
        self.reserve_btn.clicked.connect(self.on_reserve)
        buttons_layout.addWidget(self.reserve_btn)
        
        # Button 2: View my reservation
        self.view_btn = QPushButton("2. View My Reservation")
        self.view_btn.setMinimumHeight(50)
        self.view_btn.clicked.connect(self.on_view)
        buttons_layout.addWidget(self.view_btn)
        
        # Button 3: Change my info
        self.change_info_btn = QPushButton("3. Change My Info")
        self.change_info_btn.setMinimumHeight(50)
        self.change_info_btn.clicked.connect(self.on_change_info)
        buttons_layout.addWidget(self.change_info_btn)
        
        # Button 4: Exit
        self.exit_btn = QPushButton("4. Exit")
        self.exit_btn.setMinimumHeight(50)
        self.exit_btn.clicked.connect(self.on_exit)
        buttons_layout.addWidget(self.exit_btn)
        
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()  # Add stretch at bottom
        
        central_widget.setLayout(main_layout)
        
    def update_clock(self):
        """Update the clock and date label"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %B %d, %Y")
        self.clock_label.setText(f"{time_str}\n{date_str}")
    
    def on_reserve(self):
        """Handle Reserve a Table button"""
        self.reservation_window = ReservationWindow(self.system, self.user)
        self.reservation_window.show()
    
    def on_view(self):
        """Handle View My Reservation button"""
        self.view_reservation_window = ViewReservationWindow(self.system, self.user)
        self.view_reservation_window.show()
    
    def on_change_info(self):
        """Handle Change My Info button"""
        self.change_info_window = ChangeInfoWindow(self.system, self.user)
        self.change_info_window.show()
    
    def on_exit(self):
        """Handle Exit button - return to login window"""
        self.timer.stop()
        if self.login_window:
            self.login_window.reset_for_login()
        self.close()
        
    def closeEvent(self, event):
        """Handle window close event"""
        self.timer.stop()
        event.accept()


class CreateAccountWindow(QMainWindow):
    def __init__(self, system):
        super().__init__()
        self.system = system
        self.init_ui()
        
    def init_ui(self):
        """Initialize the create account interface"""
        self.setWindowTitle("Reservation System - Create Account")
        self.setGeometry(100, 100, 500, 400)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Create New Account")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # ID input
        id_layout = QHBoxLayout()
        id_label = QLabel("ID:")
        id_label.setMinimumWidth(100)
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter new ID")
        self.id_input.textChanged.connect(self.check_inputs)
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_input)
        main_layout.addLayout(id_layout)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Password input
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setMinimumWidth(100)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.check_inputs)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Confirm password input
        confirm_layout = QHBoxLayout()
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setMinimumWidth(100)
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.textChanged.connect(self.check_inputs)
        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.confirm_input)
        main_layout.addLayout(confirm_layout)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Warning label
        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red; font-size: 11px;")
        self.warning_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.warning_label)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Button layout - Return and Enter buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Return button
        self.return_button = QPushButton("Return")
        self.return_button.setMinimumWidth(100)
        self.return_button.setMinimumHeight(40)
        self.return_button.clicked.connect(self.on_return)
        button_layout.addWidget(self.return_button)
        
        # Enter button
        self.enter_button = QPushButton("Enter")
        self.enter_button.setMinimumWidth(100)
        self.enter_button.setMinimumHeight(40)
        self.enter_button.setEnabled(False)
        self.enter_button.clicked.connect(self.on_create_account)
        button_layout.addWidget(self.enter_button)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
    
    def check_inputs(self):
        """Check inputs and update warning"""
        user_id = self.id_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        self.warning_label.setText("")
        
        # Check if all fields are filled
        if not user_id or not password or not confirm:
            self.enter_button.setEnabled(False)
            return
        
        # Check if passwords match
        if password != confirm:
            self.warning_label.setText("Incorrect password")
            self.enter_button.setEnabled(False)
            return
        
        # Check if ID already exists
        for user in self.system.users:
            if user.username == user_id:
                self.warning_label.setText("This ID has been registered!")
                self.enter_button.setEnabled(False)
                return
        
        # All checks passed
        self.enter_button.setEnabled(True)
    
    def on_create_account(self):
        """Create a new account"""
        user_id = self.id_input.text().strip()
        password = self.password_input.text()
        
        # Double check validations
        if not user_id or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
        
        # Check if ID already exists
        for user in self.system.users:
            if user.username == user_id:
                QMessageBox.warning(self, "Error", "This ID has been registered!")
                return
        
        # Import Customer class for creating new user
        from user import Customer
        
        # Create new customer
        new_user = Customer(user_id, password)
        
        # Add to system
        self.system.users.append(new_user)
        
        # Save to JSON file
        self.system.save_user_to_json(new_user)
        
        QMessageBox.information(self, "Success", f"Account '{user_id}' created successfully!")
        self.close()
    
    def on_return(self):
        """Return to login window"""
        self.close()


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.system = LibrarySystem()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Reservation System - Login")
        self.setGeometry(100, 100, 500, 350)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Welcome label
        welcome_label = QLabel("Welcome to the Reservation system!")
        welcome_font = QFont()
        welcome_font.setPointSize(16)
        welcome_font.setBold(True)
        welcome_label.setFont(welcome_font)
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)
        
        # Clock and date label
        self.clock_label = QLabel()
        clock_font = QFont()
        clock_font.setPointSize(14)
        self.clock_label.setFont(clock_font)
        self.clock_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.clock_label)
        
        # Update clock initially
        self.update_clock()
        
        # Timer to update clock every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Login section layout
        login_layout = QVBoxLayout()
        
        # ID input
        id_layout = QHBoxLayout()
        id_label = QLabel("ID:")
        id_label.setMinimumWidth(60)
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter your ID")
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_input)
        login_layout.addLayout(id_layout)
        
        # Password input
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setMinimumWidth(60)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        login_layout.addLayout(password_layout)
        
        # Button layout - Enter button on the right
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add stretch to push button to the right
        self.login_button = QPushButton("Enter")
        self.login_button.setMinimumWidth(100)
        self.login_button.clicked.connect(self.on_login)
        button_layout.addWidget(self.login_button)
        login_layout.addLayout(button_layout)
        
        main_layout.addLayout(login_layout)
        
        # Add spacing
        main_layout.addSpacing(10)
        
        # Create account hyperlink
        create_account_label = QLabel("<a href='#'>Create account</a>")
        create_account_label.setOpenExternalLinks(False)
        create_account_label.linkActivated.connect(self.on_create_account)
        create_account_label.setAlignment(Qt.AlignLeft)
        create_account_label.setCursor(Qt.PointingHandCursor)
        main_layout.addWidget(create_account_label)
        
        main_layout.addStretch()  # Add stretch at bottom
        
        central_widget.setLayout(main_layout)
        
    def update_clock(self):
        """Update the clock and date label"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %B %d, %Y")
        self.clock_label.setText(f"{time_str}\n{date_str}")
        
    def on_login(self):
        """Handle login button click"""
        user_id = self.id_input.text().strip()
        password = self.password_input.text().strip()
        
        if not user_id or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both ID and password.")
            return
        
        # Authenticate user
        authenticated_user = None
        for user in self.system.users:
            if user.username == user_id and user.password == password:
                authenticated_user = user
                break
        
        if authenticated_user:
            self.system.current_user = authenticated_user
            self.timer.stop()
            # Check if user is Admin or Customer
            if authenticated_user.role == "Admin":
                # Open admin window
                self.admin_window = AdminWindow(self.system, authenticated_user, login_window=self)
                self.admin_window.show()
            else:
                # Open main menu window
                self.main_window = MainWindow(self.system, authenticated_user, login_window=self)
                self.main_window.show()
            self.hide()  # Hide login window instead of closing it
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid ID or password. Please try again.")
            self.clear_inputs()
    
    def clear_inputs(self):
        """Clear input fields"""
        self.id_input.clear()
        self.password_input.clear()
        self.id_input.setFocus()
    
    def reset_for_login(self):
        """Reset the login window when returning from main menu"""
        self.clear_inputs()
        self.timer.start(1000)  # Restart the clock timer
        self.show()
        self.raise_()  # Bring window to front
        self.activateWindow()  # Give focus to the window
    
    def on_create_account(self):
        """Handle Create account hyperlink click"""
        self.create_account_window = CreateAccountWindow(self.system)
        self.create_account_window.show()
    def closeEvent(self, event):
        """Handle window close event"""
        self.timer.stop()
        event.accept()


def run_gui():
    """Run the PyQt5 GUI application"""
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
