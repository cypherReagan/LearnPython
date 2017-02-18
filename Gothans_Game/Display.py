
import SharedConst as Const
import Utils
import copy
import Console
  

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
		
	def is_valid(self):
		
		retVal = False
		
		if ((self.xPos >= 0) and (self.yPos >=0)):
			retVal = True
		
		return retVal
		
	def compare(self, inPos):
		
		retVal = False
		
		if (inPos != None):
			if ((inPos.xPos == self.xPos) and (inPos.yPos == self.yPos)):
				retVal = True
		
		return retVal
		
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
	__DEFAULT_LAYER = Const.MAP_TILE_LAYER_INDEX_STAND
	
	@staticmethod
	def get_tileChar_orientation(tileChar, tileCategory):
		
		retOrientation = Const.INVALID_INDEX
		
		if (tileCategory == Const.MAP_CAT_WALL):
			retOrientation = MapTile.get_tileChar_orientation_from_list(tileChar, Const.MAP_CHAR_WALL_LIST)
		elif (tileCategory == Const.MAP_CAT_EXIT):
			retOrientation = MapTile.get_tileChar_orientation_from_list(tileChar, Const.MAP_CHAR_EXIT_LIST)
		
		return retOrientation
		
	@staticmethod
	def get_tileChar_orientation_from_list(tileChar, tileCharList):
		
		retVal = Const.INVALID_INDEX
		
		for count in range(0, Const.TILE_ORIENTATION_MAX_NUM):
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
		
		if (layerListLen != Const.MAP_TILE_LAYERS_NUM):
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
		self.__fill_layers(Const.MAP_CAT_SOLID_SPACE)
		# fill empty space to prevent air/floor hole
		self.__fill_layers(Const.MAP_CAT_OPEN_SPACE)
		# fill line feed to maintain consistent layer display
		self.__fill_layers(Const.MAP_CAT_LINE_FEED)
		# fill wall to prevent gaps
		self.__fill_layers(Const.MAP_CAT_WALL)
		
		floorCategory = self.get_category(Const.MAP_TILE_LAYER_INDEX_FLOOR)
		standCategory = self.get_category(Const.MAP_TILE_LAYER_INDEX_STAND)
		
		if ((floorCategory == Const.INVALID_INDEX) and (standCategory == Const.MAP_CAT_EXIT)):
			# the floor underneath the door should be a wall to prevent a hole			
			standChar = self.get_char(Const.MAP_TILE_LAYER_INDEX_STAND)
			tileOrientation = MapTile.get_tileChar_orientation(self.get_char(Const.MAP_TILE_LAYER_INDEX_STAND), Const.MAP_CAT_EXIT)
			
			if (tileOrientation == Const.INVALID_INDEX):
				Utils.Show_Game_Error("MapTile::__init_all_layers() - Invalid tileOrientation for standChar = \'%s\'" % standChar)
			else:
				exitChar = Const.MAP_CHAR_EXIT_LIST[tileOrientation]
				self.set_category(Const.MAP_CAT_EXIT, Const.MAP_TILE_LAYER_INDEX_FLOOR)
				self.set_char(exitChar, Const.MAP_TILE_LAYER_INDEX_FLOOR)
			
			
	# Fills uninitialized layers with initialized layer data
	def __fill_layers(self, srcCategory):
		
		floorCategory = self.get_category(Const.MAP_TILE_LAYER_INDEX_FLOOR)
		standCategory = self.get_category(Const.MAP_TILE_LAYER_INDEX_STAND)
		
		if ((floorCategory == Const.INVALID_INDEX) and (standCategory == srcCategory)):
				# fill uninitialized floor layer
				self.__copy_layer(Const.MAP_TILE_LAYER_INDEX_STAND, Const.MAP_TILE_LAYER_INDEX_FLOOR)
		elif ((floorCategory == srcCategory) and (standCategory == Const.INVALID_INDEX)):
			# fill uninitialized floor layer
			self.__copy_layer(Const.MAP_TILE_LAYER_INDEX_FLOOR, Const.MAP_TILE_LAYER_INDEX_STAND)
				
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
	
		rStat = Const.RT_FAILURE
	
		if (TileLayer.is_valid(newLayerIndex)):
		
			#currentLayer = self.__layerList[newLayerIndex]
			#print u"DEBUG_JW - MapContainer::insert_layer() - LAYER%d inserting (%s) into (%s)" % (newLayerIndex, newLayer.get_str(), currentLayer.get_str())
			#raw_input()
			
			self.set_category(newLayer.category, newLayerIndex)
			self.set_char(newLayer.tileChar, newLayerIndex)
			
			newColor = TileLayer.get_default_color(newLayer.category)
			
			if (newColor == None):
				Utils.Show_Game_Error("MapTile:insert_layer() - Could not insert color from newCategory = %d!" % newLayer.category)
			else:
				self.set_color(newColor, newLayerIndex)
			
			if (isCopyID):
				self.set_ID(newLayer.objID, newLayerIndex)
			
			rStat = Const.RT_SUCCESS
			
		return rStat
			
	# Gets layer where given objID resides.
	# Returns INVALID_INDEX if ID is not in tile.
	def get_layerIndex_from_ID(self, inObjID):
		
		retLayer = Const.INVALID_INDEX
		
		for layerCount in range(0, Const.MAP_TILE_LAYERS_NUM): 
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
		
		for layerCount in range(0, Const.MAP_TILE_LAYERS_NUM): 
			if (self.__layerList[layerCount].objID == inObjID):
				retVal = True
				break # done looking so quit
		
		return retVal
		
	# Accessors for tile obj category.
	# If no valid inLayer is given, functions assume default layer category.
	def get_category(self, inLayer=Const.INVALID_INDEX):
		
		retCategory = Const.INVALID_INDEX
		if (TileLayer.is_valid(inLayer)):
			retCategory = self.__layerList[inLayer].category
		else:
			retCategory = self.__layerList[self.__DEFAULT_LAYER].category
		return retCategory
		
	def set_category(self, newCategory,  inLayer=Const.INVALID_INDEX):
		
		if (TileLayer.is_valid(inLayer)):
			self.__layerList[inLayer].category = newCategory
		else:
			self.__layerList[self.__DEFAULT_LAYER].category = newCategory
			
	# Accessors for tile obj character.
	# If no valid inLayer is given, functions assume default layer char.
	def get_char(self, inLayer=Const.INVALID_INDEX):
		
		retChar = Const.INVALID_INDEX
		if (TileLayer.is_valid(inLayer)):
			retChar = self.__layerList[inLayer].tileChar
		else:
			retChar = self.__layerList[self.__DEFAULT_LAYER].tileChar
		return retChar
	
		
	def set_char(self, newChar,  inLayer=Const.INVALID_INDEX):
		
		if (TileLayer.is_valid(inLayer)):
			self.__layerList[inLayer].tileChar = newChar
		else:
			self.__layerList[self.__DEFAULT_LAYER].tileChar = newChar
			
	# Accessors for tile obj ID.
	# If no valid inLayer is given, functions assume default layer ID.
	def get_ID(self, inLayer=Const.INVALID_INDEX):
		
		retID = Const.INVALID_INDEX
		if (TileLayer.is_valid(inLayer)):
			retID = self.__layerList[inLayer].objID
		else:
			retID = self.__layerList[self.__DEFAULT_LAYER].objID
		return retID
		
	def set_ID(self, newID,  inLayer=Const.INVALID_INDEX):
		
		if (TileLayer.is_valid(inLayer)):
			self.__layerList[inLayer].objID = newID
		else:
			self.__layerList[self.__DEFAULT_LAYER].objID = newID
			
			
	# Accessors for tile color.
	# If no valid inLayer is given, functions assume default layer ID.
	def get_color(self, inLayer=Const.INVALID_INDEX):
		
		retColor = Const.INVALID_INDEX
		if (TileLayer.is_valid(inLayer)):
			retColor = self.__layerList[inLayer].color
		else:
			retColor = self.__layerList[self.__DEFAULT_LAYER].color
		return retColor
		
	def set_color(self, newColor,  inLayer=Const.INVALID_INDEX):
		
		if (TileLayer.is_valid(inLayer)):
			self.__layerList[inLayer].color = newColor
		else:
			self.__layerList[self.__DEFAULT_LAYER].color = copy.deepcpoy(newColor)
			
			
	# Provides tile char for map display
	def get_char_for_display(self):
		
		retChar = ''
		
		floorChar = self.get_char(Const.MAP_TILE_LAYER_INDEX_FLOOR)
		standChar = self.get_char(Const.MAP_TILE_LAYER_INDEX_STAND)
		
		# provide char with color applied
		if (standChar != Const.MAP_CHAR_OPEN_SPACE):
			# standing layer trumps anything on the floor for user display
			retChar = self.__layerList[Const.MAP_TILE_LAYER_INDEX_STAND].color.get_painted_char(standChar)
			
		else:
			retChar = self.__layerList[Const.MAP_TILE_LAYER_INDEX_FLOOR].color.get_painted_char(floorChar)
			
		return retChar
		
	# Updates direction for rotatable characters
	# Returns status from update
	def update_char_from_dir(self, inLayer, newDir):
		
		rStat = Const.RT_INVALID_PARAMETER
		
		if ((newDir >= 0) and (newDir < len(Const.DIR_STR_LIST))):
			# valid direction
			if (TileLayer.is_valid(inLayer)):
	
				rStat = Const.RT_SUCCESS
				
				if (self.__layerList[inLayer].category == Const.MAP_CAT_PLAYER):
					self.__layerList[inLayer].tileChar = Const.MAP_CHAR_PLAYER_LIST[newDir]
					
				elif (self.__layerList[inLayer].category == Const.MAP_CAT_ENEMY):
					self.__layerList[inLayer].tileChar = Const.MAP_CHAR_ENEMY_LIST[newDir]
				else:
					# char is not rotatable
					rStat = RT_FAILURE
				
		
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
#		color		- specifies which color the layer uses
#---------------------------------------------------
#---------------------------------------------------
		
