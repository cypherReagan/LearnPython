from sys import exit
from random import randint
import random
import os
import GameData
import GameState
import Utils

# Runs melee attack scenario of user against Gothan.
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
	print AsciiArt.OverrideDiagram2Wire
	print AsciiArt.OverrideDiagram2Wire_Seed % (keypadWire, doorWire)
	
	batteryItem = thePlayer.theInventoryMgr.get_item(GameData.ITEM_BATTERY_STR)
	
	if (batteryItem == None):
		print INVALID_OVERRIDE_EQUIP_RSP
	else:
		Utils.Clear_Screen()
		print AsciiArt.OverrideDiagram3Wire
		print AsciiArt.OverrideDiagram3Wire_Seed % (keypadWire, doorWire, batteryWire) 
	
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
		retScene = FINISH_RESULT
		self.ThePlayer = thePlayer
		
		Utils.Clear_Screen()
		print AsciiArt.Skull
		print "You died in a really horrifying way!"

		print "Do you want to play again (y/n)?"
		answer = raw_input("> ")
		
		if (answer.lower() == 'y'):
			# TODO: implement way to save score before resetting
			thePlayer.reset_data()
			retScene = GameData.CORRIDOR_KEY
		
		return retScene, thePlayer
		

class CentralCorridor(Scene):
	
	sceneMsgStr = "%s\n%s\nLocation: Central Corridor\n%s\n%s\n\nA Gothan stands before you. You must defeat him with an attack before proceeding.\n" % (AsciiArt.GameData.SEPARATOR_LINE_STR, AsciiArt.GameData.SEPARATOR_LINE_STR, AsciiArt.GameData.SEPARATOR_LINE_STR, AsciiArt.GameData.SEPARATOR_LINE_STR)
	
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
			if (answer == ATTACK_CMD_STR):
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
											
											thePlayer.theInventoryMgr.add_item(UtilityItem(GameData.ITEM_BATTERY_STR, 1))
										else:
											print GameData.INVALID_ENTRY_RSP
								
						else:
							# user chose not to attack => Death
							print "The Gothan proceeds to dismember you."
			
			else:
				# no keypad command. We should never get here
				Utils.Show_Game_Error("Invalid command.")
				
		if (retScene == GameData.BRIDGE_KEY):
			thePlayer.theInventoryMgr.add_item(UtilityItem(GameData.ITEM_BOMB_STR, 1))
			
			# TODO - allow user to pick up bomb and other weapons
			
			print "Moving to the Bridge...\n"
			
		
		raw_input(PROMPT_CONTINUE_STR)	
		
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
			
			
		raw_input(PROMPT_CONTINUE_STR)	
		
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
			
			retScene = GameData.FINISH_RESULT
		
		return retScene, thePlayer
		pass
		
		