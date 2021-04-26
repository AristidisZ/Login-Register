import sqlite3


# Connect to database
# conn = sqlite3.connect('data.db')

# create a cursor
# c = conn.cursor()


# c.execute("SELECT rowid, * FROM admin")

# c.execute("INSERT INTO admin VALUES ('kwstas','1234')")

# Create a Table
# c.execute("""CREATE TABLE admin (
# username text,
# password text

# )""")

# conn.commit()

# conn.close ()


class Database:

	def __init__(self):
		self.conn = sqlite3.connect('data.db')
		self.c = self.conn.cursor()

	def connect(self):
		self.conn = sqlite3.connect('data.db')
		self.c = self.conn.cursor()

	def commit(self):
		self.conn.commit()
		self.conn.close()

	def show_all(self):
		self.connect()
		self.c.execute("SELECT id, * FROM admin")
		# c.fetchone()
		# c.fetchemany(1)
		# print(c.fetchall())
		items = self.c.fetchall()
		for item in items:
			print(item)
		self.commit()


# add a new record to table
	def add_one(self, username, password):
		self.connect()
		self.c.execute("INSERT INTO admin (username,password) VALUES (?,?)", (username, password))
		self.commit()

	def del_one_admin(self):
		self.connect()
		self.c.execute("DELETE from admin WHERE id = 4")
		self.commit()

	def authentication(self, username, password, auth_type):
		self.connect()
		if auth_type =="admin":
			statement = f"SELECT * from admin WHERE username='{username}' AND Password = '{password}';"
		elif auth_type =="employee":
			statement = f"SELECT * from employee WHERE username='{username}' AND Password = '{password}';"
		else:
			pass
			#statement = f"SELECT username from  WHERE username='{username}' AND Password = '{password}';"


		self.c.execute(statement)
		self.conn.commit()
		account = self.c.fetchone()
		self.conn.close()

		if not account:  # An empty result evaluates to False.
			print("Login failed")
			return False
		else:
			print(f"Welcome {auth_type}")
			return account

	def create_admin_table(self):

		self.connect()
		# create table
		self.c.execute("""CREATE TABLE admin(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username text NOT NULL,
		password text NOT NULL
		
		
		)""")
		# PRIMARYKEY(id, username)
		self.commit()

	def delete_admin_table(self):

		self.connect()
		# create table
		self.c.execute("""DROP table admin

		""")

		self.commit()

	def create_employee_table(self):

		self.connect()
		# create table
		self.c.execute("""CREATE TABLE employee(
		id INTEGER PRIMARY KEY,
		username text NOT NULL UNIQUE,
		password text NOT NULL,
		first_name text NOT NULL,
		last_name text NOT NULL,
		age INTEGER NOT NULL, 
		phone_number INTEGER NOT NULL,
		department text NOT NULL,
		city text NOT NULL,
		address text NOT NULL
		

		)""")
		# PRIMARYKEY(id, username)
		self.commit()

	def update_employee_table(self,ids,username, password, first_name, last_name,age, phone_number, department, city, address):
		self.connect()
		print(self)
		self.c.execute("UPDATE employee	SET (username,password,first_name,last_name,age,phone_number,department,city,address) = (?,?,?,?,?,?,?,?,?) WHERE id = ?",(username, password, first_name, last_name,age, phone_number, department, city, address,ids))
		self.commit()

	def delete_employee_table(self):
		self.connect()
		self.c.execute("""DROP table employee""")

	def add_one_employee(self, username, password, first_name, last_name,age, phone_number, department, city, address):
		self.connect()
		self.c.execute("INSERT INTO employee (username,password,first_name,last_name,age,phone_number,department,city,address) VALUES (?,?,?,?,?,?,?,?,?)", (username, password, first_name, last_name,age, phone_number, department, city, address))
		self.commit()

	def create_medicine_table(self):
		self.connect()
		self.c.execute("""CREATE TABLE medicine(
		id INTEGER PRIMARY KEY,
		med_name text NOT NULL UNIQUE,
		expiration_date text NOT NULL,
		category text NOT NULL,
		preparation text NOT NULL,
		quantity INTEGER NOT NULL, 
		med_buy_price NUMERIC NOT NULL,
		med_sell_price NUMERIC NOT NULL
		

		)""")

	def add_one_medicine(self,med_name,expiration_date,category,preparation,quantity,medicationbp,medicationsp):
		self.connect()
		self.c.execute("INSERT INTO medicine (med_name,expiration_date,category,preparation,quantity,med_buy_price,med_sell_price) VALUES(?,?,?,?,?,?,?)",(med_name,expiration_date,category,preparation,quantity,medicationbp,medicationsp))
		self.commit()

	def show_employee(self):
		self.connect()
		self.c.execute("SELECT id, * FROM employee")
		# c.fetchone()
		# c.fetchemany(1)
		# print(c.fetchall())
		items = self.c.fetchall()
		for item in items:
			print(item)
		self.commit()

	def show_medicine(self):
		self.connect()
		self.c.execute("SELECT id, * FROM medicine")
		# c.fetchone()
		# c.fetchemany(1)
		# print(c.fetchall())
		items = self.c.fetchall()
		for item in items:
			print(item)
		self.commit()

	def create_clients_table(self):
		self.connect()
		self.c.execute("""CREATE TABLE clients(
		id INTEGER PRIMARY KEY,
		username text NOT NULL UNIQUE,
		password text NOT NULL,
		client_store text NOT NULL UNIQUE,
		client_name text NOT NULL,
		city text NOT NULL,
		client_address text NOT NULL,
		postal_code INTEGER NOT NULL, 
		client_email text NOT NULL,
		client_phone INTEGER NOT NULL


		)""")

	def delete_clients_table(self):
		self.connect()
		self.c.execute("""DROP table clients""")

	def add_one_client(self,username_client, password_client, client_store, client_name,client_city,client_address,client_postal_code,client_email,client_phone):
		self.connect()
		self.c.execute("INSERT INTO clients (username,password,client_store,client_name,city,client_address,postal_code,client_email,client_phone) VALUES (?,?,?,?,?,?,?,?,?)", (username_client,password_client, client_store,client_name,client_city,client_address,client_postal_code, client_email, client_phone))
		self.commit()


	def update_client_table(self,ids,username_client, password_client, client_store, client_name,client_city,client_address,client_postal_code,client_email,client_phone):
		self.connect()
		print(self)
		self.c.execute("UPDATE clients SET (username_client,password_client, client_store,client_name,client_city,client_address,client_postal_code, client_email) = (?,?,?,?,?,?,?,?,?) WHERE id = ?",(username_client,password_client, client_store,client_name,client_city,client_address,client_postal_code, client_email, client_phone,ids))
		self.commit()



if __name__ == "__main__":
	# add_one()
	db = Database()
	# db.show_all()
	# del_one()
    # db.authentication()
	# db.create_admin_table()
	# db.delete_admin_table()
	# db.add_one_employee()
	# db.show_all()
	db.show_employee()
	# db.create_employee_table()
	# db.delete_employee_table()
	# db.add_one_employee(username="em1",password="123",first_name="Aris",last_name="zotka",phone_number=6943690861)
	# db.del_one_admin()
	# db.create_medicine_table()
	# db.add_one_medicine(med_name='Largactil',expiration_date='12/03/21-10/5/21',category='Antipsycotics',preparation='Pills',quantity='300',med_buy_price='0.15',med_sell_price='0.2')
	# db.show_medicine()
	# db.create_clients_table()
	# db.delete_clients_table()


