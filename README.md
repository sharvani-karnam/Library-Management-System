# 📚 Library Management System

A robust console-based application to manage library operations, built using Python and MySQL. This project demonstrates backend development skills, specifically focusing on Database Management Systems (DBMS) and Python-SQL connectivity.

## 🛠️ System Architecture
The application is structured into two main classes:
1.  **Database Class:** Handles the low-level connection, cursor creation, and error handling with the MySQL server.
2.  **LibrarySystem Class:** Contains the business logic for adding books, issuing cards, and processing transactions.

## 🔑 Key Features
* **Book Management:** Add new inventory with details (Title, Author, Genre, Copies).
* **Member Management:** Issue library cards with subscription tracking.
* **Circulation:** Real-time tracking of issued books and returns using `datetime` stamping.
* **Stock Control:** Automatically updates the 'Copies' count in the database when books are issued or returned.
* **Data Persistence:** All data is stored permanently in a MySQL database, not just in memory.

## 💻 Tech Stack
* **Language:** Python
* **Database:** MySQL
* **Connector:** `mysql-connector-python`

## ⚙️ Setup Instructions
1.  **Install the connector:**
    ```bash
    pip install mysql-connector-python
    ```
2.  **Set up the database:**
    * Open your MySQL Command Line or Workbench.
    * Run the script provided in `database_setup.sql` to create the tables.
3.  **Run the Application:**
    * Run the Python file:
        ```bash
        python library.py
    * **Note:** The program is secure. When you run it, it will ask you to enter your MySQL password in the terminal.

## 🚀 Future Improvements
* Add a GUI using Tkinter or CustomTkinter.
* Implement a login system for Librarians vs. Students.

---
*Created by Sharvani Karnam - B.Tech AIML Student*
__
