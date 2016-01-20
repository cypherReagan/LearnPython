# Name				: GothansGame.py
# Author			: JWalker
# Created			: 17th September 2015
# Version			: 1.0
# Runtime			: Python27

# Implementation of Gothans Attack

# Concept from Learn Python the Hard Way ex43

from sys import exit
from random import randint
import random
import AsciiArt
import os
import platform


DEBUG_MODE = False

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
PROMPT_CONTINUE_STR = "[Press any key to continue...]> "
INVALID_OVERRIDE_EQUIP_RSP = "You do not have the necessary equipment for an override."

# User Action Commands
HELP_REQ_STR = '?'
OVERRIDE_CMD_STR = 'hack'
SEARCH_CMD_STR = 'search'
#DEBUG_JW: - TODO - add cheat cmds to restore player health, add weapons, ect...
# Also, player xp goes to 0 when you cheat

# Utility function to clear shell
def Clear_screen():
		
	if (DEBUG_MODE):
		x = 1
	else:	
		if (platform.system() == 'Windows'):
			os.system('cls')
		else:
			os.system('clear') # Linux/Mac OS

#---------------------------------------------------
#---------------------------------------------------
# Class: Attack
#
# DESCRIPTION:
# 	This is a static class used to handle attack data.
#---------------------------------------------------
#---------------------------------------------------
class Attack:

	INVALID = 0
	SLEDGEHAMMER = 1
	NET = 2
	KNIFE = 3
	
	MAX_ATTACK_NUM = 3

	ATTACK_OPTION_STR = """
	Attack Options:\n\n
	1. Sledgehammer\n
	2. Net\n
	3. Knife\n\n
	"""
	
	def is_valid(self, inputAttack):
		retVal = False
		
		if ((inputAttack == Attack.SLEDGEHAMMER) or (inputAttack == Attack.NET) or (inputAttack == Attack.KNIFE)):
			retVal = True
			
		return retVal
		
	def translate_cmd(self, attackCmd):
		retAttack = Attack.INVALID
		
		if (attackCmd == '1'):
			retAttack = Attack.SLEDGEHAMMER
		elif (attackCmd == '2'):
			retAttack = Attack.NET
		elif (attackCmd == '3'):
			retAttack = Attack.KNIFE
			
		return retAttack
		
	def get_random_attack(self):
		return randint(1, self.MAX_ATTACK_NUM)
	
	def print_desc(self):
		desc = """
		Sledgehammer (s) - beats knife, loses to net\n
		Net (n) - beats sledgehammer, loses to knife\n
		Knife (k) - beats paper, loses to sledgehammer\n
		"""

		print "-------------"
		print "%s" % desc
		print "-------------"
		
	# Gets the attack name string based on number.
	# Returns empty string on invalid attackNum.
	def get_attack_name(self, attackNum):
		retStr = ""
		
		if (attackNum == Attack.SLEDGEHAMMER):
			retStr = "Slaedgehammer"
		elif (attackNum == Attack.NET):
			retStr = "Net"
		elif (attackNum == Attack.KNIFE):
			retStr = "Knife"
		
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
			if (attack1 == self.SLEDGEHAMMER):
				if (attack2 == self.NET):
					retVal = attack2
				else:
					retVal = attack1
					
			if (attack1 == self.NET):
				if (attack2 == self.KNIFE):
					retVal = attack2
				else:
					retVal = attack1
					
			if (attack1 == self.KNIFE):
				if (attack2 == self.SLEDGEHAMMER):
					retVal = attack2
				else:
					retVal = attack1
		
		return retVal
	
