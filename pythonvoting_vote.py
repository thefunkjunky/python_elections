# PythonVoting Voting Module

import sys
import random
from pythonvoting_dbModule import dbModule

class Vote(dbModule):
	"""Voting module"""
	def __init__(self):
		super(Vote, self).__init__('votes', 'vote_id')

		
	def assign_cand(self, cand_id):
		if self.itemcheck('candidates', 'cand_id', cand_id):
			self.cand_id = cand_id
			print "Current candidate ID is %i." % cand_id
		else: 
			print "Candidate Id# not found. Please assign another."
			self.cand_id = None

	def assign_user(self, user_id):
		if self.itemcheck('users', 'user_id', user_id):
			self.user_id = user_id
			print "Current User ID is %i." % user_id
		else: 
			print "User Id# not found. Please assign another."
			self.user_id = None

	def assign_ballotid(self):
		cmd = "SELECT max(ballot_id) from votes where race_id = \'%i\'" % (race_id)
		ballot_id = [item[0] for item in votectrl.queryDB(cmd)]
		print ballot_id
		if ballot_id[0] == None: ballot_id[0] = 1
		votectrl.ballot_id= ballot_id[0]

	def addVote(self, score):
		try:
			query = self.zip('candidates', 'cand_id', self.cand_id)
			race_id, election_id = query['race_id'], query['election_id']
			cmd = "INSERT INTO votes (score, cand_id, user_id, ballot_id, race_id, election_id)" \
			"VALUES (\'%i\', \'%i\', \'%i\', \'%i\', \'%i\', \'%i\')" % (\
				score, self.cand_id, self.user_id, self.ballot_id, race_id, election_id)
			self.exec_DB(cmd)
		except Exception, e:
			print "Invalid request: ", sys.exc_info()[0], e

	def gatherVotes(self, cand_id):
		scores = []
		cmd = "SELECT score FROM votes WHERE cand_id = \'%i\'" % (cand_id)
		scores = [item[0] for item in self.queryDB(cmd)]
		return scores

	def clearVotes(self, election_id):
		cmd = "SELECT "
		cmd = "SELECT vote_id FROM votes WHERE cand_id in "


def gen_randomvotes_IRV(race_id, user_range, minrange = 1):
	votectrl = Vote()
	cmd = "SELECT max(ballot_id) from votes where race_id = \'%i\'" % (race_id)
	ballot_id = [item[0] for item in votectrl.queryDB(cmd)]
	print ballot_id
	if ballot_id[0] == None: ballot_id[0] = 1
	votectrl.ballot_id= ballot_id[0]
	print votectrl.ballot_id
	for n in xrange(user_range[0],user_range[1]):
		votectrl.assign_user(n)
		votectrl.ballot_id += 1
		cmd = "SELECT cand_id FROM candidates WHERE race_id = \'%i\'" % (race_id)
		candidates = [item[0] for item in votectrl.queryDB(cmd)]
		print "Candidates: ", candidates
		for i in xrange(minrange, len(candidates) +1):
			randcand = random.choice(candidates)
			votectrl.assign_cand(randcand)
			candidates.remove(randcand) # update to use pop()?
			print "User %s casts their #%i choice for candidate id # %i on ballot %i" % (
				n, i, randcand, votectrl.ballot_id)
			votectrl.addVote(i)
	votectrl.sqlcontrol.closeDB()

def gen_votes_IRV(race_id, user_range, cand_scores):
	votectrl = Vote()
	cmd = "SELECT max(ballot_id) from votes where race_id = \'%i\'" % (race_id)
	ballot_id = [item[0] for item in votectrl.queryDB(cmd)]
	print ballot_id
	if ballot_id[0] == None: ballot_id[0] = 1
	votectrl.ballot_id= ballot_id[0]
	print votectrl.ballot_id
	print cand_scores
	for n in xrange(user_range[0],user_range[1]):
		votectrl.ballot_id += 1
		votectrl.assign_user(n)
		for cand_id,score in cand_scores.iteritems():
			votectrl.assign_cand(cand_id)
			print "User %s casts their #%i choice for candidate id # %i. Ballot #%i." % (
				n, score, cand_id, votectrl.ballot_id)
			votectrl.addVote(score)
	votectrl.sqlcontrol.closeDB()

gen_votes_IRV(1, [100,149], {1:1, 2:2, 3:3, 4:4})
gen_votes_IRV(1, [150,199], {2:1, 1:2, 4:3, 3:4})
gen_votes_IRV(1, [200,210], {3:1, 4:2, 1:3, 2:4})
gen_votes_IRV(1, [211,215], {4:1, 3:2, 2:3, 1:4})
gen_randomvotes_IRV(1, [2,500])


# votectrl = Vote()
# cmd = "SELECT max(ballot_id) from votes where race_id = \'%i\'" % (1)
# ballot_id = [item[0] for item in votectrl.queryDB(cmd)]
# print ballot_id
# if ballot_id[0] == None: ballot_id[0] = 1
# votectrl.ballot_id= ballot_id[0]
# candidates = [1,2,3,4]
# for user_id in xrange(2,500):
# 	votectrl.assign_user(user_id)
# 	votectrl.ballot_id += 1
# 	for cand in candidates:
# 		votectrl.assign_cand(cand)
# 		score = random.choice([0,1])
# 		print "score: ", score
# 		votectrl.addVote(score)
		







# votectrl.assign_cand(2)
# votectrl.assign_user(5)
# votectrl.addVote(1)
# print votectrl.gatherVotes(1)



# votectrl.sqlcontrol.closeDB()


