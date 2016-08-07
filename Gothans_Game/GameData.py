# -*- coding: utf-8 -*-

# Global Game Data
# This Python file uses the following encoding: utf-8

DEBUG_MODE = True
GAME_LOG_STR = "GameLog.txt"

# Map Keys
CORRIDOR_KEY = 'central corridor'
ARMORY_KEY = 'armory'
BRIDGE_KEY = 'bridge'
ESCAPE_POD_KEY = 'escape pod'
DEATH_KEY = 'death'
FINISH_RESULT_KEY = 'done'
#START_KEY = CORRIDOR_KEY # DEBUG_JW: Put this back after testing!
START_KEY = BRIDGE_KEY

# Game String Msgs
INVALID_ENTRY_RSP = 'DOES NOT COMPUTE!'
EMPTY_ITEM_STR = '<EMPTY>'
PROMPT_CONTINUE_STR = "[Press ENTER to continue...]> "


INVALID_INDEX = -1

SEPARATOR_LINE_STR = '------------------------------------------------------------------------------------------------'

INFINITE_VAL = -1000

# User Action Commands
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

# Item Strings
ITEM_SLEDGEHAMMER_STR = 'sledgehammer'
ITEM_NET_STR = 'net'
ITEM_KNIFE_STR = 'knife'
ITEM_BLASTER_PISTOL_STR = 'pistol'
ITEM_PLASMA_RIFLE_STR = 'rifle'
ITEM_BATTERY_STR = 'battery'
ITEM_BOMB_STR = 'bomb'


ITEM_STR_LIST = [
				 ITEM_SLEDGEHAMMER_STR,
				 ITEM_NET_STR,
				 ITEM_KNIFE_STR, 
				 ITEM_BLASTER_PISTOL, 
				 ITEM_PLASMA_RIFLE, 
				 ITEM_BATTERY_STR,
				 ITEM_BOMB_STR]
				 

				 
				 
MAX_MAP_LOG_ENTRIES = 10

# Map command strings
MAP_CMD_STR_QUIT = 'q'
MAP_CMD_STR_PAUSE = 'p'
MAP_CMD_STR_CMD_PROMPT = 'y'
MAP_CMD_STR_DUMP_DATA = 'l'
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

# Special cmd not entered in the map UI but used to 
# summarize all move cmds in the MapDisplay cmd processing.
MAP_CMD_STR_MOVE = 'mv' 

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

MAP_EXIT_NUM = 9999


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
MAP_CAT_WALL = 0
MAP_CAT_OPEN_SPACE = 1
MAP_CAT_PLAYER = 2
MAP_CAT_ENEMY = 3
MAP_CAT_EXIT = 4
MAP_CAT_SOLID_SPACE = 5
MAP_CAT_LINE_FEED = 6



# Map Obj characters
MAP_CHAR_OPEN_SPACE = u'░'
MAP_CHAR_PLAYER = '+'
MAP_CHAR_ENEMY = '@'
MAP_CHAR_DOOR = '='
MAP_CHAR_SOLID_SPACE = u'▓'
MAP_CHAR_LINE_FEED = '\n'

MAP_CHAR_OPEN_SPACE_ASCII = '`'
MAP_CHAR_PLAYER_ASCII = '+'
MAP_CHAR_ENEMY_ASCII = '@'
MAP_CHAR_DOOR_ASCII = '='
MAP_CHAR_SOLID_SPACE_ASCII = '#'

MAP_CHAR_WALL_LIST = [u'▐','|',u'▄']
MAP_CHAR_WALL_LIST_ASCII = ['_','|','-']

MAP_CHAR_LIST_ENEMY = [MAP_CHAR_ENEMY]

MAP_CHARS_LIST = [	MAP_CHAR_WALL_LIST,
					[MAP_CHAR_OPEN_SPACE],
					[MAP_CHAR_PLAYER],
					MAP_CHAR_LIST_ENEMY,
					[MAP_CHAR_DOOR],
					[MAP_CHAR_SOLID_SPACE],
					[MAP_CHAR_LINE_FEED]]
					
					
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
▐░░░░░░░░@░+▐
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
▐░░░░+░░░░░░▐
▐▄▄▄▄=▄▄▄▄▄▄▐
"""

MAP_TEST_STR2_UCODE = u"""
▐▄▄▄▄▄▄▄▄▄▄=▄
▐▓▓▓▓▓▓▐░░░░▐
▐▓▓▓▓▓▓▐░░░+▐
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

# ASCII art

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