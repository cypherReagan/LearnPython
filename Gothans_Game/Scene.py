# This Python file uses the following encoding: utf-8

# DESCRIPTION:
#		Scene implementation for game

from sys import exit
from random import randint
import random
import GameData
import GameState
import GameEngine
import Entity
import Utils

# Runs melee attack scenario of user against enemy.
# Returns:
#	- thePlayer for health evaluation
def run_melee_attack(self, thePlayer):
	
	newXP = 100
	done = False
	anAttack = MeleeAttack()
	
	while (not done):
		answer = raw_input("%s> " % anAttack.get_option_str(thePlayer))
		
		if (answer == GameData.HELP_REQ_CMD_STR):
			anAttack.print_desc()
		else:
			userAttack = anAttack.translate_cmd(answer)
			
			if (userAttack == MeleeAttack.INVALID):
				print GameData.INVALID_ENTRY_RSP
			else:
				gothanAttack = anAttack.get_random_attack()
				print "\nThe Gothan attacks with %s" % anAttack.get_attack_name(gothanAttack)
				
				if (userAttack == gothanAttack):
					# we have a tie
					print "The two attacks cancel each other. Try again. (-5 HEALTH)"
					thePlayer.subtract_health(5)
					newXP -= 10
				else:
					result = anAttack.evaluate(userAttack, gothanAttack)
					
					if (result == userAttack):
						thePlayer.xp = newXP
						print "You defeated the Gothan! (+%d XP)" % newXP
						retVal = True
					else:
						playerHealth = thePlayer.get_health()
						thePlayer.set_health(0)
						print "The Gothan defeated you. (-%d HEALTH)" % playerHealth
														
					done = True
	
	thePlayer.print_stats()
	
	return thePlayer
	
	
# Runs scenario of user entering keycode.
# Returns:
#	- True if user passes, else False
#	- thePlayer for updated XP state
def run_keyPad(cheatCode, retryMax, thePlayer):
	retVal = False
	
	keyCode = randint(1, 9)
	print "DEBUG_JW: keyCode = %d" % keyCode
	print "DEBUG_JW: retryMax = %d" % retryMax
	
	newXP = 100
	tryCount = 0
	done = False
	 
	while (not done):
		answer = raw_input("[Code]> ")
		
		if (answer == GameData.OVERRIDE_CMD_STR):
		
			retVal, thePlayer = run_keypad_override(thePlayer)
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
	print GameData.OverrideDiagram2Wire
	print GameData.OverrideDiagram2Wire_Seed % (keypadWire, doorWire)
	
	batteryItem = thePlayer.theInventoryMgr.get_item(GameData.ITEM_BATTERY_STR)
	
	if (batteryItem == None):
		print GameData.NVALID_OVERRIDE_EQUIP_RSP
	else:
		Utils.Clear_Screen()
		print GameData.OverrideDiagram3Wire
		print GameData.OverrideDiagram3Wire_Seed % (keypadWire, doorWire, batteryWire) 
	
		print "\n\nChoose the wires to cross.\n"
		done = False

		# get user input for crossing wires
		while (not done):

			wireStr1 = raw_input("\tWire 1 %s> " % Override.OVERRIDE_OPTION_STR)
			wireStr1 = anOverride.translate_cmd(wireStr1)
			
			if (wireStr1 == GameData.INVALID_ENTRY_RSP):
				print GameData.INVALID_ENTRY_RSP
			else:
				wireStr2 = raw_input("\n\tWire 2 %s> " % Override.OVERRIDE_OPTION_STR)
				wireStr2 = anOverride.translate_cmd(wireStr2)
				
				if (wireStr2 == GameData.INVALID_ENTRY_RSP):
					print GameData.INVALID_ENTRY_RSP
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

		batteryItem.subtract_count(1)
		thePlayer.theInventoryMgr.update_item(batteryItem)
		
	return retVal, thePlayer

