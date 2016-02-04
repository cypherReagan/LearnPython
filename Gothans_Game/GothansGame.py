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

#---------------------------- Globals ----------------------------

# Map Keys
CORRIDOR_KEY = 'central corridor'
ARMORY_KEY = 'armory'
BRIDGE_KEY = 'bridge'
ESCAPE_POD_KEY = 'escape pod'
DEATH_KEY = 'death'
FINISH_RESULT = 'done'

INVALID_ENTRY_RSP = 'DOES NOT COMPUTE!'
PROMPT_CONTINUE_STR = "[Press any key to continue...]> "
INVALID_OVERRIDE_EQUIP_RSP = "You do not have the necessary equipment for an override."

INFINITE_VAL = -1000
INVALID_INDEX = -1

# User Action Commands
HELP_REQ_CMD_STR = '?'
QUIT_CMD_STR = 'quit'
ATTACK_CMD_STR = 'attack'
KEYPAD_CMD_STR = 'keypad'
OVERRIDE_CMD_STR = 'hack'
SEARCH_CMD_STR = 'search'
PLAYER_STATS_CMD_STR = 'stats'
PLAYER_INV_CMD_STR = 'inv'

CHEAT_CMD_STR = '-f'
CC_CHEAT_CMD_STR = CHEAT_CMD_STR + ' cc'
ARMORY_CHEAT_CMD_STR = CHEAT_CMD_STR + ' armory'
BRIDGE_CHEAT_CMD_STR = CHEAT_CMD_STR + ' bridge'
EP_CHEAT_CMD_STR = CHEAT_CMD_STR + ' ep'
DEBUG_MODE_TOGGLE_CMD_STR = CHEAT_CMD_STR + ' dbg'
#TODO - add cheat cmds to restore player health, add weapons, ect...
# Also, player xp goes to 0 when you cheat
				
#TODO - make this a list of tuples (str, number) to allow menu referencing				
CMD_STR_LIST = [HELP_REQ_CMD_STR,
				QUIT_CMD_STR,
				ATTACK_CMD_STR,
				KEYPAD_CMD_STR,
				OVERRIDE_CMD_STR,
				SEARCH_CMD_STR,
				PLAYER_STATS_CMD_STR,
				PLAYER_INV_CMD_STR,
				
				CC_CHEAT_CMD_STR,
				ARMORY_CHEAT_CMD_STR,
				BRIDGE_CHEAT_CMD_STR,
				EP_CHEAT_CMD_STR,
				
				DEBUG_MODE_TOGGLE_CMD_STR]

# Item Strings
ITEM_BATTERY_STR = 'battery'
ITEM_BOMB_STR = 'bomb'
ITEM_SLEDGEHAMMER_STR = 'sledgehammer'
ITEM_NET_STR = 'net'
ITEM_KNIFE_STR = 'knife'
#-------------------------- End Globals --------------------------

# Utility function to clear shell
def Clear_Screen():
		
	if (not DEBUG_MODE):
		if (platform.system() == 'Windows'):
			os.system('cls')
		else:
			os.system('clear') # Linux/Mac OS
			
			
# Utility function to ask user for game command
def Prompt_User_Action(thePlayer = None):
	answer = ''
	done = False
	
	while (not done):
		answer = raw_input("[Action]> ")
		answer = answer.lower()
		
		if answer in CMD_STR_LIST:
			if (not Process_Common_Actions(answer, thePlayer)):
				done = True
		else:
			print INVALID_ENTRY_RSP
				
	return answer

# Process any common user commands.
# Returns True if command is handled, else False
def Process_Common_Actions(userCmdStr, thePlayer = None):

	retVal = True
	
	if (userCmdStr == HELP_REQ_CMD_STR):
		
		print AsciiArt.Separator_Line
		print "GAME COMMANDS:\n"

		for entry in CMD_STR_LIST:
			if (CHEAT_CMD_STR not in entry):
				print entry
		
		print AsciiArt.Separator_Line
	
	elif (userCmdStr == QUIT_CMD_STR):
		print "Are you sure want to quit?"
		answer = raw_input("(y/n)> ")
		
		if (answer.lower() == 'y'):
			Exit_Game(thePlayer)
	
	elif (userCmdStr == PLAYER_STATS_CMD_STR):
		thePlayer.print_stats()
		
	elif (userCmdStr == PLAYER_INV_CMD_STR):
		thePlayer.theInventoryMgr.print_items()
		
	elif (userCmdStr == DEBUG_MODE_TOGGLE_CMD_STR):
		global DEBUG_MODE
		
		if (not DEBUG_MODE):
			DEBUG_MODE = True
			print "DEBUG_MODE = True"
		else:
			DEBUG_MODE = False
			print "DEBUG_MODE = False"

	else:
		retVal = False

		
	return retVal
	
