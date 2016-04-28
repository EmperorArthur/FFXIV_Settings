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

def print_key(in_key):
    print("Command:  "           ,in_key['command'])
    print("    key1:            ",in_key['key1'])
    print("    key1_modifier:   ",in_key['key1_modifier'])
    print("    key2:            ",in_key['key2'])
    print("    key2_modifier:   ",in_key['key2_modifier'])

in_file_name = "KEYBIND.DAT"
in_file = open(in_file_name, "rb")
out_file_name = "KEYBIND_check.DAT"
out_file = open(out_file_name, "wb")

header = read_header(in_file,0x11)
write_header(out_file,header)

#Print keybinds while there is still valid data
while in_file.tell() < header['data_size']:
    keybind=read_keybind(in_file)
    print_key(keybind)
    write_keybind(out_file,keybind)

write_padding(out_file,header)
