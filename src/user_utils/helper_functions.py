from datetime import datetime
q_ord = ord('q') - ord('0')

# A helper function to print info of books.


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

# A helper function to print info of some orders.


def print_orders(orders, info):
    print("These are the " + info + " orders:\n")
    for order in orders:
        print("Order number: " + str(order[0]))
        print("ISBN: " + order[1])
        print("Book number: " + str(order[2]))
        print("Total Price: " + str(order[3]))
        print("Ordered by: " + order[5] + "\n")


# A helper function to print info of bills.
def print_bills(bills, info):
    print("These are the " + info + " bills:\n")
    for bill in bills:
        print("Bill number: " + str(bill[0]))
        print("Date: " + str(bill[1]))
        print("Total amount: " + str(bill[2]))
        print("Operated by: " + bill[3] + "\n")


# Parse and return whether the user input is valid and other infomations.


def parse_command(command, lower_bound, upper_bound):
    cmd = list(map(lambda s: s.strip().lower(), command.split('.')))
    valid = False
    cmd_n = ord(cmd[0]) - ord('0')

    if command == "":
        return False, None, None
    if cmd[0] == 'q' or lower_bound <= cmd_n <= upper_bound:
        valid = True

    cmd_arg = None
    if len(cmd) > 1:
        if ',' in cmd[1]:
            cmd_arg = cmd[1].split(',')
        else:
            cmd_arg = cmd[1]

    return valid, cmd_n, cmd_arg

# Parse user input data string and return a python datetime object.


def parse_date(arg):
    args = arg.split('-')
    if len(args) != 3:
        raise ValueError("Wrong date input.")
    args = [int(x) for x in args]
    return (datetime(args[0], args[1], args[2]))


def print_user_info(info):
    print("\nUsername: {}".format(info[0]))
    print("True Name: {}".format(info[1].title()))
    print("ID: {}".format(info[2]))
    print("Age: {}".format(info[3]))
    if info[4] == 'm':
        gender = 'Male'
    else:
        gender = 'Female'
    print("Gender: {}".format(gender) + "\n")
