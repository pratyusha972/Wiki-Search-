import os
import linecache
import re
import math
import Stemmer
import time
from collections import defaultdict
from collections import OrderedDict
from collections import Counter
stemmer = Stemmer.Stemmer('english') 
word_list=defaultdict()
total_doc_list=defaultdict()
sorted_tfidf_values = defaultdict(float) 
tfidf_dict = defaultdict(float)

def tokenizer(content,flag):
	if content!='':
	#      start_time = time.time()
	      pattern = re.compile(r'#[A-za-z0-9]{6}|[^A-Za-z]|\s|\n', re.DOTALL | re.MULTILINE | re.IGNORECASE )
	      words = pattern.split(content)
	      words=[word.lower() for word in words]
	      freq = Counter()
	      freq.update(words) 
	      temp1 = set(freq.keys()) - stop_words
	      temp = defaultdict(int)
	      for word in temp1:
		   if word!='':
			temp[stemmer.stemWord(word)]+=freq[word]
	      for word in temp:
		   freq_word = temp[word]
		   if word not in word_list:
			dicttemp = {'f':freq_word,flag:0}
			dicttemp[flag] = freq_word
			word_list[word] = dicttemp
		   else:
			dictl = word_list[word] 
			dictl['f'] += freq_word
			dictl[flag] += freq_word
	      
       #       print("--- %s seconds ---input conversion" % (time.time() - start_time))

def search():

      flag_pattern = re.compile(r'[0-9]')
      for word in word_list.keys():
#	   try:
	   flag_word = set(word_list[word].keys())
	   #in index searching
	   file_no = 1
	   for key in term_to_term_id:
		if word <= key:
			break
		file_no+=1
	   chunk_index_file = open("post_merge_index_files/ind_" + str(file_no) + ".txt")
	   #print file_no, "file_no"
	   for line in chunk_index_file:
		key = line.split(':')
		if word == key[0]:
			line = line.strip('\n').strip('|')
			break
	   #print line
	   word_postinglist = line.split(':')
	   posting_list = word_postinglist[1].split('|')
	    
	   doc_id_sum = 0
	   #print posting_list
	   for pos_list in posting_list:   #in all the post_lists
		#print pos_list
		#frequency of the word	
	   	total_tfidf = 0.00
		flag_index = set(flag_pattern.split(pos_list)) #flags in the token in index
		
		title_flag = 0
		if 'f' in flag_word: 
			if 't' in flag_index:
				title_flag = 1

		common_flags = flag_word.intersection(flag_index) #getting common flags

		for flag in common_flags:
			if flag!='':

				string = re.search(flag+'[0-9]',pos_list)   
				string2 = string.group(0)
				freq_flag = int(re.search(r'[0-9]',string2).group(0))
				idf_val = math.log(float(17809008)/float(len(posting_list)))
				
				if title_flag==1 and flag=='f':
					freq_flag *= 10000
	
				tf_val = float(1 + math.log(float(freq_flag)))
				tfidf_val = tf_val * idf_val
				total_tfidf += tfidf_val
		
		current_doc_id = int(pos_list.split('f')[0])
		actual_doc_id = doc_id_sum + current_doc_id
		tfidf_dict[actual_doc_id] = tfidf_dict[actual_doc_id] + total_tfidf
		doc_id_sum += current_doc_id

   #except Exception:
#	   pass
#      print tfidf_dict
      global sorted_tfidf_values
      sorted_tfidf_values = sorted(tfidf_dict.iterkeys(), key=lambda k: tfidf_dict[k], reverse=True)[:100]
#      print sorted_tfidf_values
	 
def display_results():

#	starttime = time.time()
	count = 0
	global sorted_tfidf_values
	#print sorted_tfidf_values
	for docid in sorted_tfidf_values:
		try:
			file_no = 1
			for key in doc_to_title_dict:
				if docid < key:
					break
				elif docid == key:
					file_no += 1
					break
				file_no+=1
			
			doc_to_title_file = open("sec_ind_doc_title/doc_title" + str(file_no) + ".txt")
			for line in doc_to_title_file:
				line = line.split(':',1)
				if docid == int(line[0]):
					print line[1].strip('\n')
			if count == 10:
				break
			count+=1
			#print linecache.getline("doc_to_title.txt",doc_to_title_dict[docid]).split(':')[1].strip('\n')
		except Exception:
			pass
#	print("--- %s seconds --- display" % (time.time() - start_time))
		
if ( __name__ == "__main__"):

	fileDir = os.path.dirname(os.path.realpath('__file__'))
	#start_time = time.time()
	#stopwords
	stop_words = set()
	with open("stopwords.txt") as f:
		for line in f: 
			stop_words.add(line.strip())

	sec_index_f = open(os.path.join(fileDir,"sec_index_actual.txt"),'r')
	term_no = 1
	term_to_term_id = OrderedDict()
	for line in sec_index_f:
		 line = line.split(':')
		 term_to_term_id[line[0]] = term_no
		 term_no+=1
	#print("--- %s seconds ---" % (time.time() - start_time))

	#doc_to_title
	#start_time = time.time()
	doc_to_title = open(os.path.join(fileDir,"sec_doc_title.txt"),'r')
	term_no = 1
	doc_to_title_dict = OrderedDict()
	for line in doc_to_title:
	         line = line.split(':',1)
	         doc_to_title_dict[int(line[0])] = term_no
	         term_no+=1
	#print("--- %s seconds ---" % (time.time() - start_time))

	while(1):
		#taking in queries
		query = raw_input("Search query\n")
		title = raw_input("Title\n")
		body = raw_input("Body\n")
		cat = raw_input("Categories\n")
		ext_link = raw_input("External_links\n")
		ref = raw_input("References\n")
		info_box = raw_input("Info_box\n")
		
		#tokenizer
		start_time = time.time()
		tokenizer(query,'f')
		tokenizer(title,'t')
		tokenizer(body,'b')
		tokenizer(cat,'c')
		tokenizer(ext_link,'l')
		tokenizer(ref,'r')
		tokenizer(info_box,'i')
		search()
		display_results()
		word_list=defaultdict()
		total_doc_list=defaultdict()
		sorted_tfidf_values = defaultdict(float) 
		tfidf_dict = defaultdict(float)
		print("--- %s seconds ---" % (time.time() - start_time))

