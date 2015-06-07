# -*- coding: utf-8 -*-
import numpy as np
import scipy.stats as stats
import sys
sys.path.insert(1, 'D:\yourpath\pusher_client_python-master\build\lib')
#import bougie
import pusher

class MyOVBox(OVBox):
  
  def __init__(self):
	OVBox.__init__(self)
	print 'initialisation...'
	self.eeg_data  = np.array([])
	self.pin_data  = np.array([])
	self.win_len   = 0
	self.new_chunk = 0
	self.quantiles = []
  
  def initialize(self):
    self.win_len   = int(self.setting['window_len'])
    self.eeg_data  = np.zeros([self.win_len])
    self.quantiles = np.zeros(255)
    self.pin_data  = np.zeros(8)
    print 'create %i length window' %self.win_len
    #self.boug = bougie.Bougie()
    self.hand = 1.
    self.p = pusher.Pusher(app_id='99043', key='b8aa4e777b69f94c7803', secret='5e81d209f102e7cf26be')
    #self.boug.update(1.)
   
  def process(self):
     for chunkIndex in range(len(self.input[0])):
       if(type(self.input[0][chunkIndex]) == OVStreamedMatrixHeader):
         hdr = self.input[0].pop()
       
       elif(type(self.input[0][chunkIndex]) == OVStreamedMatrixBuffer):
         chunk  = np.log10(np.reshape(np.array(self.input[0].pop()),(1,-1)))
         
         if (self.getCurrentTime() > 15) & (self.new_chunk < self.win_len):
           self.eeg_data[self.new_chunk] = chunk.mean()
           print 'getting chunk %i at time %.2f : %f' %(self.new_chunk,self.getCurrentTime(),chunk.mean())
           self.new_chunk = self.new_chunk+1
         
         elif self.new_chunk == self.win_len:
           (self.quantiles) = stats.mstats.mquantiles(self.eeg_data,prob=np.arange(0,10,.1)/10.)
           print '5 percent inter-quantiles : ' + str(self.quantiles)
           self.new_chunk = self.new_chunk+1
         
         elif self.new_chunk > self.win_len:
           self.hand = sum(self.quantiles <= chunk.mean())
           #self.boug.update(self.hand)   #  <- la
           self.p['test_channel'].trigger('my_event', self.hand)
           print 'updated to %f' %self.hand
         else:
           print 'missing %i chunks' %(self.win_len-self.new_chunk)
       
       elif(type(self.input[0][chunkIndex]) == OVStreamedMatrixEnd):
         print 'End of buffer'
     # empty the input list
     while len(self.input[0]):
       self.input[0].pop()
   
  def uninitialize(self):
     self.data = []

box = MyOVBox()
