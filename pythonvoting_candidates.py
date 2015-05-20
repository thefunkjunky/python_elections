# PythonVoting Candidates Module

import sys
from pythonvoting_dbModule import dbModule

class Candidates(dbModule):
	"""Candidate db Module"""
	def __init__(self, race_id):
		super(Candidates, self).__init__('candidates', 'cand_id')
		self.assign_race(race_id)


	def assign_race(self, race_id):
		if self.itemcheck('races', 'race_id', race_id):
			self.race_id = race_id
			print "Current race ID is %i." % race_id
		else: 
			print "Race Id# not found. Please assign another."
			self.race_id = None

	def create_candidate(self, cand_name):
		try:
			if self.itemcheck('races', 'race_id', self.race_id) and not self.itemcheck(
				self.table, 'cand_name', cand_name):
				# print "Checks passed."
				query = self.zip('races', 'race_id', self.race_id)
				electid = query['election_id']
				cmd = "INSERT INTO candidates (cand_name, race_id, election_id)" \
				"VALUES (\'%s\', \'%i\', \'%i\')" % (cand_name, self.race_id, electid)
				print cmd
				self.exec_DB(cmd)
				print "Candidate created."
			else:
				print "Checks failed."
		except:
			print "Invalid request: ", sys.exc_info()[0]

cand_ctrl = Candidates(1)
cand_ctrl.create_candidate("Jack Johnson")
cand_ctrl.create_candidate("John Jackson")
cand_ctrl.create_candidate("Richard Nixon")
cand_ctrl.create_candidate("FlyingSpaghettiMonster")
cand_ctrl.sqlcontrol.closeDB()
