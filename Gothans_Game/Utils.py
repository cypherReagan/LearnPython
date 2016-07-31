# This Python file uses the following encoding: utf-8

from sys import exit
import os
import platform
import datetime
import GothansGame
import GameData
import GameState
import Entity
import signal
import msvcrt
import time	

# Globals because we need to log events from anywhere in the game
__GameLog = None
__MapLog = None # Global because we need to log map events from anywhere in the game

# Sets up the global GameLog for logging
def Init_Game_Log(fileNameStr, initMsgStr=""):
	global __GameLog

	if (__GameLog != None):
		# gracefully clear current log before starting a new one
		__GameLog.close()
		__GameLog = None
	
	__GameLog = EventLog(fileNameStr, initMsgStr)
	
# Sets up the global MapLog for logging
def Init_Map_Log(theMapLog=None):
	global __MapLog
	
	if (theMapLog == None):
		__MapLog = MapLog()
	else:
		__MapLog = theMapLog # use reference from some local map engine

# Write to global GameLog
def Log_Event(logStr):
	global __GameLog
	
	if (__GameLog != None):
		__GameLog.write(logStr)
	else:
		Show_Game_Error("Could not log event...")
		
def Write_Map_Log(logStr):
	global __MapLog
	
	if (__MapLog != None):
		__MapLog.add(logStr)
	
def Print_Map_Log():
	global __GameLog
	
	if (__MapLog != None):
		__MapLog.print_events()
	
	
# Utility function to clear shell
def Clear_Screen():
		
	if (Is_Windows_platform()):
		os.system('cls')
	else:
		os.system('clear') # Linux/Mac OS
			
# Query O/S platform
def Is_Windows_platform():
	retVal = False
	
	if (platform.system() == 'Windows'):
		retVal = True
		
	return retVal
	
# Gracefully exit the game
def Exit_Game():
	global __GameLog 
	
	Log_Event("Exiting Game")
	
	thePlayer = GameState.Get_Player()
	
	if (__GameLog != None):
		__GameLog.close()
	Clear_Screen()
	print "%s\nFINAL SCORE: %d\n\n%s\n%s" % (GameData.SEPARATOR_LINE_STR, thePlayer.xp, GameData.GameOverMsg, GameData.SEPARATOR_LINE_STR)
	exit(1)
	
	
def Show_Game_Error(errMsgStr):
	
	errMsgStr = "GAME ERROR: " + errMsgStr
	errorSeparator = '************************************************************'
	
	printMsgStr = "%s\n***  %s  ***\n%s\n%s\n" % (errorSeparator, errMsgStr, errorSeparator, GameData.PROMPT_CONTINUE_STR)
	Log_Event("\n" + printMsgStr)
	raw_input(printMsgStr)	
	
	
# Utility function to ask user for game command
def Prompt_User_Action(thePlayer):
	answer = ''
	done = False
	
	while (not done):
		answer = raw_input("[Action]> ")
		answer = answer.lower()
		
		if answer in GameData.CMD_STR_LIST:
			# we have a good command
			isCmdHandled, thePlayer = Process_Common_Actions(answer, thePlayer)
			
			if (not isCmdHandled):
				# not a common command so let caller handle this one
				done = True
		else:
			print GameData.INVALID_ENTRY_RSP
				
	return answer, thePlayer
	
