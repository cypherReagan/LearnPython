# Name				: GothansGame.py
# Author			: Jonathan Walker
# Created			: 17th September 2015
# Version			: 1.0

# Implementation of Gothans from the Planet Percal #25

# Concept from Learn Python the Hard Way ex43

import random


#Globals
CORRIDOR_KEY = 'central corridor'
ARMORY_KEY = 'armory'
BRIDGE_KEY = 'bridge'
ESCAPE_POD_KEY = 'escape pod'
DEATH_KEY = 'death'
FINISH_RESULT = 'done'

		
#---------------------------------------------------
#---------------------------------------------------
# Class: Engine
#
# Member Variables:	
#		sceneMap - Map containing all available scenes
#---------------------------------------------------
#---------------------------------------------------		
class Engine(object):
	
	def __init__(self, sceneMap):
		self.sceneMap = sceneMap
		pass
		
	def play(self):
		print "------------------------------------------------"
		print "Gothans have invaded your spaceship... time to blow this baby and escape to the planet below!\n\n"
		# need while-loop here to drive game
		result = self.sceneMap.openingScene()
		
		while (result != FINISH_RESULT):
			print "DEBUG_JW: Engine::play() - result = %s" % result
			result = self.sceneMap.nextScene(result)


#---------------------------------------------------
#---------------------------------------------------
# Class: Scene
#
# NOTE: This is the base class for all scenes
#---------------------------------------------------
#---------------------------------------------------
class Scene(object):
	
	def enter(self):
		print "DEBUG_JW - Scene base class enter()"
		pass
		
class Death(Scene):
	
	def enter(self):
		retScene = 'done'
		print "You died in a hilarious way!"

		print "Do you want to play again (y/n)?"
		answer = raw_input()
		
		if (answer == 'y'):
			retScene = 'central corridor'
		
		return retScene
		pass
		

class CentralCorridor(Scene):
	
	def enter(self):
		retScene = ARMORY_KEY
		print " This is the Central Corridor. A Gothan stands before you. You must defeat him with a joke before proceeding."
		
		return retScene
		pass
		
		
class Armory(Scene):
	
	def enter(self):
		retScene = BRIDGE_KEY
		print "This is the Laser Weapon Armory. This is where you get the neutron bomb."
		print "It must be placed on the bridge to blow up the ship. You must guess the keypad code to obtain the bomb."
		
		return retScene
		pass
		
		
class Bridge(Scene):
	
	def enter(self):
		retScene = ESCAPE_POD_KEY
		print "This is the Bridge. A Gothan stands in your way."
		print "You must defeat him in order to set the bomb and attempt to escape."
		
		return retScene
		pass
		
		
class EscapePod(Scene):
	
	def enter(self):
		retScene = FINISH_RESULT
		print "This is the Escape Pod Bay. You must guess the correct escape pod in order to leave."
		
		escapeNum = '5' # TODO: implemnent random number
		answer = raw_input()
		
		if (answer == escapeNum):
			print "\n\nYou picked the correct escape pod and successfully removed yourself from a sticky situation. Good job!"
		else: 
			retScene = DEATH_KEY
		
		return retScene
		pass
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: Map
#
# Member Variables:	
#		sceneDict		- dictionary of all game scenes
#		firstScene		- key indicating starting scene
#---------------------------------------------------
#---------------------------------------------------
		
class Map(object):
	
	def __init__(self, startScene):
	
		# declare dict for all scenes
		self.sceneDict = {	CORRIDOR_KEY	: CentralCorridor(),
							ARMORY_KEY 		: Armory(),
							BRIDGE_KEY		: Bridge(),
							ESCAPE_POD_KEY	: EscapePod(),
							DEATH_KEY		: Death()	}
					 
		self.firstScene = startScene
		
		
	def nextScene(self, sceneName):
		# run the next scene and save off the result
		retScene = ''
		theNextScene = self.sceneDict.get(sceneName)
		
		if (not theNextScene):
			# should never get here
			print "ERROR: Map::nextScene() - invalid key %s" % sceneName
		else:
			retScene = theNextScene.enter()
		
		return retScene
		
		
	def openingScene(self):
		return self.nextScene(self.firstScene)
		
		
# simple test
aMap = Map(CORRIDOR_KEY) # pass in the key for the starting scene
aGame = Engine(aMap)
aGame.play()