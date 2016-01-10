#!/usr/bin/python
#FFXIV Macro Extractor
#Copyright Arthur Moore 2016
#BSD 3 Clause License

from __future__ import print_function
from FFXIV_settings_common import *

class macro:
    def __init__(self, in_file = None):
        self.name = ''
        self.icon = 0
        self.key = 0
        self.lines = []
        if(in_file):
            self.read(in_file)

    def read(self,in_file):
        macro_sections=[]
        #There are exactly 18 sections per macro
        for i in range(0,18):
            macro_sections.append(section(0x73,in_file))
        self.name = macro_sections[0].data
        self.icon = macro_sections[1].data
        self.key = macro_sections[2].data
        #Every macro has 15 lines
        for i in range(3,18):
            self.lines.append(macro_sections[i].data)

    def write(self,out_file):
        macro_sections=[]
        for i in range(0,18):
            macro_sections.append(section(0x73))
        macro_sections[0].type = 'T'
        macro_sections[0].data = self.name
        macro_sections[1].type = 'I'
        macro_sections[1].data = self.icon
        macro_sections[2].type = 'K'
        macro_sections[2].data = self.key
        #Every macro has 15 lines
        for i in range(3,18):
            macro_sections[i].type = 'L'
            macro_sections[i].data = self.lines[i]
        for i in range(0,18):
            macro_sections[i].write(out_file)

def print_macro(in_macro):
    print("Name: ",in_macro.name)
    print("Icon: ",in_macro.icon)
    print("Key:  ",in_macro.key)
    print("Data (15 lines):")
    for i in in_macro.lines:
        #Sanitize the line to ascii only characters to prevent print from choking (For python3)
        #sanitized_line = i.encode('ascii','ignore').decode('ascii')
        sanitized_line = i
        print("    ",sanitized_line)

in_file_name = "MACRO.DAT"
in_file = open(in_file_name, "rb")

#Confirm size matches in header
check_header_size(in_file)
#Skip to end of header / begining of data
in_file.seek(0x11)

#Hardcode the number of macros (can't find it in the file anywhere)
for i in range(0,100):
    print_macro(macro(in_file))
