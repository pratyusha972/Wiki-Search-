file_no = 1
line_no = 1 
sec_index = open("sec_doc_title.txt",'w')
doc_index = open("doc_to_title.txt")
doc_title = open("doc_title" + str(file_no)+ ".txt",'w')
for line in doc_index:
	if(line_no > 5000)
		doc_title.close()
		file_no += 1
		line_no = 1
		doc_title = open("doc_title" + str(file_no)+ ".txt",'w')
		line = line.strip('\n').split(':')[0] + str(file_no)
		sec_index.write(line)
	doc_title.write(line.strip('\n'))
	line_no+=1

