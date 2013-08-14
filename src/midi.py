from midiutil.MidiFile import MIDIFile

import logging

# Tracks are numbered from zero. Times are measured in beats.
track = 0   
time = 0

class midiFile:

	def __init__(self, trackName):
		self.state = MIDIFile(1) #Num of tracksself.self.state.addTrackName(track,time,trackName)
		self.state.addTempo(track,time,120)

	def addNote(self):
		track = 0
		channel = 20
		pitch = 60
		time = 0
		duration = 1
		volume = 100

		logging.debug("Adding note.")

		self.state.addNote(track,channel,pitch,time,duration,volume)

	def writeFile(self):
		binfile = open("../output/output.mid", 'wb')
		self.state.writeFile(binfile)
		binfile.close()