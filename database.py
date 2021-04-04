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
		phone_number INTEGER NOT NULL
		
		

		)""")
		# PRIMARYKEY(id, username)
		self.commit()

	def delete_employee_table(self):
		self.connect()
		self.c.execute("""DROP table employee""")

	def add_one_employee(self, username, password, first_name, last_name, phone_number):
		self.connect()
		self.c.execute("INSERT INTO employee (username,password,first_name,last_name,phone_number) VALUES (?,?,?,?,?)", (username, password, first_name, last_name, phone_number))
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


