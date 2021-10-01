#Encodes a text file

PATH = 'example/corpus.txt'
OUTPUT_FILEPATH = 'example/corpus-reduced.txt'
OUTPUT_DICT_FILEPATH = 'example/corpus_dict-reduced.txt'
TEXT_SEPARATOR = ' '
MAX_CHAR = 0
WORD_PREFFIX = "###---"


# 1. Read source (list of sublists)
original_text = []
with open(PATH, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.replace('\n','')
        fields = line.split(TEXT_SEPARATOR)
        original_text.append(fields)

# 2. Convert source
new_dict = {}
final_text = []
global_counter = 0
for m_list in original_text:
    _list = []
    for m_text in m_list:
        processed_word = m_text
        if len(m_text) > MAX_CHAR:
            processed_word = WORD_PREFFIX + str(global_counter)
            new_dict[processed_word] = m_text
            global_counter = global_counter + 1
        _list.append(processed_word)
    final_text.append(_list)

# 3. Save output file
with open(OUTPUT_FILEPATH, 'w', encoding='utf-8') as f: 
    print('\t--> New file:', OUTPUT_FILEPATH)
    for line in final_text:
        f.write(TEXT_SEPARATOR.join(line) + '\n')

# 4. Save output dict file
with open(OUTPUT_DICT_FILEPATH, 'w', encoding='utf-8') as f: 
    print('\t--> New file:', OUTPUT_DICT_FILEPATH)
    for i in new_dict:
        f.write(i + TEXT_SEPARATOR + new_dict[i] + '\n')
    print('\t', len(new_dict),'words length > ', MAX_CHAR)