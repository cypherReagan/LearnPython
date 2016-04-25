import GameData


#---------------------------------------------------
#---------------------------------------------------
# Class: MapPos
#
# Member Variables:	
#		xPos		- map x-coordinate
#		yPos		- map y-coordinate
#---------------------------------------------------
#---------------------------------------------------
class MapPos(object):

	def __init__(self, newXVal, newYVal):
		self.xPos = newXVal
		self.yPos = newYVal

#---------------------------------------------------
#---------------------------------------------------
# Class: MapTile
#
# Member Variables:	
#		pos			- map coordinates
#		dir			- direction in which map obj faces
#		category	- category for map obj
#		tileChar	- char representing map obj
#---------------------------------------------------
#---------------------------------------------------
		
class MapTile(object):
	
	def __init__(self, newPos, newDir, newCategory, newTileChar):
		self.pos = newPos
		self.dir = newDir
		self.category = newCategory
		self.tileChar = newTileChar
		self.objID = GameData.INVALID_INDEX
		# TODO: add color attribute if desired

		
	
#---------------------------------------------------
#---------------------------------------------------
# Class: MapDisplayData
#
# Member Variables:	
#		__tileList		- list of all tiles in display map
#		
#---------------------------------------------------
#---------------------------------------------------
		
class MapDisplayData(object):
	
	def __init__(self, mapStr):
		self.set_map_str(mapStr)
		
		
	# Funtion takes raw map string and creates  
	# map tiles for display data.
	#
	# Post-Cond: __tileList updated with new tiles
	def set_map_str(self, mapStr):
	
		self.__tileList = []
	
		xVal = 0
		yVal = 0
		strPos = 0
		strLen = len(mapStr)
		
		while (strPos < strLen):
			newChar = mapStr[strPos]
			strPos += 1
			
			newMapTile = self.make_tile(xVal, yVal, newChar)
			self.__tileList.append(newMapTile)
			
			if (newChar == GameData.MAP_CHAR_LINE_FEED):
				xVal += 1
				yVal = 0
			else:
				yVal += 1
				
		
		
	def get_map(self):
		
		mapStr = ""
		
		print "DEBUG_JW: MapDisplayData.__tileList len = %d" % len(self.__tileList)
		
		for mapItem in self.__tileList:
			mapStr += mapItem.tileChar
			
		return mapStr
		
		
	def get_category_from_char(self, mapChar):
		
		mapCategory = 0
		foundMatch = False
		
		for itemList in GameData.MAP_CHARS_LIST:
			if (mapChar in itemList):
				# done looking
				foundMatch = True
				break
			else:
				mapCategory += 1
				
		if (not foundMatch):
			mapCategory = GameData.INVALID_INDEX
			
		
	def make_tile(self, xVal, yVal, newChar):
		
			mapTile = None
			
			category = self.get_category_from_char(newChar)
			
			if (category == GameData.INVALID_INDEX):
				Show_Game_Error("Invalid character for map tile construction: \"%s\"." % newChar)
			else:
				mapPos = MapPos(xVal, yVal)
				mapTile = MapTile(mapPos, GameData.DIR_INVALID, category, newChar)
			
			return mapTile
			