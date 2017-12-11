data = open('banglaDict.txt', 'r', encoding="utf-8")

count = 0
lines = []

for line in data:
    line = line.split('|')
    lines.extend([line[1]+'\n', line[2]])
    
    count += 1
    if count % 1000 == 0:
        print(count)
        

with open('proces_bangla_dict.txt','w',encoding='utf8') as f:
    for i in range(len(lines)):
        f.write(lines[i])