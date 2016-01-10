#!/usr/bin/python
#FFXIV File XORer (for testing only)
#Copyright Arthur Moore 2015
#BSD 3 Clause License

from __future__ import print_function
from FFXIV_settings_common import *
import sys

in_file_name = sys.argv[1]
xor_encoding = int(sys.argv[2],0)

in_file = open(in_file_name, "rb")

#Get the file's size
in_file.seek(0,2)
file_size = in_file.tell()
in_file.seek(0,0)

raw_file = in_file.read(file_size)
in_file.close()
xored_file = xor(raw_file,xor_encoding)
out_file = open(in_file_name+".xored",'wb')
out_file.write(xored_file)
out_file.close()

print("File Size:   ",file_size)