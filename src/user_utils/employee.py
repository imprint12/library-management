

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

        cmd_n, arg = cmd[0].strip(), cmd[1].strip()


        query = """
        SELECT *
        FROM book_info NATURAL LEFT OUTER JOIN storage NATURAL JOIN writes
        WHERE"""
        if (cmd_n == '1'):
            query += " ISBN = %s"
        elif (cmd_n == '2'):
            query += " title = %s"
        elif (cmd_n == '3'):
            query += " writer = %s"
        elif (cmd_n == '4'):
            query += " publisher = %s"
        print(arg)
        curr = self.conn.cursor()
        curr.execute(query, (arg,))
        books = curr.fetchall()
        print(books)
        for book in books:
            print(book)
        curr.close()

    def restock(self):
        pass
