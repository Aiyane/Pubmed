#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# chrN_count.py

chrM_genome = ""

with open('/home/aiyane/桌面/chrM.fa') as input_file:
    for line in input_file:
        line = line.strip().upper()
        chrM_genome = chrM_genome + line

print(len(chrM_genome))
print(chrM_genome.count("A"))
print(chrM_genome.count("G"))
print(chrM_genome.count("C"))
print(chrM_genome.count("T"))
