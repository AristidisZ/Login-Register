from database import Database
import sys
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow ,QMessageBox,QTabWidget
import sqlite3

class Login(QDialog):
    verbose = False

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

        elif self.employee_login_checkbox.isChecked():
            user = self.db.authentication(username, passw, "employee")
            if user:
                self.hide()
                self.window = Main_admin(user=user)
                self.window.show()
                self.window.tabWidget.setTabEnabled(0, False)
                self.window.tabWidget.setTabEnabled(4, False)



        elif self.client_login_checkbox.isChecked():
            user = self.db.authentication(username,passw, "clients")
            if user:
                self.hide()
                self.window = Main_admin(user=user)
                self.window.show()
                self.window.tabWidget.setTabEnabled(0, False)
                self.window.tabWidget.setTabEnabled(1, False)
                self.window.tabWidget.setTabEnabled(2, False)
                self.window.tabWidget.setTabEnabled(3, False)

            # sys.exit(sys.argv)

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
    selected_ids_client = []
    selected_ids_medication = []
    selected_ids_medication_order = []
    selected_ids_orders = []

    def __init__(self, user):
        super(Main_admin, self).__init__()
        uic.loadUi('MainWindow_admin.ui', self)
        # self.showFullScreen()
        self.showMaximized()
        # uic.loadUi('Main_admin.ui', self)
        self.user = user
        self.label_admin.setText(f"Welcome  ID : {self.user[0]}  User_name : {self.user[1]}")
        self.db = Database()
        self.refresh()
        self.refresh_medication()
        self.refresh_clients()
        self.refresh_medication_order()
        self.refresh_orders()

        # employee buttons
        self.show_dialog_employee_button.clicked.connect(self.show_dialog_employee)
        self.update_employee_buttton.clicked.connect(self.update_employee)
        self.delete_employee_button.clicked.connect(self.del_one_employee)
        self.refresh_button.clicked.connect(self.refresh)
        self.search_button.clicked.connect(self.search)
        self.employee_table.itemClicked.connect(self.select_data_employee)

        # medication buttons

        self.refresh_button_medication.clicked.connect(self.refresh_medication)
        self.delete_medicine_button.clicked.connect(self.delete_one_medication)
        self.create_dialog_medication.clicked.connect(self.show_dialog_medication)
        self.update_medication_button.clicked.connect(self.update_medication)
        self.search_button_medication.clicked.connect(self.search_medication)
        self.medication_table.clicked.connect(self.select_data_medication)




        # clients buttons
        self.clients_table.itemClicked.connect(self.select_data_client)
        self.show_dialog_client_button.clicked.connect(self.show_dialog_client)
        self.update_clients_buttton.clicked.connect(self.update_client)
        self.refresh_button_client.clicked.connect(self.refresh_clients)
        self.delete_client_button.clicked.connect(self.del_one_client)
        self.search_clients_button.clicked.connect(self.search_client)


        # order client buttons
        self.refresh_button_medication_orders.clicked.connect(self.refresh_medication_order)
        self.order_medication_table.itemClicked.connect(self.select_data_medication_order)
        self.addto_cart_button.clicked.connect(self.add_to_cart)
        self.order_clients.clicked.connect(self.save_order)
        self.refresh_orders_button.clicked.connect(self.refresh_orders)
        self.search_button_medication_orders.clicked.connect(self.search_order_medication)


        # self.cart_table.setRowCount(0)

        self.logout_button.clicked.connect(self.logout)
        # self.phone_number.clicked.connect(self.)

        #orders
        self.create_order.clicked.connect(self.show_dialog_orders)
        self.delete_orders.clicked.connect(self.del_one_order)



    def logout(self):
        self.close()
        # self.window = Login
        # self.window.()





    # employee
    def select_data_employee(self):

        selected_items = np.unique([i.row() for i in self.employee_table.selectedItems()])
        self.selected_ids = [self.employee_table.item(selected_row, 0).text() for selected_row in selected_items]
        # print('selected rows', selected_items)
        # print('selected ids', self.selected_ids)
        id=(self.selected_ids)
        for i in range(0, len(id)):
            self.selected_ids[i] = int(id[i])
        print("Modified/id list is : " + str(id))


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
        if self.selected_ids.__len__() > 0:
            self.db.connect()
            buttonReply = QMessageBox.question(self, 'PyQt5 message', f"Do you want to delete {self.selected_ids.__len__()} employees",QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if buttonReply == QMessageBox.Yes:
                for selected in self.selected_ids:
                    self.db.c.execute("DELETE FROM employee WHERE id = ?", (selected,))
                    self.db.commit()
                    self.selected_ids = []
                    self.refresh()
            elif buttonReply == QMessageBox.No:
                pass
            elif buttonReply == QMessageBox.Cancel:
                pass

    def show_dialog_employee(self):
        self.window = Dialog_employee()
        self.window.exec_()
        self.refresh()

    def update_employee(self):
        if self.selected_ids.__len__() > 0:
            for selected in self.selected_ids:
                self.window = Dialog_employee(selected)
                self.window.exec_()
                self.refresh()

    # clients
    def select_data_client(self):
        selected_items = np.unique([i.row() for i in self.clients_table.selectedItems()])
        self.selected_ids_client = [self.clients_table.item(selected_row, 0).text() for selected_row in selected_items]


    def refresh_clients(self):
        self.db.connect()
        query = self.db.c.execute("SELECT * FROM clients").fetchall()
        self.clients_table.setRowCount(len(query))

        for row, item in enumerate(query, start=0):
            for column, value in enumerate(item):
                if column == 0:
                    print(value)
                self.clients_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))

    def del_one_client(self):
        if self.selected_ids_client.__len__() > 0:
            self.db.connect()
            buttonReply = QMessageBox.question(self, 'PyQt5 message', f"Do you want to delete  {self.selected_ids_client.__len__()} clients",
                                               QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                               QMessageBox.Cancel)
            if buttonReply == QMessageBox.Yes:
                for selected in self.selected_ids_client:
                    self.db.c.execute("DELETE FROM clients WHERE id = ?", (selected,))
                    self.db.commit()
                    self.selected_ids_client = []
                    self.refresh_clients()
            elif buttonReply == QMessageBox.No:
                pass
            elif buttonReply == QMessageBox.Cancel:
                pass

    def update_client(self):
        if self.selected_ids_client.__len__() > 0:
            print("sd")
            for selected in self.selected_ids_client:
                print(selected)
                self.window = Dialog_client(selected)
                self.window.exec_()
                self.refresh_clients()

    def show_dialog_client(self):
        self.window = Dialog_client()
        self.window.exec_()
        self.refresh_clients()

    def search_client(self):
        self.db.connect()
        search = self.clients_search.text()
        query = f"SELECT * FROM clients WHERE username LIKE '%{search}%' OR client_store LIKE '%{search}%' OR " \
                f"client_name LIKE '%{search}%'OR city LIKE '%{search}%' OR client_address LIKE '%{search}%' OR postal_code LIKE '%{search}%' OR client_email LIKE '%{search}%' OR client_phone LIKE '%{search}%' "
        result = self.db.c.execute(query).fetchall()
        print(result)
        self.clients_table.setRowCount(len(result))

    # medication
    # def create_medication(self):
    #     self.med_name = self.text_medication_name_medication.text()
    #     self.expiration_date = self.text_expiration_name_medication.text()
    #     self.category = self.text_category_medication.text()
    #     self.preparation = self.text_preparation_medication.text()
    #     self.quantity = self.text_quantity_medication.text()
    #     self.medicationbp = self.text_medicationbp_medication.text()
    #     self.medicationsp = self.text_medicationsp_medication.text()
    #     for requirement in [self.med_name,self.expiration_date,self.category,self.preparation,self.quantity,self.medicationbp,self.medicationsp]:
    #         if requirement == '':
    #             QtWidgets.QMessageBox.information(
    #                 self, 'Check for registration fields',
    #                 'Please fill all values.')
    #             return
    #     self.db.add_one_medicine(self.med_name,self.expiration_date,self.category,self.preparation,self.quantity,self.medicationbp,self.medicationsp)
    #     self.text_medication_name_medication.clear()
    #     self.text_expiration_name_medication.clear()
    #     self.text_category_medication.clear()
    #     self.text_preparation_medication.clear()
    #     self.text_quantity_medication.clear()
    #     self.text_medicationbp_medication.clear()
    #     self.text_medicationsp_medication.clear()
    #     self.refresh_medication()

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


    def delete_one_medication(self):
        if self.selected_ids_medication.__len__() > 0:
            self.db.connect()
            buttonReply = QMessageBox.question(self, 'PyQt5 message',
                                               f"Do you want to delete {self.selected_ids_medication.__len__()} medications",
                                               QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                               QMessageBox.Cancel)
            if buttonReply == QMessageBox.Yes:
                for selected in self.selected_ids_medication:
                    self.db.c.execute("DELETE FROM medicine WHERE id = ?", (selected,))
                    self.db.commit()
                    self.selected_ids_medication = []
                    self.refresh_medication()
            elif buttonReply == QMessageBox.No:
                pass
            elif buttonReply == QMessageBox.Cancel:
                pass

    def select_data_medication_order(self):
        selected_items = np.unique([i.row() for i in self.order_medication_table.selectedItems()])
        self.selected_ids_medication_order = [self.order_medication_table.item(selected_row, 0).text() for selected_row in selected_items]

    def show_dialog_medication(self):
        self.window = Dialog_medication()
        self.window.exec_()
        self.refresh_medication()

    def update_medication(self):
        if self.selected_ids_medication.__len__() > 0:
            for selected in self.selected_ids_medication:
                self.window = Dialog_medication(selected)
                self.window.exec_()
                self.refresh_medication()

    def select_data_medication(self):
        selected_items = np.unique([i.row() for i in self.medication_table.selectedItems()])
        self.selected_ids_medication = [self.medication_table.item(selected_row, 0).text() for selected_row in selected_items]
        print(self.selected_ids_medication)


    # def search_medication_orders(self):
    #     self.db.connect()
    #     search = self.text_search_medication.text()
    #     query = f"SELECT * FROM medicine WHERE med_name LIKE '%{search}%' OR expiration_date LIKE '%{search}%' OR " \
    #             f"category LIKE '%{search}%'OR preparation LIKE '%{search}%' OR quantity LIKE '%{search}%' OR med_buy_price LIKE '%{search}%' OR med_sell_price LIKE '%{search}%'"
    #     result = self.db.c.execute(query).fetchall()
    #     print(result)
    #     self.medication_table.setRowCount(len(result))

    #client orders
    def refresh_medication_order(self):
        self.db.connect()
        query = self.db.c.execute("SELECT * FROM medicine").fetchall()
        self.order_medication_table.setRowCount(len(query))

        for row, item in enumerate(query, start=0):
            for column, value in enumerate(item, start=0):
                print(column, item, value)
                if column != 6:
                    column = 6 if column == 7 else column
                    self.order_medication_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))

    def add_to_cart(self):
        if len(self.selected_ids_medication_order) > 0:
            self.db.connect()
            rows_of_cart = self.cart_table.rowCount()
            print('before', rows_of_cart)

            # self.order_medication_table.setRowCount(1)
            # self.cart_table.setItem(0, 0, QtWidgets.QTableWidgetItem(str('11111')))
            # self.cart_table.setItem(0, 2, QtWidgets.QTableWidgetItem(str('222222')))

            for idx, selected_id in enumerate(self.selected_ids_medication_order, start=0):
                item = self.db.c.execute("SELECT * FROM medicine WHERE id = ?", (selected_id)).fetchone()
                self.window = Dialog_cart_order()
                self.window.setup_fields(orm=item)
                self.window.exec_()
                row = rows_of_cart + idx

                if self.window.total_value is not None:
                    self.cart_table.setRowCount(row + 1)

                    # QApplication.processEvents()
                    self.cart_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(self.window.idx)))
                    self.cart_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(self.window.med_name)))
                    self.cart_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(self.window.quantity)))
                    self.cart_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(self.window.total_value)))

    def save_order(self):
        self.db.connect()
        print(self.user)
        client_id = self.user[0]
        client_address = self.user[6]
        post_code = self.user[7]
        phone_number = self.user[8]
        # print(order_id)
        print(client_id)
        print(client_address)
        print(post_code)
        print(phone_number)

        total_prise = 0
        for row in range(0, self.cart_table.rowCount(), 1):
            item_id = self.cart_table.item(row, 0).text()
            item_name = self.cart_table.item(row, 1).text()
            item_quantity = self.cart_table.item(row, 2).text()
            item_sell_price = float(self.cart_table.item(row, 3).text())
            total_prise += item_sell_price

        self.db.add_order(client_id=client_id,
                          client_adress=client_address,
                          postal_code=post_code,
                          phone_number=phone_number,
                          total_price=total_prise
                          )

    def search_order_medication(self):
        self.db.connect()
        search = self.text_search_medication_orders.text()
        query = f"SELECT * FROM medicine WHERE med_name LIKE '%{search}%' OR expiration_date LIKE '%{search}%' OR " \
                f"category LIKE '%{search}%'OR preparation LIKE '%{search}%' OR quantity LIKE '%{search}%' OR med_buy_price LIKE '%{search}%' OR med_sell_price LIKE '%{search}%'"
        result = self.db.c.execute(query).fetchall()
        print(result)
        self.order_medication_table.setRowCount(len(result))


    # orders
    def refresh_orders(self):
        self.db.connect()
        query = self.db.c.execute("SELECT * FROM orders").fetchall()
        self.orders_table.setRowCount(len(query))

        for row, item in enumerate(query, start=0):
            for column, value in enumerate(item):
                # if column == 0:
                # print(value)
                self.orders_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))


    def update_orders(self):
        if self.selected_ids_orders.__len__() > 0:
            for selected in self.selected_ids_orders:
                self.window = Dialog_orders(selected)
                self.window.exec_()
                self.refresh_orders()

    def select_data_orders(self):
        selected_items = np.unique([i.row() for i in self.orders_table.selectedItems()])
        self.selected_ids_orders = [self.orders_table.item(selected_row, 0).text() for selected_row in selected_items]
        print(self.selected_ids_orders)


    def show_dialog_orders(self):
        self.window = Dialog_orders()
        self.window.exec_()
        self.refresh_orders()

    def del_one_order(self):
        if self.selected_ids_orders.__len__() > 0:
            self.db.connect()
            buttonReply = QMessageBox.question(self, 'PyQt5 message', f"Do you want to delete {self.selected_ids_orders.__len__()} orders",QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if buttonReply == QMessageBox.Yes:
                for selected in self.selected_ids_orders:
                    self.db.c.execute("DELETE FROM orders WHERE order_id = ?", (selected,))
                    self.db.commit()
                    self.selected_ids_orders = []
                    self.refresh_orders()
            elif buttonReply == QMessageBox.No:
                pass
            elif buttonReply == QMessageBox.Cancel:
                pass




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
        self.update_client_button.clicked.connect(self.update_client)
        if user:
            self.label_31.setText('Update Client')
            orm = self.db.c.execute('SELECT * FROM clients WHERE id = ?', (user,)).fetchone()
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
        self.client_postal_code = self.text_client_postal_code.setText(str(client_postal_code))
        self.client_email = self.text_client_email.setText(client_email)
        self.client_phone = self.text_client_phone.setText(str(client_phone))
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
        self.close()


class Dialog_medication(QDialog):
    def __init__(self, user=None):
        super(Dialog_medication, self).__init__()
        uic.loadUi('Dialog_medication.ui', self)
        self.db = Database()
        self.add_medication_button.clicked.connect(self.add_medication)
        self.update_medication_button.clicked.connect(self.update_medication)
        if user:
            self.label_medication.setText('Update Medication')
            print(f'now qery with id {user}')
            print(user)
            orm = self.db.c.execute('SELECT * FROM medicine WHERE id = ?', (user,)).fetchone()
            # print(orm)
            # print(type(orm))
            # print(len(orm))
            self.setup_fields_medication(orm)
            self.add_medication_button.hide()
        else:
            self.label_medication.setText('Add Medication')
            self.update_medication_button.hide()

    def setup_fields_medication(self, orm):
        (ids, med_name, expiration_date, category, preparation, quantity, medicationbp, medicationsp) = orm
        self.med_name = self.text_medication_name_medication.setText(med_name)
        self.expiration_date = self.text_expiration_name_medication.setText(expiration_date)
        self.category = self.text_category_medication.setText(category)
        self.preparation = self.text_preparation_medication.setText(preparation)
        self.quantity = self.text_quantity_medication.setText(str(quantity))
        self.medicationbp = self.text_medicationbp_medication.setText(str(medicationbp))
        self.medicationsp = self.text_medicationsp_medication.setText(str(medicationsp))
        self.ids = ids


    def add_medication(self):
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
        self.close()


    def update_medication(self):
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
        self.db.update_medication_table(self.ids,self.med_name, self.expiration_date,self.category,self.preparation,self.quantity,self.medicationbp,self.medicationsp)
        self.close()


class Dialog_cart_order(QDialog):
    def __init__(self):
        super(Dialog_cart_order, self).__init__()
        uic.loadUi('Dialog_cart_order.ui', self)
        self.add_medication_button.clicked.connect(self.add_to_cart)
        self.cancel_medication_button.clicked.connect(self.cancel_cart)
        self.idx = None
        self.med_name = None
        self.expiration_date = None
        self.category = None
        self.preparation = None
        self.medicationsp = None
        self.quantity = None
        self.total_value = None

    def setup_fields(self, orm):
        (idx, med_name, expiration_date, category, preparation, quantity, medicationbp, medicationsp) = orm
        self.idx = self.id_mecine.setText(str(idx))
        self.med_name = self.medication_name.setText(med_name)
        self.expiration_date = self.medication_expiration_date.setText(expiration_date)
        self.category = self.category_medication.setText(category)
        self.preparation = self.mecation_preperation.setText(preparation)
        self.quantity_box.setRange(1, quantity)
        self.quantity_box.setSingleStep(1)
        self.quantity_box.setValue(1)
        # self.quantity_value
        self.medicationsp = self.sell_price_medication.setText(str(medicationsp))

    def add_to_cart(self):
        self.idx = int(self.id_mecine.text())
        self.med_name = self.medication_name.text()
        self.expiration_date = self.medication_expiration_date.text()
        self.category = self.category_medication.text()
        self.quantity = self.quantity_box.value()
        self.medicationsp = float(self.sell_price_medication.text())
        self.total_value = self.medicationsp * self.quantity
        self.close()

    def cancel_cart(self):
        self.close()


class Dialog_orders(QDialog):
    def __init__(self, user=None):
        super(Dialog_orders, self).__init__()
        uic.loadUi('Dialog_orders.ui', self)
        self.db = Database()

        if user:
            self.label.setText('Update order')
            print(user)
            orm = self.db.c.execute('SELECT * FROM orders WHERE order_id = ?', (user,)).fetchone()
            # print(orm)
            # print(type(orm))
            # print(len(orm))
            self.setup_fields(orm)
            self.add_order_button.hide()
        else:
            self.label.setText('Add an order')
            self.update_order_button.hide()

    def setup_fields(self, orm):
        (ids,client_id,client_adress,postal_code,phone_number,total_price ) = orm
        self.adress = self.client_adress.setText(client_adress)
        self.postalcode = self.postal_code.setText(postal_code)
        self.phonenumber = self.phone_number.setText(phone_number)
        self.totalprice = self.total_price.setText(total_price)
        self.ids = ids





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
