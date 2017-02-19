# -*- coding: utf-8 -*-

# Global Game Data
# This Python file uses the following encoding: utf-8

import Console

DEBUG_MODE = True
GAME_LOG_STR = "GameLog.txt"


# #############################################################################
# Map Keys
# #############################################################################
CORRIDOR_KEY = 'central corridor'
ARMORY_KEY = 'armory'
BRIDGE_KEY = 'bridge'
ESCAPE_POD_KEY = 'escape pod'
DEATH_KEY = 'death'
FINISH_RESULT_KEY = 'done'
TEST_KEY = 'test'
START_KEY = CORRIDOR_KEY

# #############################################################################
# Game String Msgs
# #############################################################################
INVALID_ENTRY_RSP = 'DOES NOT COMPUTE!'
EMPTY_ITEM_STR = '<EMPTY>'
PROMPT_CONTINUE_STR = "[Press ENTER to continue...]> "


INVALID_INDEX = -1

SEPARATOR_LINE_STR = '------------------------------------------------------------------------------------------------'

INFINITE_VAL = -1000

# #############################################################################
# Return Status
# #############################################################################
RT_SUCCESS = 0
RT_FAILURE = 1
RT_INVALID_PARAMETER = 2
RT_NULL_ITEM = 3

RT_OUT_OF_INV_SPACE = 20
# End Status

# #############################################################################
# User Action Commands
# #############################################################################
HELP_REQ_CMD_STR = '?'
QUIT_CMD_STR = 'quit'
ATTACK_CMD_STR = 'attack'
KEYPAD_CMD_STR = 'keypad'
OVERRIDE_CMD_STR = 'hack'
SEARCH_CMD_STR = 'search'
PLAYER_STATS_CMD_STR = 'stats'
PLAYER_INV_CMD_STR = 'inv'

CHEAT_CMD_STR = '-frc'
CC_CHEAT_CMD_STR = CHEAT_CMD_STR + ' cc'
ARMORY_CHEAT_CMD_STR = CHEAT_CMD_STR + ' armory'
BRIDGE_CHEAT_CMD_STR = CHEAT_CMD_STR + ' bridge'
EP_CHEAT_CMD_STR = CHEAT_CMD_STR + ' ep'
FULL_HEALTH_CHEAT_CMD_STR = CHEAT_CMD_STR + ' health++'
SET_HEALTH_CHEAT_CMD_STR = CHEAT_CMD_STR + ' sethealth'
ADD_ITEM_CHEAT_CMD_STR = CHEAT_CMD_STR + ' item++'
DELETE_ITEM_CHEAT_CMD_STR = CHEAT_CMD_STR + ' item--'
DEBUG_MODE_TOGGLE_CMD_STR = CHEAT_CMD_STR + ' dbg'
				
#TODO - make this a list of tuples (str, number) to allow menu referencing				
CMD_STR_LIST = [HELP_REQ_CMD_STR,
				QUIT_CMD_STR,
				ATTACK_CMD_STR,
				KEYPAD_CMD_STR,
				OVERRIDE_CMD_STR,
				SEARCH_CMD_STR,
				PLAYER_STATS_CMD_STR,
				PLAYER_INV_CMD_STR,
				
				CC_CHEAT_CMD_STR,
				ARMORY_CHEAT_CMD_STR,
				BRIDGE_CHEAT_CMD_STR,
				EP_CHEAT_CMD_STR,
				FULL_HEALTH_CHEAT_CMD_STR,
				SET_HEALTH_CHEAT_CMD_STR,
				ADD_ITEM_CHEAT_CMD_STR,
				DELETE_ITEM_CHEAT_CMD_STR,
				
				DEBUG_MODE_TOGGLE_CMD_STR]

# ############################################
# 				ITEM DATA
# ############################################				
	
# Error Msgs
INVALID_TYPE_ID_STR = "Invalid Item Type ID"
	
