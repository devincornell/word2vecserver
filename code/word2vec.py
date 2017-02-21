# test.py

import gzip
import struct
import re
import numpy as np
import pandas as pd

#fname = "googlenews.bin"
MAX_WORD_SIZE = 50
FLOAT_BYTES = 4

def peek(f,numchar):
	p = f.tell()
	s = f.read(numchar)
	f.seek(p)
	return s
	
class Word2Vec():
	
	def __str(self):
		return '<Word2Vec;words:{},dimensions:{}'.format(self.numwords,self.numdim)
	
	def __init__(self, fname, testwords=np.inf):
		
		f = gzip.open(fname,'rb')
		
		# read header
		for line in f:
			head = line.split()
			numwords = int(head[0])
			numdim = int(head[1])
			break
		
		# set testwords for testing
		if testwords is not np.inf:
			numwords = testwords
			
		# store header info
		self.numwords = numwords
		self.numdim = numdim
		
		# allocate memory for dataframe
		print('Allocating memory for dataframe.')
		self.df = pd.DataFrame(np.zeros((numwords,numdim)))
			
		print('Reading data from file.')
		wordlist = []
		for i in range(numwords):
			
			# decide on length of word
			b = peek(f,MAX_WORD_SIZE)
			m = re.search(b'[\S]+(?= )',b)
			if m is not None:
				w = m.group(0)
			else:
				w = b

			# decode word
			w = w.decode('utf-8',errors='ignore').lower()
			
			# incremement fp
			f.seek(f.tell()+len(w)+1)
			
			# read in and parse data
			dat = f.read(FLOAT_BYTES*numdim)
			vec = struct.unpack('f'*numdim, dat)
			
			# store in dataframe
			# this is really slow!!!!
			self.df.loc[i,:] = np.array(vec)
			#self.df.loc[i,'word']
			
			wordlist.append(w)
			
			print(i)
			if i > testwords: break
		f.close()
		
		print('Indexing data.')
		self.df.set_index(wordlist,inplace=True)
		print('Finished loading dataset.')
		
		return

if __name__ == '__main__':
	fname = "data/GoogleNews-vectors-negative300.bin.gz"
	wv = Word2Vec(fname, testwords=100)
	print(wv.df.head())
	
