#!/usr/bin/python
import os
import sys
import xml.sax
import re
class WikiHandler( xml.sax.ContentHandler ):

   def __init__(self):

      self.current = ""
      self.title = ""
      self.parent=""
      self.queue=[]
   
   def startElement(self, tag, attributes):

      self.queue.append(tag)
      if self.current:
          self.parent = self.queue[-2]
      self.current = tag

   def endElement(self, tag):

      self.queue.pop()
    
   def characters(self, content):

      if self.current == "title":
           if re.search('[a-zA-Z0-9]',content):
           	self.title = content
      elif self.current == "id" and self.parent == "page":
           if re.search('[0-9]',content):
	    	string = str(str(content).encode('utf-8')) + ":" + self.title.encode('utf-8') 
		f.write(string + '\n')
   
if ( __name__ == "__main__"):
	
	fileDir = os.path.dirname(os.path.realpath('__file__'))
	inputfile = sys.argv[1]
        inputf = open(inputfile,'r')
        f = open("doc_to_title.txt",'w')
   	
	#parsing
	parser = xml.sax.make_parser()
   	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	Handler = WikiHandler()
	parser.setContentHandler( Handler )
	parser.parse(inputf)
	inputf.close()
	f.close()
