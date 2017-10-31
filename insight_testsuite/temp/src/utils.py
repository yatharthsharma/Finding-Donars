from datetime import datetime
# import re
import collections

def fileReader(file_name):
	try:
		fileR = open(file_name,"r")
		return fileR
	except IOError:
		print "Input file not found. Please check the input path"


def fileWriter(obj,file_name):
	try:
		# print obj
		fileW = open(file_name,"w").write('\n'.join(obj).strip())
		
		# if isZip:
		# 	for data in obj:
		# 		# saveObj = '|'.join([str(i) for i in data.itervalues()])
		# 		saveObj = "|".join(map(str,data))

		# 		# print saveObj
		# 		fileW.write("%s\n" %saveObj)

		# fileW.close()
		# else:
		# 	for cmte in sortedCmte:
		# 		for date in sortedDate:
		# 			# dateRev = date[6:]+date[4:6]+date[0:4]
		# 			# print cmte+dateRev
		# 			saveObj = '|'.join([str(i) for i in obj[cmte+date].itervalues()])
		# 			print saveObj
		# 			fileW.write("%s\n" %saveObj)
			
	except IOError:
		print "Output file not found. Please check the input path"

# def fileClose(fileW):
# 	fileW.close()

def validateDate(year,mm,dd,fullD):
	"""
		This functions validates the format of the input date and validates it

		NOTE: Tried to use datetime.strptime(str(date),format) but the performance was really bad
	"""
	try:
		# match_date = re.compile(r'(\d{2})(\d{2})(\d{4})$').match
		if len(fullD)!=8 or not fullD.isdigit():
			return False
		
		# try except block will handle conversion errors
		year = int(year)
		mm = int(mm)
		dd = int(dd)
		monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
		if(year < 1000 or year > 3000 or mm == 0 or mm > 12):
			return False;

		if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0) :
			monthLength[1] = 29;

		return dd > 0 and dd <= monthLength[mm - 1]
	except:
		return False


