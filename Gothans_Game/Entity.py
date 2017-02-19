# DESCRIPTION: 
#		Module contains implementation for all entities featured in game map levels

import SharedConst as Const
import Utils

#---------------------------------------------------
#---------------------------------------------------
# Class: Actor
#--------------------------------------------------
#---------------------------------------------------		
class Actor(object):
	
	
	def __init__(self):
		self.__cmdStrList = []
		self.reset_data()
		
	# Class: Actor
	#
	# Restore actor attributes to default
	def reset_data(self):
		self.__health = 100
		self.xp = 0
		self.theInventoryMgr = InventoryMgr()
		self.__dir = Const.DIR_NORTH
		self.oid = Const.INVALID_INDEX
		self.__cmdStrList[:] = []
		self.location = Const.INVALID_INDEX
		
		# start with default melee weapons
		# TODO: ultimately allow player to find these in map
		self.theInventoryMgr.add_item(WeaponItem(Const.ITEM_SLEDGEHAMMER_INDEX, Const.INFINITE_VAL))
		self.theInventoryMgr.add_item(WeaponItem(Const.ITEM_NET_INDEX, Const.INFINITE_VAL))
		self.theInventoryMgr.add_item(WeaponItem(Const.ITEM_KNIFE_INDEX, Const.INFINITE_VAL))
		#DEBUG_JW - this is for testing
		self.theInventoryMgr.add_item(UtilityItem(Const.ITEM_BATTERY_INDEX, 1))
		
	# Class: Actor
	#
	# Health accessors
	def get_health(self):
		return self.__health
		
	def set_health(self, healthVal):
		
		if (healthVal > 100):
			self.__health = 100
		elif (healthVal < 0):
			self.__health = 0
			
	# Class: Actor
	#
	# Accessor for direction number
	def get_dir_num(self):
		return self.__dir
		
	# Class: Actor
	#
	# Accessor for direction as a string
	def get_dir_str(self):
		dirStr = Const.DIR_DICT.get(self.__dir)
		return dirStr
	
	# Class: Actor
	#
	# Updates actor's direction.
	# Returns True if successful, else False
	def set_dir(self, newDir):
		retVal = False
		
		if ((newDir >= 0) and (newDir < len(Const.DIR_STR_LIST))):
			self.__dir = newDir
			retVal = True
			Utils.Log_Event("Changing actor Dir to %d" % self.__dir)
			
		else:
			Utils.Log_Event("Invalid change attempt of actor Dir to %d" % newDir)
			
			return retVal
			
	# Class: Actor
	#
	# Health attribute manipulations
	def add_health(self, healthVal):
		self.__health += healthVal
		
	def subtract_health(self, healthVal):
		if ((self.__health - healthVal) < 0):
			self.__health = 0
		else:
			self.__health -= healthVal
			
	# Class: Actor
	#
	# Retrieves current item as a string
	def get_current_itemStr(self):
		retStr = Const.EMPTY_ITEM_STR
		
		currentItem = self.theInventoryMgr.get_current_item()
		if (currentItem != None):
			retStr = currentItem.get_name()
		
		return retStr
		
	# Class: Actor
	#
	# Sets specified item as equipped for actor i.e. current item
	def equip_item(self,  itemDataIndex):
		
		return self.theInventoryMgr.set_current_item(itemDataIndex)
		
	# Class: Actor
	#
	# Externally update cmd list
	def set_cmdStrList(self, newCmdStrList):
		self.__cmdStrList = newCmdStrList
		
	# Class: Actor
	#
	# Gets next cmd in list
	def get_next_cmdStr(self):
		
		retStr = ''
		
		if (len(self.__cmdStrList) > 0):
			retStr = self.__cmdStrList[0]
			del self.__cmdStrList[0]
		
		return retStr

	# Class: Actor
	#
	# Show actor stats
	def print_stats(self):
		print "%s\n\nPLAYER STATS:\n\nHEALTH = %d\nXP = %d\n\n%s" % (Const.SEPARATOR_LINE_STR, self.get_health(), self.xp, Const.SEPARATOR_LINE_STR)
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: InventoryMgr
#
# NOTES:
#	Sequence of using item:	
#	-> InventoryMgr__get_item()
#	-> (operate on it)
#	-> InventoryMgr__updateItem()
#
# Member Variables:	
#		__itemList			- list of all inventory items
#		__currentItemIndex	- pointer to currently equipped item
#--------------------------------------------------
#---------------------------------------------------		
class InventoryMgr(object):
	
	def __init__(self):
		self.__itemList = []
		self.__currentItemIndex = Const.INVALID_INDEX
		
	# Class: InventoryMgr
	#
	# Accessors for current item
	def get_current_item(self):
		retItem = None
		
		maxLimit = len(self.__itemList) -1
		
		if ((self.__currentItemIndex >=0) and (self.__currentItemIndex <= maxLimit)):
			retItem = self.__itemList[self.__currentItemIndex]
		
		return retItem
		
	# Class: InventoryMgr
	#
	# Sets the current inv item.
	# Returns True if item exists, else False
	def set_current_item(self, itemDataIndex):
		retVal = False
		
		if (Item.Is_ItemDataIndex_Valid(itemDataIndex)):
		
			# Convert data index into inv list index for updating
			# the current inv list index.
			itemData = Const.ITEM_DATA_LIST[itemDataIndex]
			itemNameStr = itemData[Const.ITEM_DATA_NAME_INDEX]
			invListIndex = self.get_item_index(itemNameStr)	
			
			if (invListIndex != Const.INVALID_INDEX):
				# successful assignement
				self.__currentItemIndex = invListIndex
				retVal = True
		
		return retVal
		
	# Class: InventoryMgr
	#
	# Add new item to inventory list
	# Returns:
	#	RT_SUCCESS 			- item added successfully
	#	RT_OUT_OF_INV_SPACE	- inventory does not have space for item
	#	RT_FAILURE			- any other failure in adding item
	def add_item(self, newItem):
		
		retStat = Const.RT_SUCCESS
		
		# we have valid item name
		itemIndex = self.get_item_index(newItem.get_name())
		
		if ((itemIndex >= 0) and (itemIndex < len(self.__itemList))):
			# item already exists in list => update existing item counts
			theItem = self.__itemList[itemIndex]
			
			if (theItem.get_typeID() == Const.ITEM_UTILITY_TYPE_ID):
				
				retStat = self.check_capacity_for_item(newItem)
				
				if (retStat == Const.RT_SUCCESS):
				
					theItem.add_count(newItem.get_count())
					
			elif (theItem.get_typeID() == Const.ITEM_WEAPON_TYPE_ID):
				theItem.ammo += newItem.ammo
			else:
				# should never get here
				Utils.Show_Game_Error(Const.INVALID_TYPE_ID_STR)
				retStat = Utils.RT_FAILURE
		else:
			# brand new item to add
			retStat = self.check_capacity_for_item(newItem)
			
			if (retStat == Const.RT_SUCCESS):		
				# we are good to add item to list
				
				# Determine collection index for fast referencing
				listIndex = len (self.__itemList)
				newItem.index = listIndex
				
				self.__itemList.append(newItem) 
				
				Utils.Log_Event("Adding %s to Inventory..." % newItem.get_name()) # TODO: do this in engine
				if (Const.DEBUG_MODE):
					Utils.Log_Event("newItem.index = %d" % newItem.index)
		
		return retStat
		
	# Class: InventoryMgr
	#	
	# Determine if inventory has capacity for given item
	# Returns:
	#	RT_SUCCESS 			- inventory has space to add item
	#	RT_INVALID_PARAMETER- could not access theItem
	#	RT_OUT_OF_INV_SPACE	- inventory does not have space for item
	#	RT_FAILURE			- item size cannot be determined
	def check_capacity_for_item(self, theItem):
		
		retStat = Const.RT_SUCCESS
		
		if (theItem == None):
			retStat = Const.RT_INVALID_PARAMETER
		else:
			itemSize = theItem.get_size()
				
			if (itemSize == Const.INVALID_INDEX): 
				Utils.Show_Game_Error("InventoryMgr::is_capacity_for_item() - could not get size from item: %s" % theItem.get_name())
				retStat = Utils.RT_FAILURE
			else: 
				invSize = itemSize + self.get_total_size()
				
				if (invSize > Const.INV_SIZE_MAX):
					retStat = Const.RT_OUT_OF_INV_SPACE
		
		return retStat
		
	# Class: InventoryMgr
	#	
	# Validity check for item index
	def is_item_index_valid(self, theItem):
		retIndex = Const.INVALID_INDEX
		itemIndex = theItem.index
		
		if ((itemIndex < len(self.__itemList) and (theItem.get_name() == self.__itemList[itemIndex].get_name()))):
			retIndex = itemIndex
			
		return retIndex
	
	# Class: InventoryMgr
	#
	# Updates corresponding list item with given item.
	# Removes any depleted items.
	# Returns True if successful, else False
	def update_item(self, updatedItem):
	
		retVal = True
	
		# first try fast indexing
		itemIndex = self.is_item_index_valid(updatedItem)
		
		isUpdate = False
		
		if (itemIndex != Const.INVALID_INDEX):
			isUpdate = True
		else:
			# something is wrong with the item's assigned index => search list for item
			itemIndex = self.get_item_index(updatedItem.get_name())
			
			if (itemIndex != Const.INVALID_INDEX):
				isUpdate = True
			else:
				Utils.Show_Game_Error("InventoryMgr::update_item() - Unable to update inventory item - %s" % updatedItem.get_name())
		
		if (isUpdate):
			# item found in list
			if (not updatedItem.is_usable()):
				# we have a depleted item => get rid of it
				isUpdate = False
				retVal = self.delete_item(updatedItem)
				
			if (isUpdate):
				self.__itemList[itemIndex] = updatedItem
				retVal = True
		
		return retVal
		
	# Class: InventoryMgr
	#
	# Access item by name
	def get_item(self, itemNameStr):
		retItem = None
		
		itemIndex = self.get_item_index(itemNameStr)
		
		if (itemIndex != Const.INVALID_INDEX):
			tmpItem = self.__itemList[itemIndex]
			
			if (tmpItem.get_name() == itemNameStr):
				retItem = tmpItem
			else:
				# Something went wrong. We got a mismatching item from query.
				Utils.Show_Game_Error("get_item() fail for %s" % itemNameStr)
				
				if (Const.DEBUG_MODE):
					Utils.Log_Event("get_item(): itemNameStr = %s. itemIndex = %d. result name = %s\n" % (itemNameStr, itemIndex, tmpItem.get_name()))
		
		return retItem
		
	# Class: InventoryMgr
	#
	# Returns item index if found in the inv list, else INVALID_INDEX
	def get_item_index(self, itemName):
		
		retIndex = Const.INVALID_INDEX
		count = 0
		
		for item in self.__itemList:
			
			if (item.get_name() == itemName):
				retIndex = count
			
			count += 1
				
		return retIndex
	
	# Class: InventoryMgr
	#
	# Delete given item from itemList.
	# Returns True if successful, else False
	def delete_item(self, theItem):
	
		retVal = False
	
		itemIndex = self.is_item_index_valid(theItem)
		
		if (itemIndex != Const.INVALID_INDEX):
			# we have a valid item
				
			try:	
				del self.__itemList[itemIndex]
				
				# After any deletion (potentially in the middle of list), 
				# need to recalculate each item index to stay accurate.
				self.calculate_item_indices()
				
				Utils.Log_Event("Deleting %s from Inventory..." % theItem.get_name()) # TODO: do this in engine
				retVal = True
				
			except:
				Utils.Show_Game_Error("InventoryMgr::delete_item() - Unable to delete inventory item %s at index %d" % (theItem.get_name(), itemIndex))
		else:
			Utils.Show_Game_Error("Unable to delete inventory item - %s: Invalid Index" % theItem.get_name())
			#TODO: figure out why battery will not delete
			
		return retVal
		
	# Class: InventoryMgr
	#
	# Delete given item based on name.
	# Returns True if successful, else False
	def delete_named_item(self, itemNameStr):
	
		retVal = False
	
		theItem = self.get_item(itemNameStr)
		
		if (theItem == None):
			Utils.Log_Event("InventoryMgr::delete_named_item() - could not get item: %s" % itemNameStr)
		else:
		
			if (theItem.get_typeID() == Const.ITEM_UTILITY_TYPE_ID):
				theItem.subtract_count(1)
				retVal = self.update_item(theItem)
				
			elif (theItem.get_typeID() == Const.ITEM_WEAPON_TYPE_ID):
				# remove weapon entirely from list
				retVal = self.delete_item(theItem)
				
				
		return retVal
			
			
	# Class: InventoryMgr
	#
	# Update index for each item.
	# Done after item deletion.
	def calculate_item_indices(self):
		
		for count in range(0, len (self.__itemList)):
			self.__itemList[count].index = count
		
	# Class: InventoryMgr
	#
	# Display item and their user data
	def print_items(self):
		
		print "%s\nINVENTORY:\n\n" % Const.SEPARATOR_LINE_STR
		print "SIZE: %d\n\n" % self.get_total_size()
		
		itemNum = 1 # start label counting here (even though index starts at 0)
		itemListLen = len(Const.ITEM_DATA_LIST)
		
		for invItem in self.__itemList:
			countNameStr = ""
			invCountStr = ""
			
			if (invItem.get_typeID() == Const.ITEM_UTILITY_TYPE_ID):
				countNameStr = "Count: "
				invCountStr = invItem.get_count()
				
			elif (invItem.get_typeID() == Const.ITEM_WEAPON_TYPE_ID):
				if (invItem.ammo != Const.INFINITE_VAL):
					invCountStr = invItem.ammo
					countNameStr = "Ammo: "
					
			else:
				# should never get here
				Utils.Show_Game_Error(Const.INVALID_TYPE_ID_STR)
				
			# Calculate the correct item index corresponding to hotkeys.
			# This allows the user to use this number to equip item from menu.
			lowIndex = itemNum-1
			highIndex = itemListLen-1
				
			for itemIndex in range(lowIndex,highIndex):
	
				item = Const.ITEM_DATA_LIST[itemIndex]
				
				if (invItem.get_name() == item[Const.ITEM_DATA_NAME_INDEX]):
					itemNum = itemIndex + 1 
					# done looking so quit
					break
				
			print "%d. %s\t\t%s %s\tSize: %d" % (itemNum, invItem.get_name(), countNameStr, invCountStr, invItem.get_size())
			itemNum += 1
		
		print "\n\n%s" % Const.SEPARATOR_LINE_STR
		
	# Class: InventoryMgr
	#
	# Returns size of current item collection
	def get_total_size(self):
		
		retSize = 0
		
		for item in self.__itemList:
			retSize += item.get_size()
		
		return retSize
		