class TileLayer(object):
		
	def __init__(self, newCategory=Const.INVALID_INDEX, newTileChar='', newObjID=Const.INVALID_INDEX):
			
		self.category = newCategory
		self.tileChar = newTileChar
		self.objID = newObjID 
		
		# update tile color with pre-defined defaults
		tmpColor = TileLayer.get_default_color(self.category)
			
		if (tmpColor == None):
			# something went really wrong
			Utils.Show_Game_Error("TileLayer::init() - could not get color from category %d!" % self.category)
		else:
			self.color = copy.deepcopy(tmpColor)
			

			
	@staticmethod
	def get_default_color(inCategory):
		
		retColor = None
		
		if ((inCategory >= 0) and (inCategory < len (Const.DEFAULT_CHAR_COLOR_LIST))):

			colorForeground, colorBackground, format = Const.DEFAULT_CHAR_COLOR_LIST[inCategory]
		else:
			# given invalid category so just set generic defaults for now
			colorForeground = Console.DEFAULT_COLOR
			colorBackground = Console.DEFAULT_COLOR
			format = Const.INVALID_INDEX
			
		retColor = Console.bcolor(colorForeground, colorBackground, format)
		
		return retColor
			
	# static method to determine validity of given layer number
	@staticmethod	
	def is_valid(inLayer):
		
		retVal = False
		
		for tileLayer in Const.MAP_TILE_LAYER_LIST:
			if (inLayer == tileLayer):
				retVal = True
				break # done looking so quit
		
		return retVal
		
	@staticmethod
	# Determine layer from rules of entity location
	def get_layerIndex_from_char(mapChar):
		retLayerIndex = Const.MAP_TILE_LAYER_INDEX_STAND
		
		if (mapChar == Const.MAP_CHAR_ITEM):
			retLayerIndex = Const.MAP_TILE_LAYER_INDEX_FLOOR
		
		return retLayerIndex
		
	@staticmethod
	def get_category_from_char(mapChar):
		
		mapCategory = 0 # categories are 0-based
		foundMatch = False
		
		for itemList in Const.MAP_CHARS_LIST:
			if (mapChar in itemList):
				# done looking
				foundMatch = True
				break
			else:
				mapCategory += 1
				
		if (not foundMatch):
			mapCategory = Const.INVALID_INDEX
			
		return mapCategory
		
	# Get mapChar based on tile category.
	# Returns empty char if mapChar cannot be calculated.
	@staticmethod
	def get_char_from_category(self, mapTileCategory, charIndex=Const.INVALID_INDEX):
	
		mapChar = ''
			
		if ((mapTileCategory >= 0) and (mapTileCategory < len(Const.MAP_CHARS_LIST))):
		
			itemList = Const.MAP_CHARS_LIST[mapTileCategory]
			
			if (charIndex == Const.INVALID_INDEX):
				# caller did not provide list index so default to the 1st list entry
				charIndex = 0
			
			if (len(itemList) > charIndex):
				mapChar = itemList[charIndex]
		
		return mapChar
		
		
	# Get layer index based on tile category.
	# Assumes category relates to a map entity.
	#
	# Returns INVALID_INDEX if index cannot be calculated.
	@staticmethod
	def Get_Entity_LayerIndex_From_Category(mapTileCategory):
		
		retIndex = Const.INVALID_INDEX
		
		if ((mapTileCategory == Const.MAP_CAT_PLAYER) or (mapTileCategory == Const.MAP_CAT_ENEMY) or (mapTileCategory == Const.MAP_CAT_EXIT)):
			retIndex = Const.MAP_TILE_LAYER_INDEX_STAND
			
		elif (mapTileCategory == Const.MAP_CAT_ITEM):
			retIndex = Const.MAP_TILE_LAYER_INDEX_FLOOR
		
		return retIndex
		
		
	# Get layer index based on tile char.
	# Assumes char relates to a map entity.
	#
	# Returns INVALID_INDEX if index cannot be calculated.
	@staticmethod
	def Get_Entity_LayerIndex_From_Char(mapTileChar):
		
		retIndex = Const.INVALID_INDEX
		
		if ((mapTileChar in Const.MAP_CHAR_PLAYER_LIST) or (mapTileChar in Const.MAP_CHAR_ENEMY_LIST) or (mapTileChar in Const.MAP_CHAR_EXIT_LIST)):
			retIndex = Const.MAP_TILE_LAYER_INDEX_STAND
			
		elif (mapTileChar == Const.MAP_CHAR_ITEM):
			retIndex = Const.MAP_TILE_LAYER_INDEX_FLOOR
		
		return retIndex
	
	def get_str(self):
		retStr = self.tileChar
		
		if (self.tileChar == Const.MAP_CHAR_LINE_FEED):
			# prevent CR on print
			retStr = "<LF>"
		
		retStr += ", category= %d, " % self.category
		retStr += "ID= %d, " % self.objID
		retStr += "color=%s" % self.color.get_str()
		
		return retStr
			

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
#		IdGen			- objID generator
#		
#---------------------------------------------------
#---------------------------------------------------
		
