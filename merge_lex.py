# python3 merge_lex.py lex1 lex2 combined.lex
# Merges two Kaldi lexicons into one (no repeated entries)
# If repeated entries: the second lexicon has priority.

import sys
if len(sys.argv) != 4:
    print(sys.argv[0] + "  Please, specify both lexicon files and output file (3 args)  ")
    sys.exit(2)
 
[LEX_1, LEX_2, OUT_LEX] = sys.argv[1:4]

SEP = '\t'

def get_words(PATH):
    words =  {}
    with open(PATH, 'r', encoding='utf-8') as l1:
        for line in l1.readlines():
            line = line.replace('\n','')
            (orto, trans) = line.split(SEP)
            words[orto] = trans
    return words

def combine_words(l1, l2):
    words = {}
    for i in (l1 ,l2):
        for word in i:
            #print(i[word])
            words[word] = i[word]
    return words



words_1 =  get_words(LEX_1)
print('\tLEX_1:', len(words_1), 'words')
words_2 =  get_words(LEX_2)
print('\tLEX_2:', len(words_2), 'words')
words_combined = combine_words(words_1, words_2)
#print(len(words_1), len(words_2), len(words_combined))

with open(OUT_LEX, 'w', encoding='utf-8') as f: 
    print('\t--> New file:', OUT_LEX)
    for i in sorted (words_combined):
        f.write(i + SEP + words_combined[i] + '\n')
    print('\tOUT_LEX:', len(words_combined), 'words')