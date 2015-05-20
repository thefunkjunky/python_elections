# Election Module
# from passlib.hash import pbkdf2_sha512
import mysql.connector
# from mysql.connector import errorcode
# from collections import OrderedDict
# from contextlib import closing
from pythonvoting_mySQLinterface import mySQLinterface
# from pythonvoting_userctrl import User

class Election(object):
	"""Python Voting User Control"""
	def __init__(self):
		super(Election, self).__init__()
		self.mysql_login = "root"
		self.mysql_pass = "t3chn0"
		self.openDB()

	def openDB(self):
		self.sqlcontrol = mySQLinterface()
		self.sqlcontrol.connectmySQL(self.mysql_login, self.mysql_pass)
		self.queryDB = self.sqlcontrol.queryDB
		self.exec_DB = self.sqlcontrol.exec_DB
		self.zip = self.sqlcontrol.zip_values
		self.update = self.sqlcontrol.update_table

	def elect_namecheck(self, electname = ""):
		query = "SELECT electname FROM elections WHERE electname = \'%s\'" % (electname)
		results = [item[0] for item in self.queryDB(query)]
		return electname in results

	def create_elect(self, electname, elect_type, user_id):
		if not self.elect_namecheck(electname):
			cmd = "INSERT INTO elections "\
			"(electname, global_type, user_id) "\
			"VALUES (\'%s\', \'%s\', \'%i\')" % (electname, elect_type, user_id)
			try:
				self.exec_DB(cmd)
				print "Election added"
			except:
				print "Failed to add election"
		else:
			print "Election %s already exists." % (electname)

	def elect_values(self, elect_id):
		return self.zip('elections', 'election_id', elect_id)
		

	def list_values(self):
		# What was I trying to do here?
		# This should be made a generator in mySQLinterface
		election_full_list = []
		query = "SELECT election_id FROM elections"
		id_list = [x[0] for x in self.queryDB(query)]
		try:
			for id in id_list:
				listquery = self.elect_values(id)
				election_full_list.append(listquery)
		except:
			print "Error listing elections."

		return election_full_list 

	def update_elect(self, elect_id, newvalues={}):
		del_values = ['election_id', 'user_id', 'close_date', 'mod_date', 'open_date']
		self.update('elections', 'election_id', elect_id, newvalues, del_values)


	def delete_elect(self, elect_id):
		cmd = "DELETE FROM elections WHERE election_id = (\'%i\')" % (elect_id)
		try:
			self.exec_DB(cmd)
			print "Election #%i deleted." % (elect_id)
		except:
			print "Failed to delete election"

elect = Election()
elect.create_elect("Primaries", "IRV", 1)
# elect.delete_elect(3)
# elect.update_elect(1, {'electname': 'Final Elections', 'global_type': 'IRV'})
# print elect.list_values()

elect.sqlcontrol.closeDB()