def Exit_Game(thePlayer):
	Clear_Screen()
	print "%s\nFINAL SCORE: %d\n\n%s\n%s" % (AsciiArt.Separator_Line, thePlayer.xp, AsciiArt.GameOverMsg, AsciiArt.Separator_Line)
	exit(1)
	
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
	SLEDGEHAMMER_NUM = 1
	NET_NUM = 2
	KNIFE_NUM = 3
	
	MAX_ATTACK_NUM = 3

	
	ATTACK_OPTION_STR = """
	Attack Options:\n\n
	"""
	
	def get_option_str(self, thePlayer):
	
		retStr = self.ATTACK_OPTION_STR
		
		if (thePlayer.theInventoryMgr.get_item(ITEM_SLEDGEHAMMER_STR) != None):
			retStr += "1. %s\n" % ITEM_SLEDGEHAMMER_STR
			
		if (thePlayer.theInventoryMgr.get_item(ITEM_NET_STR) != None):
			retStr += "\t2. %s\n" % ITEM_NET_STR
			
		if (thePlayer.theInventoryMgr.get_item(ITEM_KNIFE_STR) != None):
			retStr += "\t3. %s\n\n" % ITEM_KNIFE_STR
		
		return retStr
	
	def is_valid(self, inputAttack):
		retVal = False
		
		if ((inputAttack == self.SLEDGEHAMMER_NUM) or (inputAttack == self.NET_NUM) or (inputAttack == self.KNIFE_NUM)):
			retVal = True
			
		return retVal
		
	def translate_cmd(self, attackCmd):
		retAttack = Attack.INVALID
		
		if (attackCmd == str(self.SLEDGEHAMMER_NUM)):
			retAttack = self.SLEDGEHAMMER_NUM
		elif (attackCmd == str(self.NET_NUM)):
			retAttack = self.NET_NUM
		elif (attackCmd == str(self.KNIFE_NUM)):
			retAttack = self.KNIFE_NUM
			
		return retAttack
		
	def get_random_attack(self):
		return randint(1, self.MAX_ATTACK_NUM)
	
	def print_desc(self):
		desc = """
		Melee Attack Info:
		
		Sledgehammer (s) - beats knife, loses to net\n
		Net (n) - beats sledgehammer, loses to knife\n
		Knife (k) - beats net, loses to sledgehammer\n
		"""
		print "%s\n%s\n%s" % (AsciiArt.Separator_Line, desc, AsciiArt.Separator_Line)
		
	# Gets the attack name string based on number.
	# Returns empty string on invalid attackNum.
	def get_attack_name(self, attackNum):
		retStr = ""
		
		if (attackNum == self.SLEDGEHAMMER_NUM):
			retStr = ITEM_SLEDGEHAMMER_STR
		elif (attackNum == self.NET_NUM):
			retStr = ITEM_NET_STR
		elif (attackNum == self.KNIFE_NUM):
			retStr = ITEM_KNIFE_STR
		
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
			if (attack1 == self.SLEDGEHAMMER_NUM):
				if (attack2 == self.NET_NUM):
					retVal = attack2
				else:
					retVal = attack1
					
			if (attack1 == self.NET_NUM):
				if (attack2 == self.KNIFE_NUM):
					retVal = attack2
				else:
					retVal = attack1
					
			if (attack1 == self.KNIFE_NUM):
				if (attack2 == self.SLEDGEHAMMER_NUM):
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
	
	# TODO - determine why these cannot go in init()
	wireDict = {
			'keypad': '',
			'door': '',
			ITEM_BATTERY_STR: ''
		}
	
	def __init__(self):
		
		self.set_wires()
		
	def set_wires(self):
		# randomize wire selection
		wireColorList = ['red', 'green', 'yellow']
		random.shuffle(wireColorList)
		
		self.wireDict['keypad'] = wireColorList[self.KEYPAD_ID]
		self.wireDict['door'] = wireColorList[self.DOOR_ID]
		self.wireDict[ITEM_BATTERY_STR] = wireColorList[self.BATTERY_ID]
		
	
	# Determines successful override given 2 input wires. 
	# Success = cross 'door' with 'battery'.
	# Returns TRUE if override succeeds, else FALSE
	def evaluate(self, wireStr1, wireStr2):
	
		retVal = False
		
		print "DEBUG_JW: door wire = %s" % self.wireDict['door']
		print "DEBUG_JW: battery wire = %s" % self.wireDict[ITEM_BATTERY_STR]
		
		cond1 = ((wireStr1 == self.wireDict['door']) and (wireStr2 == self.wireDict[ITEM_BATTERY_STR]))
		cond2 = ((wireStr1 == self.wireDict[ITEM_BATTERY_STR]) and (wireStr2 == self.wireDict['door']))
		
		if ((cond1) or (cond2)):
			retVal = True
		
		return retVal
		
	# Returns the wire color of each override element	
	def get_wire_color(self):
		
		keyPadStr = self.wireDict['keypad']
		doorStr = self.wireDict['door']
		batteryStr = self.wireDict[ITEM_BATTERY_STR]
		
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
		
		# start with default melee weapons
		self.theInventoryMgr.add_item(WeaponItem(ITEM_SLEDGEHAMMER_STR, INFINITE_VAL))
		self.theInventoryMgr.add_item(WeaponItem(ITEM_NET_STR, INFINITE_VAL))
		self.theInventoryMgr.add_item(WeaponItem(ITEM_KNIFE_STR, INFINITE_VAL))
		
	def print_stats(self):
		print "%s\n\nPLAYER STATS:\n\nHEALTH = %d\nXP = %d\n\n%s" % (AsciiArt.Separator_Line, self.health, self.xp, AsciiArt.Separator_Line)
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: InventoryMgr
#
# NOTES:
#	Sequence of using item:	
#	-> InventoryMgr::get_item()
#	-> (operate on it)
#	-> InventoryMgr::updateItem()
#
# Member Variables:	
#		itemList - list of all inventory items
#--------------------------------------------------
#---------------------------------------------------		
class InventoryMgr(object):
	
	# TODO - determine why these cannot go in init()
	utilItemDict = {} #DEBUG_JW - might not need this
	itemList = []
		
	INVALID_TYPE_ID_STR = "ERROR: Invalid Item Type ID"
		
	def add_item(self, newItem):
		
		#if (newItem.typeID == Item.TYPE_ID_UTILITY):
		#	# append to list
		#	self.utilItemDict[newItem.name] = newItem
		#	self.itemList.append(newItem) 
		#	print "DEBUG_JW - Adding %s to Inventory..." % newItem.name
		#else:
		#	print "ERROR: Feature not implemented yet!"
		
		
		itemIndex = self.get_item_index(newItem.name)
		
		if ((itemIndex >= 0) and (itemIndex < len(self.itemList))):
			# item already exists in list => update existing item counts
			theItem = self.itemList[itemIndex]
			
			if (theItem.typeID == Item.TYPE_ID_UTILITY):
				theItem.count += 1
			elif (theItem.typeID == Item.TYPE_ID_WEAPON):
				theItem.ammo += newItem.ammo
			else:
				# should never get here
				print INVALID_TYPE_ID_STR
		else:
			# brand new item to add
			
			# Determine collection index for fast referencing
			listIndex = len (self.itemList) - 1
			newItem.index = listIndex
			
			self.itemList.append(newItem) 
			print "Adding %s to Inventory..." % newItem.name
		
		
	def is_item_index_valid(self, theItem):
		retIndex = INVALID_INDEX
		itemIndex = theItem.index
		
		if ((itemIndex < len(self.itemList) and (theItem.name == self.itemList[itemIndex].name))):
			retIndex = itemIndex
			
		return retIndex
	
	
	def update_item(self, updatedItem):
	
		# first try fast indexing
		itemIndex = self.is_item_index_valid(updatedItem)
		
		isUpdate = False
		
		if (itemIndex != INVALID_INDEX):
			isUpdate = True
		else:
			# something is wrong with the item's assigned index => search list for item
			itemIndex = self.get_item_index(updatedItem.name)
			
			if (itemIndex != INVALID_INDEX):
				isUpdate = True
			else:
				print "ERROR: Unable to update inventory item - %s" % updatedItem.name
		
		if (isUpdate):
			# item found in list
			if (not updatedItem.is_usable()):
				# we have a depleted item => get rid of it
				isUpdate = False
				self.delete_item(updatedItem)
				
			if (isUpdate):
				self.itemList[itemIndex] = updatedItem
		
		
	def get_item(self, itemName):
		retItem = None
		
		itemIndex = self.get_item_index(itemName)
		
		if (itemIndex != INVALID_INDEX):
			tmpItem = self.itemList[itemIndex]
			
			if (tmpItem.name == itemName):
				retItem = tmpItem
			else:
				# Something went wrong. We got a mismatching item from query.
				print "ERROR: get_item fail for %s" % itemName
				print "DEBUG_JW: itemName = %s. itemIndex = %d. result name = %s\n" % (itemName, itemIndex, tmpItem.name)
		
		return retItem
		
		
	# Returns item index if found in list, else INVALID_INDEX
	def get_item_index(self, itemName):
		
		retIndex = INVALID_INDEX
		count = 0
		
		for item in self.itemList:
			if (item.name == itemName):
				retIndex = count
			
			count += 1
				
		return retIndex
	
	
	def delete_item(self, theItem):
		itemIndex = self.is_item_index_valid(theItem)
		
		if (itemIndex != INVALID_INDEX):
			# we have a valid item
				
			self.itemList.remove(itemIndex)
			# After any deletion (potentially in the middle of list), 
			# need to recalculate each item index to stay accurate.
			self.calculate_item_indices()
		else:
			print "ERROR: Unable to delete inventory item - %s" % theItem.name
		
		
	def calculate_item_indices(self):
		
		for count in range(0, len (self.itemList)):
			self.itemList[count].index = count
		
	
	def print_items(self):
		
		print "%s\nINVENTORY:\n\n" % AsciiArt.Separator_Line
		
		dictCount = len (self.utilItemDict)
		
		#for key, val in self.utilItemDict.items():
		#	print "%s. %s" % (key, val.count)
		
		#for count in range(0, dictCount):
		#	print self.utilItemDict[count].name
		
		itemNum = 1 # start label counting here (even though index starts at 0)
		
		for invItem in self.itemList:
			countNameStr = ""
			invCountStr = ""
			
			if (invItem.typeID == Item.TYPE_ID_UTILITY):
				countNameStr = "Count: "
				invCountStr = invItem.count
				
			elif (invItem.typeID == Item.TYPE_ID_WEAPON):
				if (invItem.ammo != INFINITE_VAL):
					invCountStr = invItem.ammo
					countNameStr = "Ammo: "
					
			else:
				# should never get here
				print INVALID_TYPE_ID_STR
				
				
			print "%d. %s\t\t%s %s" % (itemNum, invItem.name, countNameStr, invCountStr)
			itemNum += 1
		
		print "\n\n%s" % AsciiArt.Separator_Line
		
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: Item
#--------------------------------------------------
#---------------------------------------------------		
class Item(object):

	# Item type IDs
	TYPE_ID_UTILITY = 0
	TYPE_ID_WEAPON = 1
	
	# default common members to invalid values
	name = ""
	typeID = INVALID_INDEX
	index = INVALID_INDEX #dEBUG_JW - not sure if this is needed

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
	
	# default unique members to invalid values
	count = INVALID_INDEX
	
	def __init__(self, newName, newCount):
		self.name = newName
		self.count = newCount
		self.typeID = self.TYPE_ID_UTILITY
		
	
	def is_usable(self):
	
		retVal = False
		
		if (self.count > 0):
			retVal = True
			
		return retVal
		