#---------------------------------------------------
#---------------------------------------------------
# Class: Override
#
# Member Variables:	
#		wireDict - dictionary containing override config
#--------------------------------------------------
#---------------------------------------------------		
class Override(object):
	
	# global IDs
	KEYPAD_ID = 0
	DOOR_ID = 1
	BATTERY_ID = 2
	
	COLOR_ID_STR_RED = '1'
	COLOR_ID_STR_GREEN = '2'
	COLOR_ID_STR_YELLOW = '3'
	
	OVERRIDE_RESULT_SUCCESS = 1
	OVERRIDE_RESULT_FAIL = 2
	OVERRIDE_RESULT_DECLINE = 3
	
	OVERRIDE_OPTION_STR = """
	Override Options:\n\n
	1. Red\n
	2. Green\n
	3. Yellow\n\n
	""" 
	
	# DEBUG_JW - determine why these cannot go in init()
	wireDict = {
			'keypad': '',
			'door': '',
			'battery': ''
		}
	
	def __init__(self):
		
		self.set_wires()
		
	def set_wires(self):
		# randomize wire selection
		wireColorList = ['red', 'green', 'yellow']
		random.shuffle(wireColorList)
		
		self.wireDict['keypad'] = wireColorList[self.KEYPAD_ID]
		self.wireDict['door'] = wireColorList[self.DOOR_ID]
		self.wireDict['battery'] = wireColorList[self.BATTERY_ID]
		
	
	# Determines successful override given 2 input wires. 
	# Success = cross 'door' with 'battery'.
	# Returns TRUE if override succeeds, else FALSE
	def evaluate(self, wireStr1, wireStr2):
	
		retVal = False
		
		print "DEBUG_JW: door wire = %s" % self.wireDict['door']
		print "DEBUG_JW: battery wire = %s" % self.wireDict['battery']
		
		cond1 = ((wireStr1 == self.wireDict['door']) and (wireStr2 == self.wireDict['battery']))
		cond2 = ((wireStr1 == self.wireDict['battery']) and (wireStr2 == self.wireDict['door']))
		
		if ((cond1) or (cond2)):
			retVal = True
		
		return retVal
		
	# Returns the wire color of each override element	
	def get_wire_color(self):
		
		keyPadStr = self.wireDict['keypad']
		doorStr = self.wireDict['door']
		batteryStr = self.wireDict['battery']
		
		return keyPadStr, doorStr, batteryStr
		
		
	# Verify that the wire menu input is valid and convert them if necessary.
	# Returns converted wire string if valid, else INVALID_ENTRY_RSP.
	def translate_cmd(self, wireStr):
	
		retStr = '' 
		isValid = True
		
		# normalize to lowercase for future evalution
		wireStr = wireStr.lower()
		
		if ((wireStr == self.COLOR_ID_STR_RED) or (wireStr == 'red')):
			if (wireStr == self.COLOR_ID_STR_RED):
				wireStr = 'red'
			
		elif ((wireStr == self.COLOR_ID_STR_GREEN) or (wireStr == 'green')):
			if (wireStr == self.COLOR_ID_STR_GREEN):
				wireStr = 'green'

		elif ((wireStr == self.COLOR_ID_STR_YELLOW) or (wireStr == 'yellow')):
			if (wireStr == self.COLOR_ID_STR_YELLOW):
				wireStr = 'yellow'

		else:
			isValid = False
			
		if (isValid):
			retStr = wireStr
		else:
			retStr = INVALID_ENTRY_RSP
		
		return retStr
		

#---------------------------------------------------
#---------------------------------------------------
# Class: Player
#--------------------------------------------------
#---------------------------------------------------		
class Player(object):
	
	
	def __init__(self):
		self.reset_data()
		
	def reset_data(self):
		self.health = 100
		self.xp = 0
		self.theInventoryMgr = InventoryMgr()
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: InventoryMgr
#
# Member Variables:	
#		utilItemDict - dictionary containing utility items
#--------------------------------------------------
#---------------------------------------------------		
class InventoryMgr(object):
	
	# Item type IDs
	TYPE_ID_UTILITY = 0
	TYPE_ID_WEAPON = 1
	
	# DEBUG_JW - determine why these cannot go in init()
	utilItemDict = {}
		
		
	def add_item(self, typeID, newItem):
		
		if (typeID == TYPE_ID_UTILITY):
			# append to list
			self.utilItemDict[newItem.name] = newItem
		else:
			print "ERROR: Feature not implemented yet!"
			
			
	def print_items(self):
		#TODO - test this
	
		count = 1 
		
		for name in self.utilItemDict.items():
			print "%d. %s" % (count, name)
		
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: Item
#--------------------------------------------------
#---------------------------------------------------		
class Item(object):

	def __init__(self):
		# should never get here
		print "Item Subclasses handle implentation."
		exit(1)

		
