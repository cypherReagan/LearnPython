# This Python file uses the following encoding: utf-8

# Name				: GothansGame.py
# Author			: JWalker
# Created			: 17th September 2015
# Version			: 1.0
# Runtime			: Python27

# Implementation of Gothans Attack

# Concept from Learn Python the Hard Way ex43
import os
import GameEngine as Engine
import GameData
import GameState
import Utils
import Scene


		
			
if __name__ == '__main__':	
	# Start here when this file is being run directly (rather than being imported).
	
	# Housekeeping items
	gameLogFileStr = os.getcwd() + '\\' + GameData.GAME_LOG_STR
	Utils.Init_Game_Log(gameLogFileStr)
	goodState = GameState.Init()
	
	if (not goodState):
		Utils.Exit_Game()
	else:
		# => Start the game
		Utils.Log_Event("Game start")
		aMap = Scene.SceneMap(GameData.START_KEY) # pass in the key for the starting scene
		aGame = Engine.SceneEngine(aMap)
		
		aGame.play()
	
	
	
	
	
	
	
