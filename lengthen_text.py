#Decodes a text file

'''
# Please, first run shorten_text.py, then this script
'''

DICT_FILEPATH = 'example/corpus_dict-reduced.txt'
PATH = 'example/arpa.lm'
OUTPUT_FILEPATH = 'example/arpa-final.lm'
TEXT_SEPARATOR = ' '


# 1. Read dictionary file
new_dict = {}
with open(DICT_FILEPATH, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.replace('\n','')
        fields = line.split(TEXT_SEPARATOR)
        new_dict[fields[0]] = fields[1]

# 2. Read list of sublists
final_text = []
with open(PATH, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        _list = []
        line = line.replace('\n','')
        fields = line.split(TEXT_SEPARATOR)
        for word in fields:
            if word in new_dict:
                _list.append(new_dict[word])
            else:
                _list.append(word)
        final_text.append(_list)  

# 3. Write
with open(OUTPUT_FILEPATH, 'w', encoding='utf-8') as w:
    print('\t--> New file:', OUTPUT_FILEPATH)
    for line in final_text:
        w.write(TEXT_SEPARATOR.join(line) + '\n')