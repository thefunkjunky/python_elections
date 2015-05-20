#PythonVoting dbModule 

from pythonvoting_mySQLinterface import mySQLinterface
import mysql.connector
import MySQLdb  
import MySQLdb.cursors as cursors
import sys
import json




class dbModule(object):
	"""Election-dbModule Module"""
	def __init__(self, table_name, prime_id_name):
		super(dbModule, self).__init__()
		# Don't forget to remove values
		try:
			with open("pythonvoting_sqlconnection_config.json", 'r') as sqlcfg_file:
				sqlcfg = json.load(sqlcfg_file)
		except:
			print "Error loading sql configuration file.  Please run sql_connection_config_script.py"
			sys.exit()

		self.mysql_login = sqlcfg['user']
		self.mysql_pass = sqlcfg['password']
		self.host = sqlcfg['host']
		self.dbport = ""
		self.dbname = sqlcfg['dbname']
		self.table = table_name
		self.prime_id_name = prime_id_name
		self.openDB()

	def openDB(self):
		self.sqlcontrol = mySQLinterface()
		self.sqlcontrol.connectmySQL(self.mysql_login, self.mysql_pass)
		self.queryDB = self.sqlcontrol.queryDB
		self.exec_DB = self.sqlcontrol.exec_DB
		self.itemcheck = self.sqlcontrol.itemcheck
		self.zip = self.sqlcontrol.zip_values
		self.update = self.sqlcontrol.update_table
		self.delete = self.sqlcontrol.delete_row
		self.clear = self.sqlcontrol.clear_table

	def genCursor(self):
		self.dbconfig = {
		'user': self.mysql_login,
		'passwd': self.mysql_pass,
		'host': self.host,
		'db': self.dbname,
		# 'raise_on_warnings': True
		'cursorclass': cursors.SSCursor
		}
		conn=MySQLdb.connect(**self.dbconfig)
		self.gencursor = conn.cursor()



	def update_db(self, prime_id, newvalues={}):
		ignore_fields = [self.prime_id_name]
		self.update(self.table, self.prime_id_name, prime_id, newvalues, ignore_fields)

	def delete_entry(self, prime_id):
		self.delete(self.table, self.prime_id_name, prime_id)

	def list_values(self, prime_id):
		return self.zip(self.table, self.prime_id_name, prime_id)

	def clear_table(self):
		self.clear(self.table)