# Process any common user commands.
# Returns True if command is handled, else False
def Process_Common_Actions(userCmdStr, thePlayer):

	retVal = True
	
	if (userCmdStr == GameData.HELP_REQ_CMD_STR):
		
		print GameData.SEPARATOR_LINE_STR
		print "GAME COMMANDS:\n"

		for entry in GameData.CMD_STR_LIST:
			isDbgPrint = False
			if (GameData.DEBUG_MODE):
				isDbgPrint = True
				
			if (isDbgPrint or (GameData.CHEAT_CMD_STR not in entry)):
				print entry
		
		print GameData.SEPARATOR_LINE_STR
	
	elif (userCmdStr == GameData.QUIT_CMD_STR):
		print "Are you sure want to quit?"
		answer = raw_input("(y/n)> ")
		
		if (answer.lower() == 'y'):
			GameState.Set_Player(thePlayer)
			Exit_Game()
	
	elif (userCmdStr == GameData.PLAYER_STATS_CMD_STR):
		thePlayer.print_stats()
		
	elif (userCmdStr == GameData.PLAYER_INV_CMD_STR):
		thePlayer.theInventoryMgr.print_items()
		
		# give user option to equip inventory item from this menu
		print "Press Enter to exit, otherwise enter item number to equip"
		
		try:
			answerNum = int(raw_input("Input>"))
		except:
			answerNum = GameData.INVALID_INDEX
		
		if (answerNum != GameData.INVALID_INDEX):
			thePlayer = Equip_Player_From_Cmd(answerNum,  thePlayer)
		
	elif (userCmdStr == GameData.FULL_HEALTH_CHEAT_CMD_STR):
		thePlayer.set_health(100)
		
	elif (userCmdStr == GameData.SET_HEALTH_CHEAT_CMD_STR):
		
		done = False
		
		while (not done):
			try:
				answerNum = int(raw_input("(Enter new health value) > "))
		
				thePlayer.set_health(answerNum)
				done = True
			except:
				print "Please enter a valid number!"
				
	elif (userCmdStr == GameData.ADD_ITEM_CHEAT_CMD_STR):
		
		done = False
		
		while (not done):
			typeAnswer = raw_input("(Enter item type (u/w/q)) > ")
			
			theItem = None
			isGoodItem = False
			
			if (typeAnswer == "u"):
				# utility item
				itemAnswer = raw_input("(Enter item name) > ")
				theItem = Entity.UtilityItem(itemAnswer, 1)
				isGoodItem = True
				
			elif (typeAnswer == "w"):
				# weapon item
				itemAnswer = raw_input("(Enter item name) > ")
				theItem = Entity.WeaponItem(itemAnswer, GameData.INFINITE_VAL)
				isGoodItem = True
				
			elif (typeAnswer == "q"):
				# quit
				done = True
			else:
				print "Please enter a valid item type!"
			
			if (isGoodItem):
				try:			
					itemCount = int(raw_input("(Count) > "))
					
					if (theItem == None):
						print "DEBUG_JW: Invalid Item!"
					
					theItem.set_count(itemCount)
					
					isGoodItem = thePlayer.theInventoryMgr.add_item(theItem) 

					if (isGoodItem):
						done = True
				except:
					print "Please enter a valid number!"
					
	elif (userCmdStr == GameData.DELETE_ITEM_CHEAT_CMD_STR):
		
		done = False
		
		while (not done):
		
			itemAnswer = raw_input("(Enter item name) > ")
			
			if (itemAnswer == 'q'):
				done = True
			else:
				# TODO: put removal process inside theInventoryMgr
				theItem = thePlayer.theInventoryMgr.get_item(itemAnswer)
				
				if (theItem != None):
					theItem.subtract_count(1)
					thePlayer.theInventoryMgr.update_item(theItem)
					done = True
				else:
					print "Please enter valid item name!"
		
	elif (userCmdStr == GameData.DEBUG_MODE_TOGGLE_CMD_STR):
		Toggle_DEBUG_MODE()

	else:
		# action not processed
		retVal = False

		
	return retVal, thePlayer
	# end Process_Common_Actions()
	
	
def Toggle_DEBUG_MODE():
	global DEBUG_MODE #TODO: fix warning generated here
		
	msgStr = ""
	
	if (not GameData.DEBUG_MODE):
		DEBUG_MODE = True
		msgStr = "DEBUG_MODE = True"
	else:
		GameData.DEBUG_MODE = False
		msgStr = "DEBUG_MODE = False"
		
	print msgStr
	Log_Event(msgStr)	
	
	
