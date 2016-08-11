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
# Class: MapLog
#
# Purpose:
#		Maintains list of map events for user display.
#
# Member Variables:	
#
#	Private:
#		mapLogStrList 	- FIFO queue to store game msg strings
#		logCount			- number of msgs in queue
#---------------------------------------------------
#---------------------------------------------------
class MapLog(object):
	
	__gameLogStrList = []
	
	def __init__(self):
		
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
# Class: MapEngine
#---------------------------------------------------
#---------------------------------------------------		
class MapEngine(object):
	
	
	__theMapDisplay = None
	__theMapCmdList = []
	__theMapStrList = []
	__theMapNameStr = ""
	__theMapObjvStr = ""
	__mapIndex = 0
	__mapLog = None
	
	def __init__(self, newMapNameStr, newMapObjvStr, newMapStrList):
		self.__theMapNameStr = newMapNameStr
		self.__theMapObjvStr = newMapObjvStr
		self.__theMapStrList = newMapStrList
				
		# assign our map log to global log
		self.__mapLog = Utils.MapLog()
		Utils.Init_Map_Log(self.__mapLog) # pass ref to global
		
		if (len(newMapStrList) == 0):
			Utils.Show_Game_Error("MapEngine::init() - invalid newMapStrList!")

		
	def __update_map(self, listIndex):
		
		retVal = False
	
		if (listIndex < len (self.__theMapStrList)):
		
			newMapStr = u""
			newMapStr = self.__theMapStrList[listIndex]
			self.__theMapDisplay = MapDisplay.MapDisplayData(newMapStr)

			retVal = True
			
		return retVal
	
	# Executes series of maps in list
	def execute(self):
		
		done = False
		
		while (not done):
			if (not self.__update_map(self.__mapIndex)):
				Utils.Show_Game_Error("MapEngine::execute() - could not update map at index %d" % self.__mapIndex)
				done = True
			else:
				exitNum = self.__run_map()
				
				if (exitNum == GameData.MAP_EXIT_NUM):
					done = True
					Utils.Log_Event("MapEngine::execute() - done")
				else:
					# we're going to another map in level
					self.__mapIndex = exitNum
				
	# Determine next map based on user exit of previous map
	def calc_next_map_index(self): 
		retIndex = GameData.INVALID_INDEX
		
		# TODO: implementation
		pass
		
		return retIndex
		
	# Runs current map specified by __mapIndex
	def __run_map(self):
	
		thePlayer = GameState.Get_Player()
	
		exitNum = GameData.INVALID_INDEX # unique ID for map exit that player chooses
	
		done = False
		
		Utils.Log_Event("MapEngine::run_map() - running map %d" % self.__mapIndex)
		
		# Call utility function to iterate over map str and create list of game objs
		# DEBUG_JW: this is a hack for now!
		playerIdList = self.__theMapDisplay.get_obj_mapID_list(GameData.MAP_CAT_PLAYER)
		playerID = playerIdList[0]
		
		exitIdList = self.__theMapDisplay.get_obj_mapID_list(GameData.MAP_CAT_EXIT)
		exitDict = {}
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
				
			exitDict[exitID] = Entity.MapExitItem(exitLink)
		# end hack
			
		stateData = GameState.Get_State()
		stateData.mapExitDict = exitDict
		GameState.Set_State(stateData)
		# end hacked code
		
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
			print "\nPLAYER HEALTH:\t%d\t\tCURRENT ITEM:\t%s\nDIRECTION:\t%s" % (thePlayer.get_health(), thePlayer.get_current_itemStr(), thePlayer.get_dir_str())
			
			
			# Possible TODO: 
			# use separate thread for keyboard input
			# https://bytes.com/topic/python/answers/43936-canceling-interrupting-raw_input
			
			# OR non-blocking raw_input()
			# http://www.garyrobinson.net/2009/10/non-blocking-raw_input-for-python.html
			
			# OR msvcrt module
			# http://effbot.org/librarybook/msvcrt.htm
			
			answer = Utils.Get_Key_Input("Enter Action:>")
			#answer = nonBlockingRawInput("Enter Action:>")
			
			sendCmd = False
			
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
					isHandled = Utils.Process_Common_Actions(cmdStr, thePlayer)
					if (not isHandled):
						print GameData.INVALID_ENTRY_RSP
					else:
						raw_input(GameData.PROMPT_CONTINUE_STR)
						
				elif (answer in GameData.ITEM_CMD_STR_LIST):
					# we have item hotkey equip cmd for player
					itemIndex = int(answer)
					thePlayer = Utils.Equip_Player_From_Cmd(itemIndex,  thePlayer)
					
				elif (answer == GameData.MAP_CMD_STR_QUIT):
						# We're done here. No need to send cmd to map UI
						#done = True
						# TODO: create method to get back to the main menu
						Utils.Exit_Game()
				else:
					# we have cmd that needs to go to map UI
					sendCmd = True
				
			if (sendCmd and not done):
				# passing cmd to UI
				playerDir = GameData.DIR_INVALID
				
				if (answer in GameData.MOVE_CMD_STR_LIST):
					# translating move cmd to direction to simplify UI processing
					if (answer == GameData.MAP_CMD_STR_MOVE_NORTH):
						playerDir = GameData.DIR_NORTH
					elif (answer == GameData.MAP_CMD_STR_MOVE_WEST):
						playerDir = GameData.DIR_WEST
					elif (answer == GameData.MAP_CMD_STR_MOVE_SOUTH):
						playerDir = GameData.DIR_SOUTH
					elif (answer == GameData.MAP_CMD_STR_MOVE_EAST):
						playerDir = GameData.DIR_EAST
						
					if (thePlayer.dir != playerDir):
						Utils.Log_Event("Changing player dir to %d" % playerDir)
						thePlayer.dir = playerDir
					
					# send general move cmd to UI
					answer = GameData.MAP_CMD_STR_MOVE
			
				# construct player action
				playerAction = MapActionItem(answer, playerID, thePlayer.get_dir_num())
				self.__theMapCmdList.append(playerAction)

				
				# get enemy AI input
				pass
				
				# construct enemy moves
				pass
			
				# send actionList to map
				for cmdItem in self.__theMapCmdList:
					#Utils.Log_Event("DEBUG_JW: Map Engine sending UI cmd - %s" % cmdItem.dump_data())
					engineActionItem = self.__theMapDisplay.process_map_cmd(cmdItem)
					
					# process any return map engine action from the UI
					if (engineActionItem != None):
						Utils.Log_Event("Map Engine receiving UI cmd - %s" % engineActionItem.dump_data())
						
						# check for exit to see if we are done with current map
						exitNum = self.get_map_exit_action(engineActionItem)
						
						if (exitNum != GameData.INVALID_INDEX):
							done = True
						else:
							# process any other return action
							self.process_engine_action(engineActionItem)
				
		GameState.Set_Player(thePlayer)
				
		return exitNum
		
		
	def get_map_exit_action(self, engineActionItem):

		exitNum = GameData.INVALID_INDEX
		
		if (engineActionItem.cmdStr == GameData.MAP_CMD_STR_USE):
			stateData = GameState.Get_State()
			exitItem = stateData.mapExitDict.get(engineActionItem.objID)

			if (not exitItem):
				Utils.Show_Game_Error("MapEngine::process_engine_action() - invalid exit objID %d!" % engineActionItem.objID)
			else:
				exitNum = exitItem.linkIndex
		
		return exitNum
		
	def process_engine_action(self, engineActionItem):
		pass
		
	def print_map_str(self, isUCode=True):
		if (isUCode):
			mapStr = u"%s" % self.__theMapDisplay.get_map()
		else:
			mapStr = "%s" % self.__theMapDisplay.get_map()
			
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

		# Each scene returns the player to maintain game state.
		thePlayer = GameState.Get_Player()
		
		# need while-loop here to drive game
		result, thePlayer = self.__sceneMap.opening_scene(thePlayer)
		
		while (result != GameData.FINISH_RESULT_KEY):
			result, thePlayer = self.__sceneMap.next_scene(result, thePlayer)
			
		GameState.Set_Player(thePlayer)
		Utils.Exit_Game()	
		
