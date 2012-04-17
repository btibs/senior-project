#!/usr/bin/env python

import sys
#sys.path.append("/scratch/showerLib/beth/")
sys.path.append("C:\\Users\\Julie\\Desktop\\beth\\Senior Project\\sim\\")
import corsika
import matplotlib

# currently does stuff / appears to work on both DAT and CER

if len(sys.argv) != 2 or sys.argv[1] == '-h':
	print "Usage: %s <filename>"%sys.argv[0]
	print 'For an example: %s $AUGEROFFLINEROOT/share/auger-offline/doc/SampleShowers/Corsika-1e19-6.part'%sys.argv[0]

	exit(0)

cors_file = corsika.CorsikaFile(sys.argv[1])

cors_file.Check()

subblocks = cors_file.GetSubBlocks()
print subblocks
nsb = 0
for sb in subblocks:
	nsb+=1
	print corsika.RunHeader(sb)
	print corsika.RunTrailer(sb), "events processed:",corsika.RunTrailer(sb).fEventsProcessed
	print corsika.EventHeader(sb)
	print corsika.EventTrailer(sb), "fParticles:", corsika.EventTrailer(sb).fParticles
	#print "got a sb len: ", len(sb)

print "total subblocks were %s"%nsb

for event in cors_file.GetEvents():
	print event.GetHeader()
	print event.GetTrailer()
	count = 0
	for particle in event.GetParticles():
		count += 1

	print count, " particles"
