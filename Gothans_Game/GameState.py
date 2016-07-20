import GothansGame
import GameData


__TheGameState = None

# Sets up the global GameState
# This must be done successfully at the start of every game.
def Init():
	global __TheGameState

	retVal = True
	
	if (__TheGameState != None):
		# gracefully clear current state before starting a new one
		__TheGameState.clear()
	
	__TheGameState = StateData()
	
	if (__TheGameState == None):
		Utils.Show_Game_Error("Could not init GameState!")
		retVal = False
		
	return retVal

# Access global GameState
def Get_State():	
	global __TheGameState
	return __TheGameState
	
# Write to global GameState
def Set_State(newGameState):
	global __TheGameState
	
	if (__TheGameState != None):
		__TheGameState = newGameState # WARNING!!! This might not work with pass-by-ref
	else:
		Utils.Show_Game_Error("Could not write GameState...")
		
# Access global GameState player
def Get_Player():	
	global __TheGameState
	
	return __TheGameState.thePlayer
	
# Write to global GameState player
def Set_Player(newPlayer):
	global __TheGameState
	
	if (__TheGameState != None):
		__TheGameState.thePlayer = newPlayer # WARNING!!! This might not work with pass-by-ref
	else:
		Utils.Show_Game_Error("Could not write GameState player...")
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: StateData
#
# DESCRIPTION:
# 	This is a container for all global game state data.
#
#---------------------------------------------------
#---------------------------------------------------
class StateData(object):
	
	thePlayer = None
	
	def __init__(self):
		self.reset_state()
		
	def reset_state(self):
		self.thePlayer = GothansGame.Player()
		
	def clear(self):
		pass