#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# Calculates the WER and SER of x ctm files inside a folder.
# The ref folder must contain the same number of files as the
# hyp folder. These files must contain one unique line.
'''

from sys import argv, exit
ARGS_PLUS_1 = 5
if len(argv) != ARGS_PLUS_1:
    print(argv[0] + "  Please, specify " +str(ARGS_PLUS_1-1)+" args: hyp folder path (ctm files), ground-truth folder path (1-line files), output folder path, and a suffix for the output files")
    # python3 wer_ser.py run01_ao prompt_folder test _mt
    # Ouput: hyp_mt.txt and ref_mt.txt and SCLITE files
    exit(2)
[HYP_PATH, GROUND_TRUTH_PATH, OUTPUT_FOLDER, PREFFIX] = argv[1:ARGS_PLUS_1]

REF_FILE='ref'
HYP_FILE='hyp'
import os
REF_FILE_PATH=os.path.join(OUTPUT_FOLDER, REF_FILE+PREFFIX)
HYP_FILE_PATH=os.path.join(OUTPUT_FOLDER, HYP_FILE+PREFFIX)

print("###1. Load HYP_PATH, GROUND_TRUTH_PATH")
ref = {}
hyp = {}
for file in os.listdir(GROUND_TRUTH_PATH):
    m_id = os.path.splitext(file)[0]
    aux_path = os.path.join(HYP_PATH,m_id+'.ctm')
    # 1. Load all hyp files
    if not os.path.isfile(aux_path):
        print("Warning: ",m_id,"does not exist in", aux_path)
    else:
        with open(aux_path,'r') as f:
            file_ctm = f.readlines()
            sentence = ''
            for line in file_ctm:
                sentence+=' '+line.split()[-2]
        hyp[m_id] = sentence.strip()     
    # 2. Load all ref files
    with open(os.path.join(GROUND_TRUTH_PATH, file),'r') as f:
        file_ctm = f.readlines()
        sentence = ''
        for line in file_ctm:
            sentence+=' '+line
        ref[m_id] = sentence.strip()  

print("hyp",len(hyp))
print("ref",len(ref))


print("###2. Create new files")
with open(REF_FILE_PATH,'w') as f:
    for elem in ref:
        f.write(ref[elem]+' ('+elem+')\n')

with open(HYP_FILE_PATH,'w') as f:
    for elem in hyp:
        f.write(hyp[elem]+' ('+elem+')\n')


print("###3. WER SCLITE")
os.system('$KALDI_ROOT/tools/sctk/bin/sclite -s -i rm -r '+REF_FILE_PATH+' -h '+HYP_FILE_PATH+' -o all dtl')

print("###4. SER MANUAL")
count=0
for elem in ref:
    if hyp[elem]==ref[elem]:
        count+=1
print(PREFFIX,'correct sentences',str(count),'out of',len(ref),str(round((len(ref)-count)/len(ref)*100.00,1))+'% SER')
print()