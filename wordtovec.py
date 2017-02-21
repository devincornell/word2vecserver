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
	
class WordToVec():
	
	def __str(self):
		return '<Word2Vec;words:{},dimensions:{}'.format(self.numwords,self.numdim)
	
	def __init__(self, fname, testwords=np.inf, verbose=False):
		
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
		if verbose: print('Allocating memory for dataframe.')
		self.df = pd.DataFrame(np.zeros((numwords,numdim)))
			
		if verbose: print('Reading data from file.')
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
			
			#print(i)
			if i % 10000 == 0: print('{} of {}'.format(i,numwords))
			if i > testwords: break
		f.close()
		
		if verbose: print('Indexing data.')
		self.df['words'] = wordlist
		self.df.set_index('words',inplace=True)
		self.df.sort_index(inplace=True)
		if verbose: print('Finished loading dataset.')
		
		return

	def get_word(self, word):
		return list(self.df.loc[word,:])

if __name__ == '__main__':
	fname = "data/GoogleNews-vectors-negative300.bin.gz"
	wv = WordToVec(fname, testwords=500, verbose=True)
	print(wv.df.head())

	words = list(wv.df.index[0:10])

	print(words)

	for word in words:
		print(word + ':')
		print(wv.get_word(word))
		print()
	
