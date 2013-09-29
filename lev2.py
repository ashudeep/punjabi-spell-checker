# -*- coding: utf-8 -*-
def levenshtein(s1, s2):
	s1='#'+s1+'$'
	s2='#'+s2+'$'
	x = [[0 for _ in range(len(s2))] for _ in range(len(s1))]
	ptrs=[[None for _ in range(len(s2))] for _ in range(len(s1))]
	for i in range(len(s1)):
		for j in range(len(s2)):
			if(j==0):
				x[i][j]=i
				ptrs[i][j]='DEL'
			if(i==0):
				x[i][j]=j
				ptrs[i][j]='INS'
				if(j==0):
					ptrs[i][j]='DIA'
			else:	
				x[i][j]=min(x[i-1][j]+1,x[i][j-1]+1,x[i-1][j-1]+2*(s1[i-1]!=s2[j-1]))
				if(x[i][j]==x[i-1][j-1]+2*(s1[i-1]!=s2[j-1])):
					ptrs[i][j]='DIA'
				elif(x[i][j]==x[i-1][j]+1):
					ptrs[i][j]='DEL'
				elif(x[i][j]==x[i][j-1]+1):
					ptrs[i][j]='INS'
	print list_edits(ptrs,s1,s2)
	#print ptrs
	#print x
def list_edits(ptrs,s1,s2):
	flag=1;
	i,j=0,0;
	list=[]
	while(i in range(len(s1)) and j in range(len(s2))):
		if(ptrs[i][j]=='DIA'):
			if(s1[i-1]!=s2[j-1]):
				list.append(s2[j-1]+"|"+s1[i-1])
			i+=1;
			j+=1;
		elif(ptrs[i][j]=='DEL'):
			list.append(s2[j-2]+s2[j-1]+"|"+s2[j-2])
			j+=1;
		elif(ptrs[i][j]=='INS'):
			list.append(s2[j-1]+"|"+s1[i-1]+s1[i])
			i+=1;
	return [a.encode('utf-8') for a in list]		
b="ਸਭਿਆਚਾਰਕਤਾ".decode('utf-8')

a="ਸੱਭਿਆਚਾਰਕਤਾ".decode('utf-8')

levenshtein(a,b)
