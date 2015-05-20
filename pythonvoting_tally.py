# PythonVoting Tallying Module

import sys
import operator
from pythonvoting_dbModule import dbModule
from itertools import combinations

class Tally(dbModule):
	"""Tally Module"""
	def __init__(self):
		super(Tally, self).__init__('votes', 'race_id')

	def assign_race(self, race_id):
		if self.itemcheck('races', 'race_id', race_id):
			self.race_id = race_id
			print "Current race ID is %i." % race_id
		else: 
			print "Race Id# not found. Please assign another."
			self.race_id = None

	def gather_racedata(self, race_id):
		cmd = "SELECT race_type FROM races WHERE race_id = \'%i\'" % (race_id)
		self.racetype = [item[0] for item in self.queryDB(cmd)]
		cmd = "SELECT cand_id FROM candidates WHERE race_id = \'%i\'" % (race_id)
		self.candidates = [item[0] for item in self.queryDB(cmd)]
		print self.racetype
		print self.candidates

	def count_query(self, wherecmd, count_qry = "*"):
		cmd = "SELECT COUNT(%s) FROM votes %s" % (count_qry, wherecmd)
		return [item[0] for item in self.queryDB(cmd)]

	def returnHighestscore(self, wherecmd):
		cmd = "SELECT MAX(score) FROM votes %s" % (wherecmd)
		return [item[0] for item in self.queryDB(cmd)]

	def formatCands(self, candidates):
		formattedcands = "("
		for cand in candidates:
			formattedcands += str(cand) + ","
		formattedcands += ")"
		formattedcands = formattedcands.replace(",)", ")")
		return formattedcands

	def genBallotID(self, cmd):
		self.genCursor()
		try:
			self.gencursor.execute(cmd)
			for row in self.gencursor:
				print "Row in self.gencursor: ", row
				ballotid = row[0]
				print "ballotid: ", ballotid
				yield ballotid
		except Exception, e:
			print "EXCEPT THIS!!!", e


	def returnHighestCands(self, candidates, totals):
		results = {}
		maxscore = max(totals)
		maxscoreindices = [i for i,x in enumerate(totals) if x == maxscore]
		winners = [i for i in self.candidates if self.candidates.index(i) in maxscoreindices]
		results['MaxScore'] = maxscore
		results['Winner_IDs'] = [i for i in winners]
		return results

	def returnCandScores(self, candidates, totals):
		results = {}
		averages = []
		totalsum = float(sum(totals))
		averages = [i/totalsum for i in totals]
		for x,y in enumerate(self.candidates):
			results[y] = averages[x]
		return results


	def tally_WTA(self):
		totals = []
		for cand in self.candidates:
			cmd = "SELECT SUM(score) FROM votes WHERE cand_id = \'%i\' and race_id = \'%i\' and score='1'" % (cand, self.race_id)
			score = self.queryDB(cmd)[0][0]
			totals.append(score)
		print "totals: ", totals
		return self.returnHighestCands(self.candidates, totals)

	def tally_proportional(self):
		totals = []
		averages = []
		results = {}
		for cand in self.candidates:
			wherecmd = "WHERE cand_id = \'%i\' and score = '1'" % (cand)
			score = self.count_query(wherecmd)[0]
			totals.append(score)
		print totals
		totalsum = float(sum(totals))
		averages = [i/totalsum for i in totals]
		for x,y in enumerate(self.candidates):
			results[y] = averages[x]
		return results

	def irv_lowestcand(self, candidates, totals, blockelimination = True):
		results = {}
		sorted_cands = {}
		print "Totals: ", totals
		lowsum = 0
		losers = []
		sortedtotals = sorted(totals)
		print "Sortedtotals: ", sortedtotals
		print "Totals: ", totals
		lowscores = []

		if blockelimination == True:
			for i,n in enumerate(sortedtotals):
				lowsum += n
				print "lowsum: ", lowsum
				print "sortedtotals[i+1]: ", sortedtotals[i+1]
				if lowsum > sortedtotals[i+1]:
					print "Shit went over. time to break"
					break
				# elif lowsum == sortedtotals[i+1]:
					# lowscores.append(n)
					# break
				elif lowsum <= sortedtotals[i+1]:
					lowscores.append(n)
					print "lowscores: ", lowscores
		elif blockelimination == False:
			lowscores.append(min(totals))

		print "Lowscores :", lowscores
		print "Endlowscore: ", max(lowscores)
		print "Totals: ", totals


		for i,total in enumerate(totals):
			print "i, total: ", i,total
			if total <= max(lowscores):
				losers.append(candidates[i])
				print "Losers appended: ", losers

		results['LowScores'] = [i for i in lowscores]
		results['Loser_IDs'] = [i for i in losers]
		return results


	def tally_IRV(self, blockelimination = True):
		# Note: low score here represents higher preference, i.e. score of '1' means 1st choice
		totals = []
		results = {}
		candidates = self.candidates
		additionalcounts = {}
		highestcands = {}
		all_deleted_cands = []

		highestscore = self.returnHighestscore(
			"WHERE race_id = \'%i\'" % (self.race_id))[0]
		print "Highest score value: ", highestscore
		for i in candidates:
			additionalcounts[i] = 0
			print "additionalcounts: ", additionalcounts

		for round in xrange(1,highestscore+1):
			totals = []
			for cand in candidates:
				wherecmd = "WHERE cand_id = \'%i\' AND score = \'%i\'" % (cand, 1)
				score = self.count_query(wherecmd)[0]
				print "score before: ", score
				print "Additionalcount for cand# %i: %i" %(cand, additionalcounts[cand])
				score = self.count_query(wherecmd)[0] + additionalcounts[cand]
				print "score: ", score
				totals.append(score)
				print totals
			print "end of round: ", round
			print "tallying #1s."
			scores = self.returnCandScores(candidates, totals)
			print "scores: ", scores
			revscores = {v:k for k, v in scores.items()}


			if max(scores.values()) > 0.5:
				winner = revscores[max(scores.values())]
				print "Winner is: %i with %f percent of the votes." % (winner, scores[winner])
				return winner, scores[winner]
			
			elif max(scores.values()) < 0.5:
				nextbestscore = []
				deleted_cands = self.irv_lowestcand(candidates, totals, blockelimination)['Loser_IDs']
				print "Deleted_cands: ", deleted_cands
				for delcand in deleted_cands:
					candidates.remove(delcand)
					print "New, truncated candidates list: ", candidates
					print "delcand: ", delcand
				formattedcands = self.formatCands(candidates)
				formatted_del_cands = self.formatCands(deleted_cands)
				print "formatted_del_cands: ", formatted_del_cands
				delballotid_cmd = "SELECT ballot_id FROM votes WHERE (cand_id in %s AND score = 1)" % (formatted_del_cands)
				print "delballotid_cmd: ", delballotid_cmd

				for ballot_id in self.genBallotID(delballotid_cmd):
					cmd = "SELECT cand_id, min(score) FROM votes WHERE ballot_id=\'%i\' AND cand_id IN %s" % (
						ballot_id, formattedcands)
					next_cand_in_line = self.queryDB(cmd)[0][0]
					additionalcounts[next_cand_in_line] = additionalcounts[next_cand_in_line] + 1
					print "additionalcounts: ", additionalcounts
			else:
				print "I dont know what I'm doing here."

	def genPairResults_Schulze(self):

		# Much improved algorithm, with some help

		results = {}
		mostamazing_SELECT_ever = "SELECT tmp.cand1 As 'candidate1', tmp.cand2 AS 'candidate2', COUNT(*) FROM ( SELECT v1.`ballot_id`, v1.cand_id AS 'cand1', v1.score AS 'score1', v2.cand_id AS 'cand2', v2.score AS 'score2' FROM votes v1 INNER JOIN votes v2 ON (v1.ballot_id = v2.ballot_id) AND v1.cand_id <> v2.cand_id ) AS tmp WHERE tmp.score1 > tmp.score2 GROUP BY tmp.cand1, tmp.cand2"
		dbresults = self.queryDB(mostamazing_SELECT_ever)
		for data in dbresults:
			pair = data[0],data[1]
			results[pair] = data[2]
		return results
		
	def tally_Schulze(self):
		# Note: high score here represents higher preference, i.e. with a score of 4 vs 3, 4 wins
		pair_results = {}
		path_results = {}
		winner = {}
		pair_results = self.genPairResults_Schulze()
		candidates = self.candidates
		# I totally stole this algorithm.  BECAUSE I DONT UNDERSTAND SCHULZE
		for i in candidates:
			for j in candidates:
				if i != j:
					if pair_results[(i,j)] > pair_results[(j,i)]:
						path_results[(i,j)] = pair_results[(i,j)]
					else:
						path_results[(i,j)] = 0
		for i in candidates:
			for j in candidates:
				if i != j:
					for k in candidates:
						if (i != k) and (j != k):
							path_results[(j,k)] = max(path_results[(j,k)], min(path_results[(j,i)], path_results[(i,k)]))

		print "path_results: ", path_results

		for i in candidates:
			winner[i] = True
		for i in candidates:
			for j in candidates:
				if i != j:
					if path_results[(j,i)] > path_results[(i,j)]:
						winner[i] = False

		print "winner: ", winner
		return winner










tallyctrl = Tally()
tallyctrl.assign_race(1)
tallyctrl.gather_racedata(1)
# print tallyctrl.tally_WTA()
# print tallyctrl.tally_proportional()
# print tallyctrl.tally_IRV(True)
print tallyctrl.tally_Schulze()
tallyctrl.sqlcontrol.closeDB()



