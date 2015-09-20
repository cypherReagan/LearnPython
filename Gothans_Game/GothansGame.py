# Name				: GothansGame.py
# Author			: Jonathan Walker
# Created			: 17th September 2015
# Version			: 1.0

# Implementation of Gothans from the Planet Percal #25

# Concept from Learn Python the Hard Way ex43

import random

		
		
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
		print "Gothans have invaded your spaceship... time to blow this baby and escape to the planet below!\n\n"
		# need while-loop here to drive game
		result = self.sceneMap.openingScene()
		
		while (result != 'done'):
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
		retScene = 'armory'
		print "You died in a hilarious way!"
		#TODO: implement start over
		print "Do you want to play again?"
		
		return retScene
		pass
		

class CentralCorridor(Scene):
	
	def enter(self):
		retScene = 'armory'
		print " This is the Central Corridor. A Gothan stands before you. You must defeat him with a joke before proceeding."
		
		return retScene
		pass
		
		
class Armory(Scene):
	
	def enter(self):
		retScene = 'bridge'
		print "This is the Laser Weapon Armory. This is where you get the neutron bomb."
		print "It must be placed on the bridge to blow up the ship. You must guess the keypad code to obtain the bomb."
		
		return retScene
		pass
		
		
class Bridge(Scene):
	
	def enter(self):
		retScene = 'escape pod'
		print "This is the Bridge. A Gothan stands in your way."
		print "You must defeat him in order to set the bomb and attempt to escape."
		
		return retScene
		pass
		
		
class EscapePod(Scene):
	
	def enter(self):
		retScene = 'done'
		print "This is the Escape Pod Bay. You must guess the correct escape pod in order to leave."
		
		return retScene
		pass
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: Map
#
# Member Variables:	
#		sceneDict		- dictionary of all game scenes
#---------------------------------------------------
#---------------------------------------------------
		
class Map(object):
	
	def __init__(self, startScene):
	
		# declare dict for all scenes
		corridorScene = CentralCorridor()
		armoryScene = Armory()
		bridgeScene = Bridge() 
		escapeScene = EscapePod()
		deathScene = Death()
		
		self.sceneDict = {	'central corridor'	: corridorScene,
							'armory' 			: armoryScene,
							'bridge'			: bridgeScene,
							'escape pod'		: escapeScene,
							'death'				: deathScene	}
					 
		self.firstScene = startScene
		
		
	def nextScene(self, sceneName):
		# run the next scene and save off the result
		retScene = ''
		theNextScene = self.sceneDict.get(sceneName)
		
		if (not theNextScene):
			print "ERROR: Map::nextScene() - invalid key %s" % sceneName
		else:
			retScene = theNextScene.enter()
		
		return retScene
		
		
	def openingScene(self):
		return self.nextScene(self.firstScene)
		
		
# simple test
aMap = Map('central corridor') # pass in the key for the starting scene
aGame = Engine(aMap)
aGame.play()