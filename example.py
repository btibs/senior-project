#!/usr/bin/env python

import sys
sys.path.append("/scratch/showerLib/beth/")

import math

import corsika
import matplotlib	# lab version is 0.99.3

import matplotlib.pyplot as plt

# currently does stuff / appears to work on particle data

# find distance of particle from center
def radialdist(x, y):
	return math.sqrt(x**2 + y**2)

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
	particledata.append(particleblock)
	
	# not actually used
	cerblock = corsika.CherenkovData(sb)
	cerdata.append(cerblock)

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
maxdist = 0
for p in particledata:
	xpts.append(p.fX)
	ypts.append(p.fY)
	if radialdist(p.fX, p.fY) > maxdist:
		maxdist = radialdist(p.fX, p.fY)

ax1.plot(xpts, ypts, "r,", label="particle data")

ax1.set_xlabel("Position (m)")
ax1.set_ylabel("Position (m)")
ax1.set_title("Particle Distribution")

# not supported by lab version
#ax1.set_xmargin(0.1)
#ax1.set_ymargin(0.1)

# also not supported?
#ax1.autoscale()

# Now make a plot of density
div = 0.1 # how finely divided to make the plots

# loop through particles and place in bins
distbins = [0]*int(maxdist/div + 1)
print "maximum distance was:",maxdist
print len(distbins)
for p in particledata:
	try:
		dist = radialdist(p.fX, p.fY)
		distbins[int(dist/div)] += 1
	except:
		print "error!", dist, int(dist/div)

fig0 = plt.figure()
ax0 = fig0.add_subplot(111)
distx = [div*i for i in range(0, len(distbins))]
ax0.plot(distx, distbins, 'b,-')
ax0.fill_between(distx, distbins, facecolor='blue', alpha=0.3)
ax0.set_xlabel("Distance from origin (m)")
ax0.set_ylabel("Particles at distance")

#print distx
#print distbins

'''
# was not using earlier, both plots look the same (and wrong)
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

#'''

plt.show()