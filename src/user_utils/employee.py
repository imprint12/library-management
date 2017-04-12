from . import search


class Employee:
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
        if not 1 <= ord(command_ord) - ord('0') <= 6:
            print("Invalid command.")
            self.interface()
        command_num = ord(command_ord) - ord('0') + 1

    def search(self):

        print("\n1. (ISBN NUMBER)")
        print("2. (TITLE)")
        print("3. (WRITER'S NAME)")
        print("4. (PUBLISHER)\n\n")

        print("Please enter one of the commands above.")
        print("For example: 1. Introduction to Algorithms\n")
        command = input("Command: ")

        cmd = command.split('.')
        if len(cmd) != 2 or not('1' <= cmd[0] <= '4'):
            print("Invalid command.")
            self.interface()

        cmd_n, arg = cmd[0], cmd[1].strip()

        if cmd_n == '1':
            search.isbn(self.conn, arg)
        elif cmd_n == '2':
            search.title(self.conn, arg)
        elif cmd_n == '3':
            search.writer(self.conn, arg)
        else:
            search.publisher(self.conn, arg)

    def restock(self):
        pass
