#!/usr/bin/python
#FFXIV Macro Extractor
#Copyright Arthur Moore 2016
#BSD 3 Clause License

from __future__ import print_function
from FFXIV_settings_common import *

def read_macro(in_file):
    macro={"data": []}
    macro_sections=[]
    #There are exactly 18 sections per macro
    for i in range(0,18):
        macro_sections.append(read_section(in_file,0x73))
    macro["name"] = macro_sections[0]['data']
    macro["icon"] = macro_sections[1]['data']
    macro["key"] = macro_sections[2]['data']
    #Every macro has 15 lines
    for i in range(3,18):
        macro["data"].append(macro_sections[i]['data'])
    return macro

def write_macro(out_file,macro):
    macro_sections=[]
    for i in range(0,18):
        macro_sections.append({})
    macro_sections[0]['type'] = 'T'
    macro_sections[0]['data'] = macro["name"]
    macro_sections[1]['type'] = 'I'
    macro_sections[1]['data'] = macro["icon"]
    macro_sections[2]['type'] = 'K'
    macro_sections[2]['data'] = macro["key"]
    #Every macro has 15 lines
    for i in range(3,18):
        macro_sections[i]['type'] = 'L'
        macro_sections[i]['data'] = macro["data"][i-3]
    for i in range(0,18):
        write_section(out_file,0x73,macro_sections[i])

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

#Confirm size matches in header
check_header_size(in_file)
#Read in size of actual data
data_size = get_data_size(in_file)
#Skip to end of header / beginning of data
in_file.seek(0x11)

#Print macros while there is still valid data
while in_file.tell() < data_size:
    macro_in=read_macro(in_file)
    if(macro_in["key"] != '000'):
        print_macro(macro_in)
    write_macro(out_file,macro_in)
