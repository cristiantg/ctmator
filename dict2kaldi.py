#!/usr/bin/python3
# -*- coding: utf-8 -*- 

'''
# Kaldi dict folder preparation from a text source file (TEXT_FILE).
# The lexicon can be obtained from two sources (A or B):
#
# A. A local lexicon file (word<space>phones separated by spaces)
# Be careful: the preference is the Local lexicon file. So,
# if you specify it as an input parameter and the file exists, 
# the G2P option will be discarded although you have also specified
# the G2P values as input arguments.
#
# B. A G2P/WS tool
# Dependencies (only necessary if you do not provide a local lexicon file):
# 1. https://github.com/cristiantg/lexiconator
# 2. LaMachine environment
# 3. Credentials of: https://webservices.cls.ru.nl/ (G2P tool)
'''

import os, sys, shutil
from pathlib import Path
NUM_ARGS = 7
if len(sys.argv) != NUM_ARGS:
    print(sys.argv[0] + "  Please, specify " + str(NUM_ARGS-1) + " args: (1) OUTPUT_FOLDER, (2) TEXT_FOLDER, (3) LEXICONATOR PATH, (4) G2P_USER, (5) G2P_PWD, (6) LOCAL LEXICON FILE")
    # python3 speech2kaldi.py $myProject/homed_kaldi/dict $KALDIdir/homed_kaldi/data path_lexiconator USER PWD fake-path
    sys.exit(2)
[OUTPUT_FOLDER, TEXT_FOLDER, LEXICONATOR, USER_WS, PWD_WS, LOCAL_LEXICON] = sys.argv[1:NUM_ARGS]

shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
AUX_DICT_FOLDER = os.path.join(OUTPUT_FOLDER,'aux-text')
shutil.rmtree(AUX_DICT_FOLDER, ignore_errors=True)
Path(AUX_DICT_FOLDER).mkdir(parents=True, exist_ok=True)
TEXT_FILE='textForLM'
TEXT_FILE_PATH=os.path.join(AUX_DICT_FOLDER,TEXT_FILE)
shutil.copy(os.path.join(TEXT_FOLDER,TEXT_FILE), TEXT_FILE_PATH)
m_encoding='utf-8'
print('++ dict2kaldi.py ++')
print('- OUTPUT_FOLDER:',OUTPUT_FOLDER)
WORDLISTFILE = os.path.join(OUTPUT_FOLDER,"wordlist")
SIL_PHONES = ['sil', 'spn']
OPTIONAL_SIL_PHONES = ['sil']
NONSILENCEPHONESFILE = os.path.join(OUTPUT_FOLDER,'nonsilence_phones.txt')
OPTIONALSILPHONESFILE = os.path.join(OUTPUT_FOLDER,'optional_silence.txt')
SILPHONESFILE = os.path.join(OUTPUT_FOLDER,'silence_phones.txt')
LEXICONFILE = os.path.join(OUTPUT_FOLDER,'lexicon.txt')
SEP = '\t'

# A. Lexicon
# A.1 Local lexicon file
if os.path.isfile(LOCAL_LEXICON):
    words_source_lex =  {}
    with open(LOCAL_LEXICON, 'r', encoding=m_encoding) as l1:
        for line in l1.readlines():
            line = line.replace('\n','')
            (ortho, trans) = line.split(SEP)
            words_source_lex[ortho] = trans

    words_text_file = set()
    with open(TEXT_FILE_PATH, 'r', encoding=m_encoding) as tf:
        for line in tf.readlines():
            words_text_file.update(line.replace('\n','').split())
    words_text_file = sorted(words_text_file)

    # wordlist file
    lexicon_words = []
    with open(WORDLISTFILE, 'w', encoding=m_encoding) as wf:
        for word in words_text_file:
            if word in words_source_lex:
                lexicon_words.append(word)
                wf.write(word+'\n')
            else:
                print('** Warning: Word not found in local lexicon ->', word)
    
    # lexicon file
    with open(LEXICONFILE, 'w', encoding=m_encoding) as lf:
        for word in lexicon_words:
            lf.write(word+SEP+words_source_lex[word]+'\n')    

# A.2 GP2 tool: lexicon.txt, log.txt, mapping.txt
else:    
    os.system('python3 '+ os.path.join(LEXICONATOR,'utils', 'preparing_raw_data.py')+ ' '+AUX_DICT_FOLDER+' '+OUTPUT_FOLDER)
    os.system('python3 '+ os.path.join(LEXICONATOR,'uber_script.py')+ ' '+USER_WS+' '+PWD_WS+' '+LEXICONATOR+' 1 1 "<unk><TAB>spn" '+ WORDLISTFILE +' '+OUTPUT_FOLDER)
    shutil.rmtree(AUX_DICT_FOLDER, ignore_errors=True)
    shutil.copy(os.path.join(OUTPUT_FOLDER,'results-final','lexicon.txt'),LEXICONFILE)




# B. nonsilence_phones.txt <> lexicon
set_phones = set()
with open(LEXICONFILE, "r", encoding=m_encoding) as f:
    for line in f:
        phones = line.replace("\n", "").split("\t")[1].split(" ")
        for phone in phones:
            #"unk" must be always included the file:
            if len(phone)>0: # to avoid phone:''
                set_phones.add(phone)


set_phones = sorted(set_phones, key=lambda v: (v.upper(), v[0].islower()))
#print(len(set_phones), " ".join(set_phones))
with open(NONSILENCEPHONESFILE, "w", encoding=m_encoding) as f:
    for phone in set_phones:
        if phone not in SIL_PHONES:
            f.write(phone+"\n")
print("Created generic "+NONSILENCEPHONESFILE+" file")

# C. 
with open(SILPHONESFILE, "w", encoding=m_encoding) as f:
    for phone in SIL_PHONES:
        f.write(phone+"\n")
print("Created generic "+SILPHONESFILE+" file")

# D.
with open(OPTIONALSILPHONESFILE, "w", encoding=m_encoding) as f:
    for phone in OPTIONAL_SIL_PHONES:
        f.write(phone+"\n")
print("Created generic "+OPTIONALSILPHONESFILE+" file")