#---------------------------------------------------
#---------------------------------------------------
# Class: WeaponItem
#--------------------------------------------------
#---------------------------------------------------		
class WeaponItem(Item):

	# default unique members to invalid values
	ammo = -1
	
	def __init__(self, newName, newAmmo):
		self.name = newName
		self.ammo = newAmmo
		self.typeID = self.TYPE_ID_WEAPON
		
		
	def is_usable(self):
	
		retVal = False
		
		if ((self.ammo > 0) or (self.ammo == INFINITE_VAL)):
			retVal = True
			
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
		
	def play(self):
		Clear_Screen()
		# Show Title Screen with menu options
		print "%s\n%s\n%s\n" % (AsciiArt.Separator_Line, AsciiArt.GothansGameTitle, AsciiArt.Separator_Line)
		
		# TODO - possibly store all game msgs in separate file
		startMenuStr = """
			1. Start Game
			2. Help
			3. Quit
		"""
		
		#TODO - update this with more game details
		helpStr = """
			 Use the '?' in action prompts for hints on how to proceed.
		""" 
		
		openingMsgStr =  """
			Gothans have invaded your spaceship and killed everyone else on board. 
			Time to blow this baby and escape to the planet below!\n\n
		"""
		
		done = False
		
		while (not done):
			answer = raw_input("%s\n\t\t> " % startMenuStr)
			
			if (answer == '1'):
				# Start Game
				Clear_Screen()
				print openingMsgStr
				raw_input("\t\t\t%s" % PROMPT_CONTINUE_STR)
				Clear_Screen()
				done = True
			elif (answer == '2'):
				# Show Help
				Clear_Screen()
				print helpStr
				raw_input(PROMPT_CONTINUE_STR)
				Clear_Screen()
			elif (answer == '3'):
				# Quit
				Clear_Screen()
				exit(1)
			else:
				print INVALID_ENTRY_RSP
				Clear_Screen()

		# Each scene returns the player to maintain game state.
		thePlayer = Player()
		
		# need while-loop here to drive game
		result, thePlayer = self.sceneMap.opening_scene(thePlayer)
		
		while (result != FINISH_RESULT):
			result, thePlayer = self.sceneMap.next_scene(result, thePlayer)
			
			
		Exit_Game(thePlayer)	


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
	#	- thePlayer for health evaluation
	def run_attack(self, thePlayer):
		
		newXP = 100
		done = False
		anAttack = Attack()
		
		while (not done):
			answer = raw_input("%s> " % anAttack.get_option_str(thePlayer))
			
			if (answer == HELP_REQ_CMD_STR):
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
						print "The two attacks cancel each other. Try again. (-5 HEALTH)"
						thePlayer.health -= 5
						newXP -= 10
					else:
						result = anAttack.evaluate(userAttack, gothanAttack)
						
						if (result == userAttack):
							thePlayer.xp = newXP
							print "You defeated the Gothan! (+%d XP)" % newXP
							retVal = True
						else:
							thePlayer.health = 0
							healthDiff = 100 - thePlayer.health
							print "The Gothan defeated you. (-%d HEALTH)" % healthDiff
															
						done = True
		
		thePlayer.print_stats()
		
		return thePlayer
		
		
	# Runs scenario of user entering keycode.
	# Returns:
	#	- True if user passes, else False
	#	- thePlayer for updated XP state
	def run_keyPad(self, cheatCode, retryMax, thePlayer):
		retVal = False
		
		keyCode = randint(1, 9)
		print "DEBUG_JW: keyCode = %d" % keyCode
		print "DEBUG_JW: retryMax = %d" % retryMax
		
		newXP = 100
		tryCount = 0
		done = False
		 
		while (not done):
			answer = raw_input("[Code]> ")
			
			if (answer == OVERRIDE_CMD_STR):
			
				retVal, thePlayer = self.run_keypad_override(thePlayer)
				done = True
				
			else:
                #TODO - check for invalid inputs (i.e. ENTER key)
					
				keyCodeStr = str(keyCode)
			
				if ((answer == keyCodeStr) or (answer.lower() == cheatCode)):
					retVal = True
					done = True
					print "You successfully opened the door!"
					
					# only update XP here when the user sucessfully guesses the code
					if (answer == keyCodeStr):
						thePlayer.xp += newXP
						print "(+%d XP)" % newXP
				else:
					tryCount += 1
					
					if (tryCount > retryMax):
						print """
						You ran out of guesses. The system sounds an alarm and locks you out!\n 
						TODO - move this death elsewhere: A Gothan sneaks up and disembowels you with his super-sharp blade.
						"""
						done = True
					else:
						print "You entered an incorrect code. Please try again."
						newXP -= 10
		
		
		return retVal, thePlayer
	
	
	# Runs scenario of user overriding keypad.
	# Returns:
	#	- True if user passes, else False	
	def run_keypad_override(self, thePlayer):
		retVal = False
		
		anOverride = Override()
		keypadWire, doorWire, batteryWire = anOverride.get_wire_color()
		
		print "You pry off the panel to reveal a series of wires.\n"
		print AsciiArt.OverrideDiagram2Wire
		print AsciiArt.OverrideDiagram2Wire_Seed % (keypadWire, doorWire)
		
		batteryItem = thePlayer.theInventoryMgr.get_item(ITEM_BATTERY_STR)
		
		if (batteryItem == None):
			print INVALID_OVERRIDE_EQUIP_RSP
		else:
			Clear_Screen()
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
				thePlayer.xp += 50
				print "You successfully hacked the door! (+50 XP)\n\n"
			else:
				print """
				You failed to open the door and security now countermeasures activate.\n
				Toxic nerve gas releases, causing you to asphyxiate immediately.
				"""

			batteryItem.count -= 1
			thePlayer.theInventoryMgr.update_item(batteryItem)
			
		return retVal, thePlayer
		
		
