import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ---------------- Database Class ----------------
class Database:
    def __init__(self, host="localhost", user="root", database="library_management"):
        self.host = host
        self.user = user
        self.password = input("Enter Database Password: ")
        self.database = database
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.database
            )
            return self.conn.is_connected()
        except Error as e:
            print(f"Database connection error: {e}")
            return False

    # default to buffered cursor so fetchone()/fetchall() behave predictably
    def cursor(self, buffered=True):
        if self.conn:
            return self.conn.cursor(buffered=buffered)
        else:
            raise ConnectionError("Database not connected.")

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

# ---------------- Library System ----------------
class LibrarySystem:
    def __init__(self, db: Database):
        self.db = db
        if not self.db.connect():
            print("Failed to connect to database.")
            exit()

    # --------- Book Operations ---------
    def add_book(self):
        try:
            book_id = int(input("Enter Book_ID: "))
            title = input("Enter Book Title: ")
            author = input("Enter Author Name: ")
            genre = input("Enter Genre: ")
            copies = int(input("Enter Number of Copies: "))

            cursor = self.db.cursor()
            sql = "INSERT INTO book_details (Book_id, Title, Authors_Name, Genre, Copies) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, (book_id, title, author, genre, copies))
            self.db.commit()
            cursor.close()

            print("\n(: Book added successfully :)\n")
        except ValueError:
            print("Invalid input. Book ID and Copies must be integers.")
        except Error as e:
            print(f"Database error: {e}")

    def list_books(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM book_details")
            books = cursor.fetchall()
            cursor.close()

            if not books:
                print("No books found.")
                return

            print("\nBook_ID | Title | Author | Genre | Copies\n")
            for b in books:
                print(f"{b[0]} | {b[1]} | {b[2]} | {b[3]} | {b[4]}\n")
        except Error as e:
            print(f"Database error: {e}")

    # --------- Library Card ---------
    def issue_card(self):
        try:
            card_no = int(input("Enter Card Number: "))
            name = input("Enter Reader's Name: ")
            branch = input("Enter Branch Address: ")
            subscription = int(input("Subscription (months): "))

            cursor = self.db.cursor()
            sql = "INSERT INTO library_card (Card_No, Readers_Name, BranchAddress, Subscription) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (card_no, name, branch, subscription))
            self.db.commit()
            cursor.close()

            print("\n(: Library Card issued :)\n")
        except ValueError:
            print("Card number and subscription must be integers.")
        except Error as e:
            print(f"Database error: {e}")

    # --------- Borrower / Issue Book ---------
    def issue_book(self):
        try:
            card_no = int(input("Card Number: "))
            name = input("Borrower's Name: ")
            address = input("Address: ")
            phone = input("Phone: ")
            book_id = int(input("Book ID: "))

            cursor = self.db.cursor()

            # Check book availability
            cursor.execute("SELECT Copies FROM book_details WHERE Book_id=%s", (book_id,))
            book = cursor.fetchone()
            if not book:
                print("\nBook not found.\n")
                cursor.close()
                return
            if book[0] <= 0:
                print("No copies available.")
                cursor.close()
                return

            issued_date = datetime.today().strftime('%Y-%m-%d')
            return_date = input("Return Date (YYYY-MM-DD): ")

            # Validate return_date format
            try:
                datetime.strptime(return_date, "%Y-%m-%d")
            except ValueError:
                print("Return Date must be in YYYY-MM-DD format.")
                cursor.close()
                return

            # Insert borrower record and capture lastrowid immediately
            sql = """INSERT INTO borrower (Card_No, Name, Address, Phone, Book_ID, Issued_Date, Return_Date)
                     VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql, (card_no, name, address, phone, book_id, issued_date, return_date))
            borrower_id = cursor.lastrowid  # capture right after INSERT
            self.db.commit()

            # Decrement book copies
            cursor.execute("UPDATE book_details SET Copies = Copies - 1 WHERE Book_id=%s", (book_id,))
            self.db.commit()
            cursor.close()

            print(f"\n(: Book issued successfully! Borrower ID: {borrower_id} :)\n")
        except ValueError:
            print("Invalid input. Card Number and Book ID must be integers.")
        except Error as e:
            print(f"Database error: {e}")

    # --------- Return Book ---------
    def return_book(self):
        try:
            borrower_id = int(input("Enter Borrower ID to return book: "))
            cursor = self.db.cursor()

            # Find the borrower's Book_ID
            cursor.execute("SELECT Book_ID FROM borrower WHERE Borrower_id=%s", (borrower_id,))
            row = cursor.fetchone()
            if not row:
                print("Borrower record not found.")
                cursor.close()
                return

            book_id = row[0]

            # Increment book copies
            cursor.execute("UPDATE book_details SET Copies = Copies + 1 WHERE Book_id=%s", (book_id,))

            # Remove borrower record
            cursor.execute("DELETE FROM borrower WHERE Borrower_id=%s", (borrower_id,))
            self.db.commit()
            cursor.close()

            print("\n(: Book returned successfully :)\n")
        except ValueError:
            print("Invalid input. Borrower ID must be an integer.")
        except Error as e:
            print(f"Database error: {e}")

    # --------- View Borrower Details ---------
    def list_borrowers(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT br.Borrower_id, br.Name, br.Address, br.Phone, bd.Title, br.Issued_Date, br.Return_Date
                FROM borrower br
                JOIN book_details bd ON br.Book_ID = bd.Book_id
            """)
            rows = cursor.fetchall()
            cursor.close()

            if not rows:
                print("No borrowers found.")
                return

            print("\n ID | Name | Address | Phone | Book Title | Issued Date | Return Date \n")
            for r in rows:
                print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]}\n")
        except Error as e:
            print(f"Database error: {e}")

# ---------------- Main Menu ----------------
def main():
    db = Database()
    system = LibrarySystem(db)

    while True:
        print("\n--- LIBRARY MANAGEMENT SYSTEM ---\n")
        print("1. Add Book")
        print("2. List Books")
        print("3. Issue Library Card")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. View Borrower Details")
        print("7. Exit\n")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                system.add_book()
            elif choice == 2:
                system.list_books()
            elif choice == 3:
                system.issue_card()
            elif choice == 4:
                system.issue_book()
            elif choice == 5:
                system.return_book()
            elif choice == 6:
                system.list_borrowers()
            elif choice == 7:
                print("Exiting...")
                db.close()
                break
            else:
                print("\nInvalid choice.\n")
        except ValueError:
            print("\nEnter a valid number.\n")

if __name__ == "__main__":
    main()

