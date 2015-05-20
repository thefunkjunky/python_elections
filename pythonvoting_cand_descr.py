# PythonVoting Candidates Module

import sys
from pythonvoting_dbModule import dbModule

class Cand_description(dbModule):
	"""Cand_description db Module"""
	def __init__(self):
		super(Cand_description, self).__init__('cand_descriptions', 'cand_descr_id')
		

	def assign_cand(self, cand_id):
		if self.itemcheck('candidates', 'cand_id', cand_id):
			self.cand_id = cand_id
			print "Current candidate ID is %i." % cand_id
		else: 
			print "Candidate Id# not found. Please assign another."
			self.cand_id = None

	def create_descr(self, cand_description):
		try:
			if self.itemcheck('candidates', 'cand_id', self.cand_id):
				if not self.itemcheck(self.table, 'cand_id', self.cand_id):
					cmd = "INSERT INTO cand_descriptions (cand_description, cand_id)" \
					"VALUES (\"%s\", \'%i\')" % (cand_description, self.cand_id)
					self.exec_DB(cmd)
					print "Description created."
			else:
				print "Checks failed."
		except:
			print "Invalid request: ", sys.exc_info()[0]

	def update_descr(self, cand_id, newvalues={}):
		del_values = ['cand_id']
		self.update('cand_descriptions', 'cand_id', cand_id, newvalues, del_values)

# cand_descr = Cand_description()
# cand_descr.assign_cand(1)
# cand_descr.create_descr("Says his opponent's 3% titatanium tax goes too far.")
# cand_descr.assign_cand(2)
# cand_descr.create_descr("Says his opponent's 3% titatanium tax doesn't go too far enough.")
# cand_descr.sqlcontrol.closeDB()