class Death(Scene):
	
	def enter(self, thePlayer):
		retScene = FINISH_RESULT
		self.ThePlayer = thePlayer
		
		Clear_Screen()
		print AsciiArt.Skull
		print "You died in a really horrifying way!"

		print "Do you want to play again (y/n)?"
		answer = raw_input("> ")
		
		if (answer.lower() == 'y'):
			retScene = CORRIDOR_KEY
		
		return retScene, self.ThePlayer
		

class CentralCorridor(Scene):
	
	sceneMsgStr = "%s\n%s\nLocation: Central Corridor\n%s\n%s\n\nA Gothan stands before you. You must defeat him with an attack before proceeding.\n" % (AsciiArt.Separator_Line, AsciiArt.Separator_Line, AsciiArt.Separator_Line, AsciiArt.Separator_Line)
	
	def enter(self, thePlayer):
		retScene = DEATH_KEY
		self.ThePlayer = thePlayer
		
		Clear_Screen()
		print self.sceneMsgStr
		
		done = False
		
		answer = Prompt_User_Action(thePlayer)
		
		if (answer == CC_CHEAT_CMD_STR):
			retScene = ARMORY_KEY
		else:
			if (answer == ATTACK_CMD_STR):
				thePlayer = self.run_attack(thePlayer)
				
				if (thePlayer.health > 0):
					retScene = ARMORY_KEY
				
			else:
				# user chose not to attack => Death
				print "The Gothan proceeds to dismember you."
		
		if (retScene == ARMORY_KEY):
			
			# TODO - allow player to search (maybe include randomly generated item)
			print "Moving to the Armory..."
			
			
		raw_input(PROMPT_CONTINUE_STR)	
		
		return retScene, thePlayer
		
	
		
		