# Item Strings
ITEM_SLEDGEHAMMER_STR = 'sledgehammer'
ITEM_NET_STR = 'net'
ITEM_KNIFE_STR = 'knife'
ITEM_BLASTER_PISTOL_STR = 'pistol'
ITEM_PLASMA_RIFLE_STR = 'rifle'
ITEM_BATTERY_STR = 'battery'
ITEM_BOMB_STR = 'bomb'

# Item Type IDs
ITEM_UTILITY_TYPE_ID = 0
ITEM_WEAPON_TYPE_ID = 1

# Item Sizes
ITEM_SLEDGEHAMMER_SIZE = 4
ITEM_NET_SIZE = 3
ITEM_KNIFE_SIZE = 1
ITEM_BLASTER_PISTOL_SIZE = 3
ITEM_PLASMA_RIFLE_SIZE = 8
ITEM_BATTERY_SIZE = 1
ITEM_BOMB_SIZE = 1

INV_SIZE_MAX = 10

# Item Damage
ITEM_SLEDGEHAMMER_DAMAGE_NUM = 100
ITEM_NET_DAMAGE_NUM = 100
ITEM_KNIFE_DAMAGE_NUM = 100
ITEM_BLASTER_PISTOL_DAMAGE_NUM = 20
ITEM_PLASMA_RIFLE_DAMAGE_NUM = 80
ITEM_BATTERY_DAMAGE_NUM = INVALID_INDEX
ITEM_BOMB_DAMAGE_NUM = INVALID_INDEX

# Item Range
ITEM_SLEDGEHAMMER_RANGE_NUM = 1
ITEM_NET_RANGE_NUM = 1
ITEM_KNIFE_RANGE_NUM = 1
ITEM_BLASTER_PISTOL_RANGE_NUM = 10
ITEM_PLASMA_RIFLE_RANGE_NUM = 30
ITEM_BATTERY_RANGE_NUM = INVALID_INDEX
ITEM_BOMB_RANGE_NUM = INVALID_INDEX

# Item Type Indices
ITEM_DATA_NAME_INDEX = 0
ITEM_DATA_TYPE_INDEX = 1
ITEM_DATA_SIZE_INDEX = 2
ITEM_DATA_DAMAGE_INDEX = 3
ITEM_DATA_RANGE_INDEX = 4
ITEM_DATA_MAX_INDEX = 4

ITEM_DATA_SLEDGEHAMMER = (	ITEM_SLEDGEHAMMER_STR, 
							ITEM_WEAPON_TYPE_ID, 
							ITEM_SLEDGEHAMMER_SIZE, 
							ITEM_SLEDGEHAMMER_DAMAGE_NUM, 
							ITEM_SLEDGEHAMMER_RANGE_NUM)
							
ITEM_DATA_NET = (	ITEM_NET_STR, 
					ITEM_WEAPON_TYPE_ID, 
					ITEM_NET_SIZE, 
					ITEM_NET_DAMAGE_NUM, 
					ITEM_NET_RANGE_NUM)
					
ITEM_DATA_KNIFE = (	ITEM_KNIFE_STR, 
					ITEM_WEAPON_TYPE_ID, 
					ITEM_KNIFE_SIZE, 
					ITEM_KNIFE_DAMAGE_NUM, 	
					ITEM_KNIFE_RANGE_NUM)
					
ITEM_DATA_BLASTER_PISTOL = (ITEM_BLASTER_PISTOL_STR, 
							ITEM_WEAPON_TYPE_ID, 
							ITEM_BLASTER_PISTOL_SIZE, 
							ITEM_BLASTER_PISTOL_DAMAGE_NUM, 
							ITEM_BLASTER_PISTOL_RANGE_NUM)
							
ITEM_DATA_PLASMA_RIFLE = (	ITEM_PLASMA_RIFLE_STR, 
							ITEM_WEAPON_TYPE_ID, 
							ITEM_PLASMA_RIFLE_SIZE, 
							ITEM_PLASMA_RIFLE_DAMAGE_NUM,
							ITEM_PLASMA_RIFLE_RANGE_NUM)
							
