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
	''' 
	'''
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
		self.tree.printState()
	def __createMidiFile(self, pathToWriteTo, bpm, minPitch, maxPitch):
		FILE = open(FILE_PATH, 'r')

		midiTrack = midi.midiFile(TRACK_NAME, self.tree.getLargestDepth(), bpm)

		midiTrack.setPitchRange(minPitch, maxPitch)

		i = 0
		while i < MAX_FILE_SIZE:
			line = FILE.readline()

			if line == "": # Cuts off if end of file reached
				break
			if line == "\n":
				continue

			package = getPackageName(line)

			depth = tree.getDepth(package)

			midiTrack.addNote(depth, self.tree.getInstrumentAtDepth(package, self.instrumentDepth), 5)

		midiTrack.writeFile(pathToWriteTo)
	def create(self, pathToWriteTo, bpm=120, minPitch=0, maxPitch=127):
		"""	Create a new MIDI file based on the parsed log file.

			pathToWriteTo: Where the MIDI file will be save.
			bpm: Beats per minute in the MIDI file. Defaults to 120.
			minPitch: The lowest pitch to be used (per line pitch is determined based on package depth). Defaults to 0.
			maxPitch: The highest pitch to be used. Defaults to 127 (max value).
		"""
		self.__setUpInstrumentation()
		self.__createMidiFile(pathToWriteTo,bpm, minPitch, maxPitch)
	def setInstruments(self, packageToInstrument):
		for key, value in packageToInstrument:
			self.tree.setCustomInstrument(key, value)
	def setInstrument(self, package, instrument):
		self.tree.setCustomInstrument(package, instrument)

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

	parser = midiLogger(FILE_PATH, 4)
	parser.create(OUTPUT_PATH, 500, 20, 60)

