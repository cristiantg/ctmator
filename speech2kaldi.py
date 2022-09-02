#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# Prepares three KALDI files: spk2utt, segments and wavscp from an audio folder
'''

import os, glob, sys
from pathlib import Path
if len(sys.argv) != 3:
    print(sys.argv[0] + "  Please, specify 2 args: (1) OUTPUT_FOLDER and (2) AUDIO_FOLDER")
    # python3 speech2kaldi.py $myProject/homed_kaldi $KALDIdir/homed_testset
    sys.exit(2)
[OUTPUT_FOLDER, AUDIO_FOLDER] = sys.argv[1:3]
Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)


##########################################
print('   - OUTPUT_FOLDER:',OUTPUT_FOLDER)
m_encoding='utf-8'
# spk2utt
file_names = {}
file_names_no_ext = []
names_segments = {}
names_paths = {}
with open(os.path.join(OUTPUT_FOLDER,'spk2utt'), 'w', encoding=m_encoding) as f: 
    print('\t--> spk2utt')
    #files = os.listdir(AUDIO_FOLDER)
    for filename in glob.glob(os.path.join(AUDIO_FOLDER, '*.wav')):
        shortname = os.path.basename(filename)
        file_names[shortname]=(filename,shortname[0:shortname.find('.wav')])
    
    file_names=dict(sorted(file_names.items()))
    for my_file in file_names:
        no_ext_name = file_names[my_file][1]
        names_segments[no_ext_name] = (no_ext_name,my_file)
        f.write(no_ext_name+' '+names_segments[no_ext_name][0] + '\n')

# segments 
def get_duration(file_path):
    duration = -1
    import wave
    import contextlib
    with contextlib.closing(wave.open(file_path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration

with open(os.path.join(OUTPUT_FOLDER,'segments'), 'w', encoding=m_encoding) as f: 
    print('\t--> segments')
    for i in sorted (names_segments):        
        duration = str(round(get_duration(file_names[names_segments[i][1]][0]),3))
        f.write(names_segments[i][0]+' '+i + ' 0.000 '+ duration + ' \n')

# wavscp.scp
with open(os.path.join(OUTPUT_FOLDER,'wav.scp'), 'w', encoding=m_encoding) as f: 
    print('\t--> wav.scp')
    file_names=dict(sorted(file_names.items()))
    for i in sorted (file_names):
        f.write(file_names[i][1] +' sox '+file_names[i][0]  +' -r 16k -e signed-integer -t wav - remix - |\n')