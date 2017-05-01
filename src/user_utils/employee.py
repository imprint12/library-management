from datetime import datetime

from . import book_funcs
from . import bill_funcs
from . import restock_funcs


class Employee:
    """docstring for Librarian."""

    def __init__(self, conn, username):
        self.conn = conn
        self.username = username

    def interface(self):
        while True:
            print("Welcome, {}!".format(self.username) + "\n\n")
            print("q. Quit.")
            print("1. Search for books.")
            print("2. Change information of books.")
            print("3. Restock.")
            print("4. Pay for a restocking bill.")
            print("5. Put arrived books on shelf.")
            print("6. Selling books.")
            print()

            command = input("Enter command: ")
            if (command == "q"):
                conn.close()
                exit(0)
            if (command == ""):
                print("Empty command.")
                continue

            command_ord = ord(command[0])
            if not 1 <= command_ord - ord('0') <= 6:
                print("Invalid command.")
                self.interface()
            command_num = command_ord - ord('0')

            if command_num == 1:
                self.search()
            elif command_num == 2:
                self.change_info()
            elif command_num == 3:
                self.restock()
            elif command_num == 4:
                self.pay()
            elif command_num == 5:
                self.put_books()
            else:
                self.sell()

    def search(self):
        book_funcs.search(self)

    def change_info(self):
        book_funcs.change_info(self)

    def add_book_info(self):
        book_funcs.add_book_info(self)

    def restock(self):
        restock_funcs.restock(self)

    def put_books(self):
        restock_order.put_books(self)

    def pay(self):
        bill_funcs.pay(self)

    def sell(self):
        bill_funcs.sell(self)

    def show_transactions(self):
        bill_funcs.show_transactions(self)
