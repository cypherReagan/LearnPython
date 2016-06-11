# This Python file uses the following encoding: utf-8

from sys import exit
import os
import platform
import datetime
import GothansGame
import GameData

__GameLog = None

# Sets up the global GameLog for logging
def Init_Game_Log(fileNameStr):
	global __GameLog

	if (__GameLog != None):
		# gracefully clear current log before starting a new one
		__GameLog.close()
		__GameLog = None
	
	__GameLog = EventLog(fileNameStr)
	

# Write to global GameLog
def Log_Event(logStr):
	global __GameLog
	
	if (__GameLog != None):
		__GameLog.write(logStr)
	else:
		Show_Game_Error("Could not log event...")
		

# Utility function to clear shell
def Clear_Screen():
		
	if (not GameData.DEBUG_MODE):
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
def Exit_Game(thePlayer):
	global __GameLog 
	
	if (__GameLog != None):
		__GameLog.close()
	Clear_Screen()
	print "%s\nFINAL SCORE: %d\n\n%s\n%s" % (GameData.Separator_Line, thePlayer.xp, GameData.GameOverMsg, GameData.Separator_Line)
	exit(1)
	
	
def Show_Game_Error(errMsgStr):
	
	errMsgStr = "GAME ERROR: " + errMsgStr
	errorSeparator = '************************************************************'
	
	printMsgStr = "%s\n***  %s  ***\n%s\n%s\n" % (errorSeparator, errMsgStr, errorSeparator, GameData.PROMPT_CONTINUE_STR)
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
		
		print GameData.Separator_Line
		print "GAME COMMANDS:\n"

		for entry in GameData.CMD_STR_LIST:
			isDbgPrint = False
			if (GameData.DEBUG_MODE):
				isDbgPrint = True
				
			if (isDbgPrint or (GameData.CHEAT_CMD_STR not in entry)):
				print entry
		
		print GameData.Separator_Line
	
	elif (userCmdStr == GameData.QUIT_CMD_STR):
		print "Are you sure want to quit?"
		answer = raw_input("(y/n)> ")
		
		if (answer.lower() == 'y'):
			Exit_Game(thePlayer)
	
	elif (userCmdStr == GameData.PLAYER_STATS_CMD_STR):
		thePlayer.print_stats()
		
	elif (userCmdStr == GameData.PLAYER_INV_CMD_STR):
		thePlayer.theInventoryMgr.print_items()
		
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
				theItem = GothansGame.UtilityItem(itemAnswer, 1)
				isGoodItem = True
				
			elif (typeAnswer == "w"):
				# weapon item
				itemAnswer = raw_input("(Enter item name) > ")
				theItem = GothansGame.WeaponItem(itemAnswer, INFINITE_VAL)
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
				# TODO - put removal process inside theInventoryMgr
				theItem = thePlayer.theInventoryMgr.get_item(itemAnswer)
				
				if (theItem != None):
					theItem.subtract_count(1)
					thePlayer.theInventoryMgr.update_item(theItem)
					done = True
				else:
					print "Please enter valid item name!"
		
	elif (userCmdStr == GameData.DEBUG_MODE_TOGGLE_CMD_STR):
		global DEBUG_MODE #TODO - fix warning generated here
		
		if (not GameData.DEBUG_MODE):
			DEBUG_MODE = True
			print "DEBUG_MODE = True"
		else:
			GameData.DEBUG_MODE = False
			print "DEBUG_MODE = False"

	else:
		retVal = False

		
	return retVal, thePlayer
	
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

	def __init__(self, fileNameStr=""):
	
		if (fileNameStr != ""):
			self.open_for_write(fileNameStr)
		
	# Sets up LogFile for event writes. 
	# Assumes file is not already open.
	def open_for_write(self, fileNameStr):
		
		try:
			# clear any existing txt
			self.__LogFile = None 
			open(fileNameStr, 'w').close()
			
			# start new log file session
			self.__LogFile = open(fileNameStr, 'w')
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
	
	
	
	