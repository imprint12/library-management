from .helper_functions import *
from .book_funcs import add_book_info
import os


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
        """, (max_no + 1, isbn, num, total_price, user.username))
        user.conn.commit()
        print("\nOperation succeded.")

    except Exception as e:
        print("Error occured.")
        print(e)
    finally:
        curr.close()
        input("Press enter to continue.")


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
        user.conn.commit()
        print("\nOperation succeded.")

    except Exception as e:
        print("Error occured.")
        print(e)
    finally:
        curr.close()
        input("Press enter to continue.")
