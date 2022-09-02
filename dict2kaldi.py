#!/usr/bin/python3
# -*- coding: utf-8 -*- 

'''
# Kaldi dict folder preparation from a text source file.
# Dependencies:
# 1. https://github.com/cristiantg/lexiconator
# 2. LaMachine environment
# 3. Credentials of: https://webservices.cls.ru.nl/ (G2P tool)
'''

import os, sys, shutil
from pathlib import Path
if len(sys.argv) != 6:
    print(sys.argv[0] + "  Please, specify 5 args: (1) OUTPUT_FOLDER, (2) TEXT_FOLDER, (3) LEXICONATOR PATH, (4) G2P_USER, (5) G2P_PWD")
    # python3 speech2kaldi.py $myProject/homed_kaldi/dict $KALDIdir/homed_kaldi/data path_lexiconator USER PWD
    sys.exit(2)
[OUTPUT_FOLDER, TEXT_FOLDER, LEXICONATOR, USER_WS, PWD_WS] = sys.argv[1:6]
shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
AUX_DICT_FOLDER = os.path.join(OUTPUT_FOLDER,'aux-text')
shutil.rmtree(AUX_DICT_FOLDER, ignore_errors=True)
Path(AUX_DICT_FOLDER).mkdir(parents=True, exist_ok=True)
shutil.copy(os.path.join(TEXT_FOLDER,'textForLM'), os.path.join(AUX_DICT_FOLDER,'textForLM'))
m_encoding='utf-8'

##########################################
print('++ dict2kaldi.py ++')
print('- OUTPUT_FOLDER:',OUTPUT_FOLDER)
WORDLISTFILE = os.path.join(OUTPUT_FOLDER,"wordlist")
SIL_PHONES = ['sil', 'spn']
OPTIONAL_SIL_PHONES = ['sil']
NONSILENCEPHONESFILE = os.path.join(OUTPUT_FOLDER,'nonsilence_phones.txt')
OPTIONALSILPHONESFILE = os.path.join(OUTPUT_FOLDER,'optional_silence.txt')
SILPHONESFILE = os.path.join(OUTPUT_FOLDER,'silence_phones.txt')
LEXICONFILE = os.path.join(OUTPUT_FOLDER,'lexicon.txt')

# A. Basic files: lexicon.txt, log.txt, mapping.txt
os.system('python3 '+ os.path.join(LEXICONATOR,'utils', 'preparing_raw_data.py')+ ' '+AUX_DICT_FOLDER+' '+OUTPUT_FOLDER)
os.system('python3 '+ os.path.join(LEXICONATOR,'uber_script.py')+ ' '+USER_WS+' '+PWD_WS+' '+LEXICONATOR+' 1 1 "<unk><TAB>spn" '+ os.path.join(OUTPUT_FOLDER,'wordlist')+' '+OUTPUT_FOLDER)
shutil.rmtree(AUX_DICT_FOLDER, ignore_errors=True)
shutil.copy(os.path.join(OUTPUT_FOLDER,'results-final','lexicon.txt'),LEXICONFILE)

# B. nonsilence_phones.txt <> lexicon
set_phones = set()
with open(LEXICONFILE, "r", encoding=m_encoding) as f:
    for line in f:
        phones = line.replace("\n", "").split("\t")[1].split(" ")
        for phone in phones:
            #"unk" must be always included the file:
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