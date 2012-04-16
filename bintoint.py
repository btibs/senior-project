# Read integers from a binary file
import sys
import struct

DEBUG = False

def main(fname):
	f = open(fname, "rb")
	data = []
	s = ''
	for line in f.read(): # 4 bytes at a time?
		if DEBUG:	print "line is",repr(line)
		s += line
		if len(s) == 4:
			data.append(struct.unpack('i',s)[0])
			if DEBUG:	print "s is",repr(s),data[-1]
			s = ''
	f.close()
	print data

# command-line entry
if __name__ == "__main__":
	try:
		fname = sys.argv[1]
		main(fname)
	except IndexError:
		print "usage: bintoint.py filename"