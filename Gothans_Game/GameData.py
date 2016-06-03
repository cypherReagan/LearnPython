# -*- coding: utf-8 -*-

# Global Game Data
# This Python file uses the following encoding: utf-8

# Game String Msgs
INVALID_ENTRY_RSP = 'DOES NOT COMPUTE!'

INVALID_INDEX = -1

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