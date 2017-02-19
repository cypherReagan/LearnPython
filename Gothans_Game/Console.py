# -*- coding: utf-8 -*-

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
	
	#uCodeStr = u'Ω'
	#print "%s" % uCodeStr
	
	print "%sWarning: No active formats remain. Continue?%s\n" % (bcolor.Get_ColorStr(MAGENTA), bcolor.Get_ColorStr(ENDC))
	print "It is \033[31mnot\033[39m intelligent to use \033[32mhardcoded ANSI\033[39m \033[1mcodes!\033[0m"
	print "It is \033[31m\033[47mnot\033[39m\033[49m intelligent to use \033[92mhardcoded ANSI\033[39m \033[1mcodes!\033[0m"
	endColorStr = bcolor.Get_ColorStr(ENDC)
	defaultColorStr = bcolor.Get_ColorStr(DEFAULT_COLOR)
	whiteStr = bcolor.Get_ColorStr(WHITE)
	cyanStr = bcolor.Get_ColorStr(CYAN)
	magentaStr = bcolor.Get_ColorStr(MAGENTA)
	blueStr = bcolor.Get_ColorStr(BLUE)
	yellowStr = bcolor.Get_ColorStr(YELLOW)
	greenStr = bcolor.Get_ColorStr(GREEN)
	redStr = bcolor.Get_ColorStr(RED)
	redBoldStr = bcolor.Get_ColorStr(BOLD) + bcolor.Get_ColorStr(RED)
	blackStr = bcolor.Get_ColorStr(UNDERLINE) + bcolor.Get_ColorStr(BLACK)
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
		
		if (bcolor.Is_Valid_ColorNum(foreColorNum)):
			self.__colorList[bcolor.FOREGROUND_INDEX] = foreColorNum
		
		if (bcolor.Is_Valid_ColorNum(backColorNum)):
			self.__colorList[bcolor.BACKGROUND_INDEX] = backColorNum
			
		self.add_format(colorFormatNum)

	@staticmethod
	def Is_Valid_ColorNum(colorNum):
		
		retVal = False
		
		# normalize incoming number
		startColorNum = colorNum - DEFAULT_COLOR
		
		if ((startColorNum >= 0) and (startColorNum < len(bcolor.COLOR_NUM_LIST))):
			retVal = True
		
		return retVal
		
	@staticmethod
	def Is_Valid_Color_FormatNum(colorFormatNum):
		
		retVal = False
		
		if ((colorFormatNum >= 0) and (colorFormatNum < len(bcolor.COLOR_FORMAT_STR_LIST))):
			retVal = True
		
		return retVal
		
	# returns color format string based on number
	@staticmethod
	def Get_ColorStr(colorNum, isBackground=False):

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
		
		startCharColor = bcolor.Get_ColorStr(self.__colorList[bcolor.FOREGROUND_INDEX]) + bcolor.Get_ColorStr(self.__colorList[bcolor.BACKGROUND_INDEX], True)
		endCharColor = bcolor.Get_ColorStr(ENDC)
		
		return startCharColor + self.__formatStr + inChar + endCharColor
	
	
	def set_colorNum(self, colorNum, index):
		
		rStat = Const.RT_FAILURE
		
		if ((index >= 0) and (index < len(self.__colorList))):
			if (Is_Valid_ColorNum(colorNum)):
				self.__colorList[index] = colorNum
				rStat = Const.RT_SUCCESS
		
		return rStat
		
	def reset_format(self):
		self.__formatStr = ''
		
	def add_format(self, colorFormatNum):
	
		if (bcolor.Is_Valid_Color_FormatNum(colorFormatNum)):
			self.__formatStr += bcolor.COLOR_FORMAT_STR_LIST[colorFormatNum]
			
			
	def get_str(self):
	
		retStr = "(%d,%d)" % (self.__colorList[bcolor.FOREGROUND_INDEX], self.__colorList[bcolor.BACKGROUND_INDEX])
		
		return retStr

	


	
