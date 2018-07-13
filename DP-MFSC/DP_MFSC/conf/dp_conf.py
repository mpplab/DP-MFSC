# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 20:55:09 2017

@author: 84664
"""
#--------------------------------#
# Input parameters
#--------------------------------#

# input files directory
input_dir = "data/input/"

# original sequence database name
dataset_name = "realall-gene"

# original sequence database
dataset = input_dir + dataset_name + ".dat"

# differential privacy budget
epsilon = 1.0

epsilon1 = epsilon * 0.5   #used in the sample database to prune candidate sequences
epsilon2 = epsilon * 0.5   #used for the support computations in the original database

# Threshold
theta = 0.028

# Maximal length constraint upper bound 

#relation parameter
zeta = 0.3
 
# the percent of datasize
scale = 100

#the max motif length bound
lUp = 10

#the min motif length bound
lLeft = 5

# the error tolerance
delta = 1

#truncate len
tlen = 30

topN = 30
#alphabet = ['a','g','c','t']
alphabet = ["A", "G", "C", "T"]
#--------------------------------#
# Output files configuration 
#--------------------------------#

# output files directory
output_dir = "data/output/"

#frequent noisy file 
dataset_noisy = output_dir + dataset_name +  "[%d,%d]"%(lLeft,lUp) + "theta=" + str(theta) + "scale=%d"%(scale) + "delta=%d"%(delta) + "-Noisy.res"

#frequent true file
dataset_true = output_dir + dataset_name + "[%d,%d]"%(lLeft,lUp) + "theta=" + str(theta) + "scale=%d"%(scale) + "delta=%d"%(delta) + "-True.res"


#the Noisy topN frequent motif after caculate the consolidated frequencies 
TopNfile_noisy = output_dir + dataset_name + "[%d,%d]"%(lLeft,lUp)+"zeta="+str(zeta) +"TopN=%d"%(topN) + "scale=%d"%(scale) + "delta=%d"%(delta) +"-Noisy.res"

#the True topN frequent motif after caculate the consolidated frequencies 
TopNfile_true = output_dir + dataset_name + "[%d,%d]"%(lLeft,lUp)+"zeta="+str(zeta) +"TopN=%d"%(topN) + "scale=%d"%(scale) + "delta=%d"%(delta) +"-True.res"

mu = 0.0
sigma = 0.0 
Lambda = 0.0
phi = 0.0