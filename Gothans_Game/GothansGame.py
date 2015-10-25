# Name				: GothansGame.py
# Author			: Jonathan Walker
# Created			: 17th September 2015
# Version			: 1.0

# Implementation of Gothans from the Planet Percal #25

# Concept from Learn Python the Hard Way ex43

from sys import exit
from random import randint


#Globals
CORRIDOR_KEY = 'central corridor'
ARMORY_KEY = 'armory'
BRIDGE_KEY = 'bridge'
ESCAPE_POD_KEY = 'escape pod'
DEATH_KEY = 'death'
FINISH_RESULT = 'done'

CC_CHEAT = 'pass cc'
ARMORY_CHEAT = 'pass armory'
BRIDGE_CHEAT = 'pass bridge'
EP_CHEAT = 'pass ep'

INVALID_ENTRY_RSP = 'DOES NOT COMPUTE!'
HELP_REQ_STR = '?'
OVERRIDE_CMD_STR = 'hack'

#---------------------------------------------------
#---------------------------------------------------
# Class: Attack
#
# DESCRIPTION:
# 	This is a static class used to handle attack data.
#---------------------------------------------------
#---------------------------------------------------
class Attack:
	# TODO: rename attacks to something more appropriate
	INVALID = 0
	ROCK = 1
	PAPER = 2
	SCISSORS = 3
	
	MAX_ATTACK_NUM = 3
	OPTION_STR = 'r/p/s/' + HELP_REQ_STR
	
	def is_valid(self, inputAttack):
		retVal = False
		
		if ((inputAttack == Attack.ROCK) or (inputAttack == Attack.PAPER) or (inputAttack == Attack.SCISSORS)):
			retVal = True
			
		return retVal
		
	def translate_cmd(self, attackCmd):
		retAttack = Attack.INVALID
		
		if (attackCmd == 'r'):
			retAttack = Attack.ROCK
		elif (attackCmd == 'p'):
			retAttack = Attack.PAPER
		elif (attackCmd == 's'):
			retAttack = Attack.SCISSORS
			
		return retAttack
		
	def get_random_attack(self):
		return randint(1, self.MAX_ATTACK_NUM)
	
	def print_desc(self):
		desc = """
		Rock (r) - beats scissors, loses to paper\n
		Paper (p) - beats scissors, loses to rock\n
		Scissors (s) - beats paper, loses to rock\n
		"""

		print "-------------"
		print "%s" % desc
		print "-------------"
		
	# Gets the attack name string based on number.
	# Returns empty string on invalid attackNum.
	def get_attack_name(self, attackNum):
		retStr = ""
		
		if (attackNum == Attack.ROCK):
			retStr = "Rock"
		elif (attackNum == Attack.PAPER):
			retStr = "Paper"
		elif (attackNum == Attack.SCISSORS):
			retStr = "Scissors"
		
		return retStr
		
	# Determines winning attack given 2 inputs.
	# Returns:
	#	- attack1 if tie or attack1 wins
	#	- attack2 if attack2 wins
	#	- INVALID attack if either input is invalid.
	def evaluate(self, attack1, attack2):
		retVal = self.INVALID
	
		if (self.is_valid(attack1) and self.is_valid(attack2)):
			# we have valid inputs to work with
			if (attack1 == self.ROCK):
				if (attack2 == self.PAPER):
					retVal = attack2
				else:
					retVal = attack1
					
			if (attack1 == self.PAPER):
				if (attack2 == self.SCISSORS):
					retVal = attack2
				else:
					retVal = attack1
					
			if (attack1 == self.SCISSORS):
				if (attack2 == self.ROCK):
					retVal = attack2
				else:
					retVal = attack1
		
		return retVal
	
#---------------------------------------------------
#---------------------------------------------------
# Class: Engine
#
# Member Variables:	
#		sceneMap - Map containing all available scenes
#--------------------------------------------------
#---------------------------------------------------		
class Engine(object):
	
	def __init__(self, sceneMap):
		self.sceneMap = sceneMap
		pass
		
	def play(self):
		print "------------------------------------------------"
		print "Gothans have invaded your spaceship... time to blow this baby and escape to the planet below!\n\n"
		# need while-loop here to drive game
		result = self.sceneMap.opening_scene()
		
		while (result != FINISH_RESULT):
			print "DEBUG_JW: Engine::play() - result = %s" % result
			result = self.sceneMap.next_scene(result)
			
		print"DONE!!!"
		exit(1)


#---------------------------------------------------
#---------------------------------------------------
# Class: Scene
#
# NOTE: This is the base class for all scenes
#---------------------------------------------------
#---------------------------------------------------
class Scene(object):
	
	def enter(self):
		print "Subclasses handle implentation."
		exit(1)
		
	# Runs attack scenario of user against Gothan.
	# Returns:
	#	- True if user wins, else False
	def run_attack(self):
		retVal = False
		
		done = False
				
		while (not done):
			answer = raw_input("[Attack %s]> " % Attack.OPTION_STR)
			
			anAttack = Attack()
			
			if (answer == HELP_REQ_STR):
				anAttack.print_desc()
			else:
				userAttack = anAttack.translate_cmd(answer)
				
				if (userAttack == Attack.INVALID):
					print INVALID_ENTRY_RSP
				else:
					gothanAttack = anAttack.get_random_attack()
					print "The Gothan attacks with %s" % anAttack.get_attack_name(gothanAttack)
					
					if (userAttack == gothanAttack):
						# we have a tie
						print "The two attacks cancel each other. Try again."
					else:
						result = anAttack.evaluate(userAttack, gothanAttack)
						
						if (result == userAttack):
							retVal = True
															
						done = True
		
		return retVal
		
		
	# Runs keypad scenario of user entering keycode.
	# Returns:
	#	- True if user passes, else False
	def run_keyPad(self, cheatCode, retryMax):
		retVal = False
		
		keyCode = randint(1, 9)
		print "DEBUG_JW: keyCode = %d" % keyCode
		print "DEBUG_JW: retryMax = %d" % retryMax
		
		tryCount = 0
		done = False
		 
		while (not done):
			answer = raw_input("[Code]> ")
			answerNum = int(answer)
			print "DEBUG_JW: answerNum = %d" % answerNum
		
			if ((answerNum == keyCode) or (answerNum == cheatCode)):
				retVal = True
				done = True
			else:
				tryCount += 1
				
				if (tryCount > retryMax):
					print """
					You ran out of guesses. The system sounds an alarm and locks you out!\n 
					A Gothan sneaks up and disembowels you with his super-sharp blade.
					"""
					done = True
		
		return retVal
		
		
