from . import Librarian

class Admin():
    def __init__(self, conn, username):
        super.__init__(conn, username)


    def interface(self):
        "Welcome, {}!"
