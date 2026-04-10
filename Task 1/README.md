# 📚 Library Seat Reservation System 
This project is a library seat reservation system with a graphical user interface (GUI) built based on Python and Tkinter. The system implements core functions such as user registration, login, real-time seat viewing, reservation, and countdown reminders, and persists data through local JSON files. 
---

## 🛠️ Environment Requirements (Prerequisites) 
* **Python Version**: 3.7 or higher.
* **Tkinter Library**: Comes with the Python standard library and no additional installation is required.
* *For Linux users (such as Ubuntu) who are missing this library, please run*: `sudo apt-get install python3-tk`. 
---

## 📁 Project Structure (Project Structure) 
Please ensure that the following files are located in the same working directory to ensure the normal operation of the program: 
| File Name | Type | Function Description |
| :--- | :--- | :--- |
| **`gui.py`** | Python | **Main entry point of the program**. It is responsible for the GUI layout, user interaction logic, and the startup of background tasks. |
| **`system.py`** | Python | **Core Logic Layer**. Manages seat data, JSON read/write, and sorting algorithms (bubble sort/insertion sort). |
| **`user.py`** | Python | **User Model**. Defines two types of roles, `Customer` and `Admin`, and their attributes. |
| **`seat.py`** | Python | **Seat Model**. Contains `StandardSeat` (standard seat) and `ComputerSeat` (computer seat). |
| **`reservation.py`** | Python | **Reservation Management**. Handles the specific time of reservations, duration calculation, and status determination. |
| **`reminder.py`** | Python | **Message Reminder**. Responsible for generating notification messages when an appointment starts or is about to end. |
| **`user_data.json`** | JSON | **Local database**. Initially empty `[]`, used to store all registered user account information. |

---

## 🚀 How to Run 
1. **Open the Terminal**: Open your Terminal (macOS/Linux) or Command Prompt (Windows).
2. **Navigate to the Directory**: Use the `cd` command to enter the folder containing the above-mentioned files. ```bash
cd /your/project/path ```
3. **Start the program**: Execute the following command: ```bash
python gui.py
```
*(Note: Some systems may require using `python3 gui.py`)*. 
---

## 💡 Usage Guide 
### 1. Account Preparation
* **First Use**: Since `user_data.json` is initially empty, you need to register first.
* **Registration**: Enter your username and password in the login window, and click either **"Register as Customer"** or **"Register as Admin"**.
* **Login**: After successful registration, log in to the system directly by clicking **"Login"** with your account. 
### 2. Core Functions
* **Seat Viewing**: The system presets 5 test seats (3 standard seats and 2 computer seats). You can click "View all seats" on the dashboard to check the real-time status.
* **Seat Reservation**: Customers can select an available seat and enter the start time (format: `2026-04-10 18:00`) and reservation duration.
* **Real-time Reminders**: After a successful reservation, a real-time countdown will be displayed at the bottom of the main interface. When there are less than 5 minutes until the reservation starts or ends, a pop-up window will appear to remind you. 
### 3. Administrator Privileges
* After logging in, administrators can **add new seats**, **delete idle seats**, and view **all reservation records** in the system. 
---

> **Hint**: It is recommended to view this file with a Markdown preview-supported editor (such as **VS Code** or **Typora**), for a better effect.
  
  
  
