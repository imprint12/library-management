from .library import Librarian

class Admin(Librarian):
    def __init__(self, conn, username):
        super.__init__(conn, username)


    def interface(self):
        print("Welcome, {}!".format(self.username))