ITEM_DATA_BATTERY = (ITEM_BATTERY_STR,  
					 ITEM_UTILITY_TYPE_ID, 
					 ITEM_BATTERY_SIZE, 
					 ITEM_BATTERY_DAMAGE_NUM,
					 ITEM_BATTERY_RANGE_NUM)
					 
ITEM_DATA_BOMB = (	ITEM_BOMB_STR, 
					ITEM_UTILITY_TYPE_ID, 
					ITEM_BOMB_SIZE, 
					ITEM_BOMB_DAMAGE_NUM,
					ITEM_BOMB_RANGE_NUM)

# Item Indices used as look-up for data list
ITEM_SLEDGEHAMMER_INDEX = 0
ITEM_NET_INDEX = 1
ITEM_KNIFE_INDEX = 2
ITEM_BLASTER_PISTOL_INDEX = 3
ITEM_PLASMA_RIFLE_INDEX = 4
ITEM_BATTERY_INDEX = 5
ITEM_BOMB_INDEX = 6

ITEM_DATA_LIST = [
				 ITEM_DATA_SLEDGEHAMMER,
				 ITEM_DATA_NET,
				 ITEM_DATA_KNIFE, 
				 ITEM_DATA_BLASTER_PISTOL, 
				 ITEM_DATA_PLASMA_RIFLE, 
				 ITEM_DATA_BATTERY,
				 ITEM_DATA_BOMB]
				 

				 

# ############################################
# 				MAP DATA
# ############################################	

MAX_MAP_LOG_ENTRIES = 10

# Map command strings
MAP_CMD_STR_QUIT = 'q'
MAP_CMD_STR_PAUSE = 'p'
MAP_CMD_STR_CMD_PROMPT = 'y'
MAP_CMD_STR_DUMP_DATA = 'l'
MAP_CMD_STR_SHOOT = '\x20'	# space
MAP_CMD_STR_USE = 'e'
MAP_CMD_STR_OBJV = 'o'
MAP_CMD_STR_MOVE_NORTH = 'w'
MAP_CMD_STR_MOVE_WEST = 'a'
MAP_CMD_STR_MOVE_SOUTH = 's'
MAP_CMD_STR_MOVE_EAST = 'd'
MAP_CMD_STR_SLEDGEHAMMER = '1'
MAP_CMD_STR_NET = '2'
MAP_CMD_STR_KNIFE = '3'
MAP_CMD_STR_PISTOL = '4'
MAP_CMD_STR_RIFLE = '5'
MAP_CMD_STR_BATTERY = '6'
MAP_CMD_STR_BOMB = '7'

# ########## Special cmds not entered in the map UI ##########

MAP_CMD_STR_MOVE = 'mv' # summarizes all move cmds in the MapDisplay cmd processing
MAP_CMD_STR_PLACE_ENTITY = 'plc' # entity placement cmd


MAP_CMD_STR_LIST = [
					MAP_CMD_STR_QUIT,
					MAP_CMD_STR_PAUSE,
					MAP_CMD_STR_CMD_PROMPT,
					MAP_CMD_STR_DUMP_DATA,
					MAP_CMD_STR_USE,
					MAP_CMD_STR_OBJV,
					
					MAP_CMD_STR_MOVE,
					MAP_CMD_STR_MOVE_NORTH,
					MAP_CMD_STR_MOVE_WEST,
					MAP_CMD_STR_MOVE_SOUTH,
					MAP_CMD_STR_MOVE_EAST, 
					
					MAP_CMD_STR_SLEDGEHAMMER, 
					MAP_CMD_STR_NET, 
					MAP_CMD_STR_KNIFE, 
					MAP_CMD_STR_PISTOL, 
					MAP_CMD_STR_RIFLE, 
					MAP_CMD_STR_BATTERY, 
					MAP_CMD_STR_BOMB
					]

#TODO: find a better way to accomplish this without duplicates in the lists
MOVE_CMD_STR_LIST = [
					MAP_CMD_STR_MOVE_NORTH,
					MAP_CMD_STR_MOVE_WEST,
					MAP_CMD_STR_MOVE_SOUTH,
					MAP_CMD_STR_MOVE_EAST, 
					]