class Death(Scene):
	
	def enter(self):
		retScene = FINISH_RESULT
		print "You died in a really horrifying way!"

		print "Do you want to play again (y/n)?"
		answer = raw_input("> ")
		
		if (answer == 'y'):
			retScene = CORRIDOR_KEY
		
		return retScene
		

class CentralCorridor(Scene):
	
	def enter(self):
		retScene = DEATH_KEY
		print " This is the Central Corridor. A Gothan stands before you. You must defeat him with an attack before proceeding."
		
		answer = raw_input("[Action]> ")
		
		if (answer == CC_CHEAT):
			retScene = ARMORY_KEY
		else:
			if (answer == 'attack'):
				isWin = self.run_attack()
				
				if (isWin):
					print "You defeated the Gothan!"
					retScene = ARMORY_KEY
				
			else:
				# user chose not to attack => Death
				print "The Gothan proceeds to dismember you."
		
		return retScene
		
	
		
		
class Armory(Scene):
	
	def enter(self):
		retScene = DEATH_KEY
		print "\nYou are now in the Laser Weapon Armory. This is where you get the neutron bomb."
		print "It must be placed on the bridge to blow up the ship. You must guess the keypad code to obtain the bomb."
		
		answer = raw_input("[Action]> ")
		
		if (answer == ARMORY_CHEAT):
			retScene = BRIDGE_KEY
		else:
			if (answer == 'keypad'):
				isWin = self.run_keyPad(ARMORY_CHEAT, 4)
				
				if (isWin):
					retScene = BRIDGE_KEY
				else:
					print "A Gothan hears the alarms and moves in to attack!"
					
					answer = raw_input("[Action]> ")
		
					if (answer == ARMORY_CHEAT):
						retScene = BRIDGE_KEY
					else:
						if (answer == 'attack'):
							isWin = self.run_attack()
							
							if (isWin):
								print "You defeated the Gothan but the door is still locked."
								
								done = False
								
								while (not done):
									answer = raw_input("[Action]> ")

									if (answer == ARMORY_CHEAT):
										retScene = BRIDGE_KEY
									else:
										if (answer == OVERRIDE_CMD_STR):
											# TODO: implement override
											retScene = BRIDGE_KEY
											done = True
										else:
											print INVALID_ENTRY_RSP
								
						else:
							# user chose not to attack => Death
							print "The Gothan proceeds to dismember you."
				
			elif (answer == OVERRIDE_CMD_STR):
				#TODO: implement override functionality
				retScene = BRIDGE_KEY
		
		return retScene
		
		
class Bridge(Scene):
	
	def enter(self):
		retScene = DEATH_KEY
		print "This is the Bridge. A Gothan stands in your way."
		print "You must defeat him in order to set the bomb and attempt to escape."
		
		answer = raw_input("[Action]> ")
		
		if (answer == BRIDGE_CHEAT):
			retScene = ESCAPE_POD_KEY
		
		return retScene
		pass
		
		
class EscapePod(Scene):
	
	def enter(self):
		retScene = DEATH_KEY
		print "This is the Escape Pod Bay. You must guess the correct escape pod in order to leave."
		
		escapeNum = '5' # TODO: implemnent random number
		answer = raw_input("[pod #]> ")
		
		
		
		if ((answer == escapeNum) or (answer == EP_CHEAT)):
			print "\n\nYou picked the correct escape pod and successfully removed yourself from a sticky situation. Good job!"
			
			retScene = FINISH_RESULT
		
		return retScene
		pass
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: Map
#
# Member Variables:	
#		sceneDict		- dictionary of all game scenes
#		firstScene		- key indicating starting scene
#---------------------------------------------------
#---------------------------------------------------
		
class Map(object):
	
	def __init__(self, startScene):
	
		# declare dict for all scenes
		self.sceneDict = {	CORRIDOR_KEY	: CentralCorridor(),
							ARMORY_KEY 		: Armory(),
							BRIDGE_KEY		: Bridge(),
							ESCAPE_POD_KEY	: EscapePod(),
							DEATH_KEY		: Death()	}
					 
		self.firstScene = startScene
		
		
	def next_scene(self, sceneName):
		# run the next scene and save off the result
		retScene = ''
		theNextScene = self.sceneDict.get(sceneName)
		
		if (not theNextScene):
			# should never get here
			print "ERROR: Map::next_scene() - invalid key %s" % sceneName
		else:
			retScene = theNextScene.enter()
		
		return retScene
		
		
	def opening_scene(self):
		return self.next_scene(self.firstScene)
			
		
# simple test
aMap = Map(CORRIDOR_KEY) # pass in the key for the starting scene
aGame = Engine(aMap)
aGame.play()