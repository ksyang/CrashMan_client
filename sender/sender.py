import sys
import os
import time
import datetime
import requests

pivotTime = 0

def printUsage():
	print ("usage : python sender.py [working directory] [fuzzer name] [fuzzing program] [receiver server IP] [option]")
	print ("""
Option

-a [alias]
	set alias option.
	This is an option that set this crash sender's alias.
	If you do not specify this option, alias will be set default value, None

-p [port]
	set ping port option.
	This is an option that set crash sender's ping check port.
	If you do not specify this option, ping port will be set default value, 1337
		""")

def sendToReceiver(filename, fuzzer, fuzzingProgram, receiverIP, alias, pingPort):
	payload = {'fuzzer' : fuzzer, 'fuzzingProgram' : fuzzingProgram, 'alias' : alias, 'pingPort' : pingPort}
	r = requests.post(receiverIP+"/crash", data=payload)

def searchDir(dirname, fuzzer, fuzzingProgram, receiverIP, alias, pingPort):
	newPivotTime = pivotTime
	filenames = os.listdir(dirname)
	for filename in filenames:								#get files
		full_filename = os.path.join(dirname, filename)		#get file name
		fileCreateTime = datetime.datetime.fromtimestamp(os.path.getctime(full_filename))		#get file created time
		if(fileCreateTime > pivotTime):
			sendToReceiver(filename, fuzzer, fuzzingProgram, receiverIP, alias, pingPort)
			print ("send success!")
			newPivotTime = max(newPivotTime, fileCreateTime)
	return newPivotTime


if __name__ == "__main__":
	argc = len(sys.argv)
	alias = "None"
	pingPort = "None"

	for i in range(0, argc):
		if sys.argv[i][0] == '-':
			if sys.argv[i][1] == 'h':		#help option
				printUsage()
				exit(1)
			if sys.argv[i][1] == 'a':		#set alias option
				if i+1 >= argc:
					print ("error : specify the alias!")
					exit(1)
				alias = sys.argv[i+1]
			if sys.argv[i][1] == 'p':		#set port option
				if i+1 >= argc:
					print ("error : specify the port!")
					exit(1)
				pingPort = sys.argv[i+1]

	if argc < 4:
		printUsage()
		exit(1)

	workDir = sys.argv[1]
	fuzzer = sys.argv[2]
	fuzzingProgram = sys.argv[3]
	receiverIP = sys.argv[4]

	#print ("%s %s %s %s %s" % (workDir, fuzzer, receiverIP, alias, pingPort))

	pivotTime = datetime.datetime.now()
	print ("search start time : [%s]" % str(pivotTime))
	while True:
		time.sleep(1)
		pivotTime = searchDir(workDir, fuzzer, fuzzingProgram, receiverIP, alias, pingPort)