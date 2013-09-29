# -*- coding: utf-8 -*-
alphabet = 'ਔਐਆਈਊਭਙਘਧਝਢਞਠਛਥਖੜਫਉਇਅਏਓਁੰਣਨਵਲ਼ਸ਼ੱੌੈਾੀੂਬਹਗਦਜ਼ਡ਼ਟਚਤਕਰਪੁਿ੍ੇੋਂਮਨਵਲਸਯ'.decode('utf-8')
def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def edits2(word,freqs):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in freqs)

#print edits2("ashu")
i=0;
freqs=dict()
with open ("wordlist_full_mod2.pun", "r") as myfile:
	for line in myfile:			
		line=line
		try:
			[f,w]=line.split(' ');
			w=w[:-1]
			w=w.decode('utf-8')
			freqs[w]=f
		except ValueError:
			continue
for word,freq in freqs.iteritems():
	for word1 in edits1(word):#,freqs):
		try:
			if(freqs['word1']<freq/3):
				del freqs['word1']
		except KeyError:
			pass
with open("filtered_list.pun","a") as f:
	for word,freq in freqs.iteritems():
		word=word.encode('utf-8')
		f.write(word+"\t"+freq+"\n")
