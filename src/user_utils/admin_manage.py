from .helper_functions import *
import os
import getpass


# Accomplish the function of user management required in "1.user
# management" in the pdf file
def admin_manage(user):
    os.system('clear')
    print("1.(USERNAME) Show user's infomation.")
    print("2.(USERNAME) Change user's information.")
    print("3.(USERNAME) Change user's password.")
    print("4.Create a new user.")
    print("5.(USERNAME) Delete a user account.\n")
    command = input("Command: ")
    try:
        valid, cmd_n, cmd_arg = parse_command(command, 1, 5)
        if not valid:
            raise ValueError("Invalid command input.")

        if cmd_n == 1:
            admin_show_info(user, cmd_arg)
        elif cmd_n == 2:
            admin_change_info(user, cmd_arg)
        elif cmd_n == 3:
            admin_change_pw(user, cmd_arg)
        elif cmd_n == 4:
            create_user(user)
        else:
            delete_user(user, cmd_arg)

    except Exception as e:
        print("Error occurred.")
        print(e)
    finally:
        input("\nPress enter to continue.")

# Display the information of all employees by admin as is required in
# "1.user management" in the pdf file
def admin_show_info(admin, username):
    curr = admin.conn.cursor()
    try:
        query = "SELECT * FROM employee WHERE "
        if not username:
            query += "true"
            curr.execute(query)
            users = curr.fetchall()
            for user in users:
                print_user_info(user)
        else:
            query += "username = %s"
            curr.execute(query, (username,))
            user = curr.fetchone()
            if not user:
                raise Exception("Username doesn't exist.")
            print_user_info(user)

    except Exception as e:
        raise
    finally:
        curr.close()

# Change the information of employees by the admin as is required
# in "1.user management" in the pdf file
def admin_change_info(admin, username):
    curr = admin.conn.cursor()
    try:
        query = "SELECT * FROM employee WHERE username=%s"
        curr.execute(query, (username,))
        info = curr.fetchone()
        if not info:
            raise Exception("Username doesn't exist.")
        print_user_info(info)

        print("q. Quit")
        print("1. (NEW TRUE NAME)")
        print("2. (NEW AGE)")
        print("3. (NEW GENDER('m' or 'f') )")

        command = input("\nEnter a command: ").strip()
        valid, cmd_n, cmd_arg = parse_command(command, 1, 3)
        if not valid:
            raise Exception("Invalid command input.")
        if cmd_n == q_ord:
            return

        if cmd_n == 1:
            info_type = 'true_name'
        elif cmd_n == 2:
            info_type = 'age'
        elif cmd_n == 3:
            info_type = 'gender'
        curr.execute("UPDATE employee SET {}= %s WHERE username=%s".format(
            info_type), (cmd_arg, username))
        admin.conn.commit()
        print("Operation succeeded.")
    except Exception as e:
        raise e
    finally:
        curr.close()

# Change the password of the employee by the admin as is required
# in "1.user management" in the pdf file
def admin_change_pw(admin, username):
    curr = admin.conn.cursor()
    try:
        curr.execute(
            "SELECT %s in (SELECT username FROM employee)", (username,))
        exist = curr.fetchone()
        if not exist[0]:
            raise Exception("Username doesn't exist.")
        while True:
            pw1 = getpass.getpass("Enter the new password: ")
            pw2 = getpass.getpass("Please confirm the password: ")
            if pw1 != pw2:
                print("Two inputs of password don't match!")
                continue
            else:
                break
        query = "ALTER USER employee WITH  PASSWORD %s"
        curr.execute(query, (pw1,))
        admin.conn.commit()
        print("Operation succeeded.")

    except Exception as e:
        raise
    finally:
        curr.close()

# Create an employee account by the admin as is required in "1.user management"
# in the pdf file
def create_user(admin):
    curr = admin.conn.cursor()

    try:
        username = input("Username: ").strip()
        while True:
            pw1 = getpass.getpass("Enter the new password: ")
            pw2 = getpass.getpass("Please confirm the password: ")
            if pw1 != pw2:
                print("Two inputs of password don't match!")
                continue
            else:
                break
        # calculate the new employee id
        curr.execute("SELECT max(id) FROM employee")
        n_id = curr.fetchone()[0]
        if not n_id:
            n_id = 1
        else:
            n_id += 1
        true_name = input("True name: ").strip()
        age = input("Age: ").strip()
        gender = input("Gender(f or m): ").strip()

        curr.execute("CREATE USER {} WITH ENCRYPTED PASSWORD %s IN GROUP employee".format(
            username), (pw1,))
        curr.execute("INSERT INTO employee VALUES (%s, %s,%s, %s, %s)",
                     (username, true_name, n_id, age, gender))
        admin.conn.commit()
    except Exception as e:
        raise
    finally:
        curr.close()

# Delete certain employee account by the admin as is required in "1.user management"
def delete_user(admin, username):
    curr = admin.conn.cursor()
    try:
        curr.execute("SELECT * FROM employee WHERE username=%s", (username,))
        info = curr.fetchone()
        if not info:
            raise Exception("Username doesn't exist.")
        print_user_info(info)

        query = """
        BEGIN;
        DROP USER {};
        DELETE FROM employee
        WHERE username = %s;
        COMMIT;
        """.format(username)
        curr.execute(query, (username,))

        admin.conn.commit()
        print("This account has been deleted.")
    except Exception as e:
        raise
    finally:
        curr.close()
