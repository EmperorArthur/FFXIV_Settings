#!/usr/bin/python
#FFXIV Keybind Extractor
#Copyright Arthur Moore 2016
#BSD 3 Clause License

from __future__ import print_function
from FFXIV_settings_common import *

class key_bind:
    def __init__(self, in_file = None):
        self.command = ''
        self.key1 = ''
        self.key1_modifier = ''
        self.key2 = ''
        self.key2_modifier = ''
        if(in_file):
            self.read(in_file)

    def read(self,in_file):
        self.command = section(0x73,in_file).data
        key_string = section(0x73,in_file).data
        keys = key_string.split(',')
        self.key1 = keys[0].split('.')[0]
        self.key1_modifier = keys[0].split('.')[1]
        self.key2 = keys[1].split('.')[0]
        self.key2_modifier = keys[1].split('.')[1]

    def write(self,out_file):
        command_section = section(0x73)
        command_section.type = 'T'
        command_section.data = self.command
        command_section.write(out_file)
        keys_section = section(0x73)
        keys_section.type = 'C'
        keys_section.data = self.key1 + '.' + self.key1_modifier + ',' + self.key2 + '.' + self.key2_modifier + ','
        keys_section.write(out_file)

def print_key(in_key):
    print("Command:  ",in_key.command)
    print("    key1:            ",in_key.key1)
    print("    key1_modifier:   ",in_key.key1_modifier)
    print("    key2:            ",in_key.key2)
    print("    key2_modifier:   ",in_key.key2_modifier)

in_file_name = "KEYBIND.DAT"
in_file = open(in_file_name, "rb")

#Confirm size matches in header
check_header_size(in_file)
#Read in size of actual data
data_size = get_data_size(in_file)
#Skip to end of header / beginning of data
in_file.seek(0x10)

#Print keybinds while there is still valid data
while in_file.tell() < data_size:
    print_key(key_bind(in_file))
