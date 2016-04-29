#!/usr/bin/python
#FFXIV Macro Extractor
#Copyright Arthur Moore 2016
#BSD 3 Clause License

from __future__ import print_function
from FFXIV_settings_common import *

#Note \xee\80\b3 is a special '*' used by ffxiv
#Use http://xivdb.com/item/(Item # Here)/ to look up what each piece is

#Each gearset is 444 bytes
#Think each slot takes 28 bytes
def read_gearset(in_file):
    gearset = {'pieces':[]}
    gearset["number"] = xor(in_file.read(1),0x73)
    gearset["name"] = xor(in_file.read(46),0x73)    #15 chars max, but each character may be longer than 1 byte! Also, may have garbage after the first 0x00!)
    gearset["unkown"] = xor(in_file.read(5),0x73)
    #14 gear slots, counting the soul gem
    for i in range(0,14):
        raw_piece = unpack('7I',xor(in_file.read(28),0x73))
        #If a piece is HQ, remove 1,000,000 from it's #
        piece={}
        piece["equipped"] = raw_piece[0]
        piece["glamour"] = raw_piece[1]
        piece["dye_color"] = raw_piece[2]  #Note, if glamored, this is the final color you actually see
        piece["unkown"] = raw_piece[2:5]
        piece["status"] = raw_piece[6]
        gearset["pieces"].append(piece)    #Note, if missing, this is 256
    return gearset

def read_gearset_file(in_file_name):
    in_file = open(in_file_name, "rb")
    header = read_header(in_file,0x15)
    gearsets = []
    while in_file.tell() < header['data_size']:
        gearsets.append(read_gearset(in_file))
    return (header,gearsets)

def print_gearset(gearset):
    print("Number: ",gearset["number"])
    print("Name: ",gearset["name"])
    print("Unkown: ",gearset["unkown"].encode('hex'))
    for piece in gearset["pieces"]:
        print("Slot: ? Equipped:",piece["equipped"],"\tGlamored to:",piece["glamour"],"\tStatus Code:",piece["status"],"\tUnkown Vars: ",end="").expandtabs(5)
        for i in piece["unkown"]:
            print(i,end="; ")
        print("")

in_file_name="GEARSET.DAT"
(header,gearsets) = read_gearset_file(in_file_name)
print_gearset(gearsets[1])
