import GothansGame
import GameData
import Utils
import copy


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
#		__layerList	- container for all layers in the tile
#---------------------------------------------------
#---------------------------------------------------
		
class MapTile(object):
	
	# static members
	__DEFAULT_LAYER = GameData.MAP_TILE_LAYER_INDEX_STAND
	
	@staticmethod
	def get_tileChar_orientation(tileChar, tileCategory):
		
		retOrientation = GameData.INVALID_INDEX
		
		if (tileCategory == GameData.MAP_CAT_WALL):
			retOrientation = MapTile.get_tileChar_orientation_from_list(tileChar, GameData.MAP_CHAR_WALL_LIST)
		elif (tileCategory == GameData.MAP_CAT_EXIT):
			retOrientation = MapTile.get_tileChar_orientation_from_list(tileChar, GameData.MAP_CHAR_EXIT_LIST)
		
		return retOrientation
		
	@staticmethod
	def get_tileChar_orientation_from_list(tileChar, tileCharList):
		
		retVal = GameData.INVALID_INDEX
		
		for count in range(0, GameData.TILE_ORIENTATION_MAX_NUM):
			if (tileCharList[count] == tileChar):
				retVal = count
				break
				
		return retVal
	
	
	def __init__(self, newPos, newLayerList):
		self.pos = newPos
		# TODO: add color attribute if desired
		# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
		# https://msdn.microsoft.com/en-us/library/mt638032?f=255&MSPPError=-2147217396
		# http://stackoverflow.com/questions/37500076/how-to-enable-windows-console-quickedit-mode-from-python
		
		
		layerListLen = len(newLayerList)
		
		if (layerListLen != GameData.MAP_TILE_LAYERS_NUM):
			Utils.Show_Game_Error("MapTile::init() - invalid layerList length!")
		else:
			self.__layerList = copy.deepcopy(newLayerList)
			# The given layer list potentially does not have all the layers
			# initialized so we need to fill in the rest of the layers
			self.__init_all_layers()
		
	# Perform steps to ensure layer validity
	# NOTE: Assumes self.layerList has at least one layer properly initialized
	def __init_all_layers(self):
	
		# fill solid space to prevent holes inside walls
		self.__fill_layers(GameData.MAP_CAT_SOLID_SPACE)
		# fill empty space to prevent air/floor hole
		self.__fill_layers(GameData.MAP_CAT_OPEN_SPACE)
		# fill line feed to maintain consistent layer display
		self.__fill_layers(GameData.MAP_CAT_LINE_FEED)
		# fill wall to prevent gaps
		self.__fill_layers(GameData.MAP_CAT_WALL)
		
		floorCategory = self.get_category(GameData.MAP_TILE_LAYER_INDEX_FLOOR)
		standCategory = self.get_category(GameData.MAP_TILE_LAYER_INDEX_STAND)
		
		if ((floorCategory == GameData.INVALID_INDEX) and (standCategory == GameData.MAP_CAT_EXIT)):
			# the floor underneath the door should be a wall to prevent a hole			
			standChar = self.get_char(GameData.MAP_TILE_LAYER_INDEX_STAND)
			tileOrientation = MapTile.get_tileChar_orientation(self.get_char(GameData.MAP_TILE_LAYER_INDEX_STAND), GameData.MAP_CAT_EXIT)
			
			if (tileOrientation == GameData.INVALID_INDEX):
				Utils.Show_Game_Error("MapTile::__init_all_layers() - Invalid tileOrientation for standChar = \'%s\'" % standChar)
			else:
				exitChar = GameData.MAP_CHAR_EXIT_LIST[tileOrientation]
				self.set_category(GameData.MAP_CAT_EXIT, GameData.MAP_TILE_LAYER_INDEX_FLOOR)
				self.set_char(exitChar, GameData.MAP_TILE_LAYER_INDEX_FLOOR)
			
			
	# Fills uninitialized layers with initialized layer data
	def __fill_layers(self, srcCategory):
		
		floorCategory = self.get_category(GameData.MAP_TILE_LAYER_INDEX_FLOOR)
		standCategory = self.get_category(GameData.MAP_TILE_LAYER_INDEX_STAND)
		
		if ((floorCategory == GameData.INVALID_INDEX) and (standCategory == srcCategory)):
				# fill uninitialized floor layer
				self.__copy_layer(GameData.MAP_TILE_LAYER_INDEX_STAND, GameData.MAP_TILE_LAYER_INDEX_FLOOR)
		elif ((floorCategory == srcCategory) and (standCategory == GameData.INVALID_INDEX)):
			# fill uninitialized floor layer
			self.__copy_layer(GameData.MAP_TILE_LAYER_INDEX_FLOOR, GameData.MAP_TILE_LAYER_INDEX_STAND)
				
	# Copies source layer data to target layer.
	# NOTE: Function preserves the target layer obj ID
	def __copy_layer(self, srcLayerIndex, destLayerIndex):
	
		if ((TileLayer.is_valid(srcLayerIndex)) and (TileLayer.is_valid(destLayerIndex))):
			srcCategory = self.get_category(srcLayerIndex)
			srcChar = self.get_char(srcLayerIndex)
			
			self.set_category(srcCategory, destLayerIndex)
			self.set_char(srcChar, destLayerIndex)
			
	# Inserts layer data into tile.
	# Returns RT_SUCCESS if inserted correctly, else RT_FAILURE
	# NOTE: Function preserves the existing layer obj ID unless specified otherwise
	def insert_layer(self, newLayer, newLayerIndex, isCopyID=False):
	
		rStat = GameData.RT_FAILURE
	
		if (TileLayer.is_valid(newLayerIndex)):
		
			#currentLayer = self.__layerList[newLayerIndex]
			#print u"DEBUG_JW - MapDisplay::insert_layer() - LAYER%d inserting (%s) into (%s)" % (newLayerIndex, newLayer.get_str(), currentLayer.get_str())
			#raw_input()
			
			self.set_category(newLayer.category, newLayerIndex)
			self.set_char(newLayer.tileChar, newLayerIndex)
			
			if (isCopyID):
				self.set_ID(newLayer.objID, newLayerIndex)
			
			rStat = GameData.RT_SUCCESS
			
		return rStat
			
	# Gets layer where given objID resides.
	# Returns INVALID_INDEX if ID is not in tile.
	def get_layerIndex_from_ID(self, inObjID):
		
		retLayer = GameData.INVALID_INDEX
		
		for layerCount in range(0, GameData.MAP_TILE_LAYERS_NUM): 
			if (self.__layerList[layerCount].objID == inObjID):
				retLayer = layerCount
		
		return retLayer
		
	# Gets layer at given index.
	# Returns None if index is not in tile.
	def get_layer_from_index(self, layerIndex):
		
		retLayer = None
		
		if (TileLayer.is_valid(layerIndex)):
			retLayer = self.__layerList[layerIndex]
		
		return retLayer
		
	# Determine if given ID exists in any layer
	def contains_ID(self,  inObjID):
		
		retVal = False
		
		for layerCount in range(0, GameData.MAP_TILE_LAYERS_NUM): 
			if (self.__layerList[layerCount].objID == inObjID):
				retVal = True
				break # done looking so quit
		
		return retVal
		
	# Accessors for tile obj category.
	# If no valid inLayer is given, functions assume default layer category.
	def get_category(self, inLayer=GameData.INVALID_INDEX):
		
		retCategory = GameData.INVALID_INDEX
		if (TileLayer.is_valid(inLayer)):
			retCategory = self.__layerList[inLayer].category
		else:
			retCategory = self.__layerList[self.__DEFAULT_LAYER].category
		return retCategory
		
	def set_category(self, newCategory,  inLayer=GameData.INVALID_INDEX):
		
		if (TileLayer.is_valid(inLayer)):
			self.__layerList[inLayer].category = newCategory
		else:
			self.__layerList[self.__DEFAULT_LAYER].category = newCategory
			
	# Accessors for tile obj character.
	# If no valid inLayer is given, functions assume default layer char.
	def get_char(self, inLayer=GameData.INVALID_INDEX):
		
		retChar = GameData.INVALID_INDEX
		if (TileLayer.is_valid(inLayer)):
			retChar = self.__layerList[inLayer].tileChar
		else:
			retChar = self.__layerList[self.__DEFAULT_LAYER].tileChar
		return retChar
		
	def set_char(self, newChar,  inLayer=GameData.INVALID_INDEX):
		
		if (TileLayer.is_valid(inLayer)):
			self.__layerList[inLayer].tileChar = newChar
		else:
			self.__layerList[self.__DEFAULT_LAYER].tileChar = newChar
			
	# Accessors for tile obj ID.
	# If no valid inLayer is given, functions assume default layer ID.
	def get_ID(self, inLayer=GameData.INVALID_INDEX):
		
		retID = GameData.INVALID_INDEX
		if (TileLayer.is_valid(inLayer)):
			retID = self.__layerList[inLayer].objID
		else:
			retID = self.__layerList[self.__DEFAULT_LAYER].objID
		return retID
		
	def set_ID(self, newID,  inLayer=GameData.INVALID_INDEX):
		
		if (TileLayer.is_valid(inLayer)):
			self.__layerList[inLayer].objID = newID
		else:
			self.__layerList[self.__DEFAULT_LAYER].objID = newID
			
			
	# Provides tile char for map display
	def get_char_for_display(self):
		
		retChar = ''
		
		floorChar = self.get_char(GameData.MAP_TILE_LAYER_INDEX_FLOOR)
		standChar = self.get_char(GameData.MAP_TILE_LAYER_INDEX_STAND)
		
		if (standChar != GameData.MAP_CAT_OPEN_SPACE):
			# standing layer trumps anything on the floor for user display
			retChar = standChar
		else:
			retChar = floorChar
			
		return retChar
		
		
	def get_str(self):
		retStr = self.pos.get_str() + ": "
		
		# align columns
		if (self.pos.xPos < 10):
			retStr += " "
		if (self.pos.yPos < 10):
			retStr += " "
		
		# show layer data
		count = 0
		
		for layer in self.__layerList:
			retStr += "-LAYER%d %s " % (count, layer.get_str())
			count += 1
		
		return retStr
				

