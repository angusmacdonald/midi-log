import re
import logging
import os

import midi

MAX_FILE_SIZE=50000
FILE_PATH='..' + os.sep + 'tests' + os.sep + 'logExample.log'
TRACK_NAME="Log File MIDI"

def getPackageName(line):
	ma = re.match(u'[^\[A-Z]*', line) #End on capital letter (class name) or after entire name.
    
	package = None
	
	if ma:
		package = ma.group()

		#Remove possible trailing dot.
		if package.endswith('.'):
			package = package[:-1]
    
	return package

def splitPackageNames(package):
	names = re.split('[ .]', package)

	return names

if __name__ == '__main__':

	logging.basicConfig(level=logging.DEBUG)

	logging.debug("Starting.")

	FILE = open(FILE_PATH, 'r')

	midiTrack = midi.midiFile(TRACK_NAME, 6) #TODO depth

	i = 0
	while i < MAX_FILE_SIZE:
		line = FILE.readline()

		if line == "": # Cuts off if end of file reached
			break

		package = getPackageName(line)

		logging.debug("FQ Package name: {0}".format(package))

		splitPackage = splitPackageNames(package)
		depth = len(splitPackage)
		isJavaCore = splitPackage[0] == "java"
		logging.debug("Package name array: {0} (depth={1}, isJava={2})".format(splitPackage, depth, isJavaCore))

		midiTrack.addNote(depth)

	midiTrack.writeFile()

