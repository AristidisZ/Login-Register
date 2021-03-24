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

	def del_one(self):
		self.connect()
		self.c.execute("DELETE from admin WHERE id = 2")
		self.commit()

	def authentication(self, username, password):
		self.connect()
		statement = f"SELECT username from admin WHERE username='{username}' AND Password = '{password}';"
		self.c.execute(statement)
		self.conn.commit()
		if not self.c.fetchone():  # An empty result evaluates to False.
			print("Login failed")
		else:
			print("Welcome")
		self.conn.close()

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


if __name__ == "__main__":
	# add_one()
	# del_one()
	db = Database()
	# db.show_all()
	# db.del_one()
    # db.authentication()
	# db.create_admin_table()
	# db.delete_admin_table()
	db.show_all()