#---------------------------------------------------
#---------------------------------------------------
# Class: Item
#--------------------------------------------------
#---------------------------------------------------		
class Item(object):
	
	__constData = None # TODO: determine if this should be static
	
	def __init__(self):
		# should never get here
		Utils.Show_Game_Error("Item Subclasses handle init implentation.")
		Utils.Exit_Game()
		
	# Class: Item
	#
	# Static item method to determine item data index validity
	@staticmethod
	def Is_ItemDataIndex_Valid(itemDataIndex):
		
		retVal = False
		
		if ((itemDataIndex >= 0) and (itemDataIndex < len(Const.ITEM_DATA_LIST))):
			retVal = True
		
		return retVal
	
	# Class: Item
	#
	# Static item method to determine item validity based on name
	@staticmethod
	def Is_ItemStr_Valid(itemStr):
		
		retVal = False
		
		for item in Const.ITEM_DATA_LIST:
			if (itemStr == item[Const.ITEM_DATA_NAME_INDEX]):
				retVal = True
				# we have a match so quit looking
				break
		
		return retVal
		
	# Class: Item
	#	
	# Static item method to obtain an item's dataList index based on name
	# Returns INVALID_INDEX if no match was found.
	@staticmethod
	def Get_ItemIndex_From_ItemStr(itemStr):
		retIndex = Const.INVALID_INDEX
		
		count = 0
		
		for dataItem in Const.ITEM_DATA_LIST:
			if (dataItem[Const.ITEM_DATA_NAME_INDEX] == itemStr):
				retIndex = count
				break
			else:
				count = count + 1
		
		return retIndex
	
	# Class: Item
	#
	# Static method retrieves itemData from table based on index.
	# NOTE: Always returns a valid itemData obj
	@staticmethod
	def Get_ItemData_From_Index(itemDataIndex):
	
		itemData = None
	
		if (not Item.Is_ItemDataIndex_Valid(itemDataIndex)):
			defaultIndex = 0
			Utils.Show_Game_Error("Item::Get_ItemData_From_Index() - Cannot get item data from index %d... defaulting index to %d!" % (itemDataIndex, defaultIndex))
			itemDataIndex = defaultIndex
			
		itemData = Const.ITEM_DATA_LIST[itemDataIndex]
		
		return itemData
		
	# Class: Item
	#
	# Set constData from index
	def populate_constData(self, itemDataIndex):
	
		self.__constData = self.Get_ItemData_From_Index(itemDataIndex)
			
	# Class: Item
	#
	# Accessor for item name
	# Returns empty string if name could not be accessed
	def get_name(self):
		
		retStr = "" 
		
		if (self.__constData != None):
			retStr = self.__constData[Const.ITEM_DATA_NAME_INDEX]
		
		return retStr
		
	# Class: Item
	#
	# Accessor for item typeID
	# Returns INVALID_INDEX if ID could not be accessed
	def get_typeID(self):
		
		retID = Const.INVALID_INDEX
		
		if (self.__constData != None):
			retID = self.__constData[Const.ITEM_DATA_TYPE_INDEX]
		
		return retID
			
	# Class: Item
	#	
	# Accessor for item size
	# Returns INVALID_INDEX if size could not be accessed
	def get_size(self):
	
		retSize = Const.INVALID_INDEX
		
		if (self.__constData != None):
		
			itemType = self.__constData[Const.ITEM_DATA_TYPE_INDEX]
		
			if (itemType == Const.ITEM_UTILITY_TYPE_ID):
				retSize = self.get_count() * self.__constData[Const.ITEM_DATA_SIZE_INDEX]
			elif (itemType == Const.ITEM_WEAPON_TYPE_ID):
				retSize = self.__constData[Const.ITEM_DATA_SIZE_INDEX]
			else:
				# Should never get here
				Utils.Show_Game_Error("Item::get_size() - invalid item type %d" % itemType)
		
		return retSize
		
		
