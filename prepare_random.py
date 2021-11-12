#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
# Generates a list of random elements (full source path) inside train/test folders: 
# .wav and .ctm files.
'''

import sys, random, os, shutil
from pathlib import Path

if len(sys.argv) != 8:
    print(sys.argv[0] + "  Please, specify 7 args: (1) source WAV path, (2) train path, (3) test path, (4) ctm source, (5) ctm output train path, (6) ctm output test path, (7) Train percentage.")
    # python3 prepare_random.py $KALDIdir/homed_wav $KALDIdir/homed_trainset $KALDIdir/homed_testset $KALDIdir/ctmator/ref_original/ $KALDIdir/ctmator/ctm_train $KALDIdir/ctmator/ctm_wer 90
    sys.exit(2)
[SOURCE_PATH, OUTPUT_TRAIN, OUTPUT_TEST, CTM_SOURCE_PATH, CTM_TRAIN_PATH, CTM_TEST_PATH, TRAIN_PER] = sys.argv[1:8]
# Set the train set %. The test set % will be: 100-TRAIN%
TRAIN_PER = int(TRAIN_PER)

# Set 0 to put all files in the test folder
DELETE_FOLDERS = True
for folder in OUTPUT_TRAIN, OUTPUT_TEST, CTM_TRAIN_PATH, CTM_TEST_PATH:
    Path(folder).mkdir(parents=True, exist_ok=True)
    if DELETE_FOLDERS:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
############################################################################


print('\n--- 1. wav files ---')
# relative path, without SOURCE_PATH
total_elements = os.listdir(SOURCE_PATH)

len_total_elements = len(total_elements)
len_train_elements = int(round(len_total_elements * TRAIN_PER / 100))
len_test_elements = len_total_elements - len_train_elements
#print('total_elements', len_total_elements, 'len_train_elements', len_train_elements, 'len_test_elements', len_test_elements)
print('Total audio files:', len_total_elements)

# without
train_elements = random.sample(total_elements, len_train_elements)
test_elements = total_elements[:]

for x in train_elements:
    test_elements.remove(x)
#print('train_elements',len(train_elements), 'test_elements',len(test_elements) )

my_dict = {OUTPUT_TRAIN:train_elements, OUTPUT_TEST:test_elements}
for my_output in my_dict:
    #my_result=[]
    print('\tCopying', len(my_dict[my_output]), 'elements -> ', my_output)
    for fname in my_dict[my_output]:
        srcpath = os.path.join(SOURCE_PATH, fname)
        shutil.copyfile(srcpath, os.path.join(my_output,fname))
        #my_result.append(srcpath)
    #print('\n'.join(my_result))


print('\n--- 2. ctm files ---')
source_files = os.listdir(CTM_SOURCE_PATH)
print('- All ctm files:', len(source_files), 'files')

m_dict={OUTPUT_TRAIN:CTM_TRAIN_PATH, OUTPUT_TEST:CTM_TEST_PATH}
for m_path in m_dict:
    filter_files = os.listdir(m_path)
    print('-->',len(filter_files), 'files',m_path)
    for f in filter_files:   
        new_file = f.replace('.wav','.ctm')
        shutil.copyfile(os.path.join(CTM_SOURCE_PATH,new_file), os.path.join(m_dict[m_path],new_file))
    print('--> output folder (ctm)',m_dict[m_path])
print()