file_no = 1
line_no = 1 
sec_index = open('sec_index_actual.txt','w')
index = open('index.txt','r')
index_file = open("ind_" + str(file_no)+ ".txt",'w')
for line in index:
	index_file.write(line)
	line_no+=1
	if line_no == 5000:
		outline = line.strip('\n').split(':')[0] + ':' + str(file_no)
		sec_index.write(outline + '\n')
		index_file.close()
		file_no += 1
		line_no = 1
		index_file = open("ind_" + str(file_no)+ ".txt",'w')

