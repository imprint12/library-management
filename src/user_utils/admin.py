from .employee import Employee
from . import search

class Admin(Employee):

    def interface(self):
        while True:
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

            command = input("Enter command: ").strip()
            if (command == ""):
                print("Empty command.")
                continue

            if (command[0] == "q"):
                self.conn.close()
                return

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
