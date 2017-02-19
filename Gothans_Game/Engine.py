# Name				: Engine.py
# Author			: JWalker
# Created			: 17th September 2015
# Version			: 1.0
# Runtime			: Python27
# ASCII Colors		: ANSICON

# Implementation of Gothans Attack

# Concept from Learn Python the Hard Way ex43

import Display
import SharedConst as Const
import GameState
import Utils
import datetime
import Scene
import Entity
import os
import Console
import codecs
import copy

#---------------------------------------------------
#---------------------------------------------------
# Class: MapLog
#
# Purpose:
#		Maintains list of map events for user display.
#
# Member Variables:	
#
#	Private:
#		gameLogStrList	- FIFO queue to store game msg strings
#		logCount		- number of msgs in queue
#---------------------------------------------------
#---------------------------------------------------
class MapLog(object):
	
	def __init__(self):
		
		self.__gameLogStrList = []
		self.clear()
			
	
	def clear(self):
		self.__logCount = 0
		del self.__gameLogStrList[:]
		
		for count in range(0, Const.MAX_GAME_LOG_ENTRIES):
			self.__gameLogStrList.append("")
		
	
	def add(self,  newStr):
		
		listSize = len (self.__gameLogStrList)
		
		# Timestamp each entry
		timeStampStr = '{:%H:%M:%S}'.format(datetime.datetime.now())
		newStr = "\n%s\t---\t%s" % (timeStampStr, newStr)
		
		if (self.__logCount < listSize):
			# add to empty end slot 
			self.__gameLogStrList[self.__logCount] = newStr
			self.__logCount = self.__logCount + 1
		else:
			# add latest event to end of queue while maintaining max size
			del self.__gameLogStrList[0]
			self.__gameLogStrList.append(newStr)
	
	
	def print_events(self):
		
		gameLogStr =""
		
		for logStr in self.__gameLogStrList:
			gameLogStr = gameLogStr + logStr + "\n"
			
		print "\n\n%s\n%s\n%s\n\n" % (Const.SEPARATOR_LINE_STR,  gameLogStr,  Const.SEPARATOR_LINE_STR)
		

#---------------------------------------------------
#---------------------------------------------------
# Class: MapObjContainer
#
# Used to store objs mapped to display entities
#
# Member Variables:	
#
#	Public:
#		exitDict	- dictionary of current map's exits (these don't change hence using dict)
#		itemList	- list of item placed in map (not those currently contained by players)
#		actorList	- list of non-playable actors
#---------------------------------------------------
#---------------------------------------------------		
class MapObjContainer(object):
	
	PLAYER_INDEX = 0 # player starts at beginning of actorList

	def __init__(self):
		
		self.exitDict = {}
		self.itemList = []		
		self.__actorList = []
		
		self.clear()
			
	# Class: MapObjContainer
	#
	# Reset container data
	def clear(self):
		self.exitDict.clear()
		self.itemList[:] = []
		self.__actorList[:] = []
		# start with empty player slot (so no other actors are inserted here)
		self.__actorList.append(Entity.Actor()) 
		self.__actorList[0] = None
		
	# Class: MapObjContainer
	#
	# Methods to simplify player access
	def get_player(self):
		return self.get_actor(self.PLAYER_INDEX)
		
	def set_player(self, playerObj):
		self.set_actor(playerObj, self.PLAYER_INDEX)
		
	def get_num_actors(self):
		return len (self.__actorList)
		
	# Class: MapObjContainer
	#
	# Accessor for actor count
	def get_num_valid_actors(self):
		retVal = len (self.__actorList)
		
		if (retVal > 0):
			if (self.__actorList[0] == None):
				retVal -= 1
		
		return retVal
		
	# Class: MapObjContainer
	#
	# Adds actor obj to container
	def add_actor(self, actorObj, isPlayer=False):
		if (isPlayer):
			# replace current player
			self.__actorList[self.PLAYER_INDEX] = actorObj
		else:
			# need to insert player slot in list
			self.__actorList.append(actorObj)
		
	# Class: MapObjContainer
	#
	# Actor Accessors
	def get_actor(self, actorIndex):
		retObj = None
		
		if ((actorIndex >= 0) and (actorIndex < len (self.__actorList))):
			retObj = self.__actorList[actorIndex]
		
		return retObj
		
	def set_actor(self, actorObj, actorIndex):
		if (len (self.__actorList) > actorIndex):
			# slot already exists so replace existing oid
			self.__actorList[actorIndex] = actorObj
		else:
			# need to insert player slot in list
			self.__actorList.append(actorObj)
		
			
	

