'''
Calculates (%) number of words of the reference transcription included in the ASR lexicon.
'''

####LEXICON_FILE = '/vol/tensusers3/ctejedor/lacristianmachine/opt/kaldi_nl/testLG_5/corpus.txt'
####LEXICON_FILE = '/vol/tensusers3/ctejedor/homed_21_simple/corpus.txt'
####LEXICON_FILE = '/vol/tensusers3/ctejedor/homed_21_cgn_simple/corpus.txt'
LEXICON_FILE = '/vol/tensusers3/ctejedor/homed_21_cgn_simple_light/corpus.txt'
LEXICON_SEP = ''
# Set LEXICON_LOWER = True if you want to convert all lexicon words to lowercase
LEXICON_LOWER = True
SOURCE_TEXT = 'sclite_output/ref.txt'
SOURCE_SEP = ' '
# Set SOURCE_LOWER = True if you want to convert all source words to lowercase
SOURCE_LOWER = False

#################################################


source_words = set([])

def read_lexicon(m_path):
    lexicon_words = set()
    with open(m_path, 'r', encoding='utf-8') as f:  
        for line in f.readlines():
            line = line.replace('\n','')
            if len(LEXICON_SEP)>0:
                fields = line.split(LEXICON_SEP)
                lexicon_words.add(fields[0].lower() if LEXICON_LOWER else fields[0])
            else:
                lexicon_words.add(line.lower() if LEXICON_LOWER else line)
    return lexicon_words

def read_source(m_path, sclite_lines=False):
    source_words = set()
    source_text_list = []
    source_text_map = {}
    with open(m_path, 'r', encoding='utf-8') as f:  
        for line in f.readlines():
            line = line.replace('\n','')
            fields = line.split(SOURCE_SEP)
            aux_id = line[line.rfind('('):]
            if sclite_lines:
                source_text_map[aux_id] = []
            for word in fields:
                aux_word = word.lower() if SOURCE_LOWER else word
                if aux_word != aux_id:
                    source_words.add(aux_word)
                    source_text_list.append(aux_word)
                    if sclite_lines:
                        source_text_map[aux_id].append(aux_word)
    return source_words, source_text_list, source_text_map

def combine_sets(set1, set2):
    return set1 | set2

def difference(set1, set2):
    return set1 - set2

def intersection(set1, set2):
    return set1.intersection(set2)

def print_lexica_coverage(source, source_list, source_map, lexica):
    print('LEXICON_FILE',LEXICON_FILE)
    print('SOURCE_TEXT',SOURCE_TEXT)    


    x = len((intersection(source, lexica)))/len(source)
    print('Lexical coverage (unique words):', str(round(x*100.0,1))+ '%')

    counter = 0
    for w in source_text_list:
        if w in lexica:
            counter +=1
    print('Lexical coverage:', str(round(counter/len(source_text_list)*100.0,1))+ '%')

    indiv_lexica = {}

    for m_aux in source_map:
        counter = 0
        aux_id = m_aux.replace('(','').replace(')','')
        indiv_lexica[aux_id] = 0
        for w in source_map[m_aux]:
            if w in lexica:
                counter +=1
        indiv_lexica[aux_id] = str(round((counter/len(source_map[m_aux]))*100.0,1))+ '%'

    for elem, v in sorted(indiv_lexica.items()):
        print('\t', elem, ';',v)



###############################################
print('\nStats:')
# 1. Read original lexicon file
original_lexicon = read_lexicon(LEXICON_FILE)
print("-> original_lexicon", len(original_lexicon))

# 2. Read source text to add new words
source_text, source_text_list, source_text_map = read_source(SOURCE_TEXT, True)
print("-> source_text", len(source_text), len(source_text_list))


# 3. Unique single set -> lexicon
combined = combine_sets(original_lexicon, source_text)
print("-> combined", len(combined))


# 4. Diff 1 - 2
diff_set = difference(original_lexicon, source_text)
print("-> difference original_lexicon-source_text", len(diff_set))


# 5. Diff 2 - 1
diff_set2 = difference(source_text, original_lexicon)
print("-> difference source_text-original_lexicon", len(diff_set2))
#print(diff_set2)

# 5. Diff 2 - 1
inter = intersection(source_text, original_lexicon)
print("-> Common words (intersection)", len(inter))

print()
# Final
print_lexica_coverage(source_text, source_text_list, source_text_map, original_lexicon)