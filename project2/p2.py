#!/usr/bin/env python3

# Anna Blendermann

import sys
import random
import collections
import decimal

# Reward for mutual cooperation
CC_REWARD = 3

# Reward for cooperating, when the other player defects
CD_REWARD = 0

# Reward for defecting, when the other player cooperates
DC_REWARD = 4

# Reward for mutual defection
DD_REWARD = 1


# Bots

class TFTBot:
	"""
	Plays Tit for Tat strategy, initally cooperating

	play_count is unused, but provides an example how to initialize
	instance variables in Python
	"""

	def __init__(self):
		self.rounds_played = 0

	def play(self, prev):
		"""
		prev refers to the other player's previous action; for the first
		action of a repeated game, prev will be None
		"""
		self.rounds_played += 1
		if prev == "D":
			return "D"
		else:
			return "C"

	def reset(self):
		"""
		Reset instance variables (call before each game of iterated
		prisoner's dilemma)
		"""
		self.rounds_played = 0


class CooperateBot:
	"""Always cooperates"""
	def __init__(self):
		pass

	def play(self, prev):
		return "C"

	def reset(self):
		pass


class DefectBot:
	"""Always defects"""
	def __init__(self):
		pass

	def play(self, prev):
		return "D"

	def reset(self):
		pass


class RandomBot:
	""""Plays randomly (equal probability)"""
	def __init__(self):
		pass

	def play(self, prev):
		if random.uniform(0, 1) > 0.5:
			return "C"
		else:
			return "D"

	def reset(self):
		pass

class GrudgeBot:
	"""
	GrudgeBot will cooperate in IPD until the other player defects,
	after which GrudgeBot will always defect
	"""
	def __init__(self):
		self.holding_grude = 0

	def play(self, prev):
	if prev == "D":
		self.holding_grude = 1

	if self.holding_grude == 1:
		return "D"
	else:
		return "C"

	def reset(self):
		self.holding_grudge = 0


class ForgivingBot:
	"""	
	ForgivingBot will cooperate, unless the other player has defected
	in the previous two rounds (also known as "Tit for two tats")
	"""
	def __init__(self):
		self.patience = 0

	def play(self, prev):	
		if prev == "D":
			self.patience += 1

		if self.patience == 2:
			return "D"
		else:
			return "C"
	
	def reset(self):
		self.patience = 0


# Some helper functions

def duplicate_bot(old_bot):
	"""Return a new instance of old_bot's class"""
	return old_bot.__class__()


def name_of_bot(bot):
	"""Return the name of bot's class"""
	return bot.__class__.__name__


def count_bots(bots):
	"""Count the number of each type of bot in a list of bots"""
	return dict(collections.Counter([name_of_bot(b) for b in bots]))


# TODO: implement play_ipd, play_tournament, evolutionary_ipd

def play_ipd(bot1, bot2, rounds, noise=0.0):
	"""
	Play iterated prisoner's dilemma between bot1 and bot2

	rounds - number of rounds
	noise - probability that a bot performs the OPPOSITE of its intended
			action; by default, this probability is zero

	Return (a, b) where a is total utility of bot1, b is total utility bot2
	"""

	# Instantiate both bots and utility vars
	playBot1 = bot1()
	playBot2 = bot2()
	utilBot1 = 0, utilBot2 = 0
	
	# Get the first move from bot1
	moveBot1 = get_move(bot1, None, noise)

	# Play rounds for bot1 and bot2, adding rewards as you go
	x = 0
	currentBot = bot2
	prev = moveBot1

	while (x < rounds):
	move = get_move(currentBot, prev, noise) 
		utilBot1 += get_reward(prev, move)
	utilBot2 += get_reward(move, prev)
	bot = bot1
	prev = move # clever!
		
	return (utilBot1, utilBot2)


def get_move(bot, prev, noise)

	move = bot.play(noise)

	prob_flip = decimal.Decimal(random.randrange(0, 50))/100
		if (prob_flip < noise):
 		if move == "C":
		return "D"
		else:
		return "C"
	else:
		return move


def get_reward(move, prev)

	if prev == "C":
	if move == "C":
		return CC_REWARD
	elif move == "D"
		return DC_REWARD
	else prev == "D":
	if move == "C":
		return CD_REWARD
	elif move == "D"
		return DD_REWARD
	 

def play_tournament(bots, rounds, noise=0.0):
	"""
	Play a round-robin IPD tournament
	Every bot plays every other bot exactly once
	Bots DO NOT play against themselves.

	bots - list of bot objects
	rounds - number of rounds in IPD
	
	Return list of (utility, bot), where utility is the total utiltiy
	and bot is the Bot object, e.g. 
	[(10, <CooperateBot instance at 0x...), ...
	"""
	return []


def evolutionary_ipd(bots, rounds, generations, noise=0.0):
	"""
	Play an IPD tournament for a given number of rounds

	At the end, the two highest scoring bots get duplicated; the two
	lowest scoring bots get removed. This becomes a 'new generation'.
	Repeat this process for a given number of 'generations'

	bots - list of bot objects
	rounds - number of rounds for each iterated prisoner's dilemma
	generations - number of tournaments to play; each tournament
				  constitutes a 'generation'

	Return the last generation (a list of bot objects)
	"""
	return []

def main():

	population = ([CooperateBot() for i in range(5)]
				+ [DefectBot() for i in range(5)]
				+ [TFTBot() for i in range(5)])

	play_ipd(CooperateBot(), DefectBot())


def main2():
	"""Example: play evolutionary IPD with different noise levels"""

	# Initial population is 5 Cooperate, Defect and TFT Bots
	population = ([CooperateBot() for i in range(5)]
				+ [DefectBot() for i in range(5)]
				+ [TFTBot() for i in range(5)])
	
	# Low noise; favors CooperateBot and TFTBot
	print(count_bots(evolutionary_ipd(population, 10, 20, 0.05)))

	# Medium noise
	print(count_bots(evolutionary_ipd(population, 10, 20, 0.1)))

	# High noise; favors DefectBot
	print(count_bots(evolutionary_ipd(population, 10, 20, 0.25)))


if __name__ == "__main__":
	main()

