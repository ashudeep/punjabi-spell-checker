# -*- coding: utf-8 -*-
import re, collections, codecs

'''
def words(text): 
	return re.findall(ur'[\u0a00-\u0a7f]+',text) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('newspapers.txt').read().decode('utf-8')))
'''
NWORDS=dict()
with open ("wordlist_full_mod2.pun", "r") as myfile:
	for line in myfile:
		try:
			[f,w]=line.split(' ');
			w=w[:-1]
			w=w.decode('utf-8')
			NWORDS[w]=int(f)
		except ValueError:
			continue

BIGRAMS=dict()
with open("Pan_2-Grams.txt", "r") as myfile:
	for line in myfile:			
		try:
			[w1,w2,f]=line.split('\t');
			f=f[:-1]
			w1=w1.decode('utf-8')
			w2=w2.decode('utf-8')
			BIGRAMS[w1+" "+w2]=int(f)
		except ValueError:
			continue


alphabet = 'ਔਐਆਈਊਭਙਘਧਝਢਞਠਛਥਖੜਫਉਇਅਏਓਁੰਣਨਵਲ਼ਸ਼ੱੌੈਾੀੂਬਹਗਦਜ਼ਡ਼ਟਚਤਕਰਪੁਿ੍ੇੋਂਮਨਵਲਸਯ'.decode('utf-8')

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word, prev_word):
    return set(e2+" "+prev_word for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words, prev_word): return set(w+" "+prev_word for w in words if w in NWORDS)

def correct(word, prev_word):
    candidates = known([word], prev_word) or known(edits1(word), prev_word) or known_edits2(word,prev_word) or [word+" "+prev_word]
    return max(candidates, key=BIGRAMS.get).split(' ')[0]

def corrections(word, prev_word):
    "Spell-correct all words in text."
    correct_word = correct(word, prev_word)
    #print word+' : '+correct_word
    
    if word!=correct_word:
        #print word,":",correct_word
        print word+' : '+correct_word
    #print
    #return regex.sub('[\w]+', lambda m: correct(m.group(0)), text)

if __name__=="__main__":
    test = codecs.open('incorrect.txt','r',encoding = 'utf-8').readlines()
    #test=test.decode('utf-8')
    for line in test:
	line=line[:-1]
        test1=line.split(' ')
	prev_word=" "
        for w in test1:
             w.encode('utf-8')
             corrections(w,prev_word)
             prev_word=w