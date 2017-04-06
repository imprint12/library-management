import getpass
import psycopg2

print('Welcome to the library management software!')

while True:
    try:
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        conn = psycopg2.connect(dbname='library', user=username, password=password)
        break

    except psycopg2.OperationalError:
        print("Failed to login.")
        retry = input("Retry?(y/n) ")

        if retry != 'y' and retry != 'Y':
            exit(-1)


curr = conn.cursor()