# -*- coding: utf-8 -*-
import codecs
import os
os.remove('comparison.txt')
h = open('comparison.txt','a')#split("\n")
h.write("Word\taspell_suggestions\tmy_code_suggestions\n");
with open ("aspell_results.txt", "r") as aspell_results:
	my_results = open('correct.txt','r').readlines()
	for line1 in aspell_results:			
		line1=line1[:-1].decode('utf-8')
		if line1.split(' ')[0]=='&':# or line1.split(' ')[0]=='#':
			h.write(line1.split(' ')[1].encode('utf-8')+"\t")
			corrections=line1.split(':')[1].split(", ")
			try:
				h.write(corrections[0].encode('utf-8')+","+corrections[1].encode('utf-8')+","+corrections[2].encode('utf-8')+"\t")
			except IndexError:
				try:
					h.write(corrections[0].encode('utf-8')+","+corrections[1].encode('utf-8')+"\t")
				except IndexError:
					try:
						h.write(corrections[0].encode('utf-8')+"\t")
					except IndexError:
						h.write("\t")
					
			for line in my_results:
				line=line.decode('utf-8')
				if line.split(" : ")[0]==line1.split(' ')[1]:
					h.write(line.split(" : ")[1][:-1].encode('utf-8')+"\n");
					break
		elif line1.split(' ')[0]=='#':
			h.write(line1.split(' ')[1].encode('utf-8')+"\t")
			h.write('<No Replacements>\t');
			for line in my_results:
				line=line.decode('utf-8')
				if line.split(" : ")[0]==line1.split(' ')[1]:
					h.write(line.split(" : ")[1][:-1].encode('utf-8')+"\n");
					break
					
					