#---------------------------------------------------
#---------------------------------------------------
# Class: UtilityItem
#--------------------------------------------------
#---------------------------------------------------		
class UtilityItem(Item):
		
	def __init__(self, newDataIndex, newCount):

		self.populate_constData(newDataIndex)
		self.__count = newCount
		self.oid = Const.INVALID_INDEX

		
	# Class: UtilityItem
	#
	# Checks item usability
	def is_usable(self):
	
		retVal = False
		
		if (self.__count > 0):
			retVal = True
			
		return retVal
		
	# Class: UtilityItem
	#
	# Count accessors
	def get_count(self):
		return self.__count

	def set_count(self, newCountNum):
		
		if (newCountNum > 0):
			self.__count = newCountNum
		else:
			self.__count = 0
			
	def add_count(self, countIncrNum):
		self.__count += countIncrNum
		
	def subtract_count(self, countDecrNum):
		tmpVal = self.__count - countDecrNum
		
		if (tmpVal >= 0):
			self.__count = tmpVal
		else:
			self.__count = 0
		
#---------------------------------------------------
#---------------------------------------------------
# Class: WeaponItem
#--------------------------------------------------
#---------------------------------------------------		
class WeaponItem(Item):
	
	def __init__(self, newDataIndex, newAmmo):
		
		self.populate_constData(newDataIndex)
		self.ammo = newAmmo
		self.oid = Const.INVALID_INDEX
		
	# Class: WeaponItem
	#
	# Checks item usability
	def is_usable(self):
	
		retVal = False
		
		if ((self.ammo > 0) or (self.ammo == Const.INFINITE_VAL)):
			retVal = True
			
		return retVal
		
	# Class: WeaponItem
	#
	# Updates count
	def set_count(self, newCount):
		retVal = False
		
		if ((newCount > 0) or (newCount == Const.INFINITE_VAL)):
			self.ammo = newCount
			
		return retVal

