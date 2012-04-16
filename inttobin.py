# Print integer range to a binary file
import sys
import struct

DEBUG = False

def main(start, end, fname):
	f = open(fname, 'wb')
	for i in range(start, end):
		if DEBUG:	print "writing",repr(i)
		b = struct.pack('i', i)
		if DEBUG:	print "is",repr(b)
		f.write(b)
	f.close()

# command-line entry
if __name__ == "__main__":
	try:
		fname, start, end = sys.argv[1:]
		start = int(start)
		end = int(end)
		main(start, end, fname)
	except IndexError, ValueError:
		print "usage: inttobin.py filename start end"
