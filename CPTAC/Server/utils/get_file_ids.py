#/usr/bin/env python
import json
import sys
import subprocess

def concat(arr, delim):
    final = ""
    for x in arr:
        final += x + delim
    return final[:-1]

results = subprocess.check_output(['rclone', 'lsjson', '-R', 'PayneLabData:'])
files = json.loads(results)

resultsarr = []
for x in files:
    resultlist = []
    if not x['IsDir']:
        resultlist.append(concat(x['Path'].split('/')[1:],'/'))
        resultlist.append(x['ID'])
        resultsarr.append(resultlist)
print(resultsarr)

outfile = open('dictionary.txt', 'w')
for y in resultsarr:
    outfile.write(y[0] + '\t' + y[1] + '\n')

outfile.close()
