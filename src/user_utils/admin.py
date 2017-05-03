from .employee import Employee
from .helper_functions import *
import os
from . import admin_manage

class Admin(Employee):

    def __init__(self, conn, username):
        self.conn = conn
        self.username = username
        self.group = 'admin'


    def interface(self):
        while True:
            os.system('clear')

            print("\n--------------------------------------------------")
            print("\nWelcome, {}!\n".format(self.username))

            print("q. Quit.")
            print("1. Search for books.")
            print("2. Change information of books.")
            print("3. Restock.")
            print("4. Pay for a restocking bill.")
            print("5. Put arrived books on shelf.")
            print("6. Selling books.")
            print("7. Show transactions' records.")
            print("8. Manage the information of yourself.")
            print("9. Manage accounts of employees.\n")

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
                print("Invalid input.")
                return
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
                self.put_books()
            elif cmd_n == 6:
                self.sell()
            elif cmd_n == 7:
                self.show_transactions()
            elif cmd_n == 8:
                self.manage_info()
            else:
                self.admin_manage()

    def admin_manage(self):
        admin_manage.admin_manage(self)
