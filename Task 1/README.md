# This is a guide on how to run program
------------------------------------------

**First, we need to modify the VS Code Settings to make it output in the Terminal panel.**
* **Step 1:** Open settings
  * Shortcut key: `Ctrl + ,` (Windows) or `Cmd + ,` (Mac)
* **Step 2:** Enter in the search box
  * Plaintext: `code runner run in terminal`
* **Step 3:** Check the box
  * Check `Code-runner: Run in Terminal`
* **Step 4:** Then click the button
  * Click the play button in the top right corner of the editor and the program will automatically start in the Terminal panel
 
-----------------------------------------

**Second, we find gui.py, and then click "run code"**
* We will see a web page "Library Seat Reservation System GUI" (page content):
  1. Username (you need to input your name)
  2. Password (you need to input your password)
  3. Login (Login after registration)
  4. Register as Customer (Select the role you need to choose)
  5. Register as Admin (Select the role you need to choose)

---------------------------------------

**Third, we need to enter username and password, and register as customer**
* Enter username:
  * e.g. Username: ZHU
* Enter password:
  * e.g. Password: 123456

> ** If you don't enter your name or password, register directly. The system will pop up automatically: Please fill in the username and password you want to register in the input boxes above!

> ** If you don't enter your name or password, login directly. The system will pop up automatically: Username and Password cannot be empty!

* Click on the "Register as customer":
  * e.g. You will enter the Customer Dashboard

--------------------------------------

**Fourth, we will see Customer Dashboard (content page) and use the functions inside:**

* **View all seats:**
  When we click on it, we will see 
  ```text
  [Standard Desk] Seat 1: Available
  [Standard Desk] Seat 2: Available
  [Standard Desk] Seat 3: Available
  [Computer Seat] Seat 4: Available
  [Computer Seat] Seat 5: Available 
* **Reserve a seat:** when we click on it, we will see
  
  ```text
  Available seats: [1,2,3,4,5] 
  Please enter the seat number you want to reserve:
Step 1: Please enter the seat number you want to want to reserve (e.g. 1).

Step 2: Click on "OK" (If you click on "Cancel", you will exit this interface).

Step 3: You will see "Enter start time (format: 2025-03-04 14:00): " (If you don't see this page, you need to click on the main page again, because this page is hidden on the main page).

🔸 Case 1: If you enter an unreasonable time (e.g. 111), the system will pop up automatically: Invalid time format.

🔸 Case 2: If you enter past time (e.g. 2025-01-12 00:00), the system will pop up automatically: The start time cannot be the past.

🔸 Case 3: If you enter normal time (e.g. 2026-04-07 01:00), and then click on "OK", you will enter the next page (If you click on "Cancel", you will exit this interface).

Step 4: You will see "Enter reservation duration(e.g., 10, 20, 30, 60 miniutes): " (Default value is 30).

e.g. You can input "10" then click on "OK" (If you click on "Cancel", you will exit this interface).

Step 5: You will see system message "Reservation successful! ZHU resered seat 1 from 2026-04-07 01:00 to 2026-04-07 01:10(10 min)".

🔹 Case 1: If the time you have made an appointment is within 5 minutes from now, the system will also pop up automatically: [REMIND] Seat 1 will start soon!.

🔹 Case 2: If the time you have made an appointment happens to be the current time, the system will also pop up automatically: [REMIND] Seat 1 reservation time is officially beginning..

💡 Attention: After you have made an appointment, you will see how much time is left until the start or end (With only five minutes left, the system will also pop up automatically: [REMIND] Seat 1 will end soon, please prepare to leave).

------------------------------------------
Release my seat:
when we click on it, you will see “Your reservations:
                                   1. ZHU reserved seat 1 from 2026-04-07 01:00 to 2026-04-07 01:10(10 min)[Active]
                                   Enter the reservation number to release(1,2...):”
e.g. Step 1: You can input: 1

     Step 2: Click on the "OK" (If you click on the "Cancel", you will exit this interface)

     Step 3: You will see the system will also pop up automatically: Seat 1 has been successfully released!

-----------------------------------------

View my reservations:
when we click on it,

Case 1: If you made an appointment but it wasn't released, the system will also pop up automatically: ZHU reserved seat 1 from 2026-04-07 01:00 to 2026-04-07 01:10(10 min)[Active]

Case 2: If you haven't made an appointment or have cancelled it, the system will also pop up automatically: You have no reservation records.

----------------------------------------

Logout：
when we click on it, you will exit to the login interface.

---------------------------------------
  
  
  
  
  
