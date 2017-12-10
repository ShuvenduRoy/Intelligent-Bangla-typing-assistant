data = open('text8', 'r')

lines = []
for line in data:
    lines.append(line)
    
words = line.split(" ")

count_dict = {}

for word in words:
    if word in count_dict.keys():
        count_dict[word] += 1
    else:
        count_dict[word] = 1
    
import operator
sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1))[::-1]

output_file = open("eng_word_count.txt", "w")
for i in range(len(sorted_dict)):
    output_file.write(sorted_dict[i][0]+' ' + str(sorted_dict[i][1]) +'\n')
    
output_file.close()