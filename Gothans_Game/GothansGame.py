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
		pass
		
	def play(self):
		print "Gothans have invaded your spaceship... time to blow this baby and escape to the planet below!\n\n"


#---------------------------------------------------
#---------------------------------------------------
# Class: Scene
#
# NOTE: This is the base class for all scenes
#---------------------------------------------------
#---------------------------------------------------
class Scene(object):
	
	def enter(self):
		pass		
		
class Death(Scene):
	
	def enter(self):
		print "You died in a hilarious way!"
		#TODO: implement start over
		print "Do you want to play again?"
		pass
		

class CentralCorridor(Scene):
	
	def enter(self):
		print 
		"""
			This is the Central Corridor. A Gothan stands before you.
			You must defeat him with a joke before proceeding.
		"""
		pass
		
		
class Armory(Scene):
	
	def enter(self):
		print 
		"""
			This is the Laser Weapon Armory. This is where you get the neutron bomb. 
			It must be placed on the bridge to blow up the ship.
			You must guess the keypad code to obtain the bomb.
		"""
		pass
		
		
class Bridge(Scene):
	
	def enter(self):
		print 
		"""
			This is the Bridge. A Gothan stands in your way. You must defeat him in]
			order to set the bomb and attempt to escape.
		"""
		pass
		
		
class EscapePod(Scene):
	
	def enter(self):
		print 
		"""
			This is the Escape Pod Bay. You must guess the correct escape pod in order to leave.
		"""
		pass
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: Map
#
# Member Variables:	
#		currentScene - contains the current map state
#---------------------------------------------------
#---------------------------------------------------
		
class Map(object):
	
	def __init__(self, startScene):
		pass
		
	def nextScene(self, sceneName):
		pass
		
	def openingScene(self):
		pass
		
		
# simple test
aMap = Map('central corridor')
aGame = Engine(aMap)
aGame.play()