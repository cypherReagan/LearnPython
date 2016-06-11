# -*- coding: utf-8 -*-

# Global Game Data
# This Python file uses the following encoding: utf-8

DEBUG_MODE = False
GAME_LOG_STR = "GameLog.txt"

# Game String Msgs
INVALID_ENTRY_RSP = 'DOES NOT COMPUTE!'
EMPTY_ITEM_STR = '<EMPTY>'
PROMPT_CONTINUE_STR = "[Press any key to continue...]> "


INVALID_INDEX = -1

Separator_Line = '------------------------------------------------------------------------------------------------'

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
ITEM_BATTERY_STR = 'battery'
ITEM_BOMB_STR = 'bomb'
ITEM_SLEDGEHAMMER_STR = 'sledgehammer'
ITEM_NET_STR = 'net'
ITEM_KNIFE_STR = 'knife'

ITEM_STR_LIST = [ITEM_BATTERY_STR,
				 ITEM_BOMB_STR,
				 ITEM_SLEDGEHAMMER_STR,
				 ITEM_NET_STR,
				 ITEM_KNIFE_STR]

# Map command strings
MAP_CMD_STR_QUIT = 'q'
MAP_CMD_STR_PAUSE = 'p'
MAP_CMD_DUMP_DATA = 'l'
MAP_CMD_STR_MOVE_NORTH = 'w'
MAP_CMD_STR_MOVE_WEST = 'a'
MAP_CMD_STR_MOVE_SOUTH = 's'
MAP_CMD_STR_MOVE_EAST = 'd'

MAP_CMD_STR_LIST = [
					MAP_CMD_STR_QUIT,
					MAP_CMD_DUMP_DATA,
					
					MAP_CMD_STR_MOVE_NORTH,
					MAP_CMD_STR_MOVE_WEST,
					MAP_CMD_STR_MOVE_SOUTH,
					MAP_CMD_STR_MOVE_EAST
					]

# Map Obj directions
DIR_INVALID = 0
DIR_NORTH = 1
DIR_SOUTH = 2
DIR_EAST = 3
DIR_WEST = 4

# Map Obj categories
MAP_CAT_WALL = 0
MAP_CAT_OPEN_SPACE = 1
MAP_CAT_PLAYER = 2
MAP_CAT_ENEMY = 3
MAP_CAT_DOOR = 4
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

MAP_BRIDGE_STR2_UCODE = u"""
▐▄▄▄▄▄▄▄====▄
▐░░░░░░░░@░░▐
▐▄▄▄▄▄▄▄░░░░▐
▐▓▓▓▓▓▓▐░░░░▐
▐▓▓▓▓▓▓▐░░░░▐
▐▄▄▄▄▄▄▐░░░░▐
▐░░░░░░░░░░░▐
▐░░░░░░▐▄▄▄▄▐
▐░░░░░░▐▄▄▄▄▐
▐░░░░+░░░░░░▐
▐▄▄▄==▄▄▄▄▄▄▐
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