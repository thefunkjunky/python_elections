# Python voting
# by Garrett Anderson

# MySQL db init and interface

import sys
import mysql.connector
import MySQLdb  
import MySQLdb.cursors as cursors
import json
from mysql.connector import errorcode
from collections import OrderedDict
from contextlib import closing
from passlib.hash import pbkdf2_sha512
from faker import Faker


def yesno(yesno_input):
	if yesno_input.lower() in ['y', 'yes', 'yeah', 'yup', 'yay']:
		return True
	elif yesno_input.lower() in ['n', 'no', 'nah', 'nope', 'naw', 'nay']:
		return False
	else:
			return "Invalid"


class mySQLinterface(object):
	"""MySQL connection interface"""
	def __init__(self):
		super(mySQLinterface, self).__init__()
		self.adminpass = "asdf"
		self.adminpasshash = pbkdf2_sha512.encrypt(self.adminpass)
		self.faker = Faker()


	def queryDB(self, query):
		with closing(self.mysqlCNX.cursor()) as dbcursor:
			dbcursor.execute(query)
			results = dbcursor.fetchall()
			return results

	def exec_DB(self, insert_cmd):
		with closing(self.mysqlCNX.cursor()) as dbcursor:
			dbcursor.execute(insert_cmd)
			print "Command executed."
			self.mysqlCNX.commit()

	def itemcheck(self, table, item_field, item_name):
		query = "SELECT %s FROM %s WHERE %s = \'%s\'" % (item_field, table, item_field, item_name)
		results = [item[0] for item in self.queryDB(query)]
		return item_name in results

	def zip_values(self, table, primary_id_field, primary_id_value):
		query1= "SELECT column_name FROM information_schema.columns WHERE table_name = \'%s\'" % (table)
		query2 = "SELECT * FROM %s WHERE %s = (\'%i\')" % (table, primary_id_field, primary_id_value)
		results1 = [x[0] for x in self.queryDB(query1)]
		results2 = self.queryDB(query2)[0]
		zipped_values = dict(zip(list(results1), list(results2)))

	def update_table(self, table, primary_id_field, primary_id_value, newvalues={}, ignore_fields = []):
		values = self.zip_values(table, primary_id_field, primary_id_value)
		values.update(newvalues)
		for val in ignore_fields: del values[val]
		try:
			for field, data in values.iteritems():
				cmd = "UPDATE %s SET %s = (\'%s\') WHERE %s = (\'%i\')" % (
					table, field, data, primary_id_field, primary_id_value)
				self.exec_DB(cmd)
			print "%s #%i updated." % (primary_id_field, primary_id_value)
		except:
			print "Failed to update. ", sys.exc_info()[0]

	def delete_row(self, table, primary_id_field, primary_id_value):
		cmd = "DELETE FROM %s WHERE %s = (\'%i\')" % (table, primary_id_field, primary_id_value)
		try:
			self.exec_DB(cmd)
			print "%s #%i deleted." % (primary_id_field, primary_id_value)
		except:
			print "Failed to delete %s. " % (primary_id_field)

	def clear_table(self, table):
		cmd = "DELETE FROM %s" % (table)
		try:
			self.exec_DB(cmd)
			print "Table %s cleared." % (table)
			if table == 'users':
				initadmin = "INSERT INTO users (username, password) VALUES (\'%s\', \'%s\')" % (
							"admin", self.adminpasshash)
				self.exec_DB(initadmin)
				print "User 'admin' created with password %s" % (self.adminpass)
		except:
			print "Clearing Table Failed. ", sys.exc_info()[0] 



	def create_DB(self, username, password, host = "127.0.0.1", dbname = "pythonvoting"):
		self.mysqlCNX = mysql.connector.connect(user = username, password = password, host = host)
		cursor = self.mysqlCNX.cursor()
		try:
			cursor.execute(
			"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(dbname))
			print "New Database '%s' successfully created." % (dbname)
			self.mysqlCNX.database = dbname
			cursor.close()
			self.initDB()
		except mysql.connector.Error as err:
			print("Failed to create database %s: {}".format(err) % (dbname))

	def connectmySQL(self, username, password, host = "127.0.0.1", dbname = "pythonvoting"):
		self.dbconfig = {
		'user': username,
		'password': password,
		'host': host,
		'database': dbname,
		}

		try:
			self.mysqlCNX = mysql.connector.connect(**self.dbconfig)
			print("Connection successful for db %s.") % (dbname)
			self.dbname = dbname
		except mysql.connector.Error as err:
			if err.errno == errorcode.CR_CONN_HOST_ERROR:
				print "Error connecting to host %s" % (host)
			elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Invalid MySQL user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist. Attempt to create \'%s\' Python Voting database?"
				% (dbname))
				yn_input = raw_input('Y or N> ')
				if yesno(yn_input) == True:
					self.create_DB(username, password, host, dbname)
				else:
					print "No database created."
			else:
				print(err)

	def initDB(self):
		try:
			TABLES = OrderedDict({})

			TABLES['users'] = (
				"CREATE TABLE users ("
					"username VARCHAR(20) NOT NULL,"
					"password CHAR(130) NOT NULL,"
					"user_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY)")

			TABLES['elections'] = (
				"CREATE TABLE elections ("
					"electname VARCHAR(40) NOT NULL,"
					"status ENUM('O', 'C') NOT NULL DEFAULT 'O',"
					"global_type ENUM('WinnerTA', 'Proportional', 'IRV', 'Shulze')"
					"NOT NULL DEFAULT 'WinnerTA',"
					"open_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
					# "mod_date TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
					"close_date TIMESTAMP DEFAULT 0,"
					"user_id INT UNSIGNED,"
					"election_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,"
					"FOREIGN KEY (user_id) REFERENCES users (user_id))")

			TABLES['races'] = (
				"CREATE TABLE races ("
					"racename VARCHAR(40) NOT NULL,"
					"race_type ENUM('WinnerTA', 'Proportional', 'IRV', 'Shulze') NULL,"
					"election_id INT UNSIGNED,"
					"race_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,"
					"FOREIGN KEY (election_id) REFERENCES elections (election_id))")

			TABLES['candidates'] = (
				"CREATE TABLE candidates ("
					"cand_name VARCHAR(40) NOT NULL,"
					"race_id INT UNSIGNED,"
					"election_id INT UNSIGNED," # is this even necessary?
					"cand_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,"
					"FOREIGN KEY (race_id) REFERENCES races (race_id),"
					"FOREIGN KEY (election_id) REFERENCES elections (election_id))")

			TABLES['cand_descriptions'] = (
				"CREATE TABLE cand_descriptions ("
					"cand_description TEXT,"
					"cand_id INT UNSIGNED,"
					"cand_descr_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,"
					"FOREIGN KEY (cand_id) REFERENCES candidates(cand_id))")

			TABLES['votes'] = (
				"CREATE TABLE votes ("
					"cand_id INT UNSIGNED,"
					"race_id INT UNSIGNED,"
					"election_id INT UNSIGNED,"
					"user_id INT UNSIGNED,"
					"ballot_id INT UNSIGNED NOT NULL,"
					"score INT UNSIGNED NOT NULL DEFAULT 0,"
					"vote_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,"
					"FOREIGN KEY (cand_id) REFERENCES candidates(cand_id),"
					"FOREIGN KEY (race_id) REFERENCES races(race_id),"
					"FOREIGN KEY (election_id) REFERENCES elections(election_id),"
					"FOREIGN KEY (user_id) REFERENCES users(user_id))")

			for name, cmd in TABLES.items():
				try:
					# print("Creating table {}: ".format(name), end='')
					print("Creating table {}: ".format(name))
					cursor = self.mysqlCNX.cursor()
					cursor.execute(cmd)
				except mysql.connector.Error as err:
					if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
						print("Already exists.")
					else:
						print(err.msg)
				else:
						print ("OK.")
						cursor.close()
		except AttributeError:
			print "No database connection. Please connect to database."

		initadmin = "INSERT INTO users (username, password) VALUES (\'%s\', \'%s\')" % (
					"admin", self.adminpasshash)
		self.exec_DB(initadmin)
		print "User 'admin' created with password %s" % (self.adminpass)

	def deleteDB(self):
		try:
			print "Deleting database %s." % (self.dbname)
			delcmd = "DROP DATABASE %s" % (self.dbname)
			# print delcmd
			cursor = self.mysqlCNX.cursor()
			cursor.execute(delcmd)
			cursor.close()
		except AttributeError:
			print "No database connection. Please connect to database."

	def closeDB(self):
		try:
			print "Closing DB Connection"
			# self.mysqlCursor.close()
			self.mysqlCNX.close()
		except AttributeError:
			print "No database connection. Please connect to database."




sqlcontrol = mySQLinterface()
# sqlcontrol.deleteDB()
# sqlcontrol.create_DB('root', 't3chn0')

sqlcontrol.closeDB()