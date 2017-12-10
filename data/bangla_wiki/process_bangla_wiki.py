import re
import codecs

data = open('bnwiki-20170101-pages-articles.xml', 'r', encoding="utf-8")

lines = ""
line_count = 0

words = []

for line in data:
    # line = data.readline()
    # lines += line
    
    replaced = re.sub('[a-zA-Z0-9<>।"/?+!৩২৫৪৯৮৬০৭১_,.=@#$%^&*(){}\[\]]+', ' ', line)
    replaced = re.sub('\n|\r|\t', ' ', replaced)
    replaced = re.sub(' +', ' ', replaced)
    replaced = re.split(' +', replaced)
    words.extend(replaced)
    
    line_count += 1
    if line_count % 1000 == 0:
        print("{2} % Completed, Total lines: {0}k of {1}k".format(line_count/1000, 10928, (line_count/10)/10928))
    


# full_data_corpus = " ".join(words)
output_file = codecs.open("bangla_corpus.txt", "w", "utf-8")
for i in range(len(words)):
    if words[i] is not '':
        output_file.write(words[i]+' ')
        
    if i % 1000 == 0:
        answer = (i/10)/(len(words)/1000)
        print("{2} % Completed, Total lines: {0}k of {1}k".format(i/1000, len(words)/1000, str(round(answer, 2)) ))

#output_file.write(full_data_corpus)
output_file.close()

count_dict = {}

for word in words:
    if word in count_dict.keys():
        count_dict[word] += 1
    else:
        count_dict[word] = 1

import operator
sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1))[::-1]

# output_file = codecs.open("bangla_word_freq_count.txt", "w", "utf-8")
with open('bangla_word_freq_count.txt','w',encoding='utf8') as f:
    for i in range(len(sorted_dict)):
        f.write(sorted_dict[i][0]+' ' + str(sorted_dict[i][1]) +'\n')
    


