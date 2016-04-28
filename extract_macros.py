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

def read_macro_file(in_file_name):
    in_file = open(in_file_name, "rb")
    header = read_header(in_file,0x11)
    macros=[]
    while in_file.tell() < header['data_size']:
        macros.append(read_macro(in_file))
    return (header,macros)

def write_macro_file(out_file_name,(header,macros)):
    out_file = open(out_file_name, "wb")
    write_header(out_file,header)
    for i in macros:
         write_macro(out_file,i)
    write_padding(out_file,header)

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

#Example usage
macro_file = read_macro_file("MACRO.DAT")
write_macro_file("MACRO_check.DAT",macro_file)

for i in macro_file[1]:
    if(i["key"] != '000'):
        print_macro(i)
