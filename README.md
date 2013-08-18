midi-log
========

Python project thatcreates a MIDI file by parsing a Java log file.

Used to 'listen' to the running of your Java program.

The package structure of the log message is used to determine the tone and pitch of the sound that is played.

### Current Status

Currently supports parsing of a basic single-line java logger, where the package name is the first part of the log message.