#---------------------------------------------------
#---------------------------------------------------
# Class: UtilityItem
#--------------------------------------------------
#---------------------------------------------------		
class UtilityItem(Item):

	def __init__(self, newName, newCount):
		self.name = newName
		self.count = newCount

		
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
		
	def play(self):
		Clear_screen()
		print "------------------------------------------------------------------------------------------------"
		print AsciiArt.GothansGameTitle
		print "------------------------------------------------------------------------------------------------\n"
		print """
		Gothans have invaded your spaceship and killed everyone else on board. 
		Time to blow this baby and escape to the planet below!\n\n
		"""
		
		startMenuStr = """
			1. Start Game
			2. Help
			3. Quit
		"""
		
		helpStr = """
			 Use the '?' in action prompts for hints on how to proceed.
		""" 
		
		done = False
		
		while (not done):
			answer = raw_input("%s\n\t\t> " % startMenuStr)
			
			if (answer == '1'):
				done = True
			elif (answer == '2'):
				Clear_screen()
				print helpStr
				raw_input(PROMPT_CONTINUE_STR)
				Clear_screen()
			elif (answer == '3'):
				Clear_screen()
				exit(1)
			else:
				print INVALID_ENTRY_RSP
				Clear_screen()

		#DEBUG_JW - create player and pass them to every scene. 
		# Each scene should return the player obj to maintain state.
		thePlayer = Player()
		
		# need while-loop here to drive game
		result, thePlayer = self.sceneMap.opening_scene(thePlayer)
		
		while (result != FINISH_RESULT):
			result, thePlayer = self.sceneMap.next_scene(result, thePlayer)
			
		Clear_screen()
		print AsciiArt.GameOverMsg
		print "DEBUG_JW: Engine::play() - thePlayer.xp = %d" % thePlayer.xp
		exit(1)