def Equip_Player_From_Cmd(itemIndex,  thePlayer):
	# Cmd is 1-based while the item list is 0-based-> we must normalize the index
	if (itemIndex == 0):
		itemIndex = 10
	else:
		itemIndex = itemIndex - 1
	
	if (len(GameData.ITEM_STR_LIST) > itemIndex):
		itemStr = GameData.ITEM_STR_LIST[itemIndex]
		if (thePlayer.equip_item(itemStr)):
			Write_Map_Log("Equipped %s" % itemStr)
	
	return thePlayer
	
# ------------------------ Start Linux code ------------------------
# ------------------------------------------------------------------

#---------------------------------------------------
#---------------------------------------------------
# Class: AlarmException
#---------------------------------------------------
#---------------------------------------------------
class AlarmException(Exception):
# http://www.garyrobinson.net/2009/10/non-blocking-raw_input-for-python.html
	pass

def alarmHandler(signum, frame):
	raise AlarmException
	
def NonBlockingRawInput(prompt='', timeout=20):
	signal.signal(signal.SIGALRM, alarmHandler)
	signal.alarm(timeout)
	
	try:
		text = raw_input(prompt)
		signal.alarm(0)
		return text
	except AlarmException:
		print '\nPrompt timeout. Continuing...'
		
	signal.signal(signal.SIGALRM, signal.SIG_IGN)
	return ''
	
# ------------------------- End Linux code -------------------------
# ------------------------------------------------------------------
	
# Gets single char from keyboard with non-blocking input
# NOTE: Only works on Windows platform.
def Get_Key_Input(prompStr):

	retStr = ""
	
	if (not Is_Windows_platform()):
		# Linux implementation
		retStr = NonBlockingRawInput("Enter Action:>")
	else:
		print "%s" % prompStr
		
		inputTimeout = False
		
		while ((not msvcrt.kbhit()) and not inputTimeout):
			# do something else while we're waiting
			time.sleep(1.0)
			inputTimeout = True
			
		# clear the keyboard buffer
		inChar = ''
		while msvcrt.kbhit():
			inChar = msvcrt.getch()
			retStr += inChar
	
		#if (retStr != ""):
		#	print "DEBUG_JW: Get_Key_Input() - You entered %s" % retStr
		
	return retStr
	
#---------------------------------------------------
#---------------------------------------------------
# Class: EventLog
#
# DESCRIPTION:
# 	This class writes a timestamped string to external file.
#
#---------------------------------------------------
#---------------------------------------------------
class EventLog:

	__LogFile = None

	def __init__(self, fileNameStr="", initMsgStr=""):
	
		if (fileNameStr != ""):
			self.open_for_write(fileNameStr, initMsgStr)
		
	# Sets up LogFile for event writes. 
	# Assumes file is not already open.
	def open_for_write(self, fileNameStr, initMsgStr):
		
		try:
			# clear any existing txt
			self.__LogFile = None 
			open(fileNameStr, 'w').close()
			
			# start new log file session
			self.__LogFile = open(fileNameStr, 'w')
			
			# Log any initialization msg
			if (initMsgStr != ""):
				self.write(initMsgStr)
		except:
			Show_Game_Error("Could not create log file \"%s\"" % fileNameStr)
		
	# Close out the LogFile
	def close(self):
	
		if (self.__LogFile != None):
			self.__LogFile.close()
			self.__LogFile = None
		
	# Write to LogFile
	def write(self, eventStr):
		if (self.__LogFile != None):
		
			timeStampStr = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
			self.__LogFile.write(timeStampStr + "\t---\t" + eventStr + "\n")
			
			if (GameData.DEBUG_MODE):
				# pipe log to map UI
				Write_Map_Log(eventStr)
	
	
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
		
		for count in range(0, GameData.MAX_MAP_LOG_ENTRIES):
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

