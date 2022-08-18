#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# Generates a single file with one word in each line from all ctm files in a directory.
# Words are "cleaned" following v2 protocol in word_filter_protocol.py
'''

from sys import argv, exit
if len(argv) != 3:
    print(argv[0] + "  Please, specify 2 args: ctm input folder path and lexicon output folder path")
    # python3 extractCtmWords.py ctm_files output_lexicon_folder
    # python3 extractCtmWords.py /vol/tensusers4/ctejedor/lanewcristianmachine/opt/kaldi/egs/kaldi_egs_CGN/s5/homed/test /vol/tensusers4/ctejedor/lanewcristianmachine/opt/kaldi/egs/kaldi_egs_CGN/s5/homed/outputlexicon
    exit(2)
[INPUT_CTM_PATH, OUTPUT_LEXICON_FOLDER_PATH] = argv[1:3]

import os
output_lexicon='extracted_words.txt'
os.makedirs(OUTPUT_LEXICON_FOLDER_PATH, exist_ok=True)
absolute_output_path=os.path.join(OUTPUT_LEXICON_FOLDER_PATH,output_lexicon)
#print(INPUT_CTM_PATH, OUTPUT_LEXICON_FOLDER_PATH)
ctm_files = [f for f in os.listdir(INPUT_CTM_PATH) if f.endswith('.ctm')]
#print(ctm_files)
all_words = set([])
from word_filter_protocol import v2
for file in ctm_files:    
    with open(os.path.join(INPUT_CTM_PATH,file),'r', encoding='utf-8') as f:    
        aux_line = []
        for line in f.readlines():
            fields = line.split()
            all_words.add(v2(fields[4]))

print('->',len(all_words), 'unique words extracted from', len(ctm_files), 'files.\nPath:',absolute_output_path)

with open(absolute_output_path,'w', encoding='utf-8') as f:
    f.write('\n'.join(all_words))


