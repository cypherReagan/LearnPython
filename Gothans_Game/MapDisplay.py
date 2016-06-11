import GothansGame
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
	
	def __init__(self, newPos=None, newDir=GameData.INVALID_INDEX, newCategory=GameData.INVALID_INDEX, newTileChar='', newObjID=GameData.INVALID_INDEX):
		self.pos = newPos
		self.dir = newDir
		self.category = newCategory
		self.tileChar = newTileChar
		self.objID = newObjID
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
				yVal += 1
				xVal = 0
			else:
				xVal += 1
				
		
		
	def get_map(self):
		
		mapStr = ""
		
		#print "DEBUG_JW: MapDisplayData.__tileList len = %d" % len(self.__tileList)
		
		for mapItem in self.__tileList:
			mapStr += mapItem.tileChar
			
		return mapStr
		
		
	def dump_map_data(self):
		
		print "###### MAP DATA ######"
		
		for mapItem in self.__tileList:
			print "\'%s\' , category = %d, ID = %d at (%d, %d)" % (mapItem.tileChar, mapItem.category, mapItem.objID, mapItem.pos.xPos, mapItem.pos.yPos)
		
	def get_category_from_char(self, mapChar):
		
		mapCategory = 0 # categories are 0-based
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
			
		return mapCategory
			
		
	def make_tile(self, xVal, yVal, newChar):
		
		mapTile = None
		
		category = self.get_category_from_char(newChar)
		
		if (category == GameData.INVALID_INDEX):
			Utils.Show_Game_Error("Invalid character for map tile construction: \"%s\" (%d, %d)." % (newChar, xVal, yVal))
		else:
			mapPos = MapPos(xVal, yVal)
			objID = len (self.__tileList) # use list index as unique ID
			mapTile = MapTile(mapPos, GameData.DIR_INVALID, category, newChar, objID)
			
			print "DEBUG_JW: make_tile() - \'%s\' , category = %d, ID = %d at (%d, %d)" % (newChar, category, objID, mapPos.xPos, mapPos.yPos)
		
		return mapTile
		
	def get_tileIndex_from_ID(self, objID):
		retIndex = GameData.INVALID_INDEX
		count = 0
		
		for mapItem in self.__tileList:
			if (mapItem.objID == objID):
				retIndex = count
				break
			else:
				count += 1
		
		return retIndex
		
		
	def get_tileIndex_from_Pos(self, pos):
		retIndex = GameData.INVALID_INDEX
		count = 0
		
		for mapItem in self.__tileList:
			if ((mapItem.pos.xPos == pos.xPos) and (mapItem.pos.yPos == pos.yPos)):
				retIndex = count
				break
			else:
				count += 1
		
		return retIndex
		
	# Swaps tile data while preserving position data.
	def swap_tiles_in_List(self, index1, index2):
		listLen = len(self.__tileList)
		
		if ((index1 > listLen) or (index2 > listLen)):
			Utils.Show_Game_Error("DEBUG_JW: swap_tiles_in_List() - invalid indices %d and %d!" % (index1, index2))
		else:
			tmpTile = MapTile() # get new insance to avoid copy-by-reference
			
			tmpTile.dir = self.__tileList[index1].dir
			tmpTile.category = self.__tileList[index1].category
			tmpTile.tileChar = self.__tileList[index1].tileChar
			tmpTile.objID = self.__tileList[index1].objID
			
			#print u"DEBUG_JW: swap_tiles_in_List() - tmpTileChar = %s, srcTileChar = %s (%d, %d), destTileChar = %s (%d, %d)" % (tmpTile.tileChar, self.__tileList[index1].tileChar, self.__tileList[index1].pos.xPos, self.__tileList[index1].pos.yPos, self.__tileList[index2].tileChar, self.__tileList[index2].pos.xPos, self.__tileList[index2].pos.yPos)
			
			self.__tileList[index1].dir = self.__tileList[index2].dir
			self.__tileList[index1].category = self.__tileList[index2].category
			self.__tileList[index1].tileChar = self.__tileList[index2].tileChar
			self.__tileList[index1].objID = self.__tileList[index2].objID
			
			#print u"DEBUG_JW: swap_tiles_in_List() - tmpTileChar = %s, srcTileChar = %s (%d, %d), destTileChar = %s (%d, %d)" % (tmpTile.tileChar, self.__tileList[index1].tileChar, self.__tileList[index1].pos.xPos, self.__tileList[index1].pos.yPos, self.__tileList[index2].tileChar, self.__tileList[index2].pos.xPos, self.__tileList[index2].pos.yPos)
			
			self.__tileList[index2].dir = tmpTile.dir
			self.__tileList[index2].category = tmpTile.category
			self.__tileList[index2].tileChar = tmpTile.tileChar
			self.__tileList[index2].objID = tmpTile.objID
			
			
	def get_ID(self, objCategory):
		retID = GameData.INVALID_INDEX
		count = 0
		
		for mapItem in self.__tileList:
			if (mapItem.category == objCategory):
				retID = mapItem.objID
				break
		
		return retID
		
	def process_map_cmd(self, cmdStr, objID):
		if ((cmdStr == GameData.MAP_CMD_STR_MOVE_NORTH) or (cmdStr == GameData.MAP_CMD_STR_MOVE_EAST) or (cmdStr == GameData.MAP_CMD_STR_MOVE_SOUTH) or (cmdStr == GameData.MAP_CMD_STR_MOVE_WEST)):
			self.move_map_item(cmdStr, objID)
		elif(cmdStr == GameData.MAP_CMD_DUMP_DATA):
			self.dump_map_data()
		else:
			pass
	
	
	def move_map_item(self, cmdStr, objID):
		currentTileIndex = self.get_tileIndex_from_ID(objID)
		
		if (currentTileIndex == GameData.INVALID_INDEX):
			Utils.Show_Game_Error("move_map_item() - invalid objID %d!" % objID)
		else:
			currentTile = self.__tileList[currentTileIndex]
			currentPos = currentTile.pos
			
			#print "DEBUG_JW: move_map_item() - objID = %d, map ID = %d (%d, %d)" % (objID, currentTile.objID, currentPos.xPos, currentPos.yPos)
			
			targetPos = MapPos(currentPos.xPos, currentPos.yPos) # get new instance to avoid copy-by-reference
			isGoodCmd = True
			
			if (cmdStr == GameData.MAP_CMD_STR_MOVE_NORTH):
				targetPos.yPos -= 1 # y-axis is inverted in map str
			elif (cmdStr == GameData.MAP_CMD_STR_MOVE_WEST):
				targetPos.xPos -= 1
			elif (cmdStr == GameData.MAP_CMD_STR_MOVE_SOUTH):
				targetPos.yPos += 1 # y-axis is inverted in map str
			elif (cmdStr == GameData.MAP_CMD_STR_MOVE_EAST):
				targetPos.xPos += 1
			else:
				Utils.Show_Game_Error("move_map_item() - invalid cmdStr %s!" % cmdStr)
				isGoodCmd = False
				
			if (isGoodCmd):
				targetTileIndex = self.get_tileIndex_from_Pos(targetPos)
				
				#print "DEBUG_JW: move_map_item() - isGoodCmd. targetTileIndex =  %d" % targetTileIndex
				
				if (targetTileIndex == GameData.INVALID_INDEX):
					Utils.Show_Game_Error("move_map_item() - invalid target position (%d, %d)!" % (targetPos.xPos, targetPos.yPos))
				else:
					targetTile = self.__tileList[targetTileIndex]
					
					#print "DEBUG_JW: move_map_item() - targetTile.category = %d at (%d, %d)" % (targetTile.category, targetPos.xPos, targetPos.yPos)
					
					if (targetTile.category == GameData.MAP_CAT_OPEN_SPACE):
						# this is a valid move so proceed with swap
						# TODO: force current tile dir to co=md dir
						#print "DEBUG_JW: move_map_item() - swapping tile %d with tile %d" % (currentTileIndex, targetTileIndex)
						self.swap_tiles_in_List(currentTileIndex, targetTileIndex)
					else:
						pass #print "DEBUG_JW: target tile is not open. Target Tile Category = %d" % targetTile.category
					
					