ITEM_CMD_STR_LIST = [
				MAP_CMD_STR_SLEDGEHAMMER, 
				MAP_CMD_STR_NET, 
				MAP_CMD_STR_KNIFE, 
				MAP_CMD_STR_PISTOL, 
				MAP_CMD_STR_RIFLE, 
				MAP_CMD_STR_BATTERY, 
				MAP_CMD_STR_BOMB]

LEVEL_EXIT_NUM = -2 # exit that triggers player map level completion


# Map Obj directions
DIR_INVALID = INVALID_INDEX
DIR_NORTH = 0
DIR_SOUTH = 1
DIR_EAST = 2
DIR_WEST = 3

DIR_STR_LIST = ["North", "South", "East", "West"]

#DEBUG_JW - might not need this
DIR_DICT = {DIR_NORTH	: "North",
			DIR_SOUTH 	: "South",
			DIR_EAST	: "East",
			DIR_WEST	: "West"}

# Map Obj categories
# WARNING!!!
# must be in sync with MAP_CHARS_LIST
MAP_CAT_WALL = 0
MAP_CAT_OPEN_SPACE = 1
MAP_CAT_PLAYER = 2
MAP_CAT_ENEMY = 3
MAP_CAT_EXIT = 4
MAP_CAT_SOLID_SPACE = 5
MAP_CAT_LINE_FEED = 6
MAP_CAT_ITEM = 7



# Map Obj characters
MAP_CHAR_WALL_LIST = [u'▄',u'▐']			# 0
MAP_CHAR_OPEN_SPACE = u'░'					# 1
MAP_CHAR_PLAYER_LIST = ['^','v','>','<']	# 2
MAP_CHAR_ENEMY_LIST = ['W','M','E','3']		# 3
MAP_CHAR_EXIT_LIST = ['=',u'║']				# 4
MAP_CHAR_SOLID_SPACE = u'▓'					# 5
MAP_CHAR_LINE_FEED = '\n'					# 6
MAP_CHAR_ITEM = '$'							# 7


# Default Map Obj characters colors -> use category as index
# Order: Forground, Background, Format
							
DEFAULT_CHAR_COLOR_LIST = [ (Console.DEFAULT_COLOR, Console.WHITE, 			INVALID_INDEX), 
							(Console.DEFAULT_COLOR, Console.DEFAULT_COLOR,	INVALID_INDEX),
							(Console.GREEN, 		Console.DEFAULT_COLOR,	Console.BOLD),
							(Console.YELLOW, 		Console.DEFAULT_COLOR,	Console.BOLD),
							(Console.DEFAULT_COLOR, Console.DEFAULT_COLOR,	Console.UNDERLINE),
							(Console.DEFAULT_COLOR, Console.DEFAULT_COLOR,	INVALID_INDEX),
							(Console.DEFAULT_COLOR, Console.DEFAULT_COLOR,	INVALID_INDEX),
							(Console.MAGENTA, 		Console.DEFAULT_COLOR,	INVALID_INDEX)]


MAP_CHAR_OPEN_SPACE_ASCII = '`'
MAP_CHAR_PLAYER_ASCII = '+'
MAP_CHAR_ENEMY_ASCII = 'v'
MAP_CHAR_DOOR_ASCII = '='
MAP_CHAR_SOLID_SPACE_ASCII = '#'

MAP_CHAR_WALL_LIST_ASCII = ['_','|','-']

MAP_CHARS_LIST = [	MAP_CHAR_WALL_LIST,
					[MAP_CHAR_OPEN_SPACE],
					MAP_CHAR_PLAYER_LIST,
					MAP_CHAR_ENEMY_LIST,
					MAP_CHAR_EXIT_LIST,
					[MAP_CHAR_SOLID_SPACE],
					[MAP_CHAR_LINE_FEED], 
					[MAP_CHAR_ITEM]]
					
