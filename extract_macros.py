#!/usr/bin/python
#FFXIV Macro Extractor
#Copyright Arthur Moore 2015
#BSD 3 Clause License

from __future__ import print_function
from struct import *
import os
import sys

in_file_name = "MACRO.DAT"

#After a 0x11 byte header, the macro entries begin. All macro entries are XOR encoded with 0x73.

#Exclusive or each byte of a string wtih a number
#Returns the modified string
def xor(in_str,num):
    output = []
    for i in in_str:
        #This doesn't work in python3 :(
        output.append(chr(ord(i) ^ num))
    #convert output to a string
    output = ''.join(output)
    return output


#Read and unpack a section of data
class section:
    xor_value = 0x73
    def __init__(self, in_file = None):
        self.type = ''
        self.data = ''
        if(in_file):
            self.read(in_file)

    def read(self,in_file):
        header = xor(in_file.read(3),self.xor_value)
        self.type = header[0]
        size = unpack('H',header[1:3])[0]
        #Going to go ahead and lop off the null terminating byte now
        self.data= xor(in_file.read(size),self.xor_value)[0:-1]

    def write(self,out_file):
        if(len(self.type) != 1):
            raise Exception('Invalid section type!')
        header= self.type + pack('H',len(self.data))
        out_file.write(header)
        out_file.write(xor(self.data,self.xor_value))
        #Add back the null byte when writing
        out_file.write(0x00)

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
            macro_sections.append(section(in_file))
        self.name = macro_sections[0].data
        self.icon = macro_sections[1].data
        self.key = macro_sections[2].data
        #Every macro has 15 lines
        for i in range(3,18):
            self.lines.append(macro_sections[i].data)

    def write(self,out_file):
        macro_sections=[]
        for i in range(0,18):
            macro_sections.append(section())
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



in_file = open(in_file_name, "rb")

#Get the file's size
in_file.seek(0,2)
file_size = in_file.tell()
in_file.seek(0,0)

#Read in the header
header = unpack('4Ib',in_file.read(0x11))
header_file_size=header[1]
if(file_size - header_file_size != 32):
    raise Exception('Invalid header size!')

#For when not reading the header
#in_file.seek(0x11)

#Each file has 100 macros
for i in range(0,100):
    print_macro(macro(in_file))