#---------------------------------------------------
#---------------------------------------------------
# Class: LevelEngine
#---------------------------------------------------
#---------------------------------------------------		
class LevelEngine(object):
	
	def __init__(self, levelDataFileStr):
		
		# DEBUG_JW start
		newMapNameStr = "Bridge"
		newMapObjvStr = "Location: Bridge.\nA Gothan stands in your way.\nYou must defeat him in order to set the bomb and attempt to escape.\n"
		newMapStrList = [Const.MAP_CC_STR1_UCODE, Const.MAP_TEST_STR1_UCODE, Const.MAP_TEST_STR2_UCODE]
		# DEBUG_JW end

		self.__theMapDisplayList = []
		self.__theMapNameStr = ""	# name of current map level
		self.__theMapObjvStr = ""	# player's current level obj
		
		self.__mapIndex = 0			# points to current player map
		
		self.__objContainer = MapObjContainer() # stores all scene entity objs
		self.__numMaps = Const.INVALID_INDEX
				
		# Clear the ID range so that all map obj in this level 
		# have unique IDs starting from 0.
		Display.MapContainer.IdGen.reset(0) 
				
		# assign our map log to global log
		self.__mapLog = Utils.MapLog()
		Utils.Init_Map_Log(self.__mapLog) # pass ref to global
		
		if (levelDataFileStr == ""):
			Utils.Show_Game_Error("LevelEngine::init() - invalid levelDataFileStr!")
		else:
			# parse level file
			
			# init internal map data (TODO: mapData init done in level file parse so should pass that here)
			self.init_map_data(newMapNameStr,  newMapObjvStr, newMapStrList)
			pass

	# Class: LevelEngine
	#
	# init all map data from level script
	def init_map_data(self,  newMapNameStr, newMapObjvStr, newMapStrList):
		
		for mapStr in newMapStrList:
			self.__theMapDisplayList.append(Display.MapContainer(mapStr))
		
		self.__numMaps = len (self.__theMapDisplayList)
		
		playerActor = GameState.Get_Player()
		
		# ---------------- from script --------------------------------
		playerActor.set_cmdStrList(['p','w','w','w','d','d','d','w','w','w','w','w','w','e','s','e','s','d','d','d','w','e','w'])
		
		self.__theMapNameStr = newMapNameStr
		self.__theMapObjvStr = newMapObjvStr
		playerPos = Display.MapPos(5, 11)
		
		playerMapIndex = 0 
		
		gothanActor1 = Entity.Actor()
		gothanPos1 = Display.MapPos(9, 2)
		batteryItem = Entity.UtilityItem(Const.ITEM_BATTERY_INDEX, 1)
		itemPos1 = Display.MapPos(5, 10)
		
		exit_char_H = Const.MAP_CHAR_EXIT_LIST[Const.TILE_ORIENTATION_HOROZONTAL]
		exit1_0_pos = Display.MapPos(8, 1)
		exit1_0_linkPos = Display.MapPos(5, 4)
		exit1_0 = Entity.MapExitItem(0, exit1_0_pos, exit_char_H, 1, exit1_0_linkPos)
		
		exit2_0_pos = Display.MapPos(11, 1)
		exit2_0_linkPos = Display.MapPos(11, 4)
		exit2_0 = Entity.MapExitItem(0, exit2_0_pos, exit_char_H, 2, exit2_0_linkPos)
		
		exit3_0_pos = Display.MapPos(5, 12)
		exit3_0_linkPos = None
		exit3_0 = Entity.MapExitItem(0, exit3_0_pos, exit_char_H, -1, exit3_0_linkPos) # starting point in level
		
		exit1_1_pos = Display.MapPos(5, 4)
		exit1_1_linkPos = Display.MapPos(8, 1)
		exit1_1 = Entity.MapExitItem(1, exit1_1_pos, exit_char_H, 0, exit1_1_linkPos)
		
		exit1_2_pos = Display.MapPos(11, 1)
		exit1_2_linkPos = None
		exit1_2 = Entity.MapExitItem(2, exit1_2_pos, exit_char_H, Const.LEVEL_EXIT_NUM, exit1_2_linkPos) # last exit in level
		
		exit2_2_pos = Display.MapPos(11, 4)
		exit2_2_linkPos = Display.MapPos(11, 1)
		exit2_2 = Entity.MapExitItem(2, exit2_2_pos, exit_char_H, 0, exit2_2_linkPos)
		
		levelScriptExitList = [exit1_0, exit2_0, exit3_0, exit1_1, exit1_2, exit2_2]
		#  ----------------------------------------------------------------
		
		for mapIndex in range(0, self.__numMaps):
			
			mapDisplay = self.__theMapDisplayList[mapIndex]
			
			# populate exitItem objs in container
			maxExitItem = len(levelScriptExitList)
			
			for exit in levelScriptExitList:
				exitMapIndex = exit.mapIndex
				if (exitMapIndex >= self.__theMapDisplayList):
					Utils.Show_Game_Error("LevelEngine::init_map_data() - invalid exitItem mapIndex %d" % exitMapIndex)
				else:
					exitID = mapDisplay.place_map_entity(exit.char, exit.pos)
					self.__objContainer.exitDict[exitID] = exit
					levelScriptExitList.remove(exit)
			
			if (mapIndex == playerMapIndex):
				playerActor.oid = self.__theMapDisplayList[mapIndex].place_map_entity(Const.MAP_CHAR_PLAYER_LIST[Const.DIR_NORTH], playerPos)
				playerActor.location = mapIndex
				self.__objContainer.set_actor(playerActor, MapObjContainer.PLAYER_INDEX)
		
			mapExitDict = {}
		
			if (mapIndex == 0):
				gothanChar = Const.MAP_CHAR_ENEMY_LIST[Const.DIR_SOUTH]
				gothanActor1.oid = self.__theMapDisplayList[mapIndex].place_map_entity(gothanChar, gothanPos1)
				gothanActor1.location = mapIndex
				self.__objContainer.set_actor(gothanActor1, 1)
				
				batteryItem.oid = self.__theMapDisplayList[mapIndex].place_map_entity(Const.MAP_CHAR_ITEM, itemPos1)
				self.__objContainer.itemList.append(batteryItem)
				
				#exitID = mapDisplay.place_map_entity(Const.MAP_CHAR_DOOR, exitPos1)
				#mapExitDict[exitID] = Entity.MapExitItem(mapIndex,  exitPos1, 0)
				
				exitID = mapDisplay.place_map_entity(exit1_0.char, exit1_0.pos)
				self.__objContainer.exitDict[exitID] = exit1_0
				
				exitID = mapDisplay.place_map_entity(exit2_0.char, exit2_0.pos)
				self.__objContainer.exitDict[exitID] = exit2_0
				
				exitID = mapDisplay.place_map_entity(exit3_0.char, exit3_0.pos)
				self.__objContainer.exitDict[exitID] = exit3_0
				
			if (mapIndex == 1):
				exitID = mapDisplay.place_map_entity(exit1_1.char, exit1_1.pos)
				self.__objContainer.exitDict[exitID] = exit1_1
				
			if (mapIndex == 2):
				exitID = mapDisplay.place_map_entity(exit1_2.char, exit1_2.pos)
				self.__objContainer.exitDict[exitID] = exit1_2
				
				exitID = mapDisplay.place_map_entity(exit2_2.char, exit2_2.pos)
				self.__objContainer.exitDict[exitID] = exit2_2
				

	# Class: LevelEngine
	#
	# determines if given mapIndex is in range of __theMapDisplayList
	def is_valid_map_index(self, mapIndex):
		retVal = False
		
		if ((mapIndex >= 0) and (mapIndex < len(self.__theMapDisplayList))):
			retVal = True
		
		return retVal
			
	# Class: LevelEngine
	#
	# Writes relative data to GameState
	def __create_checkPoint(self):
		pass
		
	
	# Executes series of maps in list
	def execute(self):
		
		done = False
		
		while (not done):
			if (self.__mapIndex >= len (self.__theMapDisplayList)):
				# we've hit an exit that moves player out of current level
				done = True
			else:
				# save off game progress and proceed player to next map
				self.__create_checkPoint()
				exitNum = self.__run_maps()
				
				if (exitNum == Const.LEVEL_EXIT_NUM):
					done = True
					Utils.Log_Event("MapEngine::execute() - done")
				else:
					# we're going to another map in level
					self.__mapIndex = exitNum # TODO: handle map transition
					Utils.Log_Event("LevelEngine::execute() - player moves to map %d" % exitNum)
								
		GameState.Set_Player(self.__objContainer.get_player())
		
	# Class: LevelEngine
	#	
	# Determine next map based on user exit of previous map
	def calc_next_map_index(self): 
		retIndex = Const.INVALID_INDEX
		
		# TODO: implementation
		pass
		
		return retIndex
		
	# Class: LevelEngine
	#
	# Runs all maps in level until player is done current map
	def __run_maps(self):
	
		exitNum = Const.INVALID_INDEX # unique ID for map exit that player chooses
		
		Utils.Log_Event("LevelEngine::__run_maps() - displaying map %d" % self.__mapIndex)
	
		done = False
		
		while (not done):
			
			# TODO: implement DisplayPrint thread and use list to pass display strings.
			#		Set list values here.
			# http://www.tutorialspoint.com/python/python_multithreading.htm
			
			# update user display
			Utils.Clear_Screen()
			
			print "LOCATION: %s" % self.__theMapNameStr
			Utils.Print_Map_Log()
			
			self.print_map_str()
			thePlayerObj = self.__objContainer.get_player()
			print "\nPLAYER HEALTH:\t%d\t\tCURRENT ITEM:\t%s\nDIRECTION:\t%s" % (thePlayerObj.get_health(), thePlayerObj.get_current_itemStr(), thePlayerObj.get_dir_str())
			
			
			# Possible TODO: 
			# use separate thread for keyboard input
			# https://bytes.com/topic/python/answers/43936-canceling-interrupting-raw_input
			
			# OR non-blocking raw_input()
			# http://www.garyrobinson.net/2009/10/non-blocking-raw_input-for-python.html
			
			# OR msvcrt module
			# http://effbot.org/librarybook/msvcrt.htm
			
			# iterate through all maps and process any changes
			maxMapCount = len(self.__theMapDisplayList)
			objContainer = self.__objContainer
			maxActorCount = objContainer.get_num_actors()
			
			for mapIndex in range(0, maxMapCount):
			
				# iterate through all actors of current map and get input
				for actorIndex in range(0, maxActorCount):
				
					actorObj = objContainer.get_actor(actorIndex)
					
					if (actorObj != None):
						answer = ''
						sendCmd = False
						
						# only process valid actors in the current map
						if (actorObj.location == mapIndex):
							
							# first, check for scripted cmd
							answer = actorObj.get_next_cmdStr()
							
							if (answer != ''):
								sendCmd = True
							elif (actorIndex == MapObjContainer.PLAYER_INDEX):
							
								# get user input
								#answer = Utils.Get_Key_Input("Enter Action:>")
								answer = Utils.Get_Key_Input("DEBUG_JW: mapIndex == %d, actorIndex == %d:>" % (mapIndex, actorIndex))
								#answer = nonBlockingRawInput("Enter Action:>")
								#answer = 'a'
								
								retStr = self.process_player_cmd(answer)
								
								if (retStr != ''):
									if (retStr == Const.MAP_CMD_STR_QUIT):
										# We're done here. No need to send cmd to map UI
										done = True
										
										# TODO: create method to get back to the main menu
										Utils.Exit_Game()
										break
									else:
										sendCmd = True
							
						if (sendCmd):
							# passing player cmd to UI
							exitNum = self.process_actor_cmd(mapIndex, answer, actorIndex)
							
							if (exitNum != Const.INVALID_INDEX):
								# actor transported to different map
								if (actorIndex == MapObjContainer.PLAYER_INDEX):
									# player has exited current map
									done = True
				
		return exitNum
		
	# TODO: remove???
	def get_map_exit_action(self, mapIndex, actionCmdStr, oid):

		exitNum = Const.INVALID_INDEX
		
		if (not self.is_valid_map_index(mapIndex)):
			Utils.Show_Game_Error("MapEngine::get_map_exit_action() - invalid mapIndex %d!" % mapIndex)
		else:
		
			objContainer = self.__objContainer
			
			if (actionCmdStr == Const.MAP_CMD_STR_USE):
				
				exitItem = objContainer.exitDict.get(oid)

				if (not exitItem):
					Utils.Show_Game_Error("LevelEngine::process_engine_action() - invalid exit oid %d!" % oid)
				else:
					exitNum = exitItem.linkIndex
		
		return exitNum
		
	# TODO: remove???
	def process_engine_action(self, engineActionItem):
		pass
		
	# Class: LevelEngine
	#
	# Process cmd entered by user on behalf of player
	# Returns:
	#	retCmdStr - empty str if cmd was processed, else original cmd		 	 
	def process_player_cmd(self, answer):
		
		retCmdStr = ''
			
		if (not answer in Const.MAP_CMD_STR_LIST):
			if (answer != ""):
				print Const.INVALID_ENTRY_RSP
		else:
			# valid cmd
			if (answer == Const.MAP_CMD_STR_PAUSE):
				raw_input("****** GAME PAUSED ******\n%s" % Const.PROMPT_CONTINUE_STR)
			
			elif (answer == Const.MAP_CMD_STR_OBJV):
				raw_input("****** GAME PAUSED ******\n\nOBJECTIVE:\n%s\n\n%s" % (self.__theMapObjvStr, Const.PROMPT_CONTINUE_STR))
				
			elif (answer == Const.MAP_CMD_STR_CMD_PROMPT):
				print "****** GAME PAUSED ******"
				cmdStr = raw_input("CMD>")
				isHandled = Utils.Process_Common_Actions(cmdStr, self.__objContainer.get_player())
				
				if (not isHandled):
					print Const.INVALID_ENTRY_RSP
				else:
					raw_input(Const.PROMPT_CONTINUE_STR)
					
			elif (answer in Const.ITEM_CMD_STR_LIST):
				# we have item hotkey equip cmd for player
				itemIndex = int(answer)
				playerObj = self.__objContainer.get_player()
				self.__objContainer.set_player(Utils.Equip_Player_From_Cmd(itemIndex, playerObj)) # DEBUG_JW: if playerObj is ef, dow we need to set_player()
				
			elif (answer == Const.MAP_CMD_STR_DUMP_DATA):
				mapNumStr = raw_input("Enter map # >")
				if (not mapNumStr.isdigit()):
					raw_input(Const.INVALID_ENTRY_RSP)
				else:
					mapIndex = int(mapNumStr)
					self.__theMapDisplayList[mapIndex].dump_map_data(mapIndex)
				
			else:
				# we have actor cmd that needs to go to map UI
				retCmdStr = answer
				
		return retCmdStr
		
	# Class: LevelEngine
	#
	# Processes actor action cmd that needs to go to map
	# Returns exitNum if actor exits current map, else INVALID_INDEX
	def process_actor_cmd(self, mapIndex, actionCmdStr, actorIndex):
		
		retVal = Const.INVALID_INDEX
		
		actorObj = self.__objContainer.get_actor(actorIndex)
				
		if (actorObj == None):
			Utils.Show_Game_Error("LevelEngine::process_actor_cmd() - could not get actorObj from actorIndex = %d!" % actorIndex)
		else:
			# MOVE
			if (actionCmdStr in Const.MOVE_CMD_STR_LIST):
				# translating move cmd to direction to simplify UI processing
				actorDir = Const.DIR_INVALID
				
				if (actionCmdStr == Const.MAP_CMD_STR_MOVE_NORTH):
					actorDir = Const.DIR_NORTH
				elif (actionCmdStr == Const.MAP_CMD_STR_MOVE_WEST):
					actorDir = Const.DIR_WEST
				elif (actionCmdStr == Const.MAP_CMD_STR_MOVE_SOUTH):
					actorDir = Const.DIR_SOUTH
				elif (actionCmdStr == Const.MAP_CMD_STR_MOVE_EAST):
					actorDir = Const.DIR_EAST
					
				if (actorObj.get_dir_num() != actorDir):
					actorObj.set_dir(actorDir)
				
				# send general move cmd to UI
				Utils.Log_Event("LevelEngine::process_actor_cmd() - moving actor %d in dir = %d" % (actorObj.oid, actorDir))
				self.__theMapDisplayList[mapIndex].move_map_item(actorObj.oid, actorDir)
			
			# USE
			elif (actionCmdStr == Const.MAP_CMD_STR_USE):
				actorDir = actorObj.get_dir_num()
				Utils.Log_Event("LevelEngine::process_actor_cmd() - actor %d issued use cmd in dir = %d" % (actorObj.oid, actorDir))
				useObjID, useObjCategory = self.__theMapDisplayList[mapIndex].use_map_item(actorObj.oid, actorDir)
				
				if (useObjCategory == Const.MAP_CAT_EXIT):
					# check to see if actor can exit current map
					exitItem = self.__objContainer.exitDict.get(useObjID)
				
					if (exitItem == None):
						Utils.Show_Game_Error("LevelEngine::process_actor_cmd() - could not get exit from useObjID=%d" % (useObjID))
					else:
						exitNum = exitItem.linkIndex
						retVal = exitNum
						
						if (exitNum != Const.LEVEL_EXIT_NUM):
							# not done with level yet
							if ((exitNum > Const.INVALID_INDEX) and (exitNum < len(self.__theMapDisplayList))):
								# ping display to see if actor has open space to move in next map
								Utils.Log_Event("LevelEngine::process_actor_cmd() - actor %d encountered exit map %d" % (actorObj.oid, exitNum))
								
								actorCategory = Const.INVALID_INDEX
								
								if (actorIndex == MapObjContainer.PLAYER_INDEX):
									actorCategory = Const.MAP_CAT_PLAYER
								else:
									actorCategory = Const.MAP_CAT_ENEMY
								
								
								isOpen = self.__theMapDisplayList[exitNum].is_open_pos_from_pos(exitItem.linkPos, actorCategory, actorDir)
									
								if (not isOpen):
									# the door is blocked so actor cannot proceed
									retVal = Const.INVALID_INDEX
									Utils.Write_Map_Log("This door is blocked")
								else:
									rStat = self.__transport_entity(actorObj, actorCategory, mapIndex, exitNum, exitItem.linkPos)
									Utils.Log_Event("LevelEngine::process_actor_cmd() - actor %d transported with Stat=%d" % (actorObj.oid, rStat))
									
									if (rStat != Const.RT_SUCCESS):
										# something went wrong... cannot proceed to next map
										retVal = Const.INVALID_INDEX
									
					
			# SHOOT
			elif (actionCmdStr == Const.MAP_CMD_STR_SHOOT):
				pass
				
		return retVal
		
	# Class: LevelEngine
	#
	# Transports actor entity between display maps.
	# Entity will be placed in their current direction 
	# outside the target map's exit.
	#
	# NOTE:
	#	Entity Oid will be updated to a valid Oid within new display
	#
	#	Parameters:
	#		entityObj		- entity data
	#		entityCategory	- map entity category
	#		currentMapIndex	- current map location of entity
	#		targetMapIndex	- target map location to move entity
	#		targetExitPos	- pos of target map's exit in which to move entity to 
	#
	#	Return:
	#		rStat - status of transport
	def __transport_entity(self, entityObj, entityCategory, currentMapIndex, targetMapIndex, targetExitPos):
	
		rStat = Const.RT_SUCCESS
		
		if ((entityObj == None) or (currentMapIndex < 0) or (currentMapIndex >= len(self.__theMapDisplayList)) or (targetMapIndex < 0) or (targetMapIndex >= len(self.__theMapDisplayList)) or (targetExitPos == None)):
			Utils.Show_Game_Error("LevelEngine::__transport_entity() - invalid parameter:category=%d, currentMap=%d, targetMap=%d!" % (entityCategory, currentMapIndex, targetMapIndex))
			rStat = Const.RT_INVALID_PARAMETER
		else:
		
			entityChar = ''
			entityDir = entityObj.get_dir_num()
			
			if (entityCategory == Const.MAP_CAT_PLAYER):
				entityChar = Const.MAP_CHAR_PLAYER_LIST[entityDir]
			elif (entityCategory == Const.MAP_CAT_ENEMY):
				entityChar = Const.MAP_CHAR_ENEMY_LIST[entityDir]
			else:
				Utils.Show_Game_Error("LevelEngine::__transport_entity() - invalid entityCategory %d!" % entityCategory)
				rStat = Const.RT_INVALID_PARAMETER
				
			if (entityChar != ''):
				# remove entity from current map and insert into target map
				rStat = self.__theMapDisplayList[currentMapIndex].remove_map_entity(entityObj.oid)
				
				if (rStat == Const.RT_SUCCESS):
					# create new entity in target map with new OID
					newOid = self.__theMapDisplayList[targetMapIndex].place_map_entity_from_dir(entityChar, targetExitPos, entityCategory, entityDir, True)
					
					if (newOid == Const.INVALID_INDEX):
						Utils.Show_Game_Error("LevelEngine::__transport_entity() - invalid obj entity placement at map %d - pos %s!" % (targetMapIndex, targetPos.get_str()))
						rStat = Const.RT_FAILURE
					else:
						entityObj.oid = newOid
						entityObj.location = targetMapIndex
		
		return rStat
		
	# Class: LevelEngine
	#
	# Displays current map as specified by __mapIndex
	def print_map_str(self, isUCode=True):
		if (isUCode):
			mapStr = u"%s" % self.__theMapDisplayList[self.__mapIndex].get_map_for_display()
		else:
			mapStr = "%s" % self.__theMapDisplayList[self.__mapIndex].get_map_for_display()
			
		"""
		DEBUG_JW: 
		ORIGINAL SETTINGS (works):
		>chcp 437
		>set PYTHONIOENCODING=
		
		NEW SETTINGS (crashes):
		>chcp 65001
		>set PYTHONIOENCODING=utf-8
		
		<set console font to Lucida>
		"""
		print mapStr
		
		
	# Class: LevelEngine
	#
	# Update level's map log
	def write_map_log(self,  gameStr):
		self.__mapLog.add(gameStr)
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: SceneEngine
#
# Member Variables:	
#		sceneMap - Map containing all available scenes
#--------------------------------------------------
#---------------------------------------------------		
class SceneEngine(object):
	
	def __init__(self, sceneMap):
		self.__sceneMap = Scene.SceneMap(Const.START_KEY)
	
	# Class: SceneEngine
	#
	# Drives game by running through scene state machine
	def play(self):

		Utils.Clear_Screen()
		# Show Title Screen with menu options
		print "%s\n%s\n%s\n" % (Const.SEPARATOR_LINE_STR, Const.ART_STR_GAME_TITLE, Const.SEPARATOR_LINE_STR)
		
		startMenuStr = """
			1. Start Game
			2. Help
			3. Quit
		"""
		
		if (Const.DEBUG_MODE):
			startMenuStr += "\t4. Test Scene"
		
		#TODO: - update this with more game details
		helpStr = """
			 Use the '?' in action prompts for hints on how to proceed.
		""" 
		
		openingMsgStr =  """
			Gothans have invaded your spaceship and killed everyone else on board. 
			Time to blow this baby and escape to the planet below!\n\n
		"""
		
		if (Const.DEBUG_MODE):
			Console.test_formatting()
		
		done = False
		
		while (not done):
			answer = raw_input("%s\n\t\t> " % startMenuStr)
			
			if (answer == '1'):
				# Start Game
				Utils.Clear_Screen()
				print openingMsgStr
				raw_input("\t\t\t%s" % Const.PROMPT_CONTINUE_STR)
				Utils.Clear_Screen()
				done = True
			elif (answer == '2'):
				# Show Help
				Utils.Clear_Screen()
				print helpStr
				raw_input(Const.PROMPT_CONTINUE_STR)
				Utils.Clear_Screen()
			elif (answer == '3'):
				# Quit
				Utils.Clear_Screen()
				exit(1)
			else:
				if (Const.DEBUG_MODE and ((answer == '4') or (answer == ''))):
					# Test mode
					done = True
					self.__sceneMap.firstScene = Const.TEST_KEY
				else:
					print Const.INVALID_ENTRY_RSP
					Utils.Clear_Screen()
					print "%s\n%s\n%s\n" % (Const.SEPARATOR_LINE_STR, Const.ART_STR_GAME_TITLE, Const.SEPARATOR_LINE_STR)

		# Each scene returns the player to maintain game state.
		thePlayer = GameState.Get_Player()
		
		# need while-loop here to drive game
		result, thePlayer = self.__sceneMap.opening_scene(thePlayer)
		
		while (result != Const.FINISH_RESULT_KEY):
			result, thePlayer = self.__sceneMap.next_scene(result, thePlayer)
			
		GameState.Set_Player(thePlayer)
		Utils.Exit_Game()	
	
	
# Module method to perform housekeeping items and initiate game 
def start():
	gameLogFileStr = os.getcwd() + '\\' + Const.GAME_LOG_STR
	Utils.Init_Game_Log(gameLogFileStr, "Starting Game")
	goodState = GameState.Init()
	
	codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

	if (not goodState):
		Utils.Log_Event("Could not init game state!")
		Utils.Exit_Game()
	else:
		# => Start the game
		aMap = Scene.SceneMap(Const.START_KEY) # pass in the key for the starting scene
		aGame = SceneEngine(aMap)
		
		aGame.play()
			
			
if __name__ == '__main__':	
	# Start here when this file is being run directly (rather than being imported).
	start()
