# Python Voting by Garrett Anderson
# Main menu module

from passlib.hash import pbkdf2_sha512
from pythonvoting_global import MenuObject, User
import pickle


class MainMenu(MenuObject):
	"""The Main Menu"""

	def selected(self):
		while True:
			if self.usr_selection == 0:
				# print 'Logging in existing User'
				user_login()
				self.usr_selection = ""
			elif self.usr_selection == 1:
				# print "Create new User"
				create_user()
				self.usr_selection = ""
			elif self.usr_selection == 2:
				# print "View Polls"
				view_polls()
				self.usr_selection = ""
			else:
				print "Thank you for voting! Goodbye!"
				exit()

class UserDashboard(MenuObject):
	"""Regular User Dashboard"""
	def __init__(self):
		super(UserDashboard, self).__init__()
		
	def selected(self):
		pass

class AdminDashboard(MenuObject):
	"""Admin Dashboard"""
	def __init__(self):
		super(AdminDashboard, self).__init__()
	
	def selected(self):
		pass

class UserPollsMenu(MenuObject):
	"""Polls Menu for Regular User"""
	def __init__(self):
		super(UserPollsMenu, self).__init__()
	
	def selected(self):
		pass

class AdminPollsMenu(MenuObject):
	"""Polls Menu for Admin"""
	def __init__(self):
		super(AdminPollsMenu, self).__init__()
	
	def selected(self):
		pass

class EditUsersMenu(MenuObject):
	"""Admin 'Edit Users' Dashboard"""
	def __init__(self):
		super(EditUsersMenu, self).__init__()
		
	def selected(self):
		pass

class AdminSettings(MenuObject):
	"""Admin Settings Dashboard"""
	def __init__(self):
		super(AdminSettings, self).__init__()
		
	def selected(self):
		pass


def initmenus():
	main_menu_options = ['Log in User', 'Create New User', 'View polls']
	user_dashboard_options = ['View/Vote Polls', 'Change Password', 'Delete Account']
	admin_dashboard_options = ['View/Edit Polls', 'Edit UserDB', 'Admin Settings']

	user_polls_menu_options = ['View Polls', 'Vote', 'Clear Votes']
	admin_polls_menu_options = ['View Polls', 'Add Poll', 'Edit Poll', 'Remove Poll', 'Close Poll']
	admin_editusers_menu_options = ['List Users', 'Create User', 'Remove User','Reset User Password',
	 'Change User Password', 'Reset UserDB File']
	admin_settings_menu_options = ['Change Admin Password', 'Change max # Password Attempts',
	 'Reset UserDB', 'Reset PollsDB']


	global menu_main
	menu_main = MainMenu('Main Menu', main_menu_options)
	menu_userdashboard = UserDashboard('User Dashboard', user_dashboard_options)
	menu_admindashboard = AdminDashboard('Admin Dashboard', admin_dashboard_options)
	menu_userpolls = UserPollsMenu('Polls Menu', user_polls_menu_options)
	menu_adminpolls = AdminPollsMenu('Admin Polls Menu', admin_polls_menu_options)
	menu_admineditusers = EditUsersMenu('Admin Edit Users Menu', admin_editusers_menu_options)
	menu_adminsettings = AdminSettings('Admin Settings', admin_settings_menu_options)
	

	

def create_user():
	# print "Create a new user"
	userControl.create()
	if userControl.login != "":
		# Goto User Dashboard
		pass


def user_login():
	# print "Log in existing user"
	userControl.usrlogin()
	if userControl.login != "":
		# Goto User Dashboard
		pass

def view_polls():
	print "View Polls"


def mainmenu():

	print menu_main.name
	menu_main.presentoptions()
	menu_main.getinput()
	menu_main.selected()
	

print "Hello, welcome to Python Voting."
userControl = User()
initmenus()
mainmenu()
