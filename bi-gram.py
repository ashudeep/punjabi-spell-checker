# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unicodedata
import codecs
#import regex
import re, string, random, glob, operator, heapq
from collections import defaultdict
from math import log10
import sys
sys.setrecursionlimit(10000)


alphabet = 'बहगदडजपरकतचटमनवलसयभङघधझढञफऱखथछठणऩशषऔऐौैाीूुि्ेोॆं़ॉृॊःऋआईऊओएअइउऎँऑ'


h = codecs.open('correct_1bi.txt','a',encoding = 'utf-8')


def product(nums):
    "Return the product of a sequence of numbers."
    return reduce(operator.mul, nums, 1)


def corrections(word, prev, next):
    "Spell-correct all words in text."
    correct_word = correct(word, prev, next)
    if word!=correct_word:
        #print word,":",correct_word
        h.write(word+' : '+correct_word+'\n')
    #print
    #return regex.sub('[\w]+', lambda m: correct(m.group(0)), text)


def correct(w, prev, next):
    "Return the word that is the most likely spell correction of w."
    candid = edits(w)   ##now we have the candidates with the edits as the possible replacements
    if (prev=="" and next == "") or (prev==" " and next==" "):# or prev:
        print w
        candidates = sorted(candid, key=lambda (c,e): Pedit(e) * Pw(c), reverse=True)
    elif prev=="":
        candidates= sorted(candid.iteritems(), key=lambda (c,e): cPw(next,c), reverse=True)
    elif next=="":
        candidates= sorted(candid.iteritems(), key=lambda (c,e): cPw(c,prev), reverse=True)
    else:
        candidates= sorted(candid.iteritems(), key=lambda (c,e): cPw(next,c) * cPw(c,prev), reverse=True)
    #candidates = sorted(candid, key=lambda (c,e): Pedit(e) * Pw(c), reverse=True)
    #print candidates
    c1=""
    c2=""
    c3=""
    c=""
    l = len(candidates)
    #sorted_x = sorted(candidates.iteritems(), key=operator.itemgetter(1))
    if(l!=0):
        c1, edit1 = candidates[0]
        c = c1
        if(l>1):
            c2, edit2 = candidates[1]
            c = c+','+c2
        if(l>2):
            c3, edit3 = candidates[2]
            c = c+','+c3
        return c
    else:
        return w



class Pdist(dict):
    "A probability distribution estimated from counts in datafile."
    def __init__(self, data, N=None, missingfn=None):
        for key,count in data:
            self[key] = self.get(key, 0) + int(count)
            self.N = float(N or sum(self.itervalues( )))
            self.missingfn = missingfn or (lambda k, N: 1./N)
    def __call__(self, key):
        if key in self: return self[key]/self.N
        else: return self.missingfn(key, self.N)


N = 7000567 ## Number of tokens in corpus


def datafileUni(name, sep=' '):
    "Read key,value pairs from file."
    test = codecs.open(name,'r',encoding = 'utf-8')
    for line in test:
        yield line.split(sep)


def datafileBi(name, sep='\t'):
    "Read key,value pairs from file."
    test = codecs.open(name,'r',encoding = 'utf-8')
    for line in test:
        yield line.split(sep)

def datafile(name, sep=' '):
    "Read key,value pairs from file."
    uni_vocab = codecs.open(name,'r',encoding = 'utf-8')
    for line in uni_vocab:
        #print line
        yield line.split(sep)


def avoid_long_words(word, N):
    "Estimate the probability of an unknown word."
    return 10./(N * 10**len(word))


N_bi = 6255937 * 2 + 34413           ## Number of bi tokens in corpus

Pw = Pdist(datafileUni('count_uni_final.txt'), N, avoid_long_words)


P2w = Pdist(datafileBi('count_bigram_final.txt'), N_bi)  ##finds the probability of each token (bigram here)


def cPw(word, prev):
    "Conditional probability of word, given previous word."
    try:
        return P2w[prev + ' ' + word]/float(Pw[prev])
    except KeyError:
        return Pw(word)



#P(w | c) is computed by Pedit:
def Pedit(edit):
    "The probability of an edit; can be '' or 'a|b' or 'a|b+c|d'."
    if edit == '':
        return (1. - p_spell_error)
    return p_spell_error*product(P1edit(e) for e in edit.split('+'))

p_spell_error = 1./20.

P1edit = Pdist(datafile('count_edit_final.txt')) ## Probabilities of single edits

def edits(word, d=2):   #d is the edit distance
    "Return a dict of {correct: edit} pairs within d edits of word."
    ## e.g. edits('adiabatic', 2)
    ## returns {'adiabatic': '', 'diabetic': '<a|<+a|e', 'diabatic': '<a|<'}
    results = {}
    def editsR(hd, tl, d, edits):
        def ed(L,R): return edits+[R+'|'+L]
        C = hd+tl
        if C in Pw:
            e = '+'.join(edits)
            if C not in results: results[C] = e
            else: results[C] = max(results[C], e, key=Pedit)
        if d <= 0: return
        extensions = [hd+c for c in alphabet if hd+c in PREFIXES]
        p = (hd[-1] if hd else '#') ## previous character '#' in place of '<' for marking start of string
        ## Insertion
        for h in extensions:
            editsR(h, tl, d-1, ed(p+h[-1], p))
        if not tl: return
        ## Deletion
        editsR(hd, tl[1:], d-1, ed(p, p+tl[0]))
        for h in extensions:
            if h[-1] == tl[0]: ## Match
                editsR(h, tl[1:], d, edits)
            else: ## Replacement
                editsR(h, tl[1:], d-1, ed(h[-1], tl[0]))

        ## Transpose
        if len(tl)>=2 and tl[0]!=tl[1] and hd+tl[1] in PREFIXES:
            editsR(hd+tl[1], tl[0]+tl[2:], d-1,ed(tl[1]+tl[0], tl[0:2]))

    ## Body of edits:
    editsR('', word, d, [])
    return results


PREFIXES = set(w[:i] for w in Pw for i in range(len(w) + 1))


if __name__=="__main__":
    test = codecs.open('hi-spell2.txt','r',encoding = 'utf-8').readlines()
    #print test
    #test=test.decode('utf-8')
    for line in test:
#        print "Line is:  "+line
        test1=line.split(' ')
        l = len(test1)
        #print l
        if l>0:
            for i in range(l):
                #print test1[i]
                w=test1[i]#.encode('utf-8')
#                print "word:    " + w
                prev=""
                next=""
                if i>0:
                    p=i-1
                    prev=test1[p]#.encode('utf-8')
#                    print "prev:    "+ prev#.encode('utf-8')
                if i<l-1:
                    n=i+1
                    next=test1[n]#.encode('utf-8')
#                    print "next:    "+ next#.encode('utf-8')

                if w!="" and w!=" " and w!="\t" and w!="\n":
                    corrections(w, prev, next)
            #print prev,"+",w,"+",next

        #for w in test1:
        #     w.encode('utf-8')
        #     print w
          #   corrections(w)
        #print test1.encode('utf-8')
    #test1=test.split(' ')
    #print test1
    #print test
    #corrections(test)
