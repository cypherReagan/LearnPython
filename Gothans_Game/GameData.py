# Global Game Data

INVALID_INDEX = -1

# Map Obj directions
DIR_INVALID = 0
DIR_NORTH = 1
DIR_SOUTH = 2
DIR_EAST = 3
DIR_WEST = 4

# Map Obj categories
MAP_CAT_OPEN_SPACE = 1
MAP_CAT_WALL = 2
MAP_CAT_PLAYER = 3
MAP_CAT_ENEMY = 4
MAP_CAT_DOOR = 5
MAP_CAT_SOLID_SPACE = 6


# Map Obj characters
MAP_CHAR_OPEN_SPACE = '`'
MAP_CHAR_PLAYER = '+'
MAP_CHAR_ENEMY = '@'
MAP_CHAR_DOOR = '='
MAP_CHAR_SOLID_SPACE = '#'
MAP_CHAR_LINE_FEED = '\n'

MAP_CHAR_WALL_LIST = ['_','|','-']
MAP_CHAR_LIST_ENEMY = [MAP_CHAR_ENEMY]

MAP_CHARS_LIST = [	MAP_CHAR_WALL_LIST,
					[MAP_CHAR_OPEN_SPACE],
					[MAP_CHAR_PLAYER],
					[MAP_CHAR_LIST_ENEMY],
					[MAP_CHAR_DOOR],
					[MAP_CHAR_SOLID_SPACE],
					[MAP_CHAR_LINE_FEED]]
					
					
# Game Maps
MAP_BRIDGE_STR1 = """
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
					