#---------------------------------------------------
#---------------------------------------------------
# Class: MeleeAttack
#
# DESCRIPTION:
# 	This is a static class used to handle attack data.
#
# TODO: move this to gameAI
#---------------------------------------------------
#---------------------------------------------------
class MeleeAttack:

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
		
		if (thePlayer.theInventoryMgr.get_item(GameData.ITEM_SLEDGEHAMMER_STR) != None):
			retStr += "1. %s\n" % GameData.ITEM_SLEDGEHAMMER_STR
			
		if (thePlayer.theInventoryMgr.get_item(GameData.ITEM_NET_STR) != None):
			retStr += "\t2. %s\n" % GameData.ITEM_NET_STR
			
		if (thePlayer.theInventoryMgr.get_item(GameData.ITEM_KNIFE_STR) != None):
			retStr += "\t3. %s\n\n" % GameData.ITEM_KNIFE_STR
		
		return retStr
	
	def is_valid(self, inputAttack):
		retVal = False
		
		if ((inputAttack == self.SLEDGEHAMMER_NUM) or (inputAttack == self.NET_NUM) or (inputAttack == self.KNIFE_NUM)):
			retVal = True
			
		return retVal
		
	def translate_cmd(self, attackCmd):
		retAttack = MeleeAttack.INVALID
		
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
		print "%s\n%s\n%s" % (GameData.SEPARATOR_LINE_STR, desc, GameData.SEPARATOR_LINE_STR)
		
	# Gets the attack name string based on number.
	# Returns empty string on invalid attackNum.
	def get_attack_name(self, attackNum):
		retStr = ""
		
		if (attackNum == self.SLEDGEHAMMER_NUM):
			retStr = GameData.ITEM_SLEDGEHAMMER_STR
		elif (attackNum == self.NET_NUM):
			retStr = GameData.ITEM_NET_STR
		elif (attackNum == self.KNIFE_NUM):
			retStr = GameData.ITEM_KNIFE_STR
		
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
			GameData.ITEM_BATTERY_STR: ''
		}
	
	def __init__(self):
		
		self.set_wires()
		
	def set_wires(self):
		# randomize wire selection
		wireColorList = ['red', 'green', 'yellow']
		random.shuffle(wireColorList)
		
		self.wireDict['keypad'] = wireColorList[self.KEYPAD_ID]
		self.wireDict['door'] = wireColorList[self.DOOR_ID]
		self.wireDict[GameData.ITEM_BATTERY_STR] = wireColorList[self.BATTERY_ID]
		
	
	# Determines successful override given 2 input wires. 
	# Success = cross 'door' with 'battery'.
	# Returns TRUE if override succeeds, else FALSE
	def evaluate(self, wireStr1, wireStr2):
	
		retVal = False
		
		print "DEBUG_JW: door wire = %s" % self.wireDict['door']
		print "DEBUG_JW: battery wire = %s" % self.wireDict[GameData.ITEM_BATTERY_STR]
		
		cond1 = ((wireStr1 == self.wireDict['door']) and (wireStr2 == self.wireDict[GameData.ITEM_BATTERY_STR]))
		cond2 = ((wireStr1 == self.wireDict[GameData.ITEM_BATTERY_STR]) and (wireStr2 == self.wireDict['door']))
		
		if ((cond1) or (cond2)):
			retVal = True
		
		return retVal
		
	# Returns the wire color of each override element	
	def get_wire_color(self):
		
		keyPadStr = self.wireDict['keypad']
		doorStr = self.wireDict['door']
		batteryStr = self.wireDict[GameData.ITEM_BATTERY_STR]
		
		return keyPadStr, doorStr, batteryStr
		
		
	# Verify that the wire menu input is valid and convert them if necessary.
	# Returns converted wire string if valid, else GameData.INVALID_ENTRY_RSP.
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
			retStr = GameData.INVALID_ENTRY_RSP
		
		return retStr

#---------------------------------------------------
#---------------------------------------------------
# Class: SceneMap
#
# Member Variables:	
#		sceneDict		- dictionary of all game scenes
#		firstScene		- key indicating starting scene
#---------------------------------------------------
#---------------------------------------------------
		
class SceneMap(object):
	
	def __init__(self, startScene):
	
		# declare dict for all scenes
		self.__sceneDict = {	GameData.CORRIDOR_KEY	: CentralCorridor(),
								GameData.ARMORY_KEY 	: Armory(),
								GameData.BRIDGE_KEY		: Bridge(),
								GameData.ESCAPE_POD_KEY	: EscapePod(),
								GameData.DEATH_KEY		: Death()	}
								
		self.firstScene = startScene
		
		
	def next_scene(self, sceneName, thePlayer):
		# run the next scene and save off the result
		retScene = ''
		theNextScene = self.__sceneDict.get(sceneName)
		
		if (not theNextScene):
			# should never get here
			Utils.Show_Game_Error("Map::next_scene() - invalid key %s" % (sceneName))
		else:
			retScene, thePlayer = theNextScene.enter(thePlayer)
		
		return retScene, thePlayer
		
		
	def opening_scene(self, thePlayer):
		return self.next_scene(self.firstScene, thePlayer)


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
		Utils.Show_Game_Error("Scene Subclasses handle implentation.")
		exit(1)
		
		
		
