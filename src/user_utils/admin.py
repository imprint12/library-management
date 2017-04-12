from .employee import Employee


class Admin(Employee):

    def interface(self):
        print("Welcome, {}!".format(self.username))
