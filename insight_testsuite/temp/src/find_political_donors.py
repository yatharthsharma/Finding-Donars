#!/usr/bin/python
from collections import defaultdict
from utils import *
from runningMedian import median
import time
import heapq
import sys

class mainInterface:
	"""docstring for mainInterface"""

	def __init__(self, inputFile,outputZip,outputDate):

		millisS = int(round(time.time() * 1000))


		self.fileReader = fileReader(inputFile)
		
		#Instance of median class from runningMedianfile
		self.runningMed =  median()

		#hash for date,zip and main hash (see init hash definition)
		self.cmteDateHash ={}
		self.cmteZip ={}
		self.cmte = defaultdict(dict)

		# contains values to be written to file
		self.cmteDateWriter = []
		self.cmteZipWriter = []

		# runs the calculateMedian() which calls everyother code
		self.calculateMedian()
		

		# writing to file
		fw = fileWriter(self.cmteZipWriter,outputZip)
		self.writeCmteDateFile(outputDate,self.cmte)
		

		millisE= int(round(time.time() * 1000))
		
		print (millisE-millisS)/1000.0
	
		# print len(self.cmte)


	def writeCmteDateFile(self,filename,hash):
		"""
			This function sorts cmte ID by alphabetical order and Date by chronological order and saves it to the file
		"""

		for cmteDate in sorted(self.cmteDateHash):
			# print cmteDate
			hVal = hash[cmteDate[0:9]][cmteDate[9:]]
			hVal['median'].sort()
			# print hVal['nTrans']

			size = int(hVal['nTrans'])
			if size%2 == 0:
		
				med = round((hVal['median'][size/2] + hVal['median'][(size/2)-1])/2.0)
			else:
				med = hVal['median'][size/2]
			saveObj = "|".join([str(cmteDate[0:9]),str(hVal['date']),str(int(med)),str(hVal['nTrans']),str(int(hVal["tAmt"]))])
			self.cmteDateWriter.append(saveObj)
			# print saveObj,'\n'
		fw = fileWriter(self.cmteDateWriter,filename)


	def initHash(self,hashObj,key,zipCode=None,dateCode=None):
		"""
			This function create the master hash which is defined as below:
			hash[cmte][zipCode] = {"minH": [],"maxH": [],"nTrans":0,"tAmt": 0}
			hash[cmte][dateCode] = {"median":[],"nTrans":0,"tAmt": 0,"date":0}	
		"""
		if key not in hashObj:
			hashObj[key] = {}

		if zipCode != None and zipCode not in hashObj[key]:
			hashObj[key][zipCode] ={"minH": [],"maxH": [],"nTrans":0,"tAmt": 0}
		elif dateCode!=None and dateCode not in hashObj[key]:
			hashObj[key][dateCode] ={"median":[],"nTrans":0,"tAmt": 0,"date":0}			


	def calculateDateMedian(self,cmte,col,dateRev):
		
		"""
			This function will calculate the values of Date hash i.e  median, nTrans (number of Transaction), tAmt (total Amt), date
			median is calculate by appending the transaction amount in median hash index and sorting it at the end
		"""

		#checking if hash is present else initializing it
		self.initHash(self.cmte,col[0],dateCode=dateRev)

		#making a separte hash for cmte_date combination 
		# This is making the run time faster
		self.cmteDateHash[col[0]+dateRev] = 1

		#calculting the hash values
		self.cmte[col[0]][dateRev]['median'].append(float(col[14]))
		self.cmte[col[0]][dateRev]['nTrans'] +=1
		self.cmte[col[0]][dateRev]['tAmt'] += float(col[14])
		self.cmte[col[0]][dateRev]['date'] = col[13]


	def calculateZipMedian(self,col,zipCode):
			"""
				This function will calculate the values of Zip hash i.e  minH (MinHeap), maxH (MaxHeap), nTrans (number of Transaction), tAmt (total Amt)
				running median is calculated by calling the getMedian function from Median class in runningMedian.py
				runningMedian calculation is done using MinHeap and MaxHeap (see the description in runningMedian.py)
			"""

			#checking if hash is present else initializing it
			self.initHash(self.cmte,col[0],zipCode)

			#calculating running median
			self.runningMed.add(self.cmte,col[0],zipCode,float(col[14]))

			#calculating the values of number of transaction and total amt using the hash(Dict)
			self.cmte[col[0]][zipCode]['nTrans'] +=1
			
			self.cmte[col[0]][zipCode]['tAmt'] += float(col[14])
			# appending the values in a list to be saved in medainval_by_zip.txt at the end
			saveObj = "|".join([col[0],str(zipCode),str(self.runningMed.getMedian(self.cmte,col[0],zipCode)),str(self.cmte[col[0]][zipCode]['nTrans']),str(int(self.cmte[col[0]][zipCode]['tAmt']))])
			self.cmteZipWriter.append(saveObj)

			#TODO: check if this is efficient or not
			# fileW.write("%s\n" %saveObj)
			# zip_file.write(saveObj)



	def calculateMedian(self):
		"""
			This function is the Driver function which calls everything and calculates the median etc.
		"""
		
		for row in self.fileReader:

			col = row.split("|")

			# Checking if line is valid according to CMTE_ID, Others_ID and Transaction Amount
			# TODO : check if col[15] = ' ' is valid or not

			if col[15] or col[0].strip() == "" or col[14].strip() == "":
				try:
					val = float(col[14])
				except:
					continue
				continue
			zipCode = col[10][0:5]
			if len(zipCode)==5 and zipCode.isdigit():
				#TODO check if hashing will be efficent or not
				self.calculateZipMedian(col,zipCode)


			year = col[13][4:]
			dd = col[13][2:4]
			mm = col[13][0:2]

			dateRev = col[13][4:]+col[13][0:4]
			if  validateDate(year,mm,dd,col[13]):	
				self.calculateDateMedian(self.cmte,col,dateRev)



if __name__ == "__main__":

	if len(sys.argv)!=4:
		print "invalid number of arguments need 4.. args - input_file, output_file1, output_file2"
		exit(1)
	# filePath = "../input/test.txt"
	# filePath = "../input/itcont_2018_20170530_20170907.txt"
	# filePath = "../input/itcont_2018_20170908_20171103.txt"
	# filePath = "../input/itcont_2018_20120521_20170529.txt"

	mainInterface(sys.argv[1],sys.argv[2],sys.argv[3])

