from .employee import Employee
from . import search

class Admin(Employee):

    def interface(self):
        print("\n--------------------------------------------------")
        print("\nWelcome, {}!\n".format(self.username))

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
            self.conn.close()
            return
        if (command == ""):
            print("Empty command.")
            self.interface()

        command_ord = ord(command[0])
        if not 1 <= command_ord - ord('0') <= 6:
            print("Invalid command.")
            self.interface()
        command_num = command_ord - ord('0')

        if command_num == 1:
            self.search()
