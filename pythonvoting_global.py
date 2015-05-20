# Python Voting Global Classes Module
# by Garrett Anderson
from passlib.hash import pbkdf2_sha512



class MenuObject(object):
	"""Generic Menu Class Object. Send name as a string, options as
	a list of strings.  'Quit' is automatically added to list"""
	def __init__(self, name, options):
		super(MenuObject, self).__init__()
		self.name = name
		self.options = options
		self.options.append('Quit')
		self.usr_selection = 'unassigned'

	def presentoptions(self):
		print self.name
		print "Please choose from the following options:"
		for x in self.options:
			print '(', self.options.index(x), ') ', x

	def getinput(self):
		while True:
			try:
				self.usr_selection = int(raw_input('> '))
				if self.usr_selection in range(len(self.options)):
					print "Thank you for choosing: (%i) %s" % (self.usr_selection, 
						self.options[self.usr_selection])
					break
				else:
					print "Invalid selection. Please choose a # between 0 and ", \
					len(self.options)
			except ValueError:
				print "Input was not a digit.  Please try again."

	def selected(self):
		print "Nothing has been assigned to the selected() function"

class User(object):
	"""Python Voting User Control"""
	def __init__(self):
		super(User, self).__init__()
		self.login = ""
		self.userDB = {}
		self.openDB()

	def newDB(self):
		self.userDB_clear= open('userdb.udb', 'w')
		while True:
			pass1 = raw_input('Please enter new Admin password. >')
			pass2 = raw_input('Please re-enter new Admin password. >')
			if pass1 == pass2:
				pwdhash = pbkdf2_sha512.encrypt(pass1)
				user_pass = "admin " + pwdhash + "\n"
				self.userDB_clear.write(user_pass)
				self.userDB_clear.close()
				break
			else: print "Passwords did not match."

	def openDB(self):
		# self.userDB_r = open('userdb.udb', r)
		for line in open('userdb.udb', 'r'):
			user, passwd = line.split(' ', 2)
			# print user, passwd
			# self.userDB = {user:passwd for user,passwd in line.split(' ', 2)}
			# self.userDB[user] = passwd
			self.userDB.update({user:passwd.rstrip("\n")})
			# print self.userDB

	def checkname(self, username = ""):
		return username in self.userDB

	def checkpass(self, username, password):
		return pbkdf2_sha512.verify(password, self.userDB[username])

	def yesno(self, yesno_input):
		if yesno_input.lower() in ['y', 'yes', 'yeah', 'yup']:
			return True
		elif yesno_input.lower() in ['n', 'no', 'nah', 'nope', 'naw']:
			return False
		else:
			return "Invalid"

	def create(self, username = ""):
		# self.openDB()
		
		while True:
			if username == "": 
				username = raw_input('Please enter new User Name. (0) to quit. > ')
			elif username == "0":
				print "Quitting..."
				break 
			elif not self.checkname(username):
				while True:
					pass1 = raw_input('Please enter new password for %s. >' % (username))
					pass2 = raw_input('Please re-enter new password for %s. >' % (username))
					if pass1 == pass2:
						pwdhash = pbkdf2_sha512.encrypt(pass1)
						user_pass = username +" " + pwdhash + "\n"
						self.userdb_append= open('userdb.udb', 'a')
						self.userdb_append.write(user_pass)
						self.userdb_append.close()
						self.login = username
						print "User created! %s now logged in." % (username)
						break
					elif pass1 != pass2: 
						print "Passwords did not match."
				break
			elif self.checkname(username): 
				print "User already exists."
				username = ""

	def usrlogin(self):
		print "Log in Existing User."
		# self.openDB()
		while True:
			username = raw_input('Please enter User Name. (0) to quit: ')
			if username == '0':
				print "Quitting..."
				break
			elif self.checkname(username):
				wrongattempts = 0
				while wrongattempts < 4:
					password = raw_input('Please enter password for %s: ' % (username))
					if self.checkpass(username, password):
						self.login = username
						self.password = password
						print "User %s logged in successfully." % (username)
						break
					else: 
						wrongattempts += 1
						print "Wrong password. %i of 3 attempts used." % (wrongattempts)
						if wrongattempts >= 3: 
							print "Too many incorrect logins. Now exiting."
							break

			elif not self.checkname(username):
				print "User %s does not exist. Would you like to create it? (Y/ N)" % (username)
				yesnoinput = raw_input('> ')
				if self.yesno(yesnoinput):
					self.create(username)
				elif not self.yesno(yesnoinput):
					continue
				else:
					print "Invalid Input. Assuming 'NO'."
					continue
			break

	def deleteusr(self, username = ""):
		# self.openDB()
		print "Delete User..."
		userDB_formatted = {}
		for key,value in self.userDB.iteritems():
			userDB_formatted[key] = value + "\n"

		while True:
			if self.login == "":
				print "Not logged in."
				self.usrlogin()
				# break
				continue
			elif self.login != "admin":
				username = self.login
				print "username: ", username
				break
			elif self.login == "admin":
				while not self.checkname(username):
					username = raw_input('Please enter a user currently in the db. (0) to quit: ')
					if username == '0':
						print "Quitting..." 
						break
					elif self.checkname(username) and username != "admin":
						print "User %s selected." % (username)
						break
					elif username == "admin":
						print "Cannot delete admin account."
						username = ""
					elif not self.checkname(username):
						print "Account doesn't exist."
						username = ""

				break

		confirm = raw_input('Are you sure you want to delete user %s? (Y or N)> ' % (username))
		if self.yesno(confirm):
			del userDB_formatted[username]
			# print "formatted after delete: \n", userDB_formatted
			userDB_raw = ""
			for key, value in userDB_formatted.iteritems():
				userDB_raw = userDB_raw + key + " " + value
			# print "userDB_raw", userDB_raw
			self.userdb_overwrite = open('userdb.udb', 'w')
			self.userdb_overwrite.write(userDB_raw)
			self.userdb_overwrite.close()
			print "%s deleted." % (username)
		elif not self.yesno(confirm):
			print "Cancelling operation..."
			# break
		else:
			print "Invalid input. Cancelling operation..."
			# break

	def changepwd(self, username = ""):
		# self.openDB()
		print "Change Password..."
		userDB_formatted = {}
		for key,value in self.userDB.iteritems():
			userDB_formatted[key] = value + "\n"

		while True:
			if self.login == "":
				print "Not logged in."
				self.usrlogin()
				# break
				continue
			elif self.login != "admin":
				username = self.login
				print "username: ", username
				break
			elif self.login == "admin":
				while not self.checkname(username):
					username = raw_input('Please enter a user currently in the db. (0) to quit: ')
					if username == '0':
						print "Quitting..." 
						break
					elif self.checkname(username) and username != "admin":
						print "User %s selected." % (username)
						break
					elif not self.checkname(username):
						print "Account doesn't exist."
						username = ""
				break

		newpass1 = raw_input('Please enter new password for user %s> ' % (username))
		newpass2 = raw_input('Please re-enter new password for user %s> ' % (username))
		if newpass1 == newpass2:
			userDB_formatted[username] = pbkdf2_sha512.encrypt(newpass1) + "\n" 
			# print "formatted after delete: \n", userDB_formatted
			userDB_raw = ""
			for key, value in userDB_formatted.iteritems():
				userDB_raw = userDB_raw + key + " " + value
			# print "userDB_raw", userDB_raw
			self.userdb_overwrite = open('userdb.udb', 'w')
			self.userdb_overwrite.write(userDB_raw)
			self.userdb_overwrite.close()
			print "Password for %s changed." % (username)
		elif newpass1 != newpass2:
			print "Passwords don't match. Cancelling operation..."
			# break
		else:
			print "Invalid input. Cancelling operation..."
			# break

