#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# python3 ser.py hyp-filepath ref-filepath

# Computes the SER (sentence error rate of the pair hyp/ref from SCLITE format)
@since 2023/02/22
'''

import sys
if len(sys.argv) != 3:
    print(sys.argv[0] + "Please, specify 2 parameters: hyp-filepath ref-filepath")
    # python3 ser.py hyp.txt ref.txt
    sys.exit(2)
[HYP, REF] = sys.argv[1:3]

print("### Calculating SER...")
def read_file(sclite_file):
    lines_map = {}
    with open(sclite_file,'r') as f:
        for line in f:
            fields = line.strip().split(' ')
            lines_map[fields[-1]]=' '.join(fields[:-1])
    return lines_map


hyp = read_file(HYP)
ref = read_file(REF)


count=0
for elem in ref:
    if hyp[elem]==ref[elem]:
        count+=1
print('Correct sentences:',str(count),'out of',len(ref),' -> ',str(round((len(ref)-count)/len(ref)*100.00,1))+'% SER')
print()