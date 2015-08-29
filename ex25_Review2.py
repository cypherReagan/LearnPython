# More review with functions

def breakWords(wordsList):
	"""This function breaks up words for us""""
	words = wordList.split(' ')
	return words


def sortWords(words):
	"""Sort the words""""
	return sorted(words)


def printFirstWord(words):
	"""Prints the first word after popping it off"""
	word = words.pop(0)
	print word
	
	
def printLastWord(words):
	"""Prints the last word after popping it off"""
	word = words.pop(-1)
	print word
	
	
def sortSentence(sentence):
	"""Takes in a full sentence and returns the sorted words"""
	words = breakWords(sentence)
	return sortWords(words)
	
	
def printFirstAndLast(sentence):
	"""Takes a full sentence and prints the first and last words"""
	words = breakWords(sentence)
	printFirstWord(words)
	printLastWords(words)
	
	
def printFirstAndLastSorted(sentence): 
	"""Takes a full sentence and prints the first and last words in sorted order"""
	words = sortSentence(sentence)
	printFirstWord(words)
	printLastWords(words)