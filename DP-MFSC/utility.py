# -*- coding: utf-8 -*-
"""
Created on Sun May 14 17:56:49 2017

@author: 84664
"""
import string
import numpy as np
import math
from sklearn.metrics import mean_squared_error
def getSeqDict( fileTrue, fileNoise ):
    True_seq_dic = {}
    Noise_seq_dic = {}

    for line in open( fileTrue, "r" ):
        line = line.strip().split(":") 
        True_seq_dic[line[0].strip()] = string.atof( line[1].strip() )
        
    for line in open( fileNoise, "r" ):
        line = line.strip().split(":")
        Noise_seq_dic[line[0].strip()] = string.atof( line[1].strip() )

    return True_seq_dic, Noise_seq_dic
'''
1.RE
Relative error of published motif counts
This measures the error with respect to the actual motif frequency in the dataset. 
This is calculated over all published frequent motifs.
'''
def RE(Truefile,Noisefile,top_k):
    True_seq_dic, Noise_seq_dic = getSeqDict( Truefile, Noisefile)
    RE = []
    
    for key in True_seq_dic:
        if Noise_seq_dic.has_key(key):
            ratio = abs(Noise_seq_dic[key] - True_seq_dic[key])/ True_seq_dic[key]
            RE.append(ratio)

    midRE = get_median(RE)
    
    #print " TOP-K : %d" % (top_k) 
    
    #print "模式支持度计数可用性度量"
    print "(2)midRE: %s\n" %(str(midRE))

def ARE(Truefile,Noisefile,top_k):
    True_seq_dic, Noise_seq_dic = getSeqDict( Truefile, Noisefile)
    ARE = 0.0
    
    for key in True_seq_dic:
        if Noise_seq_dic.has_key(key):
            ratio = abs(Noise_seq_dic[key] - True_seq_dic[key])/ True_seq_dic[key]
            ARE += ratio
        else:
            ARE += 0
    ARE = ARE / top_k
    #print " TOP-K : %d" % (top_k) 
    #print "模式支持度计数可用性度量"
    print "(3)ARE: %s\n" %(str(ARE))

def Accuracy(Truefile, Noisefile, top_k ):
    True_seq_dic, Noise_seq_dic = getSeqDict( Truefile, Noisefile)
    TP = 0.0
    FP = 0.0
    sup = []
    for key in Noise_seq_dic:
        if True_seq_dic.has_key(key):
            TP += 1             
        else:
            FP += 1

    print "(1) Accuracy : %s\n" % (TP/top_k)
    #print "   (2) FP : %f" % (FP/top_k)


def NRMSE(Truefile, Noisefile, top_k):
    True_seq_dic, Noise_seq_dic = getSeqDict( Truefile, Noisefile)
    MSE = 0.0
    TP = 0.0

    for key in True_seq_dic:
        if Noise_seq_dic.has_key(key):

            MSE += abs(Noise_seq_dic[key] - True_seq_dic[key])**2
            TP += 1
        #else:
            #MSE += abs(True_seq_dic[key])**2
            
    RMSE = math.sqrt(MSE/TP)
    NRMSE = RMSE/(sum(True_seq_dic.values())/TP)
    print "(3)NRMSE : %s"%(NRMSE)

'''
False negative rate: This measures the fraction of actual frequent itemsets 
which do not appear in the published result
'''

def FNR(Truefile, Noisefile, top_k):
	True_seq_dic, Noise_seq_dic = getSeqDict( Truefile, Noisefile)
	count = 0.0
	FNR = 0.0
	for key in True_seq_dic.keys():
		if Noise_seq_dic.has_key(key):
			count += 1
	FNR = abs((count - top_k) / top_k)
	print "(4)FNR: " +str(FNR)
	return FNR

def get_median(data):
   data = sorted(data)
   size = len(data)
   if size % 2 == 0: # 判断列表长度为偶数
    median = (data[size//2]+data[size//2-1])/2
    data[0] = median
   if size % 2 == 1: # 判断列表长度为奇数
    median = data[(size-1)//2]
    data[0] = median
   return data[0]


def main():
    epsilon = 1.0
    n_max = 3
    l_max = 30
    lLeft = 5
    deta = 2
    topN = 30
    lUp = 10
    input_dir = "data/input/"
    output_dir = "data/output/"
    dataset_name = "realall"
    outdataset_name_info =output_dir + dataset_name + "nmax=%dN=%d[%d,%d]deta=%deps=%.2f"
    noise_outdataset_name = output_dir+dataset_name+ "nmax=%dN=%d[%d,%d]deta=%deps=%.2f-noise"
    true_outdataset_name = output_dir+dataset_name + "nmax=%dN=%d[%d,%d]deta=%d-true"
                                                     
    # original sequence database
    Truefile = true_outdataset_name % (n_max, topN, lLeft, lUp, deta) + ".dat"
    Noisefile = noise_outdataset_name % (n_max, topN, lLeft, lUp, deta, epsilon) + ".dat"
    print  "l_max:" + str(l_max)
    print "L_l:%d"%(lLeft)
    print "l_u:%d"%(lUp)
    print "deta:%d"%(deta)
    print "epsilon:%f"%(epsilon)
    ARE(Truefile,Noisefile,topN) 
    Accuracy(Truefile, Noisefile, topN) 
    NRMSE(Truefile, Noisefile,topN)            
    



if __name__ == "__main__":

	main()
	
