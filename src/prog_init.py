from subprocess import call
import getpass
import psycopg2
from init.schemas import *

print('Warning!')
print('This script should only be run by the superintendent of the library to initiate the library management program.')
print('The database and admin account will be established during the execution.')
print('Root account may be need as well.')
run = input('Initiate the program?(y/n)')

if run not in ['y', 'Y']:
    exit(0)

call(["createdb", "library"])
print("Postgres database 'library' has been created.")

admin_name = input("Enter the user name of admin account: ")
while True:
    admin_pass1 = getpass.getpass("Enter the password of admin account: ")
    admin_pass2 = getpass.getpass("Please confirm the password: ")
    if admin_pass1 != admin_pass2:
        print("Two inputs of password don't match!")
        continue
    else:
        break

conn = psycopg2.connect("dbname=library")
curr = conn.cursor()

curr.execute("CREATE USER " + admin_name + " WITH ENCRYPTED PASSWORD %s", (admin_pass1,))
curr.execute("GRANT ALL PRIVILEGES ON DATABASE library to " + admin_name)
print("Admin account {} have been constructed.".format(admin_name))


create_book(curr)
create_on_shelf_book(curr)
create_restore(curr)
create_payment_bill(curr)
create_collection_bill(curr)
create_storage(curr)

conn.commit()

curr.close()
conn.close()
