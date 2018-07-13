# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 21:33:24 2017

@author: 84664
"""
from __future__ import division 
import sys
sys.path.append('conf')
import dp_conf as conf
import PreMining as PM
import Mining as M
import numpy as np
import ConsolidatedFrequency as CF
import utility
import datetime
import os

def getNoisyConFrequency():
    
    print "*****Read Data********************"
    Dataset = []
    Dataset = PM.read(conf.dataset, conf.tlen, conf.scale)
    print "*****Read sucessfully*************"

    print "*****Start Mining Phase***********"
    height = conf.lUp - conf.lLeft + 1
    dbSets = M.randomly_partition_database(Dataset, height)
    each_epsilon = conf.epsilon2 / height
    
    CandidateSets = {}
    new_CandidateSets = {}
    FS = {}
    FS_sup = {}
    FSlist = []
    FSlist_sup = []
    print "len(dbSets)" + str(len(dbSets))
    i = 0
    for k in range(conf.lLeft, conf.lUp + 1):
        if k == conf.lLeft :
            CandidateSets[k] = M.getcandidate(conf.alphabet, k)
        else:

            CandidateSets[k] = M.generate_candidate(FS[k - 1], conf.alphabet)
        
        #print "len of dbset:" + str( len(dbSets) )
    
        new_CandidateSets[k] = M.SamplingbasedCandidatePruning(k, CandidateSets[k], dbSets[i], conf.epsilon1, conf.theta)
        i += 1
        #print new_CandidateSets[k]
        (FS[k], FS_sup[k])= M.discover_frequent_sequence1(k,new_CandidateSets[k], each_epsilon, Dataset, conf.theta)
        #(FS[k], FS_sup[k]) = M.discoverFrequentSequences(k, Dataset, new_CandidateSets[k], each_epsilon, conf.theta, conf.l_max, conf.l_max)
        FSlist += FS[k]
        FSlist_sup += FS_sup[k]

    print "*************  End Mining Phase    ****************"
    fp = open(conf.dataset_noisy, 'w')
    print len(FSlist)
    print len(FSlist_sup)
    for i in range(len(FSlist)):
        fp.write(str(FSlist[i]) + ":" + str(FSlist_sup[i]) + '\n')
    fp.close()

    print"Caculate the consolidated frequencies"
    CF.calculateConsolidatedFrequency(conf.dataset_noisy, conf.lLeft, conf.lUp, conf.delta, conf.TopNfile_noisy, conf.topN)
    print "End Caculate the consolidate frquencies"
    
def getTrueConFrequency():
    print "*****getTrueConFrequency**********"
    print "*****Read Data********************"
    Dataset = []
    Dataset = PM.read(conf.dataset, conf.tlen, conf.scale)
    print "len of dataset:" + str(len(Dataset))
    print "*****Read sucessfully*************"

    print "*****Start Mining Phase***********"
    #dbSets = M.randomly_partition_database(Dataset, conf.lUp)
    CandidateSets = {}
    FS = {}
    FS_sup = {}
    FSlist = []
    FSlist_sup = []
    
    for k in range(1, conf.lUp + 1):
        print "k=" + str(k)
        if k == 1 :
            CandidateSets[k] = M.getcandidate(conf.alphabet, k)
        else:
            CandidateSets[k] = M.generate_candidate(FS[k - 1], conf.alphabet)
        #CandidateSets[k] = M.SamplingbasedCandidatePruning(k, CandidateSets[k], dbSets[k - 1], conf.theta, conf.l_max)
        (FS[k], FS_sup[k])= M.discover_frequent_sequence2(CandidateSets[k],  Dataset, conf.theta)
        FSlist += FS[k]
        FSlist_sup += FS_sup[k]
    print "*************  End Mining Phase    ****************"
    fp = open(conf.dataset_true, 'w')
    print len(FSlist)
    print len(FSlist_sup)
    for i in range(len(FSlist)):
        fp.write(str(FSlist[i]) + ":" + str(FSlist_sup[i]) + '\n')
    fp.close()
   
    print"Caculate the consolidated frequencies"
    CF.calculateConsolidatedFrequency(conf.dataset_true, conf.lLeft, conf.lUp, conf.delta, conf.TopNfile_true, conf.topN)
    print "End Caculate the consolidate frquencies"

begin = datetime.datetime.now()

getNoisyConFrequency()
if os.path.isfile(conf.TopNfile_true) == False :
    getTrueConFrequency()
utility.Accuracy(conf.TopNfile_true, conf.TopNfile_noisy, conf.topN)
utility.RE(conf.TopNfile_true, conf.TopNfile_noisy, conf.topN)
utility.ARE(conf.TopNfile_true, conf.TopNfile_noisy, conf.topN)
utility.FNR(conf.TopNfile_true, conf.TopNfile_noisy, conf.topN)

end = datetime.datetime.now()
print "Total running time:" + str(end - begin)
'''
f = open(conf.dataset_true)
lines = f.readlines()
utility.Recall(len(lines), conf.TopNfile_true, conf.TopNfile_noisy, conf.topN)
'''

