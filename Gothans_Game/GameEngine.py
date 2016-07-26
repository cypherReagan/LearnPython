import MapDisplay
import GameData
import GameState
import Utils
import datetime
import Scene
	
#---------------------------------------------------
#---------------------------------------------------
# Class: MapActionItem
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
		self.targetID = newTargetID
		self.dir = newDir
		
	def dump_item_data(self):
		retStr = "Action: cmdStr = %s, targetID = %d, dir = %d" % (self.cmdStr, self.targetID, self.dir)
		return retStr

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
			Utils.Log_Event("MapEngine::__update_map() - showing map %d" % listIndex)
		
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
				exitNum = self.run_map()
				# TODO: process exitNum
				tmpIndex = self.calc_next_map_index()
				
				if (tmpIndex != GameData.INVALID_INDEX):
					self.__mapIndex = tmpIndex
				else:
					done = True
				
	# Determine next map based on user exit of previous map
	def calc_next_map_index(self): 
		retIndex = GameData.INVALID_INDEX
		
		# TODO: implementation
		pass
		
		return retIndex
		
	# Runs current map specified by __mapIndex
	def run_map(self):
	
		thePlayer = GameState.Get_Player()
	
		exitNum = GameData.INVALID_INDEX # unique ID for map exit that player chooses
	
		done = False
		
		# Call utility function to iterate over map str and create list of game objs
		# DEBUG_JW: this is a hack for now!
		playerID = self.__theMapDisplay.get_ID(GameData.MAP_CAT_PLAYER)
		
		while (not done):
			# clear all old map actions
			del self.__theMapCmdList[:]
			
			# process any UI msgs from mapDisplay
			pass
			
			# TODO: implement DisplayPrint thread and use list to pass display strings.
			#		Set list values here.
			# http://www.tutorialspoint.com/python/python_multithreading.htm
			
			# update user display
			Utils.Clear_Screen()
			
			print "LOCATION: %s" % self.__theMapNameStr
			Utils.Print_Map_Log()
			
			self.print_map_str()
			print "\nPLAYER HEALTH:\t%d\t\tCURRENT ITEM:\t%s\nDIRECTION:\t%s" % (thePlayer.get_health(), thePlayer.get_current_itemStr(), thePlayer.get_dir_str())
			
			
			
			# TODO: 
			# use separate thread for keyboard input
			# https://bytes.com/topic/python/answers/43936-canceling-interrupting-raw_input
			
			# OR non-blocking raw_input()
			# http://www.garyrobinson.net/2009/10/non-blocking-raw_input-for-python.html
			
			# OR msvcrt module
			# http://effbot.org/librarybook/msvcrt.htm
			
			answer = Utils.Get_Key_Input("Enter Action:>")
			#answer = nonBlockingRawInput("Enter Action:>")
			
			isGoodInput = False
			
			if (answer == GameData.MAP_CMD_STR_PAUSE):
				raw_input("****** GAME PAUSED ******\n%s" % GameData.PROMPT_CONTINUE_STR)
				
			if (answer == GameData.MAP_CMD_STR_OBJV):
				raw_input("****** GAME PAUSED ******\n\nOBJECTIVE:\n%s\n\n%s" % (self.__theMapObjvStr, GameData.PROMPT_CONTINUE_STR))
				
			elif (answer == GameData.MAP_CMD_STR_CMD_PROMPT):
				print "****** GAME PAUSED ******"
				cmdStr = raw_input("CMD>")
				isHandled = Utils.Process_Common_Actions(cmdStr, thePlayer)
				if (not isHandled):
					print GameData.INVALID_ENTRY_RSP
				else:
					raw_input(GameData.PROMPT_CONTINUE_STR)
			else:
			
				if (answer in GameData.MAP_CMD_STR_LIST):
					# valid cmd
					if (answer in GameData.ITEM_CMD_STR_LIST):
						# we have item hotkey equip cmd for player
						itemIndex = int(answer)
						thePlayer = Utils.Equip_Player_From_Cmd(itemIndex,  thePlayer)
					else:
						# we might have cmd that needs to go to map UI
						isGoodInput = True
						
						if (answer == GameData.MAP_CMD_STR_QUIT):
							# We're done here. No need to send cmd to map UI
							done = True
				elif (answer != ""):
					print GameData.INVALID_ENTRY_RSP
				
			if (isGoodInput and not done):
				# construct player action
				playerAction = MapActionItem(answer, playerID, thePlayer.get_dir_num())
				self.__theMapCmdList.append(playerAction)
				
				# update direction based on movement
				#TODO: move this to Utils

				
				# get enemy AI input
				pass
				
				# construct enemy moves
				pass
			
				# send actionList to map
				for cmdItem in self.__theMapCmdList:
					engineActionItem = self.__theMapDisplay.process_map_cmd(cmdItem.cmdStr, cmdItem.targetID)
					
					# process any return map engine action from the UI
					if (engineActionItem != None):
						self.process_engine_action(engineActionItem)
				
		GameState.Set_Player(thePlayer)
				
		return exitNum
		
		
	def process_engine_action(self, engineActionItem):
		# TODO: process player move + dir rotate
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
		
