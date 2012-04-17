#!/usr/bin/env python

import sys
#sys.path.append("/scratch/showerLib/beth/")
sys.path.append("C:\\Users\\Julie\\Desktop\\beth\\Senior Project\\sim\\")
import corsika
import matplotlib
#matplotlib.rcParams['backend'] = 'QtAgg'

import matplotlib.pyplot as plt

# currently does stuff / appears to work on both DAT and CER

if len(sys.argv) != 2 or sys.argv[1] == '-h':
	print "Usage: %s <filename>"%sys.argv[0]
	print 'For an example: %s $AUGEROFFLINEROOT/share/auger-offline/doc/SampleShowers/Corsika-1e19-6.part'%sys.argv[0]

	exit(0)

cors_file = corsika.CorsikaFile(sys.argv[1])

cors_file.Check()

# Arrays to store the data
particledata = []	# particle data
cerdata = []	# cherenkov data

subblocks = cors_file.GetSubBlocks()
nsb = 0
for sb in subblocks:
	nsb+=1
	particleblock = corsika.ParticleData(sb)
	# print particleblock, dir(particleblock)
	particledata.append(particleblock)
	
	cerblock = corsika.CherenkovData(sb)
	# print cerblock, dir(cerblock)
	cerdata.append(cerblock)
	# print corsika.RunHeader(sb)
	# print corsika.RunTrailer(sb), "events processed:",corsika.RunTrailer(sb).fEventsProcessed
	# print corsika.EventHeader(sb)
	# print corsika.EventTrailer(sb), "fParticles:", corsika.EventTrailer(sb).fParticles
	#print "got a sb len: ", len(sb)
	

print "total subblocks were %s"%nsb

# for event in cors_file.GetEvents():
	# print event.GetHeader()
	# print event.GetTrailer()
	# count = 0
	# for particle in event.GetParticles():
		# count += 1

	# print count, " particles"


# make plot of position of particles
fig = plt.figure()
ax1 = fig.add_subplot(111)
xpts = []
ypts = []
for p in particledata:
	xpts.append(p.fX)
	ypts.append(p.fY)

ax1.plot(xpts, ypts, "r.", label="particle data")

ax1.set_xlabel("Position")
ax1.set_ylabel("Position")
ax1.set_title("Particle Map")
ax1.set_xmargin(0.1)
ax1.set_ymargin(0.1)
ax1.autoscale()

plt.show()

'''
# these both look the same and wrong

# plot for cherenkov data
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
xpts2=[]
ypts2=[]
for p in cerdata:
	xpts2.append(p.fX)
	ypts2.append(p.fY)
ax2.plot(xpts2, ypts2, "b.", label="cherenkov data")
ax2.set_title("cherenkov data")
fig2.show()

# plot for cherenkov data
fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
xpts3=[]
ypts3=[]
for p in particledata:
	xpts3.append(p.fPx)
	ypts3.append(p.fPy)
ax3.plot(xpts3, ypts3, "g.", label="particle data p3")
ax3.set_title("particle data p")
fig3.show()

'''
