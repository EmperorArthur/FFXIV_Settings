#!/usr/bin/python
#FFXIV Keybind Extractor
#Copyright Arthur Moore 2016
#BSD 3 Clause License

from __future__ import print_function
from FFXIV_settings_common import *

def read_keybind(in_file):
    keybind={}
    keybind['command'] =    read_section(in_file,0x73)['data']
    key_string =            read_section(in_file,0x73)['data']
    keys = key_string.split(',')
    keybind['key1'] = keys[0].split('.')[0]
    keybind['key1_modifier'] = keys[0].split('.')[1]
    keybind['key2'] = keys[1].split('.')[0]
    keybind['key2_modifier'] = keys[1].split('.')[1]
    return keybind

def write_keybind(out_file,keybind):
    write_section(out_file,0x73,{'type':'T','data':keybind['command']})
    data = keybind['key1'] + '.' + keybind['key1_modifier'] + ',' + keybind['key2'] + '.' + keybind['key2_modifier'] + ','
    write_section(out_file,0x73,{'type':'C','data':data})

def read_keybind_file(in_file_name):
    in_file = open(in_file_name, "rb")
    header = read_header(in_file,0x11)
    keybinds=[]
    while in_file.tell() < header['data_size']:
        keybinds.append(read_keybind(in_file))
    return (header,keybinds)

def write_keybind_file(out_file_name,(header,keybinds)):
    out_file = open(out_file_name, "wb")
    write_header(out_file,header)
    for i in keybinds:
         write_keybind(out_file,i)
    write_padding(out_file,header)

def print_keybind(in_key):
    print("Command:  "           ,in_key['command'])
    print("    key1:            ",in_key['key1'])
    print("    key1_modifier:   ",in_key['key1_modifier'])
    print("    key2:            ",in_key['key2'])
    print("    key2_modifier:   ",in_key['key2_modifier'])

#Example usage
keybind_file = read_keybind_file("KEYBIND.DAT")
write_keybind_file("KEYBIND_check.DAT",keybind_file)

for i in keybind_file[1]:
    print_keybind(i)
