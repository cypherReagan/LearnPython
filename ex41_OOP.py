import random
from urllib import urlopen
import sys

# example call: python ex41.py english

# Globals here
WORD_URL = "http://learncodethehardway.org/words.txt"
WORD_LIST = []

PHRASES_DICT = {
	"class %%%(%%%)":
		"Make a class named %%% that is-a %%%.",
	"class %%%(object): \n\tdef __init__(self, ***)":
		"class %%% has-a __init__ that takes self and *** parameters.",
	"class %%%(object): \n\tdef ***(self, @@@)":
		"class %%% has-a function named *** that takes self and @@@ parameters.",
	"*** = %%%()":
		"Set *** to an instance of class %%%.",
	"***.***(@@@)":
		"From *** get the *** function, and call it with the parameter @@@.",
	"***.*** = '***'":
		"From *** get *** attribute and set it to '***'"
}

# do they want to drill phrases first?
if ((len(sys.argv) == 2) and (sys.argv[1] == "english")):
	PHRASE_FIRST = True
else:
	PHRASE_FIRST = False
	
# load up words from the website
for word in urlopen(WORD_URL).readlines():
	WORD_LIST.append(word.strip())
	
	
# convert snippet in phrases dict
def convert(snippet, phrase):
	classNames = [w.capitalize() for w in 
				  random.sample(WORD_LIST, snippet.count("%%%"))]
				  
	otherNames = random.sample(WORD_LIST, snippet.count("***"))
	resultList = []
	paramNamesList = [] 
	
	for i in range(0, snippet.count("@@@")):
		paramCount = random.randint(1,3)
		paramNamesList.append(','.join(random.samples(WORD_LIST, paramCount)))
		
	for sentence in snippet, phrase:
		result = sentence[:]
		
		# fake class names
		for word in classNames:
			result = result.replace("%%%", word, 1)
			
		# fake other names
		for word in otherNames:
			result = result.replace("***", word, 1)
			
		# fake parameter list
		for word in paramNamesList:
			result = result.replace("@@@", word, 1)
			
		resultList.append(result)
		
	return resultList
	
	
# keep going until user hits CTRL-D
try:
	while True:
		# get list of all phrase keys (code snippets) 
		# and shuffle the
		snippetList = PHRASES_DICT.keys()
		random.shuffle(snippetList)
		
		for snippet in snippetList:
		# use randomly-shuffled key to get current phrase
			phrase = PHRASES_DICT[snippet]
			question, answer = convert(snippet, phrase)
			
			if (PHRASE_FIRST):
				question, answer = answer, question
				
			print question
			
			raw_input("> ")
			print "ANSWER: %s\n\n" % answer
			
except EOFError:
	print "\nEnd of File!"
			
	
