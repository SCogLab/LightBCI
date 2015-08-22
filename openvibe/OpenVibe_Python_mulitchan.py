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
        self.calib_data  = np.array([])
        self.calib_length = 0
        self.new_chunk = 0
        self.distribution = []
        self.arduino_port = "COM11"
        
    def initialize(self):
        # Get calibration duration from the openvibe settings (python box)
        self.calib_length = int(self.setting['calib_duration'])
        self.calib_data  = np.zeros([2, self.calib_length])
        self.distribution = np.zeros([2, 255])
        print 'create %i length window' %self.calib_length
        # command to be sent to the arduino
        self.command = 1. # should be between 1 and 100
        # serial connection that send the command to the arduino
        self.port_serie = Serial(port=self.arduino_port, 
                                baudrate=9600, 
                                timeout=1, 
                                writeTimeout=1)
    
    def process(self):
        for chunkIndex in range(len(self.input[0])):
            # check that the input is of type OVStreamedMatrixHeader
            if(type(self.input[0][chunkIndex]) == OVStreamedMatrixHeader):
                hdr = self.input[0].pop()
            # check that the input is of type OVStreamedMatrixBuffer
            elif(type(self.input[0][chunkIndex]) == OVStreamedMatrixBuffer):
                # computing log10 power (normalisation)
                # chunk  = np.log10(np.reshape(np.array(self.input[0].pop()),(1,-1)))
                chunk  = np.log10(np.reshape(self.input[0].pop(), (2,-1)))
                print 'received chunk of size', chunk.shape
                # check that the experiments begins and get new chunk if calibration length is not reached
                if (self.getCurrentTime() > 15) & (self.new_chunk < self.calib_length):
                    # average across electrodes
                    self.calib_data[:, self.new_chunk] = chunk.mean(1)
                    print 'getting chunk %i at time %.2f : %f' %(self.new_chunk,self.getCurrentTime(),chunk.mean())
                    self.new_chunk = self.new_chunk+1
                # check that calibration length is reached
                elif self.new_chunk == self.calib_length:
                    # computes data distribution
                    self.distribution_a = stats.mstats.mquantiles(self.calib_data[0],
                                            prob=np.linspace(0,1,255))
                    print '5 percent inter-distribution : ' + str(self.distribution_a)
                    self.distribution_b = stats.mstats.mquantiles(self.calib_data[1],
                                            prob=np.linspace(0,1,255))
                    self.new_chunk = self.new_chunk+1
                # check that calibration length is over
                elif self.new_chunk > self.calib_length:
                    # the command is computed for a given chunk received after calibration
                    # count number of values in the distribution that are lower than the chunk
                    self.command_a = sum(self.distribution_a <= chunk[0].mean())
                    self.command_b = sum(self.distribution_b <= chunk[1].mean())
                    # writes the command to the arduino (serial port)
                    self.port_serie.write([self.command_a, self.command_b])
                    print 'updated to %f' %self.command_a
                    print 'updated to %f' %self.command_b
                else:
                    print 'missing %i chunks' %(self.calib_length-self.new_chunk)
            # check that the input is of type OVStreamedMatrixEnd
            elif(type(self.input[0][chunkIndex]) == OVStreamedMatrixEnd):
                print 'End of buffer'
        
        # empty the input list
        while len(self.input[0]):
            self.input[0].pop()
   
    def uninitialize(self):
        self.data = []
        self.port_serie.close()
    

box = MyOVBox()
