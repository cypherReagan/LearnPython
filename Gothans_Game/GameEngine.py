import GothansGame
import MapDisplay
import GameData
import GameState
import Utils
import datetime
import Scene
import Entity
	
#---------------------------------------------------
#---------------------------------------------------
# Class: MapActionItem
#
#	Base class for action items.
#
# Member Variables:	
#
#	Required:
#		cmdStr		- map manipulation command
#		targetID	- target objID in map 
#
#	Optional:
#		dir			- map direction
#---------------------------------------------------
#---------------------------------------------------
class MapActionItem(object):

	def __init__(self, newCmdStr, newTargetID, newDir=GameData.DIR_INVALID):
		self.cmdStr = newCmdStr
		self.objID = newTargetID
		self.dir = newDir
		
	def dump_data(self):
		retStr = "Action: cmdStr = %s, objID = %d, dir = %d" % (self.cmdStr, self.objID, self.dir)
		return retStr
	
#---------------------------------------------------
#---------------------------------------------------
# Class: UseActionItem
#
# Member Variables:	
#
#	Required:
#		itemType	- item type being used
#
#	Optional:
#		exitNum		- number of exit door order
#---------------------------------------------------
#---------------------------------------------------	
class UseActionItem(MapActionItem):

	def __init__(self, newItemType, newExitNum=GameData.INVALID_INDEX):
		self.itemType = newItemType
		self.exitnum = newExitNum
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: PlaceEntityActionItem
#
# Member Variables:	
#
#	Required:
#		entityType	- entity type being placed
#		entityPos	- target map position
#---------------------------------------------------
#---------------------------------------------------	
class PlaceEntityActionItem(MapActionItem):

	def __init__(self, newEntityType, newEntityPos):
		self.entityType = newEntityType
		self.entityPos = newEntityPos
		

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
#		mapLogStrList 	- FIFO queue to store game msg strings
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
		
		for count in range(0, GameData.MAX_GAME_LOG_ENTRIES):
			self.__gameLogStrList.append("")
		
	
	def add(self,  newStr):
		
		listSize = len (self.__gameLogStrList)
		#Utils.Show_Game_Error("DEBUG_JW: GameLog.add(%s) - listSize = %d" % (newStr,  listSize))
		
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
			
		print "\n\n%s\n%s\n%s\n\n" % (GameData.SEPARATOR_LINE_STR,  gameLogStr,  GameData.SEPARATOR_LINE_STR)
		

#---------------------------------------------------
#---------------------------------------------------
# Class: MapObjContainer
#
# Used to store objs mapped to display entities
#
# Member Variables:	
#
#	Public:
#		exitDict	- dictionary of current map's exits
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
			
	
	def clear(self):
		self.exitDict.clear()
		self.itemList[:] = []
		self.__actorList[:] = []
		# start with empty player slot (so no other actors are inserted here)
		self.__actorList.append(Entity.Actor()) 
		self.__actorList[0] = None
		
	# Methods to simplify player access
	def get_player(self):
		return self.get_actor(self.PLAYER_INDEX)
		
	def set_player(self, playerObj):
		self.set_actor(playerObj, self.PLAYER_INDEX)
		
	def get_num_actors(self):
		return len (self.__actorList)
		
	def get_num_valid_actors(self):
		retVal = len (self.__actorList)
		
		if (retVal > 0):
			if (self.__actorList[0] == None):
				retVal -= 1
		
		return retVal
		
	# Actor Accessors
	def get_actor(self, actorIndex):
		retObj = None
		
		if ((actorIndex >= 0) and (actorIndex < len (self.__actorList))):
			retObj = self.__actorList[actorIndex]
		
		return retObj
		
	def set_actor(self, actorObj, actorIndex):
		if (len (self.__actorList) > actorIndex):
			# slot already exists so replace existing objID
			self.__actorList[actorIndex] = actorObj
		else:
			# need to insert player slot in list
			self.__actorList.append(actorObj)
		
			
	

