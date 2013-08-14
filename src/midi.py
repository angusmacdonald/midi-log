from midiutil.MidiFile import MIDIFile

import logging

# Tracks are numbered from zero. Times are measured in beats.
track = 0  

class midiFile:
	"""
		Allows MIDI files to be gradually built up.

		On creation, a MIDI file track is created, and notes are added through calls
		to addNote.

		The file can be saved through a call to writeFile.

		More information on the library being used at:
			http://www.emergentmusics.org/mididutil-class-reference
	"""

	def __init__(self, trackName, maxDepth):
		self.state = MIDIFile(1) #Number of tracks.
		
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

	def writeFile(self, savePath):
		""" Write the current state of the MIDI file to disk.

			savePath: Name+Path of the MIDI file to be saved.
		"""
		binfile = open(savePath, 'wb')
		self.state.writeFile(binfile)
		binfile.close()


def getPitch(depth, maxDepth):
	"""	Changes pitch based on a given package structure depth
		Pitch is between 0-127.
	"""
	pitch = (float(depth) / maxDepth) * 127
	logging.debug("Pitch: {0}, Depth: {1}, Max: {2}".format(pitch, depth, maxDepth))
	return pitch


