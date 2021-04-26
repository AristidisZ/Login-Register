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
    selected_ids = []

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
        self.show_dialog_employee_button.clicked.connect(self.show_dialog_employee)
        self.update_employee_buttton.clicked.connect(self.update_employee)
        # self.load_button.clicked.connect(self.create_employee)
        self.delete_employee_button.clicked.connect(self.del_one_employee)
        self.refresh_button.clicked.connect(self.refresh)
        self.search_button.clicked.connect(self.search)
        self.employee_table.itemClicked.connect(self.select_data_employee)

        # medication buttons
        # self.create_button_medication.clicked.connect(self.create_medication)
        self.refresh_button_medication.clicked.connect(self.refresh_medication)
        self.delete_medicine_button.clicked.connect(self.delete_one_medication)
        self.create_button_medication.clicked.connect(self.create_medication)


        # clients buttons
        self.clients_table.itemClicked.connect(self.select_data_client)
        self.show_dialog_client_button.clicked.connect(self.show_dialog_client)
        self.update_employee_buttton.clicked.connect(self.update_client)
        self.refresh_button_client.clicked.connect(self.refresh_clients)
        self.delete_client_button.clicked.connect(self.del_one_client)
        self.clients_table.itemClicked.connect(self.select_data_client)



    def select_data_employee(self):

        selected_items = np.unique([i.row() for i in self.employee_table.selectedItems()])
        self.selected_ids = [self.employee_table.item(selected_row, 0).text() for selected_row in selected_items]
        # print('selected rows', selected_items)
        # print('selected ids', self.selected_ids)
        id=(self.selected_ids)
        for i in range(0, len(id)):
            self.selected_ids[i] = int(id[i])
        print("Modified/id list is : " + str(id))


    def select_data_client(self):
        selected_items = np.unique([i.row() for i in self.clients_table.selectedItems()])
        self.selected_ids_client = [self.clients_table.item(selected_row, 0).text() for selected_row in selected_items]
        print('selected rows', selected_items)
        print('selected ids', self.selected_ids_client)
        print('nai')


    def refresh(self):
        self.db.connect()
        query = self.db.c.execute("SELECT * FROM employee").fetchall()
        self.employee_table.setRowCount(len(query))

        for row, item in enumerate(query, start=0):
            for column, value in enumerate(item):
                # if column == 0:
                    # print(value)
                self.employee_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))

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
        self.text_id.clear()
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
        self.text_preparation_medication.clear()
        self.text_quantity_medication.clear()
        self.text_medicationbp_medication.clear()
        self.text_medicationsp_medication.clear()
        self.refresh_medication()

    def refresh_medication(self):
        self.db.connect()
        query = self.db.c.execute("SELECT * FROM medicine").fetchall()
        self.medication_table.setRowCount(len(query))

        for row, item in enumerate(query, start=0):
            for column, value in enumerate(item):
                self.medication_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))

    def search_medication(self):
        self.db.connect()
        search = self.text_search_medication.text()
        query = f"SELECT * FROM medicine WHERE med_name LIKE '%{search}%' OR expiration_date LIKE '%{search}%' OR " \
                f"category LIKE '%{search}%'OR preparation LIKE '%{search}%' OR quantity LIKE '%{search}%' OR med_buy_price LIKE '%{search}%' OR med_sell_price LIKE '%{search}%'"
        result = self.db.c.execute(query).fetchall()
        print(result)
        self.medication_table.setRowCount(len(result))
        for row, item in enumerate(result, start=0):
            # print(f"row: {row} item: {item}")
            for column, value in enumerate(item):
                # print(f"row: {row} item: {column}")
                self.medication_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))
        self.refresh_medication()

    def select_data_medication(self):
        pass

    def delete_one_medication(self):
        self.db.connect()
        id = self.text_id_medicine.text()
        self.db.c.execute("DELETE FROM medicine WHERE id = ?", (id,))
        self.db.commit()
        self.text_id_medicine.clear()
        self.refresh_medication()
    #
    # def create_client(self):
    #     self.username_client = self.text_username_client.text()
    #     self.password_client = self.text_password_client.text()
    #     self.client_store = self.text_client_store.text()
    #     self.client_name = self.text_client_name.text()
    #     self.client_city = self.text_client_city.text()
    #     self.client_address = self.text_client_address.text()
    #     self.client_postal_code = self.text_client_postal_code.text()
    #     self.client_email = self.text_client_email.text()
    #     self.client_phone = self.text_client_phone.text()
    #     for requirement in [self.username_client,self.password_client,self.client_store,self.client_name,self.client_city,self.client_address,self.client_postal_code,self.client_email,self.client_phone]:
    #         if requirement == '':
    #             QtWidgets.QMessageBox.information(
    #                 self, 'Check for registration fields',
    #                 'Please fill all values.')
    #             return
    #     self.db.add_one_client(self.username_client,self.password_client,self.client_store,self.client_name,self.client_city,self.client_address,self.client_postal_code,self.client_email,self.client_phone)
    #     self.text_username_client.clear()
    #     self.text_password_client.clear()
    #     self.text_client_store.clear()
    #     self.text_client_name.clear()
    #     self.text_client_city.clear()
    #     self.text_client_address.clear()
    #     self.text_client_postal_code.clear()
    #     self.text_client_email.clear()
    #     self.text_client_phone.clear()
    #     self.refresh_clients()

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
        self.db.c.execute("DELETE FROM clientS WHERE id = ?", (id,))
        self.db.commit()
        self.text_id_client.clear()
        self.refresh_clients()

    def show_dialog_employee(self):
        self.window = Dialog_employee()
        self.window.exec_()
        self.refresh()

    def show_dialog_client(self):
        self.window = Dialog_client()
        self.window.exec_()
        self.refresh_clients()


    def update_employee(self):
        if self.selected_ids.__len__() > 0:
            for selected in self.selected_ids:
                self.window = Dialog_employee(selected)
                self.window.exec_()
                self.refresh()

    def update_client(self):
        if self.selected_ids.__len__() > 0:
            for selected in self.selected_ids:
                self.window = Dialog_client(selected)
                self.window.exec_()
                self.refresh_clients()





