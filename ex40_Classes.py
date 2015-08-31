# An example of class implementation

class Song(object):
	
	def __init__(self, lyrics):
		self.lyrics = lyrics
		
	
	def singSong(self):
		for line in self.lyrics:
			print line
			
			
			
happyBday = Song(["Happy birthday to you ",
				 "I don't want to get sued",
				 "So I'll stop right here"])
				 
bullsOnParade = Song(["They rally round tha family",
					  "With a pocket full of shells"])
					  

happyBday.singSong()
bullsOnParade.singSong()