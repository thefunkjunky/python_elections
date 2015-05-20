from passlib.hash import pbkdf2_sha512
import mysql.connector
from mysql.connector import errorcode
from collections import OrderedDict
from contextlib import closing
from pythonvoting_mySQLinterface import mySQLinterface

class pythonvoting_Users(dbModule):
	"""DBmodule for User Control"""
	def __init__(self):
		super(pythonvoting_Users, self).__init__("users", "user_id")
		
	def checkUser(self, username):
		query = "SELECT username FROM users WHERE username = \'%s\'" % (username)
		results = [item[0] for item in self.queryDB(query)]
		return username in results

	def checkpass(self, username, password):
		query = "SELECT password FROM users WHERE username = \'%s\'" % (username)
		results = self.queryDB(query)
		dbpass = "%s" % results[0]
		return pbkdf2_sha512.verify(password, dbpass)

	def create_usr(self, username = "", password = ""):
		if username == "" or password == "":
			print "Username or password blank"
		else:
			pwdhash = pbkdf2_sha512.encrypt(password)
			insert_cmd = "INSERT INTO users (username, password) VALUES (\'%s\', \'%s\')" % (
				username, pwdhash)
			try;
				self.exec_DB(insert_cmd)
				print "User %s added." % (username)
			except Exception as e:
				print "Error: exception ", e

	def generateRandUsers(numUsers):
		userconsole = User()
		for n in xrange(numUsers):
			fakename = userconsole.faker.name()
			fakename = ((fakename.replace(" ","")).replace(".","")).replace("'","")[:20]
			print fakename, ":", len(fakename)
			userconsole.create_usr(fakename, "asdf")
			userconsole.sqlcontrol.closeDB()





