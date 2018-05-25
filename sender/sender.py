import sys
import os
import time
import datetime

pivotTime = 0

def sendToReceiver(filename, fuzzer):
	print(filename)
	print(fuzzer)

def searchDir(dirname, fuzzer):
	newPivotTime = pivotTime
	filenames = os.listdir(dirname)
	for filename in filenames:								#get files
		full_filename = os.path.join(dirname, filename)		#get file name
		fileCreateTime = datetime.datetime.fromtimestamp(os.path.getctime(full_filename))		#get file created time
		if(fileCreateTime > pivotTime):
			sendToReceiver(filename, fuzzer)
			newPivotTime = max(newPivotTime, fileCreateTime)
	return newPivotTime


if __name__ == "__main__":
	argc = len(sys.argv)
	if argc < 3:
		print "usage : python sender.py [working directory] [fuzzer name]"
		exit(1)
	workDir = sys.argv[1]
	fuzzer = sys.argv[2]

	pivotTime = datetime.datetime.now()
	print ("search start time : [%s]" % str(pivotTime))
	while True:
		time.sleep(1)
		pivotTime = searchDir(workDir, fuzzer)