# Tile orientation
TILE_ORIENTATION_HOROZONTAL = 0
TILE_ORIENTATION_VERTICAL = 1

TILE_ORIENTATION_MAX_NUM = 2


				
# Tile layers
MAP_TILE_LAYER_INDEX_FLOOR = 0
MAP_TILE_LAYER_INDEX_STAND = 1

MAP_TILE_LAYERS_NUM = 2

MAP_TILE_LAYER_LIST = [MAP_TILE_LAYER_INDEX_FLOOR, MAP_TILE_LAYER_INDEX_STAND]
				
# Files containing level data
LEVEL_DATA_FILE_CC_STR = "CcData.txt"
LEVEL_DATA_FILE_AMORY_STR = "AmoryData.txt"
LEVEL_DATA_FILE_BRIDGE_STR = "BridgeData.txt"
LEVEL_DATA_FILE_ESCAPE_STR = "EscapeData.txt"
					
# Game Maps
MAP_BRIDGE_STR1_TEST = """
\u00de\u0220\u0220\u0220\u0220====\u0220
\u0176\u0176\u0176\u0176\u0176\u0176\u0176\u0176  
"""

MAP_BRIDGE_STR1_UCODE = u"""
▐▄▄▄▄▄▄▄====▄
▐░░░░░░░░@░░▐
▐░░░░░░░░░░░▐
▐░░░░░░░░░░░▐
▐░░░░░░░░░░░▐
▐░░░░░░░░░░░▐
▐░░░░░░░░░░░▐
▐░░░░░░░░░░░▐
▐▄▄▄░░░░░░░░▐
▐▓▓▐░░░░░░░░▐
▐▓▓▐░░░░░░░░▐
▐▓▓▐░░░░░░░░▐
▐▄▄▐░░░░░░░░▐
▐░░░░░░░░░░░▐
▐░░░░░░░░░░░▐
▐░░░░░░▐▄▄▄▄▐
▐░░░░░░▐▓▓▓▓▐
▐░░░░░░▐▓▓▓▓▐
▐░░░░░░▐▄▄▄▄▐
▐░░░░+░░░░░░▐
▐▄▄▄==▄▄▄▄▄▄▐
"""

MAP_CC_STR1_UCODE = u"""
▐▄▄▄▄▄▄▄=▄▄=▄
▐░░░░░░░░░░░▐
▐░░░░░░░░░░░▐
▐▄▄▄▄▄▄▄░░░░▐
▐▓▓▓▓▓▓▐░░░░▐
▐▓▓▓▓▓▓▐░░░░▐
▐▄▄▄▄▄▄▐░░░░▐
▐░░░░░░░░░░░▐
▐░░░░░░▐▄▄▄▄▐
▐░░░░░░▐▄▄▄▄▐
▐░░░░░░░░░░░▐
▐▄▄▄▄=▄▄▄▄▄▄▐
"""

MAP_TEST_STR1_UCODE = u"""
▐▄▄▄▄▄▄▄▄▄▄▄▄
▐░░░░░░░░░░░▐
▐░░░░░░░░░░░▐
▐▄▄▄▄=▄▄▄▄▄▄▐
"""

MAP_TEST_STR2_UCODE = u"""
▐▄▄▄▄▄▄▄▄▄▄=▄
▐▓▓▓▓▓▓▐░░░░▐
▐▓▓▓▓▓▓▐░░░░▐
▐▄▄▄▄▄▄▄▄▄▄=▐
"""

MAP_BRIDGE_STR1_ASCII = """
________====_ 
|`````@`````|
|```````````|
|```````````|
|```````````|
|```````````|
|```````````|
|```````````|
|__`````````|
|##|````````|
|##|````````|
|##|````````|
|__|````````|
|```````````|
|```````````|
|```````____|
|``````|####|
|``````|####|
|``````|____|
|````+``````|
|___==______|
"""

# ############################################
# 				MAP DATA
# ############################################	

