import sys
import os

prime = sys.argv[1]
result = os.popen('python sample.py --save_dir save --prime "' + prime  + '"').read()
print (result.split("\n")[0].split(" ")[len(prime.split(" "))-1])