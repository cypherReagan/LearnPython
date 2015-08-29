# implementation of HashMap data structure

def new(numBuckets=256):
	"""Initialize a Map with a given number of buckets"""
	aMap = []
	
	for i in range(0, numBuckets):
		# Each hash map has a list of buckets which is a 
		# list of items containing a key and a value
		aMap.append([])
		
	return aMap
	
	
def hashKey(aMap, key):
	"""Given a key this will create a number and then convert it to an index for aMap's bucket"""
	return hash(key) % len(aMap)
	
	
def getBucket(aMap, key):
	"""Given a key, find the bucket where would go"""
	# This ID is gauranteed to be in range of aMap size
	bucketID = hashKey(aMap, key)
	# try an assert anyways
	assert (bucketID <= len(aMap))
	
	return aMap[bucketID]
	
	
def getSlot(aMap, key, default=None):
	"""
	Returns the key, index, and value of a slot found in the bucket.
	Returns -1, key, and defualt(None if not set) when not found.
	"""
	retIndex =  -1
	retKey = key
	retVal = default
	
	bucket = getBucket(aMap, key)
	
	for i, keyVal in enumerate(bucket):
		k, v = keyVal
		if (key == k):
			retIndex = i
			retKey = k
			retVal = v
	
	return retIndex, retKey, retVal
	
	
def get(aMap, key, default=None):
	"""Get the value in a bucket for a given key, or the default"""
	tmpIndex, tmpKey, tmpVal = getSlot(aMap, key, default)
	
	return tmpVal
	
	
def set(aMap, key, value):
	"""Sets the key of the value replacing any existing value"""
	bucket = getBucket(aMap, key)
	tmpIndex, tmpKey, tmpVal = getSlot(aMap, key)
	
	if (tmpIndex >= 0):
		# the key exists => replace it
		bucket[tmpIndex] =(key, value)
	else:
		# the key does not exists => append to create it
		bucket.append((key, value))
	
	
def delete(aMap, key):
	"""Deletes the given key from the Map"""
	bucket = getBucket(aMAp, key)
	
	for i in xrange(len(bucket)):
		k, v = bucket[i]
		if (k == key):
			del bucket[i]
			break
			
	
def list(aMap):
	"""Prints out what's in the map"""
	for bucket in aMap:
		if bucket:
			for k,v in bucket:
				print k, v
	

def dump(aMap):
	"""Prints everything"""
	for bucket in aMap:
		if bucket:
			for k,v in bucket:
				print k, v
		
		
		
		
		
		
		