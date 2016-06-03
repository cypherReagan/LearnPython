import GothansGame
import MapDisplay
import GameData
import signal
import msvcrt
import time

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
	
def Get_Key_Input():

	retStr = ""
	
	if (not GothansGame.Is_Windows_platform()):
		# Linux implementation
		retStr = nonBlockingRawInput("Enter Action:>")
	else:
		print "Enter Action:>"
		
		inputTimeout = False
		
		while ((not msvcrt.kbhit()) and not inputTimeout):
			# do something else while we're waiting
			time.sleep(3.0)
			inputTimeout = True
			
		# clear the keyboard buffer
		inChar = ''
		while msvcrt.kbhit():
			inChar = msvcrt.getch()
			retStr += inChar
	
		print "DEBUG_JW: Get_Key_Input() - You entered %s" % retStr
		
	return retStr

	
#---------------------------------------------------
#---------------------------------------------------
# Class: MapActionItem
#
# Member Variables:	
#		cmdStr		- map manipulation command
#		targetID	- target objID in map 
#---------------------------------------------------
#---------------------------------------------------
class MapActionItem(object):

	def __init__(self, newCmdStr, newTargetID):
		self.cmdStr = newCmdStr
		self.targetID = newTargetID
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

#---------------------------------------------------
#---------------------------------------------------
# Class: MapEngine
#---------------------------------------------------
#---------------------------------------------------		
class MapEngine(object):
	
	
	__theMapDisplay = None
	__theMapCmdList = []
	
	def __init__(self, newMapStrList):
		self.update_map(newMapStrList, 0)
		
		
	def update_map(self, newMapStrList, listIndex):
		newMapStr = u""
		newMapStr = newMapStrList[listIndex]
		self.__theMapDisplay = MapDisplay.MapDisplayData(newMapStr)
		
		
	def run_map(self, thePlayer):
	
		done = False
		
		# DEBUG_JW: this is a hack for now!
		playerID = self.__theMapDisplay.get_ID(GameData.MAP_CAT_PLAYER)
		
		while (not done):
			# clear all old map actions
			del self.__theMapCmdList[:]
			
			# update user display
			#GothansGame.Clear_Screen()
			self.print_map_str()
			
			# TODO: 
			# use separate thread for keyboard input
			# https://bytes.com/topic/python/answers/43936-canceling-interrupting-raw_input
			
			# OR non-blocking raw_input()
			# http://www.garyrobinson.net/2009/10/non-blocking-raw_input-for-python.html
			
			# OR msvcrt module
			# http://effbot.org/librarybook/msvcrt.htm
			
			answer = Get_Key_Input()
			#answer = nonBlockingRawInput("Enter Action:>")
			
			isGoodInput = False
			
			if (answer == GameData.MAP_CMD_STR_PAUSE):
				raw_input("****** GAME PAUSED ******\n%s" % GothansGame.PROMPT_CONTINUE_STR)
			else:
			
				if (answer in GameData.MAP_CMD_STR_LIST):
					isGoodInput = True
					
					if (answer == GameData.MAP_CMD_STR_QUIT):
						done = True
				else:
					print GameData.INVALID_ENTRY_RSP
				
			if (isGoodInput and not done):
				# construct player move
				playerAction = MapActionItem(answer, playerID)
				self.__theMapCmdList.append(playerAction)
			
				# get enemy AI input
				
				# construct enemy moves
			
				# send actionList to map
				for cmdItem in self.__theMapCmdList:
					self.__theMapDisplay.process_map_cmd(cmdItem.cmdStr, cmdItem.targetID)
				
				
		return thePlayer
		
		
	def print_map_str(self):
		mapStr = u"%s" % self.__theMapDisplay.get_map()
		print mapStr