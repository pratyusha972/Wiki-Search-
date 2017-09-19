#!/usr/bin/python
import os
import sys
import xml.sax
import time
import math
import re
import Stemmer
from nltk.corpus import stopwords
from collections import OrderedDict
from collections import Counter
from collections import defaultdict
stemmer = Stemmer.Stemmer('english') 
#stop_words = set(stopwords.words('english')) 
word_list=defaultdict()
pages=0
class WikiHandler( xml.sax.ContentHandler ):

   def __init__(self):

      self.current = ""
      self.title = ""
      self.id = ""
      self.parent=""
      self.stemmer = stemmer 
      self.queue=[]
      self.refflag=0
      self.infflag=0
      self.linkflag=0
      self.text=""
      self.ref=""
      self.link=""
      self.inf=""
      self.cat=""
      self.pages=0 
      self.file_size=0
      self.file_no=0
      self.max_size = 1*pow(10,8)
   
   def startElement(self, tag, attributes):

      self.queue.append(tag)
      if self.current:
          self.parent = self.queue[-2]
      self.current = tag

   def endElement(self, tag):

      self.queue.pop()
      try:
      	    if self.queue[-1]=="page":
       	        self.pages+=1
		self.tokenizer(self.text,'b')
		self.tokenizer(self.cat,'c')
		self.tokenizer(self.link,'l')
		self.tokenizer(self.ref,'r')
		self.tokenizer(self.inf,'i')
            	self.text=""
      		self.ref=""
      		self.link=""
      		self.cat=""
		self.inf=""
		self.linkflag=0
		self.refflag = 0

      except Exception as e:
            global pages
	    pages = self.pages
      if self.file_size > self.max_size:
	    print self.file_no
	    print self.id
	    write_to_file(self.file_no)
	    self.file_no+=1
	    self.file_size=0
    
   def characters(self, content):

      self.file_size+=len(content)
      if self.current == "title":
           if re.search('[A-za-z0-9]',content):
           	self.title = content
      elif self.current == "text":
	   if content.startswith('[[Category:'):
		content = content.strip('[[Category:')
                self.cat+=content
	   elif content.startswith('==External Links==') or self.linkflag==1:
               	if content.startswith('{{') and not content.startswith('{{Sister'):
			self.linkflag = 0
			self.text+=content
		else:
	               self.link+=content
		       self.linkflag=1
	   elif content.startswith('==References==') or self.refflag==1:
		self.refflag=1
                words = content.split()
                self.ref+=content
		try:
                	if '}}' in words[-1]:
				self.refflag = 0
		except Exception:
			pass
	   elif content.startswith('{{Infobox') or self.infflag==1:
		self.infflag=1
                words = content.split()
                self.inf+=content
		try:
                	if '}}' in words[-1]:
				self.infflag = 0
		except Exception:
			pass
	   else:
                self.text+=content

      elif self.current == "id" and self.parent == "page":
           if re.search('[0-9]',content):
           	self.id = content
         	self.tokenizer(self.title,'t')
   
   def tokenizer(self,content,flag):

      if content!='':
	      pattern = re.compile(r'#[A-za-z0-9]{6}|[^A-Za-z]|\s|\n', re.DOTALL | re.MULTILINE | re.IGNORECASE)
	      words = pattern.split(content)
	      words=[word.lower() for word in words]
	      freq = Counter()
	      freq.update(words) 
	      temp1 = set(freq.keys()) - stop_words
	      temp = defaultdict(int)
	      for word in temp1:
		   if word!='':
			temp[self.stemmer.stemWord(word)]+=freq[word]
	      for word in temp:
		   freq_word = temp[word]
		   if word not in word_list:
			listtemp = {'f':freq_word,'inf':""}
			listtemp['inf']= listtemp['inf']+flag+str(freq_word)
			dicttemp = OrderedDict() 
			dicttemp[self.id] = listtemp
			word_list[word] = dicttemp
		   else:
			listl = word_list[word] 
			if self.id in listl:
				listl[self.id]['f']+=freq_word
				listl[self.id]['inf'] = listl[self.id]['inf']+flag+str(freq_word)
			else:
				listtemp = {'f':freq_word,'inf':""} 
				listtemp['inf']=listtemp['inf']+flag+str(freq_word)
				listl[self.id] = listtemp

def write_to_file(file_no):

	global word_list
        f = open(os.path.join(fileDir,"dict_file"+str(file_no)+".txt" ),'w')	
	word_list = OrderedDict(sorted(word_list.items()))
        #print word_list

	for word,value in word_list.iteritems():
	    	string = word.encode('utf-8') + ":" 
		key_default = 0    	
		for key in value:
			temp1 = value[key]['f']
			temp2 = value[key]['inf']
			gap = int(key) - int(key_default)
			print gap	
	 		string = string + str(gap) + 'f' +  str(temp1) + temp2 + '|'
			key_default = int(key) 
		string.strip('|')
		f.write(string + '\n')
	word_list = defaultdict()
        f.close()
 
if ( __name__ == "__main__"):
	
	fileDir = os.path.dirname(os.path.realpath('__file__'))
	#stopwords
	stop_words = set()
	with open("stopwords.txt") as f:
    		for line in f: 
        		stop_words.add(line.strip())
	
	inputfile = sys.argv[1]
     #   outputfile = sys.argv[2]
        inputf = open(inputfile,'r')
   	
	#parsing
	parser = xml.sax.make_parser()
   	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	Handler = WikiHandler()
	parser.setContentHandler( Handler )
	parser.parse(inputf)
	inputf.close()
#        write_to_file(1)

'''	#tfidf 
	tfidfdict=defaultdict(int)
        tfidfsum = 0
        for word,values in word_list.iteritems():
		totalfreq = 0
                df = len(values)
		idf = math.log10(pages/df)
		for key in values:
			totalfreq += values[key]['f']
	        tfidf =  (1 + math.log10(1+totalfreq))*idf
                tfidfdict[word] = tfidf
                tfidfsum+=tfidf

        tfidfavg = (tfidfsum/len(word_list)) 
       
	for word in word_list.keys():
            if tfidfdict[word] < tfidfavg:
		word_list.pop(word)
'''
