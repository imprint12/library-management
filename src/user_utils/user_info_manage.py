from .helper_functions import *
import getpass
import os
# Accomplish the function of user management by himself as is required in "1.user management"
def manage_info(self):
    os.system('clear')
    curr = self.conn.cursor()
    try:
        query = "SELECT * FROM {} WHERE username=%s".format(self.group)
        curr.execute(query, (self.username,))
        info = curr.fetchone()
        print_user_info(info)

        print("q. Quit")
        print("1. Change password")
        print("2. (NEW TRUE NAME)")
        print("3. (NEW AGE)")
        print("4. (NEW GENDER('m' or 'f') )")

        command = input("\nEnter a command: ").strip()
        valid, cmd_n, cmd_arg = parse_command(command, 1, 3)

        if not valid:
            raise Exception("Invalid command input.")
        if cmd_n == q_ord:
            return

        if cmd_n == 1:
            change_pw_interface(self)
        elif cmd_n == 2:
            change_info(self, 'true_name', cmd_arg)
        elif cmd_n == 3:
            change_info(self, 'age', cmd_arg)
        else:
            change_info(self, 'gender', cmd_arg)

        self.conn.commit()

    except Exception as e:
        print(e)
    finally:
        curr.close()
        input("\nPress enter to continue.")

# Change the information of the employee by himself as is required
# in "1.user management" in the pdf file
def change_info(self, info, arg):
    curr = self.conn.cursor()
    try:
        query = "UPDATE {} SET {}=%s WHERE username=%s".format(self.group, info)
        curr.execute(query, (arg,self.username))
    except Exception as e:
        print(e)
    finally:
        curr.close()

# Change the password of the employee by himself as is required
# in "1.user management" in the pdf file
def change_pw_interface(self):
    while True:
        pw1 = getpass.getpass("Enter the new password: ")
        pw2 = getpass.getpass("Please confirm the password: ")
        if pw1 != pw2:
            print("Two inputs of password don't match!")
            continue
        else:
            break
    change_pw(self, pw1)


def change_pw(self, pw):
    curr = self.conn.cursor()
    try:
        query = "ALTER USER {} WITH  PASSWORD %s".format(self.username)
        curr.execute(query, (pw,))

    except Exception as e:
        raise e
    finally:
        curr.close()
