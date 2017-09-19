from collections import defaultdict
import os
import sys
import re
import math
flag_set = ('t','l','i','c','r')
for file_no in range(1259,1260):
	index_file = open("ind_" + str(file_no) + ".txt",'r')
	out_file = open("champion_" + str(file_no) + ".txt",'w')
	for line in index_file:
		mod1 = line.strip('\n').strip('|')
		entry = mod1.split(':')
		word = entry[0]
		posting_list = entry[1].split('|')
		doc_id_sum = 0
		tfidf_dict = defaultdict(float)
		flag_dict = []
		word_list = defaultdict(float)
		special_flag = 0
		count = 0
		if len(posting_list) >= 1:
			for posting in posting_list:
				special_flag = 0
				gap = int(posting.split('f')[0])
				actual_doc_id = gap + doc_id_sum
				count += 1
				doc_id_sum = gap
				if actual_doc_id > 0:
					word_list[actual_doc_id] = posting.split('f')[1]
					for flag in flag_set:
						if flag in posting:
							flag_dict.append(actual_doc_id)
							special_flag = 1
							break		
					if special_flag==0:		
						string = re.search('f[0-9]',posting)
						string2 = string.group(0)
						freq_flag = int(re.search(r'[0-9]',string2).group(0))
						tf_val = float(1 + math.log(float(freq_flag)))
						idf_val = math.log(float(17809008)/float(len(posting_list)))
						tfidf_val = tf_val * idf_val
						tfidf_dict[actual_doc_id] = tfidf_val
			
			sorted_tfidf_values = sorted(tfidf_dict.iterkeys(), key=lambda k: tfidf_dict[k], reverse=True)[:5000]
			flag_dict.extend(sorted_tfidf_values)
			key_default = 0
			string = word.encode('utf-8') + ":"
			sorted_tfidf_values.sort()
			for doc_id in sorted_tfidf_values:
				gap = int(doc_id) - int(key_default)
				string = string + str(gap) + 'f' + word_list[doc_id] + '|'
				key_default = int(doc_id)
			#string.strip('|')
			out_file.write(string + '\n')
		else:
			out_file.write(line)
	out_file.close()	
			



			
			
			
		
