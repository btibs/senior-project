#!/usr/bin/env python
# lab python is 2.6.6

# this is a haxed version of plot.py to put multiple DAT files on the same plots

import sys
import corsika

import matplotlib	# lab version is 0.99.3
import matplotlib.pyplot as plt

import math

# currently works on DAT* files, not CER

filelist = ["data\\20120215-150008\\DAT000001", "data\\DAT000001", "data\\DAT000004"]
descriptions = ["1 PeV", "1 PeV, 5 runs", "1 PeV"]
colors = ['b', 'g', 'r'] # add more later
particlelists = []

# return distance from origin
def radialdist(x, y):
	return math.sqrt(x**2.0 + y**2.0)

if len(sys.argv) > 1 and sys.argv[1] == '-h':
	print "Usage: %s"%sys.argv[0]
	print "Plots hardcoded list of DAT files on same axes"
	print "use plot.py instead to plot individual files"
	#print 'For an example: %s $AUGEROFFLINEROOT/share/auger-offline/doc/SampleShowers/Corsika-1e19-6.part'%sys.argv[0]
	#print 'Or: python example.py /scratch/showerLib/beth/DAT000001'

	exit(0)

for filename in filelist:
	cors_file = corsika.CorsikaFile(filename)

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
		
		cerblock = corsika.CherenkovData(sb)
		cerdata.append(cerblock)

	print "total subblocks in file %s were %s"%(filename, nsb)
	
	particlelists.append(particledata)

# make plot of position of particles
div = 1.0 # for density plot
maxdists = [0]*len(filelist)

fig = plt.figure()
ax1 = fig.add_subplot(111)
for i in range(0, len(filelist)):
	xpts = []
	ypts = []
	for p in particlelists[i]:
		xpts.append(p.fX)
		ypts.append(p.fY)
		if radialdist(p.fX, p.fY) > maxdists[i]:
			maxdists[i] = radialdist(p.fX, p.fY)

	ax1.plot(xpts, ypts, ".", label=descriptions[i], color=colors[i])

ax1.set_xlabel("Position (cm)")
ax1.set_ylabel("Position (cm)")
ax1.set_title("Particle Map")
ax1.legend()

# square plot
maxy = max([abs(i) for i in ax1.get_ylim()])
maxx = max([abs(i) for i in ax1.get_xlim()])
lim = max(maxx, maxy)
ax1.set_ylim(lim*-1, lim)
ax1.set_xlim(lim*-1, lim)

# make density plot
fig0 = plt.figure()
ax0 = fig0.add_subplot(111)
for i in range(0, len(filelist)):
	distbins = [0] * (int(maxdists[i]/div)+1)
	for p in particlelists[i]:
		distbins[int(radialdist(p.fX, p.fY)/div)] += 1

	distx = [div*j for j in range(0, len(distbins))]

	ax0.plot(distx, distbins, '.-', color=colors[i], label=descriptions[i])
	ax0.fill_between(distx, distbins, color=colors[i], alpha=0.3)

ax0.set_ylim(0, ax0.get_ylim()[1])
ax0.set_xlabel("Distance from origin (cm)")
ax0.set_ylabel("Number of particles (%s cm bins)"%div)
ax0.set_title("Number of particles vs. distance")
ax0.legend()

'''
densbins = [0]*len(distbins)
for i in range(0, len(distbins)):
	areaofring = math.pi*math.pow((i+1)*div, 2) - math.pi*math.pow(i*div, 2)
	densbins[i] = distbins[i] / areaofring

fig00 = plt.figure()
ax00 = fig00.add_subplot(111)
ax00.plot(distx, densbins, 'b.-')
ax00.fill_between(distx, densbins, color='blue', alpha=0.3)
ax00.set_ylim(0, ax00.get_ylim()[1])
ax00.set_xlabel("Distance from origin (cm)")
ax00.set_ylabel("Density of particles (per cm^2)")
ax00.set_title("Density of particles vs. distance")
#'''

# these both look the same and wrong
'''
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
#fig2.show()

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
#fig3.show()
#'''

plt.show()

