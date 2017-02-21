# test.py

import gzip
import struct
import re

fname = "data/GoogleNews-vectors-negative300.bin.gz"
#fname = "googlenews.bin"
MAX_WORD_SIZE = 50
FLOAT_BYTES = 4

def peeker(f,numchar):
	p = f.tell()
	s = f.read(numchar)
	f.seek(p)
	return s
	

with gzip.open(fname,'rb') as f:
	#d = f.peek(10)
	for line in f:
		head = line.split()
		numwords = int(head[0])
		numdim = int(head[1])
		break
	print(numwords, numdim)
	
	for i in range(numwords):
		print(i)
		
		# get vocab word
		
		#print(w[0:20])
		#w = w.decode(encoding='ascii',errors='ignore')
		
		b = peeker(f,MAX_WORD_SIZE)
		
		m = re.search(b'[\S]+(?= )',b)
		if m is not None:
			w = m.group(0)
		else:
			w = b
		
		# decode word
		w = w.decode('utf-8',errors='ignore')
		
		# incremement fp
		f.seek(f.tell()+len(w)+1)
		
		# read in and parse data
		dat = f.read(FLOAT_BYTES*numdim)
		vec = struct.unpack('f'*numdim, dat)
		
		print(w)


