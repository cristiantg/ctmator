#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# Encodes a text file (repeated words are encoded with the same key)
'''

import sys
if len(sys.argv) != 4:
    print(sys.argv[0] + "  Please, specify (3 args): corpus, reduced and dict  ")
    # python3 shorten_text $myProject/sentences.txt $myProject/corpus-reduced.txt $myProject/corpus_dict-reduced.txt
    sys.exit(2)
[PATH, OUTPUT_FILEPATH, OUTPUT_DICT_FILEPATH] = sys.argv[1:4]


TEXT_SEPARATOR = ' '
MAX_CHAR = 0
WORD_PREFFIX = "###---"


# 1. Read source (list of sublists)
original_text = []
with open(PATH, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.replace('\n','')
        fields = line.split(TEXT_SEPARATOR)
        original_text.append(fields)

# 2. Convert source
new_dict = {}
original_words = {}
final_text = []
global_counter = 0
for m_list in original_text:
    _list = []
    for m_text in m_list:
        processed_word = m_text
        if len(m_text) > MAX_CHAR:
            processed_word = ''
            if m_text in original_words:
                processed_word = original_words[m_text]
            else:
                processed_word = WORD_PREFFIX + str(global_counter)
                new_dict[processed_word] = m_text
                original_words[m_text] = processed_word
                global_counter = global_counter + 1
        _list.append(processed_word)
    final_text.append(_list)

# 3. Save output file
with open(OUTPUT_FILEPATH, 'w', encoding='utf-8') as f: 
    print('\t--> New file:', OUTPUT_FILEPATH)
    for line in final_text:
        f.write(TEXT_SEPARATOR.join(line) + '\n')

# 4. Save output dict file
with open(OUTPUT_DICT_FILEPATH, 'w', encoding='utf-8') as f: 
    print('\t--> New file:', OUTPUT_DICT_FILEPATH)
    for i in new_dict:
        f.write(i + TEXT_SEPARATOR + new_dict[i] + '\n')
    print('\t', len(new_dict),'words length > ', MAX_CHAR)