class Death(Scene):
	
	def enter(self, thePlayer):
		retScene = GameData.FINISH_RESULT_KEY
		self.ThePlayer = thePlayer
		
		Utils.Clear_Screen()
		print GameData.ART_STR_SKULL
		print "You died in a really horrifying way!"

		print "Do you want to play again (y/n)?"
		answer = raw_input("> ")
		
		if (answer.lower() == 'y'):
			# TODO: implement way to save score before resetting
			thePlayer.reset_data()
			retScene = GameData.CORRIDOR_KEY
		
		return retScene, thePlayer
		

class CentralCorridor(Scene):
	
	sceneMsgStr = "%s\n%s\nLocation: Central Corridor\n%s\n%s\n\nA Gothan stands before you. You must defeat him with an attack before proceeding.\n" % (GameData.SEPARATOR_LINE_STR, GameData.SEPARATOR_LINE_STR, GameData.SEPARATOR_LINE_STR, GameData.SEPARATOR_LINE_STR)
	
	def enter(self, thePlayer):
		retScene = GameData.DEATH_KEY
		self.ThePlayer = thePlayer
		
		Utils.Clear_Screen()
		print self.sceneMsgStr
		
		done = False
		
		while (not done):
			answer, thePlayer = Utils.Prompt_User_Action(thePlayer)
			
			if ((answer == GameData.CC_CHEAT_CMD_STR) or (answer == GameData.ATTACK_CMD_STR)):
				done = True
			else:
				print GameData.INVALID_ENTRY_RSP
		
		if (answer == GameData.CC_CHEAT_CMD_STR):
			retScene = GameData.ARMORY_KEY
		else:
			if (answer == GameData.ATTACK_CMD_STR):
				thePlayer = run_melee_attack(thePlayer)
				
				if (thePlayer.get_health() > 0):
					retScene = GameData.ARMORY_KEY
				
			else:
				# user chose not to attack => Death
				print "The Gothan proceeds to dismember you."
		
		if (retScene == GameData.ARMORY_KEY):
			
			# TODO - allow player to search (maybe include randomly generated item)
			print "Moving to the Armory...\n"
			
			
		raw_input(GameData.PROMPT_CONTINUE_STR)	
		
		return retScene, thePlayer
		
	
		
		
class Armory(Scene):
	
	sceneMsgStr = "\nLocation: Laser Weapon Armory.\nThis is where you get the neutron bomb that must be placed on the bridge to blow up the ship.\n You must guess the keypad code to obtain the bomb.\n"
	
	def enter(self, thePlayer):
		retScene = GameData.DEATH_KEY
		self.ThePlayer = thePlayer
		
		Utils.Clear_Screen()
		print self.sceneMsgStr
		
		answer = ""
		done = False
		
		while (not done):
		
			answer, thePlayer = Utils.Prompt_User_Action(thePlayer)
			
			if ((answer == GameData.ARMORY_CHEAT_CMD_STR) or (answer == GameData.KEYPAD_CMD_STR)):
				done = True
			else:
				print GameData.INVALID_ENTRY_RSP
			
		
		if (answer == GameData.ARMORY_CHEAT_CMD_STR):
			retScene = GameData.BRIDGE_KEY
		else:
			if (answer == GameData.KEYPAD_CMD_STR):

				isWin, thePlayer = run_keyPad(GameData.ARMORY_CHEAT_CMD_STR, 4, thePlayer)
				
				if (isWin):
					retScene = GameData.BRIDGE_KEY
				else:
					# Failed door code entry scenario
					print "A Gothan hears the alarms and moves in to attack!"
					
					answer, thePlayer = Utils.Prompt_User_Action(thePlayer)
		
					if (answer == GameData.ARMORY_CHEAT_CMD_STR):
						retScene = GameData.BRIDGE_KEY
					else:
						if (answer == GameData.ATTACK_CMD_STR):
							isWin = run_melee_attack(thePlayer)
							
							#DEBUG_JW - remove 'or not isWin' which is only for testing
							if (thePlayer.get_health() > 0):
								isWin = True
							
							#DEBUG_JW- remove this after testing...
							if ( not isWin):
								isWin = True	
								print "DEBUG_JW: Forcing user to recover lost melee attack"
								
							if (isWin):
								print "You defeated the Gothan but the door is still locked."
								
								done = False
								
								while (not done):
									answer, thePlayer = Utils.Prompt_User_Action(thePlayer)

									if (answer == GameData.ARMORY_CHEAT_CMD_STR):
										retScene = GameData.BRIDGE_KEY
									else:
										if (answer == GameData.OVERRIDE_CMD_STR):
											isWin, thePlayer = run_keypad_override(thePlayer)
											
											if (isWin):
												retScene = GameData.BRIDGE_KEY
												done = True
											
										elif (answer == GameData.SEARCH_CMD_STR):
											print "You search the Gothans dead body and find a battery pack!"
											
											thePlayer.theInventoryMgr.add_item(Entity.UtilityItem(GameData.ITEM_BATTERY_STR, 1))
										else:
											print GameData.INVALID_ENTRY_RSP
								
						else:
							# user chose not to attack => Death
							print "The Gothan proceeds to dismember you."
			
			else:
				# no keypad command. We should never get here
				Utils.Show_Game_Error("Invalid command.")
				
		if (retScene == GameData.BRIDGE_KEY):
			thePlayer.theInventoryMgr.add_item(Entity.UtilityItem(GameData.ITEM_BOMB_STR, 1))
			
			# TODO - allow user to pick up bomb and other weapons
			
			print "Moving to the Bridge...\n"
			
		
		raw_input(GameData.PROMPT_CONTINUE_STR)	
		
		return retScene, thePlayer
		
		
