# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 14:20:05 2017

@author: hadoop
"""


def read_data(filename):
    file = open(filename)
    #lines = len(file.readlines())# + np.random.laplace(0,scale,1)[0]
    lines = file.readlines()
    sequence_num = len(lines) 
    print "sequences total:" + str(sequence_num)
    sequence_counter = {}
    for line in lines:
        length = len(line.split(':')[0])
        if sequence_counter.has_key(length):
            sequence_counter[length] += 1
        else:
            sequence_counter[length] = 1
    return sequence_counter

filename = "data/output/realall-gene[5,10]theta=0.028-True.res"
counter = read_data(filename)
print str(counter)