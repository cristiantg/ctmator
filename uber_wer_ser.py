#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# python3 uber_wer_ser.py > output.txt

# ASTLA uber script for obtaining the WER and SER of different runs.
@since 2022/06/17
'''
import os

output='/vol/tensusers4/ctejedor/lanewcristianmachine/opt/kaldi_nl/ctmator/test'
prompt_folder='/vol/tensusers4/bmolenaar/jasmin_data_prep_fix/jasmin_qG1-1/prompts/'
mt_folder='/vol/tensusers4/bmolenaar/jasmin_data_prep_fix/jasmin_qG1-1/manual_transcriptions/'

run_path='/vol/tensusers4/ctejedor/shared/bo/'

#####################################################################





os.makedirs(output, exist_ok=True)
all_runs = [
    #print("1A) _ao PROMPTS _pr")
    (os.path.join(run_path,'run001_ao'), prompt_folder, output, '_run001_pr'),
    (os.path.join(run_path,'run002_ao'), prompt_folder, output, '_run002_pr'),
    (os.path.join(run_path,'run003_ao'), prompt_folder, output, '_run003_pr'),
    (os.path.join(run_path,'run004_ao'), prompt_folder, output, '_run004_pr'),
    #print("1B) _ao MANUAL TRANSCRIPTIONS _mt")
    (os.path.join(run_path,'run001_ao'), mt_folder, output, '_run001_mt'),
    (os.path.join(run_path,'run002_ao'), mt_folder, output, '_run002_mt'),
    (os.path.join(run_path,'run003_ao'), mt_folder, output, '_run003_mt'),
    (os.path.join(run_path,'run004_ao'), mt_folder, output, '_run004_mt'),
]

for elem in all_runs:
    os.system('echo '+elem[3])
    os.system('python3 wer_ser.py '+elem[0]+' '+elem[1]+' '+elem[2]+' '+elem[3])

for file in os.listdir(output):
    if file.endswith('.sys'):
        with open(os.path.join(output,file),'r') as f:
            m_file= f.readlines()
            for line in m_file:
                if '|    Mean    |' in line:
                    print(file, line.split()[-3])

