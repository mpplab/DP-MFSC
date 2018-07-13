# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 01:01:14 2017

@author: hadoop
"""

from collections import Counter
import Levenshtein

def TopN(dicta,dictb, top_K):
	dictMerged = dict( dicta.items() + dictb.items() ) 
	d = sorted(dictMerged.iteritems(),key=lambda t:t[1],reverse=True)[:top_K]
	return dict(d)

def calculateConsolidatedFrequency(dataset_name,lLeft,lUp,deta,output_filename,top_k):
    fp = open(dataset_name,'r')

    lines = fp.readlines()
    grams = []
    sups = []
    for line in lines:  # First line of the file is a number
        #print line
        #print line
        parts = line.strip().partition(':')
        tokens = parts[0].strip()
        grams.append(tokens)
        sups.append(parts[2])

    
    len_gram_sup = {}
    seqAllCounter = Counter()
    
    for i in range(len(grams)):
        curLen = len(grams[i])
        strList = []
        strList.append(grams[i])
        if curLen >= lLeft and curLen <= lUp:
            if curLen in len_gram_sup.keys():
                counter = len_gram_sup[curLen]
                counter[grams[i]] = sups[i]
                len_gram_sup[curLen] = counter
            else:
                counter = Counter()
                counter[grams[i]] = sups[i]
                len_gram_sup[curLen] = counter
        seqAllCounter[grams[i]] = sups[i]
    
    N = {}
    l = lLeft
    len_motifs_consolidatesup ={}
    while l<=lUp:
		#print len_gram_sup
        if len_gram_sup.has_key(l):
    		seq_l = len_gram_sup[l]
    		s = seq_l.keys()[0]
    		Bucket = {}
    		for each_seq1 in seq_l:
    			for i in range(int(l)+1):
    				if Levenshtein.hamming(each_seq1, s) == i:
    					if i not in Bucket.keys():
    						Bucket.setdefault(i,[])
    						Bucket[i].append(each_seq1)
    					else:
    						Bucket[i].append(each_seq1)
    		for i in Bucket.keys():
    			for each_seq1 in Bucket[i]:
    				len_motifs_consolidatesup.setdefault(l,{})[each_seq1]  = 0
    				if i >= deta :
    					for j in xrange(i-deta,min(i+deta,l)+1):
    						if j in Bucket.keys():
    							for each_seq2 in Bucket[j]:
    								if 0<=Levenshtein.hamming(each_seq1,each_seq2 )<=deta:
    									#len_motifs_consolidatesup.setdefault(l,{})[each_seq1]  += len_gram_sup[l][each_seq2]
										#print len_motifs_consolidatesup.setdefault(l,{})[each_seq1]
										#print len_gram_sup[l][each_seq2]
										len_motifs_consolidatesup.setdefault(l,{})[each_seq1]=round(float(len_motifs_consolidatesup.setdefault(l,{})[each_seq1]))  + round(float(len_gram_sup[l][each_seq2]))
    				else:
    					for j in xrange(0,min(i+deta,1)+1):
    						if j in Bucket.keys():
    							for each_seq2 in Bucket[j]:
    								if 0<=Levenshtein.hamming(each_seq1,each_seq2 )<=deta:
    									len_motifs_consolidatesup.setdefault(l,{})[each_seq1]=round(float(len_motifs_consolidatesup.setdefault(l,{})[each_seq1]))  + round(float(len_gram_sup[l][each_seq2]))
    		N = TopN(N,len_motifs_consolidatesup[l],top_k)
    	l += 1
    f = open(output_filename,'w')
    for i in dict(sorted(N.iteritems(),key=lambda t:t[1],reverse=True)).keys():
        print i
        f.write(' '.join(i) + ': ' + str(N[i]) + '\n')