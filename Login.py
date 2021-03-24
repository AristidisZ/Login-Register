from database import Database
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog , QApplication ,QMainWindow




class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('Login.ui',self)
        self.show()

        self.loginbutton.clicked.connect(self.loginfunction)
        self.createbutton.clicked.connect(self.createfunction)
        self.db=Database()



    def loginfunction(self):
        username=self.username.text()
        passw=self.passw.text()
        print(username,passw)
        self.db.authentication(username,passw)
        sys.exit(sys.argv)



    def createfunction(self):
        self.hide()
        self.window = SignUp()
        self.window.show()





class SignUp(QDialog):
    def __init__(self):
        super(SignUp, self).__init__()
        uic.loadUi('SignUp.ui',self)
        self.db = Database()

        self.signbutton.clicked.connect(self.createaccount)

    def createaccount(self):
        if self.passw.text()==self.confirmpassw.text():
            username = self.username.text()
            passw=self.passw.text()
            self.db.add_one(username,passw)
            print(username,passw)
            self.hide()
            self.window = Login()
            self.window.show()


if __name__ == '__main__':
    app =QApplication(sys.argv)
    window = Login()
    window.show()

    sys.exit(app.exec_())

    # # database.add_one("nikois", "1212")
    #  database.del_one()
    #  database.show_all()
