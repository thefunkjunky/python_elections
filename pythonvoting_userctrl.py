# Updated User Control
from passlib.hash import pbkdf2_sha512
import mysql.connector
from mysql.connector import errorcode
from collections import OrderedDict
from contextlib import closing
from pythonvoting_mySQLinterface import mySQLinterface

class User(object):
	"""Python Voting User Control"""
	def __init__(self):
		super(User, self).__init__()
		self.mysql_login = "root"
		self.mysql_pass = "t3chn0"
		self.login = dict(zip(['id','name','passhash'], [None, None, None]))
		self.openDB()

	def openDB(self):
		self.sqlcontrol = mySQLinterface()
		self.sqlcontrol.connectmySQL(self.mysql_login, self.mysql_pass)
		self.queryDB = self.sqlcontrol.queryDB
		self.exec_DB = self.sqlcontrol.exec_DB
		self.faker = self.sqlcontrol.faker

	def checkname(self, username = ""):
		query = "SELECT username FROM users WHERE username = \'%s\'" % (username)
		results = [item[0] for item in self.queryDB(query)]
		return username in results

	def checkpass(self, username, password):
		query = "SELECT password FROM users WHERE username = \'%s\'" % (username)
		results = self.queryDB(query)
		dbpass = "%s" % results[0]
		return pbkdf2_sha512.verify(password, dbpass)

	def yesno(self, yesno_input):
		if yesno_input.lower() in ['y', 'yes', 'yeah', 'yup']:
			return True
		elif yesno_input.lower() in ['n', 'no', 'nah', 'nope', 'naw']:
			return False
		else:
			return "Invalid"

	# def create_usr(self, username = "", password=""):
	# 	while True:
	# 		if username == "" or password = "": 
	# 			print "Username or password blank."
	# 		elif username == "0":
	# 			print "Quitting..."
	# 			break 
	# 		elif not self.checkname(username):
	# 			while True:
	# 				pass1 = raw_input('Please enter new password for %s. >' % (username))
	# 				pass2 = raw_input('Please re-enter new password for %s. >' % (username))
	# 				if pass1 == pass2:
	# 					pwdhash = pbkdf2_sha512.encrypt(pass1)
	# 					insert_cmd = "INSERT INTO users (username, password) VALUES (\'%s\', \'%s\')" % (
	# 						username, pwdhash)
	# 					self.exec_DB(insert_cmd)
	# 					self.login = username
	# 					print "User created! %s now logged in." % (username)
	# 					break
	# 				elif pass1 != pass2: 
	# 					print "Passwords did not match."
	# 					break
	# 			break
	# 		elif self.checkname(username): 
	# 			print "User already exists."
	# 			username = ""
	def create_usr(self, username = "", password = ""):
		if username == "" or password == "":
			print "Username or password blank"
		else:
			pwdhash = pbkdf2_sha512.encrypt(password)
			insert_cmd = "INSERT INTO users (username, password) VALUES (\'%s\', \'%s\')" % (
				username, pwdhash)
			self.exec_DB(insert_cmd)
			print "User %s added." % (username)

	def login_usr(self, username, password):
		if self.checkname(username):
			if self.checkpass(username, password):
				loginquery = self.queryDB(
					"SELECT user_id, username, password FROM users WHERE username = \'%s\'" % (username))
				id,name,passwd = loginquery[0]
				self.login = dict(zip(['id','name','passhash'], [id,name,passwd]))
				print "User %s logged in. UserID = %i." % (
					self.login['name'], self.login['id'])
				
			else: print "Wrong username or password."
		else: print "Wrong username or password."

	def delete_usr(self):
		if self.login['name'] != None:
			username = self.login['name']
			passwd = raw_input('Please enter your current password: ')
			if self.checkpass(username, passwd):
				dblchk = raw_input('Delete user %s? Are you sure? (Y or N) > ')
				if self.yesno(dblchk):
					userid = self.login['id']
					delete_cmd = "DELETE FROM users WHERE user_id= (\'%i\')" % (userid)
					self.exec_DB(delete_cmd)
					print "User %s deleted." % (username)
				else: print "Cancelling user deletion."
			else: print "Wrong username or password."
		else: print "Not logged in."

	def change_pwd(self):
		if self.login['name'] != None:
			username = self.login['name']
			oldpass = raw_input('Please enter your current password: ')
			if self.checkpass(username, oldpass):
				pass1 = raw_input('Please enter new password for %s. >' % (username))
				pass2 = raw_input('Please re-enter new password for %s. >' % (username))
				if pass1 == pass2:
					pwdhash = pbkdf2_sha512.encrypt(pass1)
					exec_cmd = "UPDATE users SET password= (\'%s\')" % (pwdhash)
					self.exec_DB(exec_cmd)
					print "Password for user %s updated." % (username)
				else: print "Passwords do not match."
			else: print "Wrong username or password."
		else: print "Not logged in."

def generateRandUsers(numUsers):
	userconsole = User()
	for n in xrange(numUsers):
		fakename = userconsole.faker.name()
		fakename = ((fakename.replace(" ","")).replace(".","")).replace("'","")[:20]
		print fakename, ":", len(fakename)
		userconsole.create_usr(fakename, "asdf")
		userconsole.sqlcontrol.closeDB()

# generateRandUsers(500)

# print userconsole.checkname('admin')
# print userconsole.checkpass('admin', 'fdsa')
# userconsole.create_usr('jason')
# userconsole.login_usr('biddy', 'asdf')
# userconsole.change_pwd()

userconsole.sqlcontrol.closeDB()

