import re
import codecs

data = open('bnwiki-20170101-pages-articles.xml', 'r', encoding="utf-8")

lines = ""

for line in data:
    # line = data.readline()
    lines += line
    # print(line)  
    
replaced = re.sub('[a-z0-9<>"/-?-_,.=-@#$%^&*(){}]+', ' ', lines)
replaced = re.sub('\n|\r|\t', ' ', replaced)
replaced = re.sub(' +', ' ', replaced)
words = re.split(' +', replaced)

full_data_corpus = " ".join(words)
output_file = codecs.open("bangla_corpus.txt", "w", "utf-8")

output_file.write(full_data_corpus)
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
    


