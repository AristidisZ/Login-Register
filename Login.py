from database import Database
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
import sqlite3


class Login(QDialog):
    verbose = True

    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('Login.ui', self)
        self.show()

        self.loginbutton.clicked.connect(self.loginfunction)
        self.createbutton.clicked.connect(self.createfunction)
        self.db = Database()

        if self.verbose:
            self.admin_login_checkbox.setChecked(True)
        # self.a = QtWidgets.QCheckBox().setChecked(True)

    def loginfunction(self):
        if self.verbose:
            username = 'asd'
            passw = 'asd'
        else:
            username = self.username.text()
            passw = self.passw.text()
        print(username, passw)
        if self.admin_login_checkbox.isChecked():
            user = self.db.authentication(username, passw, "admin")
            if user:
                self.hide()
                self.window = Main_admin(user=user)
                self.window.show()

        else:
            if self.db.authentication(username, passw, "employee"):
                sys.exit(sys.argv)

    def createfunction(self):
        self.hide()
        self.window = SignUp()
        self.window.show()


class SignUp(QDialog):
    def __init__(self):
        super(SignUp, self).__init__()
        uic.loadUi('SignUp.ui', self)
        self.db = Database()

        self.signbutton.clicked.connect(self.createaccount)

    def createaccount(self):
        if self.passw.text() == self.confirmpassw.text():
            username = self.username.text()
            passw = self.passw.text()
            self.db.add_one(username, passw)
            print(username, passw)
            self.hide()
            self.window = Login()
            self.window.show()


class Main_admin(QDialog):

    def __init__(self, user):
        super(Main_admin, self).__init__()
        uic.loadUi('Main_admin.ui', self)
        self.user = user
        self.label_admin.setText(f"Welcome \n ID : {self.user[0]} \n User_name : {self.user[1]}")
        self.db = Database()
        self.refresh()

        self.load_button.clicked.connect(self.load_data)
        self.delete_employee_button.clicked.connect(self.del_one_employee)
        self.refresh_button.clicked.connect(self.refresh)
        self.search_button.clicked.connect(self.search)

        # self.tabWidget.setEnabled(True)

    def load_data(self):
        self.username = self.text_username_employee.text()
        self.password = self.text_password_employee.text()
        self.first_name = self.text_firstname_employee.text()
        self.last_name = self.text_lastname_employee.text()
        self.phone_number = self.text_phone_number_employee.text()
        for requirement in [self.username, self.password, self.first_name, self.last_name, self.phone_number]:
            if requirement == '':
                QtWidgets.QMessageBox.information(
                    self, 'Check for registration fields',
                    'Please fill all values.')
                return
        self.db.add_one_employee(self.username, self.password, self.first_name, self.last_name, self.phone_number)
        self.text_username_employee.clear()
        self.text_password_employee.clear()
        self.text_firstname_employee.clear()
        self.text_lastname_employee.clear()
        self.text_phone_number_employee.clear()
        self.refresh()


    def refresh(self):
        self.db.connect()
        query = self.db.c.execute("SELECT * FROM employee").fetchall()
        self.tableWidget.setRowCount(len(query))

        for row, item in enumerate(query, start=0):
            for column, value in enumerate(item):
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))

    def update_search_table(self, results):
        self.tableWidget.setRowCount(len(results))
        for row, item in enumerate(results, start=0):
            # print(f"row: {row} item: {item}")
            for column, value in enumerate(item):
                print(f"row: {row} item: {column}")
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))

    def search(self):
        self.db.connect()
        search = self.text_search.text()
        query = f"SELECT * FROM employee WHERE username LIKE '%{search}%' OR first_name LIKE '%{search}%' OR " \
                f"last_name LIKE '%{search}%' OR phone_number LIKE '%{search}%' "
        result = self.db.c.execute(query).fetchall()
        print(result)
        self.tableWidget.setRowCount(len(result))
        for row, item in enumerate(result, start=0):
            # print(f"row: {row} item: {item}")
            for column, value in enumerate(item):
                # print(f"row: {row} item: {column}")
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))

    def del_one_employee(self):
        self.db.connect()
        id = self.text_id.text()
        self.db.c.execute("DELETE FROM employee WHERE id = ?", (id,))
        self.db.commit()
        self.refresh()
        print(id)

        #
        # for row_number, row_data in enumerate(query):
        #     self.tableWidget, data in enumerate(row_number)
        #     for column_number, data in enumerate(row_data):
        #         self.tableWidget.setItem(row_number,column_number,QtWidgets)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Login()
    window.show()

    sys.exit(app.exec_())

    # # database.add_one("nikois", "1212")
    #  database.del_one()
    #  database.show_all()
