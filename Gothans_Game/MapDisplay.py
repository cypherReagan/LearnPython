import GameData
import GameEngine
import Utils


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
		
	def get_str(self):
		retStr = "(%d, %d)" % (self.xPos, self.yPos)
		
		return retStr

#---------------------------------------------------
#---------------------------------------------------
# Class: MapTile
#
# Member Variables:	
#		pos			- map coordinates
#		dir			- direction in which map obj faces
#		category	- category for map obj
#		tileChar	- char representing map obj
#		objID		- unique identifier for tile
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
# Class: NumGenerator
#
# Member Variables:	
#		__counter - tracks the last assigned number
#---------------------------------------------------
#---------------------------------------------------
class NumGenerator(object):

	def __init__(self, startVal):
		self.reset(startVal)
		
	def reset(self, startVal):
		self.__counter = startVal
	
	def get_num(self):
		retVal = self.__counter
		self.__counter += 1
		
		return retVal
		
	
#---------------------------------------------------
#---------------------------------------------------
# Class: MapContainer
#
# Member Variables:	
#		__tileList		- list of all tiles in display map
#		__idGen			- objID generator
#		
#---------------------------------------------------
#---------------------------------------------------
		
class MapContainer(object):
	
	def __init__(self, mapStr):
		self.__idGen = NumGenerator(0)
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
		
		#print "DEBUG_JW: MapContainer.__tileList len = %d" % len(self.__tileList)
		
		for mapItem in self.__tileList:
			mapStr += mapItem.tileChar
			
		return mapStr
		
		
	def dump_map_data(self, mapIndex):
		# TODO: implement mapIndex dump
		
		print "###### MAP %d DATA ######" % mapIndex
		
		for mapItem in self.__tileList:
			print "\'%s\' , category = %d, ID = %d at (%d, %d)" % (mapItem.tileChar, mapItem.category, mapItem.objID, mapItem.pos.xPos, mapItem.pos.yPos)
		
		raw_input(GameData.PROMPT_CONTINUE_STR)
		
	@staticmethod
	def get_category_from_char(mapChar):
		
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
		
	# Get mapChar based on tile category.
	# Returns empty char if mapChar cannot be calculated.
	def get_char_from_category(self, mapTileCategory, charIndex=GameData.INVALID_INDEX):
	
		mapChar = ''
			
		if ((mapTileCategory >= 0) and (mapTileCategory < len(GameData.MAP_CHARS_LIST))):
		
			itemList = GameData.MAP_CHARS_LIST[mapTileCategory]
			
			if (charIndex == GameData.INVALID_INDEX):
				# caller did not provide list index so default to the 1st list entry
				charIndex = 0
			
			if (len(itemList) > charIndex):
				mapChar = itemList[charIndex]
		
		return mapChar
			
	# Creates tile obj from map data
	# Post-Cond: __exitPosList updated with any map exit positions
	def make_tile(self, xVal, yVal, newChar):
		
		mapTile = None
		
		category = self.get_category_from_char(newChar)
		
		if (category == GameData.INVALID_INDEX):
			Utils.Show_Game_Error("Invalid character for map tile construction: \"%s\" (%d, %d)." % (newChar, xVal, yVal))
		else:
			mapPos = MapPos(xVal, yVal)
			objID = self.__idGen.get_num() # use unique ID
			mapTile = MapTile(mapPos, GameData.DIR_INVALID, category, newChar, objID)
			
			dbg_showCreation = False
			
			if (dbg_showCreation):
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
		
	# Get map tile based on position.
	# Returns None if error
	def get_tile_from_Pos(self, pos):
	
		retTile = None
		
		tileIndex = self.get_tileIndex_from_Pos(pos)
		
		if (tileIndex != GameData.INVALID_INDEX):
			retTile = self.__tileList[tileIndex]
		
		return retTile
	
		
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
			
			
	def get_obj_mapID_list(self, objCategory):
		retIdList = []
		
		for mapItem in self.__tileList:
			if (mapItem.category == objCategory):
				retIdList.append(mapItem.objID)
		
		return retIdList
		
	
	def get_target_tile_from_Dir(self, objID, objDir):
	
		retTile = None
		retTileIndex = GameData.INVALID_INDEX
		
		currentTileIndex = self.get_tileIndex_from_ID(objID)
		
		if (currentTileIndex == GameData.INVALID_INDEX):
			Utils.Show_Game_Error("MapDisplay::get_target_tile_from_Dir() - invalid objID %d!" % objID)
		else:
			currentTile = self.__tileList[currentTileIndex]
			currentPos = currentTile.pos
			
			targetPos = MapPos(currentPos.xPos, currentPos.yPos) # get new instance to avoid copy-by-reference
			isGoodDir = True
			
			if (objDir == GameData.DIR_NORTH):
				targetPos.yPos -= 1 # y-axis is inverted in map str
			elif (objDir == GameData.DIR_WEST):
				targetPos.xPos -= 1
			elif (objDir == GameData.DIR_SOUTH):
				targetPos.yPos += 1 # y-axis is inverted in map str
			elif (objDir == GameData.DIR_EAST):
				targetPos.xPos += 1
			else:
				isGoodDir = False
			
			if (not isGoodDir):
				Utils.Show_Game_Error("MapDisplay::get_target_tile_from_Dir() - invalid objDir %s!" % objDir)
			else:
				targetTileIndex = self.get_tileIndex_from_Pos(targetPos)
				
				if (targetTileIndex == GameData.INVALID_INDEX):
					Utils.Show_Game_Error("MapDisplay::get_target_tile_from_Dir() - invalid target position (%d, %d)!" % (targetPos.xPos, targetPos.yPos))
				else:
					# get target
					retTile = self.__tileList[targetTileIndex]
					retTileIndex = targetTileIndex
					
		return retTile, retTileIndex
	
	# TODO: Remove
	def process_map_cmd(self, mapActionItem):
		
		retActionItem = None
		
		if (mapActionItem != None):
			Utils.Log_Event("Map Display receiving cmd - %s" % mapActionItem.dump_data())
		
			if (mapActionItem.cmdStr == GameData.MAP_CMD_STR_MOVE):
				self.move_map_item(mapActionItem.objID, mapActionItem.dir)
			elif(mapActionItem.cmdStr == GameData.MAP_CMD_STR_DUMP_DATA):
				self.dump_map_data()
			elif(mapActionItem.cmdStr == GameData.MAP_CMD_STR_USE):
				retActionItem = self.use_map_item(mapActionItem.objID, mapActionItem.dir)
			elif(mapActionItem.cmdStr == GameData.MAP_CMD_STR_PLACE_ENTITY):
				retActionItem = self.place_entity_map_item(mapActionItem.entityType, mapActionItem.entityPos)
			else:
				pass
			
		return retActionItem
	
	
	def move_map_item(self, objID, objDir):
	
		targetTile, targetTileIndex = self.get_target_tile_from_Dir(objID, objDir)
			
		if (targetTile != None):
			currentTileIndex = self.get_tileIndex_from_ID(objID)
			
			if (currentTileIndex == GameData.INVALID_INDEX):
				# should never get here since currentTileIndex was already used to calculate targetTile
				Utils.Show_Game_Error("MapDisplay::move_map_item() - invalid objID %d!" % objID)
			else:
				if (targetTile.category == GameData.MAP_CAT_OPEN_SPACE):
					# this is a valid move so proceed with swap
					self.swap_tiles_in_List(currentTileIndex, targetTileIndex)
					
					
	def use_map_item(self, objID, objDir):		
		retID = GameData.INVALID_INDEX
			
		targetTile, targetTileIndex = self.get_target_tile_from_Dir(objID, objDir)
			
		if (targetTile != None):
			if (targetTile.category == GameData.MAP_CAT_EXIT):
				# send back the exit obj ID for engine processing
				retID = targetTile.objID

		else:
			pass
		
		return retID 
		
		
	# Function places entity to target pos to empty tile in map
	# Returns new objID if successful placement, else INVALID_INDEX 
	def place_map_entity(self, newEntityChar, newEntityPos):		
	
		retID = GameData.INVALID_INDEX
		
		if (newEntityPos == None):
			Utils.Show_Game_Error("MapDisplay::place_map_entity() - invalid newEntityPos!")
		else:
			# determine if target tile is empty
			targetTile = self.get_tile_from_Pos(newEntityPos)
			
			if (targetTile == None):
				Utils.Show_Game_Error("MapDisplay::place_map_entity() - could not get targetTile from position = %s" % newEntityPos.get_str())
			else:
			
				newEntityCategory = self.get_category_from_char(newEntityChar)
				
				if (newEntityCategory == GameData.INVALID_INDEX):
					Utils.Show_Game_Error("MapDisplay::place_map_entity() - invalid newEntityChar = %s" % newEntityChar)
				else:
				
					if (targetTile.category != GameData.MAP_CAT_OPEN_SPACE):
						if (newEntityChar == targetTile.tileChar):
							# placing tile that already exists so return existing ID
							retID = targetTile.objID
							Utils.Show_Game_Error("MapDisplay::place_map_entity() - duplicate placement at pos = %s" % newEntityPos.get_str()) 
					else:
						# placing entity in open space
						testStr = "DEBUG_JW (notAnError): MapDisplay::place_map_entity() - tile %s : category = %d" % (newEntityPos.get_str(), targetTile.category)
						Utils.Show_Game_Error(testStr) 
					
						# free to place entity
						newTile = self.make_tile(newEntityPos.xPos, newEntityPos.yPos, newEntityChar)
						
						if (newTile == None):
							Utils.Show_Game_Error("MapDisplay::place_map_entity() - could not get newTile from position vals = (%d, %d)" % (newEntityPos.xPos, newEntityPos.yPos))
						else:
							# find out where to insert the new entity
							tileIndex = self.get_tileIndex_from_Pos(newEntityPos)
							
							if (tileIndex == GameData.INVALID_INDEX):
								Utils.Show_Game_Error("MapDisplay::place_map_entity() - could not get tileIndex from pos = %d" % newEntityPos.get_str())
							else:
								# insert entity into map and return actionItem listing the new entity ID
								newTile.objID = self.__idGen.get_num()
								self.__tileList[tileIndex] = newTile
								retID = newTile.objID
													
		return retID

	
		
		
		
		
		
		
		
		
		
		
		
