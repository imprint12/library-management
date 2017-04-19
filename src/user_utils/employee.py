

class Employee:
    """docstring for Librarian."""

    def __init__(self, conn, username):
        self.conn = conn
        self.username = username

    def interface(self):
        while True:
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
                continue

            command_ord = ord(command[0])
            if not 1 <= ord(command_ord) - ord('0') <= 6:
                print("Invalid command.")
                continue
            command_num = ord(command_ord) - ord('0') + 1

    def search(self):

        print("\n1. (ISBN NUMBER)")
        print("2. (TITLE)")
        print("3. (WRITER'S NAME)")
        print("4. (PUBLISHER)\n\n")

        print("Please enter one of the commands above.")
        print("For example: 2. Introduction to Algorithms\n")
        command = input("Command: ")

        cmd = command.split('.')
        if len(cmd) != 2 or not('1' <= cmd[0] <= '4'):
            print("Invalid command.")
            return

        cmd_n, arg = cmd[0].strip(), cmd[1].strip().lower()

        query = """
        SELECT *
        FROM book_info NATURAL LEFT OUTER JOIN storage
        WHERE"""
        if (cmd_n == '1'):
            query += " ISBN = %s"
        elif (cmd_n == '2'):
            query += " title = %s"
        elif (cmd_n == '3'):
            query += " %s = ANY (writer)"
        elif (cmd_n == '4'):
            query += " publisher = %s"
        curr = self.conn.cursor()
        curr.execute(query, (arg,))
        books = curr.fetchall()

        print("\nSearch result:\n")
        for book in books:
            print("ISBN: " + book[0])
            print("Title: " + book[1].title())
            print("Writers:", end='')
            for wt in book[2]:
                print(' ' + wt.title(), end=',')
            print("\b ")
            print("Publisher: " + book[3])
            print("Price: " + str(book[4]))
            print("Storage number: " + str(book[5]))
            print()
        curr.close()

    def change_info(self):
        isbn = input("Enter the ISBN of the book that need to be changed: ")
        curr = self.conn.cursor()

        print("Enter one of the following commands:")
        print("1. (new book name)")
        print("2. (new writers, splited by commas)")
        print("3. (new pulisher)")
        print("4. (new price)")

        command_table = {1: 'title', 2: 'writer', 3: 'publisher'}

        command = input("Command: ")
        cmd = command.split('.')
        if len(cmd) != 2 or not('1' <= cmd[0] <= '4'):
            print("Invalid command.")
            return
        cmd_n, arg = ord(cmd[0].strip()) - ord('0'), cmd[1].strip().lower()

        if cmd_n == 4:
            try:
                curr.execute("""
                UPDATE storage
                set price = %s
                WHERE ISBN = %s
                """, (arg, isbn))
                conn.commit()
            except:
                print("Update Error!")

        else:
            query = """
            UPDATE book_info
            set {} = %s
            WHERE ISBN = %s
            """
            try:
                print(query.format(command_table[cmd_n]))
                curr.execute(query.format(command_table[cmd_n]), (arg, isbn))
                self.conn.commit()
            except:
                print("Update Error!")

        curr.close()

    def restock(self):
        isbn = input("Enter the ISBN of the book that need to be restocked: ")
        curr = self.conn.cursor()
        num = input("How many books to order? ")
        price = input("What's the price of one book? ")

        total_price = num * price

        try:
            curr.execute("""
            SELECT max(order_no)
            FROM restock_order
            """)
            max_no = curr.fetchall
            if not max:
                max_no = 0
            else:
                max_no = max[0]

            curr.execute("""
            INSERT INTO restock_order VALUES
            (%s, %s, %s, %s, 'nonpaid', %s)
            """, (max_no + 1, isbn, num, total_price, self.username))

        except Exception as e:
            print("Error occured")
            print(e)

    def pay(self):
        pass

    def put_books(self):
        pass

    def sell(self):
        pass
