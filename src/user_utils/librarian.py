class Librarian:
    """docstring for Librarian."""
    def __init__(self, conn, username):
        self.conn = conn
        self.username = username

    def interface(self):
        print("Welcome, {}!".format(self.username))
        print()
        print()
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
            self.interface()

        command_ord = ord(command[0])
        if not 1 <= command_ord - '0' <= 6:
            print("Invalid command.")
            self.interface()

        
