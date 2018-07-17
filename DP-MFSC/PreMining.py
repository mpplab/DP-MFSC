# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 21:41:48 2017

@author: 84664
"""
from __future__ import division 
import numpy as np
import math
def read_data(filename):
    file = open(filename)
    #lines = len(file.readlines())# + np.random.laplace(0,scale,1)[0]
    lines = file.readlines()
    #sequence_num = len(lines) 
    #print "sequences total:" + str(sequence_num)
    sequence_counter = {}
    for line in lines:
        #print "line:" + str(line)
        if line.startswith('#') or line.startswith('//') or line.startswith('%') or line.startswith('>'):
                continue
        
        length = len(line.strip())
        if sequence_counter.has_key(length):
            sequence_counter[length] += 1
        else:
            sequence_counter[length] = 1
    #print "sequence_counter:"
    #print sequence_counter
    
    return sequence_counter
def read(filename, l_max, scale):
    file = open(filename)
    lines = file.readlines()
    D = []
    for line in lines:
        if line.startswith('#') or line.startswith('//') or line.startswith('%') or line.startswith('>'):
            continue
        else:
            string = line.strip()
            for i in xrange(0,len(string),l_max):
                    #print string[i:i+l_max]
                if len(string[i:i+l_max].strip() )== l_max:
                    D.append(string[i:i+l_max].strip())
    
    all_record_num = len(D)
    trunCount = int(all_record_num * scale / 100)
    print "all record number:" + str(trunCount)
    D = D[:trunCount - 1]
    
    return D
        
def Get_lmax(sequence_counter,eta,epsilon1,l1,epsilon2):  
    #sequence_counter = read_data(filename)
    lmax = l1
    l2 =  lmax
    D = 0
    trueD = sum(sequence_counter.values()) #the sum count of dataset
    D = trueD + np.random.laplace(0,1 / epsilon1,1)[0]
    #print "D=" + str(D)
    #print sequence_counter
    for i in range(1,max(sequence_counter.values()) + 1):
        p = 0
        count = 0
        if sequence_counter.has_key(i) : 
            #scale = sequence_counter[i] / epsilon1
            #print str(i) + "  sequence_counter[i]"+str(sequence_counter[i])
            #print "epsilon1:" + str(epsilon1)
            sequence_counter[i] +=  np.random.laplace(0,1 / epsilon2,1)[0]
            for j in range(1,i+1):
                if sequence_counter.has_key(j):
                    count += sequence_counter[i]
                
            p = count/D
            if p >= eta:
                l2 = i
                lmax = min(l1,l2)
                #print "p:" + str(p)
                #print "l2:" + str(l2)
                break
            else:
                print "cannot reach eta !"
    
    print "*********************"
    print "lmax:" + str(lmax)
    print "l2:" + str(l2)
    print "l1:" + str(l1)
    print "*********************"
    return lmax

def GetNoisyMaxSup(sequence_counter,lmax,epsilon3):
    for i in range(1,lmax + 1):
        if sequence_counter.has_key(i):
            sequence_counter[i] += np.random.laplace(0,int(math.log(lmax)),1)[0]
    #print"epsilon3 + sequence_counter:" + str(sequence_counter)
    return sequence_counter

def estimate_max_frequent_sequence_length(filename,eta,epsilon1,l1,epsilon2,epsilon3,theta):
    L_f = l1
    sequence_counter = read_data(filename)
    lmax = Get_lmax(sequence_counter,eta,epsilon1,l1,epsilon2)
    Beta_sequence_counter = GetNoisyMaxSup(sequence_counter,lmax,epsilon3)
    for i in range(1,lmax + 1):
        if sequence_counter.has_key(i):
            #print sequence_counter[i]
            if float(sequence_counter[i])/sum(sequence_counter.values()) > theta:
                L_f = i
    print "L_f:" + str(L_f)
    return L_f





