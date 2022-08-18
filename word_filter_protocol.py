#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
This script deals with teh following (->) points of the HoMed protocol v2.
1. Hesitations such as [uh] and [hmhmhm].
All word*char : keeps the left part
->2. *a --> discard *a an get the left part .
->3. *d --> word before is a dilect word ---> keep another table for the phonetic transciption.
->4. *x --> not 100% accurate
->5. *u --> sound that is not an actual word, when they say something in a funny way.
6. xxx --> <unk> whenever there are silence and noise
->7. medicat[medicatie]: keeps the left part
'''

def v2(word):
    if '*' in word:
        word = word[:word.index('*')]
    if '[' in word and len(word[:word.index('[')])>0:
        word = word[:word.index('[')]
    return word