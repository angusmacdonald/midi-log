from midiutil.MidiFile import MIDIFile

import logging


class midiFile:
	"""
		Allows MIDI files to be gradually built up.

		On creation, a MIDI file track is created, and notes are added through calls
		to addNote.

		The file can be saved through a call to writeFile.

		More information on the library being used at:
			http://www.emergentmusics.org/mididutil-class-reference
	"""

	def __init__(self, trackName, maxPackageDepth, bpm):
		self.state = MIDIFile(1) #Number of tracks.
		
		self.time = 0
		self.track = 0
		self.state.addTempo(self.track,self.time,bpm)
		self.maxPackageDepth = maxPackageDepth
		self.minPitch = 0	
		self.maxPitch = 127

	def setPitchRange(self, min, max):
		""" Set the range (somewhere between 0-127) that will be used in assigning pitch to notes,
			which is based on package depth.
		"""
		self.minPitch = min
		self.maxPitch = max

	def addNote(self, depth, instrument, duration):
		"""	Adds a new note to the MIDI file.
			Increments the time by 1 on addition of every note.

			depth: Package structure depth. Used to determine the pitch of the note.
			instrument: Number from 0-127 (see: http://en.wikipedia.org/wiki/General_MIDI#Program_change_events)
			duration: Number of beats note should be played over.
		"""

		channel = 0
		pitch = getPitch(depth, self.maxPackageDepth, self.minPitch, self.maxPitch)

		volume = 127

		logging.info("Adding note, with instrument {0}, pitch {1}, duration {2}".format(instrument, pitch, duration))
		self.state.addProgramChange(self.track,channel, self.time, instrument)
		self.state.addNote(0,channel,pitch,self.time,duration,volume)

		self.time+=1

	def writeFile(self, savePath):
		""" Write the current state of the MIDI file to disk.

			savePath: Name+Path of the MIDI file to be saved.
		"""
		binfile = open(savePath, 'wb')
		self.state.writeFile(binfile)
		binfile.close()


def getPitch(depth, maxPackageDepth, minPitch, maxPitch):
	"""	Changes pitch based on a given package structure depth
		Pitch is between 0-127 (or another value specified by setPitchRange())
	"""
	pitch = ((float(depth) / maxPackageDepth) * (maxPitch-minPitch)) + minPitch
	logging.info("Pitch: {0}, Depth: {1}, Max Package: {2}, Min: {3}, Max: {4}".format(pitch, depth, maxPackageDepth, minPitch, maxPitch))
	return pitch