#---------------------------------------------------
#---------------------------------------------------
# Class: MapExitItem
#
# Member Variables:	
#       mapIndex	- exit's map location in level
#       pos			- exit position in current map
#		char		- character representation on map
#		linkIndex	- pointer to next map in level
#		linkPos		- exit position in next map
#--------------------------------------------------
#---------------------------------------------------		
class MapExitItem(object):

	def __init__(self,  newMapIndex, newExitPos, newChar, newLinkIndex, linkPos):
	
		self.mapIndex = newMapIndex
		self.pos = newExitPos
		self.linkIndex = newLinkIndex
		self.char = self.__get_valid_char(newChar)
		self.linkPos = linkPos
		Utils.Log_Event("Creating MapExitItem with mapIndex = %d, pos = %s, linkIndex = %d, char = %s" % (self.mapIndex, self.pos.get_str(),  self.linkIndex, self.char))

	# Class: MapExitItem
	#
	# Returns valid version of inChar. Returns inChar unchanged if already valid.
	def __get_valid_char(self, inChar):
		
		retChar = ''
		
		tmpChar = inChar
		charLen = len(inChar)
		
		if (charLen <= 0):
			# default to generic door char
			tmpChar = Const.MAP_CHAR_EXIT_LIST[Const.TILE_ORIENTATION_HOROZONTAL]
		elif(charLen > 1):
			# just use the first character
			tmpChar = inChar[0]
			
		isMatch = False
			
		for doorChar in Const.MAP_CHAR_EXIT_LIST:
			if (doorChar == tmpChar):
				isMatch = True
				break # done looking so quit
				
		if (isMatch):
			retChar = tmpChar
		else:
			# default to generic char
			retChar = Const.MAP_CHAR_EXIT_LIST[Const.TILE_ORIENTATION_HOROZONTAL]
				
		return retChar
		
		
if __name__ == '__main__':	
	Engine.start()