from midiutil.MidiFile import MIDIFile

import logging

# Tracks are numbered from zero. Times are measured in beats.
track = 0  

#Documentation at: http://www.emergentmusics.org/mididutil-class-reference
class midiFile:

	def __init__(self, trackName, maxDepth):
		self.state = MIDIFile(1) #Num of tracksself.self.state.addTrackName(track,time,trackName)
		
		self.time = 0
		self.state.addTempo(track,self.time,120)
		self.maxDepth = maxDepth

	def addNote(self, depth):
		"""	Adds a new note to the MIDI file.
			Increments the time by 1 on addition of every note.

			depth: Package structure depth. Used to determine the pitch of the note.
		"""
		track = 0
		channel = 20
		pitch = getPitch(depth, self.maxDepth)
		duration = 1
		volume = 127

		logging.debug("Adding note.")

		self.state.addNote(track,channel,pitch,self.time,duration,volume)

		self.time+=1

	def writeFile(self):
		""" Write the current state of the MIDI file to disk.
		"""
		binfile = open("../output/output.mid", 'wb')
		self.state.writeFile(binfile)
		binfile.close()


def getPitch(depth, maxDepth):
	"""	Changes pitch based on a given package structure depth
		Pitch is between 0-127.
	"""
	pitch = (float(depth) / maxDepth) * 127
	logging.debug("Pitch: {0}, Depth: {1}, Max: {2}".format(pitch, depth, maxDepth))
	return pitch


