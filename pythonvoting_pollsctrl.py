# Python Voting by Garrett Anderson
# Polls Class module

import pickle

class PollsControl(object):
	"""docstring for PollsControl"""
	def __init__(self):
		super(PollsControl, self).__init__()
		self.name = "Empty Poll"
		self.type = ""
		self.openStatus = True
		self.options = []
		self.username = ""

	def displayPolls(self, username = ""):
		if username == "":
			print "No user passed in arg1"
		else:
			self.username = username

	def vote(self, username = ""):
		pass

	def calcResults(self):
		pass

	def closePoll(self):
		pass
	
	


