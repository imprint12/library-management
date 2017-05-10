from .helper_functions import *
from datetime import datetime
import os

# Show the transactions during some period as is required in "11.check bill"
def show_transactions(user):
    os.system('clear')
    print("Show all bills or specify a time interval")
    print("1.Show all bills.")
    print("2.Specify a time inteval.")

    valid, cmd_n, _ = parse_command(input("Command: "), 1, 2)

    if not valid:
        print("Invalid input.")
        return
    if cmd_n == 'q':
        return

    curr = user.conn.cursor()
    try:
        if cmd_n == 2:
            start = input("Enter the start date(YYYY-MM-DD): ")
            end = input("Enter the end date(YYYY-MM-DD): ")
            date_query = " WHERE dt BETWEEN %s AND %s;"
            start_date = parse_date(start)
            end_date = parse_date(end)

        pay_query = """
        SELECT *
        FROM payment_bill
        """
        rev_query = """
        SELECT *
        FROM revenue_bill
        """
        if cmd_n == 2:
            pay_query += date_query
            rev_query += date_query
            curr.execute(pay_query, (start, end))
            pay_bills = curr.fetchall()
            curr.execute(rev_query, (start, end))
            rev_bills = curr.fetchall()
        else:
            curr.execute(pay_query)
            pay_bills = curr.fetchall()
            curr.execute(rev_query)
            rev_bills = curr.fetchall()

        total_rev = sum([b[2] for b in rev_bills])
        total_pay = sum([b[2] for b in pay_bills])

        print_bills(pay_bills, 'payment')
        print_bills(rev_bills, 'revenue')
        print("\nTotal revenue: {}".format(total_rev))
        print("Total payment: {}".format(total_pay))
        print("Total balance: {}".format(total_rev - total_pay))

    except Exception as e:
        print("Error occured.")
        print(e)

    finally:
        curr.close()
        input("\nPress enter to continue")

# Pay for the books in the restock_order whose states are "unpaid"
def pay(user):
    os.system('clear')
    curr = user.conn.cursor()
    try:
        curr.execute("SELECT * FROM restock_order WHERE state = 'unpaid'")
        orders = curr.fetchall()
        if orders == []:
            print("No order is needed to be paid.")
            return

        print_orders(orders, "unpaid")

        command = input("\nEnter the order number to pay: ").strip()
        if not command.isdigit():
            raise ValueError("Invalid input.")

        command = int(command)
        order = None
        for o in orders:
            if command == o[0]:
                order = o
        if not order:
        #if command not in [o[0] for o in orders]:
            raise ValueError("Invalid input.")

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
        args = (datetime.now(), user.username)
        curr.execute(query, args)
        user.conn.commit()

        print("\nPayment succeeded.")

    except Exception as e:
        print("Error occured.")
        print(e)
    finally:
        curr.close()
        input("Press enter to continue.")

# Sell the books in the storage as is required in "9.purchase books"
def sell(user):
    os.system('clear')
    curr = user.conn.cursor()
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
                             user.username, max_no + 1, isbn))

        user.conn.commit()
        print("\nSelling succeeded.")

    except Exception as e:
        print("Error occured.")
        print(e)
    finally:
        curr.close()
        input("Press enter to continue.")
