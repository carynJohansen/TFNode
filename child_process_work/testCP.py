import sys
from datetime import datetime
from time import sleep

if __name__ == '__main__':
	file, start, end, chrom = sys.argv
	while 1:
		print datetime.now()
		sys.stdout.flush()
		sleep(5)