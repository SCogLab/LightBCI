# -*- coding: utf-8 -*-
import numpy as np
import scipy.stats as stats
import sys, os, platform
from serial import *

class MyOVBox(OVBox):
  
  def __init__(self):
	OVBox.__init__(self)
    sys_plaform = platform.system()
	print 'initialisation for ' + sys_plaform
	self.eeg_data  = np.array([])
	self.pin_data  = np.array([])
	self.win_len   = 0
	self.new_chunk = 0
	self.quantiles = []
    # find serial port as a function of system platform
    if sys_plaform == "Darwin":
        self.serial_port = "/dev/tty.usbmodem1421"
    else:
        # Port série ttyACM0
        self.serial_port="/dev/ttyACM0"
  
  def initialize(self):
    self.win_len   = int(self.setting['window_len'])
    self.eeg_data  = np.zeros([self.win_len])
    self.quantiles = np.zeros(255)
    self.pin_data  = np.zeros(8)
    print 'create %i length window' %self.win_len
    #self.boug = bougie.Bougie()
    self.hand = 1.
    self.port_serie = Serial(port=serial_port, 
                             baudrate=9600, 
                             timeout=1, 
                             writeTimeout=1)
    
   
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
           port_serie.write([self.hand])
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
