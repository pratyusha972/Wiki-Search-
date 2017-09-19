from heapq import merge
import os
from collections import defaultdict
from collections import OrderedDict
result = open("index.txt",'w')
sec_index = open("sec_index.txt",'w')
path = '/home/pratyusha/SEM_4-1/IRE/Mini_Project/phase2/indexes/index_files/'
starting = ""
count = 0
line_no = 0
flag = 0
max_no_words = 5*pow(10,3)
postings_list = defaultdict()
sum_doc_ids = defaultdict()
sum_doc_ids[0] = 0
for line in merge(*[open(path+str(f),'r') for f in os.listdir(path)]):
		line = line.strip('\n')
		temp = line.split(':')
		if starting!=temp[0]:
			if flag!=0:
				result.write('\n')
			count+=1
			doc_id_last = 0
			final_posting = starting + ':' 
			if count > max_no_words:
				sec_index.write(final_posting+str(line_no)+'\n')
				count = 0
			line_no+=1
			if postings_list:
				flag = 1
				sorted_postings = OrderedDict(sorted(postings_list.items()))
				for pos in sorted_postings:
					gap_first = pos - sum_doc_ids[doc_id_last] # modified doc id 
					doc_id_last = pos 
					final_posting += str(gap_first) + sorted_postings[pos]  # doc_id + rest
     				result.write(final_posting.strip('\n'))
				postings_list = defaultdict()
				sum_doc_ids = defaultdict()
				sum_doc_ids[0] = 0
			starting = temp[0]

		string1 = temp[1].split('|',1)  #first posting 
		string2 = string1[0].split('f') #first posting split on f
		first_doc_id = int(string2[0])
		modified_string = 'f' + string2[1] + '|' + string1[1]  # f + second part of f + '|' + rest
		postings_list[first_doc_id] = modified_string
		postings = string1[1].strip('|').split('|')
		sum_doc_id = first_doc_id 
		for pos in postings:
			if pos!= '':
				sum_doc_id += int(pos.split('f')[0])
		sum_doc_ids[first_doc_id] = sum_doc_id
result.close()
'''
	gap_first = first_doc_id - doc_id_last #doc id 
	modified_string = str(gap_first) + 'f' + string2[1] + '|' + string1[1]  # doc_id + f + second part of f + '|' + rest
	result.write(modified_string.strip('\n'))
	posting_list = (temp[1].strip('\n').strip('|')).split('|')
	for pos in posting_list:
		doc_id_last += int(pos.split('f')[0])
	'''
	#else:
		#result.write(line.strip('\n'))
		
	#posting_list = (temp[1].strip('\n').strip('|')).split('|')
	#for pos in posting_list:
	#	doc_id_last += int(pos.split('f')[0])
