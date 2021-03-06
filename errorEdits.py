# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unicodedata
import codecs
import os

os.remove('pa_edits.txt')
f = codecs.open('pa_edits.txt','a',encoding = 'utf-8');

def edits_to_file(error,correct):
    le = len(error)
    lc = len(correct)
   
    lev_mat = [[0 for x in xrange(lc+1)] for x in xrange(le+1)]
    for i in range(le+1):
        lev_mat[i][0]=i
    for i in range(lc+1):
        lev_mat[0][i]=i
    i=1
    j=1
    for i in range(1,le+1):
        for j in range(1,lc+1):
            ins = lev_mat[i][j-1]+1
            dele = lev_mat[i-1][j]+1
            if(error[i-1]==correct[j-1]):
                subs = lev_mat[i-1][j-1]
            else:
                subs = lev_mat[i-1][j-1]+2
            lev_mat[i][j] = min(ins,dele,subs)
            a = error[i-1]
            b = correct[j-1]
            c = correct[j-2]
            if(lev_mat[i][j]==subs):
                if(a!=' 'and b!=' '):
                    f.write(error[i-1]+'|'+correct[j-1]+"\n")
            if(lev_mat[i][j]==ins):
                if(j-2>0 and c != ' ' and b !=' '):
                    f.write(correct[j-2]+'|'+correct[j-2]+correct[j-1]+"\n")
                elif (b != ' '):
                    f.write('#|'+correct[j-1]+"\n")
            if(lev_mat[i][j]==dele):
                if(j-1>0 and  a!= ' ' and b !=' '):
                    f.write(correct[j-1]+error[i-1]+'|'+correct[j-1]+"\n")
                elif (a!=' '):
                    f.write(error[i-1]+'|#'+"\n")

    for i in range(min(le,lc)-1):
        if(error[i]==correct[i+1] and error[i+1]==correct[i] and error[i]!=' ' and error[i+1] != ' '):
            f.write(correct[i+1]+correct[i]+'|'+error[i]+error[i+1]+"\n")

#editDis("ashudeep","ashudeaep")

def read():
   g = codecs.open('incorrect_correct.wl','r',encoding = 'utf-8')
   for line in g:
       #print line
       error = line.split(',')[0]
       correct = line.split(',')[1]
       edits_to_file(error,correct)

if __name__=="__main__":
	read()
	edits=dict()
	with open ("pa_edits.txt", "r") as myfile:
		for line in myfile:			
			line=line[:-1].decode('utf-8')
			try:
				edits[line]+=1
			except KeyError:
				edits[line]=1
	edits.pop('',None)
	os.remove('pa_edits_count.txt')
	g = codecs.open('pa_edits_count.txt','a',encoding = 'utf-8');
	for key in edits:
		g.write(key+"\t"+str(edits[key])+"\n")		
