i=0;
with open ("filtered_list.pun", "r") as myfile:
	for line in myfile:			
		line=line
		try:
			[w,f]=line.split('\t');
			w=w.decode('utf-8')
			f=f[:-1]	
		except ValueError:
			continue
		if(int(f)>=2):
			w=w.encode('utf-8')
			print w,f