#---------------------------------------------------
#---------------------------------------------------
# Class: MapEngine
#---------------------------------------------------
#---------------------------------------------------		
class MapEngine(object):
	
	
	__theMapCmdList = []	# TODO: remove this
	__objContainer = None	# stores all level entity objs DEBUG_JW - remove this?
	
	def __init__(self, levelDataFileStr):
		
		# DEBUG_JW start
		newMapNameStr = "Bridge"
		newMapObjvStr = "Location: Bridge.\nA Gothan stands in your way.\nYou must defeat him in order to set the bomb and attempt to escape.\n"
		newMapStrList = [GameData.MAP_CC_STR1_UCODE, GameData.MAP_TEST_STR1_UCODE, GameData.MAP_TEST_STR2_UCODE]
		# DEBUG_JW end
		
		self.__theMapDisplay = None # TODO: remove
		self.__theMapDisplayList = []
		self.__theMapStrList = []
		self.__theMapNameStr = ""	# name of current map level
		self.__theMapObjvStr = ""	# player's current level obj
		
		self.__mapIndex = 0			# points to current player map
		
		self.__objContainer = MapObjContainer()
		self.__objContainerList = []	# stores all scene entity objs
		self.__numMaps = GameData.INVALID_INDEX
				
		# assign our map log to global log
		self.__mapLog = Utils.MapLog()
		Utils.Init_Map_Log(self.__mapLog) # pass ref to global
		
		if (levelDataFileStr == ""):
			Utils.Show_Game_Error("MapEngine::init() - invalid levelDataFileStr!")
		else:
			# parse level file
			
			# init internal map data (TODO: mapData init done in level file parse so should pass that here)
			self.init_map_data(newMapNameStr,  newMapObjvStr, newMapStrList)
			pass

	# init all map data from level script
	def init_map_data(self,  newMapNameStr, newMapObjvStr, newMapStrList):
		
		for mapStr in newMapStrList:
			self.__theMapStrList.append(mapStr)
			self.__objContainerList.append(MapObjContainer())
			self.__theMapDisplayList.append(MapDisplay.MapContainer(mapStr))
		
		self.__numMaps = len (self.__theMapStrList)
		
		playerActor = GameState.Get_Player()
		
		# ---------------- from script --------------------------------
		self.__theMapNameStr = newMapNameStr
		self.__theMapObjvStr = newMapObjvStr
		playerPos = MapDisplay.MapPos(5,  11)
		
		exitPos1 = MapDisplay.MapPos(5,  12)
		playerMapIndex = 0 
		
		gothanActor1 = Entity.Actor()
		gothanPos1 = MapDisplay.MapPos(9,  2)
		batteryItem = Entity.UtilityItem(GameData.ITEM_BATTERY_INDEX,  1)
		itemPos1 = MapDisplay.MapPos(5,  10)
		#  ----------------------------------------------------------------
		
		for mapIndex in range(0, self.__numMaps):
			
			mapDisplay = self.__theMapDisplayList[mapIndex]
			mapObjContainer = self.__objContainerList[mapIndex]
			
			if (mapIndex == playerMapIndex):
				playerActor.Id = self.__theMapDisplayList[mapIndex].place_map_entity(GameData.MAP_CHAR_PLAYER, playerPos)
				self.__objContainerList[mapIndex].set_actor(playerActor, MapObjContainer.PLAYER_INDEX)
		
			mapExitDict = {}
		
			if (mapIndex == 0):
				gothanChar = GameData.MAP_CHAR_ENEMY_LIST[GameData.DIR_SOUTH]
				gothanActor1.Id = self.__theMapDisplayList[mapIndex].place_map_entity(gothanChar, gothanPos1)
				self.__objContainerList[mapIndex].set_actor(gothanActor1, 1)
				
				batteryItem.Id = self.__theMapDisplayList[mapIndex].place_map_entity(GameData.MAP_CHAR_ITEM, itemPos1)
				self.__objContainerList[mapIndex].itemList.append(batteryItem)
				pass
				#exitID = mapDisplay.place_map_entity(GameData.MAP_CHAR_DOOR, exitPos1)
				#mapExitDict[exitID] = Entity.MapExitItem(mapIndex,  exitPos1, 0)
				
			mapObjContainer.exitDict = mapExitDict

	# determines if given mapIndex is in range of __theMapStrList
	def is_valid_map_index(self, mapIndex):
		retVal = False
		
		if ((mapIndex >= 0) and (mapIndex < len(self.__theMapStrList))):
			retVal = True
		
		return retVal
			
	# Writes relative data to GameState
	def __create_checkPoint(self):
		pass
		
		
	# DEBUG_JW: probebly don't need this... remove
	def __update_map(self, listIndex):
		
		retVal = False
	
		if (listIndex < len (self.__theMapStrList)):
		
			newMapStr = u""
			newMapStr = self.__theMapStrList[listIndex]
			self.__theMapDisplay = MapDisplay.MapContainer(newMapStr)

			retVal = True
			
		return retVal
	
	# Executes series of maps in list
	def execute(self):
		
		# DEBUG_JW: might need to do this at obj placement
		#self.__objContainerList[self.__mapIndex].set_player(GameState.Get_Player())
		
		done = False
		
		while (not done):
			if (self.__mapIndex >= len (self.__theMapStrList)):
				# we've hit an exit that moves player out of current level
				done = True
			else:
				# save off game progress and proceed player to next map
				self.__create_checkPoint()
				exitNum = self.__run_maps()
				
				if (exitNum == GameData.MAP_EXIT_NUM):
					done = True
					Utils.Log_Event("MapEngine::execute() - done")
				else:
					# we're going to another map in level
					self.__mapIndex = exitNum # TODO: handle map transition
					Utils.Log_Event("MapEngine::execute() - player moves to map %d" % exitNum)
					
					
		GameState.Set_Player(self.__objContainerList[self.__mapIndex].get_player())
		
				
	# Determine next map based on user exit of previous map
	def calc_next_map_index(self): 
		retIndex = GameData.INVALID_INDEX
		
		# TODO: implementation
		pass
		
		return retIndex
		
	# Runs all maps in level until player is done current map
	def __run_maps(self):
	
		exitNum = GameData.INVALID_INDEX # unique ID for map exit that player chooses
		
		Utils.Log_Event("MapEngine::__run_maps() - displaying map %d" % self.__mapIndex)
	
		done = False
		
		# Call utility function to iterate over map str and create list of game objs
		# ############### DEBUG_JW: this is a hack for now!
		
		# FIXME: DEBUG_JW - continue removing __theMapDisplay references here
		if (0):
		
			exitIdList = []#self.__theMapDisplay.__get_obj_mapID_list(GameData.MAP_CAT_EXIT)
			mapExitDict = {}
			
			tmpActor = GameState.Get_Player()

			for exitID in exitIdList:
				exitLink = GameData.INVALID_INDEX
				
				if (self.__mapIndex == 0):
					# map 0
					if (exitID == 9):
						exitLink = 1
					elif (exitID == 12):
						exitLink = 2
					elif (exitID == 160):
						exitLink = 0 # stay here when using first entry
						
				elif (self.__mapIndex == 1):
					# map 1
					if (exitID == 48):
						exitLink = 0
						
				elif (self.__mapIndex == 2):
					# map 2
					if (exitID == 12):
						exitLink = GameData.MAP_EXIT_NUM # flag the level exit using unique num ( len(__theMapStrList)? )
					if (exitID == 54):
						exitLink = 0
					
				mapExitDict[exitID] = Entity.MapExitItem(exitLink)
			
			if (self.__mapIndex == 0):
					# map 0
					tmpActor.Id = self.__theMapDisplay.place_map_entity(GameData.MAP_CHAR_PLAYER, MapDisplay.MapPos(5, 11))
			
			self.__objContainerList[0].exitDict = mapExitDict
			self.__objContainerList[self.__mapIndex].set_actor(tmpActor, MapObjContainer.PLAYER_INDEX)
			
		# ############### end hacked code
		
		while (not done):
			# clear all old map actions
			del self.__theMapCmdList[:]
			
			# TODO: implement DisplayPrint thread and use list to pass display strings.
			#		Set list values here.
			# http://www.tutorialspoint.com/python/python_multithreading.htm
			
			# update user display
			Utils.Clear_Screen()
			
			print "LOCATION: %s" % self.__theMapNameStr
			Utils.Print_Map_Log()
			
			self.print_map_str()
			thePlayerObj = self.__objContainerList[self.__mapIndex].get_player()
			print "\nPLAYER HEALTH:\t%d\t\tCURRENT ITEM:\t%s\nDIRECTION:\t%s" % (thePlayerObj.get_health(), thePlayerObj.get_current_itemStr(), thePlayerObj.get_dir_str())
			
			
			# Possible TODO: 
			# use separate thread for keyboard input
			# https://bytes.com/topic/python/answers/43936-canceling-interrupting-raw_input
			
			# OR non-blocking raw_input()
			# http://www.garyrobinson.net/2009/10/non-blocking-raw_input-for-python.html
			
			# OR msvcrt module
			# http://effbot.org/librarybook/msvcrt.htm
			
			# iterate through all maps and process any changes
			maxMapCount = len(self.__theMapStrList)
			
			for mapIndex in range(0, maxMapCount):
			
				objContainer = self.__objContainerList[mapIndex]
			
				# iterate through all actors of current map and get input
				maxActorCount = objContainer.get_num_actors()
				
				for actorIndex in range(0, maxActorCount):
				
					actorObj = objContainer.get_actor(actorIndex)
					answer = ''
					sendCmd = False
					
					if (actorObj != None):
						# only process valid actors
						if (actorIndex != MapObjContainer.PLAYER_INDEX):
							# get actor AI input
							#answer = actorObj.get_next_action()
							if (answer != ''):
								sendCmd = True
							pass
						else:
							# get user input
							#answer = Utils.Get_Key_Input("Enter Action:>")
							answer = Utils.Get_Key_Input("DEBUG_JW: mapIndex == %d, actorIndex == %d:>" % (mapIndex, actorIndex))
							#answer = nonBlockingRawInput("Enter Action:>")
							#answer = 'a'
							
							retStr = self.process_player_cmd(answer)
							
							if (retStr != ''):
								if (retStr == GameData.MAP_CMD_STR_QUIT):
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
						
						if (exitNum != GameData.INVALID_INDEX):
							if (actorIndex == MapObjContainer.PLAYER_INDEX):
								# player has exited current map
								done = True
							else:
								# actor transports to different map
								pass
							
					
						# construct player action
						#playerAction = MapActionItem(answer, playerID, self.__objContainerList[self.__mapIndex].thePlayer.get_dir_num())
						#self.__theMapCmdList.append(playerAction)

						
						# DEBUG_JW: delete this loop!
						# send action to map
						if (0):
							for cmdItem in self.__theMapCmdList:
								#Utils.Log_Event("DEBUG_JW: Map Engine sending UI cmd - %s" % cmdItem.dump_data())
								engineActionItem = self.__theMapDisplay.process_map_cmd(cmdItem)
								
								# process any return map engine action from the UI
								if (engineActionItem != None):
									Utils.Log_Event("Map Engine receiving UI cmd - %s" % engineActionItem.dump_data())
									
									# check for exit to see if we are done with current map
									exitNum = self.get_map_exit_action(mapIndex, engineActionItem)
									
									if (exitNum != GameData.INVALID_INDEX):
										done = True
									else:
										# process any other return action
										self.process_engine_action(engineActionItem)
				
		return exitNum
		
		
	def get_map_exit_action(self, mapIndex, actionCmdStr, objID):

		exitNum = GameData.INVALID_INDEX
		
		if (not self.is_valid_map_index(mapIndex)):
			Utils.Show_Game_Error("MapEngine::get_map_exit_action() - invalid mapIndex %d!" % mapIndex)
		else:
		
			objContainer = self.__objContainerList[mapIndex]
			
			if (actionCmdStr == GameData.MAP_CMD_STR_USE):
				
				exitItem = objContainer.exitDict.get(objID)

				if (not exitItem):
					Utils.Show_Game_Error("MapEngine::process_engine_action() - invalid exit objID %d!" % objID)
				else:
					exitNum = exitItem.linkIndex
		
		return exitNum
		
	def process_engine_action(self, engineActionItem):
		pass
		
	# Process cmd entered by user on behalf of player
	# Returns:
	#	retCmdStr - empty str if cmd was processed, else original cmd		 
	#			 
	def process_player_cmd(self, answer):
		
		retCmdStr = ''
			
		if (not answer in GameData.MAP_CMD_STR_LIST):
			if (answer != ""):
				print GameData.INVALID_ENTRY_RSP
		else:
			# valid cmd
			if (answer == GameData.MAP_CMD_STR_PAUSE):
				raw_input("****** GAME PAUSED ******\n%s" % GameData.PROMPT_CONTINUE_STR)
			
			elif (answer == GameData.MAP_CMD_STR_OBJV):
				raw_input("****** GAME PAUSED ******\n\nOBJECTIVE:\n%s\n\n%s" % (self.__theMapObjvStr, GameData.PROMPT_CONTINUE_STR))
				
			elif (answer == GameData.MAP_CMD_STR_CMD_PROMPT):
				print "****** GAME PAUSED ******"
				cmdStr = raw_input("CMD>")
				isHandled = Utils.Process_Common_Actions(cmdStr, self.__objContainerList[self.__mapIndex].get_player())
				
				if (not isHandled):
					print GameData.INVALID_ENTRY_RSP
				else:
					raw_input(GameData.PROMPT_CONTINUE_STR)
					
			elif (answer in GameData.ITEM_CMD_STR_LIST):
				# we have item hotkey equip cmd for player
				itemIndex = int(answer)
				playerObj = self.__objContainerList[self.__mapIndex].get_player()
				self.__objContainerList[self.__mapIndex].set_player(Utils.Equip_Player_From_Cmd(itemIndex, playerObj))
				
			elif (answer == GameData.MAP_CMD_STR_DUMP_DATA):
				mapNumStr = raw_input("Enter map # >")
				if (not mapNumStr.isdigit()):
					raw_input(GameData.INVALID_ENTRY_RSP)
				else:
					mapIndex = int(mapNumStr)
					self.__theMapDisplayList[mapIndex].dump_map_data(mapIndex)
				
			else:
				# we have actor cmd that needs to go to map UI
				retCmdStr = answer
				
		return retCmdStr
		
	# Processes actor action cmd that needs to go to map
	# Returns exitNum if actor exits current map, else INVALID_INDEX
	def process_actor_cmd(self, mapIndex, actionCmdStr, actorIndex):
		
		retVal = GameData.INVALID_INDEX
		
		actorObj = self.__objContainerList[mapIndex].get_actor(actorIndex)
				
		if (actorObj == None):
			Utils.Show_Game_Error("MapEngine::process_actor_cmd() - could not get actorObj from actorIndex = %d!" % actorIndex)
		else:
		
			if (actionCmdStr in GameData.MOVE_CMD_STR_LIST):
				# translating move cmd to direction to simplify UI processing
				actorDir = GameData.DIR_INVALID
				
				if (actionCmdStr == GameData.MAP_CMD_STR_MOVE_NORTH):
					actorDir = GameData.DIR_NORTH
				elif (actionCmdStr == GameData.MAP_CMD_STR_MOVE_WEST):
					actorDir = GameData.DIR_WEST
				elif (actionCmdStr == GameData.MAP_CMD_STR_MOVE_SOUTH):
					actorDir = GameData.DIR_SOUTH
				elif (actionCmdStr == GameData.MAP_CMD_STR_MOVE_EAST):
					actorDir = GameData.DIR_EAST
					
				if (actorObj.get_dir_num() != actorDir):
					actorObj.set_dir(actorDir)
				
				# send general move cmd to UI
				Utils.Log_Event("MapEngine::process_actor_cmd() - moving actor in dir = %d" % actorDir)
				self.__theMapDisplayList[mapIndex].move_map_item(actorObj.Id, actorDir)
				
			elif (actionCmdStr == GameData.MAP_CMD_STR_USE):
				useObjID = self.__theMapDisplay.use_map_item(actorObj.Id, actorObj.get_dir_num())
				
				# check for exit to see if actor need to exit current map
				exitNum = self.get_map_exit_action(mapIndex,  actionCmdStr, useObjID)
				
				if (exitNum != GameData.INVALID_INDEX):
					retVal = exitNum
				else:
					pass
				
			elif (actionCmdStr == GameData.MAP_CMD_STR_SHOOT):
				pass
				
		return retVal
		
		
	def print_map_str(self, isUCode=True):
		if (isUCode):
			mapStr = u"%s" % self.__theMapDisplayList[self.__mapIndex].get_map_for_display()
		else:
			mapStr = "%s" % self.__theMapDisplayList[self.__mapIndex].get_map_for_display()
			
		print mapStr
		
		
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
		self.__sceneMap = Scene.SceneMap(GameData.START_KEY)
		
	def play(self):

		Utils.Clear_Screen()
		# Show Title Screen with menu options
		print "%s\n%s\n%s\n" % (GameData.SEPARATOR_LINE_STR, GameData.ART_STR_GAME_TITLE, GameData.SEPARATOR_LINE_STR)
		
		# TODO: - possibly store all game msgs in separate file
		startMenuStr = """
			1. Start Game
			2. Help
			3. Quit
		"""
		
		#TODO: - update this with more game details
		helpStr = """
			 Use the '?' in action prompts for hints on how to proceed.
		""" 
		
		openingMsgStr =  """
			Gothans have invaded your spaceship and killed everyone else on board. 
			Time to blow this baby and escape to the planet below!\n\n
		"""
		
		# DEBUG_JW: testing colors
		#print MapDisplay.bcolors.WARNING + "Warning: No active frommets remain. Continue?" + MapDisplay.bcolors.ENDC
		print "It is \033[31mnot\033[39m intelligent to use \033[32mhardcoded ANSI\033[39m codes!"
		raw_input(GameData.PROMPT_CONTINUE_STR)
		# end debug
		
		done = False
		
		while (not done):
			answer = raw_input("%s\n\t\t> " % startMenuStr)
			
			# TODO: remove empty space detection here
			if ((answer == '1') or (answer == '')):
				# Start Game
				Utils.Clear_Screen()
				print openingMsgStr
				raw_input("\t\t\t%s" % GameData.PROMPT_CONTINUE_STR)
				Utils.Clear_Screen()
				done = True
			elif (answer == '2'):
				# Show Help
				Utils.Clear_Screen()
				print helpStr
				raw_input(GameData.PROMPT_CONTINUE_STR)
				Utils.Clear_Screen()
			elif (answer == '3'):
				# Quit
				Utils.Clear_Screen()
				exit(1)
			else:
				print GameData.INVALID_ENTRY_RSP
				Utils.Clear_Screen()
				print "%s\n%s\n%s\n" % (GameData.SEPARATOR_LINE_STR, GameData.ART_STR_GAME_TITLE, GameData.SEPARATOR_LINE_STR)

		# Each scene returns the player to maintain game state.
		thePlayer = GameState.Get_Player()
		
		# need while-loop here to drive game
		result, thePlayer = self.__sceneMap.opening_scene(thePlayer)
		
		while (result != GameData.FINISH_RESULT_KEY):
			result, thePlayer = self.__sceneMap.next_scene(result, thePlayer)
			
		GameState.Set_Player(thePlayer)
		Utils.Exit_Game()	
		
if __name__ == '__main__':	
	GothansGame.start()
