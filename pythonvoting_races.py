#PythonVoting Races Module

import sys
from passlib.hash import pbkdf2_sha512
import mysql.connector
from mysql.connector import errorcode
from collections import OrderedDict
from contextlib import closing
from pythonvoting_mySQLinterface import mySQLinterface
from pythonvoting_elections import Election

class Races(object):
	"""Election-Races Module"""
	def __init__(self, elect_id):
		super(Races, self).__init__()
		self.mysql_login = "root"
		self.mysql_pass = "t3chn0"
		self.openDB()
		self.assign_electid(elect_id)

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

	def assign_electid(self, elect_id):
		if self.itemcheck('elections', 'election_id', elect_id):
			self.elect_id = elect_id
			print "Current election ID is %i." % elect_id
		else: 
			print "Election Id# not found. Please assign another."
			self.elect_id = None

	def assign_globaltype(self):
		try:
			if self.itemcheck('elections', 'election_id', self.elect_id):
				query = "SELECT global_type FROM elections WHERE election_id = (\'%i\')" % (self.elect_id)
				self.globaltype = self.queryDB(query)[0][0]
				# print self.globaltype
			else:
				print "Invalid request."
		except:
			print "Invalid request: ", sys.exc_info()[0]

	def create_race(self, racename, racetype = None):
		try:
			if self.globaltype != None and racetype == None: racetype = self.globaltype
			print "Global type: ", self.globaltype
			if self.itemcheck('elections', 'election_id', self.elect_id) and not self.itemcheck(
				 'races', 'racename', racename):
				# print "Checks passed."
				cmd = "INSERT INTO races (racename, race_type, election_id) " \
				"VALUES (\'%s\', \'%s\', \'%i\')" % (racename, racetype, self.elect_id)
				# print cmd
				self.exec_DB(cmd)
				print "Race created."
			else:
				print "Checks failed."
		except:
			print "Invalid request: ", sys.exc_info()[0]

	def update_race(self, race_id, newvalues={}):
		del_values = ['race_id']
		self.update('races', 'race_id', race_id, newvalues, del_values)

	def delete_race(self, race_id):
		self.delete('races', 'race_id', race_id)

	def list_values(self, race_id):
		return self.zip("races", "race_id", race_id)

	def clear_races(self):
		self.clear('races')

raceconsole = Races(1)
raceconsole.assign_globaltype()
raceconsole.create_race('Vice-President of Earth')
# raceconsole.update_race(1, {'race_type': 'WinnerTA'})
# raceconsole.clear_races()
# print raceconsole.list_values(1)
raceconsole.sqlcontrol.closeDB()