# http://www.network-science.de/ascii/
ART_STR_GAME_TITLE = """
		  ________        __  .__                          
		 /  _____/  _____/  |_|  |__ _____    ____   ______
		/   \  ___ /  _ \   __\  |  \\__  \  /    \ /  ___/
		\    \_\  (  <_> )  | |   Y  \/ __ \|   |  \\___ \ 
		 \________/\____/|__| |___|  (______/___|  /______>
		   _____   __    __                 __    
		  /  _  \_/  |__/  |______    ____ |  | __
		 /  /_\  \   __\   __\__  \ _/ ___\|  |/ /
		/    |    \  |  |  |  / __ \\  \___|    < 
		\____|____/__|  |__| (______/\_____>__|__\\
		
		"""

# http://www.incredibleart.org/links/ascii/ScarecrowGifGalle.html
# From: pirillc2770_cobra_uni_edu
# TODO: fix the shift
ART_STR_SKULL =  """
		
		      .... NO! ...                 ... MNO! ...
		    ..... MNO!! ...................... MNNOO! ...
		 ..... MMNO! ......................... MNNOO!! .
		.... MNOONNOO!   MMMMMMMMMMPPPOII!   MNNO!!!! .
		 ... !O! NNO! MMMMMMMMMMMMMPPPOOOII!! NO! ....
		    ...... ! MMMMMMMMMMMMMPPPPOOOOIII! ! ...
		   ........ MMMMMMMMMMMMPPPPPOOOOOOII!! .....
		   ........ MMMMMOOOOOOPPPPPPPPOOOOMII! ...
		    ....... MMMMM..    OPPMMP    .,OMI! ....
                     ...... MMMM::   o.,OPMP,.o ::I!!   ...
                         .... NNM:::.,,OOPM!P,.::::!! ....
                          .. MMNNNNNOOOOPMO!!IIPPO!!O! .....
                         ... MMMMMNNNNOO:!!:!!IPPPPOO! ....
                           .. MMMMMNNOOMMNNIIIPPPOO!! ......
                          ...... MMMONNMMNNNIIIOO!..........
                       ....... MN MOMMMNNNIIIIIO! OO ..........
                    ......... MNO! IiiiiiiiiiiiI OOOO ...........
		  ...... NNN.MNO! . O!!!!!!!!!O . OONO NO! ........
		   .... MNNNNNO! ...OOOOOOOOOOO . MMNNON!........
		   ...... MNNNNO! .. PPPPPPPPP .. MMNON!........
		      ...... OO! ................. ON! .......
                            ...............................
		
		"""

GameOverMsg = """
  ________    _____      _____  ___________
 /  _____/   /  _  \    /     \ \_   _____/
/   \  ___  /  /_\  \  /  \ /  \ |    __)_ 
\    \_\  \/    |    \/    Y    \|        \ 
 \______  /\____|__  /\____|__  /_______  /
        \/         \/         \/        \/
____________   _________________________
\_____  \   \ /   /\_   _____/\______   \ 
 /   |   \   Y   /  |    __)_  |       _/
/    |    \     /   |        \ |    |   \ 
\_______  /\___/   /_______  / |____|_  /
        \/                 \/         \/ 
"""

OverrideDiagram2Wire = """
		-------------   -------------   
		|  Keypad   |   |   Door    |   
		|  Output   |   |   Input   | 
		-------------   -------------   
		    | |             | |             
		    | |             | |            
		    | |             | |             
		    | |             | |            
		    | |             | |             
		   -----           -----           
		"""
		
OverrideDiagram2Wire_Seed = '\t\t    %s          %s'
		
OverrideDiagram3Wire = """
		-------------   -------------   -------------
		|  Keypad   |   |   Door    |   |  Battery  |
		|  Output   |   |   Input   |   |           |
		-------------   -------------   -------------
		     | |             | |             | |
		     | |             | |             | |
		     | |             | |             | |
		     | |             | |             | |
		     | |             | |             | |
		    -----           -----           -----
		
		"""
		
OverrideDiagram3Wire_Seed = '\t\t    %s          %s          %s'




if __name__ == '__main__':	
	Engine.start()