#---------------------------------------------------
#---------------------------------------------------
# Class: Scene
#
# NOTE: This is the base class for all scenes
#---------------------------------------------------
#---------------------------------------------------
class Scene(object):
	
	def enter(self, thePlayer):
		# should never get here
		print "Scene Subclasses handle implentation."
		exit(1)
		

	# Runs attack scenario of user against Gothan.
	# Returns:
	#	- True if user wins, else False
	def run_attack(self):
		retVal = False
		
		done = False
				
		while (not done):
			answer = raw_input("%s> " % Attack.ATTACK_OPTION_STR)
			anAttack = Attack()
			
			if (answer == HELP_REQ_STR):
				anAttack.print_desc()
			else:
				userAttack = anAttack.translate_cmd(answer)
				
				if (userAttack == Attack.INVALID):
					print INVALID_ENTRY_RSP
				else:
					gothanAttack = anAttack.get_random_attack()
					print "\nThe Gothan attacks with %s" % anAttack.get_attack_name(gothanAttack)
					
					if (userAttack == gothanAttack):
						# we have a tie
						print "The two attacks cancel each other. Try again."
					else:
						result = anAttack.evaluate(userAttack, gothanAttack)
						
						if (result == userAttack):
							print "You defeated the Gothan!"
							retVal = True
						else:
							print "The Gothan defeated you."
															
						done = True
		
		return retVal
		
		
	# Runs scenario of user entering keycode.
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
			
			if (answer == OVERRIDE_CMD_STR):
			
				userHasBattery = True #DEBUG_JW: TODO - implement inventory
			
				if (not userHasBattery):
					print INVALID_OVERRIDE_EQUIP_RSP
				else:
					retVal = self.run_keypad_override()
					done = True
			else:
                # DEBUG_JW: TODO - check for invalid inputs (i.e. ENTER key)
				answerNum = int(answer)
				print "DEBUG_JW: answerNum = %d" % answerNum
			
				if ((answerNum == keyCode) or (answerNum == cheatCode)):
					retVal = True
					done = True
					print "You successfully opened the door!"
				else:
					tryCount += 1
					
					if (tryCount > retryMax):
						print """
						You ran out of guesses. The system sounds an alarm and locks you out!\n 
						DEBUG_JW - move this death elsewhere: A Gothan sneaks up and disembowels you with his super-sharp blade.
						"""
						done = True
					else:
						print "You entered an incorrect code. Please try again."
		
		return retVal
	
	
	# Runs scenario of user overriding keypad.
	# Returns:
	#	- True if user passes, else False	
	def run_keypad_override(self):
		retVal = False
		
		anOverride = Override()
		keypadWire, doorWire, batteryWire = anOverride.get_wire_color()
		
		print "You pry off the panel to reveal a series of wires.\n"
		print AsciiArt.OverrideDiagram2Wire
		print AsciiArt.OverrideDiagram2Wire_Seed % (keypadWire, doorWire)

		useBattery = True #DEBUG_JW: implement Inventory class and prompt user to use item
		if (not useBattery):
			print INVALID_OVERRIDE_EQUIP_RSP
		else:
			Clear_screen()
			print AsciiArt.OverrideDiagram3Wire
			print AsciiArt.OverrideDiagram3Wire_Seed % (keypadWire, doorWire, batteryWire) 
		
			print "\n\nChoose the wires to cross.\n"
			done = False

			# get user input for crossing wires
			while (not done):

				wireStr1 = raw_input("\tWire 1 %s> " % Override.OVERRIDE_OPTION_STR)
				wireStr1 = anOverride.translate_cmd(wireStr1)
				
				if (wireStr1 == INVALID_ENTRY_RSP):
					print INVALID_ENTRY_RSP
				else:
					wireStr2 = raw_input("\n\tWire 2 %s> " % Override.OVERRIDE_OPTION_STR)
					wireStr2 = anOverride.translate_cmd(wireStr2)
					
					if (wireStr2 == INVALID_ENTRY_RSP):
						print INVALID_ENTRY_RSP
					else:
						done = True
			
			retVal = anOverride.evaluate(wireStr1, wireStr2)
			
			if (retVal == True):
				print "You successfully hacked the door!\n\n"
			else:
				print """
				You failed to open the door and security now countermeasures activate.\n
				Toxic nerve gas releases, causing you to asphyxiate immediately.
				"""
		return retVal
		
		
class Death(Scene):
	
	def enter(self, thePlayer):
		retScene = FINISH_RESULT
		self.ThePlayer = thePlayer
		
		Clear_screen()
		print AsciiArt.Skull
		print "You died in a really horrifying way!"

		print "Do you want to play again (y/n)?"
		answer = raw_input("> ")
		
		if (answer == 'y'):
			retScene = CORRIDOR_KEY
		
		return retScene, self.ThePlayer
		

class CentralCorridor(Scene):
	
	def enter(self, thePlayer):
		retScene = DEATH_KEY
		self.ThePlayer = thePlayer
		
		Clear_screen()
		print " This is the Central Corridor. A Gothan stands before you. You must defeat him with an attack before proceeding."
		
		answer = raw_input("[Action]> ")
		
		if (answer == CC_CHEAT):
			retScene = ARMORY_KEY
		else:
			if (answer == 'attack'):
				isWin = self.run_attack()
				
				if (isWin):
					retScene = ARMORY_KEY
				
			else:
				# user chose not to attack => Death
				print "The Gothan proceeds to dismember you."
		
		raw_input(PROMPT_CONTINUE_STR)	
		
		return retScene, self.ThePlayer
		
	
		
		
