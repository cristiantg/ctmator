#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# Kaldi data folder preparation from ctm and wav source files
# (files with a no valid ctm/wav pair will be discarded).
# It takes into account the suffixes of the filenames for the ID generation.
# Output: spk2utt, text, textForLM, utt2spk and wav.scp Kaldi files.
# Let op: words conatining xxx will be always <unk> xxx-dog, dog-xxx: xxx
#├── spk2utt
#	 fn000048 fn000048_1_001 fn000048_1_002 fn000048_1_003
#	 fn000049 fn000049_1_001 fn000049_1_002 fn000049_1_003 
#├── text
#	 fn000048_1_001 naar een zwemparadijs
#	 fn000048_1_002 een mooie glijbaan
#├── textForLM
#	 naar een zwemparadijs
#	 een mooie glijbaan
#├── utt2spk
#	 fn000048_1_001 fn000048
#	 fn000048_1_002 fn000048			
#└── wav.scp
#	 fn000048_1_001 .../wav_files_to_use_train/fn000048_1_001.wav
#	 fn000048_1_002 .../wav_files_to_use_train/fn000048_1_001.wav
'''

import os, glob, sys
from pathlib import Path
if len(sys.argv) != 5:
    print(sys.argv[0] + "  Please, specify 4 args: (1) OUTPUT_FOLDER, (2) AUDIO_FOLDER, (3) CTM_FOLDER and (4) the lexiconator path")
    # python3 speech2kaldi_suffixes.py $myProject/homed_kaldi $KALDIdir/homed_testset $KALDIdir/homed_ctm $lexiconatorPath
    sys.exit(2)
[OUTPUT_FOLDER, AUDIO_FOLDER, CTM_FOLDER, LEXICONATOR] = sys.argv[1:5]
Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)


##########################################
print('   - OUTPUT_FOLDER:',OUTPUT_FOLDER)
UNK_SYMBOL = '<unk>'
extension='.wav'
extension_transcription='.ctm'
m_encoding='utf-8'
# spk2utt
file_names = {}
file_names_no_ext = []
names_segments = {}
names_paths = {}
wav_dir=glob.glob(os.path.join(AUDIO_FOLDER, '*'+extension))
ctm_dir=glob.glob(os.path.join(CTM_FOLDER, '*'+extension_transcription))
ctm_ids=set()
for abs_path in ctm_dir:
    ctm_ids.add(os.path.basename(abs_path).replace(extension_transcription,''))
print('\t->', len(wav_dir), '/',  len(ctm_ids), extension, '/', extension_transcription, "files to be prepared")

with open(os.path.join(OUTPUT_FOLDER,'spk2utt'), 'w', encoding=m_encoding) as f: 
    print('\t--> spk2utt')
    #files = os.listdir(AUDIO_FOLDER)
    for filename in wav_dir:
        shortname = os.path.basename(filename)
        aux_shortname_id = shortname[0:shortname.find('.wav')]
        if aux_shortname_id in ctm_ids:
            file_names[shortname]=(filename,aux_shortname_id)
    
    file_names=dict(sorted(file_names.items()))
    #print(file_names)
    #Key'Medicijnjournaal_februari_2019_1-81.wav':
    #Value[0] ('/vol/tensusers4/ctejedor/lanewcristianmachine/opt/kaldi/egs/kaldi_egs_CGN/s5/homed/audio_split/Medicijnjournaal_februari_2019_1-81.wav',
    #Value[1] 'Medicijnjournaal_februari_2019_1-81'),

    # Second part, grouping
    groups = {}
    for file in file_names:
        no_ext_aux = file_names[file][1]
        key = no_ext_aux[:no_ext_aux.rindex('-')]
        #print(key)
        info_aux = (file, file_names[file][0])
        if key in groups:
            groups[key].append(info_aux)
        else:
            groups[key] = [info_aux]
    #print(groups)

    # Third part, writing
    for group in groups:
        subkeys = []
        for subkey in groups[group]:
            subkeys.append(subkey[0].replace(extension,''))
        f.write(group+' '+' '.join(subkeys) + '\n')

#Run this command on a valid path:
######utils/spk2utt_to_utt2spk.pl OUTPUT_FOLDER/spk2utt > OUTPUT_FOLDER/utt2spk


# wavscp.scp, text and textForLm
from word_filter_protocol import v2
sys.path.append(LEXICONATOR)
import local.word_clean as wc
import re
with open(os.path.join(OUTPUT_FOLDER,'wav.scp'), 'w', encoding=m_encoding) as f, open(os.path.join(OUTPUT_FOLDER,'text'), 'w', encoding=m_encoding) as text_f, open(os.path.join(OUTPUT_FOLDER,'textForLM'), 'w', encoding=m_encoding) as textForLM_f:
    print('\t--> wav.scp')
    print('\t--> text')
    print('\t--> textForLm')
    file_names=dict(sorted(file_names.items()))
    for i in sorted (file_names):
        #f.write(file_names[i][1] +' sox '+file_names[i][0]  +' -r 16k -e signed-integer -t wav - remix - |\n')
        f.write(file_names[i][1] + ' ' +file_names[i][0] + '\n')
        aux_name_id = file_names[i][1]
        
        with open(os.path.join(CTM_FOLDER,aux_name_id+'.ctm'), 'r', encoding=m_encoding) as ctm_aux:
            aux_line = []
            for line in ctm_aux.readlines():
                fields = line.split()
                # Clean 1: v2
                # Clean 2: lexiconator
                m_text = v2(fields[4])
                if 'xxx' in m_text:
                    m_text = 'xxx'
                aux_line.append(wc.remove_begin_end(wc.normalize_text(wc.clean_word(wc.clean_text(m_text), UNK_SYMBOL), True), 1))
            normal_line=re.sub(' +', ' ',' '.join(aux_line).strip())
            text_f.write(aux_name_id + ' ' + normal_line  + '\n')
            textForLM_f.write(normal_line + '\n')