#---------------------------------------------------
#---------------------------------------------------
# Class: TileLayer
#
# Member Variables:	
#		category	- category for map obj
#		tileChar	- char representing map obj
#		objID		- unique identifier for layer
#---------------------------------------------------
#---------------------------------------------------
		
class TileLayer(object):
		
	def __init__(self, newCategory=GameData.INVALID_INDEX, newTileChar='', newObjID=GameData.INVALID_INDEX):
			
		self.category = newCategory
		self.tileChar = newTileChar
		self.objID = newObjID 
			
	# static method to determine validity of given layer number
	@staticmethod	
	def is_valid(inLayer):
		
		retVal = False
		
		for tileLayer in GameData.MAP_TILE_LAYER_LIST:
			if (inLayer == tileLayer):
				retVal = True
				break # done looking so quit
		
		return retVal
		
	@staticmethod
	# Determine layer from rules of entity location
	def get_layerIndex_from_char(mapChar):
		retLayerIndex = GameData.MAP_TILE_LAYER_INDEX_STAND
		
		if (mapChar == GameData.MAP_CHAR_ITEM):
			retLayerIndex = GameData.MAP_TILE_LAYER_INDEX_FLOOR
		
		return retLayerIndex
		
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
	@staticmethod
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
		
	
	def get_str(self):
		retStr = self.tileChar
		
		if (self.tileChar == GameData.MAP_CHAR_LINE_FEED):
			# prevent CR on print
			retStr = "<LF>"
		
		retStr += ", category = %d, " % self.category
		retStr += "ID = %d" % self.objID
		
		return retStr
			