class Armory(Scene):
	
	def enter(self, thePlayer):
		retScene = DEATH_KEY
		self.ThePlayer = thePlayer
		
		Clear_screen()
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
							
							#DEBUG_JW - remove 'or not isWin' which is only for testing
							if (isWin or not isWin):
								print "You defeated the Gothan but the door is still locked."
								#DEBUG_JW: - TODO - allow the user to search the defeated enemy for a battery pack (which will facilitate an override)
								
								done = False
								userHasBattery = False #DEBUG_JW - implement inventory
								
								while (not done):
									answer = raw_input("[Action]> ")

									if (answer == ARMORY_CHEAT):
										retScene = BRIDGE_KEY
									else:
										if (answer == OVERRIDE_CMD_STR):
											if (not userHasBattery):
												print INVALID_OVERRIDE_EQUIP_RSP
											else:
												# user chose to override the keypad
												isWin = self.run_keypad_override()
												
												if (isWin):
													retScene = BRIDGE_KEY
												done = True
											
										elif (answer == SEARCH_CMD_STR):
											print "You search the Gothans dead body and find a battery pack!"
											
											batteryItem = UtilityItem('battery', 1)
											userHasBattery = True
										else:
											print INVALID_ENTRY_RSP
								
						else:
							# user chose not to attack => Death
							print "The Gothan proceeds to dismember you."
							
		
		raw_input(PROMPT_CONTINUE_STR)	
		
		return retScene, self.ThePlayer
		
		
class Bridge(Scene):
	
	def enter(self, thePlayer):
		retScene = DEATH_KEY
		self.ThePlayer = thePlayer
		
		Clear_screen()
		print "This is the Bridge. A Gothan stands in your way."
		print "You must defeat him in order to set the bomb and attempt to escape."
		
		answer = raw_input("[Action]> ")
		
		if (answer == BRIDGE_CHEAT):
			retScene = ESCAPE_POD_KEY
		
		return retScene, self.ThePlayer
		pass
		
		
class EscapePod(Scene):
	
	def enter(self, thePlayer):
		retScene = DEATH_KEY
		self.ThePlayer = thePlayer
		
		Clear_screen()
		print "This is the Escape Pod Bay. You must guess the correct escape pod in order to leave."
		
		escapeNum = '5' # TODO: implemnent random number
		answer = raw_input("[pod #]> ")
		
		
		
		if ((answer == escapeNum) or (answer == EP_CHEAT)):
			print "\n\nYou picked the correct escape pod and successfully removed yourself from a sticky situation. Good job!"
			
			retScene = FINISH_RESULT
		
		return retScene, self.ThePlayer
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
		
		
	def next_scene(self, sceneName, thePlayer):
		# run the next scene and save off the result
		retScene = ''
		theNextScene = self.sceneDict.get(sceneName)
		
		if (DEBUG_MODE):
			print "\n\n\nsceneName = "
			print sceneName
			print "\n\n"
		
		if (not theNextScene):
			# should never get here
			print "ERROR: Map::next_scene() - invalid key %s" % (sceneName)
		else:
			retScene, thePlayer = theNextScene.enter(thePlayer) #DEBUG_JW - add player here
		
		return retScene, thePlayer
		
		
	def opening_scene(self, thePlayer):
		thePlayer.xp = 99
		print "DEBUG_JW: Map::opening_scene() - thePlayer.xp = %d" % thePlayer.xp
		return self.next_scene(self.firstScene, thePlayer)
			

if __name__ == '__main__':	
		# Start here when this file is being run directly (rather than being imported).
		
        # => Start the game
        aMap = Map(CORRIDOR_KEY) # pass in the key for the starting scene
        aGame = Engine(aMap)
        aGame.play()
