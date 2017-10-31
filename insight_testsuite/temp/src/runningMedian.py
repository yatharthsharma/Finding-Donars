import heapq
class median:
	"""
		This class calculates the running median using 2 heap min and max
		
	"""

	def add(self,hash,key,subkey,amount):

	
		if len(hash[key][subkey]["maxH"]) == 0:
			heapq.heappush(hash[key][subkey]["maxH"],-1*amount)
			return

		elif amount <= -1*hash[key][subkey]["maxH"][0]:
			heapq.heappush(hash[key][subkey]["maxH"],-1*amount)

		else:
			heapq.heappush(hash[key][subkey]["minH"],amount)

		sizeMin = len(hash[key][subkey]["minH"])
		sizeMax = len(hash[key][subkey]["maxH"])	
		
		if  sizeMax -sizeMin == 2:
			heapq.heappush(hash[key][subkey]["minH"],-1*heapq.heappop(hash[key][subkey]["maxH"]))
		elif sizeMin -sizeMax == -2:
			heapq.heappush(hash[key][subkey]["maxH"],-1*heapq.heappop(hash[key][subkey]["minH"]))


	def getMedian(self,hash,key,subkey):

		if len(hash[key][subkey]["maxH"]) == len(hash[key][subkey]["minH"]):
			return int(round((-1*hash[key][subkey]["maxH"][0] + hash[key][subkey]["minH"][0])/2.0))

		return int(round(-1*hash[key][subkey]["maxH"][0])) if len(hash[key][subkey]["maxH"]) > len(hash[key][subkey]["minH"]) else round(int(hash[key][subkey]["minH"][0]))







		














