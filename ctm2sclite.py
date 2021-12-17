#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# Tranforms ctm files into sclite format
# How to execute this script when printing all commented #####symbols lines:
# PYTHONIOENCODING=utf-8 python3 ctm2sclite.py
'''

import os, re, sys

if len(sys.argv) != 5:
    print(sys.argv[0] + "  Please, specify 4 args: (1) PATH_REF_FOLDER, (2) PATH_HYP_FILE, (3) PATH_SENTENCES_INPUT, (4) PATH_SCLITE_OUTPUT")
    # python3 ctm2sclite.py $KALDIdir/ctmator/ctm_test  $KALDIdir/ctmator/hyp  $KALDIdir/ctmator/ctm_train $KALDIdir/ctmator/sclite_output
    sys.exit(2)
[PATH_REF_FOLDER, PATH_HYP_FILE, PATH_SENTENCES_INPUT, PATH_SCLITE_OUTPUT] = sys.argv[1:5]

# Be careful, if you want map down digits you need the map_digits_to_words_v2.perl file
# Not included in this repo. due to copyright issues.
DIGITS_TO_WORDS_FILE_PATH = '/home/ctejedor/python-scripts/lexiconator/local/map_digits_to_words_v2.perl'
REF_FILE_NAME_SCLITE_OUTPUT = 'ref.txt'
CORPUS_FILE_NAME_SCLITE_OUTPUT = 'sentences.txt'
HYP_FILE_NAME_SCLITE_OUTPUT = 'hyp.txt'
EXTENSION_TO_EXTRACT = '.ctm'
REPLACE_SYMBOLS = {'.':'', '?':'', 'SIL':'', ',':'', '=':'-', "’":"'"} #+lowercase, xxx
DELETE_ONLY_BEGIN_END = ["-", "\'"]
REPLACE_SCLITE_SYMBOLS = {'(':'_', ')':'_', '-':'_', ' ':'_', '\t':'_'}
REPLACE_WORDS = {}
TEMPORAL_FILE = "tmp"

def map_digits(digits):
    m_text = digits    
    if os.path.isfile(DIGITS_TO_WORDS_FILE_PATH):
        os.system(("echo \"" + m_text + "\"| perl " +
                  DIGITS_TO_WORDS_FILE_PATH + " > "+TEMPORAL_FILE))
        m_text = str(open(TEMPORAL_FILE, 'r').read()).replace('\n', '')
    return m_text

'''
Lowercase word with symbols replaced.
Also deletes any - at the beg/end of the word
'''
def clean_word(m_word):
    for symbol in REPLACE_SYMBOLS:
        m_word = m_word.replace(symbol, REPLACE_SYMBOLS[symbol])
    for m_symbol in DELETE_ONLY_BEGIN_END:
        if m_word.startswith(m_symbol):
            m_word= m_word[1:] 
        if m_word.endswith(m_symbol):
            m_word = m_word[:m_word.rindex(m_symbol)]
    if m_word in REPLACE_WORDS:
        m_word = REPLACE_WORDS[m_word]
    return m_word.lower()


def remove_accents(raw_text):
    """Removes common accent characters.
    Our goal is to brute force login mechanisms, and I work primary with
    companies deploying Engligh-language systems. From my experience, user
    accounts tend to be created without special accented characters. This
    function tries to swap those out for standard Engligh alphabet.
    """
    raw_text = re.sub(u"[àáâãäå]", 'a', raw_text)
    raw_text = re.sub(u"[èéêë]", 'e', raw_text)
    raw_text = re.sub(u"[ìíîï]", 'i', raw_text)
    raw_text = re.sub(u"[òóôõö]", 'o', raw_text)
    raw_text = re.sub(u"[ùúûü]", 'u', raw_text)
    raw_text = re.sub(u"[ýÿ]", 'y', raw_text)
    raw_text = re.sub(u"[ß]", 'ss', raw_text)
    raw_text = re.sub(u"[ñ]", 'n', raw_text)
    return raw_text 

def get_words(m_path):
    m_map = {}
    if os.path.exists(m_path):
        only_files = [f for f in os.listdir(m_path) if os.path.isfile(os.path.join(m_path, f))]
        for m_file in only_files:
            current_file = m_path+os.sep+m_file            
            if current_file.endswith(EXTENSION_TO_EXTRACT):
                with open(current_file, 'r', encoding='utf-8') as f:  
                    for line in f.readlines():
                        fields = line.split()
                        id_aux = fields[0]
                        word_aux = fields[4]
                        word_aux = remove_accents(clean_word(word_aux))
                        if len(word_aux)>0:
                            # Be careful, we normalize digits with a perl file:
                            if word_aux.isdigit():
                                word_aux = map_digits(word_aux)
                            if id_aux not in m_map:
                                m_map[id_aux] = []                        
                            m_map[id_aux].append(word_aux)

    return m_map


def print_map2sclite(m_map, output_folder, file_name_output, post_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)    
    with open(output_folder+os.sep+file_name_output, 'w',encoding='utf-8') as f:
        for i in m_map:
            #####symbols = set([])
            new_i = i
            for symbol in REPLACE_SCLITE_SYMBOLS:
                new_i = new_i.replace(symbol, REPLACE_SCLITE_SYMBOLS[symbol])
            post_text = ''
            if post_name:
                post_text = ' ('+str(new_i)+'-1)'
            f.write(' '.join(m_map[i]) + post_text)
            #####for m_word in m_map[i]:
                #####for m_sym in m_word:                
                    #####symbols.add(m_sym)
            #####symbols = sorted(symbols)
            #####print('\t',new_i, len(symbols), ' '.join(symbols))
            #print(new_i, len(symbols), ' '.join(symbols))
            # Mandatory for sclite (line break at the end of the utt/file)
            f.write('\n')
    print("\t-->File generated: ", output_folder+os.sep+file_name_output)
    return None


'''
Extracts all possible sentences from a ctm which includes . and capital letters
'''
def ctm2Sentences():
    m_map = {}
    if os.path.exists(m_path):
        only_files = [f for f in os.listdir(m_path) if os.path.isfile(os.path.join(m_path, f))]
        for m_file in only_files:
            current_file = m_path+os.sep+m_file            
            if current_file.endswith(EXTENSION_TO_EXTRACT):
                with open(current_file, 'r', encoding='utf-8') as f:  
                    for line in f.readlines():
                        fields = line.split()
                        id_aux = fields[0]
                        word_aux = fields[4]
                        word_aux = remove_accents(clean_word(word_aux))
                        if len(word_aux)>0:
                            # Be careful, we normalize digits with a perl file:
                            if word_aux.isdigit():
                                word_aux = map_digits(word_aux)
                            if id_aux not in m_map:
                                m_map[id_aux] = []                        
                            m_map[id_aux].append(word_aux)

    return m_map

# 1. N ctm ref. files -> 1 sclite file
print_map2sclite(get_words(PATH_REF_FOLDER), PATH_SCLITE_OUTPUT, REF_FILE_NAME_SCLITE_OUTPUT, True)

# 2. N ctm sentences (without IDs) files -> file
print_map2sclite(get_words(PATH_SENTENCES_INPUT), PATH_SCLITE_OUTPUT, CORPUS_FILE_NAME_SCLITE_OUTPUT, False)
# 

# 3. N ctm hyp. files -> 1 sclite file
print_map2sclite(get_words(PATH_HYP_FILE), PATH_SCLITE_OUTPUT, HYP_FILE_NAME_SCLITE_OUTPUT, True)

# 4. sclite command
# /vol/customopt/lamachine.stable/opt/kaldi/tools/sctk-2.4.10/bin/sclite -s -i rm -r ref.txt -h hyp.txt -o all dtl -n "homed_XXX"

if os.path.isfile(TEMPORAL_FILE):
    os.remove(TEMPORAL_FILE)