class Armory(Scene):
	
	sceneMsgStr = "\nLocation: Laser Weapon Armory.\nThis is where you get the neutron bomb that must be placed on the bridge to blow up the ship.\n You must guess the keypad code to obtain the bomb.\n"
	
	def enter(self, thePlayer):
		retScene = DEATH_KEY
		self.ThePlayer = thePlayer
		
		Clear_Screen()
		print self.sceneMsgStr
		
		answer = ""
		done = False
		
		while (not done):
		
			answer = Prompt_User_Action(thePlayer)
			
			if ((answer == ARMORY_CHEAT_CMD_STR) or (answer == KEYPAD_CMD_STR)):
				done = True
			else:
				print INVALID_ENTRY_RSP
			
		
		if (answer == ARMORY_CHEAT_CMD_STR):
			retScene = BRIDGE_KEY
		else:
			if (answer == KEYPAD_CMD_STR):

				isWin, thePlayer = self.run_keyPad(ARMORY_CHEAT_CMD_STR, 4, thePlayer)
				
				if (isWin):
					retScene = BRIDGE_KEY
				else:
					# Failed door code entry scenario
					print "A Gothan hears the alarms and moves in to attack!"
					
					answer = Prompt_User_Action(thePlayer)
		
					if (answer == ARMORY_CHEAT_CMD_STR):
						retScene = BRIDGE_KEY
					else:
						if (answer == ATTACK_CMD_STR):
							isWin = self.run_attack(thePlayer)
							
							#DEBUG_JW - remove 'or not isWin' which is only for testing
							if (thePlayer.health > 0):
								isWin = True
							
							#DEBUG_JW- remove this after testing...
							if ( not isWin):
								isWin = True	
								print "DEBUG_JW: Forcing user to recover lost melee attack"
								
							if (isWin):
								print "You defeated the Gothan but the door is still locked."
								
								done = False
								
								while (not done):
									answer = Prompt_User_Action(thePlayer)

									if (answer == ARMORY_CHEAT_CMD_STR):
										retScene = BRIDGE_KEY
									else:
										if (answer == OVERRIDE_CMD_STR):
											# user chose to override the keypad for the first time
											isWin, thePlayer = self.run_keypad_override(thePlayer)
											
											if (isWin):
												retScene = BRIDGE_KEY
												done = True
											
										elif (answer == SEARCH_CMD_STR):
											print "You search the Gothans dead body and find a battery pack!"
											
											thePlayer.theInventoryMgr.add_item(UtilityItem(ITEM_BATTERY_STR, 1))
										else:
											print INVALID_ENTRY_RSP
								
						else:
							# user chose not to attack => Death
							print "The Gothan proceeds to dismember you."
			
			else:
				# no keypad command. We should never get here
				print "ERROR: Invalid command."
				
		if (retScene == BRIDGE_KEY):
			thePlayer.theInventoryMgr.add_item(UtilityItem(ITEM_BOMB_STR, 1))
			
			# TODO - allow user to pick up bomb and other weapons
			
			print "Moving to the Bridge..."
			
		
		raw_input(PROMPT_CONTINUE_STR)	
		
		return retScene, thePlayer
		
		
