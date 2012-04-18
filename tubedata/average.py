# Elizabeth McNany
# November 7, 2011
# Averages, plotting, etc.

# Input files are assumed to be in the format:
# mm/dd/yy hh:mm\tcount
# each line being a time we wrote down data, so we can plot counts if wanted

from optparse import OptionParser
import os
import datetime
import matplotlib.pyplot as plt
import numpy

class Avgr:
    def __init__(self, options):
        self.options = options
        self.files = []
        self.data = {}
        
        if options.file:
            self.files = [options.file]
        elif options.filelist:
            self.files = options.filelist.split(",")
        else:
            if self.options.verbose:    print "No input file specified, using all in current folder"
            self.files = [i for i in os.listdir(os.getcwd()) if i.endswith(".txt") and i.startswith("avg")]
        
        self.files.sort()
        self.parseFiles()

    def parseFiles(self):
        '''Parse data in files - self.data is like {'filename':[[date, counts], [date, counts]]}'''
        for filename in self.files:
            self.data[filename] = []
            try:
                f = open(os.path.join(os.getcwd(), filename), "r")
            except:
                print "Error opening file %s!"%os.path.join(os.getcwd(), filename)
                sys.exit(0)
            for line in f.readlines():
                timestr, counts = line.split("\t")
                counts = int(counts)
                try:
                    timestamp = datetime.datetime.strptime(timestr, "%m/%d/%y %H:%M")
                except:
                    print "Invalid date format: %s\n\tin file %s at %s"%(timestr, os.path.join(os.getcwd(), filename), line)
                self.data[filename].append([timestamp, counts])
    
    def printAverages(self):
        '''Print average rates for each file'''
        #TODO: error
        print "Average Rates"
        print "File\tStart\tEnd\tDuration\tCounts\tRate/h\tRate/m"
        for k, v in self.data.iteritems():
            fname = k
            t1 = v[0][0]
            t2 = v[-1][0]
            tdelta = t2-t1
            duration = tdelta.days*24*60. + tdelta.seconds/60. # elapsed time in minutes
            counts = v[-1][1]
            cerr = pow(counts, 0.5)
            mrate = counts / duration
            merr = cerr / duration
            hrate = mrate * 60.
            herr = merr * 60.
            #print "%s\t%s\t%s\t%s m\t%s\t%s\t /h%s /m"%(fname, t1, t2, duration, counts, hrate, mrate)
            print "\n- - - %s - - -\nStart:\t%s\nEnd:\t%s\n\t(%s m)\nCounts:\t%s +- %s\n\t(%s +- %s /h)\n\t(%s +- %s /m)"%(fname, t1, t2, duration, counts, cerr, hrate, herr, mrate, merr)
        
    def plotTimes(self):
        '''Plot counts vs. time for each run'''
        fname = self.data.keys()[0]
        xpts = [i[1] for i in self.data[fname]]
        ypts = [i[0] for i in self.data[fname]]
        mainplot = plt.plot_date(xpts, ypts, 'b.-', xdate=True, ydate=False)
        plt.ylabel("Counts")
        plt.xlabel("Time")
        plt.show()
        
    def plotRates(self):
        ''' Plot rates for each run'''
        # fig1 is pt to pt
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        
        # rotate colors
        colorlist = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        cc = -1 # loop var to choose color
        
        #fname = self.data.keys()[0]
        for k, v in self.data.iteritems():
            cc += 1
            #if True:
            fname = k
            times = [i[0] for i in self.data[fname]]
            counts = [i[1] for i in self.data[fname]]
            
            # want to calculate rates between dates
            ypts = []
            yerr = []
            xpts = []
            
            #track totals
            typts = []
            tyerr = []
            txpts = []
            
            print "\nFILE %s"%fname
            print "Start date".ljust(20),"\t","End time".ljust(20),"\t","dt".ljust(8),"\t","dt (hrs)".ljust(8),"\tCounts\tStart\tRate"
            for i in range(1, len(counts)):
                tdelta = times[i] - times[i-1]
                dt = tdelta.days*24.*60. + tdelta.seconds/60. # elapsed time in minutes
                dt /= 60 # hours
                tdeltatot = times[i] - times[0]
                dtot = tdeltatot.days*24.*60. + tdeltatot.seconds/60. # total time in minutes
                dtot /= 60 # hours
                ypts.append((counts[i] - counts[i-1])/dt)
                yerr.append( pow(counts[i]-counts[i-1], 0.5)/dt ) # poisson error for just this time period
                xpts.append(times[i])
                
                typts.append(counts[i]/dtot)
                tyerr.append(pow(counts[i], 0.5)/dtot)
                txpts.append(times[i])
                print times[i], "\t", times[i-1], "\t", tdelta, "\t", str(dt).ljust(8), "\t", counts[i], "\t", counts[i-1], "\t", ypts[i-1]
            
            
            print "overall rate was %s (%s counts over %s hours)"%(counts[-1]/dtot, counts[-1], dtot)
            #print counts
            
            #mainplot = plt.plot_date(xpts, ypts, 'bo-', xdate=True, ydate=False)
            ax1.errorbar(xpts, ypts, yerr, fmt='.-', label=fname, color=colorlist[cc%len(colorlist)])
            # add totals to the errors
            ax1.errorbar([txpts[-1]+datetime.timedelta(0, 3600*12)], [typts[-1]], [tyerr[-1]], fmt='+', color=colorlist[cc%len(colorlist)])
            # add empirical + stddev to errors
            avg = numpy.mean(ypts)
            stddev = numpy.std(ypts)
            ax1.errorbar([txpts[-1]+datetime.timedelta(0, 3600*24)], [avg], [stddev], fmt='x', color=colorlist[cc%len(colorlist)])
            
            ax2.errorbar(txpts, typts, tyerr, fmt='.-', label=fname, color=colorlist[cc%len(colorlist)])
        
		# ignore ax2 for now, it's not the useful one (just straight cumulative
        for a in ([ax1, "Average Rates"], [ax2, "Total Average"]):
            graph = a[0]
            graph.set_xlabel("Time")
            graph.set_ylabel("Counts/h")
            graph.set_title(a[1])
            #graph.legend()
            graph.set_xmargin(0.1)
            graph.autoscale()
            graph.get_figure().autofmt_xdate()
            
        plt.show()
        
# Command line entry point
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", help="Single file to process")
    parser.add_option("-l", "--list", dest="filelist", help="Comma-separated list of files to process")
    parser.add_option("-p", "--plot", dest="plot", action="store_true", default=False, help="Plot counts for file")
    parser.add_option("-r", "--rate", dest="rate", action="store_true", default=False, help="Plot rates for file")
    parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Don't print extra messages")
    
    (options, args) = parser.parse_args()
    avgr = Avgr(options)
    if options.plot:
        avgr.plotTimes()
    elif options.rate:
        avgr.plotRates()
    else:
        avgr.printAverages()