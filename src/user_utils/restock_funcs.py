from .helper_functions import *
from .book_funcs import add_book_info
import os

# Check whether the books to be reatocked are in storage


def restock(user):
    os.system('clear')
    isbn = input(
        "Enter the ISBN of the book that need to be restocked: ").strip()
    curr = user.conn.cursor()

    try:

        curr.execute("SELECT %s in (SELECT ISBN from book_info);", (isbn,))
        in_library = curr.fetchone()[0]
        if not in_library:
            print("This kind of books is currently not in the library.")
            print("You need to give information on it to order the books.")
            add_book_info(user, isbn)

        num = int(input("How many books to order? "))
        price = float(input("What's the price of one book? "))

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
        """, (max_no + 1, isbn, num, total_price, user.username))
        user.conn.commit()
        print("\nOperation succeded.")

    except Exception as e:
        print("Error occured.")
        print(e)
    finally:
        curr.close()
        input("Press enter to continue.")


def cancel(user):
    os.system('clear')
    curr = user.conn.cursor()
    try:
        curr.execute("SELECT * FROM restock_order WHERE state = 'unpaid';")
        orders = curr.fetchall()
        if orders == []:
            print("No unpaid orders")
        else:
            print_orders(orders, 'unpaid')
            command = input("\nEnter the order number to cancil: ").strip()
            if not command.isdigit():
                raise Exception("Unvalid Input")
            command = int(command)
            command = int(command)

            order = None
            for o in orders:
                if command == o[0]:
                    order = o
            if not order:
                # if command not in [o[0] for o in orders]:
                raise ValueError("Invalid input.")
            curr.execute(
                "UPDATE restock_order SET state = 'cancel' WHERE order_no=%s", (command,))

            user.conn.commit()
            print("Cancel succeeded.")
    except Exception as e:
        print("Error occured.")
        print(e)
    finally:
        curr.close()
        input("Press enter to continue.")


# Put books in the restock_order which state is "paid" on shelf and set state "put" in restock_order
# as is required in "8.add new books" in the pdf file
def put_books(user):
    os.system('clear')
    curr = user.conn.cursor()
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

        command = input(
            "\nEnter the order number to put those books on shelf: ").strip()
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
        user.conn.commit()
        print("\nOperation succeded.")

    except Exception as e:
        print("Error occured.")
        print(e)
    finally:
        curr.close()
        input("Press enter to continue.")
