import getpass
import psycopg2
from user_utils.admin import Admin
from user_utils.employee import Employee
import os

os.system('clear')
print('Welcome to the library management software!')

while True:
    try:
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        conn = psycopg2.connect(
            dbname='library', user=username, password=password)
        break

    except psycopg2.OperationalError:
        print("Failed to login.")
        retry = input("Retry?(y/n) ")

        if retry != 'y' and retry != 'Y':
            exit(-1)


curr = conn.cursor()
curr.execute("""SELECT %s IN
                            (SELECT username
                            FROM admin);
            """, (username,))
is_admin = curr.fetchone()[0]
curr.close()

if is_admin:
    adm = Admin(conn, username)
    adm.interface()

else:
    emply = Employee(conn, username)
    emply.interface()


conn.close()
