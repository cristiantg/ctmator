#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
This script deals with the following points of the HoMed protocol v2.
1. Hesitations such as [uh]->[uh], [hmhm] and [hmhmhm]->[uhm] (as in CGN2)
2. All word*char : keeps the left part
-> word*a --> discard *a an get the left part .
-> word*d --> word before is a dilect word ---> keep another table for the phonetic transciption.
-> word*x --> not 100% accurate
-> word*u --> sound that is not an actual word, when they say something in a funny way.
3. word-xxx, Xxx, xxx --> only keeps xxx
4. mispronuncation[correct] (e.g., medicat[medicatie]): keeps the left part
'''

xxx='xxx'
uhm='uhm'

def v2(word):
    w_lower = word.lower()
    if xxx in w_lower:
        word = xxx
    else:
        if 'hmhm' in w_lower or 'hmhmhm' in w_lower:
            word = word.replace('hmhm', uhm).replace('hmhmhm', uhm)
        if '*' in word:
            word = word[:word.index('*')]
        if '[' in word and len(word[:word.index('[')])>0:
            word = word[:word.index('[')]

    return word.replace(u'\u200b','').replace(u'\u200c','')