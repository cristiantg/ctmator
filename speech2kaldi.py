# Prepares three KALDI files: spk2utt, segments and wavscp from a audio folder

# OUTPUT_FOLDER - Ending with slash
OUTPUT_FOLDER = '/vol/tensusers3/ctejedor/lacristianmachine/opt/kaldi_nl/homed_kaldi/'
# AUDIO_FOLDER - Not ending with slash
AUDIO_FOLDER = '/vol/tensusers3/ctejedor/lacristianmachine/opt/kaldi_nl/homed_test_input'

import os
import glob

print('   - OUTPUT_FOLDER:',OUTPUT_FOLDER)
# spk2utt
file_names = {}
file_names_no_ext = []
names_segments = {}
names_paths = {}
with open(OUTPUT_FOLDER+'spk2utt', 'w') as f: 
    print('\t--> spk2utt')
    files = os.listdir(AUDIO_FOLDER)
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

with open(OUTPUT_FOLDER+'segments', 'w') as f: 
    print('\t--> segments')
    for i in sorted (names_segments):        
        duration = str(round(get_duration(file_names[names_segments[i][1]][0]),3))
        f.write(names_segments[i][0]+' '+i + ' 0.000 '+ duration + ' \n')

# wavscp.scp
with open(OUTPUT_FOLDER+'wavscp.scp', 'w') as f: 
    print('\t--> wavscp.scp')
    file_names=dict(sorted(file_names.items()))
    for i in sorted (file_names):
        f.write(file_names[i][1] +' sox '+file_names[i][0]  +' -r 16k -e signed-integer -t wav - remix - |\n')