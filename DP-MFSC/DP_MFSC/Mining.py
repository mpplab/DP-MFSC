# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 16:42:06 2017

@author: 84664
"""
import random
import itertools

import numpy as np
import math
import sys
sys.path.append( 'conf' )
import dp_conf as conf
from scipy.optimize import fsolve
from scipy.special import comb
import re

def chunks(l, n):
    for i in range(0,len(l), n):
        yield l[i:i+n]

def generate_candidate(FS,alphabet):
    ck=[]
    for cs in FS:
        for word in alphabet:
            ck.append(cs + word)
    return ck
            
def randomly_partition_database(newlineslist, number):
    random.shuffle(newlineslist) 
    if len(newlineslist) < number:
        print "The dataset is too small! No need to be divided."
    else:
        size = (len(newlineslist) / number) 
        print "size：" + str(size)
        dbSets = list(chunks(newlineslist, size))
        print len(dbSets)
        if len(dbSets) != number:
            del dbSets[-1]
    return dbSets

def getKConsecutiveSup(p, n, seq):
    '''
    ??这步还需要完善
    Sample:
    seq = "abaabaabaccaccaccbaba", k = 3
    result = "aba:3 cca:2 ccb:1 aba:1 "
    '''
    cps = p.sub(lambda m: m.group(1)+":"+str(1+len(m.group(2))/n)+" ", seq)
    return cps

def getcandidate(alphabet, k):
    #alphabetlist = list(alphabet)
    can = []
    candidate = []
    can = itertools.product(alphabet,repeat = k)
    for c in can:
        c = ''.join(c) 
        candidate.append(c)
    print len(candidate)
    return candidate 

def calculate_lmax(dbset):
    return max([len(i) for i in dbset])
    
def irrelevantItemDeletion(seqList, Ck):
    #resultList = []
    #alphaDict = dict([(i, seq.count(i)) for i in set(seq) if i.isalpha()])
    alphaList = list([i for i in set("".join(Ck)) if i.isalpha()])
    #print alphaList
    #sumDeletingLen = 0
    subSeqList = []
    for seq in seqList:
        seqSet = list(seq)
       # print seq
        curSeq = []
        newcurSeqList = []
        
        for item in seqSet:
            if item != ' ' and item != '\n':
                if item not in alphaList:
                    #print str(item) + " is not in candidate alphaList"
                    #a.replace(item, '*')
                    #sumDeletingLen += 1
                    curSeq.append('*')
                else:
                    curSeq.append(item)
        '''
        1.去除前缀和后缀的特殊字符'*'
        2.连续特殊字符'*'删除
        3.相同子序列删除，只保留一个(如何实现?)
        注释：执行1,2以后,每条序列从*处分割成几条子序列,这步有待商榷，暂时这样处理
        '''
        newcurSeq = "".join(curSeq).strip('*')  
        #print newcurSeq
        newcurSeqList = newcurSeq.split('*')
        SeqList = [x for x in newcurSeqList if x!='']
        subSeq = '*'.join(SeqList)
        subSeqList.append(subSeq)
        #print newcurSeqList
        '''
        for subSeq in newcurSeqList :
            if subSeq != '' :
                subSeqList.append(subSeq)
        '''
    print "subSeqList--length: " + str(len(subSeqList))
                
    return subSeqList
        #resultList.append("".join(curSeq))    

    #print "sum deleting length:" + str(sumDeletingLen)
    #return resultList

'''
    compress consecutive j patterns into consecutive k patterns
    each pattern contains no more than 3 items
    eg.  seq = abbbbbaababaabababa,k=2
    first,n=1; newseq = abbaababaabababa
    second,n=2; newseq = abbaababa(实现起来复杂？)
'''
def CompressConsecutivePatterns(seqList, k):
    resultList = []
    #num = 1
    #sumDeletingLen = 0
    for seq in seqList:
        #minLen = len(seq)
        #curSeqGen = seq
        curSeqGen = seq
        
        for n in range(1, 4):
            #print "n=" + str(n)
            rule = ur"(\w{%d})(\1*)" % n
            #print "rule:" + str(rule)
            p = re.compile(rule)
            curSeq = compressConsecutiveSeq(p, n, curSeqGen, k)
            #print "genSeq=" + curSeq
            #if len(curSeq) < minLen:
            curSeqGen = curSeq
                #minLen = len(curSeq)
        #print "No." + str(num) + ":" + seq + "->" + curSeqGen
        #deletingLen = len(seq) - len(curSeqGen)
        #print "No." + str(num) + ": delete length: " + str(deletingLen)
        #sumDeletingLen += deletingLen
        #num += 1
        resultList.append(curSeqGen)
    #print "sum deleting length:" + str(sumDeletingLen)
            
    return resultList  

def compressConsecutiveSeq(p, n, seq, k):
    cps = getKConsecutiveSup(p, n, seq)
    #print seq + ":" + cps
    cpsDic = cps.split(' ')
    resultStr = ""
    for cur in cpsDic:
        curMode = cur.split(':')[0]
        if len(cur.split(':')) == 2:
            modeLen = int(cur.split(':')[1])
            #print "modeLen=" + str(modeLen) + " k=" + str(k)
            if modeLen > k:
                modeLen = k
            #print "curMode=" + curMode
            #print "modeLen=" + str(modeLen)
            #print "curMode * modeLen=" + str(curMode * modeLen)
            resultStr += curMode * modeLen
        else:
            if curMode != " ":
                resultStr += curMode
    #print "resultStr:" + resultStr
    return resultStr

def discover_potentially_frequent_sequences(ck, new_dbSet, epsilon1, newtheta,l_max,k):
    PF = []
    for each in ck:
        count = 0
        '''
        rule = ur"(?=%s)" % each
        reg = re.compile(rule)
        '''
        for seq in new_dbSet:
            if each in seq:
                count += 1
                #length = len(reg.findall(seq))
                #print(length)
                #count +=length
        #deltak = min(comb(l_max, k), len(ck))
        deltak = l_max - k + 1
        #print "deltak: " + str(deltak)
        if count + np.random.laplace(0, deltak / epsilon1, 1)[0] >= newtheta * len(ck) :
            PF.append(each)
    return PF
'''
def erfc(x):
   
    result = 2.0/sy.sqrt(pi)*integrate(exp((-t*t)),(t,x,float("inf")))
    #print "erfc result" + str(result)
    print type(result)
    return result
'''

def cdf(z):
    mu = conf.mu
    sigma = conf.sigma
    Lambda = conf.Lambda
    phi = conf.phi
    #const = Lambda + mu - z  #常用
    #print type(const)
    #print "const:" + str(Lambda + mu - z)
    #print type( E**(I*pi))
    #print type(0.5 *  erfc(Lambda + mu - z/(sy.sqrt(2)*sigma)) )
    #print type(exp((Lambda + mu - z)/phi + sigma * sigma/(2 * phi * phi)))
    #- 0.25 * exp((Lambda + mu - z/phi + sigma * sigma/(2 * phi * phi))) *  erfc((Lambda + mu - z )/(math.sqrt(2) * sigma) + sigma/(math.sqrt(2) * sigma)))
    
    return 0.5 * math.erfc((Lambda + mu - z)/(math.sqrt(2)*sigma)) \
    - 0.25 * math.exp(((Lambda + mu - z)/phi + sigma * sigma/(2 * phi * phi))) * math.erfc((Lambda + mu - z)/(math.sqrt(2) * sigma) + sigma/(math.sqrt(2) * phi)) \
    + 0.25 * math.exp(((-(Lambda + mu - z)/phi) + sigma * sigma/(2 * phi * phi))) * math.erfc((-(Lambda + mu - z)/(math.sqrt(2) * sigma)) + sigma/(math.sqrt(2) * phi)) - 0.3
    
def SamplingbasedCandidatePruning(k, CandidateSet, dbSet, epsilon1, theta):
    print "\n"
    print "\n"
    print ">>>>>>>>>This is k = %d ."%k
    print "len of dbset: " + str(len(dbSet))
    print "len of CandidateSet:  " + str(len(CandidateSet))
    print ">>>step1: Sequence Shrinking start"
    print "Irrelevant Item Deletion"
    #print len(dbSet)
    new_dbSet = irrelevantItemDeletion(dbSet, CandidateSet)
    #print " End     Irrelevant Item Deletion"
    print "original lmax:" + str(calculate_lmax(dbSet))
    #print new_dbSet
    print "after irrelevantItemDeletion lmax:" + str(calculate_lmax(new_dbSet))
    print "Consecutive Patterns Compression"
    new_dbSet = CompressConsecutivePatterns(new_dbSet, k)
    l_max = calculate_lmax(new_dbSet)
    print "after CompressConsecutivePatterns lmax:" + str(l_max)
    #print " End    Consecutive Patterns Compression"
    
    '''
    阈值松弛待写
    '''
    print ">>>step2: Relax threshold theta  "
    
    #print ">step2: Dataset reconstruction  "
    #new_dbSet = RST.dbsetReconstruction(new_dbSet, CandidateSet, l_max, k)
    #print " End    Dataset reconstruction"
    
    #newtheta = theta - 0.005
    print "theta: " + str(theta)
    print "factorial(l_max)/factorial(k): " + str(math.factorial(l_max)/math.factorial(k))
    print "len(CandidateSet): " + str(len(CandidateSet))
    conf.mu = theta * len(new_dbSet)
    conf.sigma = math.sqrt(theta*(1-theta)*len(new_dbSet))
    conf.Lambda = 0
    print  min(math.factorial(l_max)/math.factorial(k), len(CandidateSet))
    #deltak = min(comb(l_max, k), len(CandidateSet))
    deltak = min(l_max - k + 1 , len(CandidateSet))
    print "comb: " + str(comb(l_max, k))
    print "len(ck): " + str(len(CandidateSet))
    conf.phi = deltak / epsilon1
    
    print "mu: " + str(conf.mu) +" sigma: " + str(conf.sigma) + " Lambda: " + str(conf.Lambda) +  " phi:" + str(conf.phi)
    
    newtheta = fsolve(cdf,0.0000001)[0]
    #newtheta = 0.0
    #print "方程的解：" + str(cdf(newtheta))
    print "*******newtheta: " + str(newtheta)
    print "l_max: " + str(calculate_lmax(dbSet))
    PF = discover_potentially_frequent_sequences(CandidateSet, new_dbSet, epsilon1, newtheta, l_max, k)
    print "potential frequnet sequences: " + str(len(PF))
    
    #print PF
    
    return PF

def discover_frequent_sequence1(k,new_ck, epsilon, D, theta):
    FSk = []
    FSk_sup = []

    for each in new_ck:
        count = 0
        '''
        rule = ur"(?=%s)" % each
        reg = re.compile(rule)
        '''
        for seq in D:
            if each in seq:
                count += 1
                #length = len(reg.findall(seq))
                #print(length)
                #count +=length
        '''
        这个地方加噪的敏感度待商榷
        '''
        #nosiyCount = count + np.random.laplace(0,len(new_ck)/epsilon,1)[0]
        sensisity = (calculate_lmax(new_ck) - k + 1)
        nosiyCount = count + np.random.laplace(0,sensisity/epsilon,1)[0]
        #print theta * len(D)
        if  nosiyCount >= theta * len(D):
            FSk.append(each)
            FSk_sup.append(nosiyCount)
    print "len of FSK: " + str(len(FSk))
            
    return FSk,FSk_sup

def discover_frequent_sequence2(new_ck, D, theta):
    FSk = []
    FSk_sup = []

    for each in new_ck:
        '''
        count = 0
        rule = ur"(?=%s)" % each
        reg = re.compile(rule)
        '''
        count = 0
        for seq in D:
            if each in seq:
                count += 1
                #length = len(reg.findall(seq))
                #print(length)
                #count +=length

        if  count >= theta * len(D):
            FSk.append(each)
            FSk_sup.append(count)
            
    return FSk,FSk_sup