class MapContainer(object):
	
	IdGen = NumGenerator(0)
	
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
			
			# update tiles
			layerIndex = TileLayer.get_layerIndex_from_char(newChar)
			newMapTile = self.__make_tile_from_single_layer(xVal, yVal, newChar,  layerIndex)
			self.__tileList.append(newMapTile)
			
			if (newChar == Const.MAP_CHAR_LINE_FEED):
				yVal += 1
				xVal = 0
			else:
				xVal += 1
				
	@staticmethod
	# Determines target position from current position and given direction
	# Returns:
	#	targetPos - None if target could not be calculated
	def Get_Pos_From_Dir(currentPos, objDir):
	
		targetPos = MapPos(currentPos.xPos, currentPos.yPos) # get new instance to avoid copy-by-reference
		
		if (objDir == Const.DIR_NORTH):
			targetPos.yPos -= 1 # y-axis is inverted in map str
		elif (objDir == Const.DIR_WEST):
			targetPos.xPos -= 1
		elif (objDir == Const.DIR_SOUTH):
			targetPos.yPos += 1 # y-axis is inverted in map str
		elif (objDir == Const.DIR_EAST):
			targetPos.xPos += 1
		else:
			# bad direction so return bad pos
			targetPos = None
			
		return targetPos
		
	def get_map_for_display(self):
		
		mapStr = ""
		
		#print "DEBUG_JW: MapContainer.__tileList len = %d" % len(self.__tileList)
		
		for mapItem in self.__tileList:
			mapStr += mapItem.get_char_for_display()
			
		return mapStr
		
		
	def dump_map_data(self, mapIndex):
		
		print "###### MAP %d DATA######" % (mapIndex)
		
		count = 0
		
		for mapItem in self.__tileList:
			print "%d. %s" % (count, mapItem.get_str())
			count += 1
		
		raw_input(Const.PROMPT_CONTINUE_STR)
		
			
	# Creates single-layer tile obj from map data
	# NOTE: all other layers created as empty/open space
	def __make_tile_from_single_layer(self, xVal, yVal, newChar, layerIndex):
		
		mapTile = None
		
		if (not TileLayer.is_valid(layerIndex)):
			Utils.Show_Game_Error("MapContainer::__make_tile_from_single_layer() - Invalid layerIndex for map tile construction: %d " % layerIndex)
		else:
			category = TileLayer.get_category_from_char(newChar)
			
			if (category == Const.INVALID_INDEX):
				Utils.Show_Game_Error("MapContainer::__make_tile_from_single_layer() - Invalid character for map tile construction: \"%s\" (%d, %d)." % (newChar, xVal, yVal))
			else:
				mapPos = MapPos(xVal, yVal)
				
				newTileLayerList = []
				
				for layerCount in range(0, Const.MAP_TILE_LAYERS_NUM): 
				
					objID = MapContainer.IdGen.get_num() # use unique ID for each layer obj
					
					if (layerCount == layerIndex):
						# insert tile data in proper layer
						newTileLayerList.append(TileLayer(category, newChar, objID))
					else:
						# init invalid layer data for now (except for valid ID)
						newTileLayerList.append(TileLayer(Const.INVALID_INDEX, '', objID))
						
				mapTile = MapTile(mapPos,  newTileLayerList)
				
				dbg_showCreation = False
				
				if (dbg_showCreation):
					print "DEBUG_JW: __make_tile_from_single_layer() - \'%s\' , category = %d, ID = %d at (%d, %d)" % (newChar, category, objID, mapPos.xPos, mapPos.yPos)
		
		return mapTile
		
	# Gets the tile location from objID.
	# Returns INVALID_INDEX if no tile is found.
	def __get_tileIndex_from_ID(self, objID):
		retIndex = Const.INVALID_INDEX
		count = 0
		
		for mapItem in self.__tileList:
			if (mapItem.contains_ID(objID)):
				retIndex = count
				break
			else:
				count += 1
		
		return retIndex
		
		
	def __get_tileIndex_from_Pos(self, pos):
		retIndex = Const.INVALID_INDEX
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
		
		if (tileIndex != Const.INVALID_INDEX):
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
		
		rStat = Const.RT_FAILURE
		
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
				
				if (rStat == Const.RT_SUCCESS):
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
	#		objID	- ID of starting tile obj
	#		objDir	- direction to look for target
	#
	#	Return:
	#		retTile 		- target tile of given direction
	#		retTileIndex	- target's index into tile collection
	def __get_target_tile_from_Dir(self, objID, objDir):
	
		retTile = None
		retTileIndex = Const.INVALID_INDEX
		
		currentTileIndex = self.__get_tileIndex_from_ID(objID)
		
		if (currentTileIndex == Const.INVALID_INDEX):
			Utils.Show_Game_Error("MapContainer::__get_target_tile_from_Dir() - invalid objID %d!" % objID)
		else:
			currentTile = self.__tileList[currentTileIndex]
			currentPos = currentTile.pos
			
			targetPos = MapContainer.Get_Pos_From_Dir(currentPos, objDir)
			
			if (targetPos == None):
				Utils.Show_Game_Error("MapContainer::__get_target_tile_from_Dir() - invalid objDir %s!" % objDir)
			else:
				targetTileIndex = self.__get_tileIndex_from_Pos(targetPos)
				
				if (targetTileIndex == Const.INVALID_INDEX):
					Utils.Show_Game_Error("MapContainer::__get_target_tile_from_Dir() - invalid targetPos %s from currentPos %s, ID = %d!" % (targetPos.get_str(), currentPos.get_str(), objID))
				else:
					# get target
					retTile = self.__tileList[targetTileIndex]
					retTileIndex = targetTileIndex
					
		return retTile, retTileIndex
	
	# Queries the map for a tile in a given direction from start position
	#
	#	Parameters:
	#		objPos	- position of starting tile obj
	#		objDir	- direction to look for target
	#
	#	Return:
	#		retTile - target tile of given direction
	#		retTileIndex	- target's index into tile collection
	#
	def __get_target_tile_from_Pos(self, objPos, objDir, layerIndex):
		
		retTile = None
		retTileIndex = Const.INVALID_INDEX
		
		if (objPos == None):
			Utils.Show_Game_Error("MapContainer::__get_target_tile_from_Pos() - invalid objPos!")
		else:
			# calculate starting tile location			
			tileIndex = 0
			
			for tile in self.__tileList:
				if (tile.pos.compare(objPos)):
					# we have a winner so quit
					break
					
				tileIndex += 1
					
			
			if ((tileIndex < 0) or (tileIndex >= len (self.__tileList))):
				Utils.Show_Game_Error("MapContainer::__get_target_tile_from_Pos() - invalid tileIndex %d from pos %s!" % (tileIndex, objPos.get_str()))
			else:
				currentTile = self.__tileList[tileIndex]
				retTile, retTileIndex = self.__get_target_tile_from_Dir(currentTile.get_ID(layerIndex), objDir)
				
		
		return retTile, retTileIndex
	
	# TODO: Remove
	def process_map_cmd(self, mapActionItem):
		
		retActionItem = None
		
		if (mapActionItem != None):
			Utils.Log_Event("Map Display receiving cmd - %s" % mapActionItem.dump_data())
		
			if (mapActionItem.cmdStr == Const.MAP_CMD_STR_MOVE):
				self.move_map_item(mapActionItem.objID, mapActionItem.dir)
			elif(mapActionItem.cmdStr == Const.MAP_CMD_STR_DUMP_DATA):
				self.dump_map_data()
			elif(mapActionItem.cmdStr == Const.MAP_CMD_STR_USE):
				retActionItem = self.use_map_item(mapActionItem.objID, mapActionItem.dir)
			elif(mapActionItem.cmdStr == Const.MAP_CMD_STR_PLACE_ENTITY):
				retActionItem = self.place_entity_map_item(mapActionItem.entityType, mapActionItem.entityPos)
			else:
				pass
			
		return retActionItem
	
	# Determines if target tile is an open space.
	# Looks up target based on direction from objPos.
	def is_open_pos_from_pos(self, objPos, objCategory, objDir):
		
		retVal = False
		
		layerIndex = TileLayer.Get_Entity_LayerIndex_From_Category(objCategory)
			
		if (layerIndex == Const.INVALID_INDEX):
			Utils.Show_Game_Error("MapContainer::is_open_pos_from_pos() - could not get layerIndex from objCategory %d!" % (objCategory))
		else:
	
			targetTile, targetTileIndex = self.__get_target_tile_from_Pos(objPos, objDir, layerIndex)
			
			if (targetTile != None):
			
				targetCategory = targetTile.get_category(layerIndex)
					
				if (targetCategory == Const.MAP_CAT_OPEN_SPACE):
					retVal = True
				elif (Const.DEBUG_MODE):
					Utils.Log_Event("MapContainer::is_open_pos_from_pos() - target NOT open. Start pos %s, targetTileIndex = %d, Category = %d" % (objPos.get_str(), targetTileIndex, targetCategory))
		
		return retVal
		
		
	# Determines if target tile is an open space.
	# Looks up target based on direction from objID.
	#
	# NOTE: Assumes target tile is in same map
	def is_open_pos_from_ID(self, objID, objDir):
		retVal = False
		
		targetTile, targetTileIndex = self.__get_target_tile_from_Dir(objID, objDir)
		
		if (targetTile == None):
			Utils.Show_Game_Error("MapContainer::is_open_pos_from_ID() - could not get targetTile from objID %d and dir=%d!" % (objID, objDir))
		else:
			currentLayerIndex = self.__tileList[targetTileIndex].get_layerIndex_from_ID(objID)
			targetCategory = targetTile.get_category(currentLayerIndex)
				
			if (targetCategory == Const.MAP_CAT_OPEN_SPACE):
				retVal = True
		
		return retVal
	
	def move_map_item(self, objID, objDir):
	
		targetTile, targetTileIndex = self.__get_target_tile_from_Dir(objID, objDir)
			
		if (targetTile != None):
			currentTileIndex = self.__get_tileIndex_from_ID(objID)
			
			if (currentTileIndex == Const.INVALID_INDEX):
				Utils.Show_Game_Error("MapContainer::move_map_item() - invalid objID %d!" % objID)
			else:
				currentLayerIndex = self.__tileList[currentTileIndex].get_layerIndex_from_ID(objID)
				self.__tileList[currentTileIndex].update_char_from_dir(currentLayerIndex, objDir)
				
				if (targetTile.get_category(currentLayerIndex) == Const.MAP_CAT_OPEN_SPACE):
					# this is a valid move so proceed with swap
					self.__swap_tileLayers_in_List(currentTileIndex, targetTileIndex, currentLayerIndex)
					
	# Function finds entity relative to current objID tile in map
	# Returns target (objID, category) if successfully located, else INVALID_INDEX 		
	def use_map_item(self, objID, objDir):		
		retID = Const.INVALID_INDEX
		retCategory = Const.INVALID_INDEX
			
		targetTile, targetTileIndex = self.__get_target_tile_from_Dir(objID, objDir)
			
		if (targetTile == None):
			Utils.Show_Game_Error("MapContainer::use_map_item() - could not get targetTile from objID %d and dir=%d!" % (objID, objDir))
		else:
			currentLayerIndex = targetTile.get_layerIndex_from_ID(objID)
			targetCategory = targetTile.get_category(currentLayerIndex)
			
			if (targetCategory == Const.MAP_CAT_EXIT):
				# send back the exit obj ID and category for engine processing
				retID = targetTile.get_ID(currentLayerIndex)
				retCategory = targetCategory
	
		return retID, retCategory
		
	# Function places entity to target position's empty tile in map (based on direction from starting position)
	# Returns new Oid if successful placement, else INVALID_INDEX 
	def place_map_entity_from_dir(self, newEntityChar, newEntityPos, newObjCategory, newEntityDir, needsNewOid=False):		
	
		retOid = Const.INVALID_INDEX
		
		layerIndex = TileLayer.Get_Entity_LayerIndex_From_Category(newObjCategory)
			
		if (layerIndex == Const.INVALID_INDEX):
			Utils.Show_Game_Error("MapContainer::place_map_entity_from_dir() - could not get layerIndex from objCategory %d!" % (newObjCategory))
		else:
	
			if (newEntityPos == None):
				Utils.Show_Game_Error("MapContainer::place_map_entity_from_dir() - invalid newEntityPos!")
			else:
				targetTile, targetTileIndex = self.__get_target_tile_from_Pos(newEntityPos, newEntityDir, layerIndex)
				
				if (targetTile == None):
					Utils.Show_Game_Error("MapContainer::place_map_entity_from_dir() - could not get targetTile from pos=%s, dir=%d!" % (newEntityPos.get_str(), newEntityDir))
				else:
					retOid = self.place_map_entity(newEntityChar, targetTile.pos, needsNewOid)
		
		return retOid
		
	# Function places entity to target position's empty tile in map
	# Returns new objID if successful placement, else INVALID_INDEX 
	def place_map_entity(self, newEntityChar, newEntityPos, needsNewOid=False):		
	
		retID = Const.INVALID_INDEX
		
		if (newEntityPos == None):
			Utils.Show_Game_Error("MapContainer::place_map_entity() - invalid newEntityPos!")
		else:
			# determine if target tile is empty
			targetTile = self.__get_tile_from_Pos(newEntityPos)
			
			if (targetTile == None):
				Utils.Show_Game_Error("MapContainer::place_map_entity() - could not get targetTile from position = %s" % newEntityPos.get_str())
			else:
			
				newEntityCategory = TileLayer.get_category_from_char(newEntityChar)
				
				if (newEntityCategory == Const.INVALID_INDEX):
					Utils.Show_Game_Error("MapContainer::place_map_entity() - invalid newEntityChar = %s" % newEntityChar)
				else:
				
					layerIndex = TileLayer.get_layerIndex_from_char(newEntityChar)
				
					if (targetTile.get_category(layerIndex) != Const.MAP_CAT_OPEN_SPACE):
						if (newEntityChar == targetTile.get_char(layerIndex)):
							# placing tile that already exists so return existing ID
							retID = targetTile.get_ID(layerIndex)
							Utils.Log_Event("MapContainer::place_map_entity() - duplicate placement at pos = %s" % newEntityPos.get_str()) 
					else:
						# placing entity in open space
						Utils.Log_Event("MapContainer::place_map_entity() - placing at tile %s : category = %d" % (newEntityPos.get_str(), newEntityCategory)) 
					
						# Free to place entity
						# Unless specified, don't care about new objID since we'll keep the existing one
						layerOid = Const.INVALID_INDEX
						
						if (needsNewOid):
							layerOid = MapContainer.IdGen.get_num() # caller asked for unique OID
						
						newLayer = TileLayer(newEntityCategory, newEntityChar, layerOid)
						
						# update target reference
						rStat = targetTile.insert_layer(newLayer, layerIndex)
						
						if (rStat != Const.RT_SUCCESS):
							Utils.Show_Game_Error("MapContainer::place_map_entity() - could not insert \'%s\' into pos %s,layer %d!" % (newEntityChar, newEntityPos.get_str(),  layerIndex))
						else:
							retID = targetTile.get_ID(layerIndex)
													
		return retID
		
	# Function deletes entity and replaces it with an open space in map
	# Returns status of obj removal 
	def remove_map_entity(self, objID):
		rStat = Const.RT_SUCCESS
		
		currentTileIndex = self.__get_tileIndex_from_ID(objID)
		
		if (currentTileIndex == Const.INVALID_INDEX):
			Utils.Show_Game_Error("MapContainer::remove_map_entity() - invalid objID %d!" % objID)
			rStat = Const.RT_INVALID_PARAMETER
		else:
			currentTile = self.__tileList[currentTileIndex]
		
			if (currentTile == None):
				Utils.Show_Game_Error("MapContainer::remove_map_entity() - invalid tile at index %d!" % currentTileIndex)
				rStat = Const.RT_NULL_ITEM
			else:
				currentLayerIndex = currentTile.get_layerIndex_from_ID(objID)
				currentTile.set_category(Const.MAP_CAT_OPEN_SPACE, currentLayerIndex)
				currentTile.set_char(Const.MAP_CHAR_OPEN_SPACE, currentLayerIndex)
	
		return rStat
			
		def replace_map_entity(self):
			pass

	
	if __name__ == '__main__':	
		Engine.start()
		
		
		
		
		
		
		
		
		
		
