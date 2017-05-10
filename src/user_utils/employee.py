from datetime import datetime
from .helper_functions import *
from . import book_funcs
from . import bill_funcs
from . import restock_funcs
from . import user_info_manage
import os


class Employee:
    """docstring for Librarian."""

    def __init__(self, conn, username):
        self.conn = conn
        self.username = username
        self.group = 'employee'

    # Choose the function you want to implement as is listed below
    def interface(self):
        while True:
            os.system('clear')
            print("\n--------------------------------------------------")
            print("\nWelcome, {}!\n".format(self.username))

            print("q. Quit.")
            print("1. Search for books.")
            print("2. Change information of books.")
            print("3. Restock.")
            print("4. Pay for a restocking order.")
            print("5. Cancel a restocking order.")
            print("6. Put arrived books on shelf.")
            print("7. Selling books.")
            print("8. Show transactions' records.")
            print("9. Manage the information of yourself.")

            command = input("Enter command: ")
            # if (command == ""):
            #    print("Empty command.")
            #    continue
#
            # if (command[0] == "q"):
            #    self.conn.close()
            #    return
#
            #command_ord = ord(command[0])
            # if not 1 <= command_ord - ord('0') <= 7:
            #    print("Invalid command.")
            #    self.interface()
            #cmd_n = command_ord - ord('0')

            valid, cmd_n, cmd_arg = parse_command(command, 1, 9)

            if not valid:
                raise ValueError("Invalid input.")

            if cmd_n == q_ord:
                return

            if cmd_n == 1:
                self.search()
            elif cmd_n == 2:
                self.change_info()
            elif cmd_n == 3:
                self.restock()
            elif cmd_n == 4:
                self.pay()
            elif cmd_n == 5:
                self.cancel()
            elif cmd_n == 6:
                self.put_books()
            elif cmd_n == 7:
                self.sell()
            elif cmd_n == 8:
                self.show_transactions()
            elif cmd_n == 9:
                self.manage_info()


    # Define the functions briefly and these functions
    # will be accomplished in specific source files
    def search(self):
        book_funcs.search(self)

    def change_info(self):
        book_funcs.change_info(self)

    def add_book_info(self):
        book_funcs.add_book_info(self)

    def restock(self):
        restock_funcs.restock(self)

    def cancel(self):
        restock_funcs.cancel(self)

    def put_books(self):
        restock_funcs.put_books(self)

    def pay(self):
        bill_funcs.pay(self)

    def sell(self):
        bill_funcs.sell(self)

    def show_transactions(self):
        bill_funcs.show_transactions(self)

    def manage_info(self):
        user_info_manage.manage_info(self)