class Dialog_employee(QDialog):

    def __init__(self, user=None):
        super(Dialog_employee, self).__init__()
        uic.loadUi('Dialog_employee.ui', self)
        self.db = Database()
        self.add_employee_button.clicked.connect(self.add_employee)
        self.update_employee_button.clicked.connect(self.update_employee)
        if user:
            self.label_14.setText('Update Employee')
            print(f'now qery with id {user}')
            print(user)
            orm = self.db.c.execute('SELECT * FROM employee WHERE id = ?',(user,)).fetchone()
            # print(orm)
            # print(type(orm))
            # print(len(orm))
            self.setup_fields(orm)
            self.add_employee_button.hide()
        else:
            self.label_14.setText('Add an Employee')
            self.update_employee_button.hide()

    def setup_fields(self, orm):
        (ids, username, password, first_name, last_name, age, phone_number, department, city, address) = orm
        self.username = self.text_username_employee.setText(username)
        self.password = self.text_password_employee.setText(password)
        self.first_name = self.text_firstname_employee.setText(first_name)
        self.last_name = self.text_lastname_employee.setText(last_name)
        self.age = self.text_age_employee.setText(str(age))
        self.phone_number = self.text_phone_number_employee.setText(str(phone_number))
        self.department = self.text_department_employee.setText(department)
        self.city = self.text_city_employee.setText(city)
        self.address = self.text_address_employee.setText(address)
        self.ids = ids

    def update_employee(self):
        self.username = self.text_username_employee.text()
        self.password = self.text_password_employee.text()
        self.first_name = self.text_firstname_employee.text()
        self.last_name = self.text_lastname_employee.text()
        self.age = self.text_age_employee.text()
        self.phone_number = self.text_phone_number_employee.text()
        self.department = self.text_department_employee.text()
        self.city = self.text_city_employee.text()
        self.address = self.text_address_employee.text()
        for requirement in [self.username, self.password, self.first_name, self.last_name, self.age, self.phone_number,
                            self.department, self.city, self.address]:
            if requirement == '':
                QtWidgets.QMessageBox.information(
                    self, 'Check for registration fields',
                    'Please fill all values.')
                return
        self.db.update_employee_table(self.ids,self.username, self.password, self.first_name, self.last_name, self.age, self.phone_number, self.department, self.city, self.address)
        self.close()

    def add_employee(self):
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
        self.close()


class Dialog_client(QDialog):
    def __init__(self, user=None):
        super(Dialog_client,self).__init__()
        uic.loadUi('Dialog_client.ui',self)
        self.db = Database()
        self.add_client_button.clicked.connect(self.add_client)
        if user:
            self.label_31.setText('Update Client')
            orm = self.db.c.execute('SELECT * FROM client WHERE id = ?', (user,)).fetchone()
            self.setup_fields_client(orm)
            self.add_client_button.hide()
        else:
            self.label_31.setText('Add a Client')
            self.update_client_button.hide()

    def setup_fields_client(self,orm):
        (ids, username_client, password_client, client_store, client_name, client_city, client_address, client_postal_code, client_email, client_phone) = orm
        self.username_client = self.text_username_client.setText(username_client)
        self.password_client = self.text_password_client.setText(password_client)
        self.client_store = self.text_client_store.setText(client_store)
        self.client_name = self.text_client_name.setText(client_name)
        self.client_city = self.text_client_city.setText(client_city)
        self.client_address = self.text_client_address.setText(client_address)
        self.client_postal_code = self.text_client_postal_code.setText(client_postal_code)
        self.client_email = self.text_client_email.setText(client_email)
        self.client_phone = self.text_client_phone.setText(client_phone)
        self.ids =ids


    def add_client(self):
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
        self.close()

    def update_client(self):
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
        self.db.update_client_table(self.ids,self.username_client,self.password_client,self.client_store,self.client_name,self.client_city,self.client_address,self.client_postal_code,self.client_email,self.client_phone)





if __name__ == '__main__':
    stylesheet = """
        Login {
            background-image: url("C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\medication-photo.jpg"); 
            background-repeat: no-repeat; 
            background-position: center;
        }
    """

    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = Login()
    window.show()

    sys.exit(app.exec_())