class Bridge(Scene):
	
	sceneMsgStr = "Location: Bridge.\nA Gothan stands in your way.\nYou must defeat him in order to set the bomb and attempt to escape.\n"
	
	def enter(self, thePlayer):
		retScene = GameData.DEATH_KEY
		self.ThePlayer = thePlayer
		
		Utils.Clear_Screen()
		print self.sceneMsgStr
		
		isMelee = False
		
		if (isMelee):
		
			print "A Gothan is blocking you from planting the bomb."
			
			answer, thePlayer = Utils.Prompt_User_Action(thePlayer)
			
			if (answer == GameData.BRIDGE_CHEAT_CMD_STR):
				retScene = GameData.ESCAPE_POD_KEY
			else:
				if (answer == GameData.ATTACK_CMD_STR):
					thePlayer = run_melee_attack(thePlayer)
					
					if (thePlayer.get_health() > 0):
						retScene = GameData.ESCAPE_POD_KEY
				else:
					# user chose not to attack
					print "The Gothan liquifies you with his plasma rifle"
			
		else:
			# TODO: implement map scenario
			
			# Use game loop to send map manipulation requests.
			# The map will return 
			
			#DEBUG_JW - start debug
			if (0):
				#print u'\u0420\u043e\u0441\u0441\u0438\u044f'
				
				#tmpStrU = u"➕☻↑↓→✊☠☃"
				tmpStrU = u"░▓▐▄"
				print tmpStrU
				
				#aMapDisplay = MapDisplay.MapDisplayData(GameData.MAP_BRIDGE_STR1_UCODE)
				#mapStr = u"%s" % aMapDisplay.get_map()
				#print mapStr
				
				aMapEngine = GameEngine.MapEngine(GameData.MAP_BRIDGE_STR1_UCODE)
				thePlayer = aMapEngine.run_map(thePlayer)
			
				#Utils.Show_Game_Error("DEBUG_JW - This is just a TEST!!!!\n\n%s" % mapStr)
				Utils.Show_Game_Error("DEBUG_JW - This is just a unicode string TEST!!!!\n\n")
			# end debug
			
			GameState.Set_Player(thePlayer)
			
			mapStrList = [GameData.MAP_CC_STR1_UCODE]
			
			aMapEngine = GameEngine.MapEngine("Bridge", mapStrList)
			aMapEngine.execute()
			
			retScene = GameData.ESCAPE_POD_KEY
			
		if (retScene == GameData.ESCAPE_POD_KEY):
			print "Moving to the Escape Pod Bay...\n"
			
			
		raw_input(GameData.PROMPT_CONTINUE_STR)	
		
		return retScene, thePlayer
		pass
		
		
class EscapePod(Scene):
	
	sceneMsgStr = "Location: Escape Pod Bay.\nYou must guess the correct escape pod in order to leave.\n"
	
	def enter(self, thePlayer):
		retScene = GameData.DEATH_KEY
		self.ThePlayer = thePlayer
		
		Utils.Clear_Screen()
		print self.sceneMsgStr
		
		escapeNumStr = '5' # TODO: implemnent random number
		answer = raw_input("[pod #]> ")
		
		
		
		if ((answer == escapeNumStr) or (answer == GameData.EP_CHEAT_CMD_STR)):
			print "\n\nYou picked the correct escape pod and successfully removed yourself from a sticky situation. Good job!"
			
			retScene = GameData.FINISH_RESULT_KEY
		
		return retScene, thePlayer
		pass
		
		
