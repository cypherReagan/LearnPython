import SharedConst as Const


# #############################################################################
# ANSI CONSOLE FORMATTING
# #############################################################################

ENDC = 0 # end color = '\033[0m'
BOLD = 1 #'\033[1m'
UNDERLINE = 2 #'\033[4m'

DEFAULT_COLOR = 3 #'\033[39m'
WHITE = 4 #'\033[37m'
CYAN = 5 #'\033[36m'
MAGENTA = 6 #'\033[35m'
BLUE = 7 #'\033[34m'
YELLOW = 8 #'\033[33m'
GREEN = 9 #'\033[32m'
RED = 10 #'\033[31m'
BLACK = 11 #'\033[30m'


	
def test_formatting():
	#theBcolor = bcolors()
	print "%sWarning: No active formats remain. Continue?%s\n" % (bcolor.get_colorStr(MAGENTA), bcolor.get_colorStr(ENDC))
	print "It is \033[31mnot\033[39m intelligent to use \033[32mhardcoded ANSI\033[39m \033[1mcodes!\033[0m"
	print "It is \033[31m\033[47mnot\033[39m\033[49m intelligent to use \033[92mhardcoded ANSI\033[39m \033[1mcodes!\033[0m"
	endColorStr = bcolor.get_colorStr(ENDC)
	defaultColorStr = bcolor.get_colorStr(DEFAULT_COLOR)
	whiteStr = bcolor.get_colorStr(WHITE)
	cyanStr = bcolor.get_colorStr(CYAN)
	magentaStr = bcolor.get_colorStr(MAGENTA)
	blueStr = bcolor.get_colorStr(BLUE)
	yellowStr = bcolor.get_colorStr(YELLOW)
	greenStr = bcolor.get_colorStr(GREEN)
	redStr = bcolor.get_colorStr(RED)
	redBoldStr = bcolor.get_colorStr(BOLD) + bcolor.get_colorStr(RED)
	blackStr = bcolor.get_colorStr(UNDERLINE) + bcolor.get_colorStr(BLACK)
	print "%sDEFAULT%s %sWHITE%s %sCYAN%s %sMAGENTA%s %sBLUE%s %sYELLOW%s %sGREEN%s %sRED%s %sRED_BOLD%s %sBLACK_UNDERLINE%s" % (defaultColorStr, endColorStr, whiteStr, endColorStr, cyanStr, endColorStr, magentaStr, endColorStr, blueStr, endColorStr, yellowStr, endColorStr, greenStr, endColorStr, redStr, endColorStr, redBoldStr, endColorStr, blackStr, endColorStr)
	raw_input(Const.PROMPT_CONTINUE_STR)
	
#---------------------------------------------------
#---------------------------------------------------
# Class: bcolor
#
# Member Variables:	
#	__colorList	- color number of foreground and background
#	__formatStr	- character formatting string
#	
#---------------------------------------------------
#---------------------------------------------------			
class bcolor:

	FORMAT_ESC_MODE_MAX = 107
	FORMAT_ESC_CHAR = '\033['
	FORMAT_TXT_SEQ = 'm'
	BACKGROUND_COLOR_NUM_OFFSET = 10
	
	COLOR_FORMAT_STR_LIST = ['\033[0m', '\033[1m', '\033[4m'] # [ENDC, BOLD, UNDERLINE]
	COLOR_NUM_LIST = [39, 37, 36, 35, 34, 33, 32, 31, 30] # use ANSI color indices

	FOREGROUND_INDEX = 0
	BACKGROUND_INDEX = 1

	def __init__(self, foreColorNum, backColorNum, colorFormatNum):
		
		self.__colorList = [0,0]
		self.__clear()
		
		if (bcolor.is_valid_colorNum(foreColorNum)):
			self.__colorList[bcolor.FOREGROUND_INDEX] = foreColorNum
		
		if (bcolor.is_valid_colorNum(backColorNum)):
			self.__colorList[bcolor.BACKGROUND_INDEX] = backColorNum
			
		self.add_format(colorFormatNum)

	@staticmethod
	def is_valid_colorNum(colorNum):
		
		retVal = False
		
		# normalize incoming number
		startColorNum = colorNum - DEFAULT_COLOR
		
		if ((startColorNum >= 0) and (startColorNum < len(bcolor.COLOR_NUM_LIST))):
			retVal = True
		
		return retVal
		
	@staticmethod
	def is_valid_color_formatNum(colorFormatNum):
		
		retVal = False
		
		if ((colorFormatNum >= 0) and (colorFormatNum < len(bcolor.COLOR_FORMAT_STR_LIST))):
			retVal = True
		
		return retVal
		
	# returns color format string based on number
	@staticmethod
	def get_colorStr(colorNum, isBackground=False):

		retStr = ''
		
			
		if (colorNum >= 0):
			if (colorNum < (len(bcolor.COLOR_FORMAT_STR_LIST))):
				retStr = bcolor.COLOR_FORMAT_STR_LIST[colorNum]
			else:
				# normalize color index
				colorNum -= len(bcolor.COLOR_FORMAT_STR_LIST)
				if (colorNum < (len(bcolor.COLOR_NUM_LIST))):
					colorIndex = bcolor.COLOR_NUM_LIST[colorNum]
				
				if (isBackground):
					colorIndex += bcolor.BACKGROUND_COLOR_NUM_OFFSET
					
				retStr = "%s%d%s" % (bcolor.FORMAT_ESC_CHAR, colorIndex, bcolor.FORMAT_TXT_SEQ)
			
		return retStr 
		
			
	def __clear(self):
		self.__colorList[bcolor.FOREGROUND_INDEX] = DEFAULT_COLOR
		self.__colorList[bcolor.BACKGROUND_INDEX] = DEFAULT_COLOR + bcolor.BACKGROUND_COLOR_NUM_OFFSET
		self.__formatStr = ''
		
		
	def get_painted_char(self, inChar):
	
		retChar = ''
		
		startCharColor = bcolor.get_colorStr(self.__colorList[bcolor.FOREGROUND_INDEX]) + bcolor.get_colorStr(self.__colorList[bcolor.BACKGROUND_INDEX], True)
		endCharColor = bcolor.get_colorStr(ENDC)
		
		return startCharColor + self.__formatStr + inChar + endCharColor
	
	
	def set_colorNum(self, colorNum, index):
		
		rStat = Const.RT_FAILURE
		
		if ((index >= 0) and (index < len(self.__colorList))):
			if (is_valid_colorNum(colorNum)):
				self.__colorList[index] = colorNum
				rStat = Const.RT_SUCCESS
		
		return rStat
		
	def reset_format(self):
		self.__formatStr = ''
		
	def add_format(self, colorFormatNum):
	
		if (bcolor.is_valid_color_formatNum(colorFormatNum)):
			self.__formatStr += bcolor.COLOR_FORMAT_STR_LIST[colorFormatNum]
			
			
	def get_str(self):
	
		retStr = "(%d,%d)" % (self.__colorList[bcolor.FOREGROUND_INDEX], self.__colorList[bcolor.BACKGROUND_INDEX])
		
		return retStr

	


	
