#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# Calculates the interagreeemnt beteween n transcribers.
# There must be x subfolders inside the root_folder (1subfolder=1speaker).
# In each subfolder there must be txt files (same file name for all speakers).
'''

from sys import argv, exit
if len(argv) != 3:
    print(argv[0] + "  Please, specify 2 args: root folder path and output file paths")
    # python3 interagreement.py root_folder my_out_file.txt
    exit(2)
[PATH, OUTPUT_FILEPATH] = argv[1:3]


from re import sub
from os import scandir
from os.path import basename
from glob import glob
from statistics import mean

KEY_SEPARATOR = ' <--> '
REPLACE_SYMBOLS = {'.':'', '?':'', 'SIL':'', ',':'', '=':'-', "’":"'"} #+lowercase
REPLACE_WORDS = {'xxx':'<unk>'}
'''
Lowercase word with symbols replaced.
Also deletes any - at the beg/end of the word
'''
def clean_word(m_word):
    for symbol in REPLACE_SYMBOLS:
        m_word = m_word.replace(symbol, REPLACE_SYMBOLS[symbol])
    if m_word.startswith('-'):
        m_word= m_word[1:]
    if m_word.endswith('-'):
        m_word = m_word[:m_word.rindex('-')]
    if m_word in REPLACE_WORDS:
        m_word = REPLACE_WORDS[m_word]
    ## New protocol:
    if '*' in m_word:
        m_word = m_word[m_word.index('*'):]
    if '[' in m_word:
        m_word = m_word[m_word.index('['):]
    return m_word.lower()


def remove_accents(raw_text):
    """Removes common accent characters.
    Our goal is to brute force login mechanisms, and I work primary with
    companies deploying Engligh-language systems. From my experience, user
    accounts tend to be created without special accented characters. This
    function tries to swap those out for standard Engligh alphabet.
    """
    raw_text = sub(u"[àáâãäå]", 'a', raw_text)
    raw_text = sub(u"[èéêë]", 'e', raw_text)
    raw_text = sub(u"[ìíîï]", 'i', raw_text)
    raw_text = sub(u"[òóôõö]", 'o', raw_text)
    raw_text = sub(u"[ùúûü]", 'u', raw_text)
    raw_text = sub(u"[ýÿ]", 'y', raw_text)
    raw_text = sub(u"[ß]", 'ss', raw_text)
    raw_text = sub(u"[ñ]", 'n', raw_text)
    return raw_text 

# 1. Read files
subfolders = zip([ f.path for f in scandir(PATH) if f.is_dir() ],[ f.name for f in scandir(PATH) if f.is_dir() ])
data_frame = {}
for speaker in subfolders:
    m_path = speaker[0]
    m_speaker = speaker[1]
    txt_files = glob(m_path+'/*.txt')
    all_speaker = {}
    for txt_file in txt_files:        
        segments = []
        all_speaker[basename(txt_file)] = segments
        with open(txt_file, 'r', encoding='utf-8') as f:
            segment_aux = []
            for line in f:
                line = line.replace('\n','')
                if '[EndTime:' in line:
                    segments.append(segment_aux)
                    segment_aux = []
                elif ('[StartTime:' not in line) and ('[Speaker:' not in line):
                    for word in line.split():
                        word = remove_accents(clean_word(word))
                        if len(word)>0:
                            segment_aux.append(word)
    data_frame[m_speaker] = all_speaker


# 2. Save stats
with open(OUTPUT_FILEPATH, 'w', encoding='utf-8') as w:
    
    print('\n--> Stats & Inter-agreement output file:', OUTPUT_FILEPATH)

    # T0
	#T0_1.txt
	#	T1_1.txt
	#	T2_1.txt
	#	T3_1.txt
	#T1_1
    #...
    comparisons = {}
    words_remaining = {}
    problems = {}
    for speaker in data_frame:        
        for m_file in data_frame[speaker]:
            current_segments = data_frame[speaker][m_file]
            for aux_speaker in data_frame:
                if aux_speaker!=speaker:
                    key_speakers = speaker+KEY_SEPARATOR+aux_speaker
                    #print(key_speakers, m_file)
                    aux_current_segments = data_frame[aux_speaker][m_file]
                    if (len(current_segments))!=len(aux_current_segments):
                        problems[key_speakers]=str(len(current_segments))+' != ' + str(len(aux_current_segments))
                    else:
                        if key_speakers not in comparisons:                            
                            comparisons[key_speakers]={}
                        
                        included = []
                        total_words_checked = 0                                   
                        for aux_counter in range(len(current_segments)):
                            current_segment = current_segments[aux_counter]
                            aux_current_segment = aux_current_segments[aux_counter]
                            removable_aux_current_segment = aux_current_segment[:]                            
                            for m_word in current_segment:
                                total_words_checked += 1
                                if m_word in removable_aux_current_segment:
                                    included.append(m_word)
                                    removable_aux_current_segment.remove(m_word)  

                            if len(removable_aux_current_segment)>0:
                                if key_speakers not in words_remaining:
                                    words_remaining[key_speakers]={}
                                if m_file not in words_remaining[key_speakers]:
                                    words_remaining[key_speakers][m_file] = removable_aux_current_segment[:]
                                else:
                                    words_remaining[key_speakers][m_file].extend(removable_aux_current_segment[:])

                        #print(key_speakers, m_file, len(included),total_words_checked)
                        comparisons[key_speakers][m_file]=float(len(included)/total_words_checked)
    final_to_string = ''                       
    keys_pairs = {}
    accum_agreement = {}
    m_count = 0
    for speakers_key in comparisons:
        m_count+=1
        to_string = ''
        inter_acc = 0
        for m_file in comparisons[speakers_key]:
            current_inter = comparisons[speakers_key][m_file]
            inter_acc +=comparisons[speakers_key][m_file]
            to_string+=' -> '+m_file +' '+ str(round(current_inter*100.0,2))+'%\n'
        acc_value = round(100.0*inter_acc/len(comparisons[speakers_key]),2)
        keys_pairs[speakers_key] = acc_value
        first_speaker = speakers_key.split(KEY_SEPARATOR)[0]
        if first_speaker not in accum_agreement:
            accum_agreement[first_speaker]=[acc_value]
        else:
            accum_agreement[first_speaker].append(acc_value)
        final_to_string+='\n'+str(m_count)+': '+speakers_key+' '+str(keys_pairs[speakers_key])+'%\n'+to_string
            
    final_inter = 0
    t_string=''
    for speaker in accum_agreement:       
        c_value =  round(mean(accum_agreement[speaker]),2)
        final_inter+=c_value
        t_string+='-> '+speaker+' '+str(c_value)+'% '+str(accum_agreement[speaker])+'\n'
    w.write('Inter-agreement: '+str(round(final_inter/len(accum_agreement),2))+'%\n'+t_string)
    w.write('\n\nComparisons (first speaker is the golden reference): '+str(len(comparisons))+final_to_string)

    
    w.write('\n\nProblems (not the same number of segments): '+str(len(problems)))
    for problem in problems:
        w.write(problem + ': '+ str(problems[problem]))

   
    m_string = ''
    acc_problems = 0
    n_files = 0
    acc_words = []
    from collections import Counter
    for speakers_key in words_remaining:
        for m_file in words_remaining[speakers_key]:
            n_files+=1
            current_problems = len(words_remaining[speakers_key][m_file])
            acc_problems+=current_problems
            m_string+=' -> ' +speakers_key + ': ' + m_file  + ': ' +  str(current_problems)  + ': ' + ', '.join(words_remaining[speakers_key][m_file]) + '\n'
            acc_words.extend(words_remaining[speakers_key][m_file])
    w.write('\n\nRemaining words (problematic words): '+str(acc_problems)+', average per file: '+str(round(acc_problems/n_files,3))+'\n')
    w.write(' -> '+str(Counter(acc_words))+'\n\n')
    w.write(m_string)
    

    w.write('\n\nSTATS:\n')
    for speaker in data_frame:
        w.write(speaker+ ' -> Files: '+ str(len(data_frame[speaker])) + '\n')
        for m_file in data_frame[speaker]:
            file_name = basename(m_file)
            w.write('-> ' + file_name + ' -> ' + str(len(data_frame[speaker][m_file])) + ' segments\n-> Words: ')
            m_count = 0
            for l in data_frame[speaker][m_file]:
                m_count+=len(l)
                w.write(str(len(l))+' ')
            w.write('\n -> Words (total): '+str(m_count)+'\n')
        w.write('\n')