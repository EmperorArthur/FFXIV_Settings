#!/usr/bin/python
#FFXIV Macro Extractor
#Copyright Arthur Moore 2016
#BSD 3 Clause License

from __future__ import print_function
from FFXIV_settings_common import *

def read_macro(in_file):
    macro={"data": []}
    #There are exactly 18 sections per macro
    macro["name"] = read_section(in_file,0x73)['data']
    macro["icon"] = read_section(in_file,0x73)['data']
    macro["key"]  = read_section(in_file,0x73)['data']
    #Every macro has 15 lines
    for i in range(0,15):
        macro["data"].append(read_section(in_file,0x73)['data'])
    return macro

def write_macro(out_file,macro):
    write_section(out_file,0x73,{'type':'T','data':macro["name"]})
    write_section(out_file,0x73,{'type':'I','data':macro["icon"]})
    write_section(out_file,0x73,{'type':'K','data':macro["key"]})
    #Every macro has 15 lines
    for i in range(0,15):
        write_section(out_file,0x73,{'type':'L','data':macro["data"][i]})

def print_macro(in_macro):
    print("Name: ",in_macro["name"])
    print("Icon: ",in_macro["icon"])
    print("Key:  ",in_macro["key"])
    print("Data (15 lines):")
    for i in in_macro["data"]:
        #Sanitize the line to ascii only characters to prevent print from choking (For python3)
        #sanitized_line = i.encode('ascii','ignore').decode('ascii')
        sanitized_line = i
        print("    ",sanitized_line)

in_file_name = "MACRO.DAT"
in_file = open(in_file_name, "rb")
out_file_name = "MACRO_check.DAT"
out_file = open(out_file_name, "wb")

header = read_header(in_file,0x11)
write_header(out_file,header)

#Print macros while there is still valid data
while in_file.tell() < header['data_size']:
    macro_in=read_macro(in_file)
    if(macro_in["key"] != '000'):
        print_macro(macro_in)
    write_macro(out_file,macro_in)

#Pad the output file with 0x00 (not xored)
out_file.write('\x00'*(header['file_size']-header['data_size']))
