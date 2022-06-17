#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# Splits one audio file into several audio files.
# Splits the ctm related to the audio file into several ctm files.
# The condition for splitting is set by a custom string included in the ctm.
'''

import sys, os
NUM_PARAMS=6 #number of parameters + 1
if len(sys.argv) != NUM_PARAMS:
    print(sys.argv[0] + "  Please, specify",str(NUM_PARAMS-1),"args: (1) ABSOLUTE_PATH_AUDIO_FILE, (2) ABSOLUTE_PATH_CTM_FILE, (3) SPLIT_PATTERN_STRING, (4) AUDIO_FOLDER_OUTPUT, (5) CTM_FOLDER_OUTPUT")
    # python3 splitaudioctm.py /vol/tensusers4/ctejedor/lanewcristianmachine/opt/kaldi_nl/homed_wav/Medicijnjournaal_2016_1.wav /vol/tensusers4/ctejedor/lanewcristianmachine/opt/kaldi_nl/ctmator/ref_original/Medicijnjournaal_2016_1.ctm . /home/ctejedor/python-scripts/homed_scripts/audio_split /home/ctejedor/python-scripts/homed_scripts/ctm_split
    # Explanation of the parameters    
    #### (1) ABSOLUTE_PATH_AUDIO_FILE: Absolute path to the audio file to be splitted.
    #### (2) ABSOLUTE_PATH_CTM_FILE: Absolute path to the ctm file to be splitted.
    #### (3) SPLIT_PATTERN_STRING: String that will be the separator between audio/ctm files. This string must be found in the penultimate column of the ctm file.
    #### (4) AUDIO_FOLDER_OUTPUT: Absolute path in which all audio files will be generated after splitting the original one.
    #### (5) CTM_FOLDER_OUTPUT: Absolute path in which all ctm files will be generated after splitting the original one.
    sys.exit(2)

[ABSOLUTE_PATH_AUDIO_FILE, ABSOLUTE_PATH_CTM_FILE, SPLIT_PATTERN_STRING, AUDIO_FOLDER_OUTPUT, CTM_FOLDER_OUTPUT] = sys.argv[1:NUM_PARAMS]
SUFFIX='-'
CTM_SUFFIX='.ctm'
AUDIO_SUFFIX='.wav'
CTM_SEP='\t'
PAD_DURATION='0.3' #in seconds, it will be added to the beggining and end of the audio file
PAD_DURATION_NUMBER=float(PAD_DURATION)
if not ABSOLUTE_PATH_CTM_FILE.endswith(CTM_SUFFIX):
    print(ABSOLUTE_PATH_CTM_FILE + " file must be a .ctm file")
    sys.exit(3)

print('++ Splitting:',os.path.basename(ABSOLUTE_PATH_CTM_FILE).replace(CTM_SUFFIX,''))

# 1. Read source CTM file
all_lines = []
with open(ABSOLUTE_PATH_CTM_FILE, 'r', encoding='utf-8') as f:
    aux_line = []
    for line in f.readlines():        
        fields = line.split()
        id_aux = fields[0]
        word_aux = fields[4]
        aux_line.append(line)
        if (SPLIT_PATTERN_STRING in word_aux):
            all_lines.append(aux_line[:])
            aux_line = []

# 2. SPLIT CTM FILES  (and keep the start/ending times)
os.makedirs(CTM_FOLDER_OUTPUT, exist_ok=True)
split_ctm_cont = 0
start_end_times = {}
DEFAULT_NO_TIME = 0
current_end_time = DEFAULT_NO_TIME
for line in all_lines:
    name_no_extension =  os.path.basename(ABSOLUTE_PATH_CTM_FILE).replace(CTM_SUFFIX,'')
    new_id = name_no_extension + SUFFIX + str(split_ctm_cont)
    file_path=os.path.join(CTM_FOLDER_OUTPUT,new_id+CTM_SUFFIX)
    with open(file_path, 'w', encoding='utf-8') as f:        
        for elem in line:
            fields = elem.split(CTM_SEP)           
            fields[0]=fields[0].replace(name_no_extension,new_id)
            fields[2]=str(round(PAD_DURATION_NUMBER+float(fields[2])-current_end_time,3))
            fields[3]=str(round(PAD_DURATION_NUMBER+float(fields[3])-current_end_time,3))
            f.write(CTM_SEP.join(fields))
    split_ctm_cont+=1
    current_end_time = float(line[-1].split(CTM_SEP)[-3])
    start_end_times[new_id] = (line[0].split(CTM_SEP)[2],current_end_time)
#####print('++ CTM files splitted:', CTM_FOLDER_OUTPUT)


os.makedirs(AUDIO_FOLDER_OUTPUT, exist_ok=True)

#print(start_end_times)
# 3. SPLIT AUDIO FILES with the start/ending times from CTM splitted files
#sox Medicijnjournaal_2016_1.wav out.wav trim 0:01 0:08 pad PAD_DURATION PAD_DURATION
for elem in start_end_times:
    aux=start_end_times[elem]
    commands = ['sox',ABSOLUTE_PATH_AUDIO_FILE,os.path.join(AUDIO_FOLDER_OUTPUT,elem+AUDIO_SUFFIX),'trim',str(aux[0]),'='+str(aux[1]),'pad',PAD_DURATION,PAD_DURATION]
    #print(elem,aux)
    #print(" ".join(commands))
    #soxi -DT AUDIO_FILE.wav
    os.system(" ".join(commands))
#####print('++ Audio files splitted:', AUDIO_FOLDER_OUTPUT)