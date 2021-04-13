from database import Database
import sys
import numpy as np
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


class Main_admin(QMainWindow):

    def __init__(self, user):
        super(Main_admin, self).__init__()
        uic.loadUi('MainWindow_admin.ui', self)
        # uic.loadUi('Main_admin.ui', self)
        self.user = user
        self.label_admin.setText(f"Welcome \n ID : {self.user[0]} \n User_name : {self.user[1]}")
        self.db = Database()
        self.refresh()
        self.refresh_medication()
        self.refresh_clients()

        # employee buttons
        self.load_button.clicked.connect(self.create_employee)
        self.delete_employee_button.clicked.connect(self.del_one_employee)
        self.refresh_button.clicked.connect(self.refresh)
        self.search_button.clicked.connect(self.search)
        self.employee_table.itemClicked.connect(self.select_data_admin)

        # medication buttons
        # self.create_button_medication.clicked.connect(self.create_medication)
        self.refresh_button_medication.clicked.connect(self.refresh_medication)
        self.delete_medicine_button.clicked.connect(self.delete_one_medication)
        self.create_button_medication.clicked.connect(self.create_medication)


        # clients buttons
        self.clients_table.itemClicked.connect(self.select_data_client)
        self.create_button_client.clicked.connect(self.create_client)
        self.refresh_button_client.clicked.connect(self.refresh_clients)
        self.delete_client_button.clicked.connect(self.del_one_client)
        print("")




    def create_employee(self):
        self.username = self.text_username_employee.text()
        self.password = self.text_password_employee.text()
        self.first_name = self.text_firstname_employee.text()
        self.last_name = self.text_lastname_employee.text()
        self.age = self.text_age_employee.text()
        self.phone_number = self.text_phone_number_employee.text()
        self.department = self.text_department_employee.text()
        self.city = self.text_city_employee.text()
        self.address = self.text_address_employee.text()
        for requirement in [self.username, self.password, self.first_name, self.last_name, self.age, self.phone_number, self.department, self.city,self.address]:
            if requirement == '':
                QtWidgets.QMessageBox.information(
                    self, 'Check for registration fields',
                    'Please fill all values.')
                return
        self.db.add_one_employee(self.username, self.password, self.first_name, self.last_name, self.age, self.phone_number, self.department, self.city, self.address)
        self.text_username_employee.clear()
        self.text_password_employee.clear()
        self.text_firstname_employee.clear()
        self.text_lastname_employee.clear()
        self.text_age_employee.clear()
        self.text_phone_number_employee.clear()
        self.text_department_employee.clear()
        self.text_city_employee.clear()
        self.text_address_employee.clear()
        self.refresh()


    def select_data_admin(self):

        selected_items = np.unique([i.row() for i in self.employee_table.selectedItems()])
        # selected_items = np.unique([i for i in self.employee_table.selectedItems()])
        selected_ids = [self.employee_table.item(selected_row, 0).text() for selected_row in selected_items]
        print('selected rows', selected_items)
        print('selected ids', selected_ids)

    def refresh(self):
        self.db.connect()
        query = self.db.c.execute("SELECT * FROM employee").fetchall()
        self.employee_table.setRowCount(len(query))

        for row, item in enumerate(query, start=0):
            for column, value in enumerate(item):
                if column == 0:
                    print(value)
                self.employee_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))

    # def update_search_table(self, results):
    #     self.employee_table.setRowCount(len(results))
    #     for row, item in enumerate(results, start=0):
    #         # print(f"row: {row} item: {item}")
    #         for column, value in enumerate(item):
    #             print(f"row: {row} item: {column}")
    #             self.employee_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))

    def search(self):
        self.db.connect()
        search = self.text_search.text()
        query = f"SELECT * FROM employee WHERE username LIKE '%{search}%' OR first_name LIKE '%{search}%' OR " \
                f"last_name LIKE '%{search}%'OR age LIKE '%{search}%' OR phone_number LIKE '%{search}%' OR department LIKE '%{search}%' OR city LIKE '%{search}%' OR department LIKE '%{search}%'OR address LIKE '%{search}%' "
        result = self.db.c.execute(query).fetchall()
        print(result)
        self.employee_table.setRowCount(len(result))
        for row, item in enumerate(result, start=0):
            # print(f"row: {row} item: {item}")
            for column, value in enumerate(item):
                # print(f"row: {row} item: {column}")
                self.employee_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))

    def del_one_employee(self):
        self.db.connect()
        id = self.text_id.text()
        self.db.c.execute("DELETE FROM employee WHERE id = ?", (id,))
        self.db.commit()
        self.refresh()

    def create_medication(self):
        self.med_name = self.text_medication_name_medication.text()
        self.expiration_date = self.text_expiration_name_medication.text()
        self.category = self.text_category_medication.text()
        self.preparation = self.text_preparation_medication.text()
        self.quantity = self.text_quantity_medication.text()
        self.medicationbp = self.text_medicationbp_medication.text()
        self.medicationsp = self.text_medicationsp_medication.text()
        for requirement in [self.med_name,self.expiration_date,self.category,self.preparation,self.quantity,self.medicationbp,self.medicationsp]:
            if requirement == '':
                QtWidgets.QMessageBox.information(
                    self, 'Check for registration fields',
                    'Please fill all values.')
                return
        self.db.add_one_medicine(self.med_name,self.expiration_date,self.category,self.preparation,self.quantity,self.medicationbp,self.medicationsp)
        self.text_medication_name_medication.clear()
        self.text_expiration_name_medication.clear()
        self.text_category_medication.clear()
        self.text_prepeartion_medication.clear()
        self.text_quantity_medication.clear()
        self.text_medicationbp_medication.clear()
        self.text_medicationsp_medication.clear()

    def refresh_medication(self):
        self.db.connect()
        query = self.db.c.execute("SELECT * FROM medicine").fetchall()
        self.medication_table.setRowCount(len(query))

        for row, item in enumerate(query, start=0):
            for column, value in enumerate(item):
                self.medication_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))


    def select_data_medication(self):
        pass

    def delete_one_medication(self):
        self.db.connect()
        id = self.text_id_medicine.text()
        self.db.c.execute("DELETE FROM medication WHERE id = ?", (id,))
        self.db.commit()
        self.refresh()

    def create_client(self):
        self.username_client = self.text_username_client.text()
        self.password_client = self.text_password_client.text()
        self.client_store = self.text_client_store.text()
        self.client_name = self.text_client_name.text()
        self.client_city = self.text_client_city.text()
        self.client_address = self.text_client_address.text()
        self.client_postal_code = self.text_client_postal_code.text()
        self.client_email = self.text_client_email.text()
        self.client_phone = self.text_client_phone.text()
        for requirement in [self.username_client,self.password_client,self.client_store,self.client_name,self.client_city,self.client_address,self.client_postal_code,self.client_email,self.client_phone]:
            if requirement == '':
                QtWidgets.QMessageBox.information(
                    self, 'Check for registration fields',
                    'Please fill all values.')
                return
        self.db.add_one_client(self.username_client,self.password_client,self.client_store,self.client_name,self.client_city,self.client_address,self.client_postal_code,self.client_email,self.client_phone)
        self.text_username_client.clear()
        self.text_password_client.clear()
        self.text_client_store.clear()
        self.text_client_name.clear()
        self.text_client_city.clear()
        self.text_client_address.clear()
        self.text_client_postal_code.clear()
        self.text_client_email.clear()
        self.text_client_phone.clear()
        self.refresh_clients()


    def refresh_clients(self):
        self.db.connect()
        query = self.db.c.execute("SELECT * FROM clients").fetchall()
        self.clients_table.setRowCount(len(query))

        for row, item in enumerate(query, start=0):
            for column, value in enumerate(item):
                if column == 0:
                    print(value)
                self.clients_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))


    def select_data_client(self):
        pass


    def del_one_client(self):
        self.db.connect()
        id = self.text_id_client.text()
        self.db.c.execute("DELETE FROM client WHERE id = ?", (id,))
        self.db.commit()
        self.refresh()


# class add_clients_dialog(QDialog):

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Login()
    window.show()

    sys.exit(app.exec_())

    # # database.add_one("nikois", "1212")
    #  database.del_one()
    #  database.show_all()
