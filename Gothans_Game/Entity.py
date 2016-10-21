# DESCRIPTION: 
#		Module contains implementation for all entities featured in game map

import GameData
import Utils

#---------------------------------------------------
#---------------------------------------------------
# Class: Actor
#--------------------------------------------------
#---------------------------------------------------		
class Actor(object):
	
	
	def __init__(self):
		self.reset_data()
		
	def reset_data(self):
		self.__health = 100
		self.xp = 0
		self.theInventoryMgr = InventoryMgr()
		self.__dir = GameData.DIR_NORTH
		self.Id = GameData.INVALID_INDEX
		
		# start with default melee weapons
		# TODO: ultimately allow player to find these in map
		self.theInventoryMgr.add_item(WeaponItem(GameData.ITEM_SLEDGEHAMMER_INDEX, GameData.INFINITE_VAL))
		self.theInventoryMgr.add_item(WeaponItem(GameData.ITEM_NET_INDEX, GameData.INFINITE_VAL))
		self.theInventoryMgr.add_item(WeaponItem(GameData.ITEM_KNIFE_INDEX, GameData.INFINITE_VAL))
		#DEBUG_JW - this is for testing
		self.theInventoryMgr.add_item(UtilityItem(GameData.ITEM_BATTERY_INDEX, 1))
		
	def get_health(self):
		return self.__health
		
	def set_health(self, healthVal):
		
		if (healthVal > 100):
			self.__health = 100
		elif (healthVal < 0):
			self.__health = 0
			
	def get_dir_num(self):
		return self.__dir
		
	def get_dir_str(self):
		dirStr = GameData.DIR_DICT.get(self.__dir)
		return dirStr
	
	# Updates actor's direction.
	# Returns True if successful, else False
	def set_dir(self, newDir):
		retVal = False
		
		if ((newDir >= 0) and (newDir < len(GameData.DIR_STR_LIST))):
			self.__dir = newDir
			retVal = True
			Utils.Log_Event("Changing actor Dir to %d" % self.__dir)
			
		else:
			Utils.Log_Event("Invalid change attempt of actor Dir to %d" % newDir)
			
			return retVal
			
	def add_health(self, healthVal):
		self.__health += healthVal
		
	def subtract_health(self, healthVal):
		if ((self.__health - healthVal) < 0):
			self.__health = 0
		else:
			self.__health -= healthVal
			
			
	def get_current_itemStr(self):
		retStr = GameData.EMPTY_ITEM_STR
		
		currentItem = self.theInventoryMgr.get_current_item()
		if (currentItem != None):
			retStr = currentItem.get_name()
		
		return retStr
		
		
	def equip_item(self,  itemDataIndex):
		
		return self.theInventoryMgr.set_current_item(itemDataIndex)
		

		
	def print_stats(self):
		print "%s\n\nPLAYER STATS:\n\nHEALTH = %d\nXP = %d\n\n%s" % (GameData.SEPARATOR_LINE_STR, self.get_health(), self.xp, GameData.SEPARATOR_LINE_STR)
		
		
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
	
	# TODO - determine why these cannot go in init()
	__itemList = []
	__currentItemIndex = GameData.INVALID_INDEX
		
	# Accessors for current item
	def get_current_item(self):
		retItem = None
		
		maxLimit = len(self.__itemList) -1
		
		if ((self.__currentItemIndex >=0) and (self.__currentItemIndex <= maxLimit)):
			retItem = self.__itemList[self.__currentItemIndex]
		
		return retItem
		
	# Sets the current inv item.
	# Returns True if item exists, else False
	def set_current_item(self, itemDataIndex):
		retVal = False
		
		if (Item.is_itemDataIndex_valid(itemDataIndex)):
		
			# Convert data index into inv list index for updating
			# the current inv list index.
			itemData = GameData.ITEM_DATA_LIST[itemDataIndex]
			itemNameStr = itemData[GameData.ITEM_DATA_NAME_INDEX]
			invListIndex = self.get_item_index(itemNameStr)	
			
			if (invListIndex != GameData.INVALID_INDEX):
				# successful assignement
				self.__currentItemIndex = invListIndex
				retVal = True
		
		return retVal
		
	# Add new item to inventory list
	# Returns:
	#	RT_SUCCESS 			- item added successfully
	#	RT_OUT_OF_INV_SPACE	- inventory does not have space for item
	#	RT_FAILURE			- any other failure in adding item
	def add_item(self, newItem):
		
		retStat = GameData.RT_SUCCESS
		
		# we have valid item name
		itemIndex = self.get_item_index(newItem.get_name())
		
		if ((itemIndex >= 0) and (itemIndex < len(self.__itemList))):
			# item already exists in list => update existing item counts
			theItem = self.__itemList[itemIndex]
			
			if (theItem.get_typeID() == GameData.ITEM_UTILITY_TYPE_ID):
				
				retStat = self.check_capacity_for_item(newItem)
				
				if (retStat == GameData.RT_SUCCESS):
				
					theItem.add_count(newItem.get_count())
					
			elif (theItem.get_typeID() == GameData.ITEM_WEAPON_TYPE_ID):
				theItem.ammo += newItem.ammo
			else:
				# should never get here
				Utils.Show_Game_Error(GameData.INVALID_TYPE_ID_STR)
				retStat = Utils.RT_FAILURE
		else:
			# brand new item to add
			retStat = self.check_capacity_for_item(newItem)
			
			if (retStat == GameData.RT_SUCCESS):		
				# we are good to add item to list
				
				# Determine collection index for fast referencing
				listIndex = len (self.__itemList)
				newItem.index = listIndex
				
				self.__itemList.append(newItem) 
				
				Utils.Log_Event("Adding %s to Inventory..." % newItem.get_name())
				Utils.Log_Event("DEBUG_JW:newItem.index = %d" % newItem.index)
		
		return retStat
		
		
	# Determine if inventory has capacity for given item
	# Returns:
	#	RT_SUCCESS 			- inventory has space to add item
	#	RT_OUT_OF_INV_SPACE	- inventory does not have space for item
	#	RT_FAILURE			- item size cannot be determined
	def check_capacity_for_item(self, theItem):
		
		retStat = GameData.RT_SUCCESS
		
		itemSize = theItem.get_size()
			
		if (itemSize == GameData.INVALID_INDEX): 
			Utils.Show_Game_Error("InventoryMgr::is_capacity_for_item() - could not get size from item: %s" % theItem.get_name())
			retStat = Utils.RT_FAILURE
		else: 
			invSize = itemSize + self.get_total_size()
			
			if (invSize > GameData.INV_SIZE_MAX):
				retStat = GameData.RT_OUT_OF_INV_SPACE
		
		return retStat
		
		
	def is_item_index_valid(self, theItem):
		retIndex = GameData.INVALID_INDEX
		itemIndex = theItem.index
		
		Utils.Log_Event("DEBUG_JW: InventoryMgr.is_item_index_valid() - item arg = %s item arg index = %d\n, %s item index is %d and itemList len = %d\n" % (theItem.get_name(), theItem.index, self.__itemList[itemIndex].get_name(), itemIndex, len(self.__itemList)))
		
		if ((itemIndex < len(self.__itemList) and (theItem.get_name() == self.__itemList[itemIndex].get_name()))):
			retIndex = itemIndex
			
		return retIndex
	
	
	# Updates corresponding list item with given item.
	# Removes any depleted items.
	# Returns True if successful, else False
	def update_item(self, updatedItem):
	
		retVal = True
	
		# first try fast indexing
		itemIndex = self.is_item_index_valid(updatedItem)
		
		isUpdate = False
		
		if (itemIndex != GameData.INVALID_INDEX):
			isUpdate = True
		else:
			# something is wrong with the item's assigned index => search list for item
			itemIndex = self.get_item_index(updatedItem.get_name())
			
			if (itemIndex != GameData.INVALID_INDEX):
				isUpdate = True
			else:
				Utils.Show_Game_Error("Unable to update inventory item - %s" % updatedItem.get_name())
		
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
		
	def get_item(self, itemNameStr):
		retItem = None
		
		itemIndex = self.get_item_index(itemNameStr)
		
		if (itemIndex != GameData.INVALID_INDEX):
			tmpItem = self.__itemList[itemIndex]
			
			if (tmpItem.get_name() == itemNameStr):
				retItem = tmpItem
			else:
				# Something went wrong. We got a mismatching item from query.
				Utils.Show_Game_Error("get_item() fail for %s" % itemNameStr)
				
				if (GameData.DEBUG_MODE):
					Utils.Log_Event("get_item(): itemNameStr = %s. itemIndex = %d. result name = %s\n" % (itemNameStr, itemIndex, tmpItem.get_name()))
		
		return retItem
		
		
	# Returns item index if found in the inv list, else INVALID_INDEX
	def get_item_index(self, itemName):
		
		retIndex = GameData.INVALID_INDEX
		count = 0
		
		for item in self.__itemList:
			
			if (item.get_name() == itemName):
				retIndex = count
			
			count += 1
				
		return retIndex
	
	
	# Delete given item from itemList.
	# Returns True if successful, else False
	def delete_item(self, theItem):
	
		retVal = False
	
		itemIndex = self.is_item_index_valid(theItem)
		
		if (itemIndex != GameData.INVALID_INDEX):
			# we have a valid item
				
			try:	
				del self.__itemList[itemIndex]
				
				# After any deletion (potentially in the middle of list), 
				# need to recalculate each item index to stay accurate.
				self.calculate_item_indices()
				
				Utils.Log_Event("Deleting %s from Inventory..." % theItem.get_name())
				retVal = True
				
			except:
				Utils.Show_Game_Error("Unable to delete inventory item %s at index %d" % (theItem.get_name(), itemIndex))
		else:
			Utils.Show_Game_Error("Unable to delete inventory item - %s: Invalid Index" % theItem.get_name())
			#TODO: figure out why battery will not delete
			
		return retVal
		
	
	# Delete given item based on name.
	# Returns True if successful, else False
	def delete_named_item(self, itemNameStr):
	
		retVal = False
	
		theItem = self.get_item(itemNameStr)
		
		if (theItem == None):
			Utils.Log_Event("InventoryMgr::delete_named_item() - could not get item: %s" % itemNameStr)
		else:
		
			if (theItem.get_typeID() == GameData.ITEM_UTILITY_TYPE_ID):
				theItem.subtract_count(1)
				retVal = self.update_item(theItem)
				
			elif (theItem.get_typeID() == GameData.ITEM_WEAPON_TYPE_ID):
				# remove weapon entirely from list
				retVal = self.delete_item(theItem)
				
				
		return retVal
			
			
		
	def calculate_item_indices(self):
		
		for count in range(0, len (self.__itemList)):
			self.__itemList[count].index = count
		
	
	def print_items(self):
		
		print "%s\nINVENTORY:\n\n" % GameData.SEPARATOR_LINE_STR
		print "SIZE: %d\n\n" % self.get_total_size()
		
		itemNum = 1 # start label counting here (even though index starts at 0)
		itemListLen = len(GameData.ITEM_DATA_LIST)
		
		for invItem in self.__itemList:
			countNameStr = ""
			invCountStr = ""
			
			if (invItem.get_typeID() == GameData.ITEM_UTILITY_TYPE_ID):
				countNameStr = "Count: "
				invCountStr = invItem.get_count()
				
			elif (invItem.get_typeID() == GameData.ITEM_WEAPON_TYPE_ID):
				if (invItem.ammo != GameData.INFINITE_VAL):
					invCountStr = invItem.ammo
					countNameStr = "Ammo: "
					
			else:
				# should never get here
				Utils.Show_Game_Error(GameData.INVALID_TYPE_ID_STR)
				
			# Calculate the correct item index corresponding to hotkeys.
			# This allows the user to use this number to equip item from menu.
			lowIndex = itemNum-1
			highIndex = itemListLen-1
				
			for itemIndex in range(lowIndex,highIndex):
	
				item = GameData.ITEM_DATA_LIST[itemIndex]
				
				if (invItem.get_name() == item[GameData.ITEM_DATA_NAME_INDEX]):
					itemNum = itemIndex + 1 
					# done looking so quit
					break
				
			print "%d. %s\t\t%s %s\tSize: %d" % (itemNum, invItem.get_name(), countNameStr, invCountStr, invItem.get_size())
			itemNum += 1
		
		print "\n\n%s" % GameData.SEPARATOR_LINE_STR
		
		
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
	
	__constData = None
	
	def __init__(self):
		# should never get here
		Utils.Show_Game_Error("Item Subclasses handle init implentation.")
		Utils.Exit_Game()
		
	
	# Static item method to determine item data index validity
	@staticmethod
	def is_itemDataIndex_valid(itemDataIndex):
		
		retVal = False
		
		if ((itemDataIndex >= 0) and (itemDataIndex < len(GameData.ITEM_DATA_LIST))):
			retVal = True
		
		return retVal
	
	# Static item method to determine item validity based on name
	@staticmethod
	def is_itemStr_valid(itemStr):
		
		retVal = False
		
		for item in GameData.ITEM_DATA_LIST:
			if (itemStr == item[GameData.ITEM_DATA_NAME_INDEX]):
				retVal = True
				# we have a match so quit looking
				break
		
		return retVal
		
	# Static item method to obtain an item's dataList index based on name
	# Returns INVALID_INDEX if no match was found.
	@staticmethod
	def get_itemIndex_from_itemStr(itemStr):
		retIndex = GameData.INVALID_INDEX
		
		count = 0
		
		for dataItem in GameData.ITEM_DATA_LIST:
			if (dataItem[GameData.ITEM_DATA_NAME_INDEX] == itemStr):
				retIndex = count
				break
			else:
				count = count + 1
		
		return retIndex
	

	# Static method retrieves itemData from table based on index.
	# NOTE: Always returns a valid itemData obj
	@staticmethod
	def get_itemData_from_index(itemDataIndex):
	
		itemData = None
	
		if (not Item.is_itemDataIndex_valid(itemDataIndex)):
			defaultIndex = 0
			Utils.Show_Game_Error("Cannot get item data from index %d... defaulting index to %d!" % (itemIndex, defaultIndex))
			itemDataIndex = defaultIndex
			
		itemData = GameData.ITEM_DATA_LIST[itemDataIndex]
		
		return itemData
		
	# Set constData from index
	def populate_constData(self, itemDataIndex):
	
		self.__constData = self.get_itemData_from_index(itemDataIndex)
		
		if (self.__constData == None):
			Utils.Show_Game_Error("Could not get itemData from index %d!" % itemDataIndex)
			
	
	# Accessor for item name
	# Returns empty string if name could not be accessed
	def get_name(self):
		
		retStr = "" 
		
		if (self.__constData != None):
			retStr = self.__constData[GameData.ITEM_DATA_NAME_INDEX]
		
		return retStr
		
	# Accessor for item typeID
	# Returns INVALID_INDEX if ID could not be accessed
	def get_typeID(self):
		
		retID = GameData.INVALID_INDEX
		
		if (self.__constData != None):
			retID = self.__constData[GameData.ITEM_DATA_TYPE_INDEX]
		
		return retID
			
		
	# Accessor for item size
	# Returns INVALID_INDEX if size could not be accessed
	def get_size(self):
	
		retSize = GameData.INVALID_INDEX
		
		if (self.__constData != None):
		
			itemType = self.__constData[GameData.ITEM_DATA_TYPE_INDEX]
		
			if (itemType == GameData.ITEM_UTILITY_TYPE_ID):
				retSize = self.get_count() * self.__constData[GameData.ITEM_DATA_SIZE_INDEX]
			elif (itemType == GameData.ITEM_WEAPON_TYPE_ID):
				retSize = self.__constData[GameData.ITEM_DATA_SIZE_INDEX]
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
	
	# default unique members to invalid values
	__count = GameData.INVALID_INDEX
		
	def __init__(self, newDataIndex, newCount):

		self.populate_constData(newDataIndex)
		self.__count = newCount
		self.Id = GameData.INVALID_INDEX

		
	
	def is_usable(self):
	
		retVal = False
		
		if (self.__count > 0):
			retVal = True
			
		return retVal
		
	
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

	# default unique members to invalid values
	ammo = GameData.INVALID_INDEX
	
	def __init__(self, newDataIndex, newAmmo):
		
		self.populate_constData(newDataIndex)
		self.ammo = newAmmo
		self.Id = GameData.INVALID_INDEX
		
		
	def is_usable(self):
	
		retVal = False
		
		if ((self.ammo > 0) or (self.ammo == GameData.INFINITE_VAL)):
			retVal = True
			
		return retVal
		
		
	def set_count(self, newCount):
		retVal = False
		
		if ((newCount > 0) or (newCount == GameData.INFINITE_VAL)):
			self.ammo = newCount
			
		return retVal

#---------------------------------------------------
#---------------------------------------------------
# Class: MapExitItem
#
# Member Variables:	
#		linkIndex	- pointer to next map
#--------------------------------------------------
#---------------------------------------------------		
class MapExitItem(object):

	def __init__(self, newMapIndex=GameData.INVALID_INDEX):
		self.linkIndex = newMapIndex
		Utils.Log_Event("Creating MapExitItem with linkIndex = %d" % self.linkIndex)

