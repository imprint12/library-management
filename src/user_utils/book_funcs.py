from .helper_functions import *

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
    if cmd_n == q_ord:
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