# Implementation of Gothans from the Planet Percal #25

# Concept from LearnPython the Hard Way ex43

class Scene(object):
	
	def enter(self):
		pass
		
		
		
class Engine(object):
	
	def __init__(self, sceneMap):
		pass
		
	def play(self):
		print "Engine running..."
		
		
class Death(Scene):
	
	def enter(self):
		pass
		

class CentralCorridor(Scene):
	
	def enter(self):
		pass
		
		
class Armory(Scene):
	
	def enter(self):
		pass
		
		
class Bridge(Scene):
	
	def enter(self):
		pass
		
		
class EscapePod(Scene):
	
	def enter(self):
		pass
		
		
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