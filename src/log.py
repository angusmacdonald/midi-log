import re
import logging
import os

import midi
import tree

MAX_FILE_SIZE=50000
FILE_PATH='..' + os.sep + 'tests' + os.sep + 'logExample.log'
OUTPUT_PATH='..' + os.sep + 'output' + os.sep + 'output.mid'
TRACK_NAME="Log File MIDI"

class midiLogger:
	def __init__(self, filePath, instrumentDepth):
		self.filePath = filePath
		self.instrumentDepth = instrumentDepth
		self.tree = tree.PackageTree()
	def __setUpInstrumentation(self):
		FILE = open(self.filePath, 'r')

		i = 0
		while i < MAX_FILE_SIZE:
			line = FILE.readline()

			if line == "": # Cuts off if end of file reached
				break
			if line == "\n":
				continue

			package = getPackageName(line)

			self.tree.add(package)
	def __createMidiFile(self, pathToWriteTo, bpm):
		FILE = open(FILE_PATH, 'r')

		midiTrack = midi.midiFile(TRACK_NAME, self.tree.getLargestDepth(), bpm)

		i = 0
		while i < MAX_FILE_SIZE:
			line = FILE.readline()

			if line == "": # Cuts off if end of file reached
				break
			if line == "\n":
				continue

			package = getPackageName(line)

			depth = tree.getDepth(package)

			midiTrack.addNote(depth, self.tree.getInstrumentAtDepth(package, self.instrumentDepth))

		midiTrack.writeFile(pathToWriteTo)
	def create(self, pathToWriteTo, bpm):
		self.__setUpInstrumentation()
		self.__createMidiFile(pathToWriteTo,bpm)

def getPackageName(line):
	ma = re.match(u'[^\[A-Z]*', line) #End on capital letter (class name) or after entire name.
    
	package = None
	
	if ma:
		package = ma.group()

		#Remove possible trailing dot.
		if package.endswith('.'):
			package = package[:-1]
    
	return package

if __name__ == '__main__':

	logging.basicConfig(level=logging.INFO)

	logging.debug("Starting.")

	parser = midiLogger(FILE_PATH, 2)

	parser.create(OUTPUT_PATH, 100)