class Bridge(Scene):
	
	sceneMsgStr = "Location: Bridge.\nA Gothan stands in your way.\nYou must defeat him in order to set the bomb and attempt to escape.\n"
	
	def enter(self, thePlayer):
		retScene = DEATH_KEY
		self.ThePlayer = thePlayer
		
		Clear_Screen()
		print self.sceneMsgStr
		
		print "A Gothan is blocking you from planting the bomb."
		
		answer = Prompt_User_Action(thePlayer)
		
		if (answer == BRIDGE_CHEAT_CMD_STR):
			retScene = ESCAPE_POD_KEY
		else:
			if (answer == ATTACK_CMD_STR):
				thePlayer = self.run_attack(thePlayer)
				
				if (thePlayer.health > 0):
					retScene = ESCAPE_POD_KEY
			else:
				# user chose not to attack
				print "The Gothan liquifies you with his plasma rifle"
		
		return retScene, thePlayer
		pass
		
		
class EscapePod(Scene):
	
	sceneMsgStr = "Location: Escape Pod Bay.\nYou must guess the correct escape pod in order to leave.\n"
	
	def enter(self, thePlayer):
		retScene = DEATH_KEY
		self.ThePlayer = thePlayer
		
		Clear_Screen()
		print self.sceneMsgStr
		
		escapeNumStr = '5' # TODO: implemnent random number
		answer = raw_input("[pod #]> ")
		
		
		
		if ((answer == escapeNumStr) or (answer == EP_CHEAT_CMD_STR)):
			print "\n\nYou picked the correct escape pod and successfully removed yourself from a sticky situation. Good job!"
			
			retScene = FINISH_RESULT
		
		return retScene, thePlayer
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
			retScene, thePlayer = theNextScene.enter(thePlayer)
		
		return retScene, thePlayer
		
		
	def opening_scene(self, thePlayer):
		return self.next_scene(self.firstScene, thePlayer)
			

			
			
if __name__ == '__main__':	
		# Start here when this file is being run directly (rather than being imported).
		
        # => Start the game
        aMap = Map(CORRIDOR_KEY) # pass in the key for the starting scene
        aGame = Engine(aMap)
        aGame.play()