#---------------------------------------------------
#---------------------------------------------------
# Class: bcolors
#---------------------------------------------------
#---------------------------------------------------			
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033 [ 93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
			
			# update tiles
			layerIndex = TileLayer.get_layerIndex_from_char(newChar)
			newMapTile = self.__make_tile_from_single_layer(xVal, yVal, newChar,  layerIndex)
			self.__tileList.append(newMapTile)
			
			if (newChar == GameData.MAP_CHAR_LINE_FEED):
				yVal += 1
				xVal = 0
			else:
				xVal += 1
				
		
		
	def get_map_for_display(self):
		
		mapStr = ""
		
		#print "DEBUG_JW: MapContainer.__tileList len = %d" % len(self.__tileList)
		
		for mapItem in self.__tileList:
			mapStr += mapItem.get_char_for_display()
			
		return mapStr
		
		
	def dump_map_data(self, mapIndex):
		
		print "###### MAP %d DATA######" % (mapIndex)
		
		for mapItem in self.__tileList:
			print "%s" % mapItem.get_str()
		
		raw_input(GameData.PROMPT_CONTINUE_STR)
		
			
	# Creates single-layer tile obj from map data
	# NOTE: all other layers created as empty/open space
	def __make_tile_from_single_layer(self, xVal, yVal, newChar, layerIndex):
		
		mapTile = None
		
		if (not TileLayer.is_valid(layerIndex)):
			Utils.Show_Game_Error("MapContainer::__make_tile_from_single_layer() - Invalid layerIndex for map tile construction: %d " % layerIndex)
		else:
			category = TileLayer.get_category_from_char(newChar)
			
			if (category == GameData.INVALID_INDEX):
				Utils.Show_Game_Error("MapContainer::__make_tile_from_single_layer() - Invalid character for map tile construction: \"%s\" (%d, %d)." % (newChar, xVal, yVal))
			else:
				mapPos = MapPos(xVal, yVal)
				
				newTileLayerList = []
				
				for layerCount in range(0, GameData.MAP_TILE_LAYERS_NUM): 
				
					objID = self.__idGen.get_num() # use unique ID for each layer obj
					
					if (layerCount == layerIndex):
						# insert tile data in proper layer
						newTileLayerList.append(TileLayer(category, newChar, objID))
					else:
						# init invalid layer data for now (except for valid ID)
						newTileLayerList.append(TileLayer(GameData.INVALID_INDEX, '', objID))
						
				mapTile = MapTile(mapPos,  newTileLayerList)
				
				dbg_showCreation = False
				
				if (dbg_showCreation):
					print "DEBUG_JW: __make_tile_from_single_layer() - \'%s\' , category = %d, ID = %d at (%d, %d)" % (newChar, category, objID, mapPos.xPos, mapPos.yPos)
		
		return mapTile
		
	# Gets the tile location from objID.
	# Returns INVALID_INDEX if no tile is found.
	def __get_tileIndex_from_ID(self, objID):
		retIndex = GameData.INVALID_INDEX
		count = 0
		
		for mapItem in self.__tileList:
			if (mapItem.contains_ID(objID)):
				retIndex = count
				break
			else:
				count += 1
		
		return retIndex
		
		
	def __get_tileIndex_from_Pos(self, pos):
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
	def __get_tile_from_Pos(self, pos):
	
		retTile = None
		
		tileIndex = self.__get_tileIndex_from_Pos(pos)
		
		if (tileIndex != GameData.INVALID_INDEX):
			retTile = self.__tileList[tileIndex]
		
		return retTile
	
		
	# Swaps all tile data while preserving position data.
	def __swap_tiles_in_List(self, index1, index2):
		listLen = len(self.__tileList)
		
		if ((index1 > listLen) or (index2 > listLen)):
			Utils.Show_Game_Error("DEBUG_JW: __swap_tiles_in_List() - invalid indices %d and %d!" % (index1, index2))
		else:
			# save off positions before swap
			pos1 = self.__tileList[index1].pos
			pos2 = self.__tileList[index2].pos
			
			# swap all data and restore positions
			tmpTile = copy.deepcopy(self.__tileList[index1])
			self.__tileList[index1] = copy.deepcopy(self.__tileList[index2])
			self.__tileList[index1].pos = pos1
			self.__tileList[index2] = copy.deepcopy(tmpTile)
			self.__tileList[index2].pos = pos2
			
			
	# Swaps tile layers at specified layerIndex
	# Returns: RT_SUCCESS if swap succeeds, else RT_FAILURE
	#
	# Parameters:
	#	tileIndex1 = 1st tile postion to swap
	#	tileIndex2 = 2nd tile postion to swap
	#	layerIndex = points at layer to swap
	def __swap_tileLayers_in_List(self, tileIndex1, tileIndex2, layerIndex):
		
		rStat = GameData.RT_FAILURE
		
		listLen = len(self.__tileList)
		
		if ((tileIndex1 > listLen) or (tileIndex2 > listLen)):
			Utils.Show_Game_Error("MapContainer:: __swap_tileLayers_in_List() - invalid indices %d and %d!" % (tileIndex1, tileIndex2))
		else:
			# swap entire layer including the objID
			tmpLayer1 = copy.deepcopy(self.__tileList[tileIndex2].get_layer_from_index(layerIndex))
			tmpLayer2 = copy.deepcopy(self.__tileList[tileIndex1].get_layer_from_index(layerIndex))
			
			if ((tmpLayer2 == None) or (tmpLayer2 == None)):
				Utils.Show_Game_Error("MapContainer:: __swap_tileLayers_in_List() - invalid layerIndex %d!" % (layerIndex))
			else:
				rStat = self.__tileList[tileIndex2].insert_layer(tmpLayer2, layerIndex, True)
				
				if (rStat == GameData.RT_SUCCESS):
					rStat = self.__tileList[tileIndex1].insert_layer(tmpLayer1, layerIndex, True)
			
		return rStat
			
	def __get_obj_mapID_list(self, objCategory, layerIndex):
		retIdList = []
		
		for mapItem in self.__tileList:
			if (mapItem.get_category(layerIndex) == objCategory):
				retIdList.append(mapItem.objID)
		
		return retIdList
		
	# Finds the mapTile in a given direction
	#
	#	Parameters:
	#		objID - ID of starting tile obj
	#		objDir - direction to look for target
	#
	#	Return:
	#		retTile - target tile of given direction
	#		retTileIndex - target's index into tile collection
	def __get_target_tile_from_Dir(self, objID, objDir):
	
		retTile = None
		retTileIndex = GameData.INVALID_INDEX
		
		currentTileIndex = self.__get_tileIndex_from_ID(objID)
		
		if (currentTileIndex == GameData.INVALID_INDEX):
			Utils.Show_Game_Error("MapDisplay::__get_target_tile_from_Dir() - invalid objID %d!" % objID)
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
				Utils.Show_Game_Error("MapDisplay::__get_target_tile_from_Dir() - invalid objDir %s!" % objDir)
			else:
				targetTileIndex = self.__get_tileIndex_from_Pos(targetPos)
				
				if (targetTileIndex == GameData.INVALID_INDEX):
					Utils.Show_Game_Error("MapDisplay::__get_target_tile_from_Dir() - invalid target position (%d, %d)!" % (targetPos.xPos, targetPos.yPos))
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
	
		targetTile, targetTileIndex = self.__get_target_tile_from_Dir(objID, objDir)
			
		if (targetTile != None):
			currentTileIndex = self.__get_tileIndex_from_ID(objID)
			
			if (currentTileIndex == GameData.INVALID_INDEX):
				Utils.Show_Game_Error("MapContainer::move_map_item() - invalid objID %d!" % objID)
			else:
				currentLayerIndex = self.__tileList[currentTileIndex].get_layerIndex_from_ID(objID)
				if (targetTile.get_category(currentLayerIndex) == GameData.MAP_CAT_OPEN_SPACE):
					# this is a valid move so proceed with swap
					self.__swap_tileLayers_in_List(currentTileIndex, targetTileIndex, currentLayerIndex)
					
					
	def use_map_item(self, objID, objDir):		
		retID = GameData.INVALID_INDEX
			
		targetTile, targetTileIndex = self.__get_target_tile_from_Dir(objID, objDir)
			
		if (targetTile != None):
			currentLayerIndex = self.get_layer_from_ID(objID)
			if (targetTile.get_category(currentLayerIndex) == GameData.MAP_CAT_EXIT):
				# send back the exit obj ID for engine processing
				retID = targetTile.objID

		else:
			pass
		
		return retID 
		
		
	# Function places entity to target position's empty tile in map
	# Returns new objID if successful placement, else INVALID_INDEX 
	def place_map_entity(self, newEntityChar, newEntityPos):		
	
		retID = GameData.INVALID_INDEX
		
		if (newEntityPos == None):
			Utils.Show_Game_Error("MapDisplay::place_map_entity() - invalid newEntityPos!")
		else:
			# determine if target tile is empty
			targetTile = self.__get_tile_from_Pos(newEntityPos)
			
			if (targetTile == None):
				Utils.Show_Game_Error("MapDisplay::place_map_entity() - could not get targetTile from position = %s" % newEntityPos.get_str())
			else:
			
				newEntityCategory = TileLayer.get_category_from_char(newEntityChar)
				
				if (newEntityCategory == GameData.INVALID_INDEX):
					Utils.Show_Game_Error("MapDisplay::place_map_entity() - invalid newEntityChar = %s" % newEntityChar)
				else:
				
					layerIndex = TileLayer.get_layerIndex_from_char(newEntityChar)
				
					if (targetTile.get_category(layerIndex) != GameData.MAP_CAT_OPEN_SPACE):
						if (newEntityChar == targetTile.get_char(layerIndex)):
							# placing tile that already exists so return existing ID
							retID = targetTile.get_ID(layerIndex)
							Utils.Show_Game_Error("MapDisplay::place_map_entity() - duplicate placement at pos = %s" % newEntityPos.get_str()) 
					else:
						# placing entity in open space
						testStr = "DEBUG_JW (notAnError): MapDisplay::place_map_entity() - tile %s : category = %d" % (newEntityPos.get_str(), newEntityCategory)
						Utils.Show_Game_Error(testStr) 
					
						# Free to place entity
						# don't care about new objID since we'll keep the existing one
						newLayer = TileLayer(newEntityCategory, newEntityChar, GameData.INVALID_INDEX)
						
						# update target reference
						rStat = targetTile.insert_layer(newLayer, layerIndex)
						
						if (rStat != GameData.RT_SUCCESS):
							Utils.Show_Game_Error("MapDisplay::place_map_entity() - could not insert \'%s\' into pos %s,layer %d!" % (newEntityChar, newEntityPos.get_str(),  layerIndex))
						else:
							retID = targetTile.get_ID(layerIndex)
													
		return retID
		
		def remove_map_entity(self):
			pass
			
		def replace_map_entity(self):
			pass

	
	if __name__ == '__main__':	
		GothansGame.start()
		
		
		
		
		
		
		
		
		
		
