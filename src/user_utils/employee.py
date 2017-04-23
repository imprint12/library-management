from datetime import datetime


def print_books(books):
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


def print_orders(orders, info):
    print("These are the " + info + " orders:\n")
    for order in orders:
        print("Order number: " + str(order[0]))
        print("ISBN: " + order[1])
        print("Book number: " + str(order[2]))
        print("Total Price: " + str(order[3]))
        print("Ordered by: " + str(order[5]) + "\n")


def parse_command(command, lower_bound, upper_bound):
    cmd = list(map(lambda s: s.strip().lower(), command.split('.')))

    valid = False

    cmd_n = ord(cmd[0]) - ord('0')

    if cmd[0] == 'q' or lower_bound <= cmd_n <= upper_bound:
        valid = True

    cmd_arg = None
    if len(cmd) > 1:
        if ',' in cmd[1] > 1:
            cmd_arg = cmd[1].split(',')
        else:
            cmd_arg = cmd[1]

    return valid, cmd_n, cmd_arg


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
        print("4. (PUBLISHER)")
        print("5. All books\n\n")

        print("Please enter one of the commands above.")
        print("For example: 2. Introduction to Algorithms\n")
        command = input("Command: ")

        #cmd = command.split('.')
        # if len(cmd) != 2 or not('1' <= cmd[0] <= '5'):
        #    print("Invalid command.")
        #    return

        #cmd_n, arg = cmd[0].strip(), cmd[1].strip().lower()
        valid, cmd_n, arg = parse_command(command, 1, 5)
        if not valid:
            print("Invalid input.")
            return

        try:
            query = """
            SELECT *
            FROM book_info NATURAL LEFT OUTER JOIN storage
            WHERE"""
            if (cmd_n == 1):
                query += " ISBN = %s"
            elif (cmd_n == 2):
                query += " title = %s"
            elif (cmd_n == 3):
                query += " %s = ANY (writer)"
            elif (cmd_n == 4):
                query += " publisher = %s"
            elif (cmd_n == 5):
                query += " true"
            curr = self.conn.cursor()
            curr.execute(query, (arg,))
            books = curr.fetchall()

            print_books(books)

            print("\nSearch result:\n")

        except Exception as e:
            print("Error occured when searching.")
            print(e)

        finally:
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
        if cmd_n == 2:
            arg = list(map(lambda x: x.strip().lower(), arg.split(',')))

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
                print(e)
            finally:
                curr.close()

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
                print(e)
            finally:
                curr.close()

    def add_book_info():
        isbn = input("ISBN: ")
        writers = input("Writers(split by commas): ")
        publisher = input("Publisher: ")

        writers = list(map(lambda x: x.strip().lower(), writers.split(',')))

        try:
            curr = self.conn.cursor()
            curr.execute("INSERT INTO book_info VALUES (%s, %s, %s)",
                         isbn, writers, publisher)
        except Exception as e:
            print("Error occured when adding a book info.")
            print(e)
        finally:
            curr.close()

    def restock(self):
        isbn = input(
            "Enter the ISBN of the book that need to be restocked: ").strip()
        curr = self.conn.cursor()

        try:

            curr.execute("SELECT %s in (SELECT ISBN from book_info);", (isbn,))
            in_library = curr.fetchone()[0]
            if not in_library:
                print("This kind of books is currently not in the library.")
                print("You need to give information on it to order the books.")
                self.add_book_info()

            num = int(input("How many books to order? "))
            price = int(input("What's the price of one book? "))

            total_price = num * price
            curr.execute("""
            SELECT max(order_no)
            FROM restock_order;
            """)
            max_no = curr.fetchone()[0]
            if not max_no:
                max_no = 0
            curr.execute("""
            INSERT INTO restock_order VALUES
            (%s, %s, %s, %s, 'unpaid', %s)
            """, (max_no + 1, isbn, num, total_price, self.username))
            self.conn.commit()

        except Exception as e:
            print("Error occured.")
            print(e)
        finally:
            curr.close()

    def pay(self):
        curr = self.conn.cursor()
        try:
            curr.execute("SELECT * FROM restock_order WHERE state = 'unpaid'")
            orders = curr.fetchall()
            if orders == []:
                print("No order is needed to be paid.")
                return

            print_orders(orders, "unpaid")

            command = input("\nEnter the order number to pay: ").strip()
            if not command.isdigit():
                print("Invalid input.")
                return
            command = int(command)
            if command not in [o[0] for o in orders]:
                print("Invalid input.")
                return

            curr.execute("""
            SELECT max(bill_no)
            FROM payment_bill;
            """)
            max_no = curr.fetchone()[0]
            if not max_no:
                max_no = 0

            query = """
            BEGIN;
            UPDATE restock_order
            SET state = 'paid'
            WHERE order_no = {};

            INSERT INTO payment_bill
            VALUES ({}, %s, {}, %s);

            INSERT INTO restock_pay
            VALUES ({}, {});

            COMMIT;
            """.format(command, max_no + 1, order[3], command, max_no + 1)

            order = [o for o in orders if o[0] == command][0]
            args = (datetime.now(), self.username)
            curr.execute(query, args)

        except Exception as e:
            print("Error occured.")
            print(e)
        finally:
            curr.close()

    def put_books(self):
        curr = self.conn.cursor()
        try:
            curr.execute("""
            SELECT *
            FROM restock_order
            WHERE state = 'paid'
            """)
            orders = curr.fetchall()

            if orders == []:
                print("No books are needed to be put on shelf.")
                return
            print_orders(orders, "paid")

            command = input("\nEnter the order number to pay: ").strip()
            if not command.isdigit():
                print("Invalid input.")
                return
            command = int(command)
            if command not in [o[0] for o in orders]:
                print("Invalid order number.")
                return

            order = [o for o in orders if o[0] == command][0]

            query = """
            BEGIN;
            UPDATE restock_order
            SET state = 'put'
            WHERE order_no = {};

            UPDATE storage
            SET num = num + {}
            WHERE isbn = %s;

            COMMIT;
            """.format(order[0], order[2])

            curr.execute(query, (order[1],))

        except Exception as e:
            print("Error occured.")
            print(e)
        finally:
            curr.close()

    def sell(self):
        curr = self.conn.cursor()
        try:
            curr.execute("""
            SELECT max(bill_no)
            FROM revenue_bill;
            """)
            max_no = curr.fetchone()[0]
            if not max_no:
                max_no = 0
            isbn = input(
                "Enter the ISBN of the book that is going to be selled: ")
            number = int(
                input("Enter the number of the book that is going to be selled: "))

            curr.execute("SELECT * FROM storage WHERE ISBN=%s", (isbn,))
            book_storeage = curr.fetchone()

            if book_storeage == None:
                raise ValueError("This book doesn't exist in the library.")

            if book_storeage[2] < number:
                raise ValueError("There not enough books to sell.")

            total_price = book_storeage[1] * number

            query = """
            BEGIN;
            UPDATE storage
            SET num = num - {}
            WHERE ISBN = %s;

            INSERT INTO revenue_bill
            VALUES (%s, %s, {}, %s);

            INSERT INTO revenue_storage
            VALUES (%s, %s, {});

            COMMIT;
            """.format(number, total_price, number)

            curr.execute(query, (isbn, max_no + 1, datetime.now(),
                                 self.username, max_no + 1, isbn))

        except Exception as e:
            print("Error occured.")
            print(e)
        